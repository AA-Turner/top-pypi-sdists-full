"""Python 3.10 support (plan 2.11): the 3.11-only names this package uses.

Import them from here, never from the standard library directly --
`tests/test_py310_compat.py` fails when a module does:

* ``StrEnum`` (``enum``, 3.11). The 3.10 backport keeps 3.11's behaviour where it
  matters: members ARE ``str``, and ``str(member)`` / ``format(member)`` give the
  value. A plain ``class X(str, Enum)`` gives ``"X.member"``, which would change
  every f-string and every header built from a member.
* ``UTC`` (``datetime``, 3.11): ``timezone.utc``, which is what 3.11's alias is.
* ``tomllib`` (3.11): the ``tomli`` backport on 3.10 (a dependency there only).
* ``fromisoformat``: ``datetime.fromisoformat`` accepting a trailing ``Z``, as
  3.11's does. On 3.10 the server's own timestamps (``...Z``) raise ValueError.
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
