"""Shared base class for the SDK enums."""

from enum import Enum


class ValueEnum(str, Enum):
    """
    Enum that displays as its value (e.g. ``"NONE"``) instead of ``Class.MEMBER``.

    Being a ``str`` subclass, members compare equal to their raw string value.
    ``__str__`` and ``__format__`` are defined explicitly so the output is the
    same across Python versions. If a member has an empty value, its name is shown.
    """

    def __str__(self) -> str:
        return str(self.value) if self.value else self.name

    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)
