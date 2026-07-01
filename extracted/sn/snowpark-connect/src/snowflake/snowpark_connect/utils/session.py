#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import logging
import os
from collections.abc import Sequence
from typing import Any

from snowflake import snowpark
from snowflake.connector.description import PLATFORM
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark.exceptions import SnowparkClientException, SnowparkSQLException
from snowflake.snowpark.session import _get_active_session
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.cld_context import (
    _normalize_database_name,
    get_cld_info,
    get_current_cld_context,
    is_in_cld_context,
    set_current_cld_context,
)
from snowflake.snowpark_connect.utils.describe_query_cache import (
    instrument_session_for_describe_cache,
)
from snowflake.snowpark_connect.utils.internal_query import collect_without_telemetry
from snowflake.snowpark_connect.utils.scos_query_tag import (
    instrument_session_for_scos_query_tag,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import (
    init_spark_session_cache_registry,
)
from snowflake.snowpark_connect.utils.telemetry import telemetry
from snowflake.snowpark_connect.utils.udf_cache import init_builtin_udf_cache

SKIP_SESSION_CONFIGURATION = False


def skip_session_configuration(skip: bool):
    global SKIP_SESSION_CONFIGURATION
    SKIP_SESSION_CONFIGURATION = skip


# Suppress experimental warnings from snowflake.snowpark logger
def _filter_experimental_warnings(record):
    """Filter function to suppress experimental warnings."""
    message = record.getMessage()
    return not (
        "is experimental since" in message and "Do not use it in production" in message
    )


logging.getLogger("snowflake.snowpark").addFilter(_filter_experimental_warnings)


# Sentinel returned by ``_get_connector_current_database`` when the
# connector chain is reachable but ``connection.database`` is currently
# ``None`` (transient state during a reconnect, session reset, …). This is
# distinct from ``None`` (the chain itself is unreachable, e.g. a mocked
# session or a future connector refactor that removed the private chain).
# Keeping the two cases distinguishable lets the cache layer decide whether
# a Snowpark round-trip is justified.
_CONNECTOR_DB_PRESENT_BUT_UNSET = ""


def _get_connector_current_database(
    session: snowpark.Session,
) -> str | None:
    """Best-effort, no-round-trip read of the Snowflake connector's view of
    the current database, normalized to match ``Session.get_current_database()``.

    The Snowflake connector updates ``connection.database`` synchronously
    after any ``USE DATABASE`` statement, so this attribute is the cheapest
    source of truth for "has the session moved to a different database
    since we last cached it?".

    Two normalizations vs the raw attribute matter:

    * The raw value is unquoted (e.g. ``cldUnity`` for a case-preserved
      database). Snowpark's own ``Session.get_current_database()`` wraps
      that value with ``quote_name_without_upper_casing`` before returning
      it. We do the same here so callers (and the CLD cache key
      derivation in ``_normalize_database_name``) see a single
      representation regardless of which source the value came from.
    * The connector chain is private to Snowpark / the Python connector
      and can move under us during a version bump. We catch a *broad*
      exception class (not just ``AttributeError``) so any failure walking
      this chain falls back to ``Session.get_current_database()`` instead
      of taking down the RPC.

    Returns:
        * The quoted current database name when the chain reads cleanly.
        * ``_CONNECTOR_DB_PRESENT_BUT_UNSET`` (the empty string) when the
          chain is reachable but the database attribute is itself ``None``
          / empty (transient reconnect-style state).
        * ``None`` when the chain itself is unreachable (mocked session,
          alt session impl, connector refactor, …).
    """
    try:
        raw = session._conn._conn.database
    except Exception as exc:
        # ``Exception`` is intentional: this is intentionally walking private
        # Snowpark / connector attributes that may disappear or change shape
        # under us. Any failure here MUST surface as "connector view
        # unavailable, fall back" rather than failing the whole RPC. Log at
        # debug so a sudden flip to the slow path is investigable without
        # spamming production logs.
        logger.debug(
            "Connector chain session._conn._conn.database not readable "
            "(%s: %s); falling back to Session.get_current_database().",
            type(exc).__name__,
            exc,
        )
        return None
    if not raw:
        return _CONNECTOR_DB_PRESENT_BUT_UNSET
    return quote_name_without_upper_casing(raw)


def _get_session_cached_database(session: snowpark.Session) -> str | None:
    """Return the session's current database, cached on the session itself,
    with drift detection against the Snowflake connector.

    `Session.get_current_database()` resolves to the connector's `database`
    attribute when it's set, but falls back to `SELECT CURRENT_DATABASE()`
    (a Snowflake round-trip) if that attribute is transiently `None`. With
    ~60+ session-fetch call sites firing per RPC, even a low-probability
    round-trip on the hot path would dominate latency.

    The cache (`session._sas_cached_db`) is invalidated when the connector's
    own view of the current database has moved past it. This handles the
    case where the user switches the underlying Snowflake database after
    session attach via:

    * SCOS passthrough SQL — ``spark.sql("USE DATABASE x")`` with
      ``snowpark.connect.sql.passthrough=true``
    * Direct Snowpark — ``snowpark_session.sql("USE DATABASE x")`` against
      the underlying session
    * Snowpark helper APIs — ``session.use_database(...)`` /
      ``session.use_schema("x.y")``

    Without drift detection, `_sas_cached_db` would stay stale after any of
    those and `_ensure_cld_context_for_session` would keep emitting the
    pre-switch CLD identifier-transform mode until the session was
    recreated — silently breaking identifier casing on CLDs (or the
    reverse, leaking CLD case-preservation rules into a non-CLD database).

    Three connector-view states are handled distinctly:

    * Quoted name (e.g. ``"cldUnity"``) — drift compare against the cache.
      Same-DB cache stays untouched; different-DB cache is refreshed.
    * ``_CONNECTOR_DB_PRESENT_BUT_UNSET`` — the chain reads cleanly but the
      database attribute is currently ``None`` (transient reconnect /
      session reset). The cache is at risk of being stale relative to the
      underlying session, so we verify via ``Session.get_current_database()``
      (Snowflake round-trip) instead of trusting it.
    * ``None`` — the chain itself is unreachable (mocked session,
      alternative session implementation, …) AND no cache is available;
      fall back to ``Session.get_current_database()``. If we do have a
      cache and the chain is unreachable, keep the cache rather than
      pessimistically round-tripping on every call.

    Steady-state cost (chain readable + cache valid): one attribute read +
    one cache compare. No Snowflake round-trip.
    """
    cached = getattr(session, "_sas_cached_db", None)
    connector_db = _get_connector_current_database(session)

    if cached is not None and connector_db:
        if _normalize_database_name(cached) == _normalize_database_name(connector_db):
            return cached
        # Drift: the underlying session has moved to a new database
        # (USE DATABASE, session.use_database, …). Fall through to refresh.

    if connector_db:
        session._sas_cached_db = connector_db
        return connector_db

    # connector_db is now either ``""`` (chain present, db attr currently None)
    # or ``None`` (chain unreachable). Treat those differently: the first is
    # the exact situation Felix flagged where keeping a stale cache can hold
    # the wrong CLD context after a reconnect/session reset, so we verify
    # against Snowpark. The second is the mocked-session case where there's
    # no upstream value to verify against anyway.
    if connector_db == _CONNECTOR_DB_PRESENT_BUT_UNSET:
        verified = _refresh_database_from_snowpark(session)
        if verified is not None:
            return verified
        # Snowpark returned ``None`` too (e.g. session has no database at
        # all). Fall through to the cache as a last resort below.

    if cached is not None:
        return cached

    return _refresh_database_from_snowpark(session)


def _refresh_database_from_snowpark(session: snowpark.Session) -> str | None:
    """Round-trip to ``Session.get_current_database()`` and refresh the
    SCOS cache from the result. Returns ``None`` on error or when the
    session has no current database.
    """
    try:
        current_db = session.get_current_database()
    except Exception as exc:
        logger.debug(
            "Session.get_current_database() failed (%s: %s); leaving SCOS "
            "cache untouched.",
            type(exc).__name__,
            exc,
        )
        return None
    if current_db:
        session._sas_cached_db = current_db
    return current_db


def _ensure_cld_context_for_session(session: snowpark.Session) -> None:
    """Re-establish the session-level CLD ContextVar from `session`'s current
    database, skipping all work when the ContextVar already has the right
    `CLDInfo`.

    The ContextVar is reset at every RPC entry by `clear_context_data`
    (to avoid leakage when a gRPC worker thread is reused across sessions),
    so any code path that hands back an already-attached Snowpark session
    must repopulate it. But within a single RPC the session's database
    doesn't change, so the second and subsequent calls (one for each of
    ~60+ `get_or_create_snowpark_session()` / `_get_current_snowpark_session()`
    callsites) can short-circuit on `_current_cld_context.database_name`.

    Steady-state cost: one attribute read on the session + one ContextVar
    read + one string compare. No locks, no Snowflake round-trips.
    """
    current_db = _get_session_cached_database(session)
    if not current_db:
        return
    cache_key = _normalize_database_name(current_db)
    current = get_current_cld_context()
    if current.database_name == cache_key:
        return
    cld_info = get_cld_info(session, current_db)
    set_current_cld_context(cld_info)


def _get_current_snowpark_session() -> snowpark.Session | None:
    """Return the active Snowpark session (or None) and refresh the CLD hint.

    Many code paths fetch the session via this function directly instead of
    going through `get_or_create_snowpark_session`, so this is the right
    place to re-establish `_current_cld_context` after `clear_context_data`
    wipes it at RPC entry. Without this, request handlers that bypass the
    fast-path of `get_or_create_snowpark_session` (notably the read-table
    path) see `is_cld=False` for a CLD-attached session and emit non-CLD
    identifier transformations.
    """
    try:
        session = _get_active_session()
        # if session._conn._conn.expired:
        #     _remove_session(session)
        #     return self.create()
    except SnowparkClientException as ex:
        if ex.error_code == "1403":  # No session
            return None
        raise
    _ensure_cld_context_for_session(session)
    return session


def configure_snowpark_session(session: snowpark.Session):
    """Configure a snowpark session with required parameters and settings."""
    from snowflake.snowpark_connect.config import (
        get_cte_optimization_enabled,
        global_config,
        is_cte_optimization_enabled_for_connect_version,
        set_snowflake_parameters,
    )

    global SKIP_SESSION_CONFIGURATION

    logger.info(f"Configuring session {session}")

    telemetry.initialize(session)
    session._sprocs = set()

    # built-in udf cache
    init_builtin_udf_cache(session)
    init_spark_session_cache_registry(session)

    # file format cache
    session._file_formats = set()

    # Set experimental parameters (warnings globally suppressed)
    session.ast_enabled = False
    session.eliminate_numeric_sql_value_cast_enabled = False
    session.reduce_describe_query_enabled = True

    session._join_alias_fix = True
    session.connection.arrow_number_to_decimal_setter = True
    session.custom_package_usage_config["enabled"] = True

    # TODO(SNOW-3122222): Remove this once 10.6 is fully rolled out
    session._has_structured_try_cast = False

    # Scoped temp objects may not be accessible in stored procedure and cause "object does not exist" error. So disable
    # _use_scoped_temp_objects here and use temp table instead.
    session._use_scoped_temp_objects = False

    # SNOW-3409016: opt SAS sessions in to Snowpark-Python's structured type
    # INFER_SCHEMA parser unconditionally. When True, INFER_SCHEMA results
    # like ARRAY(NUMBER), OBJECT(name TEXT), MAP(TEXT, REAL) are parsed into
    # structured ArrayType/StructType/MapType, letting SAS skip sample-based
    # FLATTEN discovery in map_read_parquet and take the JSON fast path in
    # map_read_json.
    #
    # No client-side kill-switch is wired up because flipping this to False
    # is strictly worse than leaving it on — there is no scenario where the
    # legacy parser produces a better result than the structured one:
    #
    # * Backend returns structured types (params on): the legacy parser
    #   crashes (it ``int(...)``s a non-numeric token from a structured-type
    #   string, e.g. ``OBJECT(name VARCHAR(...), ...)``).  The exception is
    #   swallowed by ``DataFrameReader._infer_schema_for_file_format`` which
    #   then falls back to a single ``$1 VARIANT`` schema, *losing column
    #   names*.  SAS would have to FLATTEN-discover everything from scratch.
    # * Backend returns simple/bare types (params off, older deployments):
    #   the structured parser handles primitives and bare ``OBJECT/ARRAY/MAP``
    #   keywords identically to the legacy parser, returning VariantType for
    #   bare keywords.  Same result either way.
    #
    # The actual rollback knob is the backend-side parameter set:
    # ENABLE_INFER_SCHEMA_NESTED_SCHEMA_SUPPORT_FOR_SCOS,
    # ENABLE_INFER_SCHEMA_NESTED_SCHEMA_JSON_SUPPORT_FOR_SCOS.
    # Turning those off makes the backend stop emitting structured types;
    # the client flag's value is then irrelevant.
    session._use_structured_type_infer_schema = True

    # SNOW-2367714: ``snowpark.connect.structured_types.fix`` defaults to "true"
    # but is a *non-static* config, so its side-effect — flipping Snowpark's
    # ``snowpark.context._enable_fix_2360274`` via ``set_snowflake_parameters`` —
    # previously only ran on an explicit ``spark.conf.set(...)``. A session that
    # never touched the config kept Snowpark's library default (False), so a
    # structured non-nullable ``array<struct<...>>`` schema projection emitted the
    # malformed ``to_array(NULL :: OBJECT(...)) :: ARRAY(OBJECT(...))`` cast and
    # failed at compile time with ``002040 Unsupported data type
    # 'STRUCTURED_OBJECT'`` (field failure 01c4ea14-...-c762061b on prod2/Apptio).
    # Apply the configured default at session start so the fix is on unless the
    # user explicitly disables it.
    set_snowflake_parameters(
        "snowpark.connect.structured_types.fix",
        # Default to "true" if the key is somehow absent: a None would propagate
        # into ``str_to_bool`` and raise at session start.
        global_config.get("snowpark.connect.structured_types.fix", "true"),
        session,
    )

    # Configure CTE optimization based on session configuration
    # If get_cte_optimization_enabled() returns None, use snowpark-connect server parameter
    # (SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION) and Snowpark Connect version.
    # If explicitly set by user, use user's choice.
    cte_optimization_setting = get_cte_optimization_enabled()
    if cte_optimization_setting is not None:
        session.cte_optimization_enabled = cte_optimization_setting
        logger.info(f"CTE optimization set by user config: {cte_optimization_setting}")
    else:
        session.cte_optimization_enabled = (
            is_cte_optimization_enabled_for_connect_version(session)
        )
        logger.info(
            f"CTE optimization using snowpark-connect server default: "
            f"{session.cte_optimization_enabled}"
        )

    # Default query tag to be used unless overridden by user using AppName or spark.addTag()
    query_tag = "SNOWPARK_CONNECT_QUERY"

    default_fallback_timezone = "UTC"
    if global_config.spark_sql_session_timeZone is None:
        try:
            result = collect_without_telemetry(
                session.sql("SHOW PARAMETERS LIKE 'TIMEZONE'")
            )
            if result and len(result) > 0:
                value = result[0]["value"]
                logger.warning(
                    f"Using Snowflake session timezone parameter as fallback: {value}"
                )
            else:
                value = default_fallback_timezone
                logger.warning(
                    f"Could not determine timezone from parameters, defaulting to {default_fallback_timezone}"
                )
        except Exception as e:
            value = default_fallback_timezone
            logger.warning(
                f"Could not query Snowflake timezone parameter ({e}), defaulting to {default_fallback_timezone}"
            )
        global_config.spark_sql_session_timeZone = value

    session_params = {
        "TIMESTAMP_TYPE_MAPPING": "TIMESTAMP_LTZ",
        "TIMEZONE": f"'{global_config.spark_sql_session_timeZone}'",
        "QUOTED_IDENTIFIERS_IGNORE_CASE": "false",
        "PYTHON_SNOWPARK_ENABLE_THREAD_SAFE_SESSION": "true",
        "ENABLE_STRUCTURED_TYPES_IN_SNOWPARK_CONNECT_RESPONSE": "true",
        "QUERY_TAG": f"'{query_tag}'",
    }
    already_configured = getattr(session, "_scos_configured", False)

    # SNOW-2245971: Stored procedures inside Native Apps run as Execute As Owner and hence cannot set session params.
    if SKIP_SESSION_CONFIGURATION:
        session_param_names = ", ".join(session_params.keys())
        logger.info(
            f"Skipping Snowpark Connect session configuration as requested. Please make sure following session parameters are set correctly: {session_param_names}"
        )
    elif already_configured:
        logger.debug(
            f"Session {session} already configured; skipping ALTER SESSION reconfiguration."
        )
    else:
        collect_without_telemetry(
            session.sql(
                f"ALTER SESSION SET {', '.join([f'{k} = {v}' for k, v in session_params.items()])}"
            )
        )
        # TODO(SNOW-3122222): Move this to the `session_params` dict and remove the session variable
        # once 10.6 is fully rolled out
        try:
            result = collect_without_telemetry(
                session.sql("ALTER SESSION SET ENABLE_TRY_CAST_STRUCTURED_TYPES = true")
            )
            session._has_structured_try_cast = (
                len(result) == 1
                and hasattr(result[0], "status")
                and result[0].status == "Statement executed successfully."
            )
        except SnowparkSQLException:
            # If the query failed, that means the parameter is not available, and we cannot use TRY_CAST
            # in JSON casting operations.
            pass
        # TODO(SNOW-3316643): Once ENABLE_SCOS_FEATURE is available on all
        # deployments, move this to the `session_params` dict and remove the
        # try block.
        try:
            result = collect_without_telemetry(
                session.sql("ALTER SESSION SET ENABLE_SCOS_FEATURE = true")
            )
            session._enable_scos_feature = (
                len(result) == 1
                and hasattr(result[0], "status")
                and result[0].status == "Statement executed successfully."
            )
        except SnowparkSQLException:
            session._enable_scos_feature = False

    # SNOW-3484790: Kick off aggregation metadata prefetch in SCOS session initialization.
    # SNOW-3619967: user might have snowpark version that don't have this function.
    try:
        session._start_async_aggregation_prefetch_if_needed()
    except AttributeError as e:
        logger.warning(
            f"aggregation metadata prefetch is skipped because: {e}, please update snowpark version"
        )

    # Instrument the snowpark session to use a cache for describe queries.
    instrument_session_for_describe_cache(session)
    instrument_session_for_scos_query_tag(session)

    # Detect CLD context from the session's current database. `get_cld_info`
    # caches the answer so subsequent per-request re-establishment via
    # `_ensure_cld_context_for_session` runs in O(1). Read the result back
    # from the ContextVar instead of re-querying `get_current_database()`
    # / `get_cld_info()` just to log it.
    _ensure_cld_context_for_session(session)
    if is_in_cld_context():
        logger.info(
            f"CLD context detected for database: {get_current_cld_context().database_name}"
        )

    # SNOW-3517484: Marker used by server startup to avoid re-running full configuration
    # when the same Session object is passed back into _serve(...).
    session._scos_configured = True


def _is_running_in_SPCS():
    return (
        os.path.exists("/snowflake/session/token")
        and os.getenv("SNOWFLAKE_ACCOUNT") is not None
        and os.getenv("SNOWFLAKE_HOST") is not None
    )


def _is_running_in_stored_procedure_or_notebook():
    return PLATFORM == "XP"


def _get_session_configs_from_ENV() -> dict[str, Any]:
    session_configs = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "protocol": "https",
        "host": os.getenv("SNOWFLAKE_HOST"),
        "port": os.getenv("SNOWFLAKE_PORT", 443),
        "authenticator": "oauth",
        "token_file_path": "/snowflake/session/token",
        "client_session_keep_alive": True,
    }
    return session_configs


def get_or_create_snowpark_session(
    custom_configs: dict | None = None,
) -> snowpark.Session:
    """
    snowpark connect code should use this function to create or get snowpark session.

    Connection resolution (when not in SPCS):
    1. Use 'spark-connect' connection if it exists (backwards compatible)
    2. Use SNOWFLAKE_DEFAULT_CONNECTION_NAME env var if set
    3. Use default_connection_name from connections.toml if set
    4. Use 'default' connection if it exists
    5. If no connections.toml exists (e.g., Snowflake Notebooks), use existing session
    6. Error if connections.toml exists but no valid connection is configured
    """
    # Fast path: if a session already exists and no custom configs are requested,
    # return it immediately without running the connection resolver.
    # This avoids repeatedly reading connections.toml on every request.
    # `_get_current_snowpark_session` already calls
    # `_ensure_cld_context_for_session`, so no need to repeat it here.
    if custom_configs is None:
        existing_session = _get_current_snowpark_session()
        if existing_session is not None:
            return existing_session

    session_configs = {}
    if _is_running_in_SPCS():
        # Running in SPCS, use environment variables injected by SPCS run time
        # We don't use connections.toml file created by SPCS because of the 0600 permissions issue
        session_configs = _get_session_configs_from_ENV()
    elif not (custom_configs and "connection_name" in custom_configs):
        # Only resolve connection name if not explicitly provided in custom_configs.
        # Uses our custom resolver which properly handles default_connection_name
        # from connections.toml (Snowpark's built-in resolution has issues)
        from snowflake.snowpark_connect.utils.connection_resolver import (
            resolve_connection_name,
        )

        resolved_connection = resolve_connection_name()
        if resolved_connection is not None:
            session_configs["connection_name"] = resolved_connection
        # If None, don't set connection_name - let Snowpark use existing session or defaults

    if os.getenv("SNOWFLAKE_DATABASE") is not None:
        session_configs["database"] = os.getenv("SNOWFLAKE_DATABASE")

    if os.getenv("SNOWFLAKE_SCHEMA") is not None:
        session_configs["schema"] = os.getenv("SNOWFLAKE_SCHEMA")

    if os.getenv("SNOWFLAKE_WAREHOUSE") is not None:
        session_configs["warehouse"] = os.getenv("SNOWFLAKE_WAREHOUSE")

    # add custom session configs
    if custom_configs:
        session_configs.update(custom_configs)

    old_session = _get_current_snowpark_session()
    new_session = snowpark.Session.builder.configs(session_configs).getOrCreate()

    if old_session is None or old_session.session_id != new_session.session_id:
        # every new session needs to be configured
        configure_snowpark_session(new_session)
    else:
        # Existing session reused — repopulate the per-request CLD ContextVar
        # since `clear_context_data` reset it at RPC entry.
        _ensure_cld_context_for_session(new_session)

    return new_session


def set_query_tags(spark_tags: Sequence[str]) -> None:
    """Sets Snowpark session query_tag value to the tag from the Spark request."""

    if any("," in tag for tag in spark_tags):
        exception = ValueError("Tags cannot contain ','.")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # TODO: Tags might not be set correctly in parallel workloads or multi-threaded code.
    snowpark_session = get_or_create_snowpark_session()
    spark_tags_str = ",".join(sorted(spark_tags)) if spark_tags else None

    if spark_tags_str and spark_tags_str != snowpark_session.query_tag:
        snowpark_session.query_tag = spark_tags_str
