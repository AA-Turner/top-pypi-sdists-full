import numpy as np

from downstream._auxlib._interleave import interleave


def test_interleave_two_arrays():
    """Test interleaving two non-empty arrays."""
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    expected = np.array([1, 4, 2, 5, 3, 6])
    result = interleave([arr1, arr2])
    np.testing.assert_array_equal(result, expected)


def test_interleave_three_arrays():
    """Test interleaving three non-empty arrays."""
    arr1 = np.array([7, 8])
    arr2 = np.array([9, 10])
    arr3 = np.array([11, 12])
    expected = np.array([7, 9, 11, 8, 10, 12])
    result = interleave([arr1, arr2, arr3])
    np.testing.assert_array_equal(result, expected)


def test_interleave_empty_arrays():
    """Test interleaving two empty arrays."""
    arr1 = np.array([])
    arr2 = np.array([])
    expected = np.array([])
    result = interleave([arr1, arr2])
    np.testing.assert_array_equal(result, expected)


def test_interleave_one_empty_array():
    """Test interleaving one empty array."""
    arr1 = np.array([])
    expected = np.array([])
    result = interleave([arr1])
    np.testing.assert_array_equal(result, expected)


def test_interleave_three_empty_arrays():
    """Test interleaving three empty arrays."""
    arr1 = np.array([])
    arr2 = np.array([])
    arr3 = np.array([])
    expected = np.array([])
    result = interleave([arr1, arr2, arr3])
    np.testing.assert_array_equal(result, expected)
