import numpy as np

from ._bitwise_count32_batched import bitwise_count32_batched
from ._jit import jit


@jit("uint8[:](uint64[:])", nogil=True, nopython=True)
def bitwise_count64_batched(v: np.ndarray) -> np.ndarray:
    """Numba-friendly population count function for 64-bit integers."""
    front = v.astype(np.uint32)
    back = (v >> np.uint64(32)).astype(np.uint32)
    return bitwise_count32_batched(front) + bitwise_count32_batched(back)
