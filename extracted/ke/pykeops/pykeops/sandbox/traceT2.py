import torch
from pykeops.torch import Genred
import pykeops

pykeops.clean_pykeops()


M, axis = 1, 1

############################################

dimfa1 = (3, 3, 3)

einsum_str1 = "aak -> k"

a1 = torch.rand(M, *dimfa1, requires_grad=True)
gamma_py1 = torch.zeros((M, 3))
for i in range(M):
    gamma_py1[i, :] = torch.einsum(einsum_str1, a1[i, :]).flatten()

Alias1 = [f"A = Vi(0, {torch.tensor(dimfa1).prod()})"]
Formula1 = f"Trace(A, {dimfa1}, [0], [1])"

a11 = a1.clone()
# myconv1 = Genred(Formula1, Alias1, reduction_op="Sum", axis=axis)
# gamma_keops1 = myconv1(a11.reshape(M, -1))

# print(torch.allclose(gamma_py1, gamma_keops1))
# assert torch.allclose(gamma_py1, gamma_keops1)

Dgamma_py1 = torch.autograd.grad(gamma_py1, [a1], gamma_py1)[0]  # M,3,3,3
# Dgamma_keops1 = torch.autograd.grad(gamma_keops1, [a11], gamma_keops1)[0]
print(Dgamma_py1)
# print(Dgamma_keops1)

# assert torch.allclose(Dgamma_py1, Dgamma_keops1)

############################################

dimfa2 = (3,)

a2 = gamma_py1.clone()

Alias2 = [f"A = Vi(0, {torch.tensor(dimfa2).prod()})"]
Formula2 = f"TraceT(A, {dimfa2}, [0, 1], [3, 3])"

myconv2 = Genred(Formula2, Alias2, reduction_op="Sum", axis=axis)
gamma_keops2 = myconv2(a2.reshape(M, -1))

print(gamma_keops2)
print(Dgamma_py1.reshape(M, -1))

# assert torch.allclose(Dgamma_py1.reshape(M, -1), gamma_keops2)
