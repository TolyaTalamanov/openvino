// Copyright (C) 2018-2022 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include "threading/ie_cpu_streams_executor.hpp"

#include <atomic>
#include <cassert>
#include <climits>
#include <condition_variable>
#include <memory>
#include <mutex>
#include <openvino/itt.hpp>
#include <queue>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include "ie_parallel_custom_arena.hpp"
#include "ie_system_conf.h"
#include "threading/ie_executor_manager.hpp"
#include "threading/ie_thread_affinity.hpp"
#include "threading/ie_thread_local.hpp"

using namespace openvino;

namespace InferenceEngine {
struct CPUStreamsExecutor::Impl {
    struct Stream {
#if IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO
        struct Observer : public custom::task_scheduler_observer {
            CpuSet _mask;
            int _ncpus = 0;
            int _threadBindingStep = 0;
            int _offset = 0;
            int _cpuIdxOffset = 0;
            Observer(custom::task_arena& arena,
                     CpuSet mask,
                     int ncpus,
                     const int streamId,
                     const int threadsPerStream,
                     const int threadBindingStep,
                     const int threadBindingOffset,
                     const int cpuIdxOffset = 0)
                : custom::task_scheduler_observer(arena),
                  _mask{std::move(mask)},
                  _ncpus(ncpus),
                  _threadBindingStep(threadBindingStep),
                  _offset{streamId * threadsPerStream + threadBindingOffset},
                  _cpuIdxOffset(cpuIdxOffset) {}
            void on_scheduler_entry(bool) override {
                PinThreadToVacantCore(_offset + tbb::this_task_arena::current_thread_index(),
                                      _threadBindingStep,
                                      _ncpus,
                                      _mask,
                                      _cpuIdxOffset);
            }
            void on_scheduler_exit(bool) override {
                PinCurrentThreadByMask(_ncpus, _mask);
            }
            ~Observer() override = default;
        };
#endif
        explicit Stream(Impl* impl) : _impl(impl) {
            {
                std::lock_guard<std::mutex> lock{_impl->_streamIdMutex};
                if (_impl->_streamIdQueue.empty()) {
                    _streamId = _impl->_streamId++;
                } else {
                    _streamId = _impl->_streamIdQueue.front();
                    _impl->_streamIdQueue.pop();
                }
            }
            _numaNodeId = _impl->_config._streams
                              ? _impl->_usedNumaNodes.at((_streamId % _impl->_config._streams) /
                                                         ((_impl->_config._streams + _impl->_usedNumaNodes.size() - 1) /
                                                          _impl->_usedNumaNodes.size()))
                              : _impl->_usedNumaNodes.at(_streamId % _impl->_usedNumaNodes.size());
#if IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO
            const auto concurrency = (0 == _impl->_config._threadsPerStream) ? custom::task_arena::automatic
                                                                             : _impl->_config._threadsPerStream;
            if (ThreadBindingType::HYBRID_AWARE == _impl->_config._threadBindingType) {
                if (Config::PreferredCoreType::ROUND_ROBIN != _impl->_config._threadPreferredCoreType) {
                    if (Config::PreferredCoreType::ANY == _impl->_config._threadPreferredCoreType) {
                        _taskArena.reset(new custom::task_arena{concurrency});
                    } else {
                        const auto selected_core_type =
                            Config::PreferredCoreType::BIG == _impl->_config._threadPreferredCoreType
                                ? custom::info::core_types().back()    // running on Big cores only
                                : custom::info::core_types().front();  // running on Little cores only
                        _taskArena.reset(new custom::task_arena{custom::task_arena::constraints{}
                                                                    .set_core_type(selected_core_type)
                                                                    .set_max_concurrency(concurrency)});
                    }
                } else {
                    // assigning the stream to the core type in the round-robin fashion
                    // wrapping around total_streams (i.e. how many streams all different core types can handle
                    // together)
                    const auto total_streams = _impl->total_streams_on_core_types.back().second;
                    const auto streamId_wrapped = _streamId % total_streams;
                    const auto& selected_core_type =
                        std::find_if(
                            _impl->total_streams_on_core_types.cbegin(),
                            _impl->total_streams_on_core_types.cend(),
                            [streamId_wrapped](const decltype(_impl->total_streams_on_core_types)::value_type& p) {
                                return p.second > streamId_wrapped;
                            })
                            ->first;
                    const auto max_concurrency = selected_core_type == 0 ? _impl->_config._threads_per_stream_small
                                                                         : _impl->_config._threads_per_stream_big;
                    const auto stream_id =
                        selected_core_type == 0 ? _streamId - _impl->_config._big_core_streams : _streamId;
                    const auto thread_binding_step = selected_core_type == 0 ? _impl->_config._threadBindingStep : 2;
                    // Prevent conflicts with system scheduling, so default cpu id on big core starts from 1
                    const auto cpu_idx_offset = selected_core_type == 0 ? _impl->_config._small_core_offset : 1;

                    _taskArena.reset(new custom::task_arena{max_concurrency});
                    CpuSet processMask;
                    int ncpus = 0;
                    std::tie(processMask, ncpus) = GetProcessMask();
                    if (nullptr != processMask) {
                        _observer.reset(new Observer{*_taskArena,
                                                     std::move(processMask),
                                                     ncpus,
                                                     stream_id,
                                                     max_concurrency,
                                                     thread_binding_step,
                                                     _impl->_config._threadBindingOffset,
                                                     cpu_idx_offset});
                        _observer->observe(true);
                    }
                }
            } else if (ThreadBindingType::NUMA == _impl->_config._threadBindingType) {
                _taskArena.reset(new custom::task_arena{custom::task_arena::constraints{_numaNodeId, concurrency}});
            } else if ((0 != _impl->_config._threadsPerStream) ||
                       (ThreadBindingType::CORES == _impl->_config._threadBindingType)) {
                _taskArena.reset(new custom::task_arena{concurrency});
                if (ThreadBindingType::CORES == _impl->_config._threadBindingType) {
                    CpuSet processMask;
                    int ncpus = 0;
                    std::tie(processMask, ncpus) = GetProcessMask();
                    if (nullptr != processMask) {
                        _observer.reset(new Observer{*_taskArena,
                                                     std::move(processMask),
                                                     ncpus,
                                                     _streamId,
                                                     _impl->_config._threadsPerStream,
                                                     _impl->_config._threadBindingStep,
                                                     _impl->_config._threadBindingOffset});
                        _observer->observe(true);
                    }
                }
            }
#elif IE_THREAD == IE_THREAD_OMP
            omp_set_num_threads(_impl->_config._threadsPerStream);
            if (!checkOpenMpEnvVars(false) && (ThreadBindingType::NONE != _impl->_config._threadBindingType)) {
                CpuSet processMask;
                int ncpus = 0;
                std::tie(processMask, ncpus) = GetProcessMask();
                if (nullptr != processMask) {
                    parallel_nt(_impl->_config._threadsPerStream, [&](int threadIndex, int threadsPerStream) {
                        int thrIdx = _streamId * _impl->_config._threadsPerStream + threadIndex +
                                     _impl->_config._threadBindingOffset;
                        PinThreadToVacantCore(thrIdx, _impl->_config._threadBindingStep, ncpus, processMask);
                    });
                }
            }
#elif IE_THREAD == IE_THREAD_SEQ
            if (ThreadBindingType::NUMA == _impl->_config._threadBindingType) {
                PinCurrentThreadToSocket(_numaNodeId);
            } else if (ThreadBindingType::CORES == _impl->_config._threadBindingType) {
                CpuSet processMask;
                int ncpus = 0;
                std::tie(processMask, ncpus) = GetProcessMask();
                if (nullptr != processMask) {
                    PinThreadToVacantCore(_streamId + _impl->_config._threadBindingOffset,
                                          _impl->_config._threadBindingStep,
                                          ncpus,
                                          processMask);
                }
            }
#endif
        }
        ~Stream() {
            {
                std::lock_guard<std::mutex> lock{_impl->_streamIdMutex};
                _impl->_streamIdQueue.push(_streamId);
            }
#if IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO
            if (nullptr != _observer) {
                _observer->observe(false);
            }
#endif
        }

        Impl* _impl = nullptr;
        int _streamId = 0;
        int _numaNodeId = 0;
        bool _execute = false;
        std::queue<Task> _taskQueue;
#if IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO
        std::unique_ptr<custom::task_arena> _taskArena;
        std::unique_ptr<Observer> _observer;
#endif
    };

    explicit Impl(const Config& config)
        : _config{config},
          _streams([this] {
              return std::make_shared<Impl::Stream>(this);
          }) {
        _exectorMgr = executorManager();
        auto numaNodes = getAvailableNUMANodes();
        if (_config._streams != 0) {
            std::copy_n(std::begin(numaNodes),
                        std::min(static_cast<std::size_t>(_config._streams), numaNodes.size()),
                        std::back_inserter(_usedNumaNodes));
        } else {
            _usedNumaNodes = numaNodes;
        }
#if (IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO)
        if (ThreadBindingType::HYBRID_AWARE == config._threadBindingType) {
            const auto core_types = custom::info::core_types();
            int sum = 0;
            // reversed order, so BIG cores are first
            for (auto iter = core_types.rbegin(); iter < core_types.rend(); iter++) {
                const auto& type = *iter;
                // calculating the #streams per core type
                const int num_streams_for_core_type =
                    type == 0 ? std::max(1, config._small_core_streams) : std::max(1, config._big_core_streams);
                sum += num_streams_for_core_type;
                // prefix sum, so the core type for a given stream id will be deduced just as a upper_bound
                // (notice that the map keeps the elements in the descending order, so the big cores are populated
                // first)
                total_streams_on_core_types.push_back({type, sum});
            }
        }
#endif
        for (auto streamId = 0; streamId < _config._streams; ++streamId) {
            _threads.emplace_back([this, streamId] {
                openvino::itt::threadName(_config._name + "_" + std::to_string(streamId));
                for (bool stopped = false; !stopped;) {
                    Task task;
                    {
                        std::unique_lock<std::mutex> lock(_mutex);
                        _queueCondVar.wait(lock, [&] {
                            return !_taskQueue.empty() || (stopped = _isStopped);
                        });
                        if (!_taskQueue.empty()) {
                            task = std::move(_taskQueue.front());
                            _taskQueue.pop();
                        }
                    }
                    if (task) {
                        Execute(task, *(_streams.local()));
                    }
                }
            });
        }
    }

    void Enqueue(Task task) {
        {
            std::lock_guard<std::mutex> lock(_mutex);
            _taskQueue.emplace(std::move(task));
        }
        _queueCondVar.notify_one();
    }

    void Execute(const Task& task, Stream& stream) {
#if IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO
        auto& arena = stream._taskArena;
        if (nullptr != arena) {
            arena->execute(std::move(task));
        } else {
            task();
        }
#else
        task();
#endif
    }

    void Defer(Task task) {
        auto& stream = *(_streams.local());
        stream._taskQueue.push(std::move(task));
        if (!stream._execute) {
            stream._execute = true;
            try {
                while (!stream._taskQueue.empty()) {
                    Execute(stream._taskQueue.front(), stream);
                    stream._taskQueue.pop();
                }
            } catch (...) {
            }
            stream._execute = false;
        }
    }

    Config _config;
    std::mutex _streamIdMutex;
    int _streamId = 0;
    std::queue<int> _streamIdQueue;
    std::vector<std::thread> _threads;
    std::mutex _mutex;
    std::condition_variable _queueCondVar;
    std::queue<Task> _taskQueue;
    bool _isStopped = false;
    std::vector<int> _usedNumaNodes;
    ThreadLocal<std::shared_ptr<Stream>> _streams;
#if (IE_THREAD == IE_THREAD_TBB || IE_THREAD == IE_THREAD_TBB_AUTO)
    // stream id mapping to the core type
    // stored in the reversed order (so the big cores, with the highest core_type_id value, are populated first)
    // every entry is the core type and #streams that this AND ALL EARLIER entries can handle (prefix sum)
    // (so mapping is actually just an upper_bound: core type is deduced from the entry for which the id < #streams)
    using StreamIdToCoreTypes = std::vector<std::pair<custom::core_type_id, int>>;
    StreamIdToCoreTypes total_streams_on_core_types;
#endif
    ExecutorManager::Ptr _exectorMgr;
};

int CPUStreamsExecutor::GetStreamId() {
    auto stream = _impl->_streams.local();
    return stream->_streamId;
}

int CPUStreamsExecutor::GetNumaNodeId() {
    auto stream = _impl->_streams.local();
    return stream->_numaNodeId;
}

CPUStreamsExecutor::CPUStreamsExecutor(const IStreamsExecutor::Config& config) : _impl{new Impl{config}} {}

CPUStreamsExecutor::~CPUStreamsExecutor() {
    {
        std::lock_guard<std::mutex> lock(_impl->_mutex);
        _impl->_isStopped = true;
    }
    _impl->_queueCondVar.notify_all();
    for (auto& thread : _impl->_threads) {
        if (thread.joinable()) {
            thread.join();
        }
    }
}

void CPUStreamsExecutor::Execute(Task task) {
    _impl->Defer(std::move(task));
}

void CPUStreamsExecutor::run(Task task) {
    if (0 == _impl->_config._streams) {
        _impl->Defer(std::move(task));
    } else {
        _impl->Enqueue(std::move(task));
    }
}

}  // namespace InferenceEngine
