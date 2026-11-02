"""Translate authoritative ready publication evidence into typed compute handles."""

from typing import TypeVar

from labqoat._generated.dataset_publication import DatasetPublication
from labqoat.dataset import Dataset
from labqoat.json_document import JsonDocument
from labqoat.references import ResolvedDatasetRef, ResourceId

T = TypeVar("T")


class PublishedDataset:
    """Require terminal success and exact revision identities at the SDK boundary."""

    @staticmethod
    def capture(publication: DatasetPublication, row_type: type[T]) -> Dataset[T]:
        """Bind retained schema/layout/data/snapshot identities after service materialization."""
        if publication.status != "ready" or not publication.snapshot_ref or not publication.data_manifest_digest:
            raise ValueError("Dataset publication is not ready")
        reference: ResolvedDatasetRef[object] = ResolvedDatasetRef(
            ResourceId.parse(publication.dataset_id),
            publication.dataset,
            ResourceId.parse(publication.id),
            publication.schema_digest,
            JsonDocument.expect_scalar(publication.layout["layout_digest"], str),
            publication.data_manifest_digest,
            publication.snapshot_ref,
        )
        return Dataset(reference, row_type)
