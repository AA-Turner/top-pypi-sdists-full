from __future__ import annotations

import time
from collections import OrderedDict
from typing import TypeVar

T = TypeVar("T")

class TTLCache[T]:
    """Generic TTL + LRU cache.

    - Items expire after `ttl_seconds` of inactivity (last access, not creation).
    - When `max_size` is reached, the least-recently-used item is evicted.
    - `get()` refreshes the TTL (marks the item as recently used).
    - Thread-safe for single-threaded async (no locks needed with asyncio).
    """

    def __init__(self, ttl_seconds: int = 1800, max_size: int = 200):
        self._ttl = ttl_seconds
        self._max_size = max_size
        self._store: OrderedDict[str, T] = OrderedDict()
        self._timestamps: dict[str, float] = {}

    def get(self, key: str) -> T | None:
        if key not in self._store:
            return None

        if self._is_expired(key):
            self._remove(key)
            return None

        self._store.move_to_end(key)
        self._timestamps[key] = time.monotonic()
        return self._store[key]

    def set(self, key: str, value: T) -> None:
        if key in self._store:
            self._store.move_to_end(key)
            self._store[key] = value
            self._timestamps[key] = time.monotonic()
            return

        self._evict_expired()

        while len(self._store) >= self._max_size:
            oldest_key, _ = self._store.popitem(last=False)
            self._timestamps.pop(oldest_key, None)

        self._store[key] = value
        self._timestamps[key] = time.monotonic()

    def remove(self, key: str) -> None:
        self._remove(key)

    def exists(self, key: str) -> bool:
        if key not in self._store:
            return False
        if self._is_expired(key):
            self._remove(key)
            return False
        return True

    def clear(self) -> None:
        self._store.clear()
        self._timestamps.clear()

    @property
    def size(self) -> int:
        return len(self._store)

    def _is_expired(self, key: str) -> bool:
        ts = self._timestamps.get(key, 0)
        return (time.monotonic() - ts) > self._ttl

    def _remove(self, key: str) -> None:
        self._store.pop(key, None)
        self._timestamps.pop(key, None)

    def _evict_expired(self) -> None:
        now = time.monotonic()
        expired = [k for k, ts in self._timestamps.items() if (now - ts) > self._ttl]
        for k in expired:
            self._remove(k)
