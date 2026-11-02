"""Bridge the CLI's authenticated download client to a shared asset cache."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from labqoat.references import AssetRef


@dataclass
class MountAssetSource:
    """Count only actual transfers when reporting a mount's cache reuse."""

    fetch: Callable[[str, Path], int]
    downloaded: bool = False

    def download_to(self, reference: AssetRef, destination: Path) -> None:
        """Write one exact asset using the explicitly authenticated CLI callback."""
        self.fetch(f"sha256:{reference.blob_sha256}", destination)
        self.downloaded = True
