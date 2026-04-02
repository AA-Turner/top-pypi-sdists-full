import numpy as np
from pykeops.numpy import Genred

# pykeops.clean_pykeops()


M, axis = 15, 1

############################################

dimfa1 = (3, 3, 3, 3)

einsum_str1 = "adea -> ed"

a1 = np.random.rand(M, *dimfa1)
gamma_py1 = np.zeros((M, 9))
for i in range(M):
    gamma_py1[i, :] = np.einsum(einsum_str1, a1[i, :]).flatten()

from pykeops.numpy import LazyTensor

A = LazyTensor(a1.reshape(M, 1, -1))

Alias1 = [f"A = Vi(0, {np.array(dimfa1).prod()})"]
Formula1 = f"Trace(A, {dimfa1}, [0], [3], permute=[1,0])"

myconv1 = Genred(Formula1, Alias1, reduction_op="Sum", axis=axis)
gamma_keops1 = myconv1(a1.reshape(M, -1))


def test_internal_contraction_permuted():
    assert np.allclose(gamma_py1, gamma_keops1)


############################################


dimfa2 = (3, 3, 3, 3)

einsum_str2 = "aade -> de"

a2 = np.random.rand(M, *dimfa2)
gamma_py2 = np.zeros((M, 9))
for i in range(M):
    gamma_py2[i, :] = np.einsum(einsum_str2, a2[i, :]).flatten()

from pykeops.numpy import LazyTensor

A2 = LazyTensor(a2.reshape(M, 1, -1))

Alias2 = [f"A2 = Vi(0, {np.array(dimfa2).prod()})"]
Formula2 = f"Trace(A2, {dimfa2}, [0], [1])"

myconv2 = Genred(Formula2, Alias2, reduction_op="Sum", axis=axis)
gamma_keops2 = myconv2(a2.reshape(M, -1))


def test_internal_contraction():
    assert np.allclose(gamma_py2, gamma_keops2)


############################################


dimfa3 = (3, 3, 3, 3)

einsum_str3 = "aadd"

a3 = np.random.rand(M, *dimfa3)
gamma_py3 = np.zeros((M, 1))
for i in range(M):
    gamma_py3[i, :] = np.einsum(einsum_str3, a3[i, :]).flatten()

from pykeops.numpy import LazyTensor

A3 = LazyTensor(a3.reshape(M, 1, -1))

Alias3 = [f"A3 = Vi(0, {np.array(dimfa3).prod()})"]
Formula3 = f"Trace(A3, {dimfa3}, [0, 2], [1, 3])"

myconv3 = Genred(Formula3, Alias3, reduction_op="Sum", axis=axis)
gamma_keops3 = myconv3(a3.reshape(M, -1))


def test_full_internal_contraction():
    assert np.allclose(gamma_py3, gamma_keops3)
