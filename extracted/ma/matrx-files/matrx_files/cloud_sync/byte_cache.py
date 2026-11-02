"""In-process LRU+TTL cache for recently-touched cloud-file bytes.

Why
---
When a user uploads an image and then submits an AI request seconds later,
the bytes are already on our server. Fetching them back from S3 (or
re-resolving share URLs) is wasted work. A small per-process cache lets
the AI / PDF / scraper layers hit memory instead of network.

Design
------
- Key: ``file_id`` (UUID from ``cld_files.id``).
- Value: ``CachedFile { bytes, mime_type, owner_id, file_path, file_size, cached_at }``.
- TTL: 10 minutes (configurable). Long enough that "upload then chat"
  flows hit cache, short enough not to hold stale bytes after updates.
- Bounded by total bytes (default 256 MB) — evict oldest first when full.
- Thread-safe (uses threading.Lock).
- Single shared instance via ``get_byte_cache()``.

Populated by:
- ``cloud_sync.SyncEngine.managed_write_async`` after every successful
  write (bytes are already in hand — caching them is free).
- ``FileManager.resolve_media_async`` after a successful URL → bytes
  resolution.

Invalidated by:
- Successful ``managed_delete_async`` (entry dropped).
- ``managed_write_async`` overwriting the file (entry replaced).
- TTL expiry on read.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class CachedFile:
    bytes_: bytes
    mime_type: str | None
    owner_id: str | None
    file_path: str | None
    file_size: int
    cached_at: float
    #: ``current_version`` of the row these bytes belong to, when the writer knew it.
    version: int | None = None

    def age_seconds(self) -> float:
        return time.monotonic() - self.cached_at


class FileByteCache:
    """LRU+TTL cache. Single-process; safe across asyncio + threads."""

    def __init__(self, *, max_total_bytes: int = 256 * 1024 * 1024, ttl_seconds: float = 600.0):
        self._max_total = max_total_bytes
        self._ttl = ttl_seconds
        self._store: OrderedDict[str, CachedFile] = OrderedDict()
        self._used = 0
        self._lock = threading.Lock()
        # Stats (cheap; useful in /health and tests)
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    def get(
        self,
        file_id: str | None,
        *,
        version: int | None = None,
        size_bytes: int | None = None,
    ) -> CachedFile | None:
        """The cached bytes, or None. A caller holding the row's CURRENT ``version`` / ``size_bytes`` gets a miss
        for bytes that no longer match: a replace on another server process cannot invalidate this process's
        cache, so without the check an edited PDF read back its old bytes for up to the TTL (Document
        properties saved, then read back empty)."""
        if not file_id:
            return None
        with self._lock:
            entry = self._store.get(file_id)
            if entry is None:
                self.misses += 1
                return None
            stale = (
                (version is not None and entry.version is not None and int(entry.version) != int(version))
                or (size_bytes is not None and int(size_bytes) != entry.file_size)
            )
            if stale:
                self._store.pop(file_id, None)
                self._used -= entry.file_size
                self.expirations += 1
                self.misses += 1
                return None
            if entry.age_seconds() > self._ttl:
                self._store.pop(file_id, None)
                self._used -= entry.file_size
                self.expirations += 1
                self.misses += 1
                return None
            self._store.move_to_end(file_id)
            self.hits += 1
            return entry

    def put(
        self,
        file_id: str | None,
        *,
        bytes_: bytes,
        mime_type: str | None = None,
        owner_id: str | None = None,
        file_path: str | None = None,
        version: int | None = None,
    ) -> None:
        if not file_id or bytes_ is None:
            return
        size = len(bytes_)
        if size > self._max_total:
            return  # Object alone exceeds cache capacity.
        entry = CachedFile(
            bytes_=bytes_,
            mime_type=mime_type,
            owner_id=owner_id,
            file_path=file_path,
            file_size=size,
            cached_at=time.monotonic(),
            version=version,
        )
        with self._lock:
            existing = self._store.pop(file_id, None)
            if existing is not None:
                self._used -= existing.file_size
            self._store[file_id] = entry
            self._used += size
            while self._used > self._max_total and self._store:
                k, v = self._store.popitem(last=False)
                self._used -= v.file_size
                self.evictions += 1

    def invalidate(self, file_id: str | None) -> None:
        if not file_id:
            return
        with self._lock:
            entry = self._store.pop(file_id, None)
            if entry is not None:
                self._used -= entry.file_size

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
            self._used = 0

    def stats(self) -> dict:
        with self._lock:
            return {
                "entries": len(self._store),
                "bytes_used": self._used,
                "max_total_bytes": self._max_total,
                "ttl_seconds": self._ttl,
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "expirations": self.expirations,
                "hit_rate": (self.hits / max(self.hits + self.misses, 1)),
            }


_singleton: FileByteCache | None = None


def get_byte_cache() -> FileByteCache:
    """Process-wide singleton."""
    global _singleton
    if _singleton is None:
        _singleton = FileByteCache()
    return _singleton


__all__ = ["CachedFile", "FileByteCache", "get_byte_cache"]
