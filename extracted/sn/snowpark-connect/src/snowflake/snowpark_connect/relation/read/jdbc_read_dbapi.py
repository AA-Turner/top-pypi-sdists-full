#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import datetime
import decimal
import os
import tempfile
import threading
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, as_completed, wait
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

import pytz
from _decimal import ROUND_HALF_EVEN, ROUND_HALF_UP
from dateutil import parser

import snowflake.snowpark
from snowflake.connector.options import pandas as pd
from snowflake.snowpark import DataFrameReader
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    get_temp_type_for_object,
    normalize_local_file,
    random_name_for_temp_object,
)
from snowflake.snowpark.dataframe import DataFrame
from snowflake.snowpark.types import (
    BinaryType,
    DataType,
    DateType,
    DecimalType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
    _NumericType,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation import jdbc_utils
from snowflake.snowpark_connect.relation.neo4j_utils import (
    validate_and_normalize_neo4j_labels,
    validate_cypher_identifier,
)
from snowflake.snowpark_connect.relation.read.utils import (
    DATA_SOURCE_SQL_COMMENT,
    Connection,
    exponential_backoff,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


class JdbcDialect:
    """
    Base class for datasource dialect.
    It defines default behavior for any unsupported datasource dialect.
    """

    def __init__(self, datasource_name: str) -> None:
        self.datasource_name = datasource_name

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: Always True as this is register last and provide default JDBC functionality.
        """
        return True

    def get_max_varchar_length(self) -> int:
        """
        Get the maximum size of the VARCHAR datatype supported.
        :return: max varchar size
        """
        return 16 * 1024 * 1024

    def get_double_type_name(self) -> str:
        """
        Get the DOUBLE type string name. SQL Server support it as REAL.
        :return: String name of DOUBLE datatype
        """
        return "DOUBLE"

    def support_numeric_in_quote(self) -> bool:
        """
        Does JDBC datasource support numeric in quote. e.g. where id > '5'
        :return: True if it supports otherwise False
        """
        return True

    def uses_sql_syntax(self) -> bool:
        """
        Does this dialect use standard SQL syntax?
        :return: True for SQL-based databases, False for others (e.g., Cypher)
        """
        return True

    def get_schema_inference_query(
        self, table: Optional[str], query: Optional[str]
    ) -> str:
        """
        Get a query that returns 0 rows for schema inference.
        :param table: Table name
        :param query: Query string
        :return: Query string for schema inference
        """
        if table is not None:
            return f"SELECT * FROM {table} WHERE 1=0"
        elif query is not None:
            return f"SELECT jdbc_query.* FROM ({query}) as jdbc_query WHERE 1=0"
        else:
            raise ValueError("table or query is not specified")

    def force_nullable_columns(self) -> bool:
        """
        Force all columns to be nullable (for schema-less databases).
        :return: True to force nullable, False to use metadata
        """
        return False

    def allow_unknown_types(self) -> bool:
        """
        Allow unknown JDBC types to default to StringType instead of raising an error.
        This is useful for schema-less databases (e.g., Neo4j) where types may not
        map cleanly to standard JDBC types.
        :return: True to allow unknown types, False to raise an error
        """
        return False

    def quote_column_names(self) -> bool:
        """
        Quote column names to preserve case-sensitivity.
        Snowflake uppercases unquoted identifiers, so quoting preserves original case.
        :return: True to quote column names, False to use as-is
        """
        return False

    def get_insert_statement(
        self, table: str, columns: list[str], placeholders: list[str]
    ) -> str:
        """
        Generate an INSERT statement for the dialect.
        :param table: Table name (or node label for graph DBs)
        :param columns: List of column names
        :param placeholders: List of placeholders (e.g., ['?', '?'])
        :return: INSERT statement
        """
        quoted_columns = ",".join([f'"{col}"' for col in columns])
        values = ",".join(placeholders)
        return f"INSERT INTO {table} ({quoted_columns}) VALUES ({values})"

    def get_create_table_statement(
        self, table: str, columns_with_types: list[tuple[str, str]]
    ) -> str:
        """
        Generate a CREATE TABLE statement for the dialect.
        :param table: Table name
        :param columns_with_types: List of (column_name, sql_type) tuples
        :return: CREATE TABLE statement
        """
        columns_str = ",".join(
            [f'"{col}" {sql_type}' for col, sql_type in columns_with_types]
        )
        return f"CREATE TABLE {table} ({columns_str})"

    def get_drop_table_statement(self, table: str) -> str:
        """
        Generate a DROP TABLE statement for the dialect.
        :param table: Table name
        :return: DROP TABLE statement
        """
        return f"DROP TABLE {table}"

    def get_table_exists_query(self, table: str) -> str:
        """
        Generate a query to check if a table exists.
        :param table: Table name
        :return: Query string
        """
        return f"SELECT 1 FROM {table} WHERE 1=0"

    def resolve_query(
        self, conn: "Connection", jdbc_options: dict[str, str]
    ) -> Optional[str]:
        """
        Resolve a query from options if needed (e.g., by discovering schema).
        Override in dialects that need special query resolution.

        :param conn: Active database connection
        :param jdbc_options: JDBC options dictionary (may contain dialect-specific markers)
        :return: Resolved query string, or None if no resolution needed
        """
        return None

    def set_fetch_size_on_cursor(self, cursor: Any, fetch_size: int) -> bool:
        """
        Set fetch size hint on the JDBC cursor/statement if supported.
        This provides a hint to JDBC drivers for optimal data transfer and memory usage.
        Some JDBC drivers use this internally to control how many rows are fetched
        from the database server in a single network round-trip.

        :param cursor: The database cursor (jdbc_utils.Cursor)
        :param fetch_size: Number of rows to fetch per network round-trip
        :return: True if fetch size was successfully set, False otherwise
        """
        if fetch_size <= 0:
            return False

        try:
            # For jdbc_utils, the cursor wraps a Java Statement
            # Try to access the underlying Statement and set fetch size
            if hasattr(cursor, "_jdbc_stmt") and cursor._jdbc_stmt is not None:
                # jdbc_utils Cursor - access the underlying JDBC Statement
                cursor._jdbc_stmt.setFetchSize(fetch_size)
                logger.debug(f"Set fetch size {fetch_size} on Statement")
                return True
        except Exception as e:
            logger.debug(f"Could not set JDBC fetch size to {fetch_size}: {e}")

        # Also try to set cursor arraysize as a Python-level hint
        try:
            cursor.arraysize = fetch_size
            logger.debug(f"Set cursor arraysize to {fetch_size}")
            return True
        except Exception as e:
            logger.debug(f"Could not set cursor arraysize to {fetch_size}: {e}")

        return False


# We will derive it from DataFrameReader of Snowpark once they merge and we refactor
# the code to reuse as much from Snowpark.
class JdbcDataFrameReader(DataFrameReader):
    """
    Derived Snowflake DataFrameReader class, so we cna reuse methods.
    This class read data from a JDBC datasource and creates Snowpark Dataframe.
    """

    def __init__(
        self,
        session: "snowflake.snowpark.session.Session",
        jdbc_options: dict[str, str],
    ) -> None:
        super().__init__(session)
        self.session = session
        self.jdbc_options = jdbc_options
        register_all_supported_jdbc_dialect()

    def jdbc_read_dbapi(
        self,
        create_connection: Callable[[dict[str, str]], "Connection"],
        close_connection: Callable[[Connection], None],
        table: Optional[str] = None,
        query: Optional[str] = None,
        *,
        column: Optional[str] = None,
        lower_bound: Optional[Union[str, int]] = None,
        upper_bound: Optional[Union[str, int]] = None,
        num_partitions: Optional[int] = None,
        max_workers: Optional[int] = None,
        query_timeout: Optional[int] = 0,
        fetch_size: Optional[int] = 0,
        predicates: Optional[List[str]] = None,
    ) -> DataFrame:

        """
        Read a table from JDBC datasource.
        If user provided column info then read in parallel using threadpool.

        Read rows using query provided. Execute this query against the JDBC Datasource to get rows.
        table name and query are mutually execlusive options. Both can't be used at the same time.
        Query option won't read in parallel as column parameters won't allowed.
        If column is specified then predicates will be ignored.

        Args:
            fetch_size: The number of rows to fetch per batch from the JDBC datasource.
                       If 0 (default), all rows are fetched at once using fetchall().
                       If > 0, rows are fetched in batches using fetchmany(fetch_size),
                       and each batch is written to a separate parquet file.
                       This can improve performance for large datasets by reducing memory usage.
                       Note: The JDBC driver's Statement.setFetchSize() is also set to this value
                       if supported by the driver, which can provide hints to the database for
                       optimal data transfer.
        """
        url = self.jdbc_options.get("url", None)
        jdbc_dialect = get_jdbc_dialect(url)
        conn = None
        try:
            conn = create_connection(self.jdbc_options)

            # this is specified to pyodbc, need other way to manage timeout on other drivers
            conn.timeout = query_timeout

            # Resolve query if dialect needs to discover schema (e.g., Neo4j labels/relationships)
            resolved_query = jdbc_dialect.resolve_query(conn, self.jdbc_options)
            if resolved_query is not None:
                query = resolved_query

            struct_schema, raw_schema = self._infer_data_source_schema(
                conn, table, query, jdbc_dialect
            )

            if column is None:
                if (
                    lower_bound is not None
                    or upper_bound is not None
                    or num_partitions is not None
                ):
                    exception = ValueError(
                        "when column is not specified, lower_bound, upper_bound, num_partitions are expected to be None"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                if table is not None:
                    partitioned_queries = []
                    table_query = f"SELECT * FROM {table}"
                    if predicates is not None and len(predicates) > 0:
                        where_clause = " AND ".join(predicates)
                        table_query += f" WHERE {where_clause}"
                    partitioned_queries.append(table_query)
                elif query is not None:
                    partitioned_queries = [query]
                else:
                    exception = ValueError("table or query is not specified")
                    attach_custom_error_code(exception, ErrorCodes.INSUFFICIENT_INPUT)
                    raise exception
            else:
                if lower_bound is None or upper_bound is None or num_partitions is None:
                    exception = ValueError(
                        "when column is specified, lower_bound, upper_bound, num_partitions must be specified"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                column_type = None
                for field in struct_schema.fields:
                    if field.name.lower() == column.lower():
                        column_type = field.datatype
                if column_type is None:
                    exception = ValueError("Column does not exist")
                    attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                    raise exception

                if not isinstance(column_type, _NumericType) and not isinstance(
                    column_type, DateType
                ):
                    exception = ValueError(f"unsupported type {column_type}")
                    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
                    raise exception
                spark_column_name = f'"{column}"'
                partitioned_queries = self._generate_partition(
                    table,
                    column_type,
                    jdbc_dialect,
                    spark_column_name,
                    lower_bound,
                    upper_bound,
                    num_partitions,
                )

                # When using partitioned reads, disable fetch_size batching to avoid
                # potential deadlocks between partition threads and upload threads.
                # Each partition will fetch all its data at once.
                if len(partitioned_queries) > 1 and fetch_size > 0:
                    logger.debug(
                        f"Disabling fetch_size ({fetch_size}) for partitioned read "
                        f"with {len(partitioned_queries)} partitions"
                    )
                    fetch_size = 0

            with tempfile.TemporaryDirectory() as tmp_dir:
                # TODO: Creating temp table and temp stage can be done in parallel, and
                # could be done earlier.

                # create temp table
                snowflake_table_type = "temporary"
                snowflake_table_name = random_name_for_temp_object(TempObjectType.TABLE)
                self.session.create_dataframe(
                    data=[], schema=struct_schema
                ).write.save_as_table(
                    snowflake_table_name, table_type=snowflake_table_type
                )
                res_df = self.table(snowflake_table_name)

                # create temp stage
                snowflake_stage_name = random_name_for_temp_object(TempObjectType.STAGE)
                sql_create_temp_stage = f"create {get_temp_type_for_object(self.session._use_scoped_temp_objects, True)} stage if not exists {snowflake_stage_name}"
                self.session._run_query(
                    sql_create_temp_stage, is_ddl_on_temp_object=True
                )

                # TODO: Set max workers depending on local resources
                # TODO: Use a thread pool executor that uses ordered or priority queue.
                # It is likely (but not guaranteed) that the first partitions have more rows
                # than later partitions.

                # Thread-safe list to collect upload futures from fetch threads
                upload_futures_lock = threading.Lock()
                upload_thread_pool_futures = []
                error_event = threading.Event()

                with ThreadPoolExecutor(
                    max_workers=max_workers
                ) as query_thread_executor, ThreadPoolExecutor(
                    max_workers=max_workers
                ) as upload_thread_executor:

                    def fetch_and_submit_uploads(
                        partition_index: int,
                        partition_query: str,
                    ):
                        """
                        Fetch data in batches and submit upload tasks immediately.
                        This enables parallel fetch and upload - while one batch uploads,
                        the next batch is being fetched.
                        """
                        for path in _task_fetch_from_data_source_generator(
                            create_connection,
                            self.jdbc_options,
                            close_connection,
                            partition_query,
                            raw_schema,
                            partition_index,
                            tmp_dir,
                            query_timeout,
                            fetch_size,
                        ):
                            if error_event.is_set():
                                # Stop if an error occurred elsewhere
                                break
                            if path:
                                # Submit upload task immediately to upload thread pool
                                future = upload_thread_executor.submit(
                                    self._upload_and_copy_into_table,
                                    path,
                                    snowflake_stage_name,
                                    snowflake_table_name,
                                    "abort_statement",
                                )
                                with upload_futures_lock:
                                    upload_thread_pool_futures.append(future)

                    # Start fetch threads for each partition
                    query_thread_pool_futures = [
                        query_thread_executor.submit(
                            fetch_and_submit_uploads,
                            query_index,
                            query,
                        )
                        for query_index, query in enumerate(partitioned_queries)
                    ]

                    # Wait for all fetch tasks to complete
                    for future in as_completed(query_thread_pool_futures):
                        if isinstance(future.result(), Exception):
                            logger.debug(
                                "fetch from data source failed, canceling all running tasks"
                            )
                            error_event.set()
                            query_thread_executor.shutdown(wait=False)
                            upload_thread_executor.shutdown(wait=False)
                            exception = future.result()
                            attach_custom_error_code(
                                exception, ErrorCodes.INTERNAL_ERROR
                            )
                            raise exception
                        try:
                            future.result()  # This will raise if there was an error
                        except Exception as e:
                            logger.debug(
                                "fetch from data source failed, canceling all running tasks"
                            )
                            error_event.set()
                            query_thread_executor.shutdown(wait=False)
                            upload_thread_executor.shutdown(wait=False)
                            attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
                            raise e

                    # Wait for all uploads to complete
                    completed_futures = wait(
                        upload_thread_pool_futures, return_when=ALL_COMPLETED
                    )
                    for f in completed_futures.done:
                        if f.result() is not None and isinstance(f.result(), Exception):
                            logger.debug(
                                "upload and copy into table failed, canceling all running tasks"
                            )
                            query_thread_executor.shutdown(wait=False)
                            upload_thread_executor.shutdown(wait=False)
                            exception = f.result()
                            attach_custom_error_code(
                                exception, ErrorCodes.INTERNAL_ERROR
                            )
                            raise exception
        finally:
            close_connection(conn)

        return res_df

    def _infer_data_source_schema(
        self,
        conn: Connection,
        table: Optional[str] = None,
        query: Optional[str] = None,
        jdbc_dialect: Optional[JdbcDialect] = None,
    ) -> tuple[StructType, tuple[tuple[str, Any, int, int, int, int, bool]]]:
        if jdbc_dialect is None:
            jdbc_dialect = JdbcDialect("default")

        try:
            sql = jdbc_dialect.get_schema_inference_query(table, query)
        except ValueError:
            exception = ValueError("table or query is not specified")
            attach_custom_error_code(exception, ErrorCodes.INSUFFICIENT_INPUT)
            raise exception

        cursor = conn.cursor()
        cursor.execute(sql)
        raw_schema = cursor.description
        rc = self._to_snowpark_type(raw_schema, jdbc_dialect), raw_schema
        cursor.close()
        return rc

    # this function is only used in data source API for SQL server
    def _to_internal_value(self, value: Union[int, str, float], column_type: DataType):
        if isinstance(column_type, _NumericType):
            return int(value)
        elif isinstance(column_type, (TimestampType, DateType)):
            # TODO: SNOW-1909315: support timezone
            dt = parser.parse(value)
            return int(dt.replace(tzinfo=pytz.UTC).timestamp())
        else:
            exception = TypeError(
                f"unsupported column type for partition: {column_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
            raise exception

    # this function is only used in data source API for SQL server
    def _to_external_value(self, value: Union[int, str, float], column_type: DataType):
        if isinstance(column_type, _NumericType):
            return value
        elif isinstance(column_type, (TimestampType, DateType)):
            # TODO: SNOW-1909315: support timezone
            return datetime.datetime.fromtimestamp(value, tz=pytz.UTC)
        else:
            exception = TypeError(
                f"unsupported column type for partition: {column_type}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
            raise exception

    def validate_numeric_precision_scale(
        self, precision: Optional[int], scale: Optional[int]
    ) -> bool:
        if precision is not None:
            if not (0 <= precision <= 38):
                return False
            if scale is not None and not (0 <= scale <= precision):
                return False
        elif scale is not None:
            return False
        return True

    def _to_snowpark_type(
        self, schema: Tuple[tuple], jdbc_dialect: Optional[JdbcDialect] = None
    ) -> StructType:
        fields = []
        for column in schema:
            name, dbapi_type, size, _, precision, scale, is_nullable = column

            # Quote the column name to preserve case-sensitivity if dialect requires it
            # Snowflake uppercases unquoted identifiers, so quoting preserves original case
            if jdbc_dialect and jdbc_dialect.quote_column_names():
                column_name = f'"{name}"'
            else:
                column_name = name

            # Force nullable if dialect requires it (e.g., Neo4j is schema-less)
            if jdbc_dialect and jdbc_dialect.force_nullable_columns():
                is_nullable = True

            match dbapi_type:
                case jdbc_utils.NUMBER:
                    field = StructField(column_name, IntegerType(), is_nullable)
                case jdbc_utils.FLOAT:
                    field = StructField(column_name, FloatType(), is_nullable)
                case jdbc_utils.DECIMAL:
                    precision, scale = int(precision), int(scale)
                    if not self.validate_numeric_precision_scale(precision, scale):
                        precision, scale = None, None

                    field = StructField(
                        column_name,
                        DecimalType(
                            precision if precision is not None else 38,
                            scale if scale is not None else 0,
                        ),
                        is_nullable,
                    )
                case jdbc_utils.STRING:
                    field = StructField(column_name, StringType(), is_nullable)
                case jdbc_utils.DATE:
                    field = StructField(column_name, DateType(), is_nullable)
                case jdbc_utils.TIME:
                    # Snowpark doesn't support TimeType for table creation,
                    # so we store TIME values as strings
                    field = StructField(column_name, StringType(), is_nullable)
                case jdbc_utils.DATETIME:
                    field = StructField(column_name, TimestampType(), is_nullable)
                case jdbc_utils.BINARY:
                    field = StructField(column_name, BinaryType(), is_nullable)
                case _:
                    if jdbc_dialect and jdbc_dialect.allow_unknown_types():
                        # Schema-less databases like Neo4j may have non-standard types
                        logger.warning(
                            f"Unknown JDBC type for column '{name}', defaulting to StringType"
                        )
                        field = StructField(column_name, StringType(), is_nullable)
                    else:
                        exception = TypeError(
                            f"Unsupported JDBC type '{dbapi_type}' for column '{name}'"
                        )
                        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
                        raise exception

            fields.append(field)
        return StructType(fields)

    def _generate_partition(
        self,
        table: str,
        column_type: DataType,
        jdbc_dialect: JdbcDialect,
        column: Optional[str] = None,
        lower_bound: Optional[Union[str, int]] = None,
        upper_bound: Optional[Union[str, int]] = None,
        num_partitions: Optional[int] = None,
    ) -> List[str]:
        select_query = f"SELECT * FROM {table}"

        processed_lower_bound = self._to_internal_value(lower_bound, column_type)
        processed_upper_bound = self._to_internal_value(upper_bound, column_type)
        if processed_lower_bound > processed_upper_bound:
            exception = ValueError("lower_bound cannot be greater than upper_bound")
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception

        if processed_lower_bound == processed_upper_bound or num_partitions <= 1:
            return [select_query]

        if (processed_upper_bound - processed_lower_bound) >= num_partitions or (
            processed_upper_bound - processed_lower_bound
        ) < 0:
            actual_num_partitions = num_partitions
        else:
            actual_num_partitions = processed_upper_bound - processed_lower_bound
            logger.warning(
                "The number of partitions is reduced because the specified number of partitions is less than the difference between upper bound and lower bound."
            )

        # decide stride length
        upper_stride = (
            processed_upper_bound / decimal.Decimal(actual_num_partitions)
        ).quantize(decimal.Decimal("1e-18"), rounding=ROUND_HALF_EVEN)
        lower_stride = (
            processed_lower_bound / decimal.Decimal(actual_num_partitions)
        ).quantize(decimal.Decimal("1e-18"), rounding=ROUND_HALF_EVEN)
        preciseStride = upper_stride - lower_stride
        stride = int(preciseStride)

        lost_num_of_strides = (
            (preciseStride - decimal.Decimal(stride))
            * decimal.Decimal(actual_num_partitions)
            / decimal.Decimal(stride)
        )
        lower_bound_with_stride_alignment = processed_lower_bound + int(
            (lost_num_of_strides / 2 * decimal.Decimal(stride)).quantize(
                decimal.Decimal("1"), rounding=ROUND_HALF_UP
            )
        )

        current_value = lower_bound_with_stride_alignment
        numeric_in_quote = jdbc_dialect.support_numeric_in_quote()
        if isinstance(column_type, _NumericType) and not numeric_in_quote:
            single_quote = ""
        else:
            single_quote = "'"

        partition_queries = []
        for i in range(actual_num_partitions):
            l_bound = (
                f"{column} >= {single_quote}{self._to_external_value(current_value, column_type)}{single_quote}"
                if i != 0
                else ""
            )
            current_value += stride
            u_bound = (
                f"{column} < {single_quote}{self._to_external_value(current_value, column_type)}{single_quote}"
                if i != actual_num_partitions - 1
                else ""
            )

            if u_bound == "":
                where_clause = l_bound
            elif l_bound == "":
                where_clause = f"{u_bound} OR {column} is null"
            else:
                where_clause = f"{l_bound} AND {u_bound}"

            partition_queries.append(select_query + f" WHERE {where_clause}")

        return partition_queries

    @exponential_backoff
    def _upload_and_copy_into_table(
        self,
        local_file: str,
        snowflake_stage_name: str,
        snowflake_table_name: Optional[str] = None,
        on_error: Optional[str] = "abort_statement",
        statements_params: Optional[Dict[str, str]] = None,
    ):
        file_name = os.path.basename(local_file)
        self._session.file.put(
            normalize_local_file(local_file),
            f"{snowflake_stage_name}",
            overwrite=True,
            statement_params=statements_params,
        )

        copy_into_table_query = f"""
        COPY INTO {snowflake_table_name} FROM @{snowflake_stage_name}/{file_name}
        FILE_FORMAT = (TYPE = PARQUET USE_VECTORIZED_SCANNER=TRUE)
        MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
        PURGE=TRUE
        ON_ERROR={on_error}
        {DATA_SOURCE_SQL_COMMENT}
        """
        self._session.sql(copy_into_table_query).collect(
            statement_params=statements_params
        )


def _task_fetch_from_data_source_generator(
    create_connection: Callable[[dict[str, str]], "Connection"],
    jdbc_options: dict[str, str],
    close_connection: Callable[[Connection], None],
    query: str,
    schema: tuple[tuple[str, Any, int, int, int, int, bool]],
    partitioned_query_index: int,
    tmp_dir: str,
    query_timeout: int = 0,
    fetch_size: int = 0,
) -> Generator[str, None, None]:
    """
    Generator that fetches data from a JDBC datasource and yields file paths as batches complete.

    This generator enables parallel reading and uploading by yielding each file path
    immediately after the batch is written, allowing the caller to start uploading
    while fetching continues.

    Args:
        create_connection: Factory function to create a JDBC connection
        jdbc_options: JDBC connection options
        close_connection: Function to close the JDBC connection
        query: SQL query to execute
        schema: Schema tuple describing the result columns
        partitioned_query_index: Index of this partition (for file naming)
        tmp_dir: Temporary directory to write parquet files
        query_timeout: Query timeout in seconds (0 = no timeout)
        fetch_size: Number of rows to fetch per batch.
                   If 0, all rows are fetched at once using fetchall().
                   If > 0, rows are fetched in batches using fetchmany(fetch_size),
                   and each batch file path is yielded immediately after writing.

    Yields:
        File paths as they are written, enabling parallel upload while fetch continues.
    """
    conn = None
    try:
        logger.debug(f"Partition {partitioned_query_index}: starting fetch generator")

        # Ensure dialects are registered (needed since this runs in a worker thread)
        register_all_supported_jdbc_dialect()
        logger.debug(f"Partition {partitioned_query_index}: dialects registered")

        # TODO: This should use connection pooling.
        logger.debug(
            f"Partition {partitioned_query_index}: creating JDBC connection..."
        )
        conn = create_connection(jdbc_options)
        logger.debug(f"Partition {partitioned_query_index}: JDBC connection created")

        # this is specified to pyodbc, need other way to manage timeout on other drivers
        conn.timeout = query_timeout
        cursor = conn.cursor()

        # Note: We intentionally do NOT set JDBC Statement.setFetchSize() here.
        # When using Python's cursor.fetchmany() for batched reading, setting
        # JDBC's setFetchSize() can cause hangs on Linux with certain JDBC drivers
        # (e.g., Oracle) due to conflicts between JDBC's internal buffering and
        # Python's fetchmany() behavior. Python's fetchmany() alone is sufficient
        # to control batch sizes for memory optimization.

        logger.debug(f"Partition {partitioned_query_index}: executing query...")
        cursor.execute(query)
        logger.debug(f"Partition {partitioned_query_index}: query executed")

        columns = [col[0] for col in schema]

        if fetch_size == 0:
            # Original behavior: fetch all rows at once
            result = cursor.fetchall()

            # We will only go through with writing an empty file for the first partition.
            # Otherwise, yield nothing to indicate there is no data.
            if not result and partitioned_query_index != 0:
                logger.info(f"Query gave no results {query}")
                cursor.close()
                return

            df = pd.DataFrame.from_records(result, columns=columns)
            path = os.path.join(tmp_dir, f"data_{partitioned_query_index}.parquet")
            df.to_parquet(path)
            cursor.close()
            yield path
        else:
            # Batched reading: fetch rows in chunks and yield file paths immediately
            batch_index = 0
            has_data = False

            while True:
                logger.debug(
                    f"Partition {partitioned_query_index}: fetching batch {batch_index}..."
                )
                rows = cursor.fetchmany(fetch_size)
                logger.debug(
                    f"Partition {partitioned_query_index}: fetched {len(rows) if rows else 0} rows"
                )

                if not rows:
                    # No more data
                    break

                has_data = True
                df = pd.DataFrame.from_records(rows, columns=columns)
                # Create unique file name with partition index and batch number
                path = os.path.join(
                    tmp_dir,
                    f"data_{partitioned_query_index}_batch_{batch_index}.parquet",
                )
                logger.debug(
                    f"Partition {partitioned_query_index}: writing batch {batch_index} to parquet..."
                )
                df.to_parquet(path)
                logger.debug(
                    f"Partition {partitioned_query_index}: wrote batch {batch_index} "
                    f"with {len(rows)} rows to {path}"
                )
                batch_index += 1
                # Yield immediately so upload can start while we fetch the next batch
                logger.debug(
                    f"Partition {partitioned_query_index}: yielding batch {batch_index - 1}"
                )
                yield path

            logger.debug(
                f"Partition {partitioned_query_index}: closing cursor after {batch_index} batches"
            )
            cursor.close()

            # If no data and not the first partition, don't yield anything
            if not has_data and partitioned_query_index != 0:
                logger.info(f"Query gave no results {query}")
                return

            # If no data but first partition, create an empty file
            if not has_data:
                df = pd.DataFrame(columns=columns)
                path = os.path.join(
                    tmp_dir, f"data_{partitioned_query_index}_batch_0.parquet"
                )
                df.to_parquet(path)
                yield path

            logger.info(
                f"Partition {partitioned_query_index}: completed with {batch_index} batches"
            )
    finally:
        close_connection(conn)


@exponential_backoff
def _task_fetch_from_data_source(
    create_connection: Callable[[dict[str, str]], "Connection"],
    jdbc_options: dict[str, str],
    close_connection: Callable[[Connection], None],
    query: str,
    schema: tuple[tuple[str, Any, int, int, int, int, bool]],
    partitioned_query_index: int,
    tmp_dir: str,
    query_timeout: int = 0,
    fetch_size: int = 0,
) -> Union[str, List[str]]:
    """
    Fetch data from a JDBC datasource and write to parquet file(s).
    This is a wrapper around the generator for backward compatibility.

    Args:
        create_connection: Factory function to create a JDBC connection
        jdbc_options: JDBC connection options
        close_connection: Function to close the JDBC connection
        query: SQL query to execute
        schema: Schema tuple describing the result columns
        partitioned_query_index: Index of this partition (for file naming)
        tmp_dir: Temporary directory to write parquet files
        query_timeout: Query timeout in seconds (0 = no timeout)
        fetch_size: Number of rows to fetch per batch.
                   If 0, all rows are fetched at once using fetchall().
                   If > 0, rows are fetched in batches using fetchmany(fetch_size),
                   and each batch is written to a separate parquet file.

    Returns:
        If fetch_size == 0: A single file path string, or "" if no data.
        If fetch_size > 0: A list of file paths, or [] if no data.
    """
    paths = list(
        _task_fetch_from_data_source_generator(
            create_connection,
            jdbc_options,
            close_connection,
            query,
            schema,
            partitioned_query_index,
            tmp_dir,
            query_timeout,
            fetch_size,
        )
    )

    if fetch_size == 0:
        return paths[0] if paths else ""
    else:
        return paths


# Hold all registered JDBC Dialects
jdbc_dialects: List["JdbcDialect"] = []
_jdbc_dialects_lock = threading.Lock()


class SnowflakeJdbcDialect(JdbcDialect):
    """
    For internal testing uses Snowflake JDBC Driver.
    Defines Snowflake capability.
    """

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: True if URL is for Snowflake JDBC driver otherwise False.
        """
        return url.lower().startswith("jdbc:snowflake:")

    def get_max_varchar_length(self) -> int:
        """
        Get the maximum size of the VARCHAR datatype supported.
        :return: max varchar size
        """
        return 16 * 1024 * 1024

    def get_double_type_name(self) -> str:
        """
        Get the DOUBLE type string name.
        :return: String name of DOUBLE datatype
        """
        return "DOUBLE"


class SqlserverJdbcDialect(JdbcDialect):
    """
    Defines SQL Server specific capability.
    """

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: True if URL is for SQL Server JDBC driver otherwise False.
        """
        return url.lower().startswith("jdbc:sqlserver:")

    def get_max_varchar_length(self) -> int:
        """
        Get the maximum size of the VARCHAR datatype supported.
        :return: max varchar size
        """
        return 8000

    def get_double_type_name(self) -> str:
        """
        Get the DOUBLE type string name.
        :return: String name of DOUBLE datatype
        """
        return "REAL"


class DerbyJdbcDialect(JdbcDialect):
    """
    Defines Derby specific capability.
    Derby is used by Spark Datasource tests
    """

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: True if URL is for SQL Server JDBC driver otherwise False.
        """
        return url.lower().startswith("jdbc:derby:")

    def support_numeric_in_quote(self) -> bool:
        """
        Does JDBC datasource support numeric in quote. e.g. where id > '5'
        :return: True if it supports otherwise False
        """
        return False


class PostgresqlJdbcDialect(JdbcDialect):
    """
    Defines Postgresql specific capability.
    """

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: True if URL is for Postgresql JDBC driver otherwise False.
        """
        return url.lower().startswith("jdbc:postgresql:")

    def get_max_varchar_length(self) -> int:
        """
        Get the maximum size of the VARCHAR datatype supported.
        :return: max varchar size
        """
        return 10485760

    def get_double_type_name(self) -> str:
        """
        Get the DOUBLE type string name.
        :return: String name of DOUBLE datatype
        """
        return "DOUBLE PRECISION"


class MySqlJdbcDialect(JdbcDialect):
    """
    Defines MySQL specific capability.
    """

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: True if URL is for MySQL JDBC driver otherwise False.
        """
        return url.lower().startswith("jdbc:mysql:")

    def get_max_varchar_length(self) -> int:
        """
        Get the maximum size of the VARCHAR datatype supported.
        :return: max varchar size
        """
        return 4000

    def get_double_type_name(self) -> str:
        """
        Get the DOUBLE type string name.
        :return: String name of DOUBLE datatype
        """
        return "DOUBLE"


class Neo4jJdbcDialect(JdbcDialect):
    """
    Defines Neo4j specific capability using Cypher query language.
    """

    def can_handle(self, url: str) -> bool:
        """
        Can this dialect handle the provided JDBC URL?
        :param url: JDBC URL
        :return: True if URL is for Neo4j JDBC driver otherwise False.
        """
        # Match all Neo4j JDBC URL variants: jdbc:neo4j://, jdbc:neo4j+s://, jdbc:neo4j+ssc://
        url_lower = url.lower()
        return url_lower.startswith("jdbc:neo4j:") or url_lower.startswith(
            "jdbc:neo4j+"
        )

    def uses_sql_syntax(self) -> bool:
        """
        Neo4j uses Cypher, not SQL.
        :return: False
        """
        return False

    def get_schema_inference_query(
        self, table: Optional[str], query: Optional[str]
    ) -> str:
        """
        Get a Cypher query that returns 0 rows for schema inference.
        :param table: Node label (for Neo4j, "table" maps to labels)
        :param query: Cypher query string
        :return: Cypher query string for schema inference
        """
        import re

        if query is not None:
            # Remove any existing LIMIT clause and add LIMIT 0
            # Strip whitespace first to handle trailing newlines/spaces
            query_stripped = query.strip()
            query_no_limit = re.sub(
                r"\s+LIMIT\s+\d+\s*$", "", query_stripped, flags=re.IGNORECASE
            )
            return f"{query_no_limit} LIMIT 0"
        elif table is not None:
            # For Neo4j, "table" maps to labels and can be a label chain.
            labels = validate_and_normalize_neo4j_labels(table)
            return f"MATCH (n:{labels}) RETURN n LIMIT 0"
        else:
            raise ValueError("table or query is not specified")

    def force_nullable_columns(self) -> bool:
        """
        Neo4j is schema-less, so all columns should be nullable.
        :return: True
        """
        return True

    def allow_unknown_types(self) -> bool:
        """
        Neo4j may return JAVA_OBJECT or other non-standard JDBC types.
        Allow these to default to StringType.
        :return: True
        """
        return True

    def quote_column_names(self) -> bool:
        """
        Quote column names to preserve case-sensitivity from Neo4j.
        :return: True
        """
        return True

    def get_insert_statement(
        self, table: str, columns: list[str], placeholders: list[str]
    ) -> str:
        """
        Generate a Cypher CREATE statement for Neo4j.
        :param table: Node label
        :param columns: List of property names
        :param placeholders: List of placeholders (e.g., ['?', '?'])
        :return: Cypher CREATE statement
        """
        # Validate labels and property names to prevent Cypher injection.
        labels = validate_and_normalize_neo4j_labels(table)
        for col in columns:
            validate_cypher_identifier(col, "property name")

        # Build property map: {prop1: ?, prop2: ?, ...}
        props = ", ".join([f"{col}: ?" for col in columns])
        return f"CREATE (n:{labels} {{{props}}})"

    def get_create_table_statement(
        self, table: str, columns_with_types: list[tuple[str, str]]
    ) -> str:
        """
        Neo4j is schema-less, no CREATE TABLE needed.
        Return a no-op query.
        :param table: Node label
        :param columns_with_types: Ignored for Neo4j
        :return: No-op Cypher query
        """
        # Neo4j doesn't require table creation - nodes are created on insert
        # Return a simple query that does nothing
        return "RETURN 1"

    def get_drop_table_statement(self, table: str) -> str:
        """
        Generate a Cypher statement to delete all nodes with a label.
        :param table: Node label
        :return: Cypher DELETE statement
        """
        labels = validate_and_normalize_neo4j_labels(table)
        return f"MATCH (n:{labels}) DETACH DELETE n"

    def get_table_exists_query(self, table: str) -> str:
        """
        Generate a Cypher query to check if nodes with a label exist.
        :param table: Node label
        :return: Cypher query
        """
        labels = validate_and_normalize_neo4j_labels(table)
        return f"MATCH (n:{labels}) RETURN n LIMIT 0"

    def resolve_query(
        self, conn: "Connection", jdbc_options: dict[str, str]
    ) -> Optional[str]:
        """
        Resolve Neo4j query by discovering properties for labels/relationships.

        :param conn: Active database connection
        :param jdbc_options: JDBC options with labels or relationship options
        :return: Resolved Cypher query, or None if no resolution needed
        """
        if "labels" in jdbc_options:
            label = jdbc_options["labels"]
            properties = self._discover_node_properties(conn, label)
            logger.info(f"Discovered properties for label '{label}': {properties}")
            return self._build_node_query(label, properties)
        elif "relationship" in jdbc_options:
            rel_type = jdbc_options["relationship"]
            properties = self._discover_relationship_properties(conn, rel_type)
            logger.info(
                f"Discovered properties for relationship '{rel_type}': {properties}"
            )
            return self._build_relationship_query(rel_type, properties)
        return None

    def _discover_node_properties(self, conn: "Connection", label: str) -> list[str]:
        """
        Discover property keys for a node label using an existing connection.
        """
        labels = validate_and_normalize_neo4j_labels(label)
        discover_query = f"MATCH (n:{labels}) RETURN keys(n) AS props LIMIT 1"

        try:
            cursor = conn.cursor()
            cursor.execute(discover_query)
            row = cursor.fetchone()
            cursor.close()

            if row and row[0]:
                props = row[0]
                if hasattr(props, "__iter__") and not isinstance(props, str):
                    return list(props)
                return []
            return []
        except Exception as e:
            logger.warning(f"Failed to discover properties for label '{labels}': {e}")
            return []

    def _discover_relationship_properties(
        self, conn: "Connection", rel_type: str
    ) -> list[str]:
        """
        Discover property keys for a relationship type using an existing connection.
        """
        validate_cypher_identifier(rel_type, "relationship type")
        discover_query = f"MATCH ()-[r:{rel_type}]->() RETURN keys(r) AS props LIMIT 1"

        try:
            cursor = conn.cursor()
            cursor.execute(discover_query)
            row = cursor.fetchone()
            cursor.close()

            if row and row[0]:
                props = row[0]
                if hasattr(props, "__iter__") and not isinstance(props, str):
                    return list(props)
                return []
            return []
        except Exception as e:
            logger.warning(
                f"Failed to discover properties for relationship '{rel_type}': {e}"
            )
            return []

    def _build_node_query(self, label: str, properties: list[str]) -> str:
        """Build a Cypher query that returns node properties as columns."""
        labels = validate_and_normalize_neo4j_labels(label)
        for prop in properties:
            validate_cypher_identifier(prop, "property name")

        if not properties:
            return f"MATCH (n:{labels}) RETURN elementId(n) AS _id"

        return_parts = [f"n.{prop} AS {prop}" for prop in properties]
        return f"MATCH (n:{labels}) RETURN {', '.join(return_parts)}"

    def _build_relationship_query(self, rel_type: str, properties: list[str]) -> str:
        """Build a Cypher query that returns relationship properties as columns."""
        validate_cypher_identifier(rel_type, "relationship type")
        for prop in properties:
            validate_cypher_identifier(prop, "property name")

        if not properties:
            return f"MATCH ()-[r:{rel_type}]->() RETURN elementId(r) AS _id, type(r) AS _type"

        return_parts = [f"r.{prop} AS {prop}" for prop in properties]
        return f"MATCH ()-[r:{rel_type}]->() RETURN {', '.join(return_parts)}"


def register_jdbc_dialect(dialect) -> None:
    """
    Register  a supported JDBC datasource
    :param dialect: Dialect class of a JDBC datasource
    """
    jdbc_dialects.append(dialect)


def register_all_supported_jdbc_dialect() -> None:
    """
    Register all supported JDBC datasources.
    Thread-safe: uses a lock to prevent race conditions when multiple
    partition threads call this simultaneously.
    """
    with _jdbc_dialects_lock:
        if len(jdbc_dialects) == 0:
            register_jdbc_dialect(DerbyJdbcDialect("derby"))
            register_jdbc_dialect(MySqlJdbcDialect("mysql"))
            register_jdbc_dialect(PostgresqlJdbcDialect("postgresql"))
            register_jdbc_dialect(SnowflakeJdbcDialect("snowflake"))
            register_jdbc_dialect(SqlserverJdbcDialect("sqlserver"))
            register_jdbc_dialect(Neo4jJdbcDialect("neo4j"))
            # Register this at last
            register_jdbc_dialect(JdbcDialect("default"))


def get_jdbc_dialect(url: str) -> JdbcDialect:
    """
    Get the JDBc Dialect class from the given JDBC URL
    :param url: JDBC URL of a driver
    :return: JDBC Dialect class
    """
    for jdbc_dialect in jdbc_dialects:
        if jdbc_dialect.can_handle(url):
            return jdbc_dialect
    exception = ValueError(f"Unsupported JDBC datasource: {url}")
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    raise exception
