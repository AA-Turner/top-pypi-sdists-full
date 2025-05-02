from __future__ import annotations

import contextlib
import functools
import queue
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Iterator, Mapping, Optional, Sequence, cast
from uuid import uuid4

import google
import pyarrow as pa

from chalk.clogging import chalk_logger
from chalk.features import Feature
from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, validate_dtypes_for_efficient_execution
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import google.cloud.bigquery
    import sqlalchemy
    from google.cloud.bigquery import ScalarQueryParameterType
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL
    from sqlalchemy.sql.ddl import CreateTable, DropTable


try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.BINARY,
        sa.BLOB,
        sa.LargeBinary,
        sa.Float,
        sa.Integer,
        sa.Time,
        sa.String,
        sa.Text,
        sa.VARBINARY,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )

_MAX_STATEMENT_LENGTH = 1024 * 1024
"""The actual maximum statement length that bigquery will accept. If the query is much longer than this, then we won't even
get a result from the server. This is likely because they refuse to process a request body this big!"""

_DEADLOCK_CIRCUMVENTING_TIMEOUT = 1
"""Used in a queue.put call to help circumvent a non-deterministic deadlock. See the function we're
using to monkeypatch the deadlocking BQ table download function for detailed explanation of the deadlock."""

_logger = get_logger(__name__)


@functools.lru_cache(maxsize=None)
def _determine_is_read_session_optional():
    # Used by monkeypatched BQ table download function.
    # If this variable fails to be resolved (remains as None)
    # then we will not monkeypatch the function.
    _is_read_session_optional = None
    try:
        import google.cloud.bigquery  # pyright: ignore[reportUnusedImport]
    except ModuleNotFoundError:
        # the user did not specify that they want to use the bigquery module
        pass
    else:
        try:
            from google.cloud.bigquery._versions_helpers import BQ_STORAGE_VERSIONS

            _is_read_session_optional = BQ_STORAGE_VERSIONS.is_read_session_optional
        except:
            try:
                # If customer's requirements.txt pins to some older version of bigquery
                from google.cloud.bigquery._helpers import (
                    BQ_STORAGE_VERSIONS,  # pyright: ignore[reportAttributeAccessIssue]
                )

                _is_read_session_optional = BQ_STORAGE_VERSIONS.is_read_session_optional
            except:
                # Failed to resolve the _is_read_session_optional variable.
                # We will evaluate the variable below and not monkeypatch
                # the BQ table download function.
                pass
    return _is_read_session_optional


def _download_table_bqstorage_stream_no_deadlock(
    download_state,  # pyright: ignore[reportMissingParameterType]
    bqstorage_client,  # pyright: ignore[reportMissingParameterType]
    session,  # pyright: ignore[reportMissingParameterType]
    stream,  # pyright: ignore[reportMissingParameterType]
    worker_queue,  # pyright: ignore[reportMissingParameterType]
    page_to_item,  # pyright: ignore[reportMissingParameterType]
):
    # Helps circumvent a non-deterministic deadlock. This deadlock could happen when:
    # 1. we are looping over the result of `to_arrow_iterable`
    # 2. an exception is raised in one of the loops
    # 3. we exit the loop, causing iterable consumption to stop, and queue popping
    #    to stop. At this point, the queue could be full. This means the worker
    #    thread would be blocked when calling the `Queue.put` method, and we never
    #    get to evaluate the download state and return.
    #
    # The following is the deadlocking portion of the original function, and is the
    # only portion that changed:
    #
    #    for page in rowstream.pages:
    #        if download_state.done:
    #            return
    #        item = page_to_item(page)
    #        worker_queue.put(item)
    #
    reader = bqstorage_client.read_rows(stream.name)

    # Avoid deprecation warnings for passing in unnecessary read session.
    # https://github.com/googleapis/python-bigquery-storage/issues/229
    if _determine_is_read_session_optional():
        rowstream = reader.rows()
    else:
        rowstream = reader.rows(session)

    for page in rowstream.pages:
        item = page_to_item(page)
        while True:
            if download_state.done:
                return
            try:
                worker_queue.put(item, timeout=_DEADLOCK_CIRCUMVENTING_TIMEOUT)
            except queue.Full:
                continue
            else:
                break


def monkeypatch_bq_table_download():
    try:
        import google.cloud.bigquery
    except ModuleNotFoundError:
        # the user did not specify that they want to use the bigquery module
        pass
    else:
        _is_read_session_optional = _determine_is_read_session_optional()
        # _is_read_session_optional being `None` means we failed to resolve the variable
        # due to import issues related to the BQ module. In that case, don't monkeypatch.
        _should_fallback = env_var_bool("CHALK_FALLBACK_TO_ORIGINAL_TABLE_DOWNLOAD_FUNC")
        if _should_fallback or _is_read_session_optional is None:
            _logger.warning(
                f"Not monkeypatching BQ table download function {_is_read_session_optional=} {_should_fallback=}"
            )
        else:
            try:
                import google.cloud.bigquery._pandas_helpers
            except ImportError:
                _logger.warning("Failed to import google.cloud.bigquery._pandas_helpers. Skipping monkey-patch.")
                pass
            else:
                _download_func_name = "_download_table_bqstorage_stream"
                if hasattr(google.cloud.bigquery._pandas_helpers, _download_func_name):
                    _logger.info("Monkeypatching BQ table download function")
                    setattr(
                        google.cloud.bigquery._pandas_helpers,
                        _download_func_name,
                        _download_table_bqstorage_stream_no_deadlock,
                    )
                else:
                    _logger.warning(
                        (
                            f"No {_download_func_name} function found in google.cloud.bigquery._pandas_helpers. "
                            "Skipping monkey-patch."
                        )
                    )


def _compile_parameter_to_bq_scalar_type(primitive: Any) -> ScalarQueryParameterType:
    # gated by import check in caller
    from google.cloud.bigquery import SqlParameterScalarTypes

    if isinstance(primitive, bool):
        return SqlParameterScalarTypes.BOOLEAN
    elif isinstance(primitive, int):
        return SqlParameterScalarTypes.INT64
    elif isinstance(primitive, float):
        return SqlParameterScalarTypes.FLOAT64
    elif isinstance(primitive, str):
        return SqlParameterScalarTypes.STRING
    elif isinstance(primitive, datetime):
        return SqlParameterScalarTypes.DATETIME
    elif isinstance(primitive, date):
        return SqlParameterScalarTypes.DATE
    elif isinstance(primitive, Decimal):
        return SqlParameterScalarTypes.DECIMAL
    elif isinstance(primitive, time):
        return SqlParameterScalarTypes.TIME
    elif isinstance(primitive, bytes):
        return SqlParameterScalarTypes.BYTES
    else:
        raise TypeError(f"Unsupported BigQuery parameter type '{type(primitive)}'")


_BQ_LOCATION_NAME = "BQ_LOCATION"
_BQ_DATASET_NAME = "BQ_DATASET"
_BQ_PROJECT_NAME = "BQ_PROJECT"
_BQ_CREDENTIALS_BASE64_NAME = "BQ_CREDENTIALS_BASE64"
_BQ_CREDENTIALS_PATH_NAME = "BQ_CREDENTIALS_PATH"


class BigQuerySourceImpl(BaseSQLSource):
    kind = SQLSourceKind.bigquery

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[str] = None,
        location: Optional[str] = None,
        credentials_base64: Optional[str] = None,
        credentials_path: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import sqlalchemy_bigquery
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")
        del sqlalchemy_bigquery  # unused
        monkeypatch_bq_table_download()
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        self.location = location or load_integration_variable(
            integration_name=name, name=_BQ_LOCATION_NAME, override=integration_variable_override
        )
        self.dataset = dataset or load_integration_variable(
            integration_name=name, name=_BQ_DATASET_NAME, override=integration_variable_override
        )
        self.project = project or load_integration_variable(
            integration_name=name, name=_BQ_PROJECT_NAME, override=integration_variable_override
        )
        self.credentials_base64 = credentials_base64 or load_integration_variable(
            integration_name=name, name=_BQ_CREDENTIALS_BASE64_NAME, override=integration_variable_override
        )
        self.credentials_path = credentials_path or load_integration_variable(
            integration_name=name, name=_BQ_CREDENTIALS_PATH_NAME, override=integration_variable_override
        )
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    @functools.cached_property
    def bigquery_read_client(self):
        import google.cloud.bigquery_storage

        with self._get_bq_client() as client:
            return google.cloud.bigquery_storage.BigQueryReadClient(
                credentials=client._credentials,  # pyright: ignore
            )

    def get_sqlglot_dialect(self) -> str | None:
        return "bigquery"

    def supports_inefficient_fallback(self) -> bool:
        return env_var_bool("CHALK_BIGQUERY_SUPPORTS_INEFFICIENT_FALLBACK", default=True)

    def compile_query(
        self,
        finalized_query: FinalizedChalkQuery,
        paramstyle: Optional[str] = None,
        use_sqlglot: bool = False,
    ) -> tuple[str, Sequence[Any], Dict[str, Any]]:
        if use_sqlglot:
            compiled_query = self._get_compiled_query(finalized_query, paramstyle)
            query_string = compiled_query.string

            import sqlglot.expressions
            from sqlglot import parse_one

            ast = parse_one(query_string, read=self.get_sqlglot_dialect())
            for placeholder in list(ast.find_all(sqlglot.expressions.Placeholder)):
                if isinstance(placeholder.this, str) and placeholder.this in compiled_query.params:
                    # Convert placeholders to use @ syntax
                    # https://cloud.google.com/bigquery/docs/parameterized-queries
                    placeholder.replace(sqlglot.expressions.var("@" + placeholder.this))
            updated_query_string = ast.sql(dialect="bigquery")

            return updated_query_string, compiled_query.positiontup, compiled_query.params
        else:
            if paramstyle is not None:
                raise ValueError("Bigquery does not support custom param styles")
            import google.cloud.bigquery
            import google.cloud.bigquery.dbapi
            import google.cloud.bigquery.dbapi._helpers
            import google.cloud.bigquery.dbapi.cursor
            from sqlalchemy_bigquery.base import BigQueryCompiler

            dialect = self.get_engine().dialect
            Compiler = cast("type[BigQueryCompiler]", self.get_engine().dialect.statement_compiler)

            compiled_stmt = Compiler(dialect, finalized_query.query)
            operation = compiled_stmt.string
            parameters = finalized_query.params if finalized_query.params else compiled_stmt.params
            (
                formatted_operation,
                parameter_types,
            ) = google.cloud.bigquery.dbapi.cursor._format_operation(  # pyright: ignore[reportPrivateUsage]
                operation, parameters
            )
            if len(formatted_operation) > _MAX_STATEMENT_LENGTH:
                raise ValueError("Query string is too large. Max supported size is 1MB.")
            # The DB-API uses the pyformat formatting, since the way BigQuery does
            # query parameters was not one of the standard options. Convert both
            # the query and the parameters to the format expected by the client
            # libraries.
            query_parameters = google.cloud.bigquery.dbapi._helpers.to_query_parameters(parameters, parameter_types)
            return formatted_operation, query_parameters, {}

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        query = {
            k: v
            for k, v in {
                "location": self.location,
                "credentials_base64": self.credentials_base64,
                "credentials_path": self.credentials_path,
            }.items()
            if v is not None
        }
        return URL.create(drivername="bigquery", host=self.project, database=self.dataset, query=query)

    @contextlib.contextmanager
    def _get_bq_client(self):
        # gated already
        import google.cloud.bigquery
        import google.cloud.bigquery.dbapi

        with self.get_engine().connect() as conn:
            dbapi = conn.connection.dbapi_connection
            assert isinstance(dbapi, google.cloud.bigquery.dbapi.Connection)
            client = dbapi._client  # pyright: ignore[reportPrivateUsage]
            assert isinstance(client, google.cloud.bigquery.Client)
            try:
                yield client
            finally:
                client.close()

    def _postprocess_table(
        self,
        features: Mapping[str, Feature],
        table: pa.RecordBatch,
    ):
        columns: list[pa.Array] = []
        column_names: list[str] = []

        for col_name, feature in features.items():
            column = table.column(col_name)
            expected_type = feature.converter.pyarrow_dtype
            if column.type != expected_type:
                column = column.cast(expected_type)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            columns.append(column)
            column_names.append(feature.root_fqn)
        return pa.RecordBatch.from_arrays(arrays=columns, names=column_names)

    @contextlib.contextmanager
    def _create_bigquery_temp_table(
        self,
        create_temp_table: CreateTable,
        temp_table: sqlalchemy.Table,
        drop_temp_table: DropTable,
        connection: google.cloud.bigquery.Client,
        temp_value: pa.Table,
        session_id: str | None,
    ):
        try:
            import google.cloud.bigquery
            import google.cloud.bigquery._pandas_helpers
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")

        create_table_sql = create_temp_table.compile(dialect=self.get_sqlalchemy_dialect()).string
        create_table_sql = create_table_sql.replace("TEMPORARY", "", 1)
        chalk_logger.info(f"Creating temporary table {temp_table.name} in BigQuery {session_id=}: {create_table_sql}")
        if session_id is not None:
            connection_properties = [google.cloud.bigquery.ConnectionProperty("session_id", session_id)]
        else:
            connection_properties = []
        job_config = google.cloud.bigquery.QueryJobConfig(
            priority="INTERACTIVE", connection_properties=connection_properties
        )
        connection.query(
            create_table_sql,
            job_config=job_config,
        ).result()
        try:
            connection.load_table_from_dataframe(
                temp_value.to_pandas(),
                f"{self.project}.{self.dataset}.{temp_table.name}",
                job_config=google.cloud.bigquery.LoadJobConfig(connection_properties=connection_properties),
            ).result()
            yield
        finally:
            drop_table_sql = drop_temp_table.compile(dialect=self.get_sqlalchemy_dialect()).string
            chalk_logger.info(f"Dropping temporary table {temp_table.name} in BigQuery: {drop_table_sql}")
            try:
                connection.query(
                    drop_table_sql,
                    job_config=job_config,
                ).result()
            except Exception as e:
                chalk_logger.warning(f"Failed to drop temporary BigQuery table {temp_table.name}: {e}")

    @contextlib.contextmanager
    def _bigquery_output_table(self, client: google.cloud.bigquery.Client) -> Iterator[str]:
        destination_table_name = f"temp_output_{str(uuid4()).replace('-', '_')}"

        destination = f"{client.project}.{self.dataset}.{destination_table_name}"

        try:
            yield destination
        finally:
            try:
                client.query(f"drop table {destination}").result()
            except Exception as e:
                chalk_logger.warning(f"Failed to drop temporary BigQuery table {destination}: {e}")

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        try:
            import google.cloud.bigquery
            import google.cloud.bigquery._pandas_helpers
            from sqlalchemy.sql import Select
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(finalized_query.query, _supported_sqlalchemy_types_for_pa_querying)

        client: google.cloud.bigquery.Client
        with self._get_bq_client() as client:
            query_job = client.query(
                "select 1;",
                job_config=google.cloud.bigquery.QueryJobConfig(priority="INTERACTIVE", create_session=True),
            )
            if query_job.session_info is not None:
                session_id = query_job.session_info.session_id
            else:
                session_id = None
            if session_id is None:
                _logger.warning("Failed to create a session, which is required for temp tables.")
            else:
                _logger.info(f"Created {session_id=}.")
            chalk_logger.info("Starting to execute BigQuery query")
            with contextlib.ExitStack() as exit_stack:
                for (
                    _,
                    temp_value,
                    create_temp_table,
                    temp_table,
                    drop_temp_table,
                ) in finalized_query.temp_tables.values():
                    exit_stack.enter_context(
                        self._create_bigquery_temp_table(
                            create_temp_table, temp_table, drop_temp_table, client, temp_value, session_id
                        )
                    )

                formatted_op, positional_params, named_params = self.compile_query(finalized_query)
                if named_params:
                    positional_params = [
                        # TODO: Consider type_ parameter more carefully.
                        google.cloud.bigquery.ScalarQueryParameter(
                            name=name, value=value, type_=_compile_parameter_to_bq_scalar_type(value)
                        )
                        for name, value in named_params.items()
                    ]
                if session_id is not None:
                    connection_properties = [google.cloud.bigquery.ConnectionProperty("session_id", session_id)]
                else:
                    connection_properties = []

                with self._bigquery_output_table(client) as destination:
                    job_config = google.cloud.bigquery.QueryJobConfig(
                        priority="INTERACTIVE",
                        query_parameters=positional_params or [],
                        connection_properties=connection_properties,
                        destination=destination,
                    )

                    chalk_logger.info(f"Executing BigQuery query: {formatted_op}")

                    res = client.query(formatted_op, job_config=job_config).result()
                    yielded = False

                    total_rows = 0
                    total_bytes = 0

                    for table in res.to_arrow_iterable(bqstorage_client=self.bigquery_read_client):
                        assert isinstance(table, pa.RecordBatch)
                        chalk_logger.info(f"Loaded table from Bigquery with {table.nbytes=}, {table.num_rows=}")
                        total_rows += table.num_rows
                        total_bytes += table.nbytes
                        features = columns_to_features(table.schema.names)
                        yield self._postprocess_table(features, table)
                        yielded = True
                    if not yielded and query_execution_parameters.yield_empty_batches:
                        # Copied from https://github.com/googleapis/python-bigquery/blob/89dfcb6469d22e78003a70371a0938a6856e033c/google/cloud/bigquery/table.py#L1954
                        arrow_schema = google.cloud.bigquery._pandas_helpers.bq_to_arrow_schema(
                            res._schema  # pyright: ignore[reportPrivateUsage]
                        )
                        if arrow_schema is not None:
                            features = columns_to_features(arrow_schema.names)
                            yield self._postprocess_table(
                                features,
                                pa.RecordBatch.from_pydict({k: [] for k in arrow_schema.names}, schema=arrow_schema),
                            )
                    chalk_logger.info(f"Loaded {total_rows=} rows and {total_bytes=} bytes from BigQuery")

    @classmethod
    def register_sqlalchemy_compiler_overrides(cls):
        try:
            from chalk.sql._internal.integrations.bigquery_compiler_overrides import register_bigquery_compiler_hooks
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")

        register_bigquery_compiler_hooks()

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_BQ_LOCATION_NAME, self.name, self.location),
                create_integration_variable(_BQ_DATASET_NAME, self.name, self.dataset),
                create_integration_variable(_BQ_PROJECT_NAME, self.name, self.project),
                create_integration_variable(_BQ_CREDENTIALS_BASE64_NAME, self.name, self.credentials_base64),
                create_integration_variable(_BQ_CREDENTIALS_PATH_NAME, self.name, self.credentials_path),
            ]
            if v is not None
        }
