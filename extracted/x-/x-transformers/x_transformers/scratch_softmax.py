import torch
import torch.nn.functional as F

sim = torch.randn(2, 3)
sim[:, 1] = -torch.finfo(sim.dtype).max
attn = sim.softmax(dim=-2)
print("sim:\\n", sim)
print("attn:\\n", attn)
