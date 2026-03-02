import typing


def tilted_get_ingest_capacity(S: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None if the number of supported ingestions is unlimited.

    See Also
    --------
    has_ingest_capacity : Does this algorithm have the capacity to ingest `n`
    data items?
    """
    surface_size_ok = S.bit_count() == 1 and S > 1
    return (2**S - 1) * surface_size_ok


get_ingest_capacity = tilted_get_ingest_capacity  # lazy loader workaround
