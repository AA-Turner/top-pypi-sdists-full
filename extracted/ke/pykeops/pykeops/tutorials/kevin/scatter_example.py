import torch
from pykeops.torch import LazyTensor

B, N, M, IN, OUT = (
    32,
    2000,
    200,
    8,
    8,
)  # Batch, Sample size, Sample Size, Channel in, Channel out


def keops_conv(x, y, f, A):
    """
    Pytorch version
    """
    x_i = LazyTensor(x.view(N, 1, 2))
    y_j = LazyTensor(y.view(1, M, 2))
    f_i = LazyTensor(f.view(B, N, 1, IN))
    A_LT = LazyTensor(A.view(1, 1, IN * OUT * 2))

    D_ij = x_i - y_j
    G = lambda _D: (_D.keops_tensordot(A_LT, (2, 1), (IN * OUT, 2), (0,), (1,))).sin()

    R = G(D_ij).keops_tensordot(f_i, (IN, OUT), (1, IN), (0,), (1,))
    return R.sum_reduction(axis=1)


def pytorch_conv(x, y, f, A):
    """
    Pytorch version
    """
    d = x.view(N, 1, 2) - y.view(1, M, 2)
    g = lambda _x: torch.einsum("ij, klj -> kli", A.view(IN * OUT, 2), _x).sin()
    return torch.einsum("ijkl, bik -> bjl", g(d).view(N, M, IN, OUT), f)


x = torch.randn(N, 2).cuda()
y = torch.randn(M, 2).cuda()
f = torch.randn(B, N, IN).cuda()  # f(x)
A = torch.randn(IN * OUT * 2).cuda()


res1 = keops_conv(x, y, f, A)
res2 = pytorch_conv(x, y, f, A)

print(res1.flatten()[1:50])
print(res2.flatten()[1:50])

print(
    "All goods ? " + "yes" if torch.allclose(res1, res2, rtol=1e-4, atol=1e-4) else "No"
)
