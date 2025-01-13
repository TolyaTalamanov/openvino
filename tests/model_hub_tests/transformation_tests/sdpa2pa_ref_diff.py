# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

nodes_to_compare = ("ScaledDotProductAttention", "PagedAttentionExtension", "Parameter", "ReadValue", "Assign")

ref_diff_map = {
	"hf-internal-testing/tiny-random-LlamaForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-CohereForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-GPTJForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 13,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-GPTNeoXForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 13,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-MistralForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-CodeGenForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 13,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/Mixtral-tiny" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-GPTBigCodeForCausalLM" : {
		"Assign" : -5,
		"PagedAttentionExtension" : 5,
		"Parameter" : 13,
		"ReadValue" : -5,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-Starcoder2ForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-BloomForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 14,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-gpt2" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 13,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-BlenderbotForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 8,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-PegasusForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 8,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-PhiForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-MptForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 14,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-StableLmForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-PersimmonForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-FalconForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-tiny-model-private/tiny-random-OPTForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 14,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"katuni4ka/tiny-random-xverse" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-baichuan2-13b" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-qwen" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-aquilachat" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-aquila2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-qwen1.5-moe" : {
		"Assign" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 11,
		"ReadValue" : -8,
		"ScaledDotProductAttention" : -4,
	},
	"katuni4ka/tiny-random-codegen2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-olmo-hf" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-baichuan2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-jais" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-internlm" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-internlm2" : {
		"Assign" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 11,
		"ReadValue" : -8,
		"ScaledDotProductAttention" : -4,
	},
	"katuni4ka/tiny-random-minicpm" : {
		"Assign" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 11,
		"ReadValue" : -8,
		"ScaledDotProductAttention" : -4,
	},
	"katuni4ka/tiny-random-falcon-40b" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-dbrx" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"fxmarty/tiny-random-GemmaForCausalLM" : {
		"Assign" : -2,
		"PagedAttentionExtension" : 1,
		"Parameter" : 5,
		"ReadValue" : -2,
		"ScaledDotProductAttention" : -1,
	},
	"fxmarty/tiny-dummy-qwen2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"fxmarty/really-tiny-falcon-testing" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"Xenova/tiny-random-Phi3ForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"facebook/opt-125m" : {
		"Assign" : -24,
		"PagedAttentionExtension" : 12,
		"Parameter" : 28,
		"ReadValue" : -24,
		"ScaledDotProductAttention" : -12,
	},
	"facebook/opt-350m" : {
		"Assign" : -48,
		"PagedAttentionExtension" : 24,
		"Parameter" : 52,
		"ReadValue" : -48,
		"ScaledDotProductAttention" : -24,
	},
	"katuni4ka/tiny-random-chatglm2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-glm4" : {
		"Assign" : -12,
		"PagedAttentionExtension" : 6,
		"Parameter" : 15,
		"ReadValue" : -12,
		"ScaledDotProductAttention" : -6,
	},
	"katuni4ka/tiny-random-llava-next" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-minicpmv-2_6" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-llava" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 7,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	# "katuni4ka/tiny-random-nanollava" : {
	# 	"Assign" : -4,
	# 	"PagedAttentionExtension" : 2,
	# 	"Parameter" : 7,
	# 	"ReadValue" : -4,
	# 	"ScaledDotProductAttention" : -2,
	# },
    "hf-internal-testing/tiny-random-GPTNeoForCausalLM" : {
		"ScaledDotProductAttention" : -4,
		"ReadValue" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 11,
		"Assign" : -8,
    }
}

ref_diff_map_cache_eviction = {
	"hf-internal-testing/tiny-random-LlamaForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-CohereForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-GPTJForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 28,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-GPTNeoXForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 28,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-MistralForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-CodeGenForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 28,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/Mixtral-tiny" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-GPTBigCodeForCausalLM" : {
		"Assign" : -5,
		"PagedAttentionExtension" : 5,
		"Parameter" : 28,
		"ReadValue" : -5,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-Starcoder2ForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-BloomForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 29,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-gpt2" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 28,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-BlenderbotForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 14,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-PegasusForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 14,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-PhiForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-MptForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 29,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"hf-internal-testing/tiny-random-StableLmForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-PersimmonForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-internal-testing/tiny-random-FalconForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"hf-tiny-model-private/tiny-random-OPTForCausalLM" : {
		"Assign" : -10,
		"PagedAttentionExtension" : 5,
		"Parameter" : 29,
		"ReadValue" : -10,
		"ScaledDotProductAttention" : -5,
	},
	"katuni4ka/tiny-random-xverse" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-baichuan2-13b" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-qwen" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-aquilachat" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-aquila2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-qwen1.5-moe" : {
		"Assign" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 23,
		"ReadValue" : -8,
		"ScaledDotProductAttention" : -4,
	},
	"katuni4ka/tiny-random-codegen2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-olmo-hf" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-baichuan2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-jais" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-internlm" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-internlm2" : {
		"Assign" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 23,
		"ReadValue" : -8,
		"ScaledDotProductAttention" : -4,
	},
	"katuni4ka/tiny-random-minicpm" : {
		"Assign" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 23,
		"ReadValue" : -8,
		"ScaledDotProductAttention" : -4,
	},
	"katuni4ka/tiny-random-falcon-40b" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-dbrx" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"fxmarty/tiny-random-GemmaForCausalLM" : {
		"Assign" : -2,
		"PagedAttentionExtension" : 1,
		"Parameter" : 8,
		"ReadValue" : -2,
		"ScaledDotProductAttention" : -1,
	},
	"fxmarty/tiny-dummy-qwen2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"fxmarty/really-tiny-falcon-testing" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"Xenova/tiny-random-Phi3ForCausalLM" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"facebook/opt-125m" : {
		"Assign" : -24,
		"PagedAttentionExtension" : 12,
		"Parameter" : 64,
		"ReadValue" : -24,
		"ScaledDotProductAttention" : -12,
	},
	"facebook/opt-350m" : {
		"Assign" : -48,
		"PagedAttentionExtension" : 24,
		"Parameter" : 124,
		"ReadValue" : -48,
		"ScaledDotProductAttention" : -24,
	},
	"katuni4ka/tiny-random-chatglm2" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-glm4" : {
		"Assign" : -12,
		"PagedAttentionExtension" : 6,
		"Parameter" : 33,
		"ReadValue" : -12,
		"ScaledDotProductAttention" : -6,
	},
	"katuni4ka/tiny-random-llava-next" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-minicpmv-2_6" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
	"katuni4ka/tiny-random-llava" : {
		"Assign" : -4,
		"PagedAttentionExtension" : 2,
		"Parameter" : 13,
		"ReadValue" : -4,
		"ScaledDotProductAttention" : -2,
	},
    # "katuni4ka/tiny-random-nanollava" : {
	# 	"Assign" : -4,
	# 	"PagedAttentionExtension" : 2,
	# 	"Parameter" : 13,
	# 	"ReadValue" : -4,
	# 	"ScaledDotProductAttention" : -2,
	# },

    "hf-internal-testing/tiny-random-GPTNeoForCausalLM" : {
		"ScaledDotProductAttention" : -4,
		"ReadValue" : -8,
		"PagedAttentionExtension" : 4,
		"Parameter" : 23,
		"Assign" : -8,
    }
}
