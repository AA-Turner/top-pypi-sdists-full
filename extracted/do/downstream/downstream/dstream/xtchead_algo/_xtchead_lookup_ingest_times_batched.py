import warnings

import numpy as np

from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..compressing_algo._compressing_lookup_ingest_times_batched import (
    compressing_lookup_ingest_times_batched,
)


def xtchead_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = False,
) -> np.ndarray:
    """Ingest time lookup algorithm for xtchead curation.

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

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: xtchead circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if parallel:
        warnings.warn(
            "parallel xtchead lookup not yet implemented, "
            "falling back to serial implementation",
        )

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    epoch = bitlen32_batched(T).astype(T.dtype)

    S_ = np.asarray(S, dtype=T.dtype)
    res1 = compressing_lookup_ingest_times_batched(
        S, np.maximum(S_, epoch), parallel=parallel
    )
    res1 = (1 << res1) - 1

    S_indices = np.arange(S)[None, :]  # shape becomes (1, S)

    x = np.maximum(S_indices - int(S).bit_length() + 1, 0)
    res2 = x + bitlen32_batched(x + bitlen32_batched(x)) - 1

    return np.where(
        S_indices < epoch[:, None],
        res1,
        res2,
    )


# lazy loader workaround
lookup_ingest_times_batched = xtchead_lookup_ingest_times_batched
