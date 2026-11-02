"""Publish and restore opaque snapshots with ordinary typed metadata and assignment-scoped authority."""

import shutil
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TypeVar
from urllib.parse import quote
from uuid import uuid4

from labqoat.compute.background_checkpoint import BackgroundCheckpoint
from labqoat.compute.checkpoint_uploads import CheckpointUploads

from labqoat.compute.checkpoint_identity import CheckpointIdentity
from labqoat.compute.checkpoint_payload import CheckpointPayload
from labqoat.compute.checkpoint_recovery import CheckpointRecovery
from labqoat.compute.run_assets import RunAssets
from labqoat.compute.value_codec import ValueCodec
from labqoat.json_document import JsonDocument
from labqoat.manifests import Manifest
from labqoat.references import CheckpointRef, ResourceId
from labqoat.schemas.identity import Identity
from labqoat.schemas.schema_document import SchemaDocument
from labqoat.storage.verified_file import VerifiedFile
from labqoat.storage.worker_asset_source import WorkerAssetSource
from labqoat.training.assets.worker_asset_publisher import WorkerAssetPublisher
from labqoat.training.transfer_log import TransferLog
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.replay_request import ReplayRequest

T = TypeVar("T")


@dataclass(frozen=True)
class RunCheckpoints:
    """Retain exact bytes and metadata before returning an immutable checkpoint handle."""

    api: WorkerApi
    assets: RunAssets
    run_id: str
    execution_digest: str
    staging: Path
    log: TransferLog = field(default_factory=TransferLog)
    uploads: CheckpointUploads = field(default_factory=CheckpointUploads, repr=False, compare=False)
    lost: list[str] = field(default_factory=list, repr=False, compare=False)

    def publish(
        self,
        payload: str | Path,
        metadata: T,
        *,
        step: int,
        key: str,
        recovery: CheckpointRecovery | None = None,
        wait: bool = False,
    ) -> CheckpointRef[object]:
        """Bind an attempt-owned key to exact bytes, metadata and optional adapter recovery evidence.

        Returns at once: the file is copied aside and uploaded behind the caller, in the order checkpoints were
        taken, so the caller may overwrite ``payload`` immediately. Reading the returned checkpoint's ``id``, or
        returning it from the function, waits for that upload. ``wait=True`` uploads before returning.
        """
        if type(step) is not int or not 0 <= step <= 2**53 - 1:
            raise ValueError("Checkpoint step must be a portable nonnegative integer")
        if not isinstance(key, str) or not 1 <= len(key.encode("utf-8")) <= 200:
            raise ValueError("Checkpoint key must contain 1 to 200 UTF-8 bytes")
        codec = ValueCodec(type(metadata))
        schema = SchemaDocument.capture(codec.schema())
        value = JsonDocument.expect_dict(codec.encode(metadata))
        document = None if recovery is None else recovery.document(step)
        manifest = partial(self._manifest, schema, value, step=step, recovery=document)
        if wait:
            return self._retain(Path(payload), manifest, key)
        staged = self._stage(Path(payload), key, step)
        upload = self.uploads.submit(partial(self._retain_staged, staged, manifest, key))
        return BackgroundCheckpoint(upload, ResourceId.parse(self.run_id), step)

    def settle(self) -> None:
        """Wait for checkpoints still uploading so none is lost when the function ends."""
        unfinished = self.uploads.unfinished()
        if unfinished:
            self.log.note(f"waiting for {unfinished} checkpoint upload{'s' if unfinished > 1 else ''} to finish")
        self.uploads.drain()
        if self.lost:
            keys = ", ".join(self.lost)
            self.log.note(
                f"{len(self.lost)} checkpoint(s) were not saved and cannot be resumed from: {keys}", level="warning"
            )

    def _stage(self, payload: Path, key: str, step: int) -> Path:
        """Copy the snapshot aside so later saves to the same path cannot change what is uploading."""
        self.assets.require_publishable(payload)
        if self.uploads.unfinished() >= self.uploads.capacity:
            self.log.note(f"checkpoint {key} at step {step} waits for earlier checkpoint uploads")
        staged = self.staging / uuid4().hex / payload.name
        staged.parent.mkdir(parents=True)
        shutil.copyfile(payload, staged)
        return staged

    def _retain_staged(self, staged: Path, manifest: "partial[Manifest]", key: str) -> CheckpointRef[object]:
        """Upload a staged copy, report a failure where the run's reader will see it, and free the copy."""
        try:
            return self._retain(staged, manifest, key)
        except Exception as error:
            step = manifest.keywords["step"]
            self.log.note(f"checkpoint {key} at step {step} was not saved: {error}", level="warning")
            self.lost.append(key)
            raise
        finally:
            shutil.rmtree(staged.parent, ignore_errors=True)

    def _retain(self, payload: Path, manifest: "partial[Manifest]", key: str) -> CheckpointRef[object]:
        """Upload exact bytes, then bind them to the captured metadata under the attempt-owned key."""
        step = manifest.keywords["step"]
        asset = CheckpointPayload(self.api, self.assets).publish(payload, step)
        captured = manifest(digest=str(asset.blob_sha256))
        response = self._bind(captured, key)
        reference = CheckpointIdentity.reference(response)
        if CheckpointIdentity.verify(response, reference) != captured:
            raise ValueError("Published checkpoint does not match the captured snapshot")
        size = TransferLog.size(asset.byte_size)
        self.log.note(f"checkpoint {key} at step {step} saved ({size})", {"checkpoint_id": str(reference.id)})
        return reference

    def restore(self, checkpoint_id: str | ResourceId, *, metadata_type: type[T], destination: Path) -> tuple[Path, T]:
        """Resolve an authorized immutable snapshot and restore verified bytes into a writable local copy."""
        ref = quote(str(checkpoint_id), safe="")
        document = self.api.json("GET", f"/api/v1/worker/checkpoints/item?ref={ref}")
        reference = CheckpointIdentity.reference(document)
        if str(reference.id) != str(checkpoint_id):
            raise ValueError("Resolved checkpoint identity mismatch")
        manifest = CheckpointIdentity.verify(document, reference)
        codec = ValueCodec(metadata_type)
        if SchemaDocument.capture(codec.schema()).digest != manifest.document["schema_digest"]:
            raise ValueError("Checkpoint metadata schema mismatch")
        metadata = codec.decode(manifest.document["metadata"])
        self._restore_bytes(manifest.document, destination)
        return destination, metadata

    def _restore_bytes(self, manifest: JsonDocument, destination: Path) -> None:
        """Stream verified bytes into destination staging independently of shared-cache capacity."""
        digest = JsonDocument.expect_scalar(manifest["payload_sha256"], str)
        document = self.api.json("GET", f"/api/v1/worker/assets/item?ref={quote(digest, safe='')}")
        asset = WorkerAssetPublisher.reference(document)
        if f"sha256:{asset.blob_sha256}" != digest:
            raise ValueError("Checkpoint payload digest mismatch")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=destination.parent) as directory:
            captured = Path(directory) / "payload"
            WorkerAssetSource(self.api).download_to(asset, captured)
            VerifiedFile.validate(captured, str(asset.blob_sha256), asset.byte_size)
            captured.replace(destination)

    def download(self, reference: CheckpointRef[object], *, destination: Path) -> Manifest:
        """Copy a content-bound opaque snapshot for a declared adapter without deserializing framework state."""
        selector = quote(str(reference.id), safe="")
        document = self.api.json("GET", f"/api/v1/worker/checkpoints/item?ref={selector}")
        manifest = CheckpointIdentity.verify(document, reference)
        self._restore_bytes(manifest.document, destination)
        return manifest

    def _bind(self, captured: Manifest, key: str) -> JsonDocument:
        """Register the snapshot under its key, explaining the one conflict an author can cause."""
        try:
            return ReplayRequest(self.api).send(
                "/api/v1/worker/checkpoints/publish", {"manifest": captured.document, "key": key}
            )
        except WorkerApiError as error:
            if error.status != 409 or error.code not in (None, "checkpoint_key_conflict"):
                raise
            raise ValueError(
                f"Checkpoint key {key!r} already names a different checkpoint in this run; give every save "
                "its own key, for example one that includes the step and a save counter"
            ) from error

    def _manifest(
        self, schema: SchemaDocument, value: JsonDocument, *, digest: str, step: int, recovery: JsonDocument | None
    ) -> Manifest:
        """Capture metadata, bytes and the service-owned execution identity in one canonical snapshot."""
        document = JsonDocument(
            {
                "manifest_version": 1,
                "execution_digest": self.execution_digest,
                "run_id": self.run_id,
                "step": step,
                "schema": Identity.decode(schema.canonical.decode()),
                "schema_digest": schema.digest,
                "payload_sha256": f"sha256:{digest}",
                "metadata": value,
            }
        )
        if recovery is not None:
            document.update(manifest_version=2, recovery=recovery)
        return Manifest.capture("checkpoint", document)
