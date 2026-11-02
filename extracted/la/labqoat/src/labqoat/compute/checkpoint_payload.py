"""Publish opaque checkpoint bytes without changing an existing asset's immutable descriptors."""

from dataclasses import dataclass
from pathlib import Path

from labqoat.compute.run_assets import RunAssets
from labqoat.json_document import JsonDocument
from labqoat.references import AssetRef
from labqoat.storage.verified_file import VerifiedFile
from labqoat.training.assets.worker_asset_publisher import WorkerAssetPublisher
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class CheckpointPayload:
    """Retain registered content metadata while still proving bytes under the current assignment."""

    api: WorkerApi
    assets: RunAssets

    def publish(self, payload: str | Path, step: int) -> AssetRef:
        """Default new snapshots to binary and reconcile only an existing registration conflict."""
        try:
            return self.assets.publish(payload, media_type="application/octet-stream", step=step)
        except WorkerApiError as error:
            if error.status != 409:
                raise
        return self._publish_registered(Path(payload), step)

    def _publish_registered(self, path: Path, step: int) -> AssetRef:
        """Resolve an authorized descriptor, verify its bytes and republish with proof of possession."""
        digest = VerifiedFile.digest(path)
        document = self.api.json("GET", f"/api/v1/worker/assets/item?ref=sha256%3A{digest}")
        asset = WorkerAssetPublisher.reference(document)
        VerifiedFile.validate(path, str(asset.blob_sha256), asset.byte_size)
        filename = document.get("filename")
        name = None if filename is None else JsonDocument.expect_scalar(filename, str)
        return self.assets.publish(path, media_type=asset.media_type, name=name, step=step)
