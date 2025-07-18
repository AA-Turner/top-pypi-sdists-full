from __future__ import annotations

import concurrent.futures
import contextlib
import dataclasses
import queue
import typing
import uuid
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Mapping, Optional, Sequence

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from pyarrow.fs import S3FileSystem

from chalk.clogging import chalk_logger
from chalk.features import Feature
from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.df_utils import pa_array_to_pl_series
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.threading import DEFAULT_IO_EXECUTOR, MultiSemaphore
from chalk.utils.tracing import safe_incr, safe_set_gauge, safe_trace

if TYPE_CHECKING:
    import sqlalchemy.types
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL

    try:
        from pyathena.connection import BaseCursor
        from pyathena.connection import Connection as AthenaConnection
    except ImportError:
        pass

_logger = get_logger(__name__)

_WorkerId = typing.NewType("_WorkerId", int)


@dataclasses.dataclass(frozen=True)
class AthenaResultHandle:
    uri: str
    compressed_size: int

    @property
    def estimated_uncompressed_size(self) -> int:
        # this is a (hopefully) conservative estimate.
        return self.compressed_size * 8

    def to_arrow(self, fs: S3FileSystem) -> pa.Table:
        import pyarrow.dataset

        dataset = pyarrow.dataset.dataset(self.uri, format="parquet", filesystem=fs)
        return dataset.to_table()


_ATHENA_AWS_REGION_NAME = "ATHENA_AWS_REGION"
_ATHENA_AWS_ACCESS_KEY_ID_NAME = "ATHENA_AWS_ACCESS_KEY_ID"
_ATHENA_AWS_ACCESS_KEY_SECRET_NAME = "ATHENA_AWS_ACCESS_KEY_SECRET"
_ATHENA_S3_STAGING_DIR_NAME = "ATHENA_S3_STAGING_DIR"
_ATHENA_ROLE_ARN_NAME = "ATHENA_ROLE_ARN"
_ATHENA_SCHEMA_NAME_NAME = "ATHENA_SCHEMA_NAME"
_ATHENA_CATALOG_NAME_NAME = "ATHENA_CATALOG_NAME"
_ATHENA_WORK_GROUP_NAME = "ATHENA_WORK_GROUP"


def _sqlalchemy_to_athena_str_type(typ: sqlalchemy.types.TypeEngine) -> str:
    try:
        import sqlalchemy.types
    except ModuleNotFoundError:
        raise missing_dependency_exception("chalkpy[athena]")
    # Only some types are needed: pushdown can only happen for strings, ints, and bools
    if isinstance(typ, sqlalchemy.types.String):
        return "string"
    elif isinstance(typ, sqlalchemy.types.Text):
        return "string"
    elif isinstance(typ, sqlalchemy.types.Integer):
        return "integer"
    elif isinstance(typ, sqlalchemy.types.BigInteger):
        return "bigint"
    elif isinstance(typ, sqlalchemy.types.Boolean):
        return "boolean"
    else:
        raise ValueError(f"Unsupported SQLAlchemy type for Athena pushdown: {typ}")


class AthenaSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.athena

    def __init__(
        self,
        *,
        name: str | None = None,
        aws_region: str | None = None,
        aws_access_key_id: str | None = None,
        aws_access_key_secret: str | None = None,
        s3_staging_dir: str | None = None,
        schema_name: str | None = None,
        catalog_name: str | None = None,
        work_group: str | None = None,
        role_arn: str | None = None,
        engine_args: Dict[str, Any] | None = None,
        executor: Optional[concurrent.futures.ThreadPoolExecutor] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import pyathena
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")
        else:
            del pyathena  # unused here

        self.aws_region = aws_region or load_integration_variable(
            integration_name=name, name=_ATHENA_AWS_REGION_NAME, override=integration_variable_override
        )
        self.aws_access_key_id = aws_access_key_id or load_integration_variable(
            integration_name=name, name=_ATHENA_AWS_ACCESS_KEY_ID_NAME, override=integration_variable_override
        )
        self.aws_access_key_secret = aws_access_key_secret or load_integration_variable(
            integration_name=name, name=_ATHENA_AWS_ACCESS_KEY_SECRET_NAME, override=integration_variable_override
        )
        self.s3_staging_dir = s3_staging_dir or load_integration_variable(
            integration_name=name, name=_ATHENA_S3_STAGING_DIR_NAME, override=integration_variable_override
        )
        self.role_arn = role_arn or load_integration_variable(
            integration_name=name, name=_ATHENA_ROLE_ARN_NAME, override=integration_variable_override
        )
        self.schema_name = schema_name or load_integration_variable(
            integration_name=name, name=_ATHENA_SCHEMA_NAME_NAME, override=integration_variable_override
        )
        self.catalog_name = catalog_name or load_integration_variable(
            integration_name=name, name=_ATHENA_CATALOG_NAME_NAME, override=integration_variable_override
        )
        self.work_group = work_group or load_integration_variable(
            integration_name=name, name=_ATHENA_WORK_GROUP_NAME, override=integration_variable_override
        )
        self.executor = executor or DEFAULT_IO_EXECUTOR

        self._cached_s3_client = None
        self._s3_client_expiration = None

        self._cached_s3_filesystem = None
        self._s3_filesystem_expiration = None
        self._s3fs_lock = Lock()

        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault("connect_args", {"s3_staging_dir": s3_staging_dir})

        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    def _pyathena_connection(self) -> AthenaConnection:
        try:
            from pyathena.arrow.async_cursor import AsyncArrowCursor
            from pyathena.connection import Connection as AthenaConnection
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")
        return AthenaConnection(
            s3_staging_dir=self.s3_staging_dir,
            role_arn=self.role_arn,
            schema_name=self.schema_name or "default",
            catalog_name=self.catalog_name or "awsdatacatalog",
            work_group=self.work_group,
            region_name=self.aws_region,
            access_key=self.aws_access_key_id,
            secret_key=self.aws_access_key_secret,
            cursor_class=AsyncArrowCursor,
        )

    def supports_inefficient_fallback(self) -> bool:
        return False

    def get_sqlglot_dialect(self) -> str | None:
        # Athena was introduced to sqlglot in v22.3.0: it does seem sqlglot version changes have historically
        # broken query pushdown so defer to trino for now
        return "trino"

    def _create_s3_client(self):
        import boto3

        assumed_aws_client_id = None
        assumed_aws_client_secret = None
        assumed_session_token = None
        if self.role_arn:
            _logger.debug(
                f"Attempting to assume arn {self.role_arn=}, (aws region override = {self.aws_region}) with a web identity"
            )
            sts_client = boto3.client("sts")
            response = sts_client.assume_role(RoleArn=self.role_arn, RoleSessionName="chalk-athena-s3-assume")
            if not response or "Credentials" not in response:
                raise ValueError(f"Failed to assume role in sts client: {self.role_arn}")
            assumed_aws_client_id = response["Credentials"]["AccessKeyId"]
            assumed_aws_client_secret = response["Credentials"]["SecretAccessKey"]
            assumed_session_token = response["Credentials"]["SessionToken"]
            if "Expiration" in response["Credentials"]:
                self._s3_client_expiration = response["Credentials"]["Expiration"]

        self._cached_s3_client = boto3.client(
            "s3",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id or assumed_aws_client_id,
            aws_secret_access_key=self.aws_access_key_secret or assumed_aws_client_secret,
            aws_session_token=assumed_session_token,
        )

    @property
    def _s3_client(self):
        if (
            self._cached_s3_client is None
            or self._s3_client_expiration is None
            or self._s3_client_expiration < datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        ):
            self._create_s3_client()
        assert self._cached_s3_client is not None
        return self._cached_s3_client

    def _create_s3_filesystem(self):
        import boto3

        assumed_aws_client_id = None
        assumed_aws_client_secret = None
        assumed_session_token = None
        if self.role_arn:
            _logger.debug(
                f"Attempting to assume arn {self.role_arn=}, (aws region override = {self.aws_region}) with a web identity"
            )
            sts_client = boto3.client("sts")
            response = sts_client.assume_role(RoleArn=self.role_arn, RoleSessionName="chalk-athena-s3-assume")
            if not response or "Credentials" not in response:
                raise ValueError(f"Failed to assume role in sts client: {self.role_arn}")
            assumed_aws_client_id = response["Credentials"]["AccessKeyId"]
            assumed_aws_client_secret = response["Credentials"]["SecretAccessKey"]
            assumed_session_token = response["Credentials"]["SessionToken"]
            if "Expiration" in response["Credentials"]:
                self._s3_filesystem_expiration = response["Credentials"]["Expiration"]

        self._cached_s3_filesystem = S3FileSystem(
            region=self.aws_region,
            access_key=self.aws_access_key_id or assumed_aws_client_id,
            secret_key=self.aws_access_key_secret or assumed_aws_client_secret,
            session_token=assumed_session_token,
        )

    def _s3_filesystem(self):
        with self._s3fs_lock:
            if (
                self._cached_s3_filesystem is None
                or self._s3_filesystem_expiration is None
                or self._s3_filesystem_expiration < datetime.now(tz=timezone.utc) + timedelta(minutes=5)
            ):
                self._create_s3_filesystem()
            assert self._cached_s3_filesystem is not None
            return self._cached_s3_filesystem

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        query = {
            k: v
            for k, v in {
                "s3_staging_dir": self.s3_staging_dir,
                "role_arn": self.role_arn,
                "work_group": self.work_group,
                "unload": "true",
            }.items()
            if v is not None
        }
        # https://laughingman7743.github.io/PyAthena/sqlalchemy.html
        return URL.create(
            drivername="awsathena+arrow",
            username=self.aws_access_key_id,
            password=self.aws_access_key_secret,
            host=f"athena.{self.aws_region}.amazonaws.com",
            port=443,
            database=self.schema_name,
            query=query,
        )

    @staticmethod
    def _rewrite_query_for_unload(sql: str, s3_staging_dir_for_job: str):
        rewritten_sql = sql.rstrip(";\n ")
        new_query = f"""
        UNLOAD ({rewritten_sql}) TO '{s3_staging_dir_for_job}' WITH (format = 'PARQUET', compression = 'SNAPPY')
        """
        return new_query

    @contextlib.contextmanager
    def _create_athena_external_table(
        self,
        ext_table_name: str,
        ext_table_columns: Dict[str, str],
        pa_table: pa.Table,
        cursor: BaseCursor,
    ):
        try:
            from pyathena.arrow.result_set import AthenaArrowResultSet
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")
        # Instead of creating temporary tables, we will upload parquets into a temporary S3 location
        assert self.s3_staging_dir is not None, "s3_staging_dir must be set to create external tables in Athena"
        external_table_folder = self.s3_staging_dir.rstrip("/") + "/chalk_external_tables/"
        chalk_logger.info(
            f"Creating external table {ext_table_name} for Athena unload query at {external_table_folder}"
        )
        tmp_table_storage_location = f"{external_table_folder.rstrip('/')}/{ext_table_name}/"

        pq.write_table(
            pa_table,
            f"{tmp_table_storage_location.rstrip('/').lstrip('s3://')}/data.parquet",
            filesystem=self._s3_filesystem(),
        )

        ext_table_sql = f"""
                    CREATE EXTERNAL TABLE {ext_table_name} (
                        {", ".join(f"{col_name} {col_type}" for col_name, col_type in ext_table_columns.items())}
                    )
                    STORED AS PARQUET
                    LOCATION '{tmp_table_storage_location}'
                    """
        with safe_trace("athena.create_external_table"):
            ext_table_query_id, ext_table_query_fut = cursor.execute(ext_table_sql)
            chalk_logger.info(f"Creating external table: {ext_table_sql}, Query ID: {ext_table_query_id}")
            ext_table_query_result = ext_table_query_fut.result()
        assert isinstance(
            ext_table_query_result, AthenaArrowResultSet
        ), "Expected athena query result to be AthenaArrowResultSet"
        if (
            ext_table_query_result.error_type
            and ext_table_query_result.error_category
            and ext_table_query_result.error_message
        ):
            chalk_logger.error(
                f"Failed to execute create external Athena table to join on. Error info: Type: {ext_table_query_result.error_type}, Category: {ext_table_query_result.error_category}, Message: {ext_table_query_result.error_message}"
            )
            raise ValueError(
                f"Failed to execute create external Athena table to join on. Error info: Type: {ext_table_query_result.error_type}, Category: {ext_table_query_result.error_category}, Message: {ext_table_query_result.error_message}"
            )
        chalk_logger.info(f"Created external table {ext_table_name} successfully")
        try:
            yield
        finally:
            chalk_logger.info(f"Dropping external table {ext_table_name} after use")
            drop_ext_table_sql = f"DROP TABLE IF EXISTS {ext_table_name}"

            with safe_trace("athena.drop_external_table"):
                drop_ext_table_query_id, drop_ext_table_query_fut = cursor.execute(drop_ext_table_sql)
                chalk_logger.info(f"Dropping external table: {drop_ext_table_sql}, Query ID: {drop_ext_table_query_id}")
                drop_ext_table_query_result = drop_ext_table_query_fut.result()
            assert isinstance(
                drop_ext_table_query_result, AthenaArrowResultSet
            ), "Expected athena query result to be AthenaArrowResultSet"
            if (
                drop_ext_table_query_result.error_type
                and drop_ext_table_query_result.error_category
                and drop_ext_table_query_result.error_message
            ):
                chalk_logger.warning(
                    f"Failed to drop external Athena table {ext_table_name} after use. Error info: Type: {drop_ext_table_query_result.error_type}, Category: {drop_ext_table_query_result.error_category}, Message: {drop_ext_table_query_result.error_message}"
                )

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        with safe_trace("athena.execute_query_efficient"):
            try:
                from pyathena.arrow.result_set import AthenaArrowResultSet
            except ModuleNotFoundError:
                raise missing_dependency_exception("chalkpy[athena]")

            if self.s3_staging_dir is None:
                raise ValueError("Could not query Athena, no s3_staging_dir set")

            formatted_op, positional_params, named_params = self.compile_query(finalized_query)
            assert (
                len(positional_params) == 0 or len(named_params) == 0
            ), "Should not mix positional and named parameters"
            execution_params = None
            paramstyle = None
            if len(positional_params) > 0:
                execution_params = list(positional_params)
                if not all(isinstance(x, str) for x in positional_params):
                    raise ValueError("Only strings are allowed as positional parameters in Athena client")
            elif len(named_params) > 0:
                execution_params = named_params
                paramstyle = "named"
            result_handles: queue.Queue[
                AthenaResultHandle
            ] = queue.Queue()  # Using a queue since we'll be concurrently reading
            with self._pyathena_connection().cursor() as cursor:
                job_id = str(uuid.uuid4())
                job_prefix = f"chalk-unload/{job_id}"
                s3_prefix = f"{self.s3_staging_dir.rstrip('/')}/{job_prefix}"

                final_sql = self._rewrite_query_for_unload(
                    sql=formatted_op,
                    s3_staging_dir_for_job=s3_prefix,
                )
                with contextlib.ExitStack() as exit_stack:
                    for (
                        ext_table_name,
                        (ext_table_columns, ext_pa_table, _, _, _),
                    ) in finalized_query.temp_tables.items():
                        exit_stack.enter_context(
                            self._create_athena_external_table(
                                ext_table_name,
                                ext_table_columns={
                                    k: _sqlalchemy_to_athena_str_type(v) for k, v in ext_table_columns.items()
                                },
                                pa_table=ext_pa_table,
                                cursor=cursor,
                            )
                        )
                    query_id, query_fut = cursor.execute(
                        operation=final_sql,
                        parameters=execution_params,
                        paramstyle=paramstyle,
                    )

                    query_result = query_fut.result()
                    assert isinstance(
                        query_result, AthenaArrowResultSet
                    ), "Expected athena query result to be AthenaArrowResultSet"
                    if query_result.error_type and query_result.error_category and query_result.error_message:
                        chalk_logger.error(
                            f"Failed to execute Athena unload query. Error info: Type: {query_result.error_type}, Category: {query_result.error_category}, Message: {query_result.error_message}"
                        )
                        raise ValueError(
                            f"Failed to execute Athena unload query. Error info: Type: {query_result.error_type}, Category: {query_result.error_category}, Message: {query_result.error_message}"
                        )

                    chalk_logger.info(
                        f"Executed Athena unload query successfully. Query ID: {query_id}",
                    )
                    bucket_name = s3_prefix.split("/")[2]
                    remaining_prefix = "/".join(s3_prefix.split("/")[3:])
                    objects_list_response = self._s3_client.list_objects_v2(Bucket=bucket_name, Prefix=remaining_prefix)
                    if "Contents" not in objects_list_response:
                        chalk_logger.warning(
                            f"Failed to enumerate unloaded files for Athena query with query ID: {query_id}. This may mean there was no data to unload."
                        )
                        # Without any unloaded files, we cannot determine the schema of the output, so even if
                        # yield_empty_batches is True, we do not yield anything
                        return

                    chalk_logger.info(f"Found {len(objects_list_response['Contents'])} unloaded files")
                    for object in objects_list_response["Contents"]:
                        if "Key" not in object or "Size" not in object:
                            raise ValueError(f"Expected 'Key' and 'Size' in Athena unload response: {object}")
                        object_key = object["Key"]
                        chalk_logger.info(f"Found unloaded file: {object_key}")
                        result_handles.put_nowait(
                            AthenaResultHandle(uri=f"{bucket_name}/{object_key}", compressed_size=object["Size"])
                        )

                    yield from self._yield_from_result_handles(
                        result_handles=result_handles,
                        query_execution_parameters=query_execution_parameters,
                        columns_to_features=columns_to_features,
                    )

    def _postprocess_table(self, features: Mapping[str, Feature], tbl: pa.Table):
        columns: list[pa.Array] = []
        column_names: list[str] = []
        chalk_logger.info(
            f"Received a PyArrow table from Athena with {len(tbl)} rows; {len(tbl.column_names)} columns; {tbl.nbytes=}; {tbl.schema=}"
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
        result_handles: queue.Queue[AthenaResultHandle],
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
                if sem:
                    if weight > sem.initial_value:
                        # If the file is larger than the maximum size, we'll truncate it, so this file will be the only one being downloaded
                        weight = sem.initial_value
                    if weight > 0:
                        # No need to acquire the semaphore for empty tables
                        if not sem.acquire(weight):
                            raise RuntimeError("Failed to acquire semaphore for reading athena unload")
                        safe_set_gauge("chalk.athena.remaining_prefetch_bytes", sem.get_value())
                if as_arrow is None:
                    as_arrow = x.to_arrow(self._s3_filesystem())
                pa_table_queue.put((as_arrow, weight))
        finally:
            # At the end, putting the worker id to signal that this worker is done
            pa_table_queue.put(worker_idx)

    def _yield_from_result_handles(
        self,
        result_handles: queue.Queue[AthenaResultHandle],
        query_execution_parameters: QueryExecutionParameters,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
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
                safe_incr("chalk.athena.downloaded_bytes", tbl.nbytes or 0)
                safe_incr("chalk.athena.downloaded_rows", tbl.num_rows or 0)
                yielded = True
            finally:
                # Releasing the semaphore post-yield to better respect the limit
                if sem is not None and weight > 0:
                    sem.release(weight)
                    safe_set_gauge("chalk.athena.remaining_prefetch_bytes", sem.get_value())
        if not yielded and query_execution_parameters.yield_empty_batches:
            if schema is not None:
                features = columns_to_features(schema.names)
                yield pa.RecordBatch.from_arrays(
                    arrays=[[] for _ in features],
                    names=[x.root_fqn for x in features.values()],
                )
                return

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_ATHENA_AWS_REGION_NAME, self.name, self.aws_region),
                create_integration_variable(_ATHENA_AWS_ACCESS_KEY_ID_NAME, self.name, self.aws_access_key_id),
                create_integration_variable(_ATHENA_AWS_ACCESS_KEY_SECRET_NAME, self.name, self.aws_access_key_secret),
                create_integration_variable(_ATHENA_S3_STAGING_DIR_NAME, self.name, self.s3_staging_dir),
                create_integration_variable(_ATHENA_ROLE_ARN_NAME, self.name, self.role_arn),
                create_integration_variable(_ATHENA_SCHEMA_NAME_NAME, self.name, self.schema_name),
                create_integration_variable(_ATHENA_CATALOG_NAME_NAME, self.name, self.catalog_name),
                create_integration_variable(_ATHENA_WORK_GROUP_NAME, self.name, self.work_group),
            ]
            if v is not None
        }
