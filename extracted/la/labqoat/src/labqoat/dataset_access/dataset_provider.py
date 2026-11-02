"""Read-only dataset injection boundary."""

from collections.abc import Iterable, Mapping, Sequence
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Protocol, TypeVar

from labqoat.dataset_files import DatasetFileManifest
from labqoat.references import AssetRef, DatasetRef, ResolvedDatasetRef
from labqoat.schemas import SchemaRecord

DatasetReference = DatasetRef[object] | ResolvedDatasetRef[object]
RowT = TypeVar("RowT", bound=SchemaRecord)


class DatasetProvider(Protocol):
    """Resolve declared datasets and expose only their pinned files."""

    def path(self, reference: DatasetReference) -> Path:
        """Return a verified materialized dataset directory."""
        ...

    def manifest(self, reference: DatasetReference) -> DatasetFileManifest:
        """Read pinned file metadata without acquiring any media bytes."""
        ...

    def local_files(
        self, reference: DatasetReference, paths: Sequence[str]
    ) -> AbstractContextManager[Mapping[str, Path]]:
        """Lease only the selected files for the duration of decoding or consumption."""
        ...

    def file(self, reference: DatasetReference, path: str) -> Path:
        """Return one verified pinned file."""
        ...

    def asset(self, reference: DatasetReference, path: str) -> AssetRef:
        """Return the immutable asset identity of one pinned file."""
        ...

    def records(self, reference: DatasetReference, path: str | None = None) -> Iterable[dict[str, object]]:
        """Read validated logical JSON records from immutable materialized parts."""
        ...

    def rows(self, reference: DatasetRef[RowT]) -> Iterable[RowT]:
        """Decode into the generated row type carried by the dataset reference."""
        ...

    def local_file(self, reference: AssetRef) -> AbstractContextManager[Path]:
        """Lease one typed asset column as a verified local file at consumption time."""
        ...
