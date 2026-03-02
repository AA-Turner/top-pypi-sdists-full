import typing

import numpy as np

from ..._auxlib._bit_floor32 import bit_floor32
from ..._auxlib._bitlen32 import bitlen32
from ..._auxlib._ctz32 import ctz32


def steady_assign_storage_site_batched(
    S: typing.Union[np.ndarray, int], T: typing.Union[np.ndarray, int]
) -> np.ndarray:
    """Site selection algorithm for steady curation.

    Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : Union[np.ndarray, int]
        Buffer size. Must be a power of two, <= 2**52.
    T : Union[np.ndarray, int]
        Current logical time. Must be <= 2**52.

    Returns
    -------
    np.array
        Selected site, if any. Otherwise, S.
    """
    S, T = np.atleast_1d(S).astype(np.int64), np.atleast_1d(T).astype(np.int64)
    assert np.logical_and(S > 1, np.bitwise_count(S) == 1).all()
    # restriction <= 2 ** 52 might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    s = bitlen32(S) - 1
    t = bitlen32(T) - s  # Current epoch (or negative)
    h = ctz32(T + 1)  # Current hanoi value

    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)

    j = bit_floor32(i) - 1  # Num full-bunch segments
    B = bitlen32(j)  # Num full bunches
    k_b = (1 << B) * (s - B + 1)  # Bunch position
    w = h - t + 1  # Segment width
    assert np.where((h >= t) & (i != 0), w > 0, True).all()
    o = w * (i - j - 1)  # Within-bunch offset

    # Special case the 0th bunch...
    zeroth_bunch = i == 0
    k_b[zeroth_bunch] = 0
    o[zeroth_bunch] = 0
    w[zeroth_bunch] = np.broadcast_to(s, w.shape)[zeroth_bunch] + 1

    with np.errstate(divide="ignore"):
        p = h % w  # Within-segment offset

    # handle discard without storing for non-top n(T) hanoi value...
    return np.where(h >= t, k_b + o + p, S)


# lazy loader workaround
assign_storage_site_batched = steady_assign_storage_site_batched
