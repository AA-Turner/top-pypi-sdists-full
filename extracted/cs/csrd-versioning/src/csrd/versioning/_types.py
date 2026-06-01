from collections.abc import Mapping
from enum import Enum
from typing import Any

VersionKey = Enum | str | int | None
VersionMap = Mapping[VersionKey, Any]
VersionedAppState = Mapping[str, Any]


__all__ = (
    "VersionKey",
    "VersionMap",
    "VersionedAppState",
)
