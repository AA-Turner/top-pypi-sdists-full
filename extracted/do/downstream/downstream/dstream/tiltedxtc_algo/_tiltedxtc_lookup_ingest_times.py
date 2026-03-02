import typing

from ..tilted_algo._tilted_has_ingest_capacity import (
    tilted_has_ingest_capacity,
)
from ..tilted_algo._tilted_lookup_ingest_times import (
    tilted_lookup_ingest_times,
)
from ..xtctail_algo._xtctail_lookup_ingest_times import (
    xtctail_lookup_ingest_times,
)


def tiltedxtc_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for tiltedxtc curation.

    Lazy implementaiton.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two greater than 4.
    T : int
        Current logical time.

    Yields
    ------
    typing.Optional[int]
        Ingest time of stored item at buffer sites in index order.
    """
    assert T >= 0
    if tilted_has_ingest_capacity(S, T):
        return tilted_lookup_ingest_times(S, T)
    else:
        return xtctail_lookup_ingest_times(S, T)


# lazy loader workaround
lookup_ingest_times = tiltedxtc_lookup_ingest_times
