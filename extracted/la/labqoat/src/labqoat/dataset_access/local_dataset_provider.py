"""Read-only local dataset injection with exact file verification."""

from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from labqoat.dataset_access.dataset_asset_index import DatasetAssetIndex
from labqoat.dataset_access.dataset_input import DatasetInput
from labqoat.dataset_access.dataset_provider import DatasetReference
from labqoat.dataset_access.schema_rows import SchemaRows
from labqoat.dataset_files import DatasetFileManifest
from labqoat.references import AssetRef, DatasetRef, ResolvedDatasetRef
from labqoat.references.dataset_binding import DatasetBinding
from labqoat.schemas import SchemaRecord
from labqoat.storage.file_access import FileAccess
from labqoat.storage.verified_file import VerifiedFile

RowT = TypeVar("RowT", bound=SchemaRecord)


@dataclass(frozen=True, slots=True)
class LocalDatasetProvider:
    """Expose caller-pinned local files using the same dataset API as workers."""

    inputs: tuple[DatasetInput, ...]
    assets: FileAccess | None = None
    _references: DatasetAssetIndex = field(default_factory=DatasetAssetIndex, compare=False, repr=False)

    def _input(self, reference: DatasetReference) -> DatasetInput:
        """Resolve only explicitly injected datasets without consulting latest."""
        selected = (
            reference
            if isinstance(reference, ResolvedDatasetRef)
            else DatasetBinding.select(reference, tuple(item.reference for item in self.inputs))
        )
        matches = tuple(item for item in self.inputs if item.reference == selected)
        if len(matches) != 1:
            raise ValueError("Dataset reference does not identify one pinned input")
        return matches[0]

    def path(self, reference: DatasetReference) -> Path:
        """Verify every indexed file before exposing the dataset directory."""
        selected = self._input(reference)
        for item in selected.manifest.files:
            self.file(reference, item.path)
        return selected.root

    def manifest(self, reference: DatasetReference) -> DatasetFileManifest:
        """Return injected metadata without reading dataset file contents."""
        return self._input(reference).manifest

    @contextmanager
    def local_files(self, reference: DatasetReference, paths: Sequence[str]) -> Iterator[Mapping[str, Path]]:
        """Resolve a subset using the same scoped interface as managed workers."""
        selected = {path: self.asset(reference, path) for path in paths}
        yield {path: self.file(reference, path) for path in selected}

    def asset(self, reference: DatasetReference, path: str) -> AssetRef:
        """Return a declared asset identity, rejecting unindexed paths."""
        for item in self._input(reference).manifest.files:
            if item.path == path:
                return item.asset
        raise ValueError("File is not present in the pinned dataset")

    def file(self, reference: DatasetReference, path: str) -> Path:
        """Verify the selected file's containment, size, and digest."""
        selected = self._input(reference)
        asset = self.asset(reference, path)
        target = selected.root / VerifiedFile.relative(path)
        if not target.resolve().is_relative_to(selected.root.resolve()) or target.is_symlink():
            raise ValueError("Dataset file escapes its pinned directory")
        return VerifiedFile.validate(target, str(asset.blob_sha256), asset.byte_size)

    def records(self, reference: DatasetReference, path: str | None = None) -> Iterator[dict[str, object]]:
        """Read the captured physical layout with the same validation as managed workers."""
        from labqoat.dataset_access.revision_records import RevisionRecords

        selected = self._input(reference)
        names = tuple(item.path for item in selected.manifest.files) if path is None else (path,)
        for name in names:
            with self.local_files(reference, (name,)) as files:
                yield from RevisionRecords.read(selected.revision, name, files[name], self._references)

    def rows(self, reference: DatasetRef[RowT]) -> Iterable[RowT]:
        """Return the reference's generated record type without a second authored declaration."""
        self._input(reference)
        return SchemaRows.read(self.records(reference), reference.record_type)

    @contextmanager
    def local_file(self, reference: AssetRef) -> Iterator[Path]:
        """Open an asset column through its exact pinned file membership."""
        for selected in self.inputs:
            for member in selected.manifest.files:
                if member.asset == reference:
                    yield self.file(selected.reference, member.path)
                    return
        if self._references.revision(reference) is None:
            raise ValueError("Asset is not present in the pinned dataset")
        if self.assets is None:
            raise ValueError("Dataset asset content is unavailable locally")
        with self.assets.local_file(reference) as path:
            yield VerifiedFile.validate(path, str(reference.blob_sha256), reference.byte_size)

    def close(self) -> None:
        """Release the local provider's disk-backed reference membership."""
        self._references.close()
