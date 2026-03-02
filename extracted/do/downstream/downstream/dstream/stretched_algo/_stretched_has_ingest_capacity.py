def stretched_has_ingest_capacity(S: int, T: int) -> bool:
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
    surface_size_ok = int(S).bit_count() == 1 and S > 1
    return surface_size_ok and int(T + 1).bit_length() <= S


has_ingest_capacity = stretched_has_ingest_capacity  # lazy loader workaround
