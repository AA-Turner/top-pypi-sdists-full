import numpy as np


def modpow2(dividend: int, divisor: int) -> int:
    """Perform fast mod using bitwise operations.

    Parameters
    ----------
    dividend : int
        The dividend of the mod operation. Must be a positive integer.
    divisor : int
        The divisor of the mod operation. Must be a positive integer and a
        power of 2.

    Returns
    -------
    int
        The remainder of dividing the dividend by the divisor.
    """
    # Assert divisor is a power of two
    assert (
        np.min_scalar_type(divisor) == np.object_
        or (np.bitwise_count(np.asarray(divisor)) == 1).all()
    )
    return dividend & (divisor - 1)
