"""Python 3.10 support (plan 2.11): StrEnum, UTC, tomllib, and a fromisoformat that reads ``Z``.

Import them from here, never the stdlib (`tests/test_py310_compat.py`). Why each: DESIGN.md.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone

UTC = timezone.utc


def fromisoformat(value: str) -> datetime:
    """``datetime.fromisoformat``, with 3.11's reading of a trailing ``Z``."""
    if value[-1:] in ("Z", "z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)

def _strenum_backport() -> type:
    """``enum.StrEnum`` for Python 3.10. Built by a function so the tests can
    check it against the real one on any interpreter."""
    import enum

    class StrEnum(str, enum.Enum):
        """Enum where members are also (and must be) strings."""

        def __new__(cls, *values):
            if len(values) > 3:
                raise TypeError(f"too many arguments for str(): {values!r}")
            if len(values) == 1 and not isinstance(values[0], str):
                raise TypeError(f"{values[0]!r} is not a string")
            value = str(*values)
            member = str.__new__(cls, value)
            member._value_ = value
            return member

        __str__ = str.__str__
        __format__ = str.__format__

        @staticmethod
        def _generate_next_value_(name, start, count, last_values):
            return name.lower()

    return StrEnum


if sys.version_info >= (3, 11):
    import tomllib
    from enum import StrEnum
else:  # pragma: no cover - exercised by the 3.10 CI leg
    import tomli as tomllib

    StrEnum = _strenum_backport()


__all__ = ["UTC", "StrEnum", "fromisoformat", "tomllib"]
