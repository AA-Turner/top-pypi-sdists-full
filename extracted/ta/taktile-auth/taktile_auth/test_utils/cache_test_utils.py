import threading
import typing as t


class MemoryCache:
    """Only for testing purposes. Internal lock supports concurrent
    use in the same test."""

    def __init__(self) -> None:
        self._cache: t.Dict[str, str] = {}
        self._counters: t.Dict[str, int] = {}
        self._lock = threading.Lock()

    def get(
        self, key: str, *, skip_local_cache: bool = False
    ) -> t.Optional[str]:
        del skip_local_cache  # single-tier, nothing to skip
        return self._cache.get(key)

    def put(
        self, key: str, value: str, time_to_live: t.Optional[int] = None
    ) -> None:
        del time_to_live
        self._cache[key] = value

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
        if key in self._counters:
            del self._counters[key]

    def put_marker(self, key: str, ttl_seconds: int) -> bool:
        del ttl_seconds
        if key in self._cache:
            return False
        self._cache[key] = ""
        return True

    def increment(self, key: str, amount: int, ttl_seconds: int) -> int:
        del ttl_seconds  # in-memory: TTL is not modelled
        with self._lock:
            new_value = self._counters.get(key, 0) + amount
            self._counters[key] = new_value
        return new_value


class TwoTierMemoryCache:
    """Simulates DynamoDBCache with local_cache_max_entries > 0.

    - _local: per-instance in-memory cache (like Lambda's local cache)
    - _shared: backing store (like DynamoDB, shared across instances)
    - get() checks local first, falls through to shared on miss
    - put() writes to both local and shared
    - put_marker() only touches shared (like DDB conditional write)
    """

    def __init__(self) -> None:
        self._local: t.Dict[str, str] = {}
        self._shared: t.Dict[str, str] = {}
        self._counters: t.Dict[str, int] = {}
        self._lock = threading.Lock()

    def get(
        self, key: str, *, skip_local_cache: bool = False
    ) -> t.Optional[str]:
        if not skip_local_cache and key in self._local:
            return self._local[key]
        value = self._shared.get(key)
        if value is not None:
            self._local[key] = value
        return value

    def put(
        self, key: str, value: str, time_to_live: t.Optional[int] = None
    ) -> None:
        del time_to_live
        self._local[key] = value
        self._shared[key] = value

    def delete(self, key: str) -> None:
        self._local.pop(key, None)
        self._shared.pop(key, None)
        self._counters.pop(key, None)

    def put_marker(self, key: str, ttl_seconds: int) -> bool:
        del ttl_seconds
        if key in self._shared:
            return False
        self._shared[key] = ""
        return True

    def increment(self, key: str, amount: int, ttl_seconds: int) -> int:
        del ttl_seconds
        with self._lock:
            new_value = self._counters.get(key, 0) + amount
            self._counters[key] = new_value
        return new_value
