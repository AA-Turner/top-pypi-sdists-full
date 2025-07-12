import datetime
import functools
import itertools
import json
import logging
import os
import random
import re
import struct
import time
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from typing import List
from typing import Optional

from py4j.protocol import Py4JJavaError
from pyspark.sql import Column
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType
from pyspark.sql.types import TimestampType

from tecton_core.time_utils import seconds_to_nanos


try:
    # available in Spark >= 3.4
    from pyspark.sql.types import TimestampNTZType
except ImportError:
    from pyspark.sql.types import TimestampType as TimestampNTZType

import tecton_core.tecton_pendulum as pendulum
from tecton_core import time_utils as core_time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.offline_store import TIME_PARTITION
from tecton_core.offline_store import EntityBucketPartitionParams
from tecton_core.offline_store import PartitionType
from tecton_core.offline_store import _check_supported_offline_store_version
from tecton_core.offline_store import datetime_to_partition_str
from tecton_core.offline_store import get_time_column_for_offline_reader
from tecton_core.offline_store import partition_col_for_parquet
from tecton_core.offline_store import partition_size_for_delta
from tecton_core.offline_store import partition_size_for_parquet
from tecton_core.offline_store import partition_type_for_delta
from tecton_core.offline_store import timestamp_formats
from tecton_core.offline_store import window_size_seconds
from tecton_core.query_consts import anchor_time
from tecton_proto.data.feature_store__client_pb2 import FeatureStoreFormatVersion
from tecton_spark import time_utils as spark_time_utils


DBRICKS_MULTI_CLUSTER_WRITES_ENABLED = "spark.databricks.delta.multiClusterWrites.enabled"
DBRICKS_RUNTIME_VERSION = "DATABRICKS_RUNTIME_VERSION"

SPARK_GCS_DELTA_LOGSTORE_CLASS = "io.delta.storage.GCSLogStore"

SPARK31_DELTA_LOGSTORE_CLASS = "spark.delta.logStore.class"
SPARK31_DYNAMODB_LOGSTORE_CLASS = "io.delta.storage.DynamoDBLogStore"

SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS = "spark.delta.logStore.s3.impl"
SPARK32_OR_HIGHER_DYNAMODB_LOGSTORE_CLASS = "io.delta.storage.S3DynamoDBLogStore"

logger = logging.getLogger(__name__)


@dataclass
class OfflineStoreWriterParams:
    s3_path: str

    """Whether the anchor column should be stored in the Offline Feature Store regardless of whether it is
    required by the storage layer.

    If this is false the anchor column will be dropped from the stored data if it's not needed by the
    OfflineStoreWriter implementation.
    """
    always_store_anchor_column: bool

    """The column containing the timestamp value used for time-based partitioning"""
    time_column: str

    join_key_columns: List[str]

    is_continuous: bool

    upsert_by_batch_publish_timestamp: bool


def get_offline_store_writer(
    params: OfflineStoreWriterParams, fd: FeatureDefinitionWrapper, version: int, spark: SparkSession
) -> "OfflineStoreWriter":
    """Creates a concrete implementation of OfflineStoreWriter based on fv_config."""
    _check_supported_offline_store_version(fd)
    fv_config = fd.offline_store_config

    case = fv_config.WhichOneof("store_type")
    if case == "delta":
        partition_size = partition_size_for_delta(fd).as_timedelta()
        partition_type = partition_type_for_delta(fd.offline_store_params)
        return DeltaWriter(params, spark, version, partition_size, partition_type)
    elif case == "parquet":
        partition_size = partition_size_for_parquet(fd).as_timedelta()
        partition_col = partition_col_for_parquet(fd)
        return ParquetWriter(params, spark, version, partition_size, partition_col)
    elif case == "iceberg":
        return IcebergWriter(fd.id, params, fv_config.iceberg.num_entity_buckets, spark)
    else:
        msg = f"Invalid store type {case} for feature definition {fd.name}."
        raise ValueError(msg)


def get_dataset_generation_writer(params: OfflineStoreWriterParams, spark: SparkSession) -> "DeltaWriter":
    return DeltaWriter(
        params=params,
        spark=spark,
        version=FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
        partition_size=None,
        partition_type=PartitionType.NONE,
    )


def get_offline_store_reader(
    spark: SparkSession, fd: FeatureDefinitionWrapper, path: Optional[str] = None
) -> "OfflineStoreReader":
    _check_supported_offline_store_version(fd)
    assert fd.materialization_enabled and fd.writes_to_offline_store
    s3_path = path or fd.materialized_data_path
    version = fd.get_feature_store_format_version

    case = fd.offline_store_config.WhichOneof("store_type")
    if case == "delta":
        partition_size = partition_size_for_delta(fd).as_timedelta()
        partition_type = partition_type_for_delta(fd.offline_store_params)
        return DeltaReader(spark, s3_path, partition_size, partition_type, version)
    elif case == "parquet":
        partition_size = partition_size_for_parquet(fd).as_timedelta()
        partition_col = partition_col_for_parquet(fd)
        return ParquetReader(spark, s3_path, partition_size, partition_col, version)
    elif case == "iceberg":
        return IcebergReader(spark, fd.id, time_column=get_time_column_for_offline_reader(fd))
    else:
        msg = f"Invalid store type {case} for feature definition {fd.name}."
        raise ValueError(msg)


class OfflineStoreWriter(ABC):
    """Interface for Offline Feature Store writers."""

    @abstractmethod
    def append_dataframe(self, data_frame: DataFrame) -> None:
        """Append the rows from data_frame to the Store table. Nothing is overwritten."""
        raise NotImplementedError

    @abstractmethod
    def upsert_dataframe(self, data_frame: DataFrame) -> None:
        """Upsert the rows from data_frame to the Store table.

        Rows with matching join keys and time column are overwritten. Other rows are inserted.
        """
        raise NotImplementedError

    def overwrite_dataframe_in_tile(self, data_frame: DataFrame, time_range: pendulum.Period) -> None:
        """Overwrites the tiles(s) in the time_range."""
        raise NotImplementedError

    @abstractmethod
    def delete_keys(self, data_frame: DataFrame) -> int:
        """Delete rows from the Store table that match the keys inside the data_frame.

        Return number of successfully deleted keys."""
        raise NotImplementedError


class OfflineStoreReader(ABC):
    @abstractmethod
    def read(self, partition_time_limits: pendulum.Period) -> DataFrame:
        """Note that partition_time_limits only applies partition filtering, so you can have records outside it"""
        raise NotImplementedError


class ParquetWriter(OfflineStoreWriter):
    """Parquet implementation of OfflineStoreWriter"""

    def __init__(
        self,
        params: OfflineStoreWriterParams,
        spark: SparkSession,
        version: int,
        partition_size: timedelta,
        partition_col: str,
    ) -> None:
        self._params = params
        self._spark = spark
        self._version = version
        self._partition_size = partition_size
        self._partition_col = partition_col

    def append_dataframe(self, data_frame: DataFrame) -> None:
        if self._partition_col == TIME_PARTITION:
            align_duration = core_time_utils.convert_timedelta_for_version(self._partition_size, self._version)
            aligned_time = _align_timestamp(functions.col(anchor_time()), functions.lit(align_duration))
            data_frame = data_frame.withColumn(TIME_PARTITION, aligned_time)

        data_frame.write.option("partitionOverwriteMode", "dynamic").partitionBy(self._partition_col).parquet(
            self._params.s3_path, mode="overwrite"
        )

    def upsert_dataframe(self, data_frame: DataFrame) -> None:
        raise NotImplementedError()

    def overwrite_dataframe_in_tile(self, data_frame: DataFrame, time_range: pendulum.Period) -> None:
        raise NotImplementedError()

    def delete_keys(self, data_frame: DataFrame) -> int:
        raise NotImplementedError()


class ParquetReader(OfflineStoreReader):
    def __init__(
        self, spark: SparkSession, path: str, partition_size: timedelta, partition_col: str, version: int
    ) -> None:
        self._spark = spark
        self._path = path
        self._partition_size = partition_size
        self._partition_col = partition_col
        self._version = version

    def read(self, partition_time_limits: Optional[pendulum.Period]) -> DataFrame:
        spark_df = self._spark.read.parquet(self._path)

        # Parquet is partitioned by TIME_PARTITION when is_continuous and ANCHOR_TIME when not.
        # We want to explicitly cast the partition type in case:
        #   `spark.sql.sources.partitionColumnTypeInference.enabled` = "false"

        spark_df = spark_df.withColumn(self._partition_col, functions.col(self._partition_col).cast("long"))

        if partition_time_limits and self._partition_size:
            aligned_start_time = core_time_utils.align_time_downwards(partition_time_limits.start, self._partition_size)
            aligned_end_time = core_time_utils.align_time_downwards(partition_time_limits.end, self._partition_size)
            start_time_epoch = core_time_utils.convert_timestamp_for_version(aligned_start_time, self._version)
            end_time_epoch = core_time_utils.convert_timestamp_for_version(aligned_end_time, self._version)
            partition_col = functions.col(self._partition_col)
            spark_df = spark_df.where((start_time_epoch <= partition_col) & (partition_col <= end_time_epoch))

        return spark_df.drop(TIME_PARTITION)


_EXCEPTION_PACKAGES = {
    "com.databricks.sql.transaction.tahoe",  # Used by Databricks
    "org.apache.spark.sql.delta",  # Used by open source
}

_EXCEPTION_CLASSES = {
    "ConcurrentAppendException",
    "ConcurrentDeleteReadException",
    "ConcurrentDeleteDeleteException",
    "ProtocolChangedException",  # This can occur when two txns create the same table concurrently
}

_RETRYABLE_DELTA_EXCEPTIONS = {
    f"{pkg}.{cls}" for pkg, cls in itertools.product(_EXCEPTION_PACKAGES, _EXCEPTION_CLASSES)
}


def _with_delta_retries(f, max_retries=5):
    """Retries the wrapped function upon Deltalake conflict errors."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        from delta.exceptions import ConcurrentAppendException
        from delta.exceptions import ConcurrentDeleteDeleteException
        from delta.exceptions import ConcurrentDeleteReadException
        from delta.exceptions import ConcurrentTransactionException
        from delta.exceptions import DeltaConcurrentModificationException
        from delta.exceptions import MetadataChangedException
        from delta.exceptions import ProtocolChangedException
        from pyspark.sql.utils import AnalysisException

        final_exception = None
        for i in range(max_retries):
            try:
                if i > 0:
                    # Add a random delay (with exponential backoff) before the retries to decrease
                    # the chance of recurrent conflicts between the parallel offline store writers.
                    # Possible 10s of seconds of delay is insignificant to the overall job's latency.
                    exponential_coef = 2 ** (i - 1)
                    retry_delay = exponential_coef * random.uniform(0, 1)
                    time.sleep(retry_delay)
                f(*args, **kwargs)
                return
            except Py4JJavaError as e:
                exception_class = e.java_exception.getClass().getCanonicalName()
                if exception_class not in _RETRYABLE_DELTA_EXCEPTIONS:
                    raise e
                final_exception = e
                logger.info(
                    f"Delta transaction failed (attempt {i + 1}/{max_retries}); retrying",
                    exc_info=True,  # Include information about the exception currently being handled
                )
            except (
                ConcurrentAppendException,
                ConcurrentDeleteDeleteException,
                ConcurrentDeleteReadException,
                ConcurrentTransactionException,
                DeltaConcurrentModificationException,
                MetadataChangedException,
                ProtocolChangedException,
                AnalysisException,
            ) as e:
                if isinstance(e, AnalysisException) and "Incompatible format detected" not in str(e):
                    # If it's NOT "Incompatible format detected", we don't retry and re-raise it
                    # Retrying "Incompatible format detected" in the case where concurrent commits are writing files before the first delta log.
                    raise
                final_exception = e
                logger.info(
                    f"Delta transaction failed (attempt {i + 1}/{max_retries}); retrying",
                    exc_info=True,  # Include information about the exception currently being handled
                )
            except Exception:
                logger.warning("Uncaught exception raised during Delta write", exc_info=True)
                raise
        msg = f"Exceeded maximum Delta transaction retries ({max_retries})"
        raise Exception(msg) from final_exception

    return wrapper


def _assert_safe_delta_write_configuration(spark: SparkSession) -> bool:
    """Asserts that the Spark configuration is such that it is safe to write to Delta concurrently.

    With the Open Source Delta JAR installed (as it is on EMR), writing to a Delta table concurrently with another
    Spark cluster could corrupt the table unless the Delta Logstore class is overridden.

    On Databricks everything is fine as multi-cluster writes are enabled (the default).
    """

    configs = {
        DBRICKS_RUNTIME_VERSION: os.environ.get(DBRICKS_RUNTIME_VERSION, None),
        DBRICKS_MULTI_CLUSTER_WRITES_ENABLED: spark.conf.get(DBRICKS_MULTI_CLUSTER_WRITES_ENABLED, None),
        SPARK31_DELTA_LOGSTORE_CLASS: spark.conf.get(SPARK31_DELTA_LOGSTORE_CLASS, None),
        SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS: spark.conf.get(SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS, None),
    }
    if configs[DBRICKS_RUNTIME_VERSION] and configs[DBRICKS_MULTI_CLUSTER_WRITES_ENABLED] == "true":
        return True

    # either the spark 3.1 or spark 3.2+ DELTA_LOGSTORE_CLASS name can be set
    if configs[SPARK31_DELTA_LOGSTORE_CLASS] in [SPARK31_DYNAMODB_LOGSTORE_CLASS, SPARK_GCS_DELTA_LOGSTORE_CLASS]:
        return True
    if configs[SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS] in [
        SPARK32_OR_HIGHER_DYNAMODB_LOGSTORE_CLASS,
        SPARK_GCS_DELTA_LOGSTORE_CLASS,
    ]:
        return True
    msg = f"Configuration is not safe for concurrent writes: {configs}"
    raise AssertionError(msg)


def _is_dbr_version_greater_than_or_equal_to_14(spark: SparkSession) -> bool:
    # Return False if not on Databricks.
    if DBRICKS_RUNTIME_VERSION not in os.environ:
        return False

    dbr_version = os.environ.get(DBRICKS_RUNTIME_VERSION)

    major_version = dbr_version.split(".")[0]  # "11.3" -> "11"
    try:
        return int(major_version) >= 14
    except ValueError:
        exception_msg = f'DBR Version from "os.environ":{dbr_version} is incorrect.'
        raise ValueError(exception_msg)


class DeltaWriter(OfflineStoreWriter):
    """DeltaLake implementation of OfflineStoreWriter"""

    def __init__(
        self,
        params: OfflineStoreWriterParams,
        spark: SparkSession,
        version: int,
        partition_size: Optional[timedelta],
        partition_type: PartitionType,
    ) -> None:
        self._params = params
        self._spark = spark
        self._version = version
        self._partition_size = partition_size
        self._partition_type = partition_type
        self._metadata_writer = DeltaMetadataWriter(spark)
        if not spark.conf.get("spark.databricks.delta.commitInfo.userMetadata"):
            msg = "Expected spark.databricks.delta.commitInfo.userMetadata to be set for delta writes"
            raise AssertionError(msg)

    def append_dataframe(self, data_frame: DataFrame) -> None:
        if self._partition_type != PartitionType.NONE:
            data_frame = self._add_partition(data_frame)
        self._ensure_table_exists(self._spark, data_frame.schema)
        self._append_dataframe(data_frame)

    def upsert_dataframe(self, data_frame):
        # See https://github.com/delta-io/delta/issues/282 for why this isn't at the top of the file
        from delta.tables import DeltaTable

        _assert_safe_delta_write_configuration(self._spark)

        data_frame = self._add_partition(data_frame)
        self._ensure_table_exists(self._spark, data_frame.schema)

        table = DeltaTable.forPath(self._spark, self._params.s3_path)

        base = table.toDF().alias("base")
        updates = data_frame.alias("updates")

        # Build a condition which matches on all join keys, the timestamp, and the time partition column. The time
        # partition column is not needed for correctness, but it allows some files to be skipped by Delta.
        all_match_keys = [self._params.time_column, TIME_PARTITION, *self._params.join_key_columns]
        key_matches = [base[k] == updates[k] for k in all_match_keys]
        match_condition = functools.reduce(lambda l, r: l & r, key_matches)

        @_with_delta_retries
        def _execute():
            table.merge(updates, match_condition).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        _execute()

    def delete_keys(self, data_frame: DataFrame) -> int:
        # See https://github.com/delta-io/delta/issues/282 for why this isn't at the top of the file
        from delta.tables import DeltaTable

        _assert_safe_delta_write_configuration(self._spark)

        deltaTable = DeltaTable.forPath(self._spark, self._params.s3_path)
        query = ""
        columns = data_frame.columns
        for column in columns:
            if query:
                query = query + " AND "
            query = query + "t." + column + " = k." + column

        @_with_delta_retries
        def _execute():
            deltaTable.alias("t").merge(data_frame.alias("k"), query).whenMatchedDelete().execute()

        @_with_delta_retries
        def _vacuum():
            deltaTable.vacuum()

        _execute()
        _vacuum()

        last_operation = deltaTable.history(1).collect()
        if not last_operation:
            return 0

        return int(last_operation[0].operationMetrics.get("numTargetRowsDeleted", 0))

    def overwrite_dataframe_in_tile(self, data_frame: DataFrame, time_range: pendulum.Period) -> None:
        df_to_write = self._add_partition(data_frame)
        self._ensure_table_exists(self._spark, df_to_write.schema)

        replace_predicate = self._in_range(time_range)

        @_with_delta_retries
        def _execute():
            df_to_write.write.format("delta").mode("overwrite").partitionBy(TIME_PARTITION).option(
                "replaceWhere", replace_predicate
            ).save(self._params.s3_path)

        _assert_safe_delta_write_configuration(self._spark)
        _execute()

    def _in_range(self, time_range: pendulum.Period) -> str:
        if self._params.time_column == anchor_time():
            assert self._params.always_store_anchor_column
            start_time = core_time_utils.convert_timestamp_for_version(time_range.start, self._version)
            end_time = core_time_utils.convert_timestamp_for_version(time_range.end, self._version)
            time_col_predicate = (
                f"{self._params.time_column} >= {start_time} AND {self._params.time_column} < {end_time}"
            )
        else:
            start_time_str = time_range.start.strftime("%Y-%m-%d %H:%M:%S")
            end_time_str = time_range.end.strftime("%Y-%m-%d %H:%M:%S")
            time_col_predicate = f"{self._params.time_column} >= timestamp('{start_time_str}') AND {self._params.time_column} < timestamp('{end_time_str}')"

        partition_aligned_start = core_time_utils.align_time_downwards(time_range.start, self._partition_size)
        partition_aligned_end = core_time_utils.align_time_downwards(time_range.end, self._partition_size)
        if self._partition_type == PartitionType.EPOCH:
            start_partition_epoch = core_time_utils.convert_timestamp_for_version(
                partition_aligned_start, self._version
            )
            end_partition_epoch = core_time_utils.convert_timestamp_for_version(partition_aligned_end, self._version)
            # offline store is partitioned by event_timestamp
            # event_timestamp <= batch_publish_timestamp
            # if batch_publish_timestamp BETWEEN start_time and end_time, then event_timestmp <= end_time,
            # so we can filter by the upper bound of the event_timestamp partition
            if self._params.upsert_by_batch_publish_timestamp:
                partition_predicate = f"{TIME_PARTITION} <= {end_partition_epoch}"
            else:
                partition_predicate = f"{TIME_PARTITION} BETWEEN {start_partition_epoch} AND {end_partition_epoch}"
        else:
            # TODO (vitaly): test that this works for hour partitions (rare case)
            start_partition_str = datetime_to_partition_str(partition_aligned_start, self._partition_size)
            end_partition_str = datetime_to_partition_str(partition_aligned_end, self._partition_size)
            # offline store is partitioned by event_timestamp
            # event_timestamp <= batch_publish_timestamp
            # if batch_publish_timestamp BETWEEN start_time and end_time, then event_timestmp <= end_time,
            # so we can filter by the upper bound of the event_timestamp partition
            if self._params.upsert_by_batch_publish_timestamp:
                partition_predicate = f"{TIME_PARTITION} <= timestamp('{end_partition_str}')"
            else:
                partition_predicate = (
                    f"{TIME_PARTITION} BETWEEN timestamp('{start_partition_str}') AND timestamp('{end_partition_str}')"
                )

        return f"{time_col_predicate} AND {partition_predicate}"

    def _add_partition(self, data_frame: DataFrame) -> DataFrame:
        """Adds the time_partition column and drops the _anchor_time column if needed."""
        partition = self._timestamp_to_partition_column(data_frame)
        data_frame = data_frame.withColumn(TIME_PARTITION, partition)
        if not self._params.always_store_anchor_column:
            data_frame = data_frame.drop(anchor_time())
        return data_frame

    def _ensure_table_exists(self, spark: SparkSession, schema: StructType) -> None:
        """Ensures that the table exists with the given schema.

        Some operations (including merge) fail when the table doesn't already exist. Others (append) can have conflicts
        where they wouldn't normally when they also create a new table. This function ensures neither will happen.
        """
        df = spark.createDataFrame([], schema)  # DF with 0 rows
        self._append_dataframe(df)

        # Manifest files are not supported on GCS
        if not self._params.s3_path.startswith("gs://"):
            # we set auto manifest so each job generates its own manifest (necessary for athena retrieval)
            self._metadata_writer.set_table_property(
                self._params.s3_path, "delta.compatibility.symlinkFormatManifest.enabled", "true"
            )

    @_with_delta_retries
    def _append_dataframe(self, df: DataFrame) -> None:
        _assert_safe_delta_write_configuration(self._spark)
        if self._partition_type == PartitionType.NONE:
            df_writer = df.coalesce(10).write.format("delta").mode("append")
        else:
            df_writer = df.write.partitionBy(TIME_PARTITION).format("delta").mode("append")

        # For DBR 14+, Deletion Vectors are auto-enabled.
        # Refer to this section on why we must disable deletion vectors:
        # https://www.notion.so/tecton/RFC-Support-DLT-Table-as-Data-Source-7ddf14a8ace04b03ba91b2e3f7db03bf?pvs=4#f520cb9f406d4c6f9fc743dc4f399607
        if _is_dbr_version_greater_than_or_equal_to_14(self._spark):
            df_writer.option("delta.enableDeletionVectors", "false")
        df_writer.save(self._params.s3_path)

    def _timestamp_to_partition_column(self, df: DataFrame) -> Column:
        # For some insane reason from_unixtime returns a timestamp in the session timezone, so it's pretty annoying to
        # convert a unix time to a formatted UTC timestamp unless the session is set to UTC. This only runs in
        # materialization so we can just assert that that's the case.
        tz = df.sql_ctx.sparkSession.conf.get("spark.sql.session.timeZone")
        if tz not in {"UTC", "Etc/UTC", "GMT"}:
            msg = f"spark.sql.session.timeZone must be UTC, not {tz}"
            raise AssertionError(msg)

        time_col = self._params.time_column
        time_column_type = df.schema[time_col].dataType
        allowed_types = {IntegerType(), TimestampType(), LongType(), TimestampNTZType()}
        if time_column_type not in allowed_types:
            msg = f"timestamp column must be one of {allowed_types}, not {time_column_type}"
            raise AssertionError(msg)

        if self._partition_type == PartitionType.EPOCH:
            assert self._partition_size is not None, "Partition size must be set for EPOCH partitions"
            assert self._version >= FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS, (
                f"FeatureStoreFormateVersion {self._version} is not supported. PartitionType.EPOCH on delta must be in nanoseconds."
            )
            partition_size_nanoseconds = core_time_utils.convert_timedelta_for_version(
                self._partition_size, self._version
            )
            time_val_nanoseconds = spark_time_utils.convert_timestamp_to_epoch(functions.col(time_col), self._version)
            aligned_time_partition_val_nanoseconds = _align_timestamp(time_val_nanoseconds, partition_size_nanoseconds)
            return aligned_time_partition_val_nanoseconds

        if time_column_type in {TimestampType(), TimestampNTZType()}:
            time_val = functions.unix_timestamp(functions.col(time_col))
        else:
            time_val = functions.col(time_col).cast(LongType())
        if time_col == anchor_time():
            time_val = spark_time_utils.convert_epoch_to_datetime(functions.col(time_col), self._version).cast(
                LongType()
            )
        aligned_time_partition_val_seconds = _align_timestamp(time_val, window_size_seconds(self._partition_size))
        aligned_time_partition_val_string = functions.from_unixtime(aligned_time_partition_val_seconds)
        partition_format_for_date_str = timestamp_formats(self._partition_size).spark_format
        return functions.date_format(
            aligned_time_partition_val_string.cast(TimestampType()), partition_format_for_date_str
        )


class DeltaMetadataWriter:
    def __init__(self, spark: SparkSession) -> None:
        self._spark = spark

    @_with_delta_retries
    def generate_symlink_manifest(self, path: str) -> None:
        _assert_safe_delta_write_configuration(self._spark)
        # we need spark_catalog in cases where the data source switches catalogs
        self._spark.sql(f"GENERATE symlink_format_manifest FOR TABLE spark_catalog.delta.`{path}`")

    @_with_delta_retries
    def set_table_property(self, path, key, val):
        _assert_safe_delta_write_configuration(self._spark)
        # we need spark_catalog in cases where the data source switches catalogs
        existing_tbl_properties = self._spark.sql(f"show tblproperties spark_catalog.delta.`{path}`").collect()
        # tblproperties are case sensitive
        has_tbl_property = any(key == r.key and val == r.value for r in existing_tbl_properties)
        # we only set it if not already set to avoid delta conflicts
        if not has_tbl_property:
            self._spark.sql(f"ALTER TABLE spark_catalog.delta.`{path}` SET TBLPROPERTIES({key}={val})")

    @_with_delta_retries
    def optimize_execute_compaction(self, path):
        _assert_safe_delta_write_configuration(self._spark)
        self._spark.sql(f"OPTIMIZE '{path}'")

    @_with_delta_retries
    def optimize_execute_sorting(self, path, join_keys):
        from delta.tables import DeltaTable

        _assert_safe_delta_write_configuration(self._spark)
        table = DeltaTable.forPath(self._spark, path)

        history = table.history().collect()  # history of commits in reverse order
        optimized_partitions = set()
        write_start_time_threshold = datetime.date.today()

        predicate_re = re.compile("time_partition = '([^']+)'")
        iso_format_length = len("YYYY-MM-DDThh:mm:ss")

        for commit in history:
            # Iterating over commit history in reverse order
            # and saving optimized partitions only if OPTIMIZE operation was after WRITE

            if commit["operation"] == "WRITE" and commit["userMetadata"]:
                # For WRITE operation we have only featureStartTime so we can only maintain write threshold
                user_metadata = json.loads(commit["userMetadata"])
                if "featureStartTime" in user_metadata:
                    feature_start_time = user_metadata["featureStartTime"][:iso_format_length]
                    write_start_time_threshold = min(
                        write_start_time_threshold, datetime.datetime.fromisoformat(feature_start_time).date()
                    )

            if commit["operation"] == "OPTIMIZE":
                predicate = json.loads(commit["operationParameters"]["predicate"])
                if not predicate:
                    continue

                # predicate should have format ["(time_partition = 2021-09-05)"]
                predicate = predicate[0]
                date_str = predicate_re.findall(predicate)[0]
                optimized_partition = datetime.date.fromisoformat(date_str)
                if optimized_partition >= write_start_time_threshold:
                    # OPTIMIZE ran before WRITE overwrote this partition
                    continue

                optimized_partitions.add(optimized_partition.isoformat())

        partitions = [row["time_partition"] for row in table.toDF().select(TIME_PARTITION).distinct().collect()]
        for partition in partitions:
            # Executing Optimize command on each partition individually.
            # That helps with resources and runs faster than a global sort, which is quite expensive.
            if partition in optimized_partitions:
                continue

            result = table.optimize().where(f"{TIME_PARTITION}='{partition}'").executeZOrderBy(*join_keys).collect()
            logger.info("ZOrder sorting for partition %s completed: %s", partition, result)

    @_with_delta_retries
    def vacuum(self, path):
        _assert_safe_delta_write_configuration(self._spark)
        self._spark.sql(f"VACUUM '{path}'")


class DeltaReader(OfflineStoreReader):
    def __init__(
        self,
        spark: SparkSession,
        path: str,
        partition_size: Optional[timedelta],
        partition_type: PartitionType,
        feature_store_format_version: int,
    ) -> None:
        self._spark = spark
        self._path = path
        self._partition_size = partition_size
        self._partition_type = partition_type
        self._feature_store_format_version = feature_store_format_version

    def read(self, partition_time_limits: Optional[pendulum.Period]) -> DataFrame:
        spark_df = self._spark.read.format("delta").load(self._path)

        if partition_time_limits is None or not self._partition_size:
            return spark_df.drop(TIME_PARTITION)

        # Whenever the partition filtering logic is changed, also make sure the changes are applied to the sql based
        # version in query/nodes.py

        # Delta is always partitioned by TIME_PARTITION. We want to explicitly cast to it's correct type in case:
        #   `spark.sql.sources.partitionColumnTypeInference.enabled` = "false"
        aligned_start_time = core_time_utils.align_time_downwards(partition_time_limits.start, self._partition_size)
        aligned_end_time = core_time_utils.align_time_downwards(partition_time_limits.end, self._partition_size)

        if self._partition_type == PartitionType.DATE_STR:
            partition_col = functions.col(TIME_PARTITION).cast("timestamp")
            start_partition = datetime_to_partition_str(aligned_start_time, self._partition_size)
            end_partition = datetime_to_partition_str(aligned_end_time, self._partition_size)
        elif self._partition_type == PartitionType.EPOCH:
            partition_col = functions.col(TIME_PARTITION).cast("long")
            start_partition = core_time_utils.convert_timestamp_for_version(
                aligned_start_time, self._feature_store_format_version
            )
            end_partition = core_time_utils.convert_timestamp_for_version(
                aligned_end_time, self._feature_store_format_version
            )
        else:
            msg = f"Invalid partition type for Delta: {self._partition_type}"
            raise AssertionError(msg)

        spark_df = spark_df.where((start_partition <= partition_col) & (partition_col <= end_partition))

        return spark_df.drop(TIME_PARTITION)


def _align_timestamp(int_timestamp_col, window_size):
    return int_timestamp_col - (int_timestamp_col % window_size)


def _with_iceberg_retries(func, max_retries=3):
    """Retries the wrapped function upon Iceberg conflict errors."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        final_exception = None
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Py4JJavaError as e:
                msg = str(e)
                retryable_exceptions = [
                    # Concurrent modification exceptions
                    "org.apache.iceberg.exceptions.CommitFailedException",
                    # Validation exceptions that might be temporary
                    "org.apache.iceberg.exceptions.ValidationException",
                    # Lock-related exceptions
                    "org.apache.iceberg.exceptions.CommitStateUnknownException",
                    # Catalog-related exceptions that might be temporary
                    "org.apache.iceberg.exceptions.ServiceFailureException",
                    # Concurrent operation exceptions
                    "org.apache.iceberg.exceptions.ConcurrentUpdateException",
                    # Temporary failures in the underlying storage
                    "org.apache.iceberg.exceptions.RuntimeIOException",
                ]

                is_retryable = any(exc in msg for exc in retryable_exceptions)
                if is_retryable:
                    logger.info(f"Iceberg transaction failed (attempt {i + 1}/{max_retries}); retrying", exc_info=True)
                    final_exception = e
                    if i == max_retries - 1:
                        break
                    # Add a random delay with exponential backoff before retrying
                    exponential_coef = 2**i
                    retry_delay = exponential_coef * random.uniform(0, 1)
                    time.sleep(retry_delay)
                else:
                    raise

        # This should be outside the loop but inside the wrapper function
        msg = f"Exceeded maximum Iceberg transaction retries ({max_retries})"
        raise Exception(msg) from final_exception

    return wrapper


class IcebergCatalog:
    # TODO: this should be configurable by Orchestrator / deployment env vars
    CATALOG_NAME = "iceberg"
    GLUE_DB = "default"


class IcebergWriter(OfflineStoreWriter):
    def __init__(
        self,
        table_id: str,
        params: OfflineStoreWriterParams,
        num_entity_buckets: int,
        spark: SparkSession,
    ) -> None:
        self._params = params
        self._spark = spark
        self._num_buckets = num_entity_buckets
        self._full_table_name = f"{IcebergCatalog.CATALOG_NAME}.{IcebergCatalog.GLUE_DB}.t_{table_id}"

    def append_dataframe(self, data_frame: DataFrame) -> None:
        df = self._add_partition(data_frame)
        self._ensure_table_exists(df.schema)
        self._append_dataframe(df)

    @_with_iceberg_retries
    def _append_dataframe(self, data_frame: DataFrame) -> None:
        data_frame.writeTo(self._full_table_name).append()

    @_with_iceberg_retries
    def upsert_dataframe(self, data_frame: DataFrame) -> None:
        """Upsert the rows from data_frame to the Store table.

        Rows with matching join keys and time column are overwritten. Other rows are inserted.
        """
        df_with_partition = self._add_partition(data_frame)
        self._ensure_table_exists(df_with_partition.schema)

        temp_upsert_data_view = "t_upsert_data"
        df_with_partition.createOrReplaceTempView(temp_upsert_data_view)

        all_match_keys = [
            EntityBucketPartitionParams.partition_by,
            self._params.time_column,
            *self._params.join_key_columns,
        ]
        join_condition = " AND ".join([f"target.{col} = source.{col}" for col in all_match_keys])
        merge_sql = f"""
        MERGE INTO {self._full_table_name} AS target
        USING {temp_upsert_data_view} AS source
        ON {join_condition}
        WHEN MATCHED THEN
          UPDATE SET *
        WHEN NOT MATCHED THEN
          INSERT *
        """

        @_with_iceberg_retries
        def _execute(sql: str) -> None:
            self._spark.sql(sql)

        _execute(merge_sql)

    def overwrite_dataframe_in_tile(self, data_frame: DataFrame, time_range: pendulum.Period) -> None:
        data_frame = self._add_partition(data_frame)
        self._ensure_table_exists(data_frame.schema)

        if self._params.time_column == anchor_time():
            start_time = seconds_to_nanos(time_range.start.timestamp())
            end_time = seconds_to_nanos(time_range.end.timestamp())
            delete_condition = f"{self._params.time_column} >= {start_time} AND {self._params.time_column} < {end_time}"
        else:
            start_time_str = time_range.start.to_iso8601_string()
            end_time_str = time_range.end.to_iso8601_string()
            delete_condition = f"{self._params.time_column} >= TIMESTAMP '{start_time_str}' AND {self._params.time_column} < TIMESTAMP '{end_time_str}'"

        @_with_iceberg_retries
        def _delete_existing_data():
            self._spark.sql(f"""
                DELETE FROM {self._full_table_name}
                WHERE {delete_condition}
            """)

        @_with_iceberg_retries
        def _append_new_data():
            data_frame.writeTo(self._full_table_name).append()

        # Execute delete and append operations sequentially
        # note: NOT atomic but Iceberg overwrite cannot support partial file overwrite.
        # INSERT OVERWRITE overwrites the entire partition.
        # MERGE INTO cannot handle a partial MATCH and NOT MATCH case.
        _delete_existing_data()
        _append_new_data()

    @_with_iceberg_retries
    def delete_keys(self, data_frame: DataFrame) -> int:
        """
        Deletes rows from the Iceberg table that match the keys in the provided DataFrame.

        :param data_frame: A Spark DataFrame containing the keys to delete.
        :return: The number of deleted rows (not directly supported by Iceberg, so returns 0).
        """

        # Create a temporary view for the keys to delete DataFrame
        temp_keys_to_delete_view = "t_keys_to_delete"
        data_frame.createOrReplaceTempView(temp_keys_to_delete_view)

        delete_condition = " AND ".join([f"t.{col} = k.{col}" for col in data_frame.columns])
        delete_sql = f"""
        DELETE FROM {self._full_table_name} t
        WHERE EXISTS (
            SELECT 1 FROM {temp_keys_to_delete_view} k
            WHERE {delete_condition}
        )
        """

        self._spark.sql(delete_sql)
        return 0

    def compact_files(
        self,
        small_file_threshold_mb: int = 100,
        target_file_size_mb: int = 256,
        dry_run: bool = False,
        compact_bucket_num: Optional[int] = None,
    ) -> None:
        """Compacts small files in the Iceberg table to reduce file count.

        Args:
            small_file_threshold_mb: Files smaller than this size (in MB) will be considered for compaction
            target_file_size_mb: Target size for compacted files (in MB)
            dry_run: whether to actually write compacted files
            compact_bucket_num: If specified, only compact files in this entity bucket
        """
        if not self._check_table_exists():
            msg = f"Table {self._full_table_name} does not exist, cannot compact any files!"
            raise ValueError(msg)

        logger.info(
            f"Starting file compaction (threshold={small_file_threshold_mb}MB, target_size={target_file_size_mb}MB)"
        )

        target_file_bytes = target_file_size_mb * 1024 * 1024
        min_file_size_bytes = small_file_threshold_mb * 1024 * 1024
        rewrite_sql = f"CALL iceberg.system.rewrite_data_files(table => '{self._full_table_name}', options => map('target-file-size-bytes', {target_file_bytes}, 'min-file-size-bytes', {min_file_size_bytes})"
        if compact_bucket_num is not None:
            filter_sql = f", where => '{EntityBucketPartitionParams.partition_by} = {compact_bucket_num}'"
            rewrite_sql += filter_sql
        rewrite_sql += ")"

        if dry_run:
            logger.info(f"dry_run=true: Skipping file compaction. Generated SQL: {rewrite_sql}")
            return

        result_df = self._spark.sql(rewrite_sql)
        logger.info("Compaction summary:")
        result_df.show()

    def _check_table_exists(self) -> bool:
        # TODO: use tableExists() method when we remove support for Spark 3.2 if hasattr(self._spark.catalog, "tableExists"):
        if hasattr(self._spark.catalog, "tableExists"):
            return self._spark.catalog.tableExists(self._full_table_name)

        from pyspark.sql.utils import AnalysisException

        try:
            # Spark < 3.3 does not support tableExists() method
            self._spark.sql(f"DESCRIBE {self._full_table_name}")
        except AnalysisException:
            return False
        else:
            return True

    @_with_iceberg_retries
    def _ensure_table_exists(self, schema: StructType) -> None:
        table_exists = self._check_table_exists()
        if table_exists:
            return

        # We should always be specifying the materialization path location, but for local integration tests we need to use a Hadoop catalog which doesn't support specifying a location
        skip_location = self._spark.conf.get("spark.tecton.test_only.skip_iceberg_table_location", "false") == "true"
        location_str = f"LOCATION '{self._params.s3_path}'" if not skip_location else ""
        empty_df = self._spark.createDataFrame([], schema)
        schema_ddl = empty_df._jdf.schema().toDDL()
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self._full_table_name} (
            {schema_ddl}
        )
        USING iceberg
        PARTITIONED BY (entity_bucket)
        {location_str}
        """
        self._spark.sql(create_table_sql)

        sort_order_sql = f"""
        ALTER TABLE {self._full_table_name}
        WRITE DISTRIBUTED BY PARTITION LOCALLY ORDERED BY {self._params.time_column}
        """
        self._spark.sql(sort_order_sql)

    def _add_partition(self, data_frame: DataFrame) -> DataFrame:
        assert self._num_buckets > 0, "`num_buckets` must be greater than 0 for entity bucket partitioning."
        bucket_udf = entity_bucket_transform(self._num_buckets)

        # Add the 'entity_bucket' column
        return data_frame.withColumn(
            EntityBucketPartitionParams.partition_by, bucket_udf(functions.col(self._params.join_key_columns[0]))
        )


def entity_bucket_transform(num_buckets):
    """
    Creates a UDF that applies a hash bucket transform to entity values.
    Computes Iceberg-compatible bucket IDs using Murmur3 32-bit hash.
    Supports only int and str types. Uses little-endian encoding for ints, per Iceberg spec.
    Args:
        num_buckets: Number of buckets to use for partitioning

    Returns:
        A Spark UDF that transforms entity values into bucket numbers
    """
    import mmh3

    # TODO: make a java udf that uses murmurhash3 to speed this up.
    # NOTE: do not use spark.functions.hash(..) because it uses a different seed than Iceberg murmurhash implementation.
    @functions.udf(IntegerType())
    def bucket_hash(value):
        if isinstance(value, int):
            # Little-endian 8-byte signed integer
            packed = struct.pack("<q", value)
            hash_val = mmh3.hash(packed)
        elif isinstance(value, str):
            hash_val = mmh3.hash(value)
        else:
            msg = f"Unsupported type for bucketing: {type(value)}. Expected int or str."
            raise TypeError(msg)

        return (hash_val & 0x7FFFFFFF) % num_buckets

    return bucket_hash


class IcebergReader(OfflineStoreReader):
    def __init__(
        self,
        spark: SparkSession,
        table_id: str,
        time_column: str,
    ) -> None:
        self._spark = spark
        self._time_column = time_column
        self._full_table_name = f"{IcebergCatalog.CATALOG_NAME}.{IcebergCatalog.GLUE_DB}.t_{table_id}"

    def read(self, partition_time_limits: Optional[pendulum.Period], drop_entity_bucket_col: bool = True) -> DataFrame:
        """
        Whenever the partition filtering logic is changed, also make sure the changes are applied to the sql based
        version in query/nodes.py
        """
        spark_df = self._spark.table(self._full_table_name)

        if partition_time_limits:
            if self._time_column == anchor_time():
                start_time = seconds_to_nanos(partition_time_limits.start.timestamp())
                end_time = seconds_to_nanos(partition_time_limits.end.timestamp())
            else:
                start_time = partition_time_limits.start
                end_time = partition_time_limits.end

            condition = (functions.col(self._time_column) >= start_time) & (functions.col(self._time_column) < end_time)

            spark_df = spark_df.where(condition)

        # TODO: add support for entity bucket filtering
        if drop_entity_bucket_col:
            spark_df = spark_df.drop(EntityBucketPartitionParams.partition_by)
        return spark_df
