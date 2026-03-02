import numpy as np

from ._jit import jit


# adapted from https://stackoverflow.com/a/71100473/17332200
@jit("uint8[:](uint32[:])", nogil=True, nopython=True)
def bitwise_count32_batched(v: np.ndarray) -> np.ndarray:
    """Numba-friendly population count function for 32-bit integers."""
    v = v - ((v >> 1) & 0x55555555)
    v = (v & 0x33333333) + ((v >> 2) & 0x33333333)
    c = ((v + (v >> 4) & 0xF0F0F0F) * 0x1010101) >> 24
    return c.astype(np.uint8)
