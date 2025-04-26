from __future__ import annotations

import base64
import concurrent.futures
import contextlib
import dataclasses
import functools
import json
import os
import queue
import typing
import uuid
from typing import TYPE_CHECKING, Any, Callable, Mapping, NewType, Optional, Sequence, cast

import orjson
import packaging.version
import pyarrow
import pyarrow as pa
import pyarrow.compute as pc

from chalk.clogging import chalk_logger
from chalk.features import Feature
from chalk.features._encoding.converter import FeatureConverter
from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, validate_dtypes_for_efficient_execution
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.df_utils import is_list_like, pa_array_to_pl_series
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.threading import DEFAULT_IO_EXECUTOR, MultiSemaphore
from chalk.utils.tracing import safe_incr, safe_set_gauge

if TYPE_CHECKING:
    from snowflake.connector.connection import SnowflakeConnection
    from snowflake.connector.result_batch import ResultBatch
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL
    from sqlalchemy.sql.ddl import CreateTable, DropTable
    from sqlalchemy.sql.schema import Table

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


@functools.lru_cache(None)
def _has_new_fetch_arrow_all():
    # The api for fetch arrow all changed in v3.7.0 to include force_return_table
    # See https://github.com/snowflakedb/snowflake-connector-python/blob/3cced62f2d31b84299b544222c836a275a6d45a2/src/snowflake/connector/cursor.py#L1344
    import snowflake.connector

    return packaging.version.parse(snowflake.connector.__version__) >= packaging.version.parse("3.7.0")


_WorkerId = NewType("_WorkerId", int)


def _stage_prefix(unload_job_identifier: str, snowflake_unload_stage: str) -> str:
    return f"{snowflake_unload_stage}/{unload_job_identifier}/"


def _rewrite_query_for_unload(sql: str, unload_job_identifier: str, snowflake_unload_stage: str):
    rewritten_sql = sql.rstrip(";\n ")
    prefix = _stage_prefix(unload_job_identifier, snowflake_unload_stage)
    new_query = f"""
    COPY INTO {prefix} FROM ({rewritten_sql}) file_format = (type = 'parquet') overwrite=true header=true; /* {json.dumps({'unload_job_identifier': unload_job_identifier})} */
    """
    return new_query


class ResultHandle(typing.Protocol):
    @property
    def estimated_uncompressed_size(self) -> int | None:
        return None

    def to_arrow(self, connection: SnowflakeConnection | None) -> pyarrow.Table:
        ...


@dataclasses.dataclass(frozen=True)
class ResultBatchResultHandle(ResultHandle):
    result_batch: ResultBatch

    @property
    def estimated_uncompressed_size(self) -> int | None:
        return self.result_batch.uncompressed_size

    @property
    def num_rows(self) -> int | None:
        return self.result_batch.rowcount

    def to_arrow(self, connection: SnowflakeConnection | None):
        from snowflake.connector.result_batch import ArrowResultBatch

        if isinstance(self.result_batch, ArrowResultBatch):
            return self.result_batch.to_arrow(connection)
        else:
            return self.result_batch.to_arrow()


@dataclasses.dataclass(frozen=True)
class UnloadedStorageFileResultHandle(ResultHandle):
    uri: str
    compressed_size: int

    @property
    def estimated_uncompressed_size(self) -> int | None:
        # this is a (hopefully) conservative estimate.
        return self.compressed_size * 8

    def to_arrow(self, connection: SnowflakeConnection | None):
        import polars as pl

        chalk_logger.info(f"Loading table from {self.uri}")
        return pl.read_parquet(source=self.uri).to_arrow()


_SNOWFLAKE_ACCOUNT_ID_NAME = "SNOWFLAKE_ACCOUNT_ID"
_SNOWFLAKE_WAREHOUSE_NAME = "SNOWFLAKE_WAREHOUSE"
_SNOWFLAKE_USER_NAME = "SNOWFLAKE_USER"
_SNOWFLAKE_PASSWORD_NAME = "SNOWFLAKE_PASSWORD"
_SNOWFLAKE_DATABASE_NAME = "SNOWFLAKE_DATABASE"
_SNOWFLAKE_SCHEMA_NAME = "SNOWFLAKE_SCHEMA"
_SNOWFLAKE_ROLE_NAME = "SNOWFLAKE_ROLE"
_SNOWFLAKE_PRIVATE_KEY_B64_NAME = "SNOWFLAKE_PRIVATE_KEY_B64"


class SnowflakeSourceImpl(BaseSQLSource):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        account_identifier: Optional[str] = None,
        warehouse: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        db: Optional[str] = None,
        schema: Optional[str] = None,
        role: Optional[str] = None,
        private_key_b64: Optional[str] = None,
        engine_args: Optional[dict[str, Any]] = None,
        executor: Optional[concurrent.futures.ThreadPoolExecutor] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import snowflake.connector  # noqa
            import snowflake.sqlalchemy  # noqa
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import serialization
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[snowflake]")
        del snowflake  # unused

        self.account_identifier = account_identifier or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_ACCOUNT_ID_NAME, override=integration_variable_override
        )
        self.warehouse = warehouse or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_WAREHOUSE_NAME, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_USER_NAME, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_PASSWORD_NAME, override=integration_variable_override
        )
        self.db = db or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_DATABASE_NAME, override=integration_variable_override
        )
        self.schema = schema or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_SCHEMA_NAME, override=integration_variable_override
        )
        self.role = role or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_ROLE_NAME, override=integration_variable_override
        )
        private_key_b64_str = private_key_b64
        if isinstance(private_key_b64_str, bytes):
            private_key_b64_str = private_key_b64_str.decode("utf-8")
        self.private_key_b64: Optional[str] = private_key_b64_str or load_integration_variable(
            integration_name=name, name=_SNOWFLAKE_PRIVATE_KEY_B64_NAME, override=integration_variable_override
        )
        self.executor = executor or DEFAULT_IO_EXECUTOR

        if engine_args is None:
            engine_args = {}
        connect_args = {
            "client_prefetch_threads": min((os.cpu_count() or 1) * 2, 32),
            "client_session_keep_alive": True,
            "application_name": "chalkai_featurepipelines",
            "application": "chalkai_featurepipelines",
        }
        if self.private_key_b64 is not None:
            raw_bytes = base64.b64decode(self.private_key_b64)
            # From https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#label-python-key-pair-authn-rotation
            private_key_bytes = serialization.load_pem_private_key(
                raw_bytes, password=None, backend=default_backend()
            ).private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            connect_args = connect_args | {"private_key": private_key_bytes}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault("connect_args", connect_args)

        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    kind = SQLSourceKind.snowflake

    def get_sqlglot_dialect(self) -> str | None:
        return "snowflake"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        query = {
            k: v
            for k, v in (
                {
                    "database": self.db,
                    "schema": self.schema,
                    "warehouse": self.warehouse,
                    "role": self.role,
                }
            ).items()
            if v is not None
        }
        return URL.create(
            drivername="snowflake",
            username=self.user,
            password=self.password,
            host=self.account_identifier,
            query=query,
        )

    def convert_db_types(self, v: Any, converter: FeatureConverter):
        """
        Overload this if a given DB type needs custom type conversion
        """
        if (is_list_like(converter.pyarrow_dtype) or pa.types.is_struct(converter.pyarrow_dtype)) and isinstance(
            v, (str, bytes)
        ):
            # Need to json-decode these types
            v = orjson.loads(v)
        return converter.from_rich_to_primitive(v, missing_value_strategy="default_or_allow")

    @contextlib.contextmanager
    def _create_temp_table(
        self,
        create_temp_table: CreateTable,
        temp_table: Table,
        drop_temp_table: DropTable,
        connection: Connection,
        temp_value: pa.Table,
    ):
        from snowflake.connector import pandas_tools

        snowflake_cnx = cast("SnowflakeConnection", connection.connection.dbapi_connection)
        with snowflake_cnx.cursor() as cursor:
            chalk_logger.info(f"Creating temporary table {temp_table.name} in Snowflake.")
            cursor.execute(create_temp_table.compile(dialect=self.get_sqlalchemy_dialect()).string)
            try:
                pandas_tools.write_pandas(
                    cursor.connection,
                    temp_value.to_pandas(),
                    str(temp_table.name),
                )
                yield
            finally:
                # "temp table", to snowflake, means that it belongs to the session. However, we keep using the same Snowflake session
                chalk_logger.info(f"Dropping temporary table {temp_table.name} in Snowflake.")
                cursor.execute(drop_temp_table.compile(dialect=self.get_sqlalchemy_dialect()).string)

    def _postprocess_table(self, features: Mapping[str, Feature], tbl: pa.Table):
        columns: list[pa.Array] = []
        column_names: list[str] = []
        chalk_logger.info(
            f"Received a PyArrow table from Snowflake with {len(tbl)} rows; {len(tbl.column_names)} columns; {tbl.nbytes=}; {tbl.schema=}"
        )

        for col_name, feature in features.items():
            try:
                column = tbl[col_name]
                expected_type = feature.converter.pyarrow_dtype
                actual_type = tbl.schema.field(col_name).type
                if pa.types.is_list(expected_type) or pa.types.is_large_list(expected_type):
                    if pa.types.is_string(actual_type) or pa.types.is_large_string(actual_type):
                        series = pa_array_to_pl_series(tbl[col_name])
                        column = series.str.json_extract(feature.converter.polars_dtype).to_arrow().cast(expected_type)
                if actual_type != expected_type:
                    column = column.cast(options=pc.CastOptions(target_type=expected_type, allow_time_truncate=True))
                if isinstance(column, pa.ChunkedArray):
                    column = column.combine_chunks()
                columns.append(column)
                column_names.append(feature.root_fqn)
            except:
                chalk_logger.error(f"Failed to deserialize column '{col_name}' into '{feature}'", exc_info=True)
                raise

        return pa.RecordBatch.from_arrays(arrays=columns, names=column_names)

    def _download_worker(
        self,
        result_handles: queue.Queue[ResultHandle],
        sem: MultiSemaphore | None,
        pa_table_queue: queue.Queue[tuple[pa.Table, int] | _WorkerId],
        worker_idx: _WorkerId,
    ):
        try:
            while True:
                try:
                    x = result_handles.get_nowait()
                except queue.Empty:
                    break
                weight = x.estimated_uncompressed_size
                as_arrow = None
                if weight is None:
                    # This is possible if the chunk is "local", which I think snowflake does for small result batches
                    as_arrow: pyarrow.Table = x.to_arrow(None)
                    weight = as_arrow.nbytes
                if sem:
                    if weight > sem.initial_value:
                        # If the file is larger than the maximum size, we'll truncate it, so this file will be the only one being downloaded
                        weight = sem.initial_value
                    if weight > 0:
                        # No need to acquire the semaphore for empty tables
                        if not sem.acquire(weight):
                            raise RuntimeError("Failed to acquire semaphore for snowflake download")
                        safe_set_gauge("chalk.snowflake.remaining_prefetch_bytes", sem.get_value())
                if as_arrow is None:
                    with self.get_engine().connect() as connection:
                        # Reusing an existing connection from the pool to avoid re-establishing sessions, tls handshakes, etc...
                        snowflake_cnx = cast(
                            "SnowflakeConnection",
                            connection.connection.dbapi_connection,
                        )
                        as_arrow = x.to_arrow(snowflake_cnx)
                pa_table_queue.put((as_arrow, weight))
        finally:
            # At the end, putting the worker id to signal that this worker is done
            pa_table_queue.put(worker_idx)

    def supports_inefficient_fallback(self) -> bool:
        return False

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ):
        # these imports are safe because the only way we end up here is if we have a valid SnowflakeSource constructed,
        # which already gates this import
        import snowflake.connector
        from sqlalchemy.sql import Select

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(finalized_query.query, _supported_sqlalchemy_types_for_pa_querying)

        result_handles: queue.Queue[ResultHandle] = queue.Queue()  # Using a queue since we'll be concurrently reading
        with (
            self.get_engine().connect() if connection is None else contextlib.nullcontext(connection)
        ) as sqlalchemy_cnx:
            con = cast(
                snowflake.connector.SnowflakeConnection,
                sqlalchemy_cnx.connection.dbapi_connection,
            )
            chalk_logger.info("Established connection with Snowflake")
            sql, positional_params, named_params = self.compile_query(finalized_query)
            assert len(positional_params) == 0, "using named param style"
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
                with con.cursor() as cursor:
                    job_id = str(uuid.uuid4())
                    if query_execution_parameters.snowflake.snowflake_unload_stage is not None:
                        original_sql = sql
                        chalk_logger.info(
                            f"Executing query to unload data to Snowflake stage for unload {job_id=} {query_execution_parameters.snowflake.snowflake_unload_stage}"
                        )
                        sql = _rewrite_query_for_unload(
                            sql=sql,
                            unload_job_identifier=job_id,
                            snowflake_unload_stage=query_execution_parameters.snowflake.snowflake_unload_stage,
                        )

                    chalk_logger.info(f"Compiled query: {repr(sql)}")

                    res = cursor.execute(sql, named_params)
                    chalk_logger.info("Executed Snowflake query. Fetching results.")
                    assert res is not None

                    empty_batch_with_schema = None
                    if query_execution_parameters.snowflake.snowflake_unload_stage is not None:
                        # get the uris of the files that were unloaded
                        prefix = _stage_prefix(
                            job_id,
                            query_execution_parameters.snowflake.snowflake_unload_stage,
                        )
                        stage_list_cursor = cursor.execute(f"LIST {prefix}")
                        if stage_list_cursor is None:
                            chalk_logger.error("Failed to enumerate unloaded files in Snowflake stage")
                            raise ValueError("Failed to enumerate unloaded files in Snowflake stage")
                        stage_list = stage_list_cursor.fetchall()
                        chalk_logger.info(f"Found {len(stage_list)} files in Snowflake stage at prefix: {prefix}")
                        for row in stage_list:
                            # name/size/md5/last_modified
                            result_handles.put_nowait(
                                UnloadedStorageFileResultHandle(uri=row[0], compressed_size=row[1])
                            )
                        if cursor.rowcount == 0:
                            cursor.execute(original_sql, named_params)
                            chalk_logger.info(
                                "Executed Snowflake query to get empty batch with schema. Fetching results."
                            )
                            empty_batch_with_schema = (
                                cursor.fetch_arrow_all(True) if _has_new_fetch_arrow_all() else None
                            )
                    else:
                        chalk_logger.info("Fetching arrow tables from Snowflake.")
                        for batch in cursor.get_result_batches() or []:
                            result_handles.put_nowait(ResultBatchResultHandle(batch))

                        empty_batch_with_schema = (
                            cursor.fetch_arrow_all(True)
                            if cursor.rowcount == 0 and _has_new_fetch_arrow_all()
                            else None
                        )

        yield from self._yield_from_result_handles(
            result_handles, query_execution_parameters, columns_to_features, empty_batch_with_schema
        )

    def _yield_from_result_handles(
        self,
        result_handles: queue.Queue[ResultHandle],
        query_execution_parameters: QueryExecutionParameters,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        empty_batch_with_schema: pa.Table | None,
    ):
        yielded = False
        max_weight = query_execution_parameters.max_prefetch_size_bytes
        if max_weight <= 0:
            max_weight = None
        pa_table_queue: queue.Queue[tuple[pa.Table, int] | _WorkerId] = queue.Queue()
        sem = None if max_weight is None else MultiSemaphore(max_weight)
        assert query_execution_parameters.num_client_prefetch_threads >= 1

        futures = {
            _WorkerId(i): self.executor.submit(
                self._download_worker,
                result_handles,
                sem,
                pa_table_queue,
                _WorkerId(i),
            )
            for i in range(query_execution_parameters.num_client_prefetch_threads)
        }
        schema: pa.Schema | None = None
        while len(futures) > 0:
            x = pa_table_queue.get()
            if isinstance(x, int):
                # It's a _WorkerId, meaning that this download worker is done
                # We'll pop this worker from the futures list, and then await the result
                # This will raise if the download worker crashed, which is what we want, or be a no-op if the download worker succeeded
                futures.pop(x).result()
                continue
            tbl, weight = x
            if schema is None:
                schema = tbl.schema
            try:
                if len(tbl) == 0:
                    continue
                assert isinstance(tbl, pa.Table)
                features = columns_to_features(tbl.schema.names)
                yield self._postprocess_table(features, tbl)
                safe_incr("chalk.snowflake.downloaded_bytes", tbl.nbytes or 0)
                safe_incr("chalk.snowflake.downloaded_rows", tbl.num_rows or 0)
                yielded = True
            finally:
                # Releasing the semaphore post-yield to better respect the limit
                if sem is not None and weight > 0:
                    sem.release(weight)
                    safe_set_gauge("chalk.snowflake.remaining_prefetch_bytes", sem.get_value())
        if not yielded and query_execution_parameters.yield_empty_batches:
            if schema is not None:
                features = columns_to_features(schema.names)
                yield pa.RecordBatch.from_arrays(
                    arrays=[[] for _ in features],
                    names=[x.root_fqn for x in features.values()],
                )
                return
            elif empty_batch_with_schema is not None:
                features = columns_to_features(empty_batch_with_schema.schema.names)
                yield self._postprocess_table(features, empty_batch_with_schema)

    @classmethod
    def register_sqlalchemy_compiler_overrides(cls):
        try:
            from chalk.sql._internal.integrations.snowflake_compiler_overrides import register_snowflake_compiler_hooks
        except ImportError:
            raise missing_dependency_exception("chalkpy[snowflake]")
        register_snowflake_compiler_hooks()

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_SNOWFLAKE_ACCOUNT_ID_NAME, self.name, self.account_identifier),
                create_integration_variable(_SNOWFLAKE_WAREHOUSE_NAME, self.name, self.warehouse),
                create_integration_variable(_SNOWFLAKE_USER_NAME, self.name, self.user),
                create_integration_variable(_SNOWFLAKE_PASSWORD_NAME, self.name, self.password),
                create_integration_variable(_SNOWFLAKE_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_SNOWFLAKE_SCHEMA_NAME, self.name, self.schema),
                create_integration_variable(_SNOWFLAKE_ROLE_NAME, self.name, self.role),
                create_integration_variable(_SNOWFLAKE_PRIVATE_KEY_B64_NAME, self.name, self.private_key_b64),
            ]
            if v is not None
        }
