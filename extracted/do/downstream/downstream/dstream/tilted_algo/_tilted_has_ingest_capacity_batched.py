import typing

import numpy as np


def tilted_has_ingest_capacity_batched(
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
    assert (np.asarray(T) >= 0).all()

    S = np.asarray(S)
    surface_size_ok = np.logical_and(np.bitwise_count(S) == 1, S > 1)
    with np.errstate(over="ignore"):
        ingest_capacity_at_least = (1 << np.asarray(S, dtype=np.uint64)) - 1
    return np.logical_and(surface_size_ok, T < ingest_capacity_at_least)


# lazy loader workaround
has_ingest_capacity_batched = tilted_has_ingest_capacity_batched
