import numpy as np

from ..tilted_algo._tilted_has_ingest_capacity_batched import (
    tilted_has_ingest_capacity_batched,
)
from ..tilted_algo._tilted_lookup_ingest_times_batched import (
    tilted_lookup_ingest_times_batched,
)
from ..xtctail_algo._xtctail_lookup_ingest_times_batched import (
    xtctail_lookup_ingest_times_batched,
)


def tiltedxtc_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = False,
) -> np.ndarray:
    """Ingest time lookup algorithm for tiltedxtc curation.

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
    """
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    tilted_has_capacity = tilted_has_ingest_capacity_batched(S, T)
    res = np.empty((T.size, S), dtype=np.uint64)
    res[tilted_has_capacity] = tilted_lookup_ingest_times_batched(
        S, T[tilted_has_capacity], parallel=parallel
    )
    res[~tilted_has_capacity] = xtctail_lookup_ingest_times_batched(
        S, T[~tilted_has_capacity], parallel=parallel
    )
    return res


# lazy loader workaround
lookup_ingest_times_batched = tiltedxtc_lookup_ingest_times_batched
