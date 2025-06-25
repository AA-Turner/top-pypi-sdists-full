from __future__ import annotations

import concurrent.futures
import contextlib
import os
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, Union

import pyarrow as pa
import pyarrow.compute as pc

from chalk.clogging import chalk_logger
from chalk.features import Feature
from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.df_utils import pa_array_to_pl_series
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.threading import DEFAULT_IO_EXECUTOR
from chalk.utils.tracing import safe_incr, safe_trace

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL

_logger = get_logger(__name__)


_DATABRICKS_HOST_NAME = "DATABRICKS_HOST"
_DATABRICKS_HTTP_PATH_NAME = "DATABRICKS_HTTP_PATH"
_DATABRICKS_TOKEN_NAME = "DATABRICKS_TOKEN"
_DATABRICKS_DATABASE_NAME = "DATABRICKS_DATABASE"
_DATABRICKS_PORT_NAME = "DATABRICKS_PORT"


class DatabricksSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.databricks

    def __init__(
        self,
        host: Optional[str] = None,
        http_path: Optional[str] = None,
        access_token: Optional[str] = None,
        db: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        executor: Optional[concurrent.futures.ThreadPoolExecutor] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            from databricks import sql
        except ImportError:
            raise missing_dependency_exception("chalkpy[databricks]")
        del sql
        self.host = host or load_integration_variable(
            name=_DATABRICKS_HOST_NAME, integration_name=name, override=integration_variable_override
        )
        self.http_path = http_path or load_integration_variable(
            name=_DATABRICKS_HTTP_PATH_NAME, integration_name=name, override=integration_variable_override
        )
        self.access_token = access_token or load_integration_variable(
            name=_DATABRICKS_TOKEN_NAME, integration_name=name, override=integration_variable_override
        )
        self.db = db or load_integration_variable(
            name=_DATABRICKS_DATABASE_NAME, integration_name=name, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                name=_DATABRICKS_PORT_NAME, integration_name=name, parser=int, override=integration_variable_override
            )
        )
        self.executor = executor or DEFAULT_IO_EXECUTOR

        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    def supports_inefficient_fallback(self) -> bool:
        return False

    def get_sqlglot_dialect(self) -> str | None:
        return "databricks"

    @contextlib.contextmanager
    def _create_temp_table(
        self,
        create_temp_table: Any,
        temp_table: Any,
        drop_temp_table: Any,
        connection: Connection,
        temp_value: pa.Table,
    ):
        """Create temporary table with data for temp table pushdown"""

        chalk_logger.info(f"Creating temporary table {temp_table.name} in Databricks.")

        # Execute the CREATE TABLE statement
        connection.execute(create_temp_table)

        try:
            # Convert PyArrow table to pandas for insertion
            df = temp_value.to_pandas()

            # Insert data using pandas to_sql
            df.to_sql(name=str(temp_table.name), con=connection, if_exists="append", index=False, method="multi")

            yield
        finally:
            chalk_logger.info(f"Dropping temporary table {temp_table.name} in Databricks.")
            connection.execute(drop_temp_table)

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query using databricks-sql-python to fetch results as Arrow RecordBatches"""
        with safe_trace("databricks.execute_query_efficient"):
            try:
                from databricks import sql
            except ImportError:
                raise missing_dependency_exception("chalkpy[databricks]")

            # The sql connector v2.5.2 seems to only support pyformat paramstyle, according to the repo's test suite
            formatted_op, positional_params, named_params = self.compile_query(finalized_query, paramstyle="pyformat")
            if len(positional_params) != 0:
                raise ValueError("Databricks efficient query uses named parameters only")

            # Handle temp table pushdown using SQLAlchemy connection
            with (
                self.get_engine().connect() if connection is None else contextlib.nullcontext(connection)
            ) as sqlalchemy_cnx:
                with contextlib.ExitStack() as exit_stack:
                    for (
                        _,
                        temp_value,
                        create_temp_table,
                        temp_table,
                        drop_temp_table,
                    ) in finalized_query.temp_tables.values():
                        exit_stack.enter_context(
                            self._create_temp_table(
                                create_temp_table,
                                temp_table,
                                drop_temp_table,
                                sqlalchemy_cnx,
                                temp_value,
                            )
                        )

                    # Connect using databricks-sql-python for efficient Arrow fetching
                    with sql.connect(
                        server_hostname=self.host,
                        http_path=self.http_path,
                        access_token=self.access_token,
                        catalog=self.db,
                    ) as databricks_conn:
                        chalk_logger.info("Established connection with Databricks using databricks-sql-python")

                        with databricks_conn.cursor() as cursor:
                            chalk_logger.info(f"Executing query: {repr(formatted_op)}")

                            # Execute the query with named parameters
                            cursor.execute(formatted_op, parameters=named_params)

                            # Fetch results as Arrow tables in batches
                            batch_size = int(os.environ.get("CHALK_DATABRICKS_DOWNLOAD_BATCH_SIZE", "10000"))
                            while True:
                                try:
                                    # Fetch a batch of results as Arrow table
                                    arrow_table = cursor.fetchmany_arrow(size=batch_size)

                                    if arrow_table is None or len(arrow_table) == 0:
                                        break

                                    chalk_logger.info(f"Fetched Arrow table with {len(arrow_table)} rows")

                                    # Convert to features mapping and postprocess
                                    features = columns_to_features(arrow_table.schema.names)
                                    record_batch = self._postprocess_table(features, arrow_table)

                                    safe_incr("chalk.databricks.downloaded_bytes", arrow_table.nbytes or 0)
                                    safe_incr("chalk.databricks.downloaded_rows", arrow_table.num_rows or 0)

                                    yield record_batch

                                except Exception as e:
                                    if "no more data" in str(e).lower() or "end of result set" in str(e).lower():
                                        break
                                    raise

                            chalk_logger.info("Completed fetching all results from Databricks")

    def _postprocess_table(self, features: Mapping[str, Feature], tbl: pa.Table):
        """Post-process PyArrow table with type conversion and schema alignment"""
        columns: list[pa.Array] = []
        column_names: list[str] = []
        chalk_logger.info(
            f"Received a PyArrow table from Databricks with {len(tbl)} rows; {len(tbl.column_names)} columns; {tbl.nbytes=}; {tbl.schema=}"
        )

        for col_name, feature in features.items():
            try:
                column = tbl[col_name]
                expected_type = feature.converter.pyarrow_dtype
                actual_type = tbl.schema.field(col_name).type

                # Handle list/array types that may be returned as JSON strings
                if pa.types.is_list(expected_type) or pa.types.is_large_list(expected_type):
                    if pa.types.is_string(actual_type) or pa.types.is_large_string(actual_type):
                        series = pa_array_to_pl_series(tbl[col_name])
                        column = series.str.json_extract(feature.converter.polars_dtype).to_arrow().cast(expected_type)

                # Cast to expected type if needed
                if actual_type != expected_type:
                    column = column.cast(options=pc.CastOptions(target_type=expected_type, allow_time_truncate=True))

                # Ensure single chunk
                if isinstance(column, pa.ChunkedArray):
                    column = column.combine_chunks()

                columns.append(column)
                column_names.append(feature.root_fqn)
            except Exception:
                chalk_logger.error(f"Failed to deserialize column '{col_name}' into '{feature}'", exc_info=True)
                raise

        return pa.RecordBatch.from_arrays(arrays=columns, names=column_names)

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="databricks",
            username="token",
            password=self.access_token,
            host=self.host,
            port=self.port,
            database=self.db,
            query={"http_path": self.http_path or ""},
        )

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_DATABRICKS_HOST_NAME, self.name, self.host),
                create_integration_variable(_DATABRICKS_HTTP_PATH_NAME, self.name, self.http_path),
                create_integration_variable(_DATABRICKS_TOKEN_NAME, self.name, self.access_token),
                create_integration_variable(_DATABRICKS_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_DATABRICKS_PORT_NAME, self.name, self.port),
            ]
            if v is not None
        }
