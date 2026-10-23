#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import logging
import os
from collections.abc import Sequence
from typing import Any

import snowflake.snowpark_connect.tcm as tcm
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
    scos_internal_query_tag,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import (
    init_spark_session_cache_registry,
)
from snowflake.snowpark_connect.utils.table_metadata_cache import (
    instrument_session_for_table_metadata_cache,
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
# ``None``. In SCOS this means exactly one thing: the attribute was never
# seeded, because nothing fed this connection a ``finalDatabaseName`` (the
# stored-procedure case — see ``_seed_connector_session_context``). It cannot
# mean "cleared by a reconnect": every authenticator SCOS uses stubs
# ``reauthenticate()`` to ``{"success": False}``, so the login handler that
# would null it is unreachable. Revisit if SCOS ever adopts the browser /
# id-token / OAuth code-grant authenticators, which do implement it.
#
# This is distinct from ``None`` (the chain itself is unreachable, e.g. a
# mocked session or a future connector refactor that removed the private
# chain), which is the one case where a Snowpark round-trip is justified.
_CONNECTOR_DB_PRESENT_BUT_UNSET = ""

# Attribute holding a database resolved without the connector's help: ``None``
# when the seed found no current database to assert, or whatever
# ``_resolve_database_from_snowpark`` last returned. Read only while the
# connector attribute is empty, so in the overwhelmingly common case (the seed
# issued a ``USE``) it is never consulted at all. Absent means "no answer yet".
_CACHED_DB_ATTR = "_sas_cached_db"
_UNSET = object()


def _get_connector_current_database(
    session: snowpark.Session,
) -> str | None:
    """Best-effort, no-round-trip read of the Snowflake connector's view of
    the current database, normalized to match ``Session.get_current_database()``.

    The connector refreshes ``connection.database`` from the
    ``finalDatabaseName`` of every query response (``connection.py:1917``), so
    once it holds a value it tracks the session for free — through explicit
    ``USE DATABASE`` and through implicit moves such as ``CREATE DATABASE``.
    That makes it the authoritative source of truth, not merely a hint,
    provided it has been seeded; see ``_seed_connector_session_context``.

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
          / empty (never seeded — the stored-procedure case).
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


def _seed_connector_session_context(session: snowpark.Session) -> None:
    """Make the connector's ``database`` / ``schema`` attributes usable for the
    life of the session, so reading them never costs a Snowflake round-trip.

    A normal client gets these populated from its login response. A SCOS server
    hosted in a stored procedure (code bundles, ``snowpark-submit`` SPROC
    workloads, TCM) does not: nothing feeds that connection a
    ``finalDatabaseName``, so the attributes stay ``None`` for the whole run.
    ``Session.get_current_database()`` is then no longer a free attribute read
    — it silently degrades to ``SELECT CURRENT_DATABASE()``. SCOS calls it (and
    ``get_current_schema()``) from ~20 call sites, roughly seven times per
    Spark Connect request, which measured as 73 metadata queries and 8.1 s of a
    17.5 s code-bundle run (SNOW-4231647). Full analysis in
    ``docs/perf-rca/sproc-current-database-round-trips.md``.

    Re-asserting the context with ``USE SCHEMA`` fixes it at the root: the
    statement is a semantic no-op, but unlike ``SELECT`` it comes back with a
    ``finalDatabaseName`` / ``finalSchemaName`` that the connector latches onto.
    From that point the attributes track the session on their own, including
    implicit moves such as ``CREATE DATABASE``.

    ``USE SCHEMA`` rather than ``USE DATABASE`` because ``USE DATABASE`` also
    moves the current schema to ``PUBLIC``, which would relocate a session
    sitting elsewhere.

    Costs two queries, once, and only for sessions whose attribute is unset;
    for every normal client this is a single attribute read and nothing else.

    Not called when ``SKIP_SESSION_CONFIGURATION`` is set, because ``USE
    SCHEMA`` changes session state and owner's-rights procedures forbid that.
    The ``USE`` is still failure-tolerant for any environment that forbids it
    without setting the flag.
    """
    if _get_connector_current_database(session) != _CONNECTOR_DB_PRESENT_BUT_UNSET:
        return

    try:
        row = collect_without_telemetry(
            session.sql("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
        )[0]
        database, schema = row[0], row[1]
    except Exception as exc:
        logger.debug(
            "Could not resolve session context to seed the connector "
            "attributes (%s: %s); database reads will round-trip.",
            type(exc).__name__,
            exc,
        )
        return

    if not database:
        # Nothing to assert, but the absence is itself the answer. Recording it
        # is what stops ``_get_session_cached_database`` re-asking forever.
        # This is the case when the session is created without a database.
        # Note it affects the corner case if the session was created with no database
        # but the user workload itself created a database using SQL "CRETAT DATABASE".
        # In this case, the older code without the negative caching of _CACHED_DB_ATTR
        # will return new database as the current database. The trade-off of vastly
        # reduced round-trips for SPROCs (aka Code Bundles) is deemed acceptable.
        setattr(session, _CACHED_DB_ATTR, None)
        return

    if not schema:
        # A current database without a current schema requires dropping the
        # schema the session was sitting in, and there is no statement that
        # re-asserts the database without also moving the schema. Leave the
        # attribute unseeded; the reader resolves this once per session.
        logger.debug(
            "Session has database %s but no current schema; skipping the "
            "connector seed.",
            database,
        )
        return

    qualified = (
        f"{quote_name_without_upper_casing(database)}."
        f"{quote_name_without_upper_casing(schema)}"
    )
    try:
        collect_without_telemetry(session.sql(f"USE SCHEMA {qualified}"))
    except Exception as exc:
        logger.debug(
            "USE SCHEMA %s failed while seeding the connector attributes "
            "(%s: %s); database reads will round-trip.",
            qualified,
            type(exc).__name__,
            exc,
        )


def _get_session_cached_database(session: snowpark.Session) -> str | None:
    """Return the session's current database without a Snowflake round-trip.

    The connector attribute is authoritative in both directions once
    ``_seed_connector_session_context`` has run: a value means that database,
    and empty means the seed found none to assert. It also self-maintains, so
    there is nothing to invalidate when the user switches database via
    passthrough ``spark.sql("USE DATABASE x")``, ``session.use_database(...)``
    or direct Snowpark — the next read simply returns the new value.

    Two cases do not resolve from the attribute:

    * The session has no current database, so there was nothing to assert and
      the attribute stays empty. ``_CACHED_DB_ATTR`` records that, and because
      it is consulted only while the attribute is empty, a later ``USE`` takes
      precedence automatically and it cannot go stale.
    * The seed never ran or could not assert the context — the session skipped
      ``configure_snowpark_session``, or the connector chain is unreachable
      (mocked session, alternative session implementation, connector
      refactor). Here there is no free signal, so resolve via Snowpark once
      and memoize, including a ``None`` result: that is a legitimate answer
      rather than a failure.

    Steady-state cost: one attribute read. No Snowflake round-trip.
    """
    connector_db = _get_connector_current_database(session)
    if connector_db:
        return connector_db

    seeded = getattr(session, _CACHED_DB_ATTR, _UNSET)
    if seeded is not _UNSET:
        return seeded

    return _resolve_database_from_snowpark(session)


def _resolve_database_from_snowpark(session: snowpark.Session) -> str | None:
    """Round-trip to ``Session.get_current_database()`` and memoize the answer
    on the session. Returns ``None`` when the session has no current database
    (memoized) or when the call failed (not memoized, so it is retried).
    """
    try:
        with scos_internal_query_tag():
            current_db = session.get_current_database()
    except Exception as exc:
        logger.debug(
            "Session.get_current_database() failed (%s: %s); not memoizing.",
            type(exc).__name__,
            exc,
        )
        return None
    setattr(session, _CACHED_DB_ATTR, current_db)
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

    # Instrument the snowpark session to use a cache for describe queries.
    instrument_session_for_describe_cache(session)
    instrument_session_for_table_metadata_cache(session)
    instrument_session_for_scos_query_tag(session)
    # Installed first, before anything here issues SQL. Everything below --
    # the ``Session.__str__`` lookups in the log line, the ALTER SESSIONs, the
    # seeding -- is SCOS plumbing that query history otherwise cannot tell from
    # user SQL, and the statement-level QUERY_TAG only exists once these hooks
    # are in place. Tag building issues no queries of its own (the base tag is
    # an attribute read, the caller frame is thread-local), so running it this
    # early cannot re-enter the connection.
    #
    # ``telemetry.report_query`` runs inside the describe-cache wrapper and is
    # a no-op until a request is in flight, which is what makes this safe ahead
    # of ``telemetry.initialize`` below. Keep that property if it changes.

    # Lazy ``%s``: ``Session.__str__`` interpolates five ``CURRENT_*`` lookups,
    # which are Snowflake round-trips until the connector attributes are
    # seeded below. An f-string would pay for them even when the record is
    # filtered out — and at INFO they are paid for regardless, which is why the
    # tag instrumentation above has to already be in place.
    #
    # Tagged internal: the probes belong to this log statement, not to anything
    # the user asked for. ``configure_snowpark_session`` runs more than once per
    # process (the ``_scos_configured`` guard below only skips the ALTER
    # SESSION block, not this line), so without the wrapper each call leaves an
    # unattributable ``CURRENT_DATABASE()``/``CURRENT_SCHEMA()`` pair in query
    # history.
    with scos_internal_query_tag():
        logger.info("Configuring session %s", session)

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

    # Scoped temp objects are not accessible inside the stored procedure that
    # hosts the embedded (TCM) server and cause an "object does not exist"
    # error, so force plain temp objects there. Other paths (regular clients
    # and Native Apps) keep Snowpark's default so scoped temp objects work in
    # owner's-rights procedures.
    if tcm.TCM_MODE:
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
    if global_config.snowpark_connect_use2000AsTwoDigitCenturyStart:
        session_params["TWO_DIGIT_CENTURY_START"] = "2000"
    already_configured = getattr(session, "_scos_configured", False)

    # SNOW-2245971: Stored procedures inside Native Apps run as Execute As Owner and hence cannot set session params.
    if SKIP_SESSION_CONFIGURATION:
        session_param_names = ", ".join(session_params.keys())
        logger.info(
            f"Skipping Snowpark Connect session configuration as requested. Please make sure following session parameters are set correctly: {session_param_names}"
        )
    elif already_configured:
        logger.debug(
            "Session %s already configured; skipping ALTER SESSION reconfiguration.",
            session,
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

    # SNOW-3484790: Drain the aggregation metadata prefetch (SHOW FUNCTIONS)
    # synchronously so it completes inside session configuration rather than
    # bleeding into the first filter() call. Session.__init__() already fired
    # the async query; _retrieve harvests the in-flight result (blocking on
    # job.result()) and publishes the aggregation function set. On a cold GS
    # function-catalog cache this takes up to 20s — without the drain, the
    # first filter() in caller code blocks on the leftover wait, silently
    # inflating measured query time.
    # SNOW-3619967: user might have snowpark version that don't have this function.
    #
    # Tagged internal: when the async job fired by ``Session.__init__()`` is
    # unavailable or failed, ``_retrieve`` falls back to a synchronous metadata
    # query (``show functions ->> select ... is_aggregate``, or an
    # ``information_schema.functions`` variant depending on the Snowpark
    # version). That runs here, after the tag hooks are installed, so without
    # the wrapper it lands in query history as plain SCOS query text. The async
    # query itself is issued inside ``Session.__init__()``, before SCOS can
    # instrument the session, and keeps the bare session-level tag.
    try:
        with scos_internal_query_tag():
            session._retrieve_aggregation_function_list()
    except AttributeError as e:
        logger.warning(
            f"aggregation metadata prefetch is skipped because: {e}, please update snowpark version"
        )

    # Populate the connector's database/schema attributes before
    # anything reads them, so every later `get_current_database()` /
    # `get_current_schema()` is an attribute read instead of a query. No-op
    # outside a stored procedure, where login already populated them.
    #
    # Gated on the same flag as the ALTER SESSION above, and for the same
    # reason (SNOW-2245971): the seed works by re-asserting the context with
    # `USE SCHEMA`, and owner's-rights procedures — Native Apps, Data Clean
    # Rooms — reject any statement that changes session state. Those sessions
    # keep resolving the database through Snowpark, which costs one query per
    # session rather than one per call.
    if not SKIP_SESSION_CONFIGURATION:
        _seed_connector_session_context(session)

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
