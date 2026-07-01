#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""
CLD (Catalog-Linked Database) context management for identifier handling.

This module provides utilities for detecting and managing CLD context,
which affects how identifiers are quoted and cased when sent to Snowflake.

Decision Logic (from design doc):
    if CLD:
        Default: no double quotes
        If backtick identifier OR spark.sql.caseSensitive=True:
            Add double quotes
        If spark.sql.caseSensitive=True:
            Keep as is (no uppercase)
        Else:
            UPPERCASE
    Else (Non-CLD):
        Default: double quotes
        If spark.sql.caseSensitive=True:
            Keep as is
        Else:
            UPPERCASE
"""
from contextvars import ContextVar
from dataclasses import dataclass
from threading import Lock
from typing import TYPE_CHECKING

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark_connect.utils.internal_query import collect_without_telemetry
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

if TYPE_CHECKING:
    from snowflake import snowpark


@dataclass
class CLDInfo:
    """Information about a Catalog-Linked Database."""

    is_cld: bool = False
    catalog_case_sensitivity: str | None = (
        None  # "CASE_SENSITIVE" or "CASE_INSENSITIVE"
    )
    database_name: str | None = None


# Session-level CLD context cache
# Key: database name (uppercase for lookup), Value: CLDInfo
_cld_cache: dict[str, CLDInfo] = {}
_cld_cache_lock = Lock()

# Warning tracking to avoid repeated warnings
_case_sensitivity_warnings_logged: set[str] = set()

# Session-level CLD hint, carried via a ContextVar so identifier
# transformation helpers (`spark_to_sf_single_id`, `_spark_field_to_sql`, ...)
# can read CLD-ness without every call site threading it as an argument.
#
# SCOS pins one Spark session to one Snowflake database and does not
# silently switch mid-session, so a single boolean "is this session on a
# CLD?" is enough to drive all identifier rendering — for 1-part,
# 2-part, and 3-part names alike, including Iceberg's
# `schema.table.metadata_table` form. There is no per-identifier CLD
# classification: the session's classification is the ground truth.
#
# Lifecycle:
#   1. Reset to `is_cld=False` at every RPC entry via `clear_context_data`
#      -> `reset_request_cld_state` (server.py). Prevents leakage between
#      RPCs handled by the same gRPC worker thread on the sync server.
#   2. Set by `utils/session.py:get_or_create_snowpark_session` immediately
#      after the Snowpark session attaches to its database, based on
#      `get_cld_info(session, current_db)`. This is the authoritative
#      and *only* place CLD-ness is computed.
#
# Callers should invoke `get_or_create_snowpark_session()` before any
# identifier rendering in an RPC so step (2) re-establishes the hint
# after step (1)'s reset.
_current_cld_context: ContextVar[CLDInfo] = ContextVar(
    "current_cld_context", default=CLDInfo(is_cld=False)
)

# Request-level mapping from multipart identifier parts -> per-part backtick
# flags. Keyed by the unquoted parts tuple (e.g. ("mydb", "mytbl")), so the
# same name appearing as different identifiers — e.g. a column `foo` and a
# table `foo` — never cross-contaminate each other. Producers (SQL AST walk
# in map_sql.py, DataFrame `.table()` path in map_read_table.py) populate
# the dict during request setup; consumers (`_spark_to_snowflake`,
# `get_table_from_name`) read it positionally per part. There is no
# name-only fallback: identifiers that aren't recorded here default to
# "not backtick-quoted" — matching Spark's parser semantics.
_multipart_backtick_flags: ContextVar[
    dict[tuple[str, ...], tuple[bool, ...]] | None
] = ContextVar("multipart_backtick_flags", default=None)


def get_current_cld_context() -> CLDInfo:
    """Get the current CLD context for the request."""
    return _current_cld_context.get()


def set_current_cld_context(info: CLDInfo) -> None:
    """Set the CLD context for the current request."""
    _current_cld_context.set(info)


def is_in_cld_context() -> bool:
    """Check if the current request is in a CLD context."""
    return _current_cld_context.get().is_cld


def record_multipart_backtick_flags(
    parts: tuple[str, ...], flags: tuple[bool, ...]
) -> None:
    """Record per-part backtick flags for one multipart identifier reference.

    `parts` is the unquoted parts tuple as seen by the rest of the system
    (e.g. what `split_fully_qualified_spark_name` returns), and `flags[i]`
    is True iff `parts[i]` was originally backtick-quoted in the user's
    input. Calling this for the same `parts` tuple a second time overwrites
    the prior entry — that's fine, since identical references must share
    the same backtick shape.

    Keying by the full parts tuple (instead of by bottom-level name) is
    what eliminates cross-contamination between a backtick-quoted column
    and an unquoted table that happen to share a leaf name. See PR #4052
    review (Felix's comment on cld_context.py:113).
    """
    state = _multipart_backtick_flags.get()
    if state is None:
        state = {}
        _multipart_backtick_flags.set(state)
    state[parts] = flags


def get_multipart_backtick_flags(
    parts: tuple[str, ...],
) -> tuple[bool, ...] | None:
    """Return the recorded per-part backtick flags for `parts`, or None."""
    state = _multipart_backtick_flags.get()
    if state is None:
        return None
    return state.get(parts)


def clear_multipart_backtick_flags() -> None:
    """Clear the recorded backtick flags. Called at RPC entry to reset state."""
    _multipart_backtick_flags.set(None)


def reset_request_cld_state() -> None:
    """Reset all per-request CLD state at the start of an RPC.

    The sync gRPC server reuses worker threads across RPCs, so a `ContextVar`
    that was set during request A would otherwise still be visible at the
    start of request B handled by the same thread. We call this at every
    Spark Connect entrypoint so each RPC sees a clean slate:

      * `_current_cld_context` is reset to "not in CLD"; the appropriate
        handler will set it again if needed via `set_current_cld_context`.
      * `_multipart_backtick_flags` is cleared.

    See PR #4052 review (Andong's comment on cld_context.py:34).
    """
    _current_cld_context.set(CLDInfo(is_cld=False))
    clear_multipart_backtick_flags()


def is_double_quoted(name: str) -> bool:
    """Check if an identifier is already wrapped in double quotes (ANSI SQL mode)."""
    return name.startswith('"') and name.endswith('"') and len(name) >= 2


def _normalize_database_name(database_name: str) -> str:
    """Normalize a Spark-side database identifier to its Snowflake-stored form.

    Two cases:
    - Double-quoted input (`"MyCLD"`): Snowflake stored it case-preserved at
      creation, so the cache key and lookup must keep that exact case. We just
      strip the surrounding quotes.
    - Unquoted input (`MyCLD` / `mycld` / `MYCLD`): Snowflake stores unquoted
      identifiers uppercased, so the cache key is the upper-case form. All
      case variants of the input collapse to the same key.

    This avoids both (a) cache-key collisions between case-preserving DBs like
    `"MyCLD"` and `"OTHER_MYCLD"` after upper-casing, and (b) `SHOW DATABASES
    LIKE 'MYCLD'` failing to match a stored `MyCLD` (Snowflake LIKE is
    case-sensitive on object names).
    """
    if (
        len(database_name) >= 2
        and database_name.startswith('"')
        and database_name.endswith('"')
    ):
        return database_name[1:-1]
    return database_name.upper()


def get_cld_info(session: "snowpark.Session", database_name: str | None) -> CLDInfo:
    """
    Get CLD information for a database.

    Args:
        session: Snowpark session
        database_name: Name of the database to check

    Returns:
        CLDInfo with is_cld flag and catalog_case_sensitivity
    """
    if not database_name:
        return CLDInfo(is_cld=False)

    # Normalize database name for cache lookup. Preserves case for
    # double-quoted input (Snowflake stored that name case-preserved) and
    # uppercases bare names (Snowflake's default).
    cache_key = _normalize_database_name(database_name)

    # Fast path: lock-free read. CPython `dict.get` is atomic under the GIL,
    # and CLDInfo entries are immutable + write-once after their first miss
    # (see double-checked locking in the slow path below), so a concurrent
    # writer can never expose a torn / partially-populated value here. Avoid
    # holding `_cld_cache_lock` to prevent this hot path from serializing
    # every session fetch across all gRPC worker threads.
    cached = _cld_cache.get(cache_key)
    if cached is not None:
        return cached

    # Slow path: query Snowflake outside the lock so a slow `SHOW DATABASES`
    # doesn't serialize callers looking up different databases. The cache
    # write below uses double-checked locking to close the TOCTOU window
    # where two threads can both miss + both query + both write.
    # Escape single quotes for LIKE clause (defensive against SQL injection).
    escaped_cache_key = cache_key.replace("'", "''")
    try:
        result = collect_without_telemetry(
            session.sql(f"SHOW DATABASES LIKE '{escaped_cache_key}'")
        )
        if result and len(result) > 0:
            row = result[0]
            # Column indices from SHOW DATABASES output:
            # Index 9: 'kind' - contains 'CATALOG-LINKED DATABASE' for CLDs
            kind = str(row[9]) if len(row) > 9 else ""
            is_cld = "CATALOG-LINKED" in kind.upper()

            # Try to get CATALOG_CASE_SENSITIVITY if available
            catalog_case_sensitivity = None
            if is_cld:
                try:
                    # Use quoted identifier for DESCRIBE (defensive against SQL injection)
                    desc_result = collect_without_telemetry(
                        session.sql(f'DESCRIBE DATABASE "{cache_key}"')
                    )
                    for desc_row in desc_result:
                        if len(desc_row) >= 2:
                            prop_name = str(desc_row[0]).upper()
                            if "CATALOG_CASE_SENSITIVITY" in prop_name:
                                catalog_case_sensitivity = str(desc_row[1])
                                break
                except Exception as e:
                    logger.debug(
                        "DESCRIBE DATABASE %r failed (skipping case-sensitivity "
                        "probe): %s",
                        cache_key,
                        e,
                    )

            info = CLDInfo(
                is_cld=is_cld,
                catalog_case_sensitivity=catalog_case_sensitivity,
                database_name=cache_key,
            )

            with _cld_cache_lock:
                # Double-check: another thread may have written between our
                # initial miss and acquiring the write lock. Prefer that
                # write to keep a single canonical CLDInfo per cache key.
                if cache_key in _cld_cache:
                    return _cld_cache[cache_key]
                _cld_cache[cache_key] = info

            # Log warning if case sensitivity mismatch
            _check_case_sensitivity_mismatch(info)

            return info
    except Exception as e:
        logger.debug(f"Could not get CLD info for database '{database_name}': {e}")

    return CLDInfo(is_cld=False)


def _check_case_sensitivity_mismatch(info: CLDInfo) -> None:
    """Log warning if spark.sql.caseSensitive doesn't match CLD's CATALOG_CASE_SENSITIVITY.

    The check-then-add on `_case_sensitivity_warnings_logged` runs under
    `_cld_cache_lock` so concurrent callers can't race past the dedupe
    check and emit duplicate warnings. The set is only updated when we
    actually log, preserving the "warnings already logged" semantics.
    """
    if not info.is_cld or not info.catalog_case_sensitivity:
        return

    # Lazy import to avoid circular dependency
    from snowflake.snowpark_connect.config import global_config

    spark_case_sensitive = global_config.spark_sql_caseSensitive
    cld_case_sensitive = info.catalog_case_sensitivity.upper() == "CASE_SENSITIVE"

    if spark_case_sensitive == cld_case_sensitive:
        return

    warning_key = f"{info.database_name}:{info.catalog_case_sensitivity}"
    with _cld_cache_lock:
        if warning_key in _case_sensitivity_warnings_logged:
            return
        _case_sensitivity_warnings_logged.add(warning_key)

    logger.warning(
        f"Case sensitivity mismatch for CLD '{info.database_name}': "
        f"spark.sql.caseSensitive={spark_case_sensitive} but "
        f"CATALOG_CASE_SENSITIVITY={info.catalog_case_sensitivity}. "
        f"Consider setting spark.sql.caseSensitive={'true' if cld_case_sensitive else 'false'} "
        f"to match the CLD configuration."
    )


def transform_identifier_for_snowflake(
    name: str,
    is_backtick_quoted: bool | None = None,
    is_cld: bool | None = None,
    is_column: bool = False,
) -> str:
    """
    Transform a Spark identifier to a Snowflake identifier following CLD rules.

    This is the central utility for identifier transformation that implements
    the decision logic for CLD vs non-CLD contexts.

    Args:
        name: The identifier name (without quotes)
        is_backtick_quoted: True if the identifier was originally backtick-quoted in Spark.
                           If None, checks the request context.
        is_cld: True if this identifier is for a CLD context.
                If None, uses the current request context.
        is_column: True if the identifier is a column name. The current rule
                   set treats columns and non-columns identically; the flag
                   is kept on the API for future column-specific behavior
                   and to keep call sites self-documenting.

    Returns:
        The transformed identifier ready for Snowflake SQL
    """
    # Use context if not explicitly provided
    if is_cld is None:
        is_cld = is_in_cld_context()

    # Caller is responsible for passing `is_backtick_quoted` per identifier
    # reference. We no longer fall back to a request-global name-keyed set:
    # that fallback caused cross-contamination between identifiers that
    # happen to share a leaf name (Felix's PR #4052 review).
    if is_backtick_quoted is None:
        is_backtick_quoted = False

    # Lazy import to avoid circular dependency
    from snowflake.snowpark_connect.config import global_config

    spark_case_sensitive = global_config.spark_sql_caseSensitive

    if is_cld:
        # CLD rules:
        # - Default: no double quotes
        # - Add double quotes if backtick-quoted OR caseSensitive=True
        # - No casing change and keep as is
        should_quote = is_backtick_quoted or spark_case_sensitive

        if should_quote:
            # Quote the identifier and keep as is
            result = quote_name_without_upper_casing(name)
            return result
        else:
            # No quoting for CLD, keep as is
            return name
    else:
        # Non-CLD rules:
        # - Default: double quotes
        # - Uppercase unless caseSensitive=True
        result = quote_name_without_upper_casing(name)
        if not spark_case_sensitive:
            result = result.upper()
        return result


def clear_cld_cache() -> None:
    """Clear the CLD cache. Useful for testing or session reset."""
    global _cld_cache, _case_sensitivity_warnings_logged
    with _cld_cache_lock:
        _cld_cache.clear()
    _case_sensitivity_warnings_logged.clear()
