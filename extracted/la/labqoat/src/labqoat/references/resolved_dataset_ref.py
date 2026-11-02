"""Exact dataset identities injected into authored workflows."""

import re
from dataclasses import dataclass
from typing import Generic, TypeVar

from labqoat.references.named_reference import NamedReference
from labqoat.references.resource_id import ResourceId

RowT = TypeVar("RowT", covariant=True)


@dataclass(frozen=True, slots=True)
class ResolvedDatasetRef(Generic[RowT]):
    """A ready revision's captured schema, layout, data, and opaque storage identity."""

    dataset_id: ResourceId
    repository: str
    revision_id: ResourceId
    schema_digest: str
    layout_digest: str
    data_manifest_digest: str
    snapshot_ref: str

    def __post_init__(self) -> None:
        """Require complete qualified identities without interpreting catalog coordinates."""
        NamedReference.validate(self.repository, "latest")
        for digest in (self.schema_digest, self.layout_digest, self.data_manifest_digest):
            if re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is None:
                raise ValueError("Expected an algorithm-qualified SHA-256 digest")
        if not self.snapshot_ref.strip():
            raise ValueError("Expected a nonempty snapshot reference")

    @property
    def family_id(self) -> ResourceId:
        """Return the stable repository identity."""
        return self.dataset_id

    @property
    def family_name(self) -> str:
        """Return the registered repository name."""
        return self.repository
