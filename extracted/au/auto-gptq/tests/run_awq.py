import torch
from transformers import AutoTokenizer

from auto_gptq import AutoGPTQForCausalLM


tokenizer = AutoTokenizer.from_pretrained("TheBloke/Llama-2-13B-chat-AWQ")
model = AutoGPTQForCausalLM.from_quantized("TheBloke/Llama-2-13B-chat-AWQ", torch_dtype=torch.float16, device="cuda:0")

prompt = "Is quantization a good compression technique?"

inp = tokenizer(prompt, return_tensors="pt").to("cuda:0")

res = model.generate(**inp, max_new_tokens=200)
print(tokenizer.decode(res[0]))
