"""Python 3.10 support: the CLI wheel vendors this package and still runs on 3.10."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:  # pragma: no cover - exercised only on 3.10
    from enum import Enum

    class StrEnum(str, Enum):
        """3.11's StrEnum: `str(member)` is its value, never `Class.MEMBER`."""

        def __str__(self) -> str:
            return str(self.value)

__all__ = ["StrEnum"]
