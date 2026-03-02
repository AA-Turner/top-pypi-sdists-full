import math
import typing


def isanan(value: typing.Any) -> bool:
    """Detect if value is NaN."""

    return isinstance(value, float) and math.isnan(value)
