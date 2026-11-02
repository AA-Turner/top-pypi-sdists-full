"""Stream assignment-authorized asset bytes directly into a cache staging file."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from labqoat.argument_codec import decode_result
from labqoat.references import AssetRef
from labqoat.storage.direct_asset_download import DirectAssetDownload
from labqoat.worker import WorkerApi


@dataclass(frozen=True, slots=True)
class WorkerAssetSource:
    """Keep bulk transfers bounded while preserving both worker credential layers."""

    api: WorkerApi

    def authorize(self, reference: AssetRef) -> None:
        """Revalidate the current assignment and complete immutable metadata."""
        metadata = self.api.json("GET", f"/api/v1/worker/assets/item?ref={reference.id}")
        identity = {
            "id": metadata["id"],
            "blob_sha256": metadata["sha256"],
            "byte_size": metadata["byte_size"],
            "media_type": metadata["media_type"],
        }
        if decode_result(identity, AssetRef) != reference:
            raise ValueError("Authorized asset does not match its immutable reference")

    def plan(self, reference: AssetRef) -> Mapping[str, object]:
        """Request a fresh assignment-authorized transfer plan with a newly signed storage grant."""
        return self.api.json("GET", f"/api/v1/worker/assets/item/transfer?ref={reference.id}")

    def download_to(self, reference: AssetRef, destination: Path) -> None:
        """Download at most the immutable descriptor's declared number of bytes."""
        if DirectAssetDownload.acquire(reference, destination, self.plan):
            return
        path = f"/api/v1/worker/assets/item/download?ref=sha256:{reference.blob_sha256}"
        self.api.download_to(path, destination, reference.byte_size)
