import numpy as np

from ._jit import jit
from ._jit_nb_or_np import nb_or_np


@jit(nogil=True, nopython=True)
def bitlen32_scalar(val: int) -> np.uint8:
    """Calculate the bit length (number of bits) needed to represent a single
    integer of numpy type.

    Parameters
    ----------
    vaal : np.{int32, int64, uint32, etc.}
        A NumPy  integers. Maximum value should be less than 2^53.

    Returns
    -------
    np.ndarray
        An array of the same shape as `arr` containing the bit lengths for each
        corresponding integer in `arr`.

    Notes
    -----
    Numba-compatible implementation.
    """
    assert val < (1 << 53)
    val1_safe = np.maximum(val + 1, val)  # +1 RE log(0), max RE overflow
    return nb_or_np.uint8(np.ceil(np.log2(val1_safe)))
