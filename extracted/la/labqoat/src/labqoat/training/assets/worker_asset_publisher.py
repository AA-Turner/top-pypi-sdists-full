"""Assignment-scoped publication of immutable training artifacts."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from labqoat.json_document import JsonDocument
from labqoat.references import AssetRef, ResourceId, Sha256
from labqoat.storage.direct_asset_upload import DirectAssetUpload
from labqoat.storage.verified_file import VerifiedFile
from labqoat.training.transfer_log import TransferLog
from labqoat.worker import WorkerApi
from labqoat.worker.replay_request import ReplayRequest


@dataclass(frozen=True, slots=True)
class WorkerAssetPublisher:
    """Stage, upload, verify, and link files using only assignment authority."""

    api: WorkerApi
    purpose: str = "training"
    maximum_bytes: int = 12 * 1024 * 1024 * 1024
    direct_from_bytes: int = 4 * 1024 * 1024
    log: TransferLog = field(default_factory=TransferLog)

    def publish(
        self, source: str | Path, *, media_type: str, name: str | None = None, step: int | None = None
    ) -> AssetRef:
        """Verify published bytes and return the catalog's retained identity and media type."""
        path = Path(source)
        filename = str(VerifiedFile.relative(path.name if name is None else name))
        if step is not None and step < 0:
            raise ValueError("Asset step cannot be negative")
        byte_size = self.require_publishable(path, filename)
        digest = VerifiedFile.digest(path)
        payload = JsonDocument(
            {
                "sha256": digest,
                "byte_size": byte_size,
                "media_type": media_type,
                "filename": filename,
                "purpose": self.purpose,
                "provenance": {"name": filename, "step": step},
            }
        )
        staged = ReplayRequest(self.api).send("/api/v1/worker/assets/prepare", payload)
        with self.log.upload(filename, byte_size):
            completed = self._transfer(staged, path, byte_size)
        asset = self.reference(completed)
        if str(asset.blob_sha256) != digest or asset.byte_size != byte_size:
            raise ValueError("Published asset identity mismatch")
        ReplayRequest(self.api).send("/api/v1/worker/assignments/produced-assets", {"asset_sha": digest})
        return asset

    def require_publishable(self, source: str | Path, name: str | None = None) -> int:
        """Reject a file over the artifact limit before hashing or copying it, and return its size."""
        path = Path(source)
        byte_size = path.stat().st_size
        if byte_size > self.maximum_bytes:
            raise ValueError(
                f"{name or path.name} is {byte_size / 1_048_576:.0f} MiB; one artifact holds at most "
                f"{self.maximum_bytes // 1_073_741_824} GiB. Publish smaller files, for example the weights without "
                "optimizer state, or several parts."
            )
        return byte_size

    def _transfer(self, staged: JsonDocument, path: Path, byte_size: int) -> JsonDocument:
        """Supply exact bytes even on a catalog hit so a digest alone never grants output authority.

        A staged asset may carry a storage grant; large files then skip the API server and completion verifies
        them. A small file is quicker on the connection already open to the service than on a new one to storage.
        """
        reference = quote(JsonDocument.expect_scalar(staged["id"], str), safe="")
        prefix = "/api/v1/worker/assets/item"
        replay = ReplayRequest(self.api)
        grant = staged.get("upload")
        if not (isinstance(grant, dict) and self._direct(grant, path, byte_size)):
            replay.upload(f"{prefix}/content?ref={reference}", path, byte_size)
        return replay.send(f"{prefix}/complete?ref={reference}", {})

    def _direct(self, grant: Mapping[str, object], path: Path, byte_size: int) -> bool:
        """Use the grant for files large enough to repay a new storage connection."""
        return byte_size >= self.direct_from_bytes and DirectAssetUpload.send(grant, path)

    @staticmethod
    def reference(document: JsonDocument) -> AssetRef:
        """Decode the platform's authoritative content identity."""
        return AssetRef(
            id=ResourceId.parse(JsonDocument.expect_scalar(document["id"], str)),
            blob_sha256=Sha256.parse(JsonDocument.expect_scalar(document["sha256"], str)),
            byte_size=JsonDocument.expect_scalar(document["byte_size"], int),
            media_type=JsonDocument.expect_scalar(document["media_type"], str),
        )
