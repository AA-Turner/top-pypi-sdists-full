import typing

from deprecated.sphinx import deprecated

from ..genome_instrumentation import HereditaryStratum
from ._pack_differentiae_str import pack_differentiae_str


@deprecated(
    version="1.8.0",
    reason="Use pack_differentiae_str instead.",
)
def pack_differentiae(
    strata: typing.Iterable[HereditaryStratum],
    differentia_bit_width: int,
) -> str:
    """Pack a sequence of differentiae together into a compact
    representation.

    Returns a string with base 64 encoded concatenation of diffferentiae.
    If `differentia_bit_width` is not an even byte multiple, the first encoded
    byte tells how many empty padding bits, if any, were placed at the end of
    the concatenation in order to align the bitstring end to byte boundaries.
    """

    return pack_differentiae_str(strata, differentia_bit_width)
