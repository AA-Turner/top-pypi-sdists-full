import typing


def tiltedxtc_get_ingest_capacity(S: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None if the number of supported ingestions is unlimited.

    See Also
    --------
    has_ingest_capacity : Does this algorithm have the capacity to ingest `n`
    data items?
    """
    # restrict S >= 8 although (in principle) S >= 4 support should be possible
    # ... restriction is due to xtctail
    surface_size_ok = S.bit_count() == 1 and S > 4
    return None if surface_size_ok else 0


# lazy loader workaround
get_ingest_capacity = tiltedxtc_get_ingest_capacity
