import typing

from .nanto import nanto


def nantozero(value: typing.Any) -> typing.Any:
    """Replace value with None if value is NaN."""

    return nanto(value, 0.0)
