from transformers import AutoTokenizer

from auto_gptq import AutoGPTQForCausalLM


tokenizer = AutoTokenizer.from_pretrained("TheBloke/Llama-2-13B-chat-GPTQ")
model = AutoGPTQForCausalLM.from_quantized("TheBloke/Llama-2-13B-chat-GPTQ", use_marlin=True, device="cuda:0")

prompt = "Is quantization a good compression technique?"

inp = tokenizer(prompt, return_tensors="pt").to("cuda:0")

res = model.generate(**inp)
print(tokenizer.decode(res[0]))
