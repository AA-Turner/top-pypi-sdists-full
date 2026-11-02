"""Verified materialized file inventory bound to an exact execution dataset pin."""

from dataclasses import dataclass

from labqoat.dataset_access.revision_data import RevisionData
from labqoat.dataset_files import DatasetFile, DatasetFileManifest
from labqoat.json_document import JsonDocument
from labqoat.references import AssetRef, ResolvedDatasetRef, ResourceId, Sha256


@dataclass(frozen=True)
class RevisionFiles:
    """Keep captured schemas and materialized assets together through runtime access."""

    reference: ResolvedDatasetRef[object]
    data: RevisionData
    manifest: DatasetFileManifest

    @classmethod
    def capture(cls, response: JsonDocument, reference: ResolvedDatasetRef[object]) -> "RevisionFiles":
        """Require the requested revision, all pinned digests, and exact manifest membership."""
        if response.get("revision_id") != str(reference.revision_id):
            raise ValueError("Dataset response does not match the pinned revision")
        data = RevisionData.capture(response)
        identities = (data.layout.schema.digest, data.layout.digest, data.manifest.digest)
        if identities != (reference.schema_digest, reference.layout_digest, reference.data_manifest_digest):
            raise ValueError("Dataset documents do not match the pinned identities")
        if response["layout_digest"] != reference.layout_digest:
            raise ValueError("Dataset response layout digest does not match the pinned identity")
        entries = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(response["files"])]
        retained = [
            JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(data.manifest.document["files"])
        ]
        if len(entries) != len(retained):
            raise ValueError("Dataset files do not match the captured manifest")
        files = tuple(cls._file(entry, expected) for entry, expected in zip(entries, retained, strict=True))
        return cls(reference, data, DatasetFileManifest(files=files))

    @staticmethod
    def _file(entry: JsonDocument, expected: JsonDocument) -> DatasetFile:
        """Attach real asset IDs to retained Parquet evidence without inventing file metadata."""
        descriptor = {key: value for key, value in entry.items() if key not in ("asset_id", "format")}
        if descriptor != expected or entry.get("format") != "parquet":
            raise ValueError("Dataset file descriptor does not match the captured manifest")
        source = JsonDocument.expect_dict(expected["input"])
        return DatasetFile(
            path=JsonDocument.expect_scalar(source["path"], str),
            asset=AssetRef(
                id=ResourceId.parse(JsonDocument.expect_scalar(entry["asset_id"], str)),
                blob_sha256=Sha256.parse(JsonDocument.expect_scalar(expected["sha256"], str).removeprefix("sha256:")),
                byte_size=JsonDocument.expect_scalar(expected["byte_size"], int),
                media_type="application/vnd.apache.parquet",
            ),
        )
