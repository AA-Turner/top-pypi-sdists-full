from __future__ import annotations

import itertools
import traceback
import time
from datetime import datetime, timedelta
import sys
import threading
import typing as t

from collections import defaultdict, deque
from concurrent.futures import Future
from dataclasses import dataclass, field
from types import TracebackType

from sqlglot import exp, parse_one
from sqlglot.optimizer.qualify_tables import qualify_tables

from dbt_state.utils import find_tables
from query_cache_common.utils import extract_select_from_ctas

if t.TYPE_CHECKING:
    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self


@dataclass
class ViewTraversalResult:
    view_definitions: dict[str, ViewDefinition]
    """A mapping of view names to their SQL definitions. Each view name is fully qualified and quoted."""
    seen_tables: set[str]
    """A set of all fully qualified and quoted table names that were seen during the traversal."""
    unresolvable_tables: set[str]
    """A subset of seen_tables whose view definition could not be fetched"""

    @property
    def view_definition_sql(self) -> t.Dict[str, str]:
        return {k: v.definition for k, v in self.view_definitions.items()}


@dataclass
class ViewFetchResult:
    definitions: t.Collection["ViewDefinition"]
    unresolvable: t.Set[str] = field(default_factory=set)


@dataclass
class ViewDefinition:
    fqn: str
    definition: str
    dialect: str
    default_catalog: str  # catalog used to qualify unqualified references within the definition
    default_schema: str  # schema used to qualify unqualified references within the definition

    _parsed: t.Optional[exp.Expr] = None

    def parsed(self) -> exp.Expr:
        if not self._parsed:
            self._parsed = parse_one(self.definition, dialect=self.dialect)
        return self._parsed

    def extract_referenced_tables(self) -> t.Set[exp.Table]:
        query = self.parsed()
        if isinstance(query, exp.Create):
            query = extract_select_from_ctas(query)
        tables = find_tables(query)

        return {
            qualify_tables(
                t, db=self.default_schema, catalog=self.default_catalog, dialect=self.dialect
            )
            for t in tables
        }


K = t.TypeVar("K", bound=t.Hashable)
V = t.TypeVar("V")


@dataclass
class CacheEntry(t.Generic[V]):
    value: V
    cached_at: datetime
    no_expire: bool = False


@dataclass
class LockStats:
    min: timedelta = timedelta(seconds=0)
    max: timedelta = timedelta(seconds=0)
    count: int = 0
    _sum: timedelta = timedelta(seconds=0)

    _local: threading.local = field(default_factory=lambda: threading.local())

    @property
    def avg(self) -> timedelta:
        if self._sum.total_seconds() > 0 and self.count > 0:
            return self._sum / self.count
        return timedelta(seconds=0)

    @property
    def _last(self) -> t.Optional[float]:
        if hasattr(self._local, "last") and isinstance(self._local.last, float):
            return self._local.last
        return None

    @_last.setter
    def _last(self, value: t.Optional[float]) -> None:
        if value is None and hasattr(self._local, "last"):
            delattr(self._local, "last")
        else:
            self._local.last = value

    def start(self) -> None:
        self._last = time.monotonic()

    def finish(self) -> timedelta:
        if self._last is None:
            raise ValueError("start() must be called first")

        duration = self.elapsed()
        if duration < self.min:
            self.min = duration
        elif duration > self.max:
            self.max = duration

        self.count += 1
        self._sum += duration
        self._last = None

        return duration

    def cancel(self) -> None:
        self._last = None

    def elapsed(self) -> timedelta:
        if self._last is None:
            return timedelta(seconds=0)

        return timedelta(seconds=time.monotonic() - self._last)


@dataclass
class CacheStats:
    cache_name: str
    """The name of this cache, to distingish the stats from other caches"""

    acquire_lock_stats: LockStats = field(default_factory=lambda: LockStats())
    """Running stats of cache lock acquisition times (how long a thread took to acquire the lock)"""

    held_lock_stats: LockStats = field(default_factory=lambda: LockStats())
    """Running stats of lock held times (how long a thread held a lock)"""

    # time occurred, wait time, thread holding lock hold time, stack trace of thread holding lock
    lock_timeouts: t.Deque[t.Tuple[datetime, float, float, str]] = field(
        default_factory=lambda: deque(maxlen=10)
    )
    """The last 10 recorded lock timeouts"""

    cache_hits: int = 0
    """A value was served directly from the cache, because it was already cached"""
    inflight_cache_hits: int = 0
    """A thread requested a value that another thread was already fetching, leading to a Future being returned"""
    cache_misses: int = 0
    """A thread either claimed an unclaimed key or attempted to resolve a key that wasnt cached or inflight"""
    added_item_count: int = 0
    """How many items were added to the cache over its lifetime"""
    removed_item_count: int = 0
    """How many items were removed from the cache over its lifetime"""

    def start_lock_acquisition(self) -> None:
        self.acquire_lock_stats.start()

    def complete_lock_acquisition(self) -> timedelta:
        acquire_time = self.acquire_lock_stats.finish()
        self.held_lock_stats.start()
        return acquire_time

    def cancel_lock_acquisition(self) -> None:
        self.acquire_lock_stats.cancel()

    def add_lock_release(self) -> None:
        self.held_lock_stats.finish()

    def add_lock_timeout(
        self, after_seconds: float, waiting_on_thread_id: int, hold_time: float
    ) -> None:
        now = datetime.now()
        waiting_on_thread_stacktrace = ""

        frames = sys._current_frames()
        if frame := frames.get(waiting_on_thread_id):
            waiting_on_thread_stacktrace = "".join(traceback.format_stack(frame))

        self.lock_timeouts.append((now, after_seconds, hold_time, waiting_on_thread_stacktrace))

    def add_cache_hit(self) -> None:
        self.cache_hits += 1

    def add_cache_miss(self) -> None:
        self.cache_misses += 1

    def add_inflight_cache_hit(self) -> None:
        self.inflight_cache_hits += 1

    def add_cache_item_added(self) -> None:
        self.added_item_count += 1

    def add_cache_item_removed(self) -> None:
        self.removed_item_count += 1

    @property
    def contains_lock_timeouts(self) -> bool:
        return len(self.lock_timeouts) > 0

    def report(self) -> t.Dict[str, t.Any]:
        def _lock_stats(stats: LockStats) -> t.Dict[str, t.Any]:
            return {
                "fastest_acquisition_ms": stats.min.total_seconds() * 1000,
                "slowest_acquisition_ms": stats.max.total_seconds() * 1000,
                "average_acquisition_time_ms": stats.avg.total_seconds() * 1000,
                "acquisition_count": stats.count,
            }

        data = {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "inflight_hits": self.inflight_cache_hits,
            "added_item_count": self.added_item_count,
            "removed_item_count": self.removed_item_count,
            "lock_stats": {
                "acquisition": _lock_stats(self.acquire_lock_stats),
                "held": _lock_stats(self.held_lock_stats),
            },
            "timeouts": [],
        }

        if len(self.lock_timeouts):
            timeouts = []
            for timeout in self.lock_timeouts:
                event_time, wait_time_seconds, held_time_seconds, blocked_by_thread_stacktrace = (
                    timeout
                )
                timeouts.append(
                    {
                        "timestamp": event_time.isoformat(),
                        "timed_out_after_seconds": wait_time_seconds,
                        "other_thread_held_seconds": held_time_seconds,
                        "other_thread_stacktrace": blocked_by_thread_stacktrace,
                    }
                )

            data["timeouts"] = timeouts

        return data


class EventualCache(t.Generic[K, V]):
    """
    This cache is designed to be used from multiple threads where:
     - Each thread may need the same data
     - But, we don't want to issue competing requests to fetch the same data - this results in a bunch of duplicate effort
     - So, one thread needs to nominate itself as the "fetcher" for that piece of data
     - Other threads then wait for the first thread to finish fetching the data
     - Other threads are still free to nominate themselves as "fetchers" for different data that doesn't already have a nominated fetcher
     - Eventually, all the data will be available in the cache and the threads can return
    """

    def __init__(
        self,
        lock_wait_timeout_seconds: int = 10,
        ttl_seconds: t.Optional[int] = None,
        cache_name: str = "cache",
    ):
        if ttl_seconds is not None and ttl_seconds < 0:
            raise ValueError("ttl_seconds must be non-negative or None")
        self._cache: t.Dict[K, CacheEntry[V]] = {}
        self._inflight: t.Dict[K, Future[V]] = {}
        self._lock = threading.RLock()
        self._owner: t.Optional[int] = (
            None  # Rlock doesn't have an is_locked() method, so we track which thread currently "owns" the lock
        )
        self._last_acquired_time = time.monotonic()
        self._last_owner = threading.get_ident()
        self._timeout = lock_wait_timeout_seconds
        self._ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else None
        self._stats = CacheStats(cache_name=cache_name)

    def __enter__(self) -> Self:
        self._stats.start_lock_acquisition()

        if not self._lock.acquire(timeout=self._timeout):
            self._stats.add_lock_timeout(
                self._timeout, self._last_owner, time.monotonic() - self._last_acquired_time
            )
            self._stats.cancel_lock_acquisition()
            raise ValueError(
                f"Timed out waiting for '{self.stats.cache_name}' cache lock after {self._timeout} seconds (last owner: {self._last_owner})"
            )

        self._owner = threading.get_ident()
        self._last_acquired_time = time.monotonic()

        try:
            self.stats.complete_lock_acquisition()
        except:
            # if there is some error and we dont release the lock, it will be held forever
            self._lock.release()
            raise

        # always track the last owner, which is never None, so that when a lock acquisition timeout occurs
        # there is always something to log. just checking self._owner is racy because it can be cleared
        # between acquire() failing and add_lock_timeout() using it
        self._last_owner = self._owner

        return self

    def __exit__(
        self,
        type_: t.Optional[t.Type[BaseException]],
        value: t.Optional[BaseException],
        traceback: t.Optional[TracebackType],
    ) -> None:
        # self._owner needs to be cleared *before* releasing the lock. otherwise the following situation could happen:
        # 1. Thread A releases the lock
        # 2. Thread B acquires the lock and sets self._owner to its thread ID
        # 3. Thread A sets self._owner = None, corrupting Thread B's ownership tracking
        self._owner = None

        try:
            # Similarly, record the release *before* releasing the lock, to avoid races on LockStats
            # counters. Wrapped in a try-finally block as a defensive measure against any failures.
            self._stats.add_lock_release()
        finally:
            self._lock.release()

    def _is_expired(self, entry: CacheEntry[V]) -> bool:
        """Check if a cache entry has expired based on TTL."""
        if self._ttl is None or entry.no_expire:
            return False
        return (datetime.now() - entry.cached_at) > self._ttl

    def _check_lock(self) -> None:
        if self._owner is None:
            raise ValueError(
                "Cache must be used from a 'with:' statement (context manager) to ensure appropriate locking"
            )

        if self._owner != threading.get_ident():
            raise ValueError(
                "Cache is locked by another thread. Use a 'with:' statement to acquire the lock before proceeding"
            )

    def _contains(self, key: K) -> bool:
        if fut := self._inflight.get(key, None):
            # if the inflight request has been marked as failed, remove it
            if fut.done() and fut.exception():
                self._inflight.pop(key, None)
            else:
                return True

        if key in self._cache:
            entry = self._cache[key]
            if self._is_expired(entry):
                self._cache.pop(key, None)
                return False
            return True

        return False

    def claim(self, key: K) -> None:
        """The caller nominates themselves as being responsible for fetching the value
        aligned with this key.

        Subsequent calls to claim() for this key will raise an error

        This method raises a KeyError if the key has already been claimed
        """
        self._check_lock()

        if key in self._inflight or key in self._cache:
            raise KeyError(f"Key {key} is already claimed")

        self.stats.add_cache_miss()

        fut: Future[V] = Future()
        self._inflight[key] = fut

    def claim_if_available(self, key: K) -> bool:
        """Call is_available() and then immediately claim() if the key is available
        If the key is already claimed, return False to indicate the key is not available

        Calling this removes the need to manage the lock externally
        """
        self._check_lock()

        if self.is_available(key):
            self.claim(key)
            return True

        return False

    def is_available(self, key: K) -> bool:
        """Whether or not this key is available to be claimed"""
        return not self.is_claimed(key)

    def is_claimed(self, key: K) -> bool:
        """Whether or not this key has already been claimed"""
        return self.contains(key)

    def contains(self, key: K) -> bool:
        """Return True if this cache has seen the key before (either the value exists, or something is fetching it)"""
        self._check_lock()
        return self._contains(key)

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def fulfill(self, key: K, value: V, no_expire: bool = False) -> None:
        """Fulfill an inflight request.

        Note that if a key has not been claim()'d, this does not error and instead just populates the
        cache with the value.

        Args:
            key: The cache key.
            value: The value to cache.
            no_expire: If True, this entry will never expire regardless of the cache TTL.
        """
        self._check_lock()

        if fut := self._inflight.pop(key, None):
            fut.set_result(value)

        entry = CacheEntry(value=value, cached_at=datetime.now(), no_expire=no_expire)
        self._cache[key] = entry
        self._stats.add_cache_item_added()

    def fulfill_many(self, items: t.Mapping[K, V], no_expire: bool = False) -> None:
        """Convenience method to fulfill a bunch of items at the same time"""

        for k, v in items.items():
            self.fulfill(k, v, no_expire=no_expire)

    def resolve(self, key: K) -> t.Optional[Future[V]]:
        """Resolve a key to a value

        - If the key doesn't exist and has not been claimed, this will return None
        - If the key exists and is currently still being processed by whatever claimed it,
          this will return a pending Future[Value] that you will need to wait() on
        - If the key exists and has been processed / resolved to a value and is now cached,
          this will return a resolved Future[Value] that you can immediately call .result() on
        """
        self._check_lock()

        if not self._contains(key):
            self.stats.add_cache_miss()
            return None

        if key in self._inflight:
            self.stats.add_inflight_cache_hit()
            return self._inflight[key]

        self.stats.add_cache_hit()
        entry = self._cache[key]
        fut: Future[V] = Future()
        fut.set_result(entry.value)
        return fut

    def resolve_or_raise(self, key: K) -> Future[V]:
        """Same as resolve() except it will raise an error if the key isn't known to this cache"""
        fut = self.resolve(key)
        if not fut:
            raise KeyError("Cannot resolve unclaimed key")
        return fut

    def remove(self, keys: t.Collection[K]) -> None:
        """Remove the specified keys from the cache"""
        self._check_lock()

        for key in keys:
            self.cancel_inflight(key)
            self._inflight.pop(key, None)

            if _ := self._cache.pop(key, None):
                self._stats.add_cache_item_removed()

    def cancel_inflight(self, key: K) -> None:
        """If the specified key is inflight, cancel the future to advance any threads that may be wait()'ing on it.
        Note that the future is not removed from the inflight list, acquire the lock and use remove() for that.

        If the specified key is not inflight, this is a no-op.

        Note that the cache lock does not need to be acquired for this to prevent a situation where:
         - Thread B holds the lock
         - Thread A times out trying to acquire it
         - Thread A needs to cancel its inflight futures but it can't because Thread B still has the lock
        """
        if (fut := self._inflight.get(key, None)) and not fut.done():
            # note: we use fut.set_exception() instead of fut.cancel()
            # to work around: https://github.com/python/cpython/issues/109934
            fut.set_exception(RuntimeError("Future cancelled"))

    @property
    def stats(self) -> CacheStats:
        return self._stats


def build_information_schema_filter(
    tables: t.Collection[exp.Table],
    parts: t.Tuple[str, str] | t.Tuple[str, str, str],
) -> exp.Expr:
    """Build optimized WHERE filter using component-level filtering.

    Groups tables by schema and creates OR-based filter expressions like:
    (schema = 'S1' AND name IN ('T1', 'T2')) OR (schema = 'S2' AND name = 'T3')

    Args:
        tables: Collection of exp.Table objects
        parts: Tuple of INFORMATION_SCHEMA column names (2 or 3 parts)

    Returns:
        Expression representing the filter
    """

    is_three_part = len(parts) == 3
    catalog_col = parts[0] if is_three_part else None
    schema_col = parts[1] if is_three_part else parts[0]
    name_col = parts[2] if is_three_part else parts[1]  # type: ignore[misc]

    schema_groups: t.Dict[t.Tuple[str | None, str], t.Set[str]] = defaultdict(set)
    for table in tables:
        key = (table.catalog if is_three_part else None, table.db)
        schema_groups[key].add(table.name)

    or_conditions = []
    for (catalog_name, schema_value), table_names in sorted(schema_groups.items()):
        table_name_condition = (
            exp.column(name_col).isin(*sorted(table_names), copy=False)
            if len(table_names) > 1
            else exp.column(name_col).eq(next(iter(table_names)))
        )
        and_conditions = [
            exp.column(schema_col).eq(schema_value),
            table_name_condition,
        ]
        if catalog_col and catalog_name:
            and_conditions.insert(0, exp.column(catalog_col).eq(catalog_name))
        or_conditions.append(exp.and_(*and_conditions, copy=False))

    if len(or_conditions) == 1:
        return or_conditions[0]
    return exp.or_(*or_conditions, copy=False)


def group_tables_by_catalog(
    tables: t.Collection[exp.Table], default_catalog: str
) -> t.Dict[str, t.Collection[exp.Table]]:
    return {
        k: list(v)
        for k, v in itertools.groupby(
            sorted(tables, key=lambda t: t.catalog or default_catalog),
            key=lambda t: t.catalog or default_catalog,
        )
    }


def map_future_payload(future_a: Future[K], conversion_fn: t.Callable[[K], V]) -> Future[V]:
    """Map Future[A] -> Future[B] using the specified payload :conversion_fn"""
    future_b: Future[V] = Future()

    def _callback(f: Future[K]) -> None:
        try:
            future_b.set_result(conversion_fn(f.result()))
        except Exception as e:
            future_b.set_exception(e)

    future_a.add_done_callback(_callback)
    return future_b
