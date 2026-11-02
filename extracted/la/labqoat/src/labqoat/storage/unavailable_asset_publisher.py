"""Explicit failure when asset storage was not injected."""

from pathlib import Path

from labqoat.references import AssetRef


class UnavailableAssetPublisher:
    """Reject publication when the caller omitted an asset adapter."""

    def publish(
        self, source: str | Path, *, media_type: str, name: str | None = None, step: int | None = None
    ) -> AssetRef:
        """Explain the missing runtime capability."""
        del source, media_type, name, step
        raise ValueError("Asset publication is unavailable in this context")

    def require_publishable(self, source: str | Path, name: str | None = None) -> int:
        """Explain the missing runtime capability."""
        del source, name
        raise ValueError("Asset publication is unavailable in this context")
