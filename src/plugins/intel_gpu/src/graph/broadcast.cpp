// Copyright (C) 2018-2022 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include "broadcast_inst.h"
#include "broadcast_shape_inference.hpp"

#include "intel_gpu/runtime/error_handler.hpp"
#include "json_object.h"
#include "primitive_type_base.h"
#include <string>
#include <vector>
#include <set>

namespace cldnn {
primitive_type_id broadcast::type_id() {
    static primitive_type_base<broadcast> instance;
    return &instance;
}

layout broadcast_inst::calc_output_layout(broadcast_node const& node, kernel_impl_params const& impl_param) {
    assert(static_cast<bool>(impl_param.desc->output_data_type) == false &&
           "Output data type forcing is not supported for broadcast_node!");
    auto input_layout = impl_param.get_input_layout();
    auto desc = impl_param.typed_desc<broadcast>();

    if (!desc->target_shape.empty()) {
        std::vector<tensor::value_type> dims_converted(desc->target_shape.begin(), desc->target_shape.end());
        for (size_t i = dims_converted.size(); i < 4; i++)
            dims_converted.push_back(1);  // extend shape to 4d

        return { input_layout.data_type,
                 input_layout.format,
                 tensor(format::get_default_format(dims_converted.size()), dims_converted) };
    } else {
        return { input_layout.data_type, input_layout.format, desc->broadcast_sizes };
    }
}

template<typename ShapeType>
std::vector<layout> broadcast_inst::calc_output_layouts(broadcast_node const& /*node*/, const kernel_impl_params& impl_param) {
    auto desc = impl_param.typed_desc<broadcast>();
    auto input0_layout = impl_param.get_input_layout(0);

    auto output_type = input0_layout.data_type;
    if (impl_param.has_fused_primitives()) {
        output_type = impl_param.get_fused_output_layout().data_type;
    }


    ov::op::v3::Broadcast op;
    op.set_broadcast_spec(desc->broadcast_mode);
    bool third_input_needed = desc->broadcast_mode == ov::op::BroadcastType::EXPLICIT;
    auto target_shape = desc->target_shape;

    ShapeType pattern_shape = impl_param.input_layouts.size() == 2 ? impl_param.get_input_layout(1).get<ShapeType>()
                                                                   : ShapeType(ov::Shape{ target_shape.size() });
    std::vector<ShapeType> output_shapes = {ShapeType{}};
    std::vector<ShapeType> input_shapes = {
        input0_layout.get<ShapeType>(),
        pattern_shape
    };

    auto axes_mapping = desc->axes_mapping.to_vector();
    ShapeType axes_mapping_shape = ov::Shape{axes_mapping.size()};

    std::map<size_t, ngraph::HostTensorPtr> const_data;
    if (third_input_needed) {
        input_shapes.emplace_back(axes_mapping_shape);

        auto axes_mapping_tensor = make_host_tensor({axes_mapping_shape, data_types::i64, format::bfyx},
                                                    static_cast<void*>(axes_mapping.data()));
        const_data.emplace(2, axes_mapping_tensor);
    }

    auto& constant_mem = impl_param.memory_deps;
    if (constant_mem.count(1)) {
        auto target_shape_mem = constant_mem.at(1);
        cldnn::mem_lock<uint8_t, mem_lock_type::read> target_shape_lock(target_shape_mem, impl_param.prog.get_stream());
        const_data.emplace(1, make_host_tensor(target_shape_mem->get_layout(), target_shape_lock.data()));
        ov::op::v3::shape_infer(&op, input_shapes, output_shapes, const_data);
    } else if (impl_param.input_layouts.size() == 1) {
        // predefined pattern shape
        auto target_shape_tensor = make_host_tensor({pattern_shape, data_types::i64, format::bfyx},
                                                     static_cast<void*>(target_shape.data()));
        const_data.emplace(1, target_shape_tensor);
        ov::op::v3::shape_infer(&op, input_shapes, output_shapes, const_data);
    } else {
        // Pattern shape is set as second input. Even though the input is scalar, the shape should be propagaterd as dynamic
        auto output_rank = input_shapes[0].size();
        output_shapes[0] = ShapeType::dynamic(std::max(output_rank, static_cast<size_t>(1)));
    }

    format output_format = format::adjust_to_rank(input0_layout.format, output_shapes[0].size());

    return { layout{output_shapes[0], output_type, output_format} };
}

template std::vector<layout> broadcast_inst::calc_output_layouts<ov::PartialShape>(broadcast_node const& node, const kernel_impl_params& impl_param);

std::string broadcast_inst::to_string(broadcast_node const& node) {
    auto desc = node.get_primitive();
    auto node_info = node.desc_to_json();
    const auto& broadcast_sizes = desc->broadcast_sizes;
    const auto& broadcast_axes = desc->broadcast_axes;
    auto& input = node.input();

    std::stringstream primitive_description;
    std::stringstream ss_broadcast_axes;

    for (size_t i = 0; i < broadcast_axes.size(); ++i) {
        ss_broadcast_axes << broadcast_axes.at(i);
        i != (broadcast_axes.size() - 1) ? ss_broadcast_axes << ", " : ss_broadcast_axes << "";
    }

    json_composite broadcast_info;
    broadcast_info.add("input id", input.id());
    broadcast_info.add("broadcast_sizes", broadcast_sizes.to_string());
    broadcast_info.add("broadcast axes", ss_broadcast_axes.str());

    node_info->add("broadcast info", broadcast_info);
    node_info->dump(primitive_description);

    return primitive_description.str();
}

broadcast_inst::typed_primitive_inst(network& network, broadcast_node const& node) : parent(network, node) {
    auto input_layout = node.input().get_output_layout();
    if (input_layout.is_dynamic())
        return;
    const auto& output_sizes = argument.broadcast_sizes;

    std::vector<tensor::value_type> input_dims = input_layout.get_dims();
    size_t max_axes_num = input_layout.get_rank();

    std::vector<tensor::value_type> reordered_input_dims(max_axes_num, 0);
    std::set<uint16_t> existing;

    const auto& broadcast_axes = node.get_primitive()->broadcast_axes;
    size_t broadcast_axes_size = broadcast_axes.size();
    size_t index = 0;
    size_t input_index = broadcast_axes_size;

    OPENVINO_ASSERT(broadcast_axes_size >= 0 && broadcast_axes_size <= max_axes_num,
                    "Incorrect parameters configuration: broadcast_axes size should be less or equal ", std::to_string(max_axes_num), ".");
    for (size_t i = 0; i < broadcast_axes_size; ++i) {
        if (broadcast_axes.at(i) >= max_axes_num) {
            CLDNN_ERROR_MESSAGE(
                node.id(),
                "Incorrect parameters configuration: broadcast_axes index should be within broadcast_sizes range.");
        }
        if (existing.find(broadcast_axes.at(i)) != existing.end()) {
            CLDNN_ERROR_MESSAGE(
                node.id(),
                "Incorrect parameters configuration: Duplicate axes numbers was found in broadcast_axes.");
        }
        existing.insert(broadcast_axes.at(i));
    }
    for (size_t i = 0; i < input_index; ++i) {
        CLDNN_ERROR_NOT_EQUAL(node.id(),
                              "Input size on dimension number " + std::to_string(i),
                              input_dims.at(i),
                              "",
                              1,
                              "Must be equal 1.");
    }
    // bfyx, bfzyx format
    for (size_t i = 0; i < max_axes_num; ++i) {
        if (std::find(broadcast_axes.begin(), broadcast_axes.end(), i) != broadcast_axes.end()) {
            reordered_input_dims.at(i) = input_dims.at(index);
            ++index;
        } else {
            reordered_input_dims.at(i) = input_dims.at(input_index);
            ++input_index;
        }
    }
    tensor input_sizes_to_compare = tensor(format::get_default_format(reordered_input_dims.size()), reordered_input_dims);

    CLDNN_ERROR_TENSOR_SIZES_NOT_DIVIDABLE(node.id(),
                                           "Broadcast sizes",
                                           output_sizes,
                                           "input sizes",
                                           input_sizes_to_compare,
                                           "Invalid broadcast size: not dividable by input size");
}
}  // namespace cldnn
