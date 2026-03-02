import numpy as np

from downstream._auxlib._modpow2 import modpow2


def test_modpow2():
    assert modpow2(10, 2) == 0  # 10 % 2 = 0
    assert modpow2(10, 4) == 2  # 10 % 4 = 2
    assert modpow2(10, 8) == 2  # 10 % 8 = 2
    assert modpow2(15, 8) == 7  # 15 % 8 = 7
    assert modpow2(20, 16) == 4  # 20 % 16 = 4
    assert modpow2(16, 16) == 0  # 16 % 16 = 0
    assert modpow2(1, 2) == 1  # 1 % 2 = 1
    assert modpow2(3, 8) == 3  # 3 % 8 = 3
    assert modpow2(1023, 1024) == 1023  # 1023 % 1024 = 1023
    assert modpow2(0, 8) == 0  # 0 % 8 = 0


def test_modpow2_numpy():
    a = np.array([10, 10, 10, 15, 20, 16, 1, 3, 1023, 0])
    b = np.array([2, 4, 8, 8, 16, 16, 2, 8, 1024, 8])

    expected = np.array([0, 2, 2, 7, 4, 0, 1, 3, 1023, 0])
    np.testing.assert_array_equal(modpow2(a, b), expected)
