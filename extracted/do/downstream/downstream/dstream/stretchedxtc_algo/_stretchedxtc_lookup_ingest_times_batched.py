import numpy as np

from ..stretched_algo._stretched_has_ingest_capacity_batched import (
    stretched_has_ingest_capacity_batched,
)
from ..stretched_algo._stretched_lookup_ingest_times_batched import (
    stretched_lookup_ingest_times_batched,
)
from ..xtchead_algo._xtchead_lookup_ingest_times_batched import (
    xtchead_lookup_ingest_times_batched,
)


def stretchedxtc_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = False,
) -> np.ndarray:
    """Ingest time lookup algorithm for stretchedxtc curation.

    Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
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
    """
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    stretched_has_capacity = stretched_has_ingest_capacity_batched(S, T)
    res = np.empty((T.size, S), dtype=np.uint64)
    res[stretched_has_capacity] = stretched_lookup_ingest_times_batched(
        S, T[stretched_has_capacity], parallel=parallel
    )
    res[~stretched_has_capacity] = xtchead_lookup_ingest_times_batched(
        S, T[~stretched_has_capacity], parallel=parallel
    )
    return res


# lazy loader workaround
lookup_ingest_times_batched = stretchedxtc_lookup_ingest_times_batched
