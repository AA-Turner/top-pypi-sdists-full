from ._circular_get_ingest_capacity import circular_get_ingest_capacity


def circular_has_ingest_capacity(S: int, T: int) -> bool:
    """Does this algorithm have the capacity to ingest a data item at logical
    time T?

    Parameters
    ----------
    S : int
        The number of buffer sites available.
    T : int
        Queried logical time.

    Returns
    -------
    bool

    See Also
    --------
    get_ingest_capacity : How many data item ingestions does this algorithm
    support?
    has_ingest_capacity_batched : Numpy-friendly implementation.
    """
    assert T >= 0
    ingest_capacity = circular_get_ingest_capacity(S)
    return ingest_capacity is None or T < ingest_capacity


has_ingest_capacity = circular_has_ingest_capacity  # lazy loader workaround
