# from transformers import AutoModelForCausalLM, PreTrainedTokenizerFast, GenerationConfig
# import torch
# from transformers.distributed import DistributedConfig

# torch.manual_seed(0)
# model_path = "gpt-oss-20b-multilingual-reasoner"
# tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path, padding_side="left")

# generation_config = GenerationConfig(
#     max_new_tokens=32,
#     eos_token_id=tokenizer.eos_token_id,
#     pad_token_id=tokenizer.pad_token_id,
#     use_cache=False,
#     num_blocks=1024 * 8,
#     block_size=64,
#     use_cuda_graph=True,
#     do_sample=True,
#     max_batch_tokens=512,  # Maximum number of tokens to process in a single batch
# )

# device_map = {
#     "tp_plan": "auto",
# }
# model = AutoModelForCausalLM.from_pretrained(
#     model_path,
#     attn_implementation="paged_attention|ft-hf-o-c/vllm-flash-attn3:flash_attn_varlen_func",
#     torch_dtype=torch.bfloat16,
#     use_kernels=False,
#     generation_config=generation_config,
#     **device_map,
# )

# # model.forward = torch.compile(model.forward, mode="max-autotune-no-cudagraphs")
# model.eval()

# inputs = tokenizer.apply_chat_template(
#     [[
#         {
#             "role": "user",
#             "content": "What is the capital of France?",
#         },
#     ]],
#     add_generation_prompt=True,
#     return_tensors="pt",
# )
# batch_outputs = model.generate(inputs=inputs, generation_config=generation_config)
# print(tokenizer.decode(batch_outputs["batch_req_0"].generated_tokens))





from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
from transformers.distributed import DistributedConfig

torch.manual_seed(0)  # For reproducibility

model_path = "gpt-oss-20b-multilingual-reasoner"
tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side="left")
generation_config = GenerationConfig(max_new_tokens=2048, do_sample=False, eos_token_id=tokenizer.eos_token_id)

device_map = {
    "distributed_config": DistributedConfig(enable_expert_parallel=True),
    "tp_plan": "auto",
}

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    generation_config=generation_config,
    attn_implementation="paged-attention|ft-hf-o-c/vllm-flash-attn3",
    **device_map,
)

messages = [
    # [{"role": "system", "content": f"reasoning language: French"}, {"role": "user", "content": "What is the capital of France?"}],
    # [{"role": "system", "content": f"reasoning language: German"}, {"role": "user", "content": "What is the capital of Canada?"}],
    # [{"role": "system", "content": f"reasoning language: Chinese"}, {"role": "user", "content": "What is the capital of Germany?"}],
    [{"role": "system", "content": f"reasoning language: Hindi"}, {"role": "user", "content": "What is the capital of Japan?"}],
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    padding=True,
    padding_side="left",
).to("cuda")
outputs = model.generate(inputs, generation_config=generation_config)


print(tokenizer.batch_decode(outputs)[0])
print("--------------------------")
# print(tokenizer.batch_decode(outputs)[1])
# print("--------------------------")
# print(tokenizer.batch_decode(outputs)[2])
# print("--------------------------")
# print(tokenizer.batch_decode(outputs)[3])

import torch.distributed as dist
if dist.is_initialized():
    dist.destroy_process_group()