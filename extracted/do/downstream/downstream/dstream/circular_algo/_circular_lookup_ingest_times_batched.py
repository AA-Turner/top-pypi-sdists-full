import numpy as np

from ..._auxlib._jit import jit
from ..._auxlib._jit_prange import jit_prange
from ..._auxlib._pick_batched_chunk_size import pick_batched_chunk_size


def circular_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = True,
) -> np.ndarray:
    """Ingest time lookup algorithm for circular curation.

    Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : int
        Buffer size. Must be positive.
    T : np.ndarray
        One-dimensional array of current logical times.
    parallel : bool, default True
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

    return [
        _circular_lookup_ingest_times_batched,
        _circular_lookup_ingest_times_batched_jit,
    ][bool(parallel)](np.int64(S), T.astype(np.int64))


def _circular_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for circular_lookup_ingest_times_batched."""
    assert np.all(T > 0)  # T < S disallowed
    T_ = T - 1
    res = np.empty((T.size, S), dtype=np.uint64)
    res[:, 0] = T_ - T_ % S
    for k_, k in zip(range(S), range(1, S)):
        res[:, k] = res[:, k_] + 1
        overflow_mask = res[:, k] == T
        res[overflow_mask, k] -= np.asarray(S, dtype=np.uint64)

    return res


# implementation detail for _circular_lookup_ingest_times_batched_jit
_circular_lookup_ingest_times_batched_jit_serial = jit(
    "uint64[:,:](int64, int64[:])", nogil=True, nopython=True
)(_circular_lookup_ingest_times_batched)


@jit(cache=True, nogil=True, nopython=True, parallel=True)
def _circular_lookup_ingest_times_batched_jit(
    S: int, T: np.ndarray, chunk_size: int = pick_batched_chunk_size()
):
    """Implementation detail for circular_lookup_ingest_times_batched."""
    num_rows = T.shape[0]
    num_chunks = (num_rows + chunk_size - 1) // chunk_size

    result = np.empty((num_rows, S), dtype=np.uint64)
    for chunk in jit_prange(num_chunks):
        chunk_slice = slice(
            chunk * chunk_size,  # begin
            min((chunk + 1) * chunk_size, num_rows),  # end
        )

        chunk_T = T[chunk_slice]
        chunk_result = _circular_lookup_ingest_times_batched_jit_serial(
            S, chunk_T
        )
        result[chunk_slice, :] = chunk_result

    return result


# lazy loader workaround
lookup_ingest_times_batched = circular_lookup_ingest_times_batched
