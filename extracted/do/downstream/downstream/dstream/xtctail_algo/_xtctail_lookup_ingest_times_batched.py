import warnings

import numpy as np

from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._ctz32_batched import ctz32_batched
from ..._auxlib._modpow2_batched import modpow2_batched
from ..compressing_algo._compressing_lookup_ingest_times_batched import (
    compressing_lookup_ingest_times_batched,
)


def xtctail_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = False,
) -> np.ndarray:
    """Ingest time lookup algorithm for xtctail curation.

    Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two greater than 4.
    T : np.ndarray
        One-dimensional array of current logical times.
    parallel : bool, default False
        Should numba be applied to parallelize operations?

    Returns
    -------
    np.ndarray
        Ingest time of stored items at buffer sites in index order.

        Two-dimensional array. Each row corresponds to an entry in T. Contains
        S columns, each corresponding to buffer sites.

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: xtctail circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    T = np.ascontiguousarray(T)  # wtf... why is this needed?
    # ... otherwise, tiltedxtc unit tests fail for S = 8
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T
    assert np.asarray(np.asarray(T) < (1 << 63)).all()
    _1, _2 = np.asarray(1, dtype=np.uint64), np.asarray(2, dtype=np.uint64)
    T = T.astype(np.uint64)
    T_ = T[:, None]  # make broadcastable with (T, S)
    S_ = np.asarray(S, dtype=np.uint64)

    if parallel:
        warnings.warn(
            "parallel xtctail lookup not yet implemented, "
            "falling back to serial implementation",
        )

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    epoch = bitlen32_batched(T).astype(np.uint64)

    # res1: compressing sites
    # -----------------------
    res1 = compressing_lookup_ingest_times_batched(
        S_, np.maximum(S_, epoch), parallel=parallel
    )
    res1 = (
        T_
        - modpow2_batched(
            T_ - (_1 << res1), _2 << res1, allow_divisor_zero=True
        )
        - _1
    )

    # res2: initialized sites
    # -----------------------
    S_indices = np.arange(S, dtype=np.uint64)[None, :]  # shape becomes (1, S)

    x = S_indices + 1
    x -= np.minimum(int(S).bit_length(), x).astype(x.dtype)  # floor subtract S
    # see https://oeis.org/A057716
    ansatz_p1 = x + bitlen32_batched(x + bitlen32_batched(x))
    assert (ansatz_p1 < T_ + 1).all()
    ansatz_h = ctz32_batched(ansatz_p1).astype(np.uint64)  # Current hv
    ansatz_h_offset = (_1 << ansatz_h) - _1
    ansatz_h_cadence = _2 << ansatz_h
    res2 = (
        _2 * ansatz_h_offset
        + ((S_ - ansatz_h_offset - _1) >> (ansatz_h + _1)) * ansatz_h_cadence
        + _1
    ).astype(np.uint64)
    res2 = np.subtract(res2, np.minimum(res2, ansatz_p1.astype(np.uint64)))

    # combine res1 and res2
    # ---------------------
    return np.where(
        S_indices < epoch[:, None],
        res1,
        res2,
    )


# lazy loader workaround
lookup_ingest_times_batched = xtctail_lookup_ingest_times_batched
