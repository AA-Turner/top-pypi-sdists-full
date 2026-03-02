import numpy as np


# see https://stackoverflow.com/a/79189999/17332200
def bitlen32(arr: np.ndarray) -> np.ndarray:
    """Calculate the bit length (number of bits) needed to represent each
    integer for 32-bit integer arrays.

    Parameters
    ----------
    arr : np.ndarray
        A NumPy array of unsigned integers. Maximum value should be less than
        2^53.

    Returns
    -------
    np.ndarray
        An array of the same shape as `arr` containing the bit lengths for each
        corresponding integer in `arr`.

    Notes
    -----
    This function uses `np.frexp` to determine the position of the highest set
    bit in each integer, effectively computing the bit length. An assertion
    checks that the maximum value in `arr` is less than 2^53, as `np.frexp`
    handles floating-point precision up to this limit.
    """
    arr = np.asarray(arr)
    assert arr.max(initial=0) < (1 << 53)
    return np.frexp(arr)[1].astype(arr.dtype)
