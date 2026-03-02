from ._bitlen32 import bitlen32


def bit_floor32(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    mask = 1 << bitlen32(n >> 1)
    return n & mask
