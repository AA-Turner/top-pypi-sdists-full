import typing


def circular_get_ingest_capacity(S: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None if the number of supported ingestions is unlimited.

    See Also
    --------
    has_ingest_capacity : Does this algorithm have the capacity to ingest `n`
    data items?
    """
    surface_size_ok = S > 0
    return None if surface_size_ok else 0


get_ingest_capacity = circular_get_ingest_capacity  # lazy loader workaround
