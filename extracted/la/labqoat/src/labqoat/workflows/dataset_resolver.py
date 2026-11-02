"""Resolve mutable dataset selectors into immutable workflow dependencies."""

from dataclasses import dataclass
from typing import TypeVar

from labqoat.dataset_access.revision_data import RevisionData
from labqoat.json_document import JsonDocument
from labqoat.management_client import ManagementClient
from labqoat.references import DatasetRef, ResolvedDatasetRef, ResourceId

RowT = TypeVar("RowT")


@dataclass(frozen=True, slots=True)
class DatasetResolver:
    """Pin ready revision-owned identities with one authoritative resolution read."""

    client: ManagementClient

    def resolve(self, reference: DatasetRef[RowT]) -> ResolvedDatasetRef[RowT]:
        """Verify captured documents and retain storage coordinates as an opaque identity."""
        revision = self.client.get("/api/v1/datasets/resolve", {"ref": str(reference)})
        if revision.get("status") != "ready":
            raise ValueError("Training requires a ready dataset revision")
        if revision.get("dataset") != reference.repository:
            raise ValueError("Resolved dataset repository does not match the requested family")
        data = RevisionData.capture(revision)
        if reference.schema_digest is not None and reference.schema_digest != data.layout.schema.digest:
            raise ValueError("Dataset revision schema does not match the required generated schema")
        return ResolvedDatasetRef(
            dataset_id=ResourceId.parse(JsonDocument.expect_scalar(revision["dataset_id"], str)),
            repository=reference.repository,
            revision_id=ResourceId.parse(JsonDocument.expect_scalar(revision["id"], str)),
            schema_digest=data.layout.schema.digest,
            layout_digest=data.layout.digest,
            data_manifest_digest=data.manifest.digest,
            snapshot_ref=JsonDocument.expect_scalar(revision["snapshot_ref"], str),
        )
