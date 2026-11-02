"""Typed immutable dataset handles shared by host and assignment-owned execution."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

from labqoat.references.resolved_dataset_ref import ResolvedDatasetRef

if TYPE_CHECKING:
    from labqoat.run_context import RunContext

T = TypeVar("T")


@dataclass(frozen=True)
class Dataset(Generic[T]):
    """Bind ordinary authored rows to an exact ready revision, never a moving alias."""

    reference: ResolvedDatasetRef[object]
    row_type: type[T]

    def __post_init__(self) -> None:
        """Reject row declarations whose complete captured interface differs from the revision."""
        from labqoat.compute.value_codec import ValueCodec
        from labqoat.schemas.schema_document import SchemaDocument

        if not is_dataclass(self.row_type):
            raise TypeError("Dataset rows must be declared as dataclasses")
        if SchemaDocument.capture(ValueCodec(self.row_type).schema()).digest != self.reference.schema_digest:
            raise ValueError("Dataset row schema does not match the captured revision")

    @property
    def id(self) -> str:
        """Return the exact immutable revision ID used for provenance and transport."""
        return str(self.reference.revision_id)

    def rows(self, context: RunContext, split: str | None = None) -> Iterator[T]:
        """Stream validated dataclass rows, optionally only those whose ``split`` field equals ``split``."""
        return context.datasets.rows(self, split)

    def files(self, context: RunContext) -> Path:
        """A read-only directory with the revision's verified Parquet files, for column or batch reads with pyarrow."""
        return context.datasets.files(self)
