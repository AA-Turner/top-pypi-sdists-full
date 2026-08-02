import autogptq_marlin_cuda
import torch


A = torch.rand(7, 768, dtype=torch.float16).to("cuda")

B = torch.randint(high=300, size=(48, 1536)).to("cuda").to(torch.int32)
C = torch.rand(7, 768, dtype=torch.float16).to("cuda")
s = torch.rand(6, 768, dtype=torch.float16).to("cuda")

workspace = torch.tensor([0, 1, 2, 3, 4, 5]).to(torch.int32).to("cuda")

thread_k = -1
thread_n = -1
sms = -1

autogptq_marlin_cuda.mul(A, B, C, s, workspace, thread_k, thread_n, sms)
