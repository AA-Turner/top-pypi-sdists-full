"""Authorize every scoped asset read, whether its bytes are transferred or already on the node."""

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from labqoat.argument_codec import decode_result
from labqoat.references import AssetRef
from labqoat.storage.authorized_asset_source import AuthorizedAssetSource
from labqoat.storage.shared_asset_cache import SharedAssetCache
from labqoat.storage.worker_asset_source import WorkerAssetSource
from labqoat.worker import WorkerApi


@dataclass(frozen=True, slots=True)
class WorkerFileAccess:
    """Keep warm cache hits subject to the current assignment's asset authority."""

    api: WorkerApi
    cache: SharedAssetCache

    @contextmanager
    def local_file(self, reference: AssetRef | Mapping[str, object]) -> Iterator[Path]:
        """Authorize full immutable identity and lease the verified local bytes."""
        asset = reference if isinstance(reference, AssetRef) else decode_result(reference, AssetRef)
        source = AuthorizedAssetSource(WorkerAssetSource(self.api))
        with self.cache.local_file(asset, source) as path:
            source.confirm(asset)
            yield path
