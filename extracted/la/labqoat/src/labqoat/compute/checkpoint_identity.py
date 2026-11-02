"""Bind checkpoint handles to canonical manifests and their exact source Run and step."""

from labqoat.json_document import JsonDocument
from labqoat.manifests import Manifest
from labqoat.references import CheckpointRef, ResourceId, Sha256
from labqoat.schemas.identity import Identity


class CheckpointIdentity:
    """Verify the immutable envelope before acquiring payload bytes."""

    @staticmethod
    def reference(document: JsonDocument) -> CheckpointRef[object]:
        """Validate a publication response and return its content-bound checkpoint reference."""
        manifest = Manifest.capture("checkpoint", document["manifest"])
        captured = manifest.document
        if document.get("manifest_digest") != manifest.digest:
            raise ValueError("Checkpoint manifest digest mismatch")
        actual = {field: document.get(field) for field in ("run_id", "step")}
        expected = {field: captured[field] for field in ("run_id", "step")}
        if Identity.bytes(actual) != Identity.bytes(expected):
            raise ValueError("Checkpoint source Run or step mismatch")
        return CheckpointRef(
            id=ResourceId.parse(JsonDocument.expect_scalar(document["id"], str)),
            run_id=ResourceId.parse(JsonDocument.expect_scalar(captured["run_id"], str)),
            step=JsonDocument.expect_scalar(captured["step"], int),
            manifest_sha256=Sha256.parse(manifest.digest.removeprefix("sha256:")),
        )

    @staticmethod
    def verify(document: JsonDocument, reference: CheckpointRef[object]) -> Manifest:
        """Require every pinned reference coordinate and validate the full embedded metadata schema."""
        if CheckpointIdentity.reference(document) != reference:
            raise ValueError("Downloaded checkpoint identity mismatch")
        return Manifest.capture("checkpoint", document["manifest"])
