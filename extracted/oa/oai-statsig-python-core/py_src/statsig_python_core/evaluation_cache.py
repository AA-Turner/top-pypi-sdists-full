import math
import os
import sys
from collections import OrderedDict
from collections.abc import KeysView
from copy import deepcopy
from threading import RLock
from time import monotonic
from typing import Any, Optional
from weakref import WeakSet

from ._frozen_json import _FrozenDict, _deep_freeze_and_measure


_VALUE_CACHE_KEY_FIELD = "__statsig_dynamic_returnable_cache_key"
_VALUE_CACHE_HIT_FIELD = "__statsig_dynamic_returnable_cache_hit"
_CACHE_ENTRY_OVERHEAD_BYTES = 256


class _EvaluationCacheKeys(KeysView[int]):
    """Live key view that retains only values observed as native cache hits."""

    def __init__(self, cache: "EvaluationCache") -> None:
        super().__init__(cache._values)
        self._cache = cache
        self._hit_values: dict[int, _FrozenDict] = {}

    def __contains__(self, key: object) -> bool:
        if isinstance(key, bool) or not isinstance(key, int):
            return False

        cache = self._cache
        with cache._lock:
            cache._evict_expired_locked()
            value = cache._values.get(key)
            if value is None or key not in cache._entries:
                return False
            self._hit_values[key] = value
            return True

    def _get_hit_value(self, key: int) -> Optional[_FrozenDict]:
        return self._hit_values.get(key)


def _validate_positive_int(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _validate_positive_float(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a positive finite number")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be a positive finite number")
    return result


def _estimated_deep_size(value: Any, limit: int) -> int:
    """Estimate retained bytes, stopping once the cacheable limit is exceeded."""

    seen: set[int] = set()

    def visit(item: Any) -> int:
        item_id = id(item)
        if item_id in seen:
            return 0
        seen.add(item_id)

        size = sys.getsizeof(item)
        if size > limit:
            return size

        if isinstance(item, dict):
            for key, child in item.items():
                size += visit(key)
                if size > limit:
                    return size
                size += visit(child)
                if size > limit:
                    return size
        elif isinstance(item, list):
            for child in item:
                size += visit(child)
                if size > limit:
                    return size

        return size

    return visit(value)


class EvaluationCache:
    """Bounded cache for immutable converted DynamicReturnable values.

    Passing an instance through ``StatsigOptions(evaluation_cache=...)`` opts an
    SDK instance into sharing immutable converted config, experiment, and layer
    values across cache hits.
    The byte budget is an estimate of retained Python object sizes and is backed
    by independent entry-count, per-entry, and TTL limits.
    Cache state is safe to share across concurrent SDK calls and instances.
    """

    def __init__(
        self,
        *,
        max_bytes: int = 16 * 1024 * 1024,
        max_entries: int = 1024,
        max_entry_bytes: int = 1024 * 1024,
        ttl_seconds: float = 300.0,
    ) -> None:
        self._max_bytes = _validate_positive_int("max_bytes", max_bytes)
        self._max_entries = _validate_positive_int("max_entries", max_entries)
        self._max_entry_bytes = _validate_positive_int(
            "max_entry_bytes", max_entry_bytes
        )
        self._ttl_seconds = _validate_positive_float("ttl_seconds", ttl_seconds)

        if self._max_entry_bytes > self._max_bytes:
            raise ValueError("max_entry_bytes cannot exceed max_bytes")

        self._lock = RLock()
        self._values: dict[int, _FrozenDict] = {}
        self._entries: OrderedDict[int, tuple[float, int]] = OrderedDict()
        self._estimated_size_bytes = 0
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._oversized_bypasses = 0
        _EVALUATION_CACHES.add(self)

    @property
    def max_bytes(self) -> int:
        return self._max_bytes

    @property
    def max_entries(self) -> int:
        return self._max_entries

    @property
    def max_entry_bytes(self) -> int:
        return self._max_entry_bytes

    @property
    def ttl_seconds(self) -> float:
        return self._ttl_seconds

    @property
    def entry_count(self) -> int:
        with self._lock:
            return len(self._entries)

    @property
    def estimated_size_bytes(self) -> int:
        with self._lock:
            return self._estimated_size_bytes

    @property
    def hits(self) -> int:
        with self._lock:
            return self._hits

    @property
    def misses(self) -> int:
        with self._lock:
            return self._misses

    @property
    def evictions(self) -> int:
        with self._lock:
            return self._evictions

    @property
    def oversized_bypasses(self) -> int:
        with self._lock:
            return self._oversized_bypasses

    def clear(self) -> None:
        with self._lock:
            self._values.clear()
            self._entries.clear()
            self._estimated_size_bytes = 0

    def _values_for_call(self) -> dict[int, _FrozenDict]:
        with self._lock:
            self._evict_expired_locked()
            return self._values

    def _keys_for_call(self) -> _EvaluationCacheKeys:
        with self._lock:
            self._evict_expired_locked()
            return _EvaluationCacheKeys(self)

    def _consume_result(
        self,
        raw: dict,
        call_keys: Optional[_EvaluationCacheKeys] = None,
    ) -> None:
        cache_key = raw.pop(_VALUE_CACHE_KEY_FIELD, None)
        cache_hit = raw.pop(_VALUE_CACHE_HIT_FIELD, False)

        if isinstance(cache_key, bool) or not isinstance(cache_key, int):
            return

        if cache_hit:
            cached = call_keys._get_hit_value(cache_key) if call_keys else None
            with self._lock:
                if cached is None and cache_key in self._entries:
                    cached = self._values.get(cache_key)
                if cached is not None and cache_key in self._entries:
                    self._touch_locked(cache_key)
                if cached is not None:
                    self._hits += 1
            if cached is not None:
                raw["value"] = cached
                return

        with self._lock:
            self._misses += 1
        value = raw.get("value")
        if not isinstance(value, dict):
            return

        graph_limit = max(0, self._max_entry_bytes - _CACHE_ENTRY_OVERHEAD_BYTES)
        try:
            if _estimated_deep_size(value, graph_limit) > graph_limit:
                self._bypass_value(raw, value, cache_hit)
                return

            frozen_value, graph_size = _deep_freeze_and_measure(value)
        except (MemoryError, RecursionError):
            self._bypass_value(raw, value, cache_hit)
            return

        if not isinstance(frozen_value, _FrozenDict):
            return

        entry_size = graph_size + sys.getsizeof(cache_key) + _CACHE_ENTRY_OVERHEAD_BYTES
        if entry_size > self._max_entry_bytes or entry_size > self._max_bytes:
            self._bypass_value(raw, value, cache_hit)
            return

        with self._lock:
            self._store_locked(cache_key, frozen_value, entry_size)
        raw["value"] = frozen_value

    def _bypass_value(self, raw: dict, value: dict, cache_hit: bool) -> None:
        if cache_hit:
            try:
                raw["value"] = deepcopy(value)
            except (MemoryError, RecursionError):
                pass
        self._record_oversized_bypass()

    def _record_oversized_bypass(self) -> None:
        with self._lock:
            self._oversized_bypasses += 1

    def _store_locked(self, key: int, value: _FrozenDict, entry_size: int) -> None:
        self._remove_locked(key)

        while self._entries and (
            len(self._entries) >= self._max_entries
            or self._estimated_size_bytes + entry_size > self._max_bytes
        ):
            self._evict_oldest_locked()

        if (
            len(self._entries) >= self._max_entries
            or self._estimated_size_bytes + entry_size > self._max_bytes
        ):
            self._oversized_bypasses += 1
            return

        self._values[key] = value
        self._entries[key] = (monotonic() + self._ttl_seconds, entry_size)
        self._estimated_size_bytes += entry_size

    def _touch_locked(self, key: int) -> None:
        entry = self._entries.pop(key, None)
        if entry is None:
            self._values.pop(key, None)
            return

        _, entry_size = entry
        self._entries[key] = (monotonic() + self._ttl_seconds, entry_size)

    def _remove_locked(self, key: int) -> None:
        entry = self._entries.pop(key, None)
        self._values.pop(key, None)
        if entry is not None:
            self._estimated_size_bytes -= entry[1]

    def _evict_oldest_locked(self) -> None:
        key, (_, entry_size) = self._entries.popitem(last=False)
        self._values.pop(key, None)
        self._estimated_size_bytes -= entry_size
        self._evictions += 1

    def _evict_expired_locked(self) -> None:
        now = monotonic()
        while self._entries:
            _, (expires_at, _) = next(iter(self._entries.items()))
            if expires_at > now:
                break
            self._evict_oldest_locked()


_EVALUATION_CACHES: WeakSet[EvaluationCache] = WeakSet()
_FORK_LOCKED_EVALUATION_CACHES: list[EvaluationCache] = []


def _acquire_evaluation_cache_locks_before_fork() -> None:
    _FORK_LOCKED_EVALUATION_CACHES.clear()
    for cache in sorted(_EVALUATION_CACHES, key=id):
        cache._lock.acquire()
        _FORK_LOCKED_EVALUATION_CACHES.append(cache)


def _release_evaluation_cache_locks_after_fork() -> None:
    while _FORK_LOCKED_EVALUATION_CACHES:
        _FORK_LOCKED_EVALUATION_CACHES.pop()._lock.release()


def _reset_evaluation_cache_locks_after_fork() -> None:
    for cache in _FORK_LOCKED_EVALUATION_CACHES:
        cache._lock = RLock()
    _FORK_LOCKED_EVALUATION_CACHES.clear()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(
        before=_acquire_evaluation_cache_locks_before_fork,
        after_in_parent=_release_evaluation_cache_locks_after_fork,
        after_in_child=_reset_evaluation_cache_locks_after_fork,
    )


def _get_evaluation_cache(options: Any) -> Optional[EvaluationCache]:
    cache = getattr(options, "evaluation_cache", None) if options is not None else None
    if cache is None:
        return None
    if not isinstance(cache, EvaluationCache):
        raise TypeError("StatsigOptions.evaluation_cache must be an EvaluationCache")
    return cache


__all__ = ["EvaluationCache"]
