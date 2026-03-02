from ._bitlen32_scalar import bitlen32_scalar
from ._jit import jit


@jit(nogil=True, nopython=True)
def ctz32_scalar(x: int) -> int:
    """Count trailing zeros."""
    return bitlen32_scalar(x & -x) - 1
