"""Pinned Python requirements resolved and installed by the service-owned builder."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipStep:
    """Retain direct pins or a local hash-locked requirements file and an explicit index."""

    packages: tuple[str, ...]
    requirements: Path | None = None
    index_url: str | None = None
