"""On-demand content-addressed files shared by independent worker processes."""

import errno
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from labqoat.references import AssetRef
from labqoat.storage.asset_source import AssetSource
from labqoat.storage.cache_eviction import CacheEviction
from labqoat.storage.cache_lock import CacheLock
from labqoat.storage.cache_receipt import CacheReceipt
from labqoat.storage.temporary_asset_file import TemporaryAssetFile
from labqoat.storage.verified_file import VerifiedFile
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True, slots=True)
class SharedAssetCache:
    """Deduplicate acquisitions and lease verified paths for the consumer's scope.

    ``verify_always`` is for a cache directory that other runs can write to: nothing found there is believed
    until its bytes have been hashed by this process, and a file that fails is downloaded again.
    """

    root: Path
    maximum_bytes: int = 10 * 1024 * 1024 * 1024
    temporary_root: Path | None = None
    verify_always: bool = False

    def __post_init__(self) -> None:
        """Reject invalid budgets without creating files or opening connections."""
        if self.maximum_bytes < 1:
            raise ValueError("Asset cache budget must be positive")

    @contextmanager
    def local_file(self, reference: AssetRef, source: AssetSource) -> Iterator[Path]:
        """Acquire just one asset and protect it from eviction until scope exit."""
        if reference.byte_size > self.maximum_bytes:
            with self._temporary(reference, source) as path:
                yield path
            return
        target = self._target(reference)
        lock = CacheLock(self.root / "locks" / str(reference.blob_sha256))
        try:
            if self._acquire(reference, source, target, lock):
                yield self._verified(reference, source, target, lock)
            else:
                with self._temporary(reference, source) as path:
                    yield path
        finally:
            lock.close()
            CacheEviction(self.root, self.maximum_bytes).trim()

    def _verified(self, reference: AssetRef, source: AssetSource, target: Path, lock: CacheLock) -> Path:
        """Check the cached bytes; in a cache other runs write to, hash every time and replace what does not match."""
        if not self.verify_always:
            return CacheReceipt(target).validate(reference)
        try:
            return CacheReceipt(target, trusted=False).validate(reference)
        except ValueError:
            lock.close()
            lock.acquire()
            target.unlink(missing_ok=True)
            self._ensure(reference, source, target)
            lock.acquire(shared=True)
            return CacheReceipt(target, trusted=False).validate(reference)

    def _temporary(self, reference: AssetRef, source: AssetSource) -> AbstractContextManager[Path]:
        """Require explicitly owned scratch before bypassing shared-cache capacity."""
        if self.temporary_root is None:
            raise ValueError("Asset exceeds the configured cache budget")
        return TemporaryAssetFile(self.temporary_root).local_file(reference, source)

    def _acquire(self, reference: AssetRef, source: AssetSource, target: Path, lock: CacheLock) -> bool:
        """Reclaim idle bytes before transfer and release the cache lock before scratch fallback."""
        try:
            lock.acquire(shared=True)
            if not target.exists():
                lock.close()
                lock.acquire()
                CacheEviction(self.root, max(0, self.maximum_bytes - reference.byte_size)).trim()
                self._ensure(reference, source, target)
                lock.acquire(shared=True)
            return True
        except (OSError, WorkerApiError) as error:
            if self.temporary_root is None or not self._capacity_error(error):
                raise
            lock.close()
            return False

    @staticmethod
    def _capacity_error(error: BaseException) -> bool:
        """Recognize full filesystems and quotas through transfer exception wrappers."""
        visited: set[int] = set()
        current: BaseException | None = error
        while current is not None and id(current) not in visited:
            visited.add(id(current))
            if isinstance(current, OSError) and current.errno in (errno.ENOSPC, errno.EDQUOT):
                return True
            current = current.__cause__ or current.__context__
        return False

    def _target(self, reference: AssetRef) -> Path:
        """Reject cache paths redirected through unexpected symbolic links."""
        for name in ("blobs", "locks"):
            directory = self.root / name
            if directory.is_symlink():
                raise ValueError("Cache directories cannot be symlinks")
            directory.mkdir(parents=True, exist_ok=True)
        target = self.root / "blobs" / str(reference.blob_sha256)
        if target.is_symlink():
            raise ValueError("Cached assets cannot be symlinks")
        return target

    @staticmethod
    def _ensure(reference: AssetRef, source: AssetSource, target: Path) -> None:
        """Publish one verified transfer while holding the digest's exclusive lock."""
        if target.exists():
            return
        with NamedTemporaryFile(prefix=".download-", dir=target.parent, delete=False) as temporary:
            pending = Path(temporary.name)
        try:
            source.download_to(reference, pending)
            VerifiedFile.validate(pending, str(reference.blob_sha256), reference.byte_size)
            pending.chmod(0o444)
            pending.replace(target)
            CacheReceipt(target).record(reference)
        finally:
            pending.unlink(missing_ok=True)
