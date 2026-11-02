"""Bounded downloads using an explicitly authenticated SDK client."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from labqoat.assets_client import AssetsClient
from labqoat.references import AssetRef
from labqoat.storage.direct_asset_download import DirectAssetDownload


@dataclass(frozen=True, slots=True)
class ClientAssetSource:
    """Stream only selected files from the authenticated public asset endpoint."""

    client: AssetsClient

    def plan(self, reference: AssetRef) -> Mapping[str, object]:
        """Request a fresh authenticated transfer plan with a newly signed storage grant."""
        return self.client.download_plan(str(reference.id))

    def download_to(self, reference: AssetRef, destination: Path) -> None:
        """Bound disk writes by the pinned size; the cache verifies the final digest."""
        if DirectAssetDownload.acquire(reference, destination, self.plan):
            return
        received = 0
        with destination.open("wb") as output:
            for chunk in self.client.download_chunks(f"sha256:{reference.blob_sha256}"):
                received += len(chunk)
                if received > reference.byte_size:
                    raise ValueError("Asset download exceeds its declared byte size")
                output.write(chunk)
