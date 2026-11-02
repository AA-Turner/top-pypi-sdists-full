"""Explicit asset publication capability for authored training."""

from pathlib import Path
from typing import Protocol

from labqoat.references import AssetRef


class AssetPublisher(Protocol):
    """Publish exact bytes produced by a training job."""

    def publish(
        self, source: str | Path, *, media_type: str, name: str | None = None, step: int | None = None
    ) -> AssetRef:
        """Publish one local file and return its immutable identity."""
        ...

    def require_publishable(self, source: str | Path, name: str | None = None) -> int:
        """Reject a file this publisher cannot retain before any work is spent on it, and return its size."""
        ...
