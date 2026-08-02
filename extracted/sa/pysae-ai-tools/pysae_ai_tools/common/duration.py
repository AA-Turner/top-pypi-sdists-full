"""Shared parsing of short duration strings like ``2h``, ``30m``, ``1d``, ``90s``."""

import re
from datetime import timedelta

_UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
_DURATION_RE = re.compile(r"^\s*(\d+)\s*([smhd]?)\s*$")


def parse_duration(value: str, *, allow_bare: bool = True, allowed_units: str = "smhd") -> timedelta:
    """Parse ``value`` into a :class:`~datetime.timedelta`.

    ``allow_bare`` controls whether a unitless number is accepted (interpreted
    as seconds). ``allowed_units`` restricts which single-letter units (``s``,
    ``m``, ``h``, ``d``) are valid. Raises ``ValueError`` on anything else.
    """
    match = _DURATION_RE.match(value)
    if not match:
        raise ValueError(f"invalid duration: {value}")
    unit = match.group(2)
    if not unit and not allow_bare:
        raise ValueError(f"invalid duration: {value}")
    if unit and unit not in allowed_units:
        raise ValueError(f"invalid duration: {value}")
    return timedelta(seconds=int(match.group(1)) * _UNIT_SECONDS[unit or "s"])
