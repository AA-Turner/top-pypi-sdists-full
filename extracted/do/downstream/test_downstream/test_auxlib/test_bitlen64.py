import numpy as np

from downstream._auxlib._bitlen64 import bitlen64


def test_bitlen64_empty():
    arr = np.array([], dtype=np.int64)
    expected = np.array([], dtype=np.int64)
    np.testing.assert_array_equal(bitlen64(arr), expected)


def test_bitlen64_zeros():
    arr = np.array([0, 0, 0])
    expected = np.array([0, 0, 0])
    np.testing.assert_array_equal(bitlen64(arr), expected)


def test_bitlen64_small_positive_integers():
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    expected = np.array([1, 2, 2, 3, 3, 3, 3, 4])
    np.testing.assert_array_equal(bitlen64(arr), expected)

    arr = np.array([1023, 1024, 1025])
    expected = np.array([10, 11, 11])
    np.testing.assert_array_equal(bitlen64(arr), expected)


def test_bitlen64_large_integers():
    arr = np.array([2**63 - 1, 2**63, 2**64 - 1], dtype=np.uint64)
    expected = np.array([63, 64, 64])
    np.testing.assert_array_equal(bitlen64(arr), expected)

    arr = np.array([2**63 - 1, 2**62, 2**61], dtype=np.int64)
    expected = np.array([63, 63, 62])
    np.testing.assert_array_equal(bitlen64(arr), expected)


def test_bitlen64_mixed():
    arr = np.array([0, 1, 0, 2, 0, 4])
    expected = np.array([0, 1, 0, 2, 0, 3])
    np.testing.assert_array_equal(bitlen64(arr), expected)
