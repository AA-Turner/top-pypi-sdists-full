import typing


def xtctail_get_ingest_capacity(S: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None if the number of supported ingestions is unlimited.

    See Also
    --------
    has_ingest_capacity : Does this algorithm have the capacity to ingest `n`
    data items?

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: Compressing circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    # restrict S >= 8 although (in principle) S >= 4 support should be possible
    surface_size_ok = S.bit_count() == 1 and S > 4
    return None if surface_size_ok else 0


get_ingest_capacity = xtctail_get_ingest_capacity  # lazy loader workaround
