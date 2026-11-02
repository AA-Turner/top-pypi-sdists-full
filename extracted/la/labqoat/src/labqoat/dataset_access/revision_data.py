"""Verify captured revision documents before exposing immutable dataset dependencies."""

from dataclasses import dataclass

from labqoat.data_layout import DatasetLayout
from labqoat.json_document import JsonDocument
from labqoat.manifests.manifest import Manifest
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True)
class RevisionData:
    """Bind full schema semantics and reproduced layout to the retained data manifest."""

    layout: DatasetLayout
    manifest: Manifest

    @classmethod
    def capture(cls, response: JsonDocument) -> "RevisionData":
        """Reject document substitution, unsupported layouts, and inconsistent row totals."""
        layout = DatasetLayout.capture(JsonDocument.expect_dict(response["schema"]))
        expected = {
            "schema_digest": layout.schema.digest,
            "layout_digest": layout.digest,
            "layout_version": 1,
            "root": layout.root.document(),
        }
        if response["schema_digest"] != layout.schema.digest or response["layout"] != expected:
            raise ValueError("Dataset schema or layout identity mismatch")
        manifest = Manifest.capture("data_manifest", response["data_manifest"])
        if manifest.digest != response["data_manifest_digest"]:
            raise ValueError("Dataset data manifest identity mismatch")
        document = manifest.document
        if any(document[key] != expected[key] for key in ("schema_digest", "layout_digest", "layout_version")):
            raise ValueError("Dataset manifest schema or layout identity mismatch")
        cls._files(document)
        return cls(layout, manifest)

    @staticmethod
    def _files(document: JsonDocument) -> None:
        """Check unique logical input paths and complete materialized row accounting."""
        files = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(document["files"])]
        paths = [JsonDocument.expect_scalar(JsonDocument.expect_dict(item["input"])["path"], str) for item in files]
        for path in paths:
            VerifiedFile.relative(path)
        if len(paths) != len(set(paths)):
            raise ValueError("Dataset manifest contains duplicate logical paths")
        if document["rows"] != sum(JsonDocument.expect_scalar(item["rows"], int) for item in files):
            raise ValueError("Dataset manifest row count mismatch")
