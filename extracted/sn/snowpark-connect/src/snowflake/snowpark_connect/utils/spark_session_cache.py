#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from snowflake.snowpark import Session
from snowflake.snowpark_connect.utils.artifacts import ArtifactKey
from snowflake.snowpark_connect.utils.concurrent import ReadWriteLock, SynchronizedDict
from snowflake.snowpark_connect.utils.context import get_spark_session_id

if TYPE_CHECKING:
    from snowflake.snowpark_connect.utils.udf_helper import SnowparkUdfBase


class UdfMonitor:
    """Single-lock monitor that owns both the external (hash-keyed) UDF cache
    and the per-session (name-keyed) UDF registry.

    All operations acquire the same ``ReadWriteLock``, eliminating nested-lock
    hazards and making cross-index operations like ``drop`` atomic.
    """

    def __init__(self) -> None:
        self._lock = ReadWriteLock()
        self._cached: dict[int, SnowparkUdfBase] = {}
        self._registered: dict[str, SnowparkUdfBase] = {}

    # -- registered (by user-facing name) ------------------------------------

    def register(self, name: str, udf: SnowparkUdfBase) -> None:
        with self._lock.writer():
            self._registered[name] = udf

    def get(self, name: str) -> SnowparkUdfBase | None:
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

    def get_cached(self, udf_hash: int) -> SnowparkUdfBase | None:
        with self._lock.reader():
            return self._cached.get(udf_hash)

    def cache(self, udf_hash: int, udf: SnowparkUdfBase) -> None:
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


class _ArtifactStoreWriter:
    """Non-locking accessor yielded by ``ArtifactStore.writer()``.

    All mutations bypass locking because the caller already holds
    ``_filenames_lock`` in write mode for the entire ``with`` block.
    """

    def __init__(self, store: ArtifactStore) -> None:
        self._store = store

    def drain_filenames(self) -> dict[str, str]:
        result = dict(self._store._filenames)
        self._store._filenames.clear()
        return result

    def add_python_file(self, path: str) -> None:
        self._store._python_files.add(path)

    def remove_python_file(self, path: str) -> None:
        self._store._python_files.discard(path)

    def has_python_file(self, path: str) -> bool:
        return path in self._store._python_files

    def add_import_file(self, path: str) -> None:
        self._store._import_files.add(path)

    def add_jar(self, path: str) -> None:
        self._store._jars.add(path)


class ArtifactStore:
    """Per-session store for artifact upload state.

    Manages artifact file mappings, chunked-upload tracking,
    dedup hash cache, and UDF import file sets.

    Thread safety is provided by three ``ReadWriteLock`` instances,
    each guarding an independent group of state:

    - ``_filenames_lock`` — ``_filenames``, ``_python_files``,
      ``_import_files``, ``_jars``
    - ``_chunk_lock`` — ``_current_chunk``
    - ``_hash_lock`` — ``_hash_cache``

    Individual public methods acquire the appropriate lock.  The
    ``writer()`` context manager acquires ``_filenames_lock`` in write
    mode for callers that need a held-lock section spanning multiple
    mutations (e.g. the post-upload stage processing).
    """

    def __init__(self) -> None:
        self._filenames_lock = ReadWriteLock()
        self._chunk_lock = ReadWriteLock()
        self._hash_lock = ReadWriteLock()

        self._filenames: dict[str, str] = {}
        self._current_chunk: dict | None = None
        self._hash_cache: set[ArtifactKey] = set()
        self._python_files: set[str] = set()
        self._import_files: set[str] = set()
        self._jars: set[str] = set()

    # -- filenames (artifact name -> local filepath) -------------------------

    def set_filename(self, name: str, filepath: str) -> None:
        with self._filenames_lock.writer():
            self._filenames[name] = filepath

    def get_filename(self, name: str) -> str | None:
        with self._filenames_lock.reader():
            return self._filenames.get(name)

    def remove_filename(self, name: str) -> str | None:
        """Pop and return the filepath for *name*, or ``None``."""
        with self._filenames_lock.writer():
            return self._filenames.pop(name, None)

    def assert_no_duplicate_filename(self, name: str) -> None:
        with self._filenames_lock.reader():
            assert name not in self._filenames, "Duplicate artifact name found."

    def assert_filename_matches(self, name: str, expected: str) -> None:
        with self._filenames_lock.reader():
            assert self._filenames[name] == expected, "Artifact staging error."

    # -- current chunk (chunked upload tracking) -----------------------------

    def get_current_chunk(self) -> dict | None:
        with self._chunk_lock.reader():
            return self._current_chunk

    def set_current_chunk(self, chunk: dict | None) -> None:
        with self._chunk_lock.writer():
            self._current_chunk = chunk

    def has_current_chunk(self) -> bool:
        with self._chunk_lock.reader():
            return self._current_chunk is not None

    # -- hash cache ----------------------------------------------------------

    def is_cached(self, key: ArtifactKey) -> bool:
        with self._hash_lock.reader():
            return key in self._hash_cache

    def cache_hashes(self, keys: set[ArtifactKey]) -> None:
        with self._hash_lock.writer():
            self._hash_cache.update(keys)

    def clear_hash_cache(self) -> None:
        with self._hash_lock.writer():
            self._hash_cache.clear()

    # -- import file sets ----------------------------------------------------

    def get_python_files(self) -> set[str]:
        with self._filenames_lock.reader():
            return set(self._python_files)

    def add_python_file(self, path: str) -> None:
        with self._filenames_lock.writer():
            self._python_files.add(path)

    def remove_python_file(self, path: str) -> None:
        with self._filenames_lock.writer():
            self._python_files.discard(path)

    def has_python_file(self, path: str) -> bool:
        with self._filenames_lock.reader():
            return path in self._python_files

    def clear_python_files(self) -> None:
        with self._filenames_lock.writer():
            self._python_files.clear()

    def get_import_files(self) -> set[str]:
        with self._filenames_lock.reader():
            return set(self._import_files)

    def add_import_file(self, path: str) -> None:
        with self._filenames_lock.writer():
            self._import_files.add(path)

    def get_jars(self) -> set[str]:
        with self._filenames_lock.reader():
            return set(self._jars)

    def add_jar(self, path: str) -> None:
        with self._filenames_lock.writer():
            self._jars.add(path)

    def clear_jars(self) -> None:
        with self._filenames_lock.writer():
            self._jars.clear()

    # -- held-lock context manager -------------------------------------------

    @contextmanager
    def writer(self):
        """Acquire ``_filenames_lock`` in write mode and yield an
        ``_ArtifactStoreWriter`` for non-locking bulk mutations.

        Use this when multiple filename / import-set mutations must be
        atomic (e.g. the post-upload stage processing loop).
        """
        with self._filenames_lock.writer():
            yield _ArtifactStoreWriter(self)

    # -- lifecycle -----------------------------------------------------------

    def clear(self) -> None:
        with self._filenames_lock.writer():
            self._filenames.clear()
            self._python_files.clear()
            self._import_files.clear()
            self._jars.clear()
        with self._chunk_lock.writer():
            self._current_chunk = None
        with self._hash_lock.writer():
            self._hash_cache.clear()


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
        self.artifacts_store = ArtifactStore()

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
        self.artifacts_store.clear()


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
    """Return the ``SparkSessionCache`` for the current Spark
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
