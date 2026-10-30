import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Generator, List, Optional, TypedDict, Union
from uuid import uuid4

import sagemaker_studio.utils.sql_handler as sql_handler
from sagemaker_studio import local_kernel
from sagemaker_studio.connections.connection import SUPPORTED_IRC_GLUE_CONNECTION_TYPES, Connection
from sagemaker_studio.connections.helper_factory import HelperFactory
from sagemaker_studio.project import Project
from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy
from sagemaker_studio.utils import duckdbutils
from sagemaker_studio.utils._sql_cache import (
    ConnectionCache,
    ManagedConnection,
    reset_connection_state,
)


class ConnectionConfig(TypedDict, total=False):
    """Connection configuration.

    Attributes:
        type: Connection type (e.g., 'spark')
    """

    type: str


logger = logging.getLogger(__name__)
logger.info("Importing sqlutils")

_project = None
_sql_executor = None

# Kernel-lifetime cache of the project S3 root (async materialization write destination).
# project.s3.root triggers an uncached DataZone GetEnvironment call (~1.7s) on every read,
# but the value is invariant for a project within a kernel session, so resolve it once.
_project_s3_root = None

# Dedicated Glue-backed Spark session for IRC queries, created when the kernel's
# default spark session is not Glue-backed. Cached for the kernel lifetime so
# repeated IRC queries reuse one Glue session instead of starting one per call.
_glue_spark = None

# Module-level state for query history metadata.
# Stores lightweight metadata from the last SQL execution so the kernel
# can include it in the execute_reply. Cleared at the start of each execution.
_last_sql_execution_metadata = None

# Module-level singleton instance (persists in kernel namespace)
_connection_cache = ConnectionCache()


def _make_cache_key(connection_id: Optional[str], connection_name: Optional[str], **kwargs) -> str:
    """Create cache key from connection identifier and relevant kwargs.

    Args:
        connection_id: Connection ID
        connection_name: Connection name
        **kwargs: Additional configuration parameters

    Returns:
        str: Composite cache key incorporating connection identifier and relevant config
    """
    base_key = connection_id or connection_name or "default"

    # Only include kwargs that affect engine configuration
    relevant_keys = ["catalog_name", "schema_name", "database_name"]
    config_parts = [f"{k}={kwargs[k]}" for k in relevant_keys if k in kwargs]

    if config_parts:
        return f"{base_key}::{':'.join(sorted(config_parts))}"
    return base_key


def _get_or_create_connection(
    connection_id: Optional[str],
    connection_name: Optional[str],
    dz_conn: Connection,
    persist_session: bool,
    **kwargs,
) -> Optional[ManagedConnection]:
    """
    Get cached connection or create new one.

    Args:
        persist_session: cache the engine AND an eagerly-opened live connection, reused
            across calls for session continuity (temp tables, transaction state) and to
            reclaim the engine build. The cached live connection is also what the async
            path reuses so it builds only one boto3 client per query (avoids the
            "Cannot inject class attribute upload_file" double-injection).

    Returns:
        Optional[ManagedConnection]: engine plus optional connection (None when
            persist_session=False); None if engine creation fails.

    On an AWS Notebook local kernel ``persist_session`` is ignored: the engine is built for the
    statement and not kept, so its first request fetches the connection's credentials from the
    app and no cell runs on credentials an earlier cell was vended (a profile switch in the app
    takes effect on the next cell). The engines a local kernel can build (Athena) carry no
    session state worth keeping.
    """
    if local_kernel.is_local_kernel():
        persist_session = False
    cache_key = _make_cache_key(connection_id, connection_name, **kwargs)

    # Try cache first (persist_session reuses across calls)
    if persist_session and cache_key:
        cached = _connection_cache.get(cache_key)
        if cached:
            return cached

    # Create new engine
    engine = _get_engine_from_connection(
        dz_conn, connection_id=connection_id, connection_name=connection_name, **kwargs
    )

    if not engine:
        return None

    # For persisted sessions, create and cache connection
    if persist_session and cache_key:
        conn = engine.connect()
        managed_conn = ManagedConnection(
            engine=engine, connection=conn, id=str(uuid4()), cache_key=cache_key
        )
        _connection_cache.put(cache_key, managed_conn)
        return managed_conn

    # For non-persisted sessions, return ephemeral ManagedConnection
    return ManagedConnection(engine=engine, connection=None, id=str(uuid4()), cache_key=cache_key)


def sql(
    query: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    persist_session: bool = True,
    **kwargs,
):
    """
    Execute a SQL query and return the result as a DataFrame.

    Supports session persistence (default enabled) for connection reuse across calls,
    enabling temporary tables, transaction state, and automatic credential refresh.

    Args:
        query (str): The SQL query to execute.
        parameters (Optional[Union[Dict[str, Any], List[str]]]): Optional parameters for the query.
        connection_id (Optional[str]): The ID of the DataZone connection to use for the query.
        connection_name (Optional[str]): The name of the DataZone connection to use for the query.
        connection (Optional[ConnectionConfig]): Connection details including type (e.g., {"type": "spark"}).
        persist_session: Cache and reuse connection (default True). Ignored on an AWS Notebook
            local kernel, where every statement builds its engine with credentials fetched
            from the app at that moment.
        catalog_name, schema_name (keyword arguments): For Athena, the query's execution context.
            For a DuckDB query with no connection, the attached catalog (see
            :func:`attach_local_catalogs`) and schema put first on DuckDB's ``search_path`` while it
            runs; one DuckDB does not have is
            :class:`~sagemaker_studio.exceptions.CatalogUnavailableError` before the query runs.

    Returns:
        DataFrame: Result of the SQL query execution.

    Note:
        Use close_connection() or close_all_connections() to close cached connections.

    Raises:
        RuntimeError: If Project is not initialized when using connection_name or if there's an error executing the SQL query.
    """
    if not query or not query.strip():
        return None

    route = _route(connection, connection_id, connection_name, parameters)
    if route.engine == _ENGINE_SPARK:
        return _ensure_spark().sql(query)
    if route.engine == _ENGINE_GLUE_IRC:
        return _execute_irc_connection_query(query, route.connection)
    if route.engine == _ENGINE_DUCKDB:
        with duckdbutils._duckdb_cell(kwargs) as duck:
            return duckdbutils._run_duckdb_statement(duck, query)

    # adding args anyway as we will filter out necessary args to pass down based on engine type
    _apply_athena_context(query, kwargs)

    if route.engine == _ENGINE_ATHENA:
        from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus
        from sagemaker_studio.utils.athena_v4 import execute_query_statements

        athena_api = _athena_api(route.connection, kwargs, parameters, required=True)
        result = next(
            execute_query_statements(athena_api, query, ErrorStrategy.STOP_ON_ERROR), None
        )
        if result is None:
            return None
        if result.status != ExecutionStatus.SUCCESS.value:
            raise RuntimeError(result.error or "Athena query failed")
        return result.result

    cached = _require_engine(
        _get_or_create_connection(
            connection_id, connection_name, route.connection, persist_session, **kwargs
        ),
        route.connection,
    )
    result = next(
        _ensure_sql_executor().execute(
            cached.engine,
            query,
            connection=cached.connection,  # May be None for non-persisted
            parameters=parameters,
        )
    )
    return result.result


def sql_stream(
    query: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    error_strategy: str = ErrorStrategy.STOP_ON_ERROR,
    persist_session: bool = True,
    **kwargs,
):
    """
    Execute SQL statements and stream results progressively.

    Supports session persistence (default enabled) for connection reuse across calls,
    enabling temporary tables, transaction state, and automatic credential refresh.

    Args:
        query (str): The SQL query to execute (can contain multiple statements).
        parameters (Optional[Union[Dict[str, Any], List[str]]]): Optional parameters for the query.
        connection_id (Optional[str]): The ID of the DataZone connection to use for the query.
        connection_name (Optional[str]): The name of the DataZone connection to use for the query.
        connection (Optional[ConnectionConfig]): Connection details including type (e.g., {"type": "spark"}).
        error_strategy (str): Error handling strategy - STOP_ON_ERROR (default) or CONTINUE_ON_ERROR.
        persist_session: Cache and reuse connection (default True). Ignored on an AWS Notebook
            local kernel, where every statement builds its engine with credentials fetched
            from the app at that moment.
        catalog_name, schema_name (keyword arguments): For Athena, the query's execution context.
            For DuckDB statements with no connection, the attached catalog (see
            :func:`attach_local_catalogs`) and schema put first on DuckDB's ``search_path`` until
            the stream is exhausted or closed; one DuckDB does not have is
            :class:`~sagemaker_studio.exceptions.CatalogUnavailableError` at the first result.

    Returns:
        Generator[ExecutionResult]: Generator yielding ExecutionResult for each statement.

    Note:
        Use close_connection() or close_all_connections() to close cached connections.

    Raises:
        RuntimeError: If Project is not initialized when using connection_name or if there's an error executing the SQL query.
    """
    if not query or not query.strip():
        return iter([])

    route = _route(connection, connection_id, connection_name, parameters)
    if route.engine == _ENGINE_SPARK:
        from sagemaker_studio.sql_engine.spark_transformer import SparkTransformer
        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

        spark = _ensure_spark()
        statements = SparkTransformer.split_query(query)

        # Force schema resolution to catch errors eagerly (e.g., TABLE_OR_VIEW_NOT_FOUND).
        # Without this, spark.sql() is lazy and returns successfully even for invalid tables
        # the error only surfaces later in IPython's display formatter where it's swallowed,
        # causing execute_reply to return OK while an error message appears on iopub.
        def _spark_executor(stmt):
            df = spark.sql(stmt)
            df.schema
            return df

        return _stream_and_capture_metadata(
            SqlExecutor.execute_statements(
                statements,
                _spark_executor,
                error_strategy,
            ),
            connection_type="SPARK",
        )

    if route.engine == _ENGINE_GLUE_IRC:
        from sagemaker_studio.sql_engine.spark_transformer import SparkTransformer
        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

        statements = SparkTransformer.split_query(query)

        def execute_stmt(stmt):
            return _execute_irc_connection_query(stmt, route.connection)

        return SqlExecutor.execute_statements(
            statements,
            execute_stmt,
            error_strategy,
        )
    if route.engine == _ENGINE_DUCKDB:
        from sagemaker_studio.sql_engine.duckdb_transformer import DuckDBTransformer
        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

        statements = DuckDBTransformer.split_query(query)

        def _run_statements(duck):
            # ``duck`` is the cell's engine: every statement of the stream runs on it.
            def _run_duckdb(stmt):
                return duckdbutils._run_duckdb_statement(duck, stmt)

            return SqlExecutor.execute_statements(statements, _run_duckdb, error_strategy)

        # The metadata capture wraps the cell, not the other way round: its reset of
        # _last_sql_execution_metadata happens now, as for every other engine, while the cell is
        # still entered when the first result is asked for.
        return _stream_and_capture_metadata(
            duckdbutils._in_duckdb_cell(kwargs, _run_statements), connection_type="DUCKDB"
        )

    if route.engine == _ENGINE_ATHENA:
        from sagemaker_studio.utils.athena_v4 import execute_query_statements

        _apply_athena_context(query, kwargs)
        athena_api = _athena_api(route.connection, kwargs, parameters, required=True)
        return _stream_and_capture_metadata(
            execute_query_statements(athena_api, query, error_strategy),
            connection_id=connection_id,
            connection_type="ATHENA",
        )

    # adding args anyway as we will filter out necessary args to pass down based on engine type
    _apply_athena_context(query, kwargs)

    cached = _require_engine(
        _get_or_create_connection(
            connection_id, connection_name, route.connection, persist_session, **kwargs
        ),
        route.connection,
    )
    conn_type = cached.engine.get_execution_options().get("connection_type", "")
    return _stream_and_capture_metadata(
        _ensure_sql_executor().execute(
            cached.engine,
            query,
            connection=cached.connection,  # May be None for non-persisted
            parameters=parameters,
            error_strategy=error_strategy,
        ),
        connection_id=connection_id,
        connection_type=conn_type,
    )


def _execute_irc_connection_query(query: str, resolved_dz_conn: Connection):
    spark = _ensure_glue_spark()
    try:
        df = spark.sql(query)
        df.schema
        return df
    except Exception as e:
        if (
            resolved_dz_conn.type in SUPPORTED_IRC_GLUE_CONNECTION_TYPES
            and "org.apache.iceberg.exceptions.NotAuthorizedException" in str(e)
        ):
            # The stored token was rejected, so force a refresh rather than re-reading
            # the same token from the connection's secret.
            spark_catalog_configs = resolved_dz_conn._spark_catalog_configs(
                force_token_refresh=True
            )
            if not spark_catalog_configs:
                raise
            catalog_names = json.loads(spark_catalog_configs["SOURCE_CATALOG_LIST"])
            for catalog_name in catalog_names:
                access_token = spark_catalog_configs["ACCESS_TOKEN"]
                spark.conf.set(f"spark.sql.catalog.{catalog_name}.token", access_token)
            # Force schema resolution like the initial attempt, so a failure of the
            # retried query surfaces here instead of later, lazily.
            retried_df = spark.sql(query)
            retried_df.schema
            return retried_df
        else:
            raise


def sql_stream_with_display(
    query: str,
    dataframe_name: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    error_strategy: str = ErrorStrategy.STOP_ON_ERROR,
    materialize: str = "sync",
    **kwargs,
):
    """
    Execute SQL statements, materialise results into the IPython namespace, and display them.

    Each successful result is assigned to the IPython user namespace as
    ``<dataframe_name>_<index>``, displayed, and the consolidated result
    (single DataFrame or list) is stored under ``<dataframe_name>``.

    On error, partial results are saved for debugging and the error is raised.

    Args:
        query (str): The SQL query to execute (can contain multiple statements).
        dataframe_name (str): Variable name prefix for storing results in the IPython namespace.
        parameters (Optional[Union[Dict[str, Any], List[str]]]): Optional parameters for the query.
        connection_id (Optional[str]): The ID of the DataZone connection to use for the query.
        connection_name (Optional[str]): The name of the DataZone connection to use for the query.
        connection (Optional[ConnectionConfig]): Connection details including type (e.g., {"type": "spark"}).
        error_strategy (str): Error handling strategy - STOP_ON_ERROR (default) or CONTINUE_ON_ERROR.

    Raises:
        Exception: If any statement fails, after saving partial results for debugging.
    """
    # first_page_rows is an async-only display knob. Pop it so it never reaches the sync
    # fallback's sql_stream(**kwargs) -> connection build (harmless today, latent otherwise).
    first_page_rows = kwargs.pop("first_page_rows", None)

    if materialize == "async":
        # Returns True when the async path fully handled the query. Returns False only
        # from the pre-execution eligibility phase (nothing ran yet) -> safe to fall back
        # to sync. Once statements execute, the async path raises rather than returning
        # False, so we never re-run side-effecting statements via the sync path below.
        async_kwargs = dict(kwargs)
        if first_page_rows is not None:
            async_kwargs["first_page_rows"] = first_page_rows
        if _stream_with_async_materialization(
            query,
            dataframe_name,
            parameters=parameters,
            connection_id=connection_id,
            connection_name=connection_name,
            connection=connection,
            error_strategy=error_strategy,
            **async_kwargs,
        ):
            return

    stream = sql_stream(
        query,
        parameters=parameters,
        connection_id=connection_id,
        connection_name=connection_name,
        connection=connection,
        error_strategy=error_strategy,
        **kwargs,
    )
    _materialise_stream(stream, dataframe_name)


def _bind_succeeded_partials(specs, dataframe_name, resolved_dz_conn, conn_type, read_chunks=None):
    """Option-A parity: on a mid-cell async failure, bind the statements that already
    succeeded as plain DataFrames (df_0, df_1, ...) so the user keeps them for debugging,
    matching the sync path. These are sync-materialized (rows read now by execution_id) --
    async first-page display never ran for this aborted cell. Best-effort per spec; a
    single bind failure is logged and skipped, never masking the original statement error.
    """
    from pandas import DataFrame

    from sagemaker_studio.utils import sqlutils_async_reader as _reader

    try:
        from IPython import get_ipython
    except Exception:
        return
    ip = get_ipython()
    if ip is None:
        return

    for spec in specs:
        var_name = f"{dataframe_name}_{spec.index}"
        try:
            if spec.kind == "dml":
                ip.user_ns[var_name] = spec.rowcount
            elif spec.kind == "result" and spec.execution_id:
                if read_chunks is not None:
                    columns, chunks, _total = read_chunks(spec.execution_id)
                else:
                    columns, chunks, _total = _reader.open_result_reader(
                        resolved_dz_conn, conn_type, spec.execution_id
                    )
                rows = [r for chunk in chunks for r in chunk]
                ip.user_ns[var_name] = DataFrame(rows, columns=columns)
        except Exception:
            logger.debug("Failed to bind partial result %s before raising", var_name, exc_info=True)


def _stream_with_async_materialization(
    query: str,
    dataframe_name: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    error_strategy: str = ErrorStrategy.STOP_ON_ERROR,
    **kwargs,
) -> bool:
    """Attempt the async materialization path.

    Returns True if the async path handled the query (first page(s) displayed inline +
    background thread(s) spawned); False to signal the caller to fall back to the
    synchronous path. Scope: Athena/Redshift result-bearing statements (single- or
    multi-statement cells).
    """
    from sqlalchemy import text

    # Async path is Athena/Redshift SQL only -- not Spark, IRC-Glue, or local DuckDB.
    #
    # Phase 1 -- eligibility + setup. Nothing has executed yet, so any negative result
    # or unexpected error here returns False and the caller safely runs the sync path.
    from sagemaker_studio.sql_engine.sql_executor import ExecutionStatus, SingleStatementResult
    from sagemaker_studio.utils import sqlutils_async as _async
    from sagemaker_studio.utils import sqlutils_async_reader as _reader

    try:
        # Async path implements STOP_ON_ERROR semantics only; for CONTINUE_ON_ERROR fall
        # back to sync (pre-execution) so behavior matches the sync path exactly.
        if error_strategy != ErrorStrategy.STOP_ON_ERROR:
            return False
        # The async path materializes pages into the project's S3 root, which an AWS Notebook
        # local kernel does not have: run its statements synchronously instead.
        if local_kernel.is_local_kernel():
            return False
        route = _route(connection, connection_id, connection_name, parameters)
        if route.engine not in (_ENGINE_ATHENA, _ENGINE_NATIVE):
            return False
        resolved_dz_conn = route.connection
        if resolved_dz_conn.type not in _async.ASYNC_SUPPORTED_CONNECTION_TYPES:
            return False

        _apply_athena_context(query, kwargs)
        athena_api = _athena_api(resolved_dz_conn, kwargs, parameters)
        if athena_api is not None:
            # Athena: execute directly through the AWS API, without a SQLAlchemy/PyAthena engine.
            cached = None
            executor = None
            conn_type = "ATHENA"
            transformer = None
        else:
            # Acquire the connection the same way the sync path does: default persist_session=True
            # (reuse one live connection across cells -- reclaims the ~1s engine build and, by
            # reusing that single connection for the statement execution below via
            # connection=cached.connection, keeps the async path at one client build per query so
            # the "Cannot inject class attribute upload_file" double-build never happens). Honor a
            # caller-supplied persist_session=False (the disable-persist-session kill switch): that
            # yields connection=None, and the executor then opens exactly one connection itself --
            # still a single build, no collision.
            # first_page_rows is a display-layer knob, not a connection param -- exclude it.
            persist_session = kwargs.get("persist_session", True)
            conn_kwargs = {
                k: v for k, v in kwargs.items() if k not in ("persist_session", "first_page_rows")
            }
            cached = _get_or_create_connection(
                connection_id,
                connection_name,
                resolved_dz_conn,
                persist_session=persist_session,
                **conn_kwargs,
            )
            if not cached:
                return False

            executor = _ensure_sql_executor()
            conn_type = cached.engine.get_execution_options().get("connection_type", "")
            transformer = executor._get_transformer(conn_type)
    except Exception:
        logger.debug("Async eligibility/setup failed; falling back to sync", exc_info=True)
        return False

    # Reuse SqlExecutor.execute for the split, the single connection across statements
    # (session / temp tables preserved), and error-strategy handling. We inject a
    # per-statement executor that captures each result-bearing statement's execution_id
    # without materializing rows here; the rows are read later by execution_id via a fresh
    # client. On Redshift we also opt the cursor out of its eager first-page download (see
    # _skip_eager_result_load below), which otherwise duplicated that fetch.
    def _async_statement_executor(connection, statement, params):
        # On the Redshift Data API path, tell the DB-API connection to skip the eager
        # first-page GetStatementResult download inside Cursor.execute. The async reader
        # re-fetches that page by statement_id with a fresh client, so the cursor's eager
        # fetch is a pure duplicate -- and for large results it is a ~6-9s/8.5MB download
        # that scales with LIMIT. We only need the execution_id/metadata here, which the
        # cursor still captures. Best-effort and Redshift-only; any failure to set the flag
        # just leaves the (correct) eager-fetch behavior in place.
        #
        # The cached connection is shared kernel-lifetime across BOTH the async and sync
        # paths (persist_session=True), so the opt-out must be confined to THIS statement:
        # we restore the previous value in a finally, otherwise a later plain sync sql()
        # on the same connection would silently inherit the skip.
        raw = None
        prev = None
        toggled = False
        if (conn_type or "").upper() == "REDSHIFT":
            try:
                raw = connection.connection.dbapi_connection
                if hasattr(raw, "_skip_eager_result_load"):
                    prev = raw._skip_eager_result_load
                    raw._skip_eager_result_load = True
                    toggled = True
            except Exception:
                logger.debug(
                    "Could not set _skip_eager_result_load; eager fetch stays on", exc_info=True
                )
        try:
            result = connection.execute(text(statement), params or {})
        finally:
            if toggled:
                raw._skip_eager_result_load = prev
        # Return a SingleStatementResult (like _execute_single) so execute_statements
        # propagates execution_metadata into each ExecutionResult -- otherwise the
        # _stream_and_capture_metadata wrap below records None and query history is lost.
        try:
            metadata = transformer.get_execution_metadata(result.cursor)
        except Exception:
            logger.debug("Failed to extract execution metadata for async path", exc_info=True)
            metadata = None
        if not result.returns_rows:
            return SingleStatementResult(result=result.rowcount, execution_metadata=metadata)
        return SingleStatementResult(
            result=_async.AsyncResultMarker(
                execution_id=_async.extract_execution_id(metadata),
                redshift_query_id=_async.extract_redshift_query_id(metadata),
            ),
            execution_metadata=metadata,
        )

    # Phase 2 -- committed. Statements execute here and may have side effects (DML), so we
    # must NOT fall back to the sync path (which would re-run them); errors propagate.
    # Wrap in _stream_and_capture_metadata so the async path populates the module-level
    # _last_sql_execution_metadata (query history / execute_reply) just like the sync path.
    #
    # executor.execute() holds `with engine.connect() as conn:` open across its yields, so
    # raising mid-iteration (the error branch below, or the RuntimeError after the loop) would
    # abandon the suspended generator and leak the pooled connection until GC. Closing the
    # generator on every exit path throws GeneratorExit into it, unwinding that `with` and
    # returning the checkout to the pool deterministically -- important now the async engine is
    # cached kernel-lifetime rather than discarded per cell. Guard on close() so a non-generator
    # iterable (already fully drained, nothing to release) is a harmless no-op.
    specs: List[Any] = []
    if athena_api is not None:
        from sagemaker_studio.utils.athena_v4 import execute_query_statements

        statement_results = execute_query_statements(
            athena_api, query, error_strategy, athena_api.execute_without_fetch
        )
    else:
        statement_results = executor.execute(
            cached.engine,
            query,
            connection=cached.connection,
            parameters=parameters,
            error_strategy=error_strategy,
            statement_executor=_async_statement_executor,
        )
    _result_stream = _stream_and_capture_metadata(
        statement_results,
        connection_id=connection_id,
        connection_type=conn_type,
    )
    try:
        for exec_result in _result_stream:
            if exec_result.status != ExecutionStatus.SUCCESS.value:
                # A statement errored -- raise (matching the sync path) rather than returning
                # False, which would re-execute the already-run statements via sync.
                # Option A parity: before raising, bind the statements that already succeeded as
                # plain DataFrames (df_0..df_{k-1}), matching the sync path's partial-save for
                # debugging. Async display (Phase 2) never ran for this aborted cell, so these
                # are sync-materialized DataFrames, not async first-page cards -- best-effort,
                # never masking the original error.
                try:
                    _bind_succeeded_partials(
                        specs,
                        dataframe_name,
                        resolved_dz_conn,
                        conn_type,
                        read_chunks=athena_api.read_chunks if athena_api is not None else None,
                    )
                except Exception:
                    logger.debug("Failed to bind partial results before raising", exc_info=True)
                # Defensive: we reuse the cached persisted connection across cells, so clear
                # any aborted-transaction state a failed statement may have left before the
                # next cell reuses it. Verified a no-op on Athena (PyAthena) and Redshift
                # (Data API) -- both leave the txn active-not-deactivated -- but this guards
                # any transactional engine/driver where reuse would otherwise raise
                # PendingRollbackError. Best-effort; never mask the original error.
                if cached is not None:
                    reset_connection_state(cached.connection)
                raise Exception(exec_result.error)
            specs.append(_async.spec_from_result(exec_result))

        result_specs = [s for s in specs if s.kind == "result"]
        if any(s.execution_id is None for s in result_specs):
            # No execution_id to read the result back by, and re-running is unsafe -- surface
            # it instead of silently double-executing through the sync fallback.
            raise RuntimeError(
                "Async materialization: missing execution_id for a result-bearing statement"
            )
    finally:
        _close = getattr(_result_stream, "close", None)
        if callable(_close):
            # Swallow any close-time error: this finally runs while a SQL error may be
            # propagating, and an exception here would REPLACE it, hiding the real failure.
            try:
                _close()
            except Exception:
                logger.debug("Error closing result stream", exc_info=True)

    # Connection-independent reader per result-bearing statement, built lazily by
    # materialize_async_multi (the Connection stays captured in this closure).
    #
    # UI-configurable inline first-page size (default 999 = one Athena round-trip). Clamped to
    # [1, MAX]: larger N pulls more pages in the synchronous reply (~N/1000 round-trips), trading
    # first-paint latency for inline rows. Invalid/missing -> default (logged, not silent, so a
    # headless run with a bad value leaves a trace).
    _requested = kwargs.get("first_page_rows", _reader.INLINE_FIRST_PAGE_ROWS)
    # bool is an int subclass -- reject it so first_page_rows=True is not read as 1 row.
    if isinstance(_requested, bool):
        logger.warning("Ignoring non-integer first_page_rows=%r; using default", _requested)
        first_page_rows = _reader.INLINE_FIRST_PAGE_ROWS
    else:
        try:
            first_page_rows = int(_requested)
        except (TypeError, ValueError):
            logger.warning("Ignoring invalid first_page_rows=%r; using default", _requested)
            first_page_rows = _reader.INLINE_FIRST_PAGE_ROWS
        else:
            # Symmetric clamp to [1, MAX], matching the documented contract.
            first_page_rows = max(1, min(first_page_rows, _reader.MAX_INLINE_FIRST_PAGE_ROWS))

    def _reader_factory(execution_id):
        if athena_api is not None:
            columns, chunks, total_rows = athena_api.read_chunks(execution_id)
            first_page, remaining = _reader.split_first_page(chunks, first_page_rows)
            stats_fn = None
            if total_rows is None:

                def stats_fn():  # noqa: F811 -- deliberate per-factory closure
                    return _reader.read_athena_output_rows(athena_api.client, execution_id)

            return columns, first_page, remaining, total_rows, stats_fn
        # For Athena, build ONE credentialed client up front and share it between the result
        # reader and the stats fetcher below. This avoids a second Session.client() creation
        # on the background thread (the create_client step exposed to the boto3 "Cannot
        # inject class attribute upload_file" attribute-injection race) and removes the need
        # for a per-cell failure cache -- there is now a single build, on the foreground
        # thread. If the build fails, stats simply fall back to the exact counted row_count.
        athena_client = None
        if (conn_type or "").upper() == "ATHENA":
            try:
                athena_client = resolved_dz_conn.create_client("athena")
            except Exception:
                logger.debug("Failed to build Athena client for async read/stats", exc_info=True)
                athena_client = None
        columns, chunks, total_rows = _reader.open_result_reader(
            resolved_dz_conn,
            conn_type,
            execution_id,
            athena_client=athena_client,
            first_page_convert_rows=first_page_rows,
        )
        # Pull up to first_page_rows for the inline first page (default 999 = ONE round-trip).
        # The background thread still re-buffers the full result into ROWS_PER_PAGE (10k) S3
        # pages -- the remaining chunk iterator carries every row past the inline page.
        first_page, remaining = _reader.split_first_page(chunks, first_page_rows)
        # Athena-only exact-total fetcher, called off the background page loop (never the
        # foreground). Redshift already returns the exact total_rows inline above, so it
        # gets no stats_fn (None) and never touches GetQueryRuntimeStatistics. Reuses the
        # SAME client the reader used (built once above), so stats never build a client on
        # the daemon thread; if that client is None (build failed), stats yield None and
        # total_rows falls back to the exact counted row_count.
        stats_fn = None
        if (conn_type or "").upper() == "ATHENA" and athena_client is not None:

            def stats_fn():  # noqa: F811 -- deliberate per-factory closure
                return _reader.read_athena_output_rows(athena_client, execution_id)

        return columns, first_page, remaining, total_rows, stats_fn

    # Resolve the S3 write destination now, just before materializing. Statements have already
    # executed (side effects committed), so this must NOT fall back to sync -- a missing
    # destination is a hard error here, mirroring the missing-execution_id raise above.
    # Cached for the kernel lifetime -- project.s3.root re-runs a ~1.7s DataZone GetEnvironment
    # call on every access otherwise.
    project_s3_root = _ensure_project_s3_root()
    if not project_s3_root:
        raise RuntimeError(
            "Async materialization: could not resolve the project S3 write destination"
        )

    # Handles result-bearing statements (async S3 materialization) AND DML-only cells
    # (synchronous display + namespace bind), so every executed cell is fully handled here.
    _async.materialize_async_multi(
        base_name=dataframe_name,
        specs=specs,
        project_s3_root=project_s3_root,
        reader_factory=_reader_factory,
        display_fn=_async._default_display,
        assign_namespace_fn=_async._default_assign_namespace,
        write_page_fn=_async._default_write_page,
        write_manifest_fn=_async._default_write_manifest,
        emit_ready_fn=_async._default_emit_dataframe_ready,
        bind_pending_fn=_async._default_bind_pending,
    )
    return True


def get_engine(
    connection_id: Optional[str] = None, connection_name: Optional[str] = None, **kwargs
):
    """
    Returns the SQL engine for the specified connection.

    Args:
        connection_id (Optional[str]): The ID of the DataZone connection to get the SQL engine for.
        connection_name (Optional[str]): The name of the DataZone connection to get the SQL engine for.

    Returns:
        The SQL engine instance for executing queries.

    Raises:
        ValueError: If multiple connection parameters are provided
        RuntimeError: If project initialization fails or if SQL is not supported for this connection type.
    """

    provided_params = sum(x is not None for x in [connection_id, connection_name])
    if provided_params == 0:
        # No connection provided, use local DuckDB engine
        return None
    if provided_params > 1:
        raise ValueError("Only one of connection_id or connection_name should be provided")

    conn = _resolve_connection(connection_id, connection_name)
    return _get_engine_from_connection(
        conn, connection_id=connection_id, connection_name=connection_name, **kwargs
    )


def _create_credential_provider(credential_getter):
    """Factory that creates a credential provider from a getter function."""

    def credential_provider():
        creds = credential_getter()
        expiry = creds.expiration

        if not expiry:
            # Default to 15 min from now if no expiry provided
            expiry = datetime.now(timezone.utc) + timedelta(minutes=15)

        return {
            "access_key_id": creds.access_key_id,
            "secret_access_key": creds.secret_access_key,
            "session_token": creds.session_token,
            "expiration": expiry.isoformat(),
        }

    return credential_provider


# The engines a statement runs on (see _route).
_ENGINE_SPARK = "SPARK"  # the kernel's Spark session
_ENGINE_GLUE_IRC = "GLUE_IRC"  # a Glue-backed Spark session, for Iceberg REST catalog connections
_ENGINE_DUCKDB = "DUCKDB"  # the kernel's DuckDB
_ENGINE_ATHENA = "ATHENA"  # the SDK-owned native Athena API executor
_ENGINE_NATIVE = "NATIVE"  # another connection's SQLAlchemy engine


@dataclass(frozen=True)
class _Route:
    """Where a statement runs: the engine, and the connection it runs with (None for none)."""

    engine: str
    connection: Optional[Connection] = None


def _route(
    connection: Optional[ConnectionConfig],
    connection_id: Optional[str],
    connection_name: Optional[str],
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
) -> _Route:
    """Decide which engine runs a statement, from the arguments ``sql``, ``sql_stream`` and the
    async path take. The one place this decision is made:

    - ``connection={"type": "spark"}``: the kernel's Spark session.
    - An Iceberg REST catalog connection: a Glue-backed Spark session.
    - An Athena connection: the SDK-owned native Athena API executor, whatever engine the
      workgroup runs.
    - Any other connection: the connection's own SQLAlchemy engine, in every mode (an S3
      connection has none, and is refused as such).
    - No connection: DuckDB.
    """
    if _is_spark_connection(connection):
        return _Route(_ENGINE_SPARK)
    resolved = _resolve_connection(connection_id, connection_name)
    if resolved is None:
        return _Route(_ENGINE_DUCKDB)
    if resolved.type in SUPPORTED_IRC_GLUE_CONNECTION_TYPES:
        return _Route(_ENGINE_GLUE_IRC, resolved)
    if _engine_type_of(resolved) == "ATHENA":
        return _Route(_ENGINE_ATHENA, resolved)
    return _Route(_ENGINE_NATIVE, resolved)


def _require_engine(
    cached: Optional[ManagedConnection], connection: Optional[Connection]
) -> ManagedConnection:
    """The connection's engine, or a clear error when none could be built for it."""
    if cached is None:
        name = getattr(connection, "name", None) or getattr(connection, "id", None)
        raise RuntimeError(f"Could not create a SQL engine for connection {name!r}.")
    return cached


def _resolve_connection(connection_id: str, connection_name: str):
    """Resolve a connection by name or id. Returns None if neither is provided."""
    if not connection_name and not connection_id:
        return None
    project = _ensure_project()
    if not project:
        raise RuntimeError("Project is not initialized.")
    if connection_name:
        return project.connection(connection_name)
    return project.connection(id=connection_id)


def _engine_type_of(conn: Connection) -> Optional[str]:
    """
    The engine ``conn``'s statements run on: :attr:`Connection.sql_engine_type`, which is the
    connection type except for a LAKEHOUSE catalog connection naming an Athena workgroup (the
    AWS Notebook app's catalog connection), which runs on Athena. That rule lives there only; a
    connection-like object without the attribute runs on its ``type``.
    """
    engine_type = getattr(conn, "sql_engine_type", None)
    return engine_type if isinstance(engine_type, str) else conn.type


def _get_engine_from_connection(
    conn: Connection,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    **kwargs,
):
    """Create a SQL engine from an already-resolved connection. Returns None if conn is None."""
    if conn is None:
        return None

    sql_executor = _ensure_sql_executor()

    engine_type = _engine_type_of(conn)
    if engine_type not in sql_executor.get_supported_connection_types():
        raise RuntimeError(
            f"SQL is not supported for connection type {conn.type}. Supported types are {', '.join(sql_executor.get_supported_connection_types())}."
        )

    sql_helper = HelperFactory.get_sql_helper(engine_type)

    # Create credential provider that refreshes credentials
    if connection_id or connection_name:
        # Re-fetch connection for fresh credentials
        def credential_getter():
            return _resolve_connection(connection_id, connection_name).connection_creds

    else:
        # Fall back to cached credentials when identifiers not available
        def credential_getter():
            return conn.connection_creds

    kwargs["credential_provider"] = _create_credential_provider(credential_getter)

    connection_config = sql_helper.to_sql_config(conn, **kwargs)

    return sql_executor.create_engine(engine_type, connection_config)


def _athena_api(resolved_dz_conn, kwargs: dict, parameters=None, required: bool = False):
    """Return the SDK-owned executor for an Athena connection.

    Optional probes return ``None`` for non-Athena or incomplete connections. Public query entry
    points set ``required`` so malformed Athena configuration raises instead of falling through to
    local DuckDB.
    """
    from sagemaker_studio.utils.athena_v4 import athena_executor

    if resolved_dz_conn is None or _engine_type_of(resolved_dz_conn) != "ATHENA":
        return None

    credential_provider = None
    if isinstance(resolved_dz_conn, Connection):
        connection_id = getattr(resolved_dz_conn, "id", None)
        connection_name = getattr(resolved_dz_conn, "name", None)

        def credential_getter():
            if isinstance(connection_id, str) and connection_id:
                return _resolve_connection(connection_id, None).connection_creds
            if isinstance(connection_name, str) and connection_name:
                return _resolve_connection(None, connection_name).connection_creds
            return resolved_dz_conn.connection_creds

        credential_provider = _create_credential_provider(credential_getter)

    executor_kwargs = {
        "catalog": kwargs.get("catalog_name"),
        "schema": kwargs.get("schema_name"),
        "selected_engine_version": (
            kwargs.get("selected_engine_version") or kwargs.get("engine_version")
        ),
        "parameters": parameters,
    }
    if credential_provider is not None:
        executor_kwargs["credential_provider"] = credential_provider
    executor = athena_executor(resolved_dz_conn, **executor_kwargs)
    if required and executor is None:
        raise ValueError(
            "Athena connection requires a non-empty workgroup_name and connection id or name"
        )
    return executor


def _apply_athena_context(query: str, kwargs: dict) -> None:
    """Extract catalog/database from the query and inject into kwargs for the engine.

    If catalog_name and schema_name are already passed from older UI logic, this is a no-op.
    """
    if "catalog_name" in kwargs and "schema_name" in kwargs:
        return

    execution_ctx = sql_handler.get_execution_context(query)
    catalog = execution_ctx.get("catalog")
    database = execution_ctx.get("database")
    logger.debug(f"Found catalog {catalog} database: {database}")
    if catalog and database:
        kwargs["catalog_name"] = catalog
        kwargs["schema_name"] = database


def list_connections() -> List[Dict[str, Any]]:
    """
    List all active persistent database connections.

    Returns:
        List[Dict[str, Any]]: List of connection details including:
            - id: Unique identifier for this cache entry (use with close_connection)
            - cache_key: Full cache key including configuration
            - created_at: When the connection was created
            - last_used: When the connection was last used

    Example:
        >>> connections = list_connections()
        >>> for conn in connections:
        ...     print(f"ID: {conn['id']}, Key: {conn['cache_key']}")
        >>> # Close a specific connection
        >>> close_connection(id=connections[0]['id'])
    """
    return [
        {
            "id": mc.id,
            "cache_key": mc.cache_key,
            "created_at": mc.created_at,
            "last_used": mc.last_used,
        }
        for mc in _connection_cache.snapshot()
    ]


def close_connection(id: str) -> bool:
    """
    Close a specific persistent database connection by its unique ID.

    Args:
        id (str): The unique identifier of the connection to close.
                  Obtain this from list_connections().

    Returns:
        bool: True if connection was found and closed, False if not found.

    Example:
        >>> connections = list_connections()
        >>> close_connection(id=connections[0]['id'])
        True
    """
    return _connection_cache.remove_by_id(id)


def close_all_connections() -> int:
    """
    Close all persistent database connections.

    Also stops the dedicated Glue Spark session created for Iceberg REST catalog
    queries, if one exists (not counted in the returned total).

    Returns:
        int: Number of connections closed.

    Example:
        >>> count = close_all_connections()
        >>> print(f"Closed {count} connections")
    """
    _stop_glue_spark()
    from sagemaker_studio.utils import athena_v4

    athena_v4.clear_cache()
    return _connection_cache.clear()


def _ensure_project():
    """Initialize Project on demand"""
    global _project
    if _project is None:
        try:
            _project = Project()
        except Exception:
            _project = False
    return _project


def _ensure_project_s3_root():
    """Resolve the project S3 root once and cache it for the kernel lifetime.

    project.s3.root re-runs a DataZone GetEnvironment call (~1.7s) on every access; the
    value does not change within a session, so cache the first successful lookup. Returns
    None on failure (caller falls back to sync), and does NOT cache the failure so a later
    call can retry.
    """
    global _project_s3_root
    if _project_s3_root:
        return _project_s3_root
    if local_kernel.is_local_kernel():
        return None  # an AWS Notebook workspace has no project S3 root
    project = _ensure_project()
    root = getattr(getattr(project, "s3", None), "root", None) if project else None
    if root:
        _project_s3_root = root
    return root


def _reset_local_kernel_state() -> None:
    """Forget the Project built for a previous local-kernel configuration (tests, embedders); the
    attached catalogs and the engine's credential-chain secret go on the same reset."""
    global _project, _project_s3_root
    _project = None
    _project_s3_root = None


local_kernel.add_reset_listener(_reset_local_kernel_state)


# --- The project's data catalogs on DuckDB: the entry points the kernel and the frontend call ----
# (the DuckDB side is ``duckdbutils``; what is attached and how is ``duckdb_engine.catalogs``)


def attach_local_catalogs() -> List[Dict[str, Any]]:
    """
    Attach the project's data catalogs to the kernel's DuckDB, afresh from the project's connections
    as listed now (:func:`duckdbutils.attach_catalogs`), signing with ``credential_chain`` secrets;
    no connection's credentials are fetched. For the kernel to call at start and the frontend on
    every sign-in, sign-out, profile switch or connection change; an empty listing (signed out)
    leaves nothing attached.

    Returns:
        The attached databases, as :func:`list_attached_catalogs` reports them (a connection that
        could not be attached is on its entry, with the reason); empty when the kernel has no
        project to list connections from.

    Raises:
        RuntimeError: The connections could not be listed; what was attached before stays.
        LocalAppUnavailableError: The AWS Notebook app could not be reached for the listing.
    """
    project = _ensure_project()
    if not project:
        logger.warning("No project to list connections from; nothing is attached to DuckDB")
        return list_attached_catalogs()
    try:
        records = project._connection_service.list_connection_records()
    except Exception as e:
        # The frontend's call shows the user nothing: the log is where this failure is seen.
        logger.warning(
            "Could not list the project's connections; the attached catalogs are unchanged: %s", e
        )
        raise
    return duckdbutils.attach_catalogs(records)


detach_local_catalogs = duckdbutils.detach_local_catalogs  # the frontend's sign-out call
list_attached_catalogs = duckdbutils.list_attached_catalogs  # the frontend's catalog selector


def _ensure_sql_executor():
    """Initialize SqlExecutor on demand"""
    global _sql_executor
    if _sql_executor is None:
        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

        _sql_executor = SqlExecutor()
    return _sql_executor


def _ensure_spark():
    """Get Spark session from kernel namespace"""
    try:
        from IPython import get_ipython

        ipython = get_ipython()
        if ipython is None:
            raise RuntimeError("IPython kernel not available")

        spark = ipython.user_ns.get("spark")
        if spark is None:
            raise RuntimeError("Spark session not initialized in kernel namespace")

        return spark
    except ImportError:
        raise RuntimeError("IPython not available - Spark execution requires Jupyter kernel")


def _get_kernel_spark():
    """Return the spark object from the IPython user namespace, or None if unavailable."""
    try:
        from IPython import get_ipython

        ipython = get_ipython()
        if ipython is None:
            return None
        return ipython.user_ns.get("spark")
    except ImportError:
        return None


def _spark_session_is_glue(spark) -> bool:
    """Best-effort check whether a kernel spark object is backed by a Glue session.

    Only LazySparkSession exposes its session manager, so anything else cannot be
    positively identified as Glue and is treated as non-Glue. A LazySparkSession
    whose manager has not been resolved yet is resolved here (connection lookups
    only — this does not start a session) and the manager is assigned back so the
    lazy session does not resolve a second time.

    Note: LazySparkSession fakes its __class__ as SparkSession and its __getattr__
    creates a session on unknown-attribute access, so the inspection goes through
    the instance __dict__ instead of isinstance/getattr.
    """
    instance_dict = getattr(spark, "__dict__", None)
    if not isinstance(instance_dict, dict) or "_session_manager" not in instance_dict:
        return False

    session_manager = instance_dict["_session_manager"]
    if session_manager is None:
        try:
            from sagemaker_studio.utils.spark.connection_resolver import (
                _resolve_connection_and_create_session_manager,
            )

            session_manager = _resolve_connection_and_create_session_manager(
                connection_name=instance_dict.get("_connection_name"),
                config=instance_dict.get("_config"),
                spark_conf=instance_dict.get("_spark_conf"),
            )
            spark._session_manager = session_manager
        except Exception as e:
            # Deliberately broad: resolution can fail with many exception types
            # (notebook metadata lookup, GetConnection, network). Failing the query
            # here would be worse than falling back, but the fallback creates a
            # dedicated Glue session — if the kernel spark was in fact Glue-backed,
            # that duplicates its session for the kernel lifetime, so surface the
            # failure loudly.
            logger.error(
                "Could not resolve the kernel spark session's backend; treating it as "
                "non-Glue and falling back to a dedicated Glue session for Iceberg "
                f"REST catalog queries: {e}"
            )
            return False

    return type(session_manager).__name__ == "GlueSparkSessionManager"


def _create_glue_spark(config=None, spark_conf=None):
    """Create a Spark session backed by the project's Glue compute connection.

    Iceberg REST catalog queries require a Glue Spark session (the catalog configs
    and vendor network path are wired for Glue), so the project's connections are
    searched for a Glue compute connection rather than assuming the notebook's
    default compute is Glue.

    Args:
        config: Optional ClientConfig whose overrides["glue"] tune CreateSession
            fields, carried over from the kernel spark session when available.
        spark_conf: Optional user Spark config overrides, carried over likewise.
    """
    try:
        from sagemaker_studio.utils.spark.connection_resolver import _identify_service_from_props
        from sagemaker_studio.utils.spark.session.glue.glue_spark_session_manager import (
            GlueSparkSessionManager,
        )
        from sagemaker_studio.utils.spark.session.lazy_spark_session import LazySparkSession
    except ImportError as e:
        raise RuntimeError(
            "PySpark is not available - querying Iceberg REST catalog connections "
            "requires a Spark-enabled kernel"
        ) from e

    project = _ensure_project()
    if not project:
        raise RuntimeError("Project is not initialized.")

    glue_connection = next(
        (
            conn
            for conn in project.connections
            if getattr(conn, "type", None) in ("SPARK", "SPARK_CONNECT")
            and _identify_service_from_props(conn) == "GLUE"
        ),
        None,
    )
    if glue_connection is None:
        raise RuntimeError(
            "Querying an Iceberg REST catalog connection requires a Glue Spark "
            "session, but no Glue compute connection was found in this project. "
            "Add a Glue compute connection to the project and try again."
        )

    logger.info(
        f"Creating a Glue Spark session for IRC queries using connection "
        f"'{getattr(glue_connection, 'name', None)}'"
    )
    # Mirror the GLUE branch of connection_resolver._create_session_manager so the
    # dedicated session honors the same ClientConfig overrides and user spark_conf
    # a normally-resolved Glue session would.
    manager_kwargs = {}
    if config is not None:
        manager_kwargs["config"] = config
    session_manager = GlueSparkSessionManager(
        connection=glue_connection,
        connection_name=getattr(glue_connection, "name", None),
        spark_conf=spark_conf,
        **manager_kwargs,
    )
    return LazySparkSession(session_manager=session_manager)


def _stop_glue_spark() -> None:
    """Stop the dedicated Glue-backed Spark session for IRC queries, if one exists.

    Safe to call multiple times; failures to stop are logged rather than raised so
    shutdown paths are never blocked.
    """
    global _glue_spark
    if _glue_spark is None:
        return
    try:
        _glue_spark.stop()
    except Exception as e:
        logger.warning(f"Error stopping the dedicated Glue Spark session: {e}")
    finally:
        _glue_spark = None


def _ensure_glue_spark():
    """Get a Glue-backed Spark session for Iceberg REST catalog queries.

    The kernel's default `spark` cannot be assumed to be Glue-backed (the default
    compute is Athena Spark Connect), so it is reused only when it is positively
    identified as Glue. Otherwise a dedicated Glue session is created from the
    project's Glue compute connection and cached for the kernel lifetime.
    """
    global _glue_spark

    # Reuse the dedicated session when one was already created: its existence means
    # the kernel spark was previously determined not to be Glue-backed, and
    # short-circuiting avoids re-running the kernel backend check (which performs
    # connection resolution network calls) on every query.
    if _glue_spark is not None:
        return _glue_spark

    kernel_spark = _get_kernel_spark()
    if kernel_spark is not None and _spark_session_is_glue(kernel_spark):
        return kernel_spark

    # Carry over the user's ClientConfig and spark_conf from the kernel's lazy
    # session (sparkutils.init arguments) when present, so the dedicated Glue
    # session honors the same overrides.
    kernel_dict = getattr(kernel_spark, "__dict__", None)
    kernel_dict = kernel_dict if isinstance(kernel_dict, dict) else {}
    _glue_spark = _create_glue_spark(
        config=kernel_dict.get("_config"),
        spark_conf=kernel_dict.get("_spark_conf"),
    )

    # Stop the server-side Glue session on interpreter shutdown so it is not left
    # running until Glue's idle timeout. _stop_glue_spark is idempotent, so a
    # duplicate registration after a stop/recreate cycle is harmless.
    import atexit

    atexit.register(_stop_glue_spark)
    return _glue_spark


def _is_spark_connection(connection: Optional[ConnectionConfig] = None) -> bool:
    """Check if connection dict specifies Spark"""
    if not connection:
        return False

    conn_type = connection.get("type", "")
    if conn_type == "spark":
        return True
    elif conn_type:
        raise ValueError(
            f"connection object is currently supported for Spark only. "
            f"Use connection_id or connection_name for other engines. Got type: {conn_type}"
        )
    return False


def _result_display_metadata(result) -> Dict[str, Any]:
    """Jupyter display_data metadata for one statement result: the Redshift query id if assigned."""
    from sagemaker_studio.utils.sqlutils_async import extract_redshift_query_id

    query_id = extract_redshift_query_id(getattr(result, "execution_metadata", None))
    return {"redshift_query_id": query_id} if query_id is not None else {}


def _materialise_stream(stream, dataframe_name: str):
    """Consume a result stream, display/assign results in IPython, and return consolidated output."""
    logger.info("display/assign results")
    from IPython import get_ipython
    from IPython.display import display

    ip = get_ipython()

    results: list = []
    for result in stream:
        if result.status == "success":
            display(result.result, metadata=_result_display_metadata(result))
            results.append(result)
        else:
            # Save partial results for debugging before raising
            if len(results) > 0:
                for r in results:
                    ip.user_ns[f"{dataframe_name}_{r.statement_index}"] = r.result
            raise Exception(result.error)

    # No results — nothing to assign
    if not results:
        return

    # All statements succeeded - save indexed vars if multiple results
    if len(results) > 1:
        for r in results:
            ip.user_ns[f"{dataframe_name}_{r.statement_index}"] = r.result

    # Save main variable
    final = results[0].result if len(results) == 1 else [r.result for r in results]
    ip.user_ns[dataframe_name] = final


def _stream_and_capture_metadata(
    stream: Generator,
    connection_id: Optional[str] = None,
    connection_type: Optional[str] = None,
) -> Generator:
    """Wrap a result stream to capture per-statement execution metadata.

    Yields results unchanged while storing lightweight metadata (statement text,
    status, engine-specific info) on the module for downstream consumers.
    Writes incrementally so metadata is available even if iteration is interrupted.

    Note: state reset happens eagerly at call time. The actual iteration is
    delegated to an inner generator so callers don't see stale metadata between
    invocation and the first next() call.
    """
    global _last_sql_execution_metadata
    _last_sql_execution_metadata = []  # Eagerly reset on call

    def _inner():
        # try/finally so that closing THIS generator (GeneratorExit from _result_stream.close())
        # propagates to `stream` -- the executor generator that holds `with engine.connect()`
        # open across its yields. A plain `for` loop would abandon that generator to GC on
        # close() rather than unwinding its context manager deterministically.
        try:
            for result in stream:
                entry = {
                    "statement_index": getattr(result, "statement_index", 0),
                    "statement": getattr(result, "statement", ""),
                    "status": getattr(result, "status", "success"),
                    "execution_metadata": getattr(result, "execution_metadata", None),
                }
                if getattr(result, "error", None):
                    entry["error"] = result.error
                if connection_id:
                    entry["connection_id"] = connection_id
                if connection_type:
                    entry["connection_type"] = connection_type
                _last_sql_execution_metadata.append(entry)
                yield result
        finally:
            _close = getattr(stream, "close", None)
            if callable(_close):
                # Swallow any close-time error: closing may run while an exception is
                # propagating out of the loop, and raising here would replace it.
                try:
                    _close()
                except Exception:
                    logger.debug("Error closing wrapped executor stream", exc_info=True)

    return _inner()


logger.info("Finished importing sqlutils")
