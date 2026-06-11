import threading
import typing as t


class MemorySharedCounter:
    """In-memory ``SharedCounter`` for tests. The internal lock supports
    concurrent use in the same test; TTL is not modelled."""

    def __init__(self) -> None:
        self._counters: t.Dict[str, int] = {}
        self._lock = threading.Lock()

    def increment(self, key: str, amount: int, ttl_seconds: int) -> int:
        del ttl_seconds
        with self._lock:
            new_value = self._counters.get(key, 0) + amount
            self._counters[key] = new_value
        return new_value
