#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Session-scoped cache for table type and schema lookups on the write path.

SNOW-3968447: ``writeTo().append()`` previously issued two independent metadata
round-trips per INSERT (``SHOW AS RESOURCE TABLES`` via ``get_table_type`` and
``show tables like`` via ``session.table().schema``). This module caches both
per Snowpark session and invalidates entries when DDL touches the table.
"""

from __future__ import annotations

import copy
import re
import threading
from typing import TYPE_CHECKING, Callable, TypeVar

from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.types import DataType
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict
from snowflake.snowpark_connect.utils.identifiers import FQN
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

if TYPE_CHECKING:
    from snowflake.snowpark import Session

_QUOTED_ID = r'"(?:""|[^"])+"'
_UNQUOTED_ID = r"[A-Za-z_][\w$]*"
_TABLE_IDENTIFIER = (
    rf"((?:{_QUOTED_ID}|{_UNQUOTED_ID})(?:\.(?:{_QUOTED_ID}|{_UNQUOTED_ID})){{0,2}})"
)
_TABLE_KIND = r"(?:TRANSIENT|TEMPORARY|TEMP|HYBRID|DYNAMIC|EXTERNAL|ICEBERG)\s+"
_DDL_TABLE_NAME_PATTERN = re.compile(
    rf"\b(?:ALTER|DROP|TRUNCATE)\s+(?:ICEBERG\s+)?TABLE\s+(?:IF\s+EXISTS\s+)?"
    rf"{_TABLE_IDENTIFIER}",
    re.IGNORECASE,
)
_UNDROP_TABLE_PATTERN = re.compile(
    rf"\bUNDROP\s+(?:ICEBERG\s+)?TABLE\s+(?:IF\s+EXISTS\s+)?{_TABLE_IDENTIFIER}",
    re.IGNORECASE,
)
_CREATE_TABLE_PATTERN = re.compile(
    rf"\bCREATE\s+(?:OR\s+REPLACE\s+)?(?:{_TABLE_KIND})*TABLE\s+"
    rf"(?:IF\s+NOT\s+EXISTS\s+)?{_TABLE_IDENTIFIER}",
    re.IGNORECASE,
)
_RENAME_TABLE_PATTERN = re.compile(
    rf"\bALTER\s+(?:ICEBERG\s+)?TABLE\s+(?:IF\s+EXISTS\s+)?{_TABLE_IDENTIFIER}\s+"
    rf"RENAME\s+TO\s+{_TABLE_IDENTIFIER}",
    re.IGNORECASE,
)
_SWAP_TABLE_PATTERN = re.compile(
    rf"\bALTER\s+(?:ICEBERG\s+)?TABLE\s+(?:IF\s+EXISTS\s+)?{_TABLE_IDENTIFIER}\s+"
    rf"SWAP\s+WITH\s+{_TABLE_IDENTIFIER}",
    re.IGNORECASE,
)

_session_cache_attach_lock = threading.Lock()

T = TypeVar("T")


def _strip_sql_for_ddl_matching(query: str) -> str:
    """Remove comments and string literals before DDL regex matching."""
    stripped = re.sub(r"/\*.*?\*/", " ", query, flags=re.DOTALL)
    stripped = re.sub(r"--[^\n]*", " ", stripped)
    stripped = re.sub(r"'(?:''|[^'])*'", " ", stripped)
    return stripped


def _cache_key(table_name: str) -> str:
    """Normalize a table identifier to a session-cache lookup key."""
    fqn = FQN.from_string(table_name)
    parts = [
        unquote_if_quoted(part).upper()
        for part in (fqn.database, fqn.schema, fqn.name)
        if part
    ]
    return ".".join(parts)


def _table_keys_match(cached_key: str, ddl_key: str) -> bool:
    """Return whether a cached key matches a DDL-extracted key (qualified or not)."""
    if cached_key == ddl_key:
        return True
    if cached_key.endswith("." + ddl_key):
        return True
    if ddl_key.endswith("." + cached_key):
        return True
    return False


def _extract_ddl_table_names(query: str) -> list[str]:
    """Extract table identifiers from DDL statements that alter cacheable metadata."""
    names: list[str] = []
    normalized = _strip_sql_for_ddl_matching(query)
    for pattern in (
        _DDL_TABLE_NAME_PATTERN,
        _UNDROP_TABLE_PATTERN,
        _CREATE_TABLE_PATTERN,
    ):
        for match in pattern.finditer(normalized):
            raw = match.group(1).strip()
            if raw:
                names.append(raw)
    for pattern in (_RENAME_TABLE_PATTERN, _SWAP_TABLE_PATTERN):
        for match in pattern.finditer(normalized):
            for group_idx in (1, 2):
                raw = match.group(group_idx).strip()
                if raw:
                    names.append(raw)
    return names


def _copy_schema_cache_value(
    value: DataType | SnowparkSQLException,
) -> DataType | SnowparkSQLException:
    """Return a defensive copy so callers cannot mutate cached schema errors."""
    if isinstance(value, SnowparkSQLException):
        return copy.copy(value)
    return value


class TableMetadataCache:
    """Per-session cache of table type and schema with DDL-driven invalidation."""

    def __init__(self) -> None:
        self._table_types = SynchronizedDict()
        self._table_schemas = SynchronizedDict()
        self._key_locks: dict[str, threading.Lock] = {}
        self._key_generations: dict[str, int] = {}
        self._key_locks_guard = threading.Lock()

    def _generation_for(self, key: str) -> int:
        with self._key_locks_guard:
            return self._key_generations.get(key, 0)

    def _bump_generation(self, key: str) -> None:
        with self._key_locks_guard:
            self._key_generations[key] = self._key_generations.get(key, 0) + 1

    def _lock_for(self, key: str) -> threading.Lock:
        """Return the per-key lock used to serialize cache misses."""
        with self._key_locks_guard:
            lock = self._key_locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._key_locks[key] = lock
            return lock

    def _get_or_compute(
        self,
        store: SynchronizedDict,
        key: str,
        lookup: Callable[[], T],
        *,
        copy_on_return: Callable[[T], T] | None = None,
    ) -> T:
        """Load from cache or compute once per key, ignoring stale in-flight results."""
        cached = store.get(key)
        if cached is not None:
            return copy_on_return(cached) if copy_on_return else cached

        with self._lock_for(key):
            cached = store.get(key)
            if cached is not None:
                return copy_on_return(cached) if copy_on_return else cached
            generation = self._generation_for(key)
            result = lookup()
            if self._generation_for(key) == generation:
                store.set(key, result)
            return copy_on_return(result) if copy_on_return else result

    def get_table_type(
        self,
        table_name: str,
        lookup: Callable[[], str],
    ) -> str:
        """Return cached table type or invoke ``lookup`` on a cache miss."""
        key = _cache_key(table_name)
        return self._get_or_compute(self._table_types, key, lookup)

    def get_table_schema(
        self,
        table_name: str,
        lookup: Callable[[], DataType | SnowparkSQLException],
    ) -> DataType | SnowparkSQLException:
        """Return cached table schema or invoke ``lookup`` on a cache miss."""
        key = _cache_key(table_name)
        return self._get_or_compute(
            self._table_schemas,
            key,
            lookup,
            copy_on_return=_copy_schema_cache_value,
        )

    def _matching_cache_keys(self, ddl_key: str) -> list[str]:
        """List cache keys that match a DDL table identifier."""
        keys: set[str] = set()
        for cached_key in self._table_types.keys():
            if _table_keys_match(cached_key, ddl_key):
                keys.add(cached_key)
        for cached_key in self._table_schemas.keys():
            if _table_keys_match(cached_key, ddl_key):
                keys.add(cached_key)
        return list(keys)

    def _drop_key_locks(self, keys: list[str]) -> None:
        """Remove per-key locks after invalidation so they do not leak."""
        if not keys:
            return
        with self._key_locks_guard:
            for key in keys:
                self._key_locks.pop(key, None)

    def invalidate(self, table_name: str | None = None) -> None:
        """Drop cached metadata for ``table_name``, or clear the entire cache."""
        if table_name is None:
            self._table_types.clear()
            self._table_schemas.clear()
            with self._key_locks_guard:
                self._key_locks.clear()
                self._key_generations.clear()
            return
        ddl_key = _cache_key(table_name)
        self._bump_generation(ddl_key)
        keys = self._matching_cache_keys(ddl_key)
        if ddl_key not in keys:
            keys.append(ddl_key)
        for key in keys:
            if key != ddl_key:
                self._bump_generation(key)
            self._table_types.remove(key)
            self._table_schemas.remove(key)
        self._drop_key_locks(keys)

    def invalidate_for_query(self, query: str) -> None:
        """Invalidate cache entries referenced by DDL in ``query``."""
        names = _extract_ddl_table_names(query)
        if not names:
            return
        for name in names:
            self.invalidate(name)
            logger.debug("Invalidated table metadata cache for %s", name)


def get_table_metadata_cache(session: Session) -> TableMetadataCache | None:
    """Return the session's metadata cache if instrumented, else ``None``."""
    cache = getattr(session, "_table_metadata_cache", None)
    if isinstance(cache, TableMetadataCache):
        return cache
    return None


def get_or_create_table_metadata_cache(session: Session) -> TableMetadataCache:
    """Attach and return the session-scoped metadata cache (idempotent)."""
    cache = get_table_metadata_cache(session)
    if cache is not None:
        return cache
    with _session_cache_attach_lock:
        cache = get_table_metadata_cache(session)
        if cache is not None:
            return cache
        cache = TableMetadataCache()
        session._table_metadata_cache = cache
        return cache


def clear_table_metadata_cache(session: Session) -> None:
    """Clear all cached table metadata for ``session``."""
    cache = get_table_metadata_cache(session)
    if cache is not None:
        cache.invalidate()


def invalidate_table_metadata_cache_for_query(session: Session, query: str) -> None:
    """Invalidate cache entries for DDL in ``query``; never raises to the caller."""
    cache = get_table_metadata_cache(session)
    if cache is None:
        return
    try:
        cache.invalidate_for_query(query)
    except Exception:
        logger.warning(
            "Failed to invalidate table metadata cache for query",
            exc_info=True,
        )


def instrument_session_for_table_metadata_cache(session: Session) -> None:
    """Ensure ``session`` has a metadata cache attached (no-op if already done)."""
    if getattr(session, "_table_metadata_cache_instrumented", False):
        return
    get_or_create_table_metadata_cache(session)
    session._table_metadata_cache_instrumented = True
