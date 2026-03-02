import warnings

import numpy as np

from ..._auxlib._bitlen32_batched import bitlen32_batched
from ._compressing_assign_storage_site_batched import (
    compressing_assign_storage_site_batched,
)


def compressing_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = False,
) -> np.ndarray:
    """Ingest time lookup algorithm for compressing curation.

    Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : int
        Buffer size. Must be a positive integer.
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
    John C. Gunther. 2014. Algorithm 938: Compressing circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if parallel:
        warnings.warn(
            "parallel compressing lookup not yet implemented, "
            "falling back to serial implementation",
        )

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    T_indices = np.arange(T.size)
    res = np.empty((T.size, S), dtype=np.uint64)

    if S % 2 == 0:  # even S: site 0 special, M = S-1
        si = bitlen32_batched((T - 2) // (S - 1))
        si_ = np.asarray(1, dtype=np.int64) << si
        assert si_.all()

        for Tbar in (0,):
            assert np.all(Tbar < T)
            k = compressing_assign_storage_site_batched(S, Tbar)
            assert np.all(k < S)
            res[T_indices, k] = Tbar

        Tbar = np.ones_like(si, dtype=np.int64)
        step = si_.astype(np.int64, copy=True)
        lb, ub = 1 + (si_ >> 1), (S - 1) * (si_ >> 1) - si_ + 1
        for __ in range(S - 1):
            assert np.all(Tbar < T)
            k = compressing_assign_storage_site_batched(S, Tbar)
            assert np.all(k < S)
            res[T_indices, k] = Tbar

            Tbar += step
            step[Tbar >= T] *= -1
            Tbar[Tbar >= T] = ub[Tbar >= T]
            Tbar[Tbar < lb] = lb[Tbar < lb]
    else:  # odd S: no special site, M = S
        si = bitlen32_batched((T - 1) // S)
        si_ = np.asarray(1, dtype=np.int64) << si
        assert si_.all()

        Tbar = np.zeros_like(si, dtype=np.int64)
        step = si_.astype(np.int64, copy=True)
        lb = si_ >> 1
        ub = np.maximum(S * (si_ >> 1) - si_, 0)
        for __ in range(S):
            assert np.all(Tbar < T)
            k = compressing_assign_storage_site_batched(S, Tbar)
            assert np.all(k < S)
            res[T_indices, k] = Tbar

            Tbar += step
            step[Tbar >= T] *= -1
            Tbar[Tbar >= T] = ub[Tbar >= T]
            Tbar[Tbar < lb] = lb[Tbar < lb]

    return res


# lazy loader workaround
lookup_ingest_times_batched = compressing_lookup_ingest_times_batched
