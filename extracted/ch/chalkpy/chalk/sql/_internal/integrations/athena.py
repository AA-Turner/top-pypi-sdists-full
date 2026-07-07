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
from chalk.utils.pl_helpers import str_json_decode_compat
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


@dataclasses.dataclass(frozen=True)
class DetectedQuerySchema:
    """
    Result of detecting schema from a SQL query via LIMIT 0 pattern.

    This is used for the Iceberg timestamp workaround to identify which columns
    need VARCHAR casting before UNLOAD operations.
    """

    timestamp_columns: set[str]
    """Set of column names that have timestamp types"""

    column_names: list[str]
    """Ordered list of all column names in the query result"""

    schema: dict[str, pa.DataType]
    """Mapping of column names to PyArrow types"""


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
        permission_tags: list[str] | None = None,
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

        BaseSQLSource.__init__(
            self, name=name, engine_args=engine_args, async_engine_args={}, permission_tags=permission_tags
        )

    def _pyathena_connection(self) -> AthenaConnection:
        try:
            from pyathena.arrow.async_cursor import AsyncArrowCursor
            from pyathena.connection import Connection as AthenaConnection
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")
        return AthenaConnection(
            s3_staging_dir=self.s3_staging_dir,
            role_arn=self.role_arn,
            schema_name=self.active_schema,
            catalog_name=self.active_catalog,
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

    @property
    def active_catalog(self) -> str:
        return self.catalog_name or "awsdatacatalog"

    @property
    def active_schema(self) -> str:
        return self.schema_name or "default"

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

    def _execute_unload_and_list_s3_results(
        self,
        cursor: BaseCursor,
        sql: str,
        execution_params: Any = None,
        paramstyle: Optional[str] = None,
    ) -> tuple[str, list[AthenaResultHandle]]:
        """
        Execute an UNLOAD query and list the resulting S3 files.

        This is the core UNLOAD execution pattern shared by all Athena query paths.

        Args:
            cursor: The PyAthena cursor to execute with
            sql: The SQL query (already wrapped in UNLOAD)
            execution_params: Optional query parameters
            paramstyle: Optional parameter style ('named' or positional)

        Returns:
            A tuple of (query_id, list of result handles)
        """
        try:
            from pyathena.arrow.result_set import AthenaArrowResultSet
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")

        query_id, query_fut = cursor.execute(
            operation=sql,
            parameters=execution_params,
            paramstyle=paramstyle,
        )

        query_result = query_fut.result()
        assert isinstance(query_result, AthenaArrowResultSet), "Expected athena query result to be AthenaArrowResultSet"

        if query_result.error_type and query_result.error_category and query_result.error_message:
            chalk_logger.error(
                f"Failed to execute Athena unload query. Error info: Type: {query_result.error_type}, "
                + f"Category: {query_result.error_category}, Message: {query_result.error_message}"
            )
            raise ValueError(
                f"Failed to execute Athena unload query. Error info: Type: {query_result.error_type}, "
                + f"Category: {query_result.error_category}, Message: {query_result.error_message}"
            )

        chalk_logger.info(f"Executed Athena unload query successfully. Query ID: {query_id}")

        # Extract S3 prefix from the UNLOAD query to determine where files were written
        # The UNLOAD query contains: UNLOAD (...) TO 's3://bucket/prefix/' WITH (...)
        # We need to extract the S3 prefix to list the files
        import re

        match = re.search(r"TO\s+'(s3://[^']+)'", sql, re.IGNORECASE)
        if not match:
            raise ValueError(f"Could not extract S3 prefix from UNLOAD query: {sql}")

        s3_prefix = match.group(1)
        bucket_name = s3_prefix.split("/")[2]
        remaining_prefix = "/".join(s3_prefix.split("/")[3:])

        objects_list_response = self._s3_client.list_objects_v2(Bucket=bucket_name, Prefix=remaining_prefix)

        if "Contents" not in objects_list_response:
            chalk_logger.warning(
                f"No unloaded files found for Athena query with query ID: {query_id}. "
                + "This may mean there was no data to unload."
            )
            return query_id, []

        chalk_logger.info(f"Found {len(objects_list_response['Contents'])} unloaded files")

        result_handles = []
        for obj in objects_list_response["Contents"]:
            if "Key" not in obj or "Size" not in obj:
                raise ValueError(f"Expected 'Key' and 'Size' in Athena unload response: {obj}")
            object_key = obj["Key"]
            chalk_logger.info(f"Found unloaded file: {object_key}")
            result_handles.append(AthenaResultHandle(uri=f"{bucket_name}/{object_key}", compressed_size=obj["Size"]))

        return query_id, result_handles

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        with safe_trace("athena.execute_query_efficient"):
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

            with self._pyathena_connection().cursor() as cursor:
                with contextlib.ExitStack() as exit_stack:
                    # Create temp tables FIRST (before schema detection)
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

                    # NOW run schema detection (after temp tables exist)
                    final_sql, _ = self._prepare_query_for_unload(
                        sql=formatted_op,
                        cursor=cursor,
                        schema=None,  # Detect schema from SQL
                        execution_params=execution_params,
                        paramstyle=paramstyle,
                    )

                    # Use the common UNLOAD execution pattern
                    _query_id, result_handles_list = self._execute_unload_and_list_s3_results(
                        cursor=cursor,
                        sql=final_sql,
                        execution_params=execution_params,
                        paramstyle=paramstyle,
                    )

                    if not result_handles_list:
                        # No results to process
                        return

                    # Convert list to queue for the existing downstream code
                    result_handles: queue.Queue[AthenaResultHandle] = queue.Queue()
                    for handle in result_handles_list:
                        result_handles.put_nowait(handle)

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
                        column = (
                            str_json_decode_compat(series, feature.converter.polars_dtype)
                            .to_arrow()
                            .cast(expected_type)
                        )
                if actual_type != expected_type:
                    # Special handling for VARCHAR -> timezone-aware timestamp conversion
                    # This occurs when we apply the Iceberg timestamp workaround
                    if (
                        (pa.types.is_string(actual_type) or pa.types.is_large_string(actual_type))
                        and pa.types.is_timestamp(expected_type)
                        and expected_type.tz is not None
                    ):
                        # Athena timestamps are timezone-naive but assumed to be UTC
                        # Cast to timezone-naive timestamp first, then assume timezone
                        naive_type = pa.timestamp(expected_type.unit)
                        column = column.cast(naive_type)
                        column = pc.assume_timezone(column, expected_type.tz)  # type: ignore[reportGeneralTypeIssues]
                    else:
                        column = column.cast(
                            options=pc.CastOptions(target_type=expected_type, allow_time_truncate=True)
                        )
                if isinstance(column, pa.ChunkedArray):
                    column = column.combine_chunks()
                columns.append(column)
                column_names.append(feature.root_fqn)
            except:
                chalk_logger.error(f"Failed to deserialize column '{col_name}' into '{feature}'", exc_info=True)
                raise

        return pa.RecordBatch.from_arrays(arrays=columns, names=column_names)

    def _postprocess_batch_to_schema(
        self, batch: pa.RecordBatch, expected_schema: Mapping[str, pa.DataType]
    ) -> pa.RecordBatch:
        """
        Post-process a RecordBatch to match the expected schema.

        This is similar to _postprocess_table but works with RecordBatches and
        schema dicts instead of Tables and Features. Used by the engine ChalkSQL path.

        Handles:
        - VARCHAR -> timestamp conversion (for Iceberg timestamp workaround)
        - Other type mismatches

        Args:
            batch: RecordBatch to post-process
            expected_schema: Expected schema mapping column names to PyArrow types

        Returns:
            RecordBatch with columns converted to expected types
        """
        # Check if we need any conversions
        needs_conversion = False
        for col_name in expected_schema:
            if col_name in batch.schema.names:
                actual_type = batch.schema.field(col_name).type
                expected_type = expected_schema[col_name]
                if actual_type != expected_type:
                    needs_conversion = True
                    break

        if not needs_conversion:
            return batch

        # Build new arrays with converted types
        new_arrays = []
        new_fields = []

        for i, field in enumerate(batch.schema):
            col_name = field.name
            column_array = batch.column(i)

            # If column not in expected schema, keep as-is
            if col_name not in expected_schema:
                new_arrays.append(column_array)
                new_fields.append(field)
                continue

            expected_type = expected_schema[col_name]
            actual_type = field.type

            # Types match, no conversion needed
            if actual_type == expected_type:
                new_arrays.append(column_array)
                new_fields.append(field)
                continue

            # Handle VARCHAR -> timestamp/date conversion (Iceberg workaround)
            if (pa.types.is_string(actual_type) or pa.types.is_large_string(actual_type)) and (
                pa.types.is_timestamp(expected_type) or pa.types.is_date(expected_type)
            ):
                if pa.types.is_timestamp(expected_type):
                    # Parse as timestamp using two-step cast
                    # Athena CAST(timestamp AS VARCHAR) always produces microsecond precision: '2023-01-03 14:30:00.123000'
                    # Step 1: Parse VARCHAR as timestamp[us] (to match the format)
                    # Step 2: Cast to expected unit (ms, s, etc.) if different, with truncation allowed

                    # First parse as timestamp[us] since Athena VARCHAR output has microsecond precision
                    parsed_timestamp = pc.cast(column_array, pa.timestamp("us"))

                    # Then cast to the expected unit if different
                    if expected_type.unit != "us":
                        timestamp_array = pc.cast(
                            parsed_timestamp,
                            options=pc.CastOptions(
                                target_type=pa.timestamp(expected_type.unit), allow_time_truncate=True
                            ),
                        )
                    else:
                        timestamp_array = parsed_timestamp

                    if expected_type.tz is not None:
                        # Timezone-aware timestamp: assume timezone on the parsed naive timestamps
                        converted = pc.assume_timezone(timestamp_array, expected_type.tz)  # type: ignore[reportGeneralTypeIssues]
                    else:
                        # Timezone-naive timestamp: use as-is
                        converted = timestamp_array
                elif pa.types.is_date(expected_type):
                    # Parse as date (date32 or date64)
                    # Cast VARCHAR directly to date type - PyArrow handles the parsing
                    converted = pc.cast(column_array, options=pc.CastOptions(target_type=expected_type))
                else:
                    raise ValueError(f"Unexpected expected_type for VARCHAR conversion: {expected_type}")

                new_arrays.append(converted)
                new_fields.append(pa.field(col_name, expected_type))
            else:
                # For other type mismatches, keep the column as-is
                # We only handle VARCHAR -> timestamp/date conversion above
                # Other conversions are left to downstream processing
                new_arrays.append(column_array)
                new_fields.append(field)

        return pa.RecordBatch.from_arrays(new_arrays, schema=pa.schema(new_fields))

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
                # Convert decimal columns to float64 for compatibility
                tbl = self._convert_decimals_to_float64_table(tbl)
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

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for Athena and return raw PyArrow RecordBatches."""
        import pyarrow.compute as pc

        with safe_trace("athena.execute_query_efficient_raw"):
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

                    # Use the shared UNLOAD execution pattern
                    _query_id, result_handles = self._execute_unload_and_list_s3_results(
                        cursor=cursor,
                        sql=final_sql,
                        execution_params=execution_params,
                        paramstyle=paramstyle,
                    )

                    if not result_handles:
                        # No data unloaded
                        if query_execution_parameters.yield_empty_batches:
                            arrays = [pa.nulls(0, field.type) for field in expected_output_schema]
                            batch = pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
                            yield batch
                        return

                    # Process unloaded files
                    for result_handle in result_handles:
                        # Download and process the file
                        tbl = result_handle.to_arrow(self._s3_filesystem())

                        if len(tbl) == 0:
                            continue

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

                        batch = pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
                        yield batch

    def list_db_schemas(self, db_schema_filter_pattern: str | None = None) -> list[str]:
        """
        List available schemas in the configured catalog.

        Args:
            db_schema_filter_pattern: Optional SQL LIKE pattern to filter schemas (case-insensitive).
                If None, returns all schemas.

        Returns:
            A list of schema names matching the filter criteria.
        """
        try:
            from pyathena.arrow.result_set import AthenaArrowResultSet
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")

        with self._pyathena_connection().cursor() as cursor:
            # Build WHERE clause based on filter pattern
            where_clause = ""
            if db_schema_filter_pattern is not None:
                where_clause = f"WHERE LOWER(schema_name) LIKE LOWER('{db_schema_filter_pattern}')"

            # Query information_schema to get schema names
            query = f"""
            SELECT schema_name
            FROM "{self.active_catalog}".information_schema.schemata
            {where_clause}
            ORDER BY schema_name
            """

            _query_id, query_fut = cursor.execute(query)
            query_result = query_fut.result()

            assert isinstance(
                query_result, AthenaArrowResultSet
            ), "Expected athena query result to be AthenaArrowResultSet"

            if query_result.error_type and query_result.error_category and query_result.error_message:
                raise ValueError(
                    f"Failed to list schemas. Error info: Type: {query_result.error_type}, "
                    + f"Category: {query_result.error_category}, Message: {query_result.error_message}"
                )

            # Convert result to list of schema names
            schema_names = []
            as_arrow = query_result.as_arrow()
            if as_arrow and len(as_arrow) > 0:
                schema_names_column = as_arrow.column("schema_name")
                schema_names = [name.as_py() for name in schema_names_column]

            return schema_names

    def list_tables(
        self, db_schema_filter_pattern: str | None = None, table_name_filter_pattern: str | None = None
    ) -> list[tuple[str, str]]:
        """
        List available tables in the configured catalog and schema.

        Args:
            db_schema_filter_pattern: Optional SQL LIKE pattern to filter schemas.
                If None, uses the configured schema_name exactly.
            table_name_filter_pattern: Optional SQL LIKE pattern to filter table names.
                If None, returns all tables.

        Returns:
            A list of tuples (schema_name, table_name) matching the filter criteria.
        """
        try:
            from pyathena.arrow.result_set import AthenaArrowResultSet
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")

        with self._pyathena_connection().cursor() as cursor:
            # Build WHERE clause based on filter patterns
            where_conditions = []

            if db_schema_filter_pattern is not None:
                where_conditions.append(f"LOWER(table_schema) LIKE LOWER('{db_schema_filter_pattern}')")
            else:
                where_conditions.append(f"table_schema = '{self.active_schema}'")

            if table_name_filter_pattern is not None:
                where_conditions.append(f"LOWER(table_name) LIKE LOWER('{table_name_filter_pattern}')")

            where_clause = " AND ".join(where_conditions)

            # Query information_schema to get table and schema names
            query = f"""
            SELECT table_schema, table_name
            FROM "{self.active_catalog}".information_schema.tables
            WHERE {where_clause}
            ORDER BY table_schema, table_name
            """

            _query_id, query_fut = cursor.execute(query)
            query_result = query_fut.result()

            assert isinstance(
                query_result, AthenaArrowResultSet
            ), "Expected athena query result to be AthenaArrowResultSet"

            if query_result.error_type and query_result.error_category and query_result.error_message:
                raise ValueError(
                    f"Failed to list tables. Error info: Type: {query_result.error_type}, "
                    + f"Category: {query_result.error_category}, Message: {query_result.error_message}"
                )

            # Convert result to list of (schema_name, table_name) tuples
            tables = []
            as_arrow = query_result.as_arrow()
            if as_arrow and len(as_arrow) > 0:
                schema_column = as_arrow.column("table_schema")
                table_column = as_arrow.column("table_name")
                tables = [(schema_column[i].as_py(), table_column[i].as_py()) for i in range(len(as_arrow))]

            return tables

    def get_table_schema(self, table_name: str, catalog: str | None = None, schema: str | None = None) -> pa.Schema:
        """
        Get the schema of a table as a PyArrow schema.

        Args:
            table_name: The name of the table
            catalog: The catalog name. If None, uses the configured catalog_name.
            schema: The schema name. If None, uses the configured schema_name.

        Returns:
            A PyArrow schema representing the table's structure
        """
        try:
            from pyathena.arrow.result_set import AthenaArrowResultSet
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[athena]")

        catalog = catalog or self.active_catalog
        schema = schema or self.active_schema

        with self._pyathena_connection().cursor() as cursor:
            # Query the table with LIMIT 0 to get schema without data
            # Need to fully qualify the table name with catalog and schema
            query = f'SELECT * FROM "{catalog}"."{schema}"."{table_name}" LIMIT 0'

            _query_id, query_fut = cursor.execute(query)
            query_result = query_fut.result()

            assert isinstance(
                query_result, AthenaArrowResultSet
            ), "Expected athena query result to be AthenaArrowResultSet"

            if query_result.error_type and query_result.error_category and query_result.error_message:
                raise ValueError(
                    f"Failed to get table schema. Error info: Type: {query_result.error_type}, "
                    + f"Category: {query_result.error_category}, Message: {query_result.error_message}"
                )

            # Extract the PyArrow schema directly from the result
            as_arrow = query_result.as_arrow()
            if as_arrow is None:
                raise ValueError(f"Table '{table_name}' not found in catalog '{catalog}', schema '{schema}'")

            return as_arrow.schema

    def _detect_timestamp_columns_from_sql(
        self,
        sql: str,
        cursor: Any,
        execution_params: Any = None,
        paramstyle: str | None = None,
    ) -> DetectedQuerySchema:
        """
        Detect timestamp columns by executing a LIMIT 0 query to get the result schema.

        This determines the schema directly from the SQL query itself, which is more
        reliable than trying to parse query metadata or use FinalizedChalkQuery properties.

        Args:
            sql: The SQL query to analyze
            cursor: PyAthena cursor to execute the schema detection query
            execution_params: Optional query parameters (positional list or named dict)
            paramstyle: Optional parameter style ("named" for named parameters)

        Returns:
            DetectedQuerySchema containing timestamp columns, all column names, and schema dict
        """
        try:
            from pyathena.arrow.result_set import AthenaArrowResultSet
        except ModuleNotFoundError:
            raise ImportError("chalkpy[athena] is required")

        # Execute LIMIT 0 query to get schema without fetching data
        schema_sql = f"SELECT * FROM ({sql}) AS _chalk_schema_detection LIMIT 0"

        chalk_logger.debug(f"Detecting schema from SQL via LIMIT 0 query")

        # Pass parameters to cursor.execute if provided
        if execution_params is not None:
            _query_id, query_fut = cursor.execute(
                schema_sql,
                parameters=execution_params,
                paramstyle=paramstyle,
            )
        else:
            _query_id, query_fut = cursor.execute(schema_sql)
        query_result = query_fut.result()

        assert isinstance(query_result, AthenaArrowResultSet), "Expected athena query result to be AthenaArrowResultSet"

        if query_result.error_type and query_result.error_category and query_result.error_message:
            raise ValueError(
                f"Failed to detect schema from Athena query. Error info: Type: {query_result.error_type}, "
                + f"Category: {query_result.error_category}, Message: {query_result.error_message}"
            )

        # Get the PyArrow schema from the result - need to call as_arrow() first
        as_arrow = query_result.as_arrow()
        if as_arrow is None:
            raise ValueError("Failed to get Arrow table from query result")

        schema = as_arrow.schema

        # Extract timestamp columns, column names, and build schema dict
        # Note: We include both DATE and TIMESTAMP columns in the VARCHAR cast workaround
        # since DATE columns may also be affected by Iceberg UNLOAD precision issues
        timestamp_columns = set()
        column_names = []
        schema_dict: dict[str, pa.DataType] = {}

        for field in schema:
            column_names.append(field.name)
            schema_dict[field.name] = field.type
            if pa.types.is_timestamp(field.type) or pa.types.is_date(field.type):
                timestamp_columns.add(field.name)
                chalk_logger.debug(f"Detected timestamp/date column '{field.name}' with type {field.type}")

        chalk_logger.info(
            f"Detected {len(timestamp_columns)} timestamp/date columns out of {len(column_names)} total columns: {timestamp_columns}"
        )

        return DetectedQuerySchema(timestamp_columns=timestamp_columns, column_names=column_names, schema=schema_dict)

    def wrap_query_with_timestamp_varchar_casts(
        self,
        sql: str,
        column_names: Sequence[str],
        timestamp_columns: set[str],
    ) -> str:
        """
        Wrap a SQL query in a subquery that casts timestamp columns to VARCHAR.

        This works around Athena's timestamp precision limitation with Iceberg tables.
        Instead of parsing the SQL, we wrap it in a subquery and apply CAST in the
        outer SELECT, which works for any valid SQL query.

        This method is used by both chalkpy direct queries and engine ChalkSQL queries.

        Args:
            sql: The original SQL query
            column_names: Ordered list of column names in the result
            timestamp_columns: Set of column names that are timestamps

        Returns:
            Modified SQL with timestamp columns cast to VARCHAR, or original SQL if no timestamps
        """
        if not timestamp_columns:
            return sql

        chalk_logger.info(
            f"Wrapping Athena query with VARCHAR casts for {len(timestamp_columns)} timestamp columns "
            + "to work around Iceberg timestamp(6) precision issue"
        )

        # Build SELECT list with casts for timestamp columns
        select_items = []
        for col_name in column_names:
            # Escape column names with double quotes for Athena/Trino
            escaped_name = col_name.replace('"', '""')

            if col_name in timestamp_columns:
                # Cast timestamp to VARCHAR to avoid precision mismatch
                select_items.append(f'CAST("{escaped_name}" AS VARCHAR) AS "{escaped_name}"')
            else:
                select_items.append(f'"{escaped_name}"')

        # Wrap the original query in a subquery
        wrapped_sql = f"""
SELECT {", ".join(select_items)}
FROM (
{sql}
) AS _chalk_timestamp_cast_subquery
"""
        return wrapped_sql

    def _prepare_query_for_unload(
        self,
        sql: str,
        cursor: Any,
        schema: Mapping[str, pa.DataType] | None = None,
        execution_params: Any = None,
        paramstyle: str | None = None,
    ) -> tuple[str, DetectedQuerySchema]:
        """
        Prepare a SQL query for UNLOAD by detecting schema and wrapping with VARCHAR casts.

        This consolidates the common preparation logic used by both chalkpy direct queries
        and engine ChalkSQL queries. It handles:
        1. Schema detection (if not provided) or extraction (if provided)
        2. Wrapping query with VARCHAR casts for timestamp columns
        3. Creating S3 job prefix and path
        4. Rewriting query for UNLOAD

        Args:
            sql: The SQL query to prepare
            cursor: PyAthena cursor for schema detection
            schema: Optional pre-known schema mapping (column name -> PyArrow type)
            execution_params: Optional query parameters (positional list or named dict)
            paramstyle: Optional parameter style ("named" for named parameters)

        Returns:
            Tuple of (final_unload_sql, detected_schema)
                - final_unload_sql: The rewritten UNLOAD SQL ready to execute
                - detected_schema: DetectedQuerySchema with timestamp columns, column names, and schema dict
        """
        if self.s3_staging_dir is None:
            raise ValueError("s3_staging_dir must be set to use Athena UNLOAD")

        # Step 1: ALWAYS detect timestamp columns from SQL, not from provided schema
        # The provided schema might have wrong types (e.g., strings instead of timestamps)
        # if a previous conversion failed. Detecting from SQL gives us the true Athena types.
        chalk_logger.debug(f"Detecting timestamp columns from SQL query. Provided schema: {schema is not None}")
        detected_schema = self._detect_timestamp_columns_from_sql(sql, cursor, execution_params, paramstyle)

        # Merge schemas if one was provided:
        # - Use detected schema to identify timestamp columns (for VARCHAR wrapping)
        # - But preserve timestamp precision from provided schema (for Iceberg timestamp(6) support)
        # The detected schema from LIMIT 0 returns timestamp[ms] for Iceberg timestamp(6) columns,
        # but we want to preserve the actual precision (timestamp[us]) if explicitly provided.
        if schema is not None:
            chalk_logger.debug(
                f"Schema provided with {len(schema)} columns. Merging with detected schema "
                + f"to preserve timestamp precision while using detected timestamp column identification."
            )
            # Build merged schema: use provided schema's types where available,
            # fall back to detected schema for missing columns
            merged_schema_dict = dict(detected_schema.schema)
            for col_name, col_type in schema.items():
                if col_name in merged_schema_dict:
                    merged_schema_dict[col_name] = col_type

            # Update detected_schema with merged types while keeping timestamp column identification
            detected_schema = DetectedQuerySchema(
                timestamp_columns=detected_schema.timestamp_columns,
                column_names=detected_schema.column_names,
                schema=merged_schema_dict,
            )

        # Step 2: Wrap query with VARCHAR casts for timestamp columns
        query_to_unload = sql
        if detected_schema.timestamp_columns and detected_schema.column_names:
            query_to_unload = self.wrap_query_with_timestamp_varchar_casts(
                sql, detected_schema.column_names, detected_schema.timestamp_columns
            )

        # Step 3: Create S3 job prefix and path
        job_id = str(uuid.uuid4())
        job_prefix = f"chalk-unload/{job_id}"
        s3_prefix = f"{self.s3_staging_dir.rstrip('/')}/{job_prefix}"

        # Step 4: Rewrite query for UNLOAD
        final_sql = self._rewrite_query_for_unload(
            sql=query_to_unload,
            s3_staging_dir_for_job=s3_prefix,
        )

        return final_sql, detected_schema

    def _convert_decimals_to_float64_table(self, tbl: pa.Table) -> pa.Table:
        """
        Convert decimal columns to float64 in a PyArrow Table.

        Decimal types are not well supported in some contexts (like ChalkSQL),
        so we convert them to float64. This may result in precision loss for
        very large or very precise decimal values.

        Args:
            tbl: PyArrow Table that may contain decimal columns

        Returns:
            PyArrow Table with decimal columns converted to float64
        """
        # Check if any columns are decimal types
        has_decimals = any(pa.types.is_decimal(field.type) for field in tbl.schema)
        if not has_decimals:
            return tbl

        # Build new schema with decimals converted to float64
        new_fields = []
        for field in tbl.schema:
            if pa.types.is_decimal(field.type):
                new_fields.append(pa.field(field.name, pa.float64()))
                chalk_logger.debug(f"Converting decimal column '{field.name}' with type {field.type} to float64")
            else:
                new_fields.append(field)

        new_schema = pa.schema(new_fields)

        # Convert decimal columns
        new_columns = []
        for i, field in enumerate(tbl.schema):
            column = tbl.column(i)
            if pa.types.is_decimal(field.type):
                try:
                    # Cast decimal to float64
                    float_column = column.cast(pa.float64())
                    new_columns.append(float_column)
                except Exception as e:
                    chalk_logger.warning(
                        f"Failed to convert decimal column '{field.name}' to float64: {e}. Keeping original type."
                    )
                    new_columns.append(column)
            else:
                new_columns.append(column)

        return pa.table(new_columns, schema=new_schema)

    @staticmethod
    def convert_decimals_to_float64_in_batch(batch: pa.RecordBatch) -> pa.RecordBatch:
        """
        Convert decimal columns to float64 in a PyArrow RecordBatch.

        This is a static method that can be used by the engine's ChalkSQL executor.
        Decimal types are not well supported in some contexts (like ChalkSQL),
        so we convert them to float64. This may result in precision loss.

        Args:
            batch: RecordBatch that may contain decimal columns

        Returns:
            RecordBatch with decimal columns converted to float64
        """
        # Check if any columns are decimal types
        has_decimals = any(pa.types.is_decimal(field.type) for field in batch.schema)
        if not has_decimals:
            return batch

        # Build new arrays with decimals converted to float64
        new_arrays = []
        new_fields = []

        for i, field in enumerate(batch.schema):
            column_array = batch.column(i)

            if pa.types.is_decimal(field.type):
                # Convert decimal to float64
                try:
                    float_array = column_array.cast(pa.float64())
                    new_arrays.append(float_array)
                    new_fields.append(pa.field(field.name, pa.float64()))
                except Exception as e:
                    chalk_logger.warning(
                        f"Failed to convert decimal column '{field.name}' to float64: {e}. Keeping original type."
                    )
                    new_arrays.append(column_array)
                    new_fields.append(field)
            else:
                # Keep non-decimal columns as-is
                new_arrays.append(column_array)
                new_fields.append(field)

        # Create new RecordBatch with converted arrays
        new_schema = pa.schema(new_fields)
        return pa.RecordBatch.from_arrays(new_arrays, schema=new_schema)

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
