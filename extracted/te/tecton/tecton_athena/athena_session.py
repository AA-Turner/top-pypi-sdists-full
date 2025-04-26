import dataclasses
import datetime
import hashlib
import json
import logging
import os
import secrets
import tempfile
import threading
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Union
from urllib.parse import urlparse

import boto3
import pandas

from tecton_athena.templates_utils import load_template
from tecton_core import conf
from tecton_core.arrow import PARQUET_WRITE_OPTIONS_KWARGS
from tecton_core.errors import TectonAthenaValidationError


logger = logging.getLogger(__name__)

# In some cases, strings in Pandas DF are actually represented as "object" types.
# Hence the sketchy 'object' -> 'string' map
PANDAS_TO_HIVE_TYPES = {
    "string": "string",
    "object": "string",
    "int64": "bigint",
    "float64": "double",
    "int32": "bigint",
}

S3_ATHENA_PANDAS_UPLOADS = "athena/pandas_uploads"

CREATE_TABLE_TEMPLATE = load_template("create_table.sql")


PARTITION_TYPE_DATESTR = "PARTITION_TYPE_DATESTR"
PARTITION_TYPE_UNIX_EPOCH_NS = "PARTITION_TYPE_UNIX_EPOCH_NS"
GLUE_CATALOG_TABLE_PROPERTY_HASH = "tecton_table_metadata_hash"
GLUE_CATALOG_TABLE_PROPERTY_SPEC_VERSION = "tecton_table_spec_version"


@dataclass
class AthenaTableCreationSpec:
    """Athena Table representation (registered in Glue)"""

    # SPEC_VERSION Explanation:
    # - The SDK will never overwrite a table registration that happened with a newer version
    # - Increment if you fundamentally change the way Athena tables, for an identical FeatureView, are registered
    #   For example, if you move away from partition projection
    # - The SPEC_VERSION must not be part of the stable_hash calculation - otherwise the SDK believes it needs to overwrite
    #   a table's registration, even if the metadata for that table is unchanged, just because the version is incremented
    # - A separate SPEC_VERSION is used here rather than relying on the SDK's version because most SDK versions will increment
    #   without ever incrementing the SPEC_VERSION here
    SPEC_VERSION = 1

    database: str
    table: str
    s3_location: str
    data_format: str
    columns: Dict[str, str]
    partition_by: str
    partition_by_type: str
    partition_by_format: str
    partition_by_range_from: str
    partition_by_range_to: str
    partition_by_interval: int
    partition_by_interval_timedelta: datetime.timedelta
    partition_type: Union[PARTITION_TYPE_DATESTR, PARTITION_TYPE_UNIX_EPOCH_NS]

    @property
    def _json_str(self):
        return json.dumps(
            dataclasses.asdict(self),
            default=str,
            sort_keys=True,
            indent=None,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")

    @property
    def stable_hash(self):
        str_representation = self._json_str
        return hashlib.md5(str_representation).hexdigest()


@dataclass
class AthenaSessionConfig:
    boto3_session: Optional[boto3.Session] = None
    workgroup: Optional[str] = None  # Athena workgroup.
    encryption: Optional[str] = None  # Valid values: [None, 'SSE_S3', 'SSE_KMS']. Notice: 'CSE_KMS' is not supported.
    kms_key: Optional[str] = None  # For SSE-KMS, this is the KMS key ARN or ID.
    enable_experimental_delta_support: bool = False  # Enables experimental Delta support. Note this will return incorrect values if you use optimize or delete.
    database: Optional[str] = (
        None  # Name of the Database in the Catalog. Can also be set via env variable ATHENA_DATABASE (backward compatibility)
    )
    s3_path: Optional[str] = (
        None  # S3 Location where spines will be uploaded and Athena output will be stored. Can be set via env variable ATHENA_S3_PATH (backward compatibility)
    )


class AthenaSession:
    def __init__(self):
        self._athena_s3_path = None
        self.config = AthenaSessionConfig()
        self._lazy_wr = None
        self._lazy_wr_lock = threading.Lock()

    @property
    def _wr(self):
        with self._lazy_wr_lock:
            if self._lazy_wr is None:
                try:
                    import awswrangler
                except ModuleNotFoundError:
                    msg = "Athena Session cannot be initialized. Python module awswrangler not found. Did you forget to pip install tecton[athena]?"
                    raise Exception(msg)

                awswrangler.engine.set("python")
                awswrangler.memory_format.set("pandas")
                self._lazy_wr = awswrangler
            return self._lazy_wr

    def _get_athena_s3_path(self):
        s3_path = self.config.s3_path or conf.get_or_none("ATHENA_S3_PATH")
        if s3_path is not None:
            # Configuration always takes precedent and can be set at any time
            self._athena_s3_path = s3_path
        elif self._athena_s3_path is None:
            # If the bucket hasn't been initialized yet, let's create a new bucket
            # Let's cache the result to ensure we don't do it unnecessarily over and over again
            self._athena_s3_path = self._wr.athena.create_athena_bucket(boto3_session=self.config.boto3_session)

        if self._athena_s3_path.endswith("/"):
            # Drop "/" - calling function expects a path without trailing "/"
            self._athena_s3_path = self._athena_s3_path[0:-1]

        if not self._athena_s3_path.startswith("s3"):
            msg = f"Provided S3 path does not start with s3://. Provided value: {s3_path}"
            raise TectonAthenaValidationError(msg)

        return self._athena_s3_path

    def delete_table_if_exists(self, database: str, table: str):
        return self._wr.catalog.delete_table_if_exists(
            database=database, table=table, boto3_session=self.config.boto3_session
        )

    def delete_view_if_exists(self, view_name: str):
        sql = f"DROP VIEW IF EXISTS {view_name}"
        self.sql(sql)

    def _get_table_parameters(self, database: str, table: str) -> Dict:
        return self._wr.catalog.get_table_parameters(
            database=database, table=table, boto3_session=self.config.boto3_session
        )

    def _does_table_exist(self, database: str, table: str) -> bool:
        return self._wr.catalog.does_table_exist(
            database=database, table=table, boto3_session=self.config.boto3_session
        )

    def _upload_pandas_to_s3(self, pandas_df: pandas.DataFrame):
        with tempfile.NamedTemporaryFile(suffix=".parquet.snappy") as f:
            s3_client = boto3.client("s3")
            pandas_df.to_parquet(f.name, engine="pyarrow", **PARQUET_WRITE_OPTIONS_KWARGS)

            local_file_name = os.path.basename(f.name)
            s3_random_dir_name = secrets.token_hex(10)

            s3_sub_directory = "/".join([S3_ATHENA_PANDAS_UPLOADS, s3_random_dir_name])

            s3_path_without_file = "/".join([self._get_athena_s3_path(), s3_sub_directory])
            s3_path_with_file = "/".join([s3_path_without_file, local_file_name])

            logger.info(f"Writing pandas df to S3 at {s3_path_with_file}...")

            # Consider switching to multipart upload
            # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html#multipart-transfers
            s3_bucket = urlparse(s3_path_with_file).netloc

            # Skip leading slash
            s3_object_key = urlparse(s3_path_with_file).path[1:]
            # When kms key is provided, use it to encrypt the file
            extra_args = (
                {"ServerSideEncryption": "aws:kms", "SSEKMSKeyId": self.config.kms_key} if self.config.kms_key else {}
            )
            # Some customers need to use bucket, but others may not have permissions to do so.
            # Fallback to use client when permission is not there.
            try:
                s3 = self.config.boto3_session.resource("s3")
                bucket = s3.Bucket(s3_bucket)
                bucket.upload_file(f.name, s3_object_key, ExtraArgs=extra_args)
            except Exception:
                s3_client.upload_file(f.name, s3_bucket, s3_object_key, ExtraArgs=extra_args)
            return s3_path_without_file

    def _create_athena_table_from_s3_path(self, s3_path: str, table_name: str, hive_columns: dict) -> str:
        athena_database = self._get_athena_database()
        query = CREATE_TABLE_TEMPLATE.render(
            database=athena_database,
            table=table_name,
            s3_location=s3_path,
            columns=hive_columns,
            offline_store_type="parquet",
        )
        logger.info(f"Creating Athena table {athena_database}.{table_name}...")

        self.sql(query)

        logger.info(f"Table {athena_database}.{table_name} was successfully created")

        # The database/table names are in the quotation marks to handle the scenario when they start with digits.
        return f'"{athena_database}"."{table_name}"'

    def _pandas_columns_to_hive_columns(self, pandas_df: pandas.DataFrame):
        column_types = {}
        for k, v in pandas_df.dtypes.to_dict().items():
            if "datetime64" in v.name:
                column_types[k] = "timestamp"
                continue
            type_name = v.name.lower()
            if type_name not in PANDAS_TO_HIVE_TYPES:
                msg = f"Pandas Type {type_name} not supported. Mapping to Hive Type not found."
                raise Exception(msg)
            column_types[k] = PANDAS_TO_HIVE_TYPES[type_name]
        return column_types

    def write_pandas(self, df: pandas.DataFrame, table_name: str) -> str:
        s3_full_path = self._upload_pandas_to_s3(df)
        hive_columns = self._pandas_columns_to_hive_columns(df)

        return self._create_athena_table_from_s3_path(s3_full_path, table_name, hive_columns)

    def sql(self, sql_query: str) -> Union[str, Dict[str, Any]]:
        return self._wr.athena.start_query_execution(
            sql_query,
            s3_output=self._get_athena_s3_path(),
            database=self._get_athena_database(),
            wait=True,
            boto3_session=self.config.boto3_session,
            workgroup=self.config.workgroup,
            encryption=self.config.encryption,
            kms_key=self.config.kms_key,
        )

    def read_sql(self, sql_query: str) -> Union[pandas.DataFrame, Iterator[pandas.DataFrame]]:
        return self._wr.athena.read_sql_query(
            sql_query,
            s3_output=self._get_athena_s3_path(),
            database=self._get_athena_database(),
            boto3_session=self.config.boto3_session,
            workgroup=self.config.workgroup,
            encryption=self.config.encryption,
            kms_key=self.config.kms_key,
        )

    def get_database(self) -> str:
        return self._get_athena_database()

    def create_table(self, table_spec: AthenaTableCreationSpec):
        logger.info(f"Registering Glue table {table_spec.database}.{table_spec.table}...")
        sql = CREATE_TABLE_TEMPLATE.render(
            database=table_spec.database,
            table=table_spec.table,
            s3_location=table_spec.s3_location,
            columns=table_spec.columns,
            partition_by=table_spec.partition_by,
            partition_by_type=table_spec.partition_by_type,
            partition_by_format=table_spec.partition_by_format,
            partition_by_range_from=table_spec.partition_by_range_from,
            partition_by_range_to=table_spec.partition_by_range_to,
            partition_by_interval=table_spec.partition_by_interval,
            tecton_table_metadata_hash=table_spec.stable_hash,
            tecton_table_spec_version=AthenaTableCreationSpec.SPEC_VERSION,
            offline_store_type=table_spec.data_format,
        )
        self.sql(sql)

    def create_view(self, view_sql, view_name):
        logger.info(f"Creating view {view_name}.")
        sql = f"CREATE VIEW {view_name} as {view_sql}"
        self.sql(sql)

    def _is_existing_table_equivalent_to_spec(self, table_spec: AthenaTableCreationSpec):
        parameters = self._get_table_parameters(table_spec.database, table_spec.table)

        return parameters.get(GLUE_CATALOG_TABLE_PROPERTY_HASH) == table_spec.stable_hash

    def _get_existing_table_spec_version(self, table_spec: AthenaTableCreationSpec):
        parameters = self._get_table_parameters(table_spec.database, table_spec.table)
        if GLUE_CATALOG_TABLE_PROPERTY_SPEC_VERSION not in parameters:
            return None

        return int(parameters[GLUE_CATALOG_TABLE_PROPERTY_SPEC_VERSION])

    def create_table_if_necessary(self, table_spec: AthenaTableCreationSpec):
        if not self._does_table_exist(table_spec.database, table_spec.table):
            return self.create_table(table_spec)

        existing_table_spec_version = self._get_existing_table_spec_version(table_spec)

        if self._is_existing_table_equivalent_to_spec(table_spec):
            logger.debug(
                f"Glue table {table_spec.database}.{table_spec.table} hash matches expectation ({table_spec.stable_hash}). No update needed."
            )
            if table_spec.data_format == "delta":
                # required for partition discovery
                self.repair_table(table_spec.database, table_spec.table)
            return
        if existing_table_spec_version is None:
            msg = f"Glue table {table_spec.database}.{table_spec.table} registration doesn't meet expectations but cannot be updated because it doesn't seem to have been registered by Tecton. Please drop the table to have Tecton manage its registration."
            raise TectonAthenaValidationError(msg)
        if existing_table_spec_version > AthenaTableCreationSpec.SPEC_VERSION:
            msg = f"Glue table {table_spec.database}.{table_spec.table} registration doesn't meet expectations but cannot be updated because it was registered with a newer version of Tecton. Please upgrade the SDK. Found Spec version: {existing_table_spec_version}. SDK Spec version: {AthenaTableCreationSpec.SPEC_VERSION}"
            raise TectonAthenaValidationError(msg)
        logger.info(
            f"Glue table {table_spec.database}.{table_spec.table} registration needs to be updated. Dropping existing table..."
        )
        self.delete_table_if_exists(table_spec.database, table_spec.table)
        table_create_result = self.create_table(table_spec)
        return table_create_result

    def repair_table(self, database, table):
        self.sql(f"MSCK REPAIR TABLE `{database}`.`{table}`")

    def get_spine_temp_table_name(self):
        return "TMP_SPINE_TABLE_" + secrets.token_hex(8)

    def _get_athena_database(self):
        return self.config.database or conf.get_or_none("ATHENA_DATABASE") or "tecton_temp_tables"


_session = None


def get_session():
    global _session

    if _session is not None:
        return _session

    _session = AthenaSession()
    return _session
