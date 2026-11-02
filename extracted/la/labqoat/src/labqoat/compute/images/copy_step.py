"""Explicit local image input awaiting bounded immutable publication."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CopyStep:
    """Record a local selection without opening or enumerating its files."""

    path: Path
    destination: str
    directory: bool
    ignore: tuple[str, ...] = ()
