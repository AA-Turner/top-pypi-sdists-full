"""Explicit missing dataset capability behavior."""

from collections.abc import Iterable, Mapping, Sequence
from contextlib import AbstractContextManager
from pathlib import Path
from typing import TypeVar

from labqoat.dataset_access.dataset_provider import DatasetReference
from labqoat.dataset_files import DatasetFileManifest
from labqoat.references import AssetRef, DatasetRef
from labqoat.schemas import SchemaRecord

RowT = TypeVar("RowT", bound=SchemaRecord)


class UnavailableDatasetProvider:
    """Reject access when no local or worker dataset adapter was injected."""

    def path(self, reference: DatasetReference) -> Path:
        """Reject implicit global dataset lookup."""
        del reference
        raise ValueError("Training dataset access is unavailable")

    def manifest(self, reference: DatasetReference) -> DatasetFileManifest:
        """Reject metadata lookup without an explicitly injected dataset."""
        del reference
        raise ValueError("Training dataset access is unavailable")

    def local_files(
        self, reference: DatasetReference, paths: Sequence[str]
    ) -> AbstractContextManager[Mapping[str, Path]]:
        """Reject scoped file access without an explicitly injected dataset."""
        del reference, paths
        raise ValueError("Training dataset access is unavailable")

    def file(self, reference: DatasetReference, path: str) -> Path:
        """Reject access to unconfigured dataset files."""
        del reference, path
        raise ValueError("Training dataset access is unavailable")

    def asset(self, reference: DatasetReference, path: str) -> AssetRef:
        """Reject access to unconfigured dataset asset identities."""
        del reference, path
        raise ValueError("Training dataset access is unavailable")

    def records(self, reference: DatasetReference, path: str | None = None) -> Iterable[dict[str, object]]:
        """Reject access to unconfigured dataset rows."""
        del reference, path
        raise ValueError("Training dataset access is unavailable")

    def rows(self, reference: DatasetRef[RowT]) -> Iterable[RowT]:
        """Reject typed reads without an explicitly injected dataset."""
        del reference
        raise ValueError("Training dataset access is unavailable")

    def local_file(self, reference: AssetRef) -> AbstractContextManager[Path]:
        """Reject asset-column reads without an explicitly injected dataset."""
        del reference
        raise ValueError("Training dataset access is unavailable")
