"""Shared local/worker physical reading and explicit reference evidence."""

from collections.abc import Iterator
from pathlib import Path

from labqoat.argument_codec import decode_result
from labqoat.data_layout.asset_references import AssetReferences
from labqoat.data_layout.dataset_rows import DatasetRows
from labqoat.dataset_access.dataset_asset_index import DatasetAssetIndex
from labqoat.dataset_access.revision_files import RevisionFiles
from labqoat.json_document import JsonDocument
from labqoat.references import AssetRef


class RevisionRecords:
    """Decode exact Parquet types, validate every logical row and retain only schema-marked assets."""

    @staticmethod
    def read(revision: RevisionFiles, name: str, path: Path, index: DatasetAssetIndex) -> Iterator[dict[str, object]]:
        """Keep reader memory bounded and compare complete part counts with captured evidence."""
        data = revision.data
        references = AssetReferences(data.layout.root)
        count = 0
        for row in DatasetRows(data.layout).parquet(path):
            count += 1
            index.add(
                (decode_result(value, AssetRef) for _, value in references.read(row)), revision.reference.revision_id
            )
            yield dict(row)
        entries = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(data.manifest.document["files"])]
        expected = next(item["rows"] for item in entries if JsonDocument.expect_dict(item["input"])["path"] == name)
        if count != expected:
            raise ValueError("Materialized rows do not match the captured manifest")
