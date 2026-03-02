import typing

from .nanto import nanto


def nantonone(value: typing.Any) -> typing.Any:
    """Replace value with None if value is NaN."""

    return nanto(value, None)
