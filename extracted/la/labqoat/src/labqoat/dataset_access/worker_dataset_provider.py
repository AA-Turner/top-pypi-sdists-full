"""Verified file dataset materialization for authored workers."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

from labqoat.argument_codec import decode_result
from labqoat.dataset_access.dataset_asset_index import DatasetAssetIndex
from labqoat.dataset_access.dataset_provider import DatasetReference
from labqoat.dataset_access.dataset_requester import DatasetRequester
from labqoat.dataset_access.dataset_view import DatasetView
from labqoat.dataset_access.schema_rows import SchemaRows
from labqoat.dataset_files import DatasetFileManifest
from labqoat.references import AssetRef, DatasetRef, ResolvedDatasetRef, ResourceId
from labqoat.references.dataset_binding import DatasetBinding
from labqoat.schemas import SchemaRecord
from labqoat.storage.asset_source import AssetSource
from labqoat.storage.cache_receipt import CacheReceipt
from labqoat.storage.shared_asset_cache import SharedAssetCache

if TYPE_CHECKING:
    from labqoat.dataset_access.revision_files import RevisionFiles

RowT = TypeVar("RowT", bound=SchemaRecord)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkerDatasetProvider:
    """Materialize only pinned file bytes and validate their content identities."""

    requester: DatasetRequester
    inputs: tuple[ResolvedDatasetRef[object], ...]
    root: Path
    cache: SharedAssetCache | None = None
    _manifests: dict[ResourceId, DatasetFileManifest] = field(default_factory=dict, compare=False, repr=False)
    _revisions: dict[ResourceId, RevisionFiles] = field(default_factory=dict, compare=False, repr=False)
    _files: dict[ResourceId, dict[str, AssetRef]] = field(default_factory=dict, compare=False, repr=False)
    _assets: dict[AssetRef, ResolvedDatasetRef[object]] = field(default_factory=dict, compare=False, repr=False)
    _references: DatasetAssetIndex = field(default_factory=DatasetAssetIndex, compare=False, repr=False)
    _paths: dict[AssetRef, Path] = field(default_factory=dict, compare=False, repr=False)
    _leases: ExitStack = field(default_factory=ExitStack, compare=False, repr=False)

    def __post_init__(self) -> None:
        """Reject duplicate input revision declarations."""
        revisions = tuple(item.revision_id for item in self.inputs)
        if len(revisions) != len(set(revisions)):
            raise ValueError("Worker dataset inputs must be unique")

    def manifest(self, reference: DatasetReference) -> DatasetFileManifest:
        """Read immutable file membership without downloading media files."""
        from labqoat.dataset_access.revision_files import RevisionFiles

        selected = self._resolve(reference)
        cached = self._manifests.get(selected.revision_id)
        if cached is not None:
            return cached
        response = self.requester.dataset_request("manifest", {"revision_id": str(selected.revision_id)})
        if not isinstance(response, RevisionFiles) or response.reference != selected:
            raise ValueError("Worker dataset response does not match the pinned input")
        manifest = response.manifest
        files = manifest.files
        self._files[selected.revision_id] = {item.path: item.asset for item in files}
        self._assets.update({item.asset: selected for item in files})
        self._manifests[selected.revision_id] = manifest
        self._revisions[selected.revision_id] = response
        return manifest

    def asset(self, reference: DatasetReference, path: str) -> AssetRef:
        """Return an indexed file's exact immutable asset identity."""
        selected = self._resolve(reference)
        self.manifest(selected)
        asset = self._files[selected.revision_id].get(path)
        if asset is None:
            raise ValueError("File is not present in the pinned dataset")
        return asset

    def file(self, reference: DatasetReference, path: str) -> Path:
        """Download and verify one indexed file."""
        asset = self.asset(reference, path)
        return self._cached(asset)

    @contextmanager
    def local_files(self, reference: DatasetReference, paths: Sequence[str]) -> Iterator[Mapping[str, Path]]:
        """Validate a selection before acquiring it and release every lease on exit."""
        selected = {path: self.asset(reference, path) for path in paths}
        with ExitStack() as leases:
            acquired = {
                asset: leases.enter_context(self.local_file(asset))
                for asset in sorted(set(selected.values()), key=self._digest)
            }
            yield {path: acquired[asset] for path, asset in selected.items()}

    def records(self, reference: DatasetReference, path: str | None = None) -> Iterator[dict[str, object]]:
        """Stream validated logical rows from verified materialized Parquet parts."""
        selected = self._resolve(reference)
        manifest = self.manifest(selected)
        paths = tuple(item.path for item in manifest.files) if path is None else (path,)
        for name in paths:
            yield from self._part_rows(selected, name)

    def _part_rows(self, selected: ResolvedDatasetRef[object], name: str) -> Iterator[dict[str, object]]:
        """Retain one file lease while validating physical rows and explicit asset positions."""
        from labqoat.dataset_access.revision_records import RevisionRecords

        with self.local_files(selected, (name,)) as files:
            yield from RevisionRecords.read(self._revisions[selected.revision_id], name, files[name], self._references)

    def rows(self, reference: DatasetRef[RowT]) -> Iterable[RowT]:
        """Infer row types from generated bindings and retain every acquired part lease."""
        self._resolve(reference)
        return SchemaRows.read(self.records(reference), reference.record_type)

    def path(self, reference: DatasetReference) -> Path:
        """Build a safe view containing only the pinned manifest files."""
        selected = self._resolve(reference)
        manifest = self.manifest(selected)
        files = {item.path: self.file(selected, item.path) for item in manifest.files}
        return DatasetView(self.root, self._cache().root).publish(selected.revision_id, manifest.sha256(), files)

    @contextmanager
    def local_file(self, reference: AssetRef | Mapping[str, object]) -> Iterator[Path]:
        """Lease a complete file reference only when it belongs to a pinned input."""
        asset = reference if isinstance(reference, AssetRef) else decode_result(reference, AssetRef)
        for selected in self.inputs:
            self.manifest(selected)
        if self._asset_dataset(asset) is None:
            raise ValueError("Asset is not present in the pinned dataset")
        self.requester.authorize(asset)
        with self._cache().local_file(asset, self) as path:
            yield path

    def _resolve(self, reference: DatasetReference) -> ResolvedDatasetRef[object]:
        """Match immutable references exactly and require one family binding."""
        if isinstance(reference, ResolvedDatasetRef):
            matches = tuple(item for item in self.inputs if item == reference)
        else:
            return DatasetBinding.select(reference, self.inputs)
        if len(matches) != 1:
            raise ValueError("Dataset reference does not identify one pinned input")
        return matches[0]

    def _cached(self, asset: AssetRef) -> Path:
        """Retain unscoped paths until this provider is explicitly closed."""
        self.requester.authorize(asset)
        if asset not in self._paths:
            self._paths[asset] = self._leases.enter_context(self._cache().local_file(asset, self))
        return CacheReceipt(self._paths[asset]).validate(asset)

    def download_to(self, reference: AssetRef, destination: Path) -> None:
        """Transfer only an asset discovered in this provider's pinned metadata."""
        dataset = self._asset_dataset(reference)
        if dataset is None:
            raise ValueError("Asset is not present in the pinned dataset")
        content = self.requester.dataset_request(
            "download", {"revision_id": str(dataset.revision_id), "sha256": str(reference.blob_sha256)}
        )
        if isinstance(content, AssetSource):
            content.download_to(reference, destination)
        elif isinstance(content, bytes):
            destination.write_bytes(content)
        else:
            raise ValueError("Dataset download did not return bytes or a file source")

    def close(self) -> None:
        """Release path leases at the end of a worker or local run."""
        self._leases.close()
        self._paths.clear()
        self._references.close()

    def _asset_dataset(self, reference: AssetRef) -> ResolvedDatasetRef[object] | None:
        """Resolve materialized parts or exact references discovered in schema-owned positions."""
        output = self._assets.get(reference)
        if output is not None:
            return output
        revision = self._references.revision(reference)
        return next((item for item in self.inputs if item.revision_id == revision), None)

    def _cache(self) -> SharedAssetCache:
        """Use the injected node cache or an explicitly owned private fallback."""
        return self.cache if self.cache is not None else SharedAssetCache(self.root / "assets")

    @staticmethod
    def _digest(asset: AssetRef) -> str:
        """Acquire multi-file leases in stable content order."""
        return str(asset.blob_sha256)
