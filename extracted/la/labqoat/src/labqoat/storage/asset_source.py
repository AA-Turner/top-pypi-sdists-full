"""Bounded file-transfer dependency for verified asset caches."""

from pathlib import Path
from typing import Protocol, runtime_checkable

from labqoat.references import AssetRef


@runtime_checkable
class AssetSource(Protocol):
    """Write authorized asset bytes into a caller-owned temporary file."""

    def download_to(self, reference: AssetRef, destination: Path) -> None:
        """Transfer one exact asset without publishing incomplete cache entries."""
        ...
