from __future__ import annotations

import contextlib
import io
import logging
import os
import queue
import threading
import typing
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    NewType,
    Optional,
    Sequence,
    Type,
    Union,
    cast,
)

import pyarrow as pa
import pyarrow.parquet as pq

import chalk.logging
from chalk.features import Feature, FeatureConverter
from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.integrations.util import json_parse_and_cast
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    SQLSourceKind,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.df_utils import is_binary_like, read_parquet
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import LABELS_KEY, get_logger, get_logging_context
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.threading import DEFAULT_IO_EXECUTOR, MultiSemaphore
from chalk.utils.tracing import safe_incr, safe_set_gauge

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL
    from sqlalchemy.types import TypeEngine

_logger = get_logger(__name__)
_public_logger = chalk.logging.chalk_logger

_WorkerId = NewType("_WorkerId", int)


def _get_resolver_tags() -> list[str] | None:
    """Extract resolver_fqn from log context and return as tags list."""
    try:
        log_ctx = get_logging_context()
        labels = log_ctx.get(LABELS_KEY, {})
        resolver_fqn = labels.get("resolver_fqn")
        if resolver_fqn:
            return [f"resolver_fqn:{resolver_fqn}"]
    except Exception:
        # Don't fail if we can't get the resolver_fqn
        pass
    return None


def get_supported_redshift_unload_types() -> List[Type["TypeEngine"]]:
    """
    This is a method instead of a constant to avoid import issues
    :return:
    """

    import sqlalchemy as sa

    return [
        # SQL Standard types
        sa.JSON,
        sa.ARRAY,
        sa.REAL,
        sa.FLOAT,
        sa.NUMERIC,
        sa.DECIMAL,
        sa.INTEGER,
        sa.SMALLINT,
        sa.BIGINT,
        sa.TIMESTAMP,
        sa.DATETIME,
        sa.DATE,
        sa.TIME,
        sa.TEXT,
        sa.CLOB,
        sa.VARCHAR,
        sa.NVARCHAR,
        sa.CHAR,
        sa.NCHAR,
        sa.BLOB,
        sa.BINARY,
        # sa.VARBINARY, # This dtype is not supported for UNLOAD into PARQUET
        sa.BOOLEAN,
        # Generic types
        sa.Integer,
        sa.Float,
        sa.Numeric,
        sa.SmallInteger,
        sa.BigInteger,
        sa.DateTime,
        sa.Date,
        sa.Time,
        sa.Text,
        sa.Boolean,
    ]


_DEFAULT_REDSHIFT_S3_CLIENT = None
_BOTO_CLIENT_LOCK = threading.Lock()
_BOTO_SERIALIZE_CALLS: bool = env_var_bool("CHALK_REDSHIFT_SERIALIZE_BOTO_CALLS")


_REDSHIFT_HOST_NAME = "REDSHIFT_HOST"
_REDSHIFT_DB_NAME = "REDSHIFT_DB"
_REDSHIFT_USER_NAME = "REDSHIFT_USER"
_REDSHIFT_PASSWORD_NAME = "REDSHIFT_PASSWORD"
_REDSHIFT_UNLOAD_IAM_ROLE_NAME = "REDSHIFT_UNLOAD_IAM_ROLE"
_REDSHIFT_PORT_NAME = "REDSHIFT_PORT"
_REDSHIFT_UNLOAD_S3_BUCKET_NAME = "REDSHIFT_UNLOAD_S3_BUCKET"


class RedshiftSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.redshift

    def __init__(
        self,
        host: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        unload_iam_role: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        s3_client: Optional[S3Client] = None,
        s3_bucket: Optional[str] = None,
        executor: Optional[ThreadPoolExecutor] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import boto3
            import redshift_connector
        except ImportError:
            raise missing_dependency_exception("chalkpy[redshift]")
        del redshift_connector
        self.host = host or load_integration_variable(
            name=_REDSHIFT_HOST_NAME, integration_name=name, override=integration_variable_override
        )
        self.db = db or load_integration_variable(
            name=_REDSHIFT_DB_NAME, integration_name=name, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            name=_REDSHIFT_USER_NAME, integration_name=name, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            name=_REDSHIFT_PASSWORD_NAME, integration_name=name, override=integration_variable_override
        )
        self.unload_iam_role = unload_iam_role or load_integration_variable(
            name=_REDSHIFT_UNLOAD_IAM_ROLE_NAME, integration_name=name, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                name=_REDSHIFT_PORT_NAME, integration_name=name, parser=int, override=integration_variable_override
            )
        )
        # TODO customer may want to provide the s3 creds via the "AWS Integration" we provide.
        # NOTE: Chalk Engine injects its own S3 client via `_DEFAULT_REDSHIFT_S3_CLIENT`
        self._s3_client = s3_client or _DEFAULT_REDSHIFT_S3_CLIENT or boto3.client("s3")
        self._s3_bucket = s3_bucket or load_integration_variable(
            name=_REDSHIFT_UNLOAD_S3_BUCKET_NAME, integration_name=name, override=integration_variable_override
        )
        if self._s3_bucket is not None:
            self._s3_bucket = self._s3_bucket.removesuffix("s3://").lstrip("/")
        self._executor = executor or DEFAULT_IO_EXECUTOR

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
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    @property
    def s3_bucket(self):
        return self._s3_bucket

    def convert_db_types(self, v: Any, converter: FeatureConverter):
        """
        Redshift returns binary data as a hex string. Need to convert to bytes before returning as feature data.
        """
        if is_binary_like(converter.pyarrow_dtype):
            assert isinstance(v, str)
            v = bytes.fromhex(v)
        return super().convert_db_types(v, converter)

    def get_sqlglot_dialect(self) -> str | None:
        return "redshift"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="redshift+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
            port=self.port,
        )

    def supports_inefficient_fallback(self) -> bool:
        return False

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        temp_query_id = id(finalized_query)
        _public_logger.debug(f"Executing RedShift query [{temp_query_id}]...")

        if self._s3_bucket is None:
            raise UnsupportedEfficientExecutionError(
                "No S3 destination bucket configured for Redshift UNLOAD command, falling back to default execution mode.",
                log_level=logging.INFO,
            )
        with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
            with cnx.begin():
                cursor = cnx.connection.cursor()
                compiled_statement = self._get_compiled_query(finalized_query)

                from sqlalchemy.sql import Select

                if isinstance(finalized_query.query, Select):
                    validate_dtypes_for_efficient_execution(
                        finalized_query.query, supported_types=get_supported_redshift_unload_types()
                    )
                execution_context = self.get_engine().dialect.execution_ctx_cls._init_compiled(  # type: ignore
                    connection=cnx,
                    dialect=cnx.dialect,
                    dbapi_connection=cnx.connection.dbapi_connection,
                    execution_options={},
                    compiled=compiled_statement,
                    parameters=[],
                    invoked_statement=None,
                    extracted_parameters=None,
                )
                assert isinstance(execution_context, self.get_engine().dialect.execution_ctx_cls)
                operation = execution_context.statement
                assert operation is not None
                operation = operation.strip().removesuffix(";")
                params = execution_context.parameters[0]
                unload_destination = None

                # Redshift requires that the query used for an unload statement is literal quoted. That means that we CANNOT use a bind parameters within it
                # So, we will get around this using a "CREATE TEMP TABLE as SELECT (query with bind parameters)"
                # Then, we will run an unload query without any parameters: UNLOAD ('select * from temp_table')
                # Finally, we can drop the temp table
                temp_table_name = f"query_{str(uuid.uuid4()).replace('-', '_')}"
                try:
                    _logger.debug(f"Executing query & creating temp table '{temp_table_name}'")
                    _public_logger.info(f"Executing Redshift query [{temp_query_id}]: {operation}")
                    _public_logger.debug(f"Query parameters [{temp_query_id}]: {params}")
                    cursor.execute(f"CREATE TEMP TABLE {temp_table_name} AS ({operation})", params)
                except Exception as e:
                    _public_logger.error(f"Failed to create temp table for operation: {operation}", exc_info=e)
                    raise RuntimeError(f"Failed to create temp table for operation: {operation}") from e
                else:
                    unload_destination = f"{temp_table_name}/"
                    unload_uri = f"s3://{self._s3_bucket}/{unload_destination}"
                    unload_iam_role = "default" if self.unload_iam_role is None else f"'{self.unload_iam_role}'"
                    unload_query = f"UNLOAD ('SELECT * FROM {temp_table_name}') TO '{unload_uri}' IAM_ROLE {unload_iam_role} FORMAT PARQUET EXTENSION 'parquet'"
                    _public_logger.info(f"Executing UNLOAD query [{temp_query_id}]: {unload_query}")
                    cursor.execute(unload_query)
                finally:
                    try:
                        cursor.execute(f"DROP TABLE {temp_table_name}")
                    except Exception:
                        _logger.warning(f"Failed to drop temp table '{temp_table_name}'", exc_info=True)
        # Redshift is case-insensitive with column names, so let's map it back to what we were expecting
        assert unload_destination is not None
        _public_logger.info(
            f"Finished executing redshift UNLOAD, [{temp_query_id}] reading parquet data from {unload_destination}..."
        )
        yield from self._download_objs_async(
            unload_destination=unload_destination,
            columns_to_features=columns_to_features,
            yield_empty_batches=query_execution_parameters.yield_empty_batches,
            max_prefetch_size_bytes=query_execution_parameters.max_prefetch_size_bytes,
            num_client_prefetch_threads=query_execution_parameters.num_client_prefetch_threads,
        )

    def _download_worker(
        self,
        file_handles: queue.Queue[str],
        sem: MultiSemaphore | None,
        pa_table_queue: queue.Queue[tuple[pa.Table, int] | _WorkerId],
        worker_idx: _WorkerId,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
    ):
        """Worker thread that downloads files from S3 with memory control."""
        assert self._s3_bucket is not None
        try:
            while True:
                try:
                    filename = file_handles.get_nowait()
                except queue.Empty:
                    break

                # Estimate file size from S3 metadata if possible
                weight: int | None = None
                try:
                    with _boto_lock_ctx():
                        head_response = self._s3_client.head_object(Bucket=self._s3_bucket, Key=filename)
                        # Boto3 types indicate ContentLength is always int, but cast to Optional for defensive programming
                        content_length = cast(int | None, head_response.get("ContentLength"))
                        if content_length is not None:
                            # Estimate uncompressed size (parquet typically compresses 3-5x)
                            weight = content_length * 4
                except Exception as e:
                    _logger.warning(f"Failed to get file size for {filename}, will estimate after download", exc_info=e)

                # Acquire semaphore before downloading
                if sem and weight is not None:
                    if weight > sem.initial_value:
                        # If the file is larger than the maximum size, truncate to max
                        weight = sem.initial_value
                    if weight > 0:
                        if not sem.acquire(weight):
                            raise RuntimeError("Failed to acquire semaphore for redshift download")
                        safe_set_gauge(
                            "chalk.redshift.remaining_prefetch_bytes", sem.get_value(), tags=_get_resolver_tags()
                        )

                # Download and convert to table
                tbl = _download_file_to_table(self._s3_client, self._s3_bucket, filename, columns_to_features)

                # If we didn't have a weight estimate, use actual table size
                if weight is None:
                    weight = tbl.nbytes
                    if sem and weight is not None and weight > 0:
                        if not sem.acquire(weight):
                            raise RuntimeError("Failed to acquire semaphore for redshift download")
                        safe_set_gauge(
                            "chalk.redshift.remaining_prefetch_bytes", sem.get_value(), tags=_get_resolver_tags()
                        )

                # Ensure weight is always an int
                final_weight: int = weight if weight is not None else 0
                pa_table_queue.put((tbl, final_weight))
        finally:
            # Signal that this worker is done
            pa_table_queue.put(worker_idx)

    def _download_objs_async(
        self,
        unload_destination: str,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        yield_empty_batches: bool,
        max_prefetch_size_bytes: int,
        num_client_prefetch_threads: int,
    ) -> Iterable[pa.RecordBatch]:
        """Download objects from S3 with byte-bounded memory control."""
        assert self._s3_bucket is not None
        filenames = list(_list_files(self._s3_client, self._s3_bucket, unload_destination))
        _public_logger.info(
            f"Downloading parquet data partitioned into {len(filenames)} files "
            + f"(max_prefetch_bytes={max_prefetch_size_bytes}, threads={num_client_prefetch_threads})..."
        )

        if len(filenames) == 0:
            if yield_empty_batches:
                # Need to get schema somehow - return empty batch
                # This matches the original behavior
                schema: pa.Schema | None = None
                if schema is not None:
                    yield pa.RecordBatch.from_pydict({k: [] for k in schema.names}, schema)
            return

        # Set up queues and semaphore for memory control
        file_handles: queue.Queue[str] = queue.Queue()
        for filename in filenames:
            file_handles.put(filename)

        max_weight = max_prefetch_size_bytes if max_prefetch_size_bytes > 0 else None
        pa_table_queue: queue.Queue[tuple[pa.Table, int] | _WorkerId] = queue.Queue()
        sem = None if max_weight is None else MultiSemaphore(max_weight)

        # Start download workers
        futures = {
            _WorkerId(i): self._executor.submit(
                self._download_worker,
                file_handles,
                sem,
                pa_table_queue,
                _WorkerId(i),
                columns_to_features,
            )
            for i in range(num_client_prefetch_threads)
        }

        schema: pa.Schema | None = None
        yielded = False

        # Process downloaded tables as they become available
        while len(futures) > 0:
            x = pa_table_queue.get()
            if isinstance(x, int):
                # Worker finished - remove from futures and check for errors
                futures.pop(x).result()
                continue

            tbl, weight = x
            if schema is None:
                schema = tbl.schema

            try:
                if len(tbl) > 0:
                    yield tbl.combine_chunks().to_batches()[0]
                    safe_incr("chalk.redshift.downloaded_bytes", tbl.nbytes or 0, tags=_get_resolver_tags())
                    safe_incr("chalk.redshift.downloaded_rows", tbl.num_rows or 0, tags=_get_resolver_tags())
                    yielded = True
            finally:
                # Release semaphore after yielding
                if sem is not None and weight > 0:
                    sem.release(weight)
                    safe_set_gauge(
                        "chalk.redshift.remaining_prefetch_bytes", sem.get_value(), tags=_get_resolver_tags()
                    )

        if not yielded and yield_empty_batches and schema is not None:
            yield pa.RecordBatch.from_pydict({k: [] for k in schema.names}, schema)

    def _download_worker_raw(
        self,
        file_handles: queue.Queue[str],
        sem: MultiSemaphore | None,
        pa_table_queue: queue.Queue[tuple[pa.Table, int] | _WorkerId],
        worker_idx: _WorkerId,
        expected_output_schema: pa.Schema,
    ):
        """Worker thread that downloads files from S3 with memory control for raw execution."""
        import pyarrow.compute as pc

        assert self._s3_bucket is not None
        try:
            while True:
                try:
                    filename = file_handles.get_nowait()
                except queue.Empty:
                    break

                # Estimate file size from S3 metadata if possible
                weight: int | None = None
                try:
                    with _boto_lock_ctx():
                        head_response = self._s3_client.head_object(Bucket=self._s3_bucket, Key=filename)
                        # Boto3 types indicate ContentLength is always int, but cast to Optional for defensive programming
                        content_length = cast(int | None, head_response.get("ContentLength"))
                        if content_length is not None:
                            # Estimate uncompressed size (parquet typically compresses 3-5x)
                            weight = content_length * 4
                except Exception as e:
                    _logger.warning(f"Failed to get file size for {filename}, will estimate after download", exc_info=e)

                # Acquire semaphore before downloading
                if sem and weight is not None:
                    if weight > sem.initial_value:
                        weight = sem.initial_value
                    if weight > 0:
                        if not sem.acquire(weight):
                            raise RuntimeError("Failed to acquire semaphore for redshift download")
                        safe_set_gauge(
                            "chalk.redshift.remaining_prefetch_bytes", sem.get_value(), tags=_get_resolver_tags()
                        )

                # Download parquet file
                buffer = io.BytesIO()
                with _boto_lock_ctx():
                    self._s3_client.download_fileobj(Bucket=self._s3_bucket, Key=filename, Fileobj=buffer)
                    buffer.seek(0)
                    if env_var_bool("CHALK_REDSHIFT_POLARS_PARQUET"):
                        tbl = read_parquet(buffer, use_pyarrow=False).to_arrow()
                    else:
                        tbl = pq.read_table(buffer)

                # If we didn't have a weight estimate, use actual table size
                if weight is None:
                    weight = tbl.nbytes
                    if sem and weight is not None and weight > 0:
                        if not sem.acquire(weight):
                            raise RuntimeError("Failed to acquire semaphore for redshift download")
                        safe_set_gauge(
                            "chalk.redshift.remaining_prefetch_bytes", sem.get_value(), tags=_get_resolver_tags()
                        )

                # Map columns to expected schema
                arrays: list[pa.Array] = []
                for field in expected_output_schema:
                    if field.name in tbl.column_names:
                        col = tbl.column(field.name)
                        # Cast to expected type if needed
                        if col.type != field.type:
                            col = pc.cast(col, field.type)
                        arrays.append(col)
                    else:
                        # Column not found, create null array
                        arrays.append(pa.nulls(len(tbl), field.type))

                mapped_tbl = pa.Table.from_arrays(arrays, schema=expected_output_schema)
                # Ensure weight is always an int
                final_weight: int = weight if weight is not None else 0
                pa_table_queue.put((mapped_tbl, final_weight))
        finally:
            # Signal that this worker is done
            pa_table_queue.put(worker_idx)

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for Redshift and return raw PyArrow RecordBatches."""
        temp_query_id = id(finalized_query)
        _public_logger.debug(f"Executing RedShift query [{temp_query_id}]...")

        if self._s3_bucket is None:
            raise UnsupportedEfficientExecutionError(
                "No S3 destination bucket configured for Redshift UNLOAD command, falling back to default execution mode.",
                log_level=logging.INFO,
            )

        with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
            with cnx.begin():
                cursor = cnx.connection.cursor()
                compiled_statement = self._get_compiled_query(finalized_query)

                from sqlalchemy.sql import Select

                if isinstance(finalized_query.query, Select):
                    validate_dtypes_for_efficient_execution(
                        finalized_query.query, supported_types=get_supported_redshift_unload_types()
                    )

                execution_context = self.get_engine().dialect.execution_ctx_cls._init_compiled(  # type: ignore
                    connection=cnx,
                    dialect=cnx.dialect,
                    dbapi_connection=cnx.connection.dbapi_connection,
                    execution_options={},
                    compiled=compiled_statement,
                    parameters=[],
                    invoked_statement=None,
                    extracted_parameters=None,
                )
                assert isinstance(execution_context, self.get_engine().dialect.execution_ctx_cls)
                operation = execution_context.statement
                assert operation is not None
                operation = operation.strip().removesuffix(";")
                params = execution_context.parameters[0]
                unload_destination = None

                temp_table_name = f"query_{str(uuid.uuid4()).replace('-', '_')}"
                try:
                    _logger.debug(f"Executing query & creating temp table '{temp_table_name}'")
                    _public_logger.info(f"Executing Redshift query [{temp_query_id}]: {operation}")
                    _public_logger.debug(f"Query parameters [{temp_query_id}]: {params}")
                    cursor.execute(f"CREATE TEMP TABLE {temp_table_name} AS ({operation})", params)
                except Exception as e:
                    _public_logger.error(f"Failed to create temp table for operation: {operation}", exc_info=e)
                    raise RuntimeError(f"Failed to create temp table for operation: {operation}") from e
                else:
                    unload_destination = f"{temp_table_name}/"
                    unload_uri = f"s3://{self._s3_bucket}/{unload_destination}"
                    unload_iam_role = "default" if self.unload_iam_role is None else f"'{self.unload_iam_role}'"
                    unload_query = f"UNLOAD ('SELECT * FROM {temp_table_name}') TO '{unload_uri}' IAM_ROLE {unload_iam_role} FORMAT PARQUET EXTENSION 'parquet'"
                    _public_logger.info(f"Executing UNLOAD query [{temp_query_id}]: {unload_query}")
                    cursor.execute(unload_query)
                finally:
                    try:
                        cursor.execute(f"DROP TABLE {temp_table_name}")
                    except Exception:
                        _logger.warning(f"Failed to drop temp table '{temp_table_name}'", exc_info=True)

        # Download files with memory control
        assert unload_destination is not None
        assert self._s3_bucket is not None
        filenames = list(_list_files(self._s3_client, self._s3_bucket, unload_destination))
        _public_logger.info(
            f"Downloading {len(filenames)} parquet files from Redshift UNLOAD "
            + f"(max_prefetch_bytes={query_execution_parameters.max_prefetch_size_bytes}, "
            + f"threads={query_execution_parameters.num_client_prefetch_threads})..."
        )

        if len(filenames) == 0:
            if query_execution_parameters.yield_empty_batches:
                arrays = [pa.nulls(0, field.type) for field in expected_output_schema]
                yield pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
            return

        # Set up queues and semaphore for memory control
        file_handles: queue.Queue[str] = queue.Queue()
        for filename in filenames:
            file_handles.put(filename)

        max_weight = (
            query_execution_parameters.max_prefetch_size_bytes
            if query_execution_parameters.max_prefetch_size_bytes > 0
            else None
        )
        pa_table_queue: queue.Queue[tuple[pa.Table, int] | _WorkerId] = queue.Queue()
        sem = None if max_weight is None else MultiSemaphore(max_weight)

        # Start download workers
        futures = {
            _WorkerId(i): self._executor.submit(
                self._download_worker_raw,
                file_handles,
                sem,
                pa_table_queue,
                _WorkerId(i),
                expected_output_schema,
            )
            for i in range(query_execution_parameters.num_client_prefetch_threads)
        }

        yielded = False

        # Process downloaded tables as they become available
        while len(futures) > 0:
            x = pa_table_queue.get()
            if isinstance(x, int):
                # Worker finished - remove from futures and check for errors
                futures.pop(x).result()
                continue

            tbl, weight = x

            try:
                if len(tbl) > 0:
                    yield tbl.to_batches()[0]
                    safe_incr("chalk.redshift.downloaded_bytes", tbl.nbytes or 0, tags=_get_resolver_tags())
                    safe_incr("chalk.redshift.downloaded_rows", tbl.num_rows or 0, tags=_get_resolver_tags())
                    yielded = True
            finally:
                # Release semaphore after yielding
                if sem is not None and weight > 0:
                    sem.release(weight)
                    safe_set_gauge(
                        "chalk.redshift.remaining_prefetch_bytes", sem.get_value(), tags=_get_resolver_tags()
                    )

        if not yielded and query_execution_parameters.yield_empty_batches:
            arrays = [pa.nulls(0, field.type) for field in expected_output_schema]
            yield pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)

    @classmethod
    def register_sqlalchemy_compiler_overrides(cls):
        try:
            from chalk.sql._internal.integrations.redshift_compiler_overrides import register_redshift_compiler_hooks
        except ImportError:
            raise missing_dependency_exception("chalkpy[redshift]")

        register_redshift_compiler_hooks()

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_REDSHIFT_HOST_NAME, self.name, self.host),
                create_integration_variable(_REDSHIFT_DB_NAME, self.name, self.db),
                create_integration_variable(_REDSHIFT_USER_NAME, self.name, self.user),
                create_integration_variable(_REDSHIFT_PASSWORD_NAME, self.name, self.password),
                create_integration_variable(_REDSHIFT_PORT_NAME, self.name, self.port),
                create_integration_variable(_REDSHIFT_UNLOAD_IAM_ROLE_NAME, self.name, self.unload_iam_role),
                create_integration_variable(_REDSHIFT_UNLOAD_S3_BUCKET_NAME, self.name, self._s3_bucket),
            ]
            if v is not None
        }


def _boto_lock_ctx() -> typing.ContextManager:
    if _BOTO_SERIALIZE_CALLS:
        lock_ctx = _BOTO_CLIENT_LOCK
    else:
        lock_ctx = contextlib.nullcontext()
    return lock_ctx


def _list_files(client: S3Client, bucket: str, prefix: str) -> Iterable[str]:
    try:
        continuation_token = None
        while True:
            with _boto_lock_ctx():
                if continuation_token is None:
                    resp = client.list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix,
                    )
                else:
                    resp = client.list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix,
                        ContinuationToken=continuation_token,
                    )
            # If no keys returned, the server omits 'Contents'
            for row in resp.get("Contents", []):
                key = row.get("Key")
                assert key is not None, "all objects must have a key"
                yield key
            if not resp["IsTruncated"]:
                return
            continuation_token = resp["NextContinuationToken"]
    except Exception:
        _logger.error(f"Got exception while listing files for {prefix=}", exc_info=True)
        raise


def _download_file_to_table(
    client: S3Client,
    bucket: str,
    filename: str,
    cols_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
) -> pa.Table:
    _logger.debug(f"Downloading parquet file {filename} into arrow table....")
    buffer = io.BytesIO()
    with _boto_lock_ctx():
        client.download_fileobj(Bucket=bucket, Key=filename, Fileobj=buffer)
        _logger.debug(f"Fetched parquet file {filename}. Reading into arrow...")
        buffer.seek(0)
        if env_var_bool("CHALK_REDSHIFT_POLARS_PARQUET"):
            tbl = read_parquet(buffer, use_pyarrow=False).to_arrow()
        else:
            tbl = pq.read_table(buffer)
        _logger.debug(f"Read parquet file {filename} into arrow: {tbl.nbytes=}, {tbl.num_rows=}. Converting columns...")
    # TODO (CHA-2232) Delete the `filename` from the bucket since we'll never look at it again

    # Infer results schema from table columns & map to correct dtype
    features = cols_to_features(tbl.column_names)
    results_schema = {v.root_fqn: v.converter.pyarrow_dtype for v in features.values()}
    tbl = tbl.select(list(features.keys())).rename_columns([x.root_fqn for x in features.values()])
    table = json_parse_and_cast(tbl, results_schema)
    _logger.debug(f"Finished downloading parquet file {filename}.")
    return table
