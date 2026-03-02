import typing

from ..tilted_algo._tilted_assign_storage_site import (
    tilted_assign_storage_site,
)
from ..tilted_algo._tilted_has_ingest_capacity import (
    tilted_has_ingest_capacity,
)
from ..xtctail_algo._xtctail_assign_storage_site import (
    xtctail_assign_storage_site,
)
from ._tiltedxtc_has_ingest_capacity import tiltedxtc_has_ingest_capacity


def tiltedxtc_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for tiltedxtc curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two greater than 4.
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

        See `tiltedxtc_algo.has_ingest_capacity` for details.
    """
    if not tiltedxtc_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    if tilted_has_ingest_capacity(S, T):
        return tilted_assign_storage_site(S, T)
    else:
        return xtctail_assign_storage_site(S, T)


# lazy loader workaround
assign_storage_site = tiltedxtc_assign_storage_site
