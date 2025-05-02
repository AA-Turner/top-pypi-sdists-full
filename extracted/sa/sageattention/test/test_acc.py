import os
import torch, time
import pickle
import sageattention
import torch.nn.functional as F
torch.backends.cuda.enable_mem_efficient_sdp(False)

B, H, S, D  = 4, 32, 1630, 64
is_causal = False
dtype = torch.float16

# with open("./24_q_tensor.pkl", "rb") as f:
#     q = pickle.load(f).to('cuda').to(torch.float16).contiguous()
# with open("./24_k_tensor.pkl", "rb") as f:
#     k = pickle.load(f).to('cuda').to(torch.float16).contiguous()
# with open("./24_v_tensor.pkl", "rb") as f:
#     v = pickle.load(f).to('cuda').to(torch.float16).contiguous()

q = (torch.randn((B, H, S, D), dtype=dtype, device="cuda"))
k = torch.randn((B, H, S, D), dtype=dtype, device="cuda") + torch.randn((B, H, S, D), dtype=dtype, device="cuda") * 200 * (torch.randn((B, H, S, D), dtype=dtype, device="cuda") > 1.5)
v = (torch.randn((B, H, S, D), dtype=dtype, device="cuda"))

def flops_test(is_causal):
    for _ in range(20):
        sageattention.sageattn(q,k,v,is_causal=is_causal)
    torch.cuda.synchronize()
    _st = time.perf_counter()
    for _ in range(100):
        sageattention.sageattn(q,k,v,is_causal=is_causal)
    torch.cuda.synchronize()
    end_time = time.perf_counter()
    latency = (end_time - _st) / 100
    FLOPS = B * H * S * S * D * 4 / latency / 1e12
    if is_causal:
        FLOPS/=2
    return FLOPS

import torch.nn.functional as F
def precision_metric(quant_o, fa2_o): 
        x, xx = quant_o.float(), fa2_o.float() 
        sim = F.cosine_similarity(x.reshape(1, -1), xx.reshape(1, -1)).item()
        l1 =   ( (x - xx).abs().sum() / xx.abs().sum() ).item()
        rmse = torch.sqrt(torch.mean((x -xx) ** 2)).item()
        print(f'Cossim: {sim:.6f}, L1: {l1:.6f}, RMSE:{rmse:.6f}\n')


def test_acc(is_causal):
    torch_stand = torch.nn.functional.scaled_dot_product_attention(q, k, v,is_causal=is_causal)
    quant_o = sageattention.sageattn(q,k,v,is_causal=is_causal)
    precision_metric(quant_o, torch_stand)

if __name__ == "__main__":
    test_acc(is_causal)
    FLOPS = flops_test(is_causal)
    print(FLOPS)