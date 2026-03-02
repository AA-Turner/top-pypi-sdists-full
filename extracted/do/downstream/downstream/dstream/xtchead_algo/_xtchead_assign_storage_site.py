import typing

from ..compressing_algo._compressing_assign_storage_site import (
    compressing_assign_storage_site,
)
from ._xtchead_has_ingest_capacity import xtchead_has_ingest_capacity


def xtchead_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for xtchead curation.

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

        See `xtchead_algo.has_ingest_capacity` for details.

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: Compressing circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    if not xtchead_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    # special-case site 0 for T = 0, to fill entire buffer
    S, T = int(S), int(T)

    if (T + 1).bit_count() <= 1:
        return compressing_assign_storage_site(S, T.bit_length())
    elif T < S:
        # inverse of https://oeis.org/A057716
        return S.bit_length() + T - T.bit_length()
    else:
        return None


assign_storage_site = xtchead_assign_storage_site  # lazy loader workaround
