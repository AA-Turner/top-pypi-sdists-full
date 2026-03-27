#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from snowflake.snowpark import Session
from snowflake.snowpark_connect.utils.concurrent import ReadWriteLock, SynchronizedDict
from snowflake.snowpark_connect.utils.context import get_spark_session_id

if TYPE_CHECKING:
    from snowflake.snowpark_connect.utils.udf_helper import SnowparkUDF


class UdfMonitor:
    """Single-lock monitor that owns both the external (hash-keyed) UDF cache
    and the per-session (name-keyed) UDF registry.

    All operations acquire the same ``ReadWriteLock``, eliminating nested-lock
    hazards and making cross-index operations like ``drop`` atomic.
    """

    def __init__(self) -> None:
        self._lock = ReadWriteLock()
        self._cached: dict[int, SnowparkUDF] = {}
        self._registered: dict[str, SnowparkUDF] = {}

    # -- registered (by user-facing name) ------------------------------------

    def register(self, name: str, udf: SnowparkUDF) -> None:
        with self._lock.writer():
            self._registered[name] = udf

    def get(self, name: str) -> SnowparkUDF | None:
        with self._lock.reader():
            return self._registered.get(name)

    def has(self, name: str) -> bool:
        with self._lock.reader():
            return name in self._registered

    def drop(self, name: str) -> None:
        """Atomically remove a registered UDF and evict any stale cached
        entries that reference the same Snowflake function name."""
        with self._lock.writer():
            udf_entry = self._registered.pop(name, None)
            if udf_entry is not None:
                sf_name = getattr(udf_entry, "name", None)
                if sf_name:
                    self._cached = {
                        k: v
                        for k, v in self._cached.items()
                        if getattr(v, "name", None) != sf_name
                    }

    # -- cached (by proto hash) ----------------------------------------------

    def get_cached(self, udf_hash: int) -> SnowparkUDF | None:
        with self._lock.reader():
            return self._cached.get(udf_hash)

    def cache(self, udf_hash: int, udf: SnowparkUDF) -> None:
        """Cache *udf* under *udf_hash*, first evicting any prior entry that
        shares the same Snowflake function name (prevents stale cache hits
        after a CREATE OR REPLACE)."""
        with self._lock.writer():
            sf_name = udf.name
            self._cached = {
                k: v
                for k, v in self._cached.items()
                if getattr(v, "name", None) != sf_name
            }
            self._cached[udf_hash] = udf

    # -- lifecycle -----------------------------------------------------------

    def clear_cached(self) -> None:
        with self._lock.writer():
            self._cached.clear()

    def clear_registered(self) -> None:
        with self._lock.writer():
            self._registered.clear()

    def clear(self) -> None:
        with self._lock.writer():
            self._cached.clear()
            self._registered.clear()


class UdtfMonitor:
    """Single-lock monitor that owns both the external (hash-keyed) UDTF cache
    and the per-session (name-keyed) UDTF registry.
    """

    def __init__(self) -> None:
        self._lock = ReadWriteLock()
        self._cached: dict[int, object] = {}
        self._registered: dict[str, tuple] = {}

    # -- registered (by user-facing name) ------------------------------------

    def register(self, name: str, udtf, spark_column_names=None) -> None:
        with self._lock.writer():
            self._registered[name] = (udtf, spark_column_names)

    def get(self, name: str):
        with self._lock.reader():
            return self._registered.get(name)

    def has(self, name: str) -> bool:
        with self._lock.reader():
            return name in self._registered

    def drop(self, name: str) -> None:
        """Atomically remove a registered UDTF and evict any stale cached
        entries that reference the same Snowflake function name."""
        with self._lock.writer():
            udtf_entry = self._registered.pop(name, None)
            if udtf_entry is not None:
                udtf_obj = (
                    udtf_entry[0] if isinstance(udtf_entry, tuple) else udtf_entry
                )
                sf_name = getattr(udtf_obj, "name", None)
                if sf_name:
                    self._cached = {
                        k: v
                        for k, v in self._cached.items()
                        if getattr(v, "name", None) != sf_name
                    }

    # -- cached (by proto hash) ----------------------------------------------

    def get_cached(self, udf_hash: int):
        with self._lock.reader():
            return self._cached.get(udf_hash)

    def cache(self, udf_hash: int, udtf) -> None:
        with self._lock.writer():
            self._cached[udf_hash] = udtf

    # -- lifecycle -----------------------------------------------------------

    def clear_cached(self) -> None:
        with self._lock.writer():
            self._cached.clear()

    def clear_registered(self) -> None:
        with self._lock.writer():
            self._registered.clear()

    def clear(self) -> None:
        with self._lock.writer():
            self._cached.clear()
            self._registered.clear()


class SparkSessionCache:
    """Per-Spark-session cache that isolates cached objects across different
    Spark sessions sharing the same underlying Snowpark session.

    Each Spark session that connects to the server gets its own
    ``SparkSessionCache`` instance, keyed by the Spark session ID.
    Thread safety is provided by the monitors' internal locks.
    """

    def __init__(self, spark_session_id: str) -> None:
        self._spark_session_id = spark_session_id
        self.udfs = UdfMonitor()
        self.udtfs = UdtfMonitor()

    @property
    def spark_session_id(self) -> str:
        return self._spark_session_id

    def clear_cached(self) -> None:
        """Clear only the external proto-hash caches (e.g. after artifact
        changes) without touching the per-session registries."""
        self.udfs.clear_cached()
        self.udtfs.clear_cached()

    def clear(self) -> None:
        """Drop all cached objects for this Spark session."""
        self.udfs.clear()
        self.udtfs.clear()


class SparkSessionCacheRegistry(SynchronizedDict):
    """Thread-safe registry that maps Spark session IDs to their
    ``SparkSessionCache`` instances.

    A single ``SparkSessionCacheRegistry`` is attached to each Snowpark
    ``Session`` during ``configure_snowpark_session()``.  It is the
    authoritative owner of all per-Spark-session caches.
    """

    def get_or_create(self, spark_session_id: str) -> SparkSessionCache:
        with self._lock.writer():
            cache = self._dict.get(spark_session_id)
            if cache is None:
                cache = SparkSessionCache(spark_session_id)
                self._dict[spark_session_id] = cache
            return cache

    def remove(self, spark_session_id: str) -> None:
        """Remove and clear the cache for a specific Spark session."""
        cache = SynchronizedDict.remove(self, spark_session_id)
        if cache is not None:
            cache.clear()

    def clear(self) -> None:
        """Clear all individual session caches, then drop them."""
        for _, cache in self.items():
            cache.clear()
        SynchronizedDict.clear(self)


# -- Module-level convenience API --------------------------------------------
# Thin wrappers that look up the active Snowpark session and current
# Spark session ID so callers don't have to thread those values through
# manually.


def init_spark_session_cache_registry(session: Session) -> None:
    """Attach a fresh ``SparkSessionCacheRegistry`` to *session*.

    Called once from ``configure_snowpark_session()`` when a new Snowpark
    session is created.
    """
    session._spark_session_cache_registry = SparkSessionCacheRegistry()


def get_spark_session_cache() -> SparkSessionCache:
    """Return the ``SparkSessionCache`` for the current (or given) Spark
    session, creating one if it doesn't exist yet."""
    spark_session_id = get_spark_session_id()
    registry: SparkSessionCacheRegistry = (
        Session.get_active_session()._spark_session_cache_registry
    )
    return registry.get_or_create(spark_session_id)


def clear_spark_session_cache(spark_session_id: str) -> None:
    """Clear only the external (hash-keyed) caches for a Spark session.

    Called when artifacts or imports change and cached UDXFs need to be
    recreated.  The per-session name registries are left intact.
    """
    if spark_session_id is None:
        raise ValueError(
            "Failed to clear spark session cache: spark_session_id is required."
        )
    registry: SparkSessionCacheRegistry = (
        Session.get_active_session()._spark_session_cache_registry
    )
    cache = registry.get(spark_session_id)
    if cache is not None:
        cache.clear_cached()
