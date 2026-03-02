import typing

import numpy as np


def steady_has_ingest_capacity_batched(
    S: typing.Union[int, np.ndarray],
    T: typing.Union[int, np.ndarray],
) -> np.ndarray:
    """Does this algorithm have the capacity to ingest a data item at logical
    time T?

        Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : int or np.ndarray
        The number of buffer sites available.
    T : int or np.ndarray
        Queried logical time.

    Returns
    -------
    np.ndarray of bool
        True if ingest capacity is sufficient, False otherwise.

    See Also
    --------
    get_ingest_capacity : How many data item ingestions does this algorithm
    support?
    """
    S, T = np.asarray(S), np.asarray(T)
    assert (T >= 0).all()

    surface_size_ok = np.logical_and(np.bitwise_count(S) == 1, S > 1)
    return surface_size_ok + np.zeros_like(T, dtype=bool)  # Broadcast T.size


# lazy loader workaround
has_ingest_capacity_batched = steady_has_ingest_capacity_batched
