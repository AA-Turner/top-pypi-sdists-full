import numpy as np

from ._bitlen32_batched import bitlen32_batched
from ._jit import jit


@jit(nogil=True, nopython=True)
def bit_floor32_batched(n: np.ndarray) -> np.ndarray:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    mask = 1 << bitlen32_batched(n >> 1)
    return n & mask
