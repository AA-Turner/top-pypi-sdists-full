#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""
CLD (Catalog-Linked Database) context management for identifier handling.

This module provides utilities for detecting and managing CLD context,
which affects how identifiers are quoted and cased when sent to Snowflake.

Decision Logic (from design doc):
    Effective rule set is CLD when either (a) the session is on a CLD, or
    (b) ``snowpark.connect.identifier.useCldRules`` is true (POC opt-in flag,
    default false).

    if CLD rules apply:
        Default: no double quotes
        If spark.sql.caseSensitive=True, invalid unquoted Snowflake id, or
        backtick-quoted non-\\w+ name: add double quotes, preserve casing
        Else: passthrough bare identifier
    Else (legacy non-CLD):
        Default: double quotes
        If spark.sql.caseSensitive=True:
            Keep as is
        Else:
            UPPERCASE
"""
import json
import re
from contextvars import ContextVar
from dataclasses import dataclass, replace
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
    # External catalog provider label for telemetry. "managed" for a non-CLD
    # (Snowflake-managed) session; for a CLD, one of the values produced by
    # `_classify_catalog_provider` (glue / unity / horizon / other), or
    # "unknown" when the integration lookup fails.
    catalog_provider: str | None = None


# Telemetry catalog-provider labels. Non-CLD sessions report MANAGED; CLD
# sessions resolve their catalog integration's CATALOG_SOURCE (+ REST config)
# to one of the external providers. UNKNOWN is the safe fallback when the
# integration can't be resolved.
CATALOG_PROVIDER_MANAGED = "managed"
CATALOG_PROVIDER_GLUE = "glue"
CATALOG_PROVIDER_UNITY = "unity"
CATALOG_PROVIDER_HORIZON = (
    "horizon"  # emitted for CATALOG_SOURCE = POLARIS (Open Catalog / Horizon)
)
# Any resolved external catalog that isn't glue / unity / horizon (object store,
# S3 Tables, a generic Iceberg REST endpoint, ...). Only the three above are
# broken out; everything else is deliberately collapsed here.
CATALOG_PROVIDER_OTHER = "other"
CATALOG_PROVIDER_UNKNOWN = "unknown"

# Canonical telemetry catalog_kind vocabulary. Docstrings that enumerate the
# values should point here so they can't drift from the classifier.
CATALOG_PROVIDERS = frozenset(
    {
        CATALOG_PROVIDER_MANAGED,
        CATALOG_PROVIDER_GLUE,
        CATALOG_PROVIDER_UNITY,
        CATALOG_PROVIDER_HORIZON,
        CATALOG_PROVIDER_OTHER,
        CATALOG_PROVIDER_UNKNOWN,
    }
)


def _classify_catalog_provider(
    catalog_source: str | None,
    catalog_api_type: str | None = None,
    catalog_uri: str | None = None,
) -> str:
    """Map a catalog integration's DESCRIBE output to a telemetry provider label.

    Only glue / unity / horizon are broken out; every other resolved catalog
    source (object store, S3 Tables, a generic Iceberg REST endpoint, or an
    unmapped source) collapses to ``"other"``. ``catalog_source`` is the
    CATALOG_SOURCE property (GLUE / POLARIS / OBJECT_STORE / AWS_S3_TABLES /
    ICEBERG_REST); glue and unity can both arrive as ICEBERG_REST, so they're
    split by the REST config (``catalog_api_type`` first, then the
    ``catalog_uri`` host). ``"unknown"`` is reserved for "couldn't resolve the
    source at all" (empty source / lookup failed).
    """
    src = (catalog_source or "").strip().upper()
    api = (catalog_api_type or "").strip().upper()
    uri = (catalog_uri or "").strip().lower()

    if not src:
        return CATALOG_PROVIDER_UNKNOWN
    if src == "GLUE":
        return CATALOG_PROVIDER_GLUE
    if src == "POLARIS":
        return CATALOG_PROVIDER_HORIZON
    if src == "UNITY":
        return CATALOG_PROVIDER_UNITY
    if src == "ICEBERG_REST":
        if api in ("AWS_GLUE", "AWS_PRIVATE_GLUE") or "glue." in uri:
            return CATALOG_PROVIDER_GLUE
        if (
            api in ("UNITY", "DATABRICKS")
            or "databricks" in uri
            or "/unity-catalog" in uri
        ):
            return CATALOG_PROVIDER_UNITY
        return CATALOG_PROVIDER_OTHER
    # OBJECT_STORE, AWS_S3_TABLES, and any other resolved-but-uninteresting source.
    return CATALOG_PROVIDER_OTHER


def _extract_config_value(raw: str, key: str) -> str | None:
    """Pull ``key`` from a config blob that may be JSON or SQL-ish key=value text.

    DESCRIBE CATALOG INTEGRATION's ``REST_CONFIG`` property_value has been seen as
    both a JSON object and a parenthesized ``KEY = 'value'`` string, so try JSON
    first and fall back to a case-insensitive ``key=value`` scan. None on any miss.
    """
    if not raw:
        return None
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            for k, v in obj.items():
                if str(k).upper() == key.upper() and v is not None:
                    return str(v)
    except (ValueError, TypeError):
        pass
    match = re.search(
        rf"{re.escape(key)}\s*=\s*'?([A-Za-z0-9_.:/\-]+)'?", raw, re.IGNORECASE
    )
    return match.group(1) if match else None


def _get_cld_catalog_integration(
    session: "snowpark.Session", database_cache_key: str
) -> str | None:
    """Return the catalog-integration name a CLD is linked to, or None.

    ``SYSTEM$GET_CATALOG_LINKED_DATABASE_CONFIG`` returns JSON with the documented
    keys ``catalog_integration`` (the integration name) and ``catalog_name`` (the
    external catalog *namespace* -- never the integration identifier, so it is not
    used here). We read ``catalog_integration`` (accepting a camelCase spelling
    defensively) and ignore everything else.
    """
    escaped = database_cache_key.replace("'", "''")
    try:
        rows = collect_without_telemetry(
            session.sql(
                f"SELECT SYSTEM$GET_CATALOG_LINKED_DATABASE_CONFIG('{escaped}')"
            )
        )
    except Exception as e:
        logger.debug(
            "GET_CATALOG_LINKED_DATABASE_CONFIG %r failed: %s", database_cache_key, e
        )
        return None
    if not rows or rows[0] is None or rows[0][0] is None:
        return None
    try:
        cfg = json.loads(str(rows[0][0]))
    except (ValueError, TypeError):
        return None
    if not isinstance(cfg, dict):
        return None
    for candidate in ("catalog_integration", "catalogIntegration"):
        val = cfg.get(candidate)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def _resolve_catalog_provider(
    session: "snowpark.Session", database_cache_key: str
) -> str:
    """Resolve a CLD's external catalog provider label (best-effort, never raises).

    CLD -> linked catalog integration -> ``DESCRIBE CATALOG INTEGRATION`` ->
    CATALOG_SOURCE (+ REST config) -> provider label. Any failure degrades to
    ``"unknown"`` so telemetry resolution never breaks a request.
    """
    integration_name = _get_cld_catalog_integration(session, database_cache_key)
    if not integration_name:
        return CATALOG_PROVIDER_UNKNOWN
    safe = integration_name.replace('"', '""')
    try:
        rows = collect_without_telemetry(
            session.sql(f'DESCRIBE CATALOG INTEGRATION "{safe}"')
        )
    except Exception as e:
        logger.debug("DESCRIBE CATALOG INTEGRATION %r failed: %s", integration_name, e)
        return CATALOG_PROVIDER_UNKNOWN

    # DESCRIBE CATALOG INTEGRATION columns: property, property_type,
    # property_value, property_default. Value is at index 2.
    catalog_source = catalog_api_type = catalog_uri = None
    for r in rows:
        try:
            prop = str(r[0]).upper()
            val = str(r[2])
        except (IndexError, TypeError):
            continue
        if prop == "CATALOG_SOURCE":
            catalog_source = val
        elif prop == "CATALOG_API_TYPE":
            catalog_api_type = val
        elif prop == "CATALOG_URI":
            catalog_uri = val
        elif prop == "REST_CONFIG":
            catalog_api_type = catalog_api_type or _extract_config_value(
                val, "CATALOG_API_TYPE"
            )
            catalog_uri = catalog_uri or _extract_config_value(val, "CATALOG_URI")
    return _classify_catalog_provider(catalog_source, catalog_api_type, catalog_uri)


# Session-level CLD context cache
# Key: database name (uppercase for lookup), Value: CLDInfo
_cld_cache: dict[str, CLDInfo] = {}
_cld_cache_lock = Lock()

# Warning tracking to avoid repeated warnings
_case_sensitivity_warnings_logged: set[str] = set()

# CLDs whose catalog provider couldn't be resolved yet (logged once each).
_provider_resolution_warned: set[str] = set()

# Bounded provider-resolution retries for a cached CLD still labeled unknown, so a
# missing USAGE grant doesn't cost DESCRIBE CATALOG INTEGRATION on every RPC forever.
_PROVIDER_MAX_RETRIES = 3
_provider_retry_counts: dict[str, int] = {}


def _maybe_retry_provider(session: "snowpark.Session", cache_key: str) -> str | None:
    """Retry provider resolution for a cached-unknown CLD, up to a bounded count.

    Returns the resolved provider label, or None to signal "keep the cached
    unknown" (either the retry didn't resolve it, or the budget is exhausted and
    we pin unknown to stop querying).
    """
    with _cld_cache_lock:
        if _provider_retry_counts.get(cache_key, 0) >= _PROVIDER_MAX_RETRIES:
            return None
        _provider_retry_counts[cache_key] = _provider_retry_counts.get(cache_key, 0) + 1
    provider = _resolve_catalog_provider(session, cache_key)
    if provider and provider != CATALOG_PROVIDER_UNKNOWN:
        with _cld_cache_lock:
            _provider_retry_counts.pop(cache_key, None)
        return provider
    return None


def _warn_provider_unresolved_once(database_name: str) -> None:
    """Warn once per database when a CLD's catalog provider can't be resolved."""
    with _cld_cache_lock:
        if database_name in _provider_resolution_warned:
            return
        _provider_resolution_warned.add(database_name)
    logger.warning(
        "Could not resolve catalog provider for CLD %r; telemetry catalog_kind will "
        "report 'unknown' until the lookup succeeds (check USAGE on the catalog "
        "integration).",
        database_name,
    )


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


def catalog_kind() -> str:
    """Return the telemetry catalog-provider label for the current session.

    ``"managed"`` for a non-CLD (Snowflake-managed) session; for a CLD, the
    resolved external provider (glue / unity / horizon / other) or ``"unknown"`` when the integration couldn't be classified.

    Replaces the old inline ``"cld" if is_in_cld_context() else "managed"``
    idiom at the Iceberg telemetry call sites so the emitted ``catalog_kind``
    carries the actual provider.
    """
    ctx = _current_cld_context.get()
    if ctx.catalog_provider:
        return ctx.catalog_provider
    return CATALOG_PROVIDER_UNKNOWN if ctx.is_cld else CATALOG_PROVIDER_MANAGED


def should_use_cld_identifier_rules(is_cld: bool | None = None) -> bool:
    """Return whether CLD identifier rules should apply for this identifier.

    Used by :func:`transform_identifier_for_snowflake` and other identifier
    rendering that must follow real CLD session semantics on main.

    When ``snowpark.connect.identifier.useCldRules`` is enabled, CLD rules apply
    to all databases (POC for unifying identifier rendering without CLD
    detection). Otherwise, CLD rules apply when the session is on a CLD or when
    the caller passes ``is_cld=True``.

    **Unified-rules behavior** (SQL preprocess, temp-view column renames, etc.) must
    gate on :func:`is_cld_unified_identifier_rules_enabled` instead. That helper
    checks only the global flag so ``useCldRules=false`` (the default) has no
    effect even inside a CLD session — see Felix's review on this function.
    """
    from snowflake.snowpark_connect.config import global_config

    if global_config.snowpark_connect_identifier_useCldRules:
        return True

    if is_cld is None:
        return is_in_cld_context()
    return is_cld


def is_cld_unified_identifier_rules_enabled() -> bool:
    """Return whether the SNOW-3758410 unified-rules flag is explicitly enabled.

    Gate new SCOS behavior introduced for unified CLD identifier rules on this
    helper only. Unlike :func:`should_use_cld_identifier_rules`, this does not
    consult CLD session context, preserving the guarantee that the default-off
    flag is a no-op for unified-rules changes.

    Identifier rendering and existing CLD write paths (e.g. ``_spark_to_snowflake``
    on a CLD session) continue to use :func:`should_use_cld_identifier_rules`.
    """
    from snowflake.snowpark_connect.config import global_config

    return global_config.snowpark_connect_identifier_useCldRules


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
        # CLD-ness and case-sensitivity are cached write-once. Only the provider
        # is retried (bounded): if a cached CLD is still unresolved, re-attempt
        # resolution without re-running SHOW DATABASES / DESCRIBE DATABASE.
        if cached.is_cld and cached.catalog_provider in (
            None,
            CATALOG_PROVIDER_UNKNOWN,
        ):
            provider = _maybe_retry_provider(session, cache_key)
            if provider:
                updated = replace(cached, catalog_provider=provider)
                with _cld_cache_lock:
                    _cld_cache[cache_key] = updated
                return updated
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
            catalog_provider = CATALOG_PROVIDER_MANAGED
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
                # Resolve the external catalog provider (glue / unity / horizon /
                # ...). Best-effort and self-contained; degrades to "unknown".
                catalog_provider = _resolve_catalog_provider(session, cache_key)

            info = CLDInfo(
                is_cld=is_cld,
                catalog_case_sensitivity=catalog_case_sensitivity,
                database_name=cache_key,
                catalog_provider=catalog_provider,
            )

            # Always cache CLD-ness + case-sensitivity (both stable and worth not
            # re-querying). If the provider came back "unknown" (missing USAGE on
            # the catalog integration, or a transient DESCRIBE failure) it stays
            # retryable: subsequent cache hits re-attempt only the provider lookup
            # (bounded), so we never re-run SHOW DATABASES / DESCRIBE DATABASE just
            # to retry the provider.
            if is_cld and catalog_provider == CATALOG_PROVIDER_UNKNOWN:
                _warn_provider_unresolved_once(cache_key)

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
    # Caller is responsible for passing `is_backtick_quoted` per identifier
    # reference. We no longer fall back to a request-global name-keyed set:
    # that fallback caused cross-contamination between identifiers that
    # happen to share a leaf name (Felix's PR #4052 review).
    if is_backtick_quoted is None:
        is_backtick_quoted = False

    # Lazy import to avoid circular dependency
    from snowflake.snowpark_connect.config import global_config

    spark_case_sensitive = global_config.spark_sql_caseSensitive
    use_cld_rules = should_use_cld_identifier_rules(is_cld)

    if use_cld_rules:
        from snowflake.snowpark_connect.utils.identifiers import (
            cld_identifier_needs_snowflake_quotes,
        )

        should_quote = cld_identifier_needs_snowflake_quotes(
            name,
            is_backtick_quoted=is_backtick_quoted,
            spark_case_sensitive=spark_case_sensitive,
        )

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
    global _cld_cache, _case_sensitivity_warnings_logged, _provider_resolution_warned
    with _cld_cache_lock:
        _cld_cache.clear()
        _provider_retry_counts.clear()
    _case_sensitivity_warnings_logged.clear()
    _provider_resolution_warned.clear()
