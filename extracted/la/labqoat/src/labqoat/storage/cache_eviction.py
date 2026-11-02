"""Bound retained cache bytes without removing actively leased assets."""

from dataclasses import dataclass
from pathlib import Path

from labqoat.storage.cache_lock import CacheLock


@dataclass(frozen=True, slots=True)
class CacheEviction:
    """Reclaim least-recently-used, unleased blobs after consumers release them."""

    root: Path
    maximum_bytes: int

    def trim(self) -> None:
        """Keep only the configured retained budget plus the active working set."""
        lock = CacheLock(self.root / "locks" / "eviction")
        try:
            if lock.acquire(blocking=False):
                self._trim()
        finally:
            lock.close()

    def _trim(self) -> None:
        """Account regular entries once and discard available oldest entries."""
        entries = [path for path in (self.root / "blobs").glob("[0-9a-f]" * 64) if path.is_file()]
        total = sum(path.stat().st_size for path in entries)
        for path in sorted(entries, key=self._accessed):
            if total <= self.maximum_bytes:
                break
            total -= self._remove(path)

    def _remove(self, path: Path) -> int:
        """Try exclusive ownership so open readers and downloads always win."""
        lock = CacheLock(self.root / "locks" / path.name)
        try:
            if not lock.acquire(blocking=False):
                return 0
            size = path.stat().st_size
            path.unlink()
            path.with_suffix(".verified.json").unlink(missing_ok=True)
            return size
        finally:
            lock.close()

    @staticmethod
    def _accessed(path: Path) -> int:
        """Order verified entries by their receipt's most recent access time."""
        receipt = path.with_suffix(".verified.json")
        return receipt.stat().st_mtime_ns if receipt.exists() else path.stat().st_mtime_ns
