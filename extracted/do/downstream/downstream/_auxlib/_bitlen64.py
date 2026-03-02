import numpy as np


# see https://stackoverflow.com/a/79189999/17332200
def bitlen64(arr: np.ndarray) -> np.ndarray:
    """Calculate the bit length (number of bits) needed to represent each
    integer in a 64-bit integer array.

    Parameters
    ----------
    arr : np.ndarray
        A NumPy array of 64-bit or smaller unsigned integers.

    Returns
    -------
    np.ndarray
        An array of the same shape as `arr` containing the bit lengths for each
        corresponding integer in `arr`.
    """
    _, high_exp = np.frexp(arr >> 32)
    _, low_exp = np.frexp(arr & 0xFFFFFFFF)
    exponents = np.where(high_exp, high_exp + 32, low_exp)

    return exponents
