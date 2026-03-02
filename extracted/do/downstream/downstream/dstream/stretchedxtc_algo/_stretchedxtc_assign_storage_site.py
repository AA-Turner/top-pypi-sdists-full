import typing

from ..stretched_algo._stretched_assign_storage_site import (
    stretched_assign_storage_site,
)
from ..stretched_algo._stretched_has_ingest_capacity import (
    stretched_has_ingest_capacity,
)
from ..xtchead_algo._xtchead_assign_storage_site import (
    xtchead_assign_storage_site,
)
from ._stretchedxtc_has_ingest_capacity import stretchedxtc_has_ingest_capacity


def stretchedxtc_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for stretchedxtc curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
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

        See `stretchedxtc_algo.has_ingest_capacity` for details.
    """
    if not stretchedxtc_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    if stretched_has_ingest_capacity(S, T):
        return stretched_assign_storage_site(S, T)
    else:
        return xtchead_assign_storage_site(S, T)


# lazy loader workaround
assign_storage_site = stretchedxtc_assign_storage_site
