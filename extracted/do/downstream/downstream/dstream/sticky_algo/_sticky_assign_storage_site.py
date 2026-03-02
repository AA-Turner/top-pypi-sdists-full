import typing

from ._sticky_has_ingest_capacity import sticky_has_ingest_capacity


def sticky_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for sticky curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be positive.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.

    Raises
    ------
    ValueError
        If insufficient ingest capacity is available.

        See `sticky_algo.has_ingest_capacity` for details.
    """
    if not sticky_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    return T if T < S else None


assign_storage_site = sticky_assign_storage_site  # lazy loader workaround
