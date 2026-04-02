import torch
from pykeops.torch import LazyTensor, Genred

device = "cuda" if torch.cuda.is_available() else "cpu"

# No broadcasting : WORKS
"""
B, M, N = 3, 5, 4
_x = torch.rand(B, M, 1, 1, device=device)
x = LazyTensor(_x)
_p = torch.rand(B, 1, 1, 1, device=device)
p = LazyTensor(_p)


print(
    torch.allclose(
        (x * p).sum(dim=2).reshape(B, M),
        (_p * _x).sum(dim=2).reshape(B, M)
    )
)
"""

# Broadcasting : DOES NOT WORK
B, M, N = 3, 5, 4
_x = torch.rand(1, M, 1, 1, device=device)
x = LazyTensor(_x)
_p = torch.rand(B, 1, 1, 1, device=device)
p = LazyTensor(_p)


print((p * x).sum(dim=2).reshape(B, M))
print((_p * _x).sum(dim=2).reshape(B, M))

import torch
from pykeops.numpy import Vi, Vj

device = "cuda" if torch.cuda.is_available() else "cpu"


M, N = 1000, 1001

# A standard LazyTensor
X = LazyTensor(torch.rand(M, 1, 1, device=device))
Y = LazyTensor(torch.rand(1, N, 1, device=device))
DX = (X - Y).square()

# An indices based LazyTensor
I = LazyTensor(torch.arange(M, device=device).type(torch.float32).reshape(M, 1, 1))
J = LazyTensor(torch.arange(N, device=device).type(torch.float32).reshape(1, N, 1))
C_IJ = (I - J).abs()

# reduce the LazyTensors
print((DX * C_IJ).sum(1))
