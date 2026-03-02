import typing

from .isanan import isanan


def nanto(
    value: typing.Any,
    replacement: typing.Any,
) -> typing.Any:
    """Replace value with replacement if value is NaN."""

    return replacement if isanan(value) else value
