"""Retain explicit local mounts independently of bounded cache eviction."""

import errno
import os
import shutil
from collections.abc import Callable, Mapping
from pathlib import Path
from uuid import uuid4

from labqoat.cli.mount_asset_source import MountAssetSource
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.references import AssetRef, ResourceId, Sha256
from labqoat.storage.cache_lock import CacheLock
from labqoat.storage.cache_receipt import CacheReceipt
from labqoat.storage.shared_asset_cache import SharedAssetCache


class MountedAssetFile:
    """Keep a project-owned hardlink so a mount remains valid after CLI exit."""

    @staticmethod
    def acquire(
        root: Path, entry: Mapping[str, JsonValue], cache: SharedAssetCache, fetch: Callable[[str, Path], int]
    ) -> tuple[Path, bool]:
        """Acquire one verified blob, retaining it without copying on the same device."""
        asset = MountedAssetFile.reference(entry)
        anchor = root / ".labqoat" / "cache" / "sha256" / str(asset.blob_sha256)
        if anchor.is_symlink() or not anchor.resolve().is_relative_to(root.resolve()):
            raise ValueError("Mounted asset escapes its project cache")
        source = MountAssetSource(fetch)
        lock = CacheLock(anchor.parent / "locks" / str(asset.blob_sha256))
        try:
            lock.acquire()
            if not anchor.exists():
                with cache.local_file(asset, source) as path:
                    MountedAssetFile._retain(path, anchor)
                    CacheReceipt(anchor).record(asset)
            return CacheReceipt(anchor).validate(asset), source.downloaded
        finally:
            lock.close()

    @staticmethod
    def reference(entry: Mapping[str, JsonValue]) -> AssetRef:
        """Decode actual platform identities from the enriched manifest response."""
        return AssetRef(
            id=ResourceId.parse(JsonDocument.expect_scalar(entry.get("asset_id"), str)),
            blob_sha256=Sha256.parse(JsonDocument.expect_scalar(entry.get("sha256"), str)),
            byte_size=JsonDocument.expect_scalar(entry.get("byte_size"), int),
            media_type=JsonDocument.expect_scalar(entry.get("media_type"), str),
        )

    @staticmethod
    def _retain(source: Path, destination: Path) -> None:
        """Publish a persistent link or a verified cross-filesystem copy atomically."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        pending = destination.with_suffix(f".{uuid4()}.tmp")
        try:
            try:
                os.link(source, pending)
            except OSError as error:
                if error.errno != errno.EXDEV:
                    raise
                shutil.copyfile(source, pending)
                pending.chmod(0o444)
            pending.replace(destination)
        finally:
            pending.unlink(missing_ok=True)
