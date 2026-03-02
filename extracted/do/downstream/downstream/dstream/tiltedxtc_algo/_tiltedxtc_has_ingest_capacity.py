from ._tiltedxtc_get_ingest_capacity import tiltedxtc_get_ingest_capacity


def tiltedxtc_has_ingest_capacity(S: int, T: int) -> bool:
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
    """
    assert T >= 0
    ingest_capacity = tiltedxtc_get_ingest_capacity(S)
    return ingest_capacity is None or T < ingest_capacity


# lazy loader workaround
has_ingest_capacity = tiltedxtc_has_ingest_capacity
