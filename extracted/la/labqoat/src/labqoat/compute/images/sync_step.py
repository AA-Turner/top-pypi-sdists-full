"""Locked uv project dependency and local-source selection."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SyncStep:
    """Keep uv package, group and extra selection independent of source enumeration."""

    project: Path
    package: str | None = None
    groups: tuple[str, ...] = ()
    extras: tuple[str, ...] = ()
