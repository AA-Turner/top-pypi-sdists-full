import numpy as np
import pytest

from downstream._auxlib._modpow2_batched import modpow2_batched


def test_modpow2_batched():
    a = np.array([10, 10, 10, 15, 20, 16, 1, 3, 1023, 0])
    b = np.array([2, 4, 8, 8, 16, 16, 2, 8, 1024, 8])

    expected = np.array([0, 2, 2, 7, 4, 0, 1, 3, 1023, 0])
    np.testing.assert_array_equal(modpow2_batched(a, b), expected)


def test_modpow2_batched_allow_divisor_zero():
    a = np.array([10, 10, 10, 15, 20, 16, 1, 3, 1023, 0])
    b = np.array([2, 4, 8, 8, 16, 16, 2, 8, 1024, 0])

    with pytest.raises(AssertionError):
        modpow2_batched(a, b, allow_divisor_zero=False)

    expected = np.array([0, 2, 2, 7, 4, 0, 1, 3, 1023, 0])
    np.testing.assert_array_equal(
        modpow2_batched(a, b, allow_divisor_zero=True), expected
    )
