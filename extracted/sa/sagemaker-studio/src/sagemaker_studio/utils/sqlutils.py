import logging
from typing import Any, Dict, List, Optional, TypedDict, Union

import sagemaker_studio.utils.sql_handler as sql_handler
from sagemaker_studio.connections.helper_factory import HelperFactory
from sagemaker_studio.project import Project
from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy


class ConnectionConfig(TypedDict, total=False):
    """Connection configuration.

    Attributes:
        type: Connection type (e.g., 'spark')
    """

    type: str


logger = logging.getLogger()
logger.info("Importing sqlutils")

_project = None
_duckdb = None
_sql_executor = None


def sql(
    query: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    **kwargs,
):
    """
    Executes a SQL query on the specified connection and returns the result.

    Args:
        query (str): The SQL query to execute.
        parameters (Optional[Union[Dict[str, Any], List[str]]]): Optional parameters for the query.
        connection_id (Optional[str]): The ID of the DataZone connection to use for the query.
        connection_name (Optional[str]): The name of the DataZone connection to use for the query.
        connection (Optional[ConnectionConfig]): Connection details including type (e.g., {"type": "spark"}).

    Returns:
        DataFrame: Result of the SQL query execution.

    Raises:
        RuntimeError: If Project is not initialized when using connection_name or if there's an error executing the SQL query.
    """
    if not query or not query.strip():
        return None

    if _is_spark_connection(connection):
        spark = _ensure_spark()
        return spark.sql(query)

    # adding args anyway as we will filter out necessary args to pass down based on engine type
    _apply_athena_context(query, kwargs)
    engine = get_engine(connection_id, connection_name, **kwargs)
    if engine:
        result = next(_ensure_sql_executor().execute(engine, query, parameters))
        return result.result
    else:
        # Execute query locally using DuckDB if no connection specified
        return (lambda x: x.df() if x else None)(_ensure_duckdb().sql(query))


def sql_stream(
    query: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    error_strategy: str = ErrorStrategy.STOP_ON_ERROR,
    **kwargs,
):
    """
    Execute SQL statements and stream results progressively.

    Args:
        query (str): The SQL query to execute (can contain multiple statements).
        parameters (Optional[Union[Dict[str, Any], List[str]]]): Optional parameters for the query.
        connection_id (Optional[str]): The ID of the DataZone connection to use for the query.
        connection_name (Optional[str]): The name of the DataZone connection to use for the query.
        connection (Optional[ConnectionConfig]): Connection details including type (e.g., {"type": "spark"}).
        error_strategy (str): Error handling strategy - STOP_ON_ERROR (default) or CONTINUE_ON_ERROR.

    Returns:
        Generator[ExecutionResult]: Generator yielding ExecutionResult for each statement.

    Raises:
        RuntimeError: If Project is not initialized when using connection_name or if there's an error executing the SQL query.
    """
    if not query or not query.strip():
        return iter([])

    if _is_spark_connection(connection):
        from sagemaker_studio.sql_engine.spark_transformer import SparkTransformer
        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

        spark = _ensure_spark()
        statements = SparkTransformer.split_query(query)
        return SqlExecutor.execute_statements(
            statements,
            lambda stmt: spark.sql(stmt),
            error_strategy,
        )

    # adding args anyway as we will filter out necessary args to pass down based on engine type
    _apply_athena_context(query, kwargs)

    engine = get_engine(connection_id, connection_name, **kwargs)
    if engine:
        return _ensure_sql_executor().execute(engine, query, parameters, error_strategy)
    else:
        from sagemaker_studio.sql_engine.duckdb_transformer import DuckDBTransformer
        from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

        statements = DuckDBTransformer.split_query(query)
        return SqlExecutor.execute_statements(
            statements,
            lambda stmt: (lambda x: x.df() if x else None)(_ensure_duckdb().sql(stmt)),
            error_strategy,
        )


def sql_stream_with_display(
    query: str,
    dataframe_name: str,
    parameters: Optional[Union[Dict[str, Any], List[str]]] = None,
    connection_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    connection: Optional[ConnectionConfig] = None,
    error_strategy: str = ErrorStrategy.STOP_ON_ERROR,
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

    project = _ensure_project()
    if not project:
        raise RuntimeError("Project is not initialized.")

    # Need to handle connection_id case
    if connection_name:
        connection = project.connection(connection_name)
    elif connection_id:
        connection = project.connection(id=connection_id)

    sql_executor = _ensure_sql_executor()

    if connection.type not in sql_executor.get_supported_connection_types():
        raise RuntimeError(
            f"SQL is not supported for connection type {connection.type}. Supported types are {', '.join(sql_executor.get_supported_connection_types())}."
        )

    sql_helper = HelperFactory.get_sql_helper(connection.type)
    connection_config = sql_helper.to_sql_config(connection, **kwargs)

    return sql_executor.create_engine(connection.type, connection_config)


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


def _ensure_project():
    """Initialize Project on demand"""
    global _project
    if _project is None:
        try:
            _project = Project()
        except Exception:
            _project = False
    return _project


def _ensure_duckdb():
    """Initialize Project on demand"""
    global _duckdb
    if _duckdb is None:
        import duckdb as _duckdb

        # Refer to https://duckdb.org/duckdb-docs.pdf
        _duckdb.sql("SET python_scan_all_frames = true;")
        # Refer to https://duckdb.org/docs/stable/core_extensions/httpfs/s3api#credential_chain-provider
        _duckdb.sql("CREATE SECRET (TYPE s3, PROVIDER credential_chain);")
    return _duckdb


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


def _materialise_stream(stream, dataframe_name: str):
    """Consume a result stream, display/assign results in IPython, and return consolidated output."""
    logger.info("display/assign results")
    from IPython import get_ipython
    from IPython.display import display

    ip = get_ipython()

    results: list = []
    for result in stream:
        if result.status == "success":
            display(result.result)
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


logger.info("Finished importing sqlutils")
