import numpy as np


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert (np.asarray(x) > 0).all()
    return (x & -x).bit_length() - 1
