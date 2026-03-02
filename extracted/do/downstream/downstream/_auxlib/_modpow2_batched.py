import numpy as np

from ._bitwise_count64_batched import bitwise_count64_batched
from ._jit import jit


@jit(nogil=True, nopython=True)
def modpow2_batched(
    dividend: np.ndarray,
    divisor: np.ndarray,
    allow_divisor_zero: bool = False,
) -> np.ndarray:
    """Perform fast mod using bitwise operations.

    Parameters
    ----------
    dividend : np.ndarray
        The dividend of the mod operation. Must be positive integers.
    divisor : np.ndarray
        The divisor of the mod operation. Must be positive integers and an even
        power of 2.
    allow_divisor_zero : bool, default False
        If True, allows divisor to be zero. In this case, the dividend is
        returned.

    Returns
    -------
    np.ndarray
        The remainder of dividing the dividends by the divisors.

    Notes
    -----
    Numba-compatible implementation.
    """
    _1 = np.asarray(1, dtype=divisor.dtype)
    # Assert divisor is a power of two
    assert (
        allow_divisor_zero
        or (
            bitwise_count64_batched(divisor.astype(np.uint64).ravel()) == _1
        ).all()
    )
    return dividend & (divisor - _1)
