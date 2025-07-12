"""Helper module for creating spark data source operations such as creating DataFrames and
registering temp views. Methods within this class should exclusively operate on proto
representations of the data model.
"""

import base64
import json
import logging
import os
import time
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from pyspark.sql import functions
from pyspark.sql.functions import coalesce
from pyspark.sql.functions import to_timestamp
from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import DateType
from pyspark.sql.types import MapType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
import tecton_spark.errors_spark
from tecton_core import conf
from tecton_core import specs
from tecton_core.filter_context import FilterContext
from tecton_core.snowflake_context import decrypt_private_key
from tecton_core.spark_type_annotations import PySparkColumn
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_core.spark_type_annotations import PySparkSession
from tecton_proto.args.data_source_config__client_pb2 import INITIAL_STREAM_POSITION_LATEST
from tecton_proto.args.data_source_config__client_pb2 import INITIAL_STREAM_POSITION_TRIM_HORIZON
from tecton_proto.args.data_source_config__client_pb2 import INITIAL_STREAM_POSITION_UNSPECIFIED
from tecton_proto.common.data_source_type__client_pb2 import DataSourceType
from tecton_proto.data.batch_data_source__client_pb2 import FileDataSourceFormat
from tecton_spark.data_source_credentials import get_kafka_secrets
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


logger = logging.getLogger(__name__)

INITIAL_STREAM_POSITION_STR_TO_ENUM = {
    "latest": INITIAL_STREAM_POSITION_LATEST,
    "trim_horizon": INITIAL_STREAM_POSITION_TRIM_HORIZON,
}

INITIAL_STREAM_POSITION_ENUM_TO_STR: Dict[str, Optional[str]] = {
    v: k for k, v in INITIAL_STREAM_POSITION_STR_TO_ENUM.items()
}
INITIAL_STREAM_POSITION_ENUM_TO_STR[INITIAL_STREAM_POSITION_UNSPECIFIED] = None

KAFKA_DEFAULT_MAX_OFFSETS_PER_TRIGGER = 100000

# Set of temporal Kafka consumer settings that will be set by the environment variables set in the
# cluster's `textproto` files.
#
# Defines maximum number of records (across all partitions) from Kafka to be consumed by a micro-batch.
KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV = "KAFKA_MAX_OFFSETS_PER_TRIGGER"
# Option to set starting timestamps for each Kafka partitions so that all of the Kafka's retention
# data is not processed. It's only relevant for the fist streaming job before the checkpoint exists on S3.
KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV = "KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST"
# Only necessary when KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV is set.
KAFKA_NUM_PARTITIONS_ENV = "KAFKA_NUM_PARTITIONS"

TEST_ONLY_UNITY_CATALOG_NAME = "TECTON_LOCAL_INTEGRATION_TEST_ONLY_UNITY_CATALOG"

KAFKA_STARTING_OFFSET_CONFIG_KEYS = {"startingOffsetsByTimestamp", "startingOffsets", KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV}


def _is_running_on_emr() -> bool:
    return (
        "EMR_RELEASE_LABEL" in os.environ
        or os.environ.get("TECTON_RUNTIME_ENV") == "EMR"
        or conf.get_or_none("TECTON_RUNTIME_ENV") == "EMR"
    )


def _get_raw_hive_table_dataframe(spark: PySparkSession, database: str, table: str) -> PySparkDataFrame:
    spark.sql("USE {}".format(database))
    return spark.table(table)


def _get_raw_unity_table_dataframe(spark: PySparkSession, catalog: str, schema: str, table: str) -> PySparkDataFrame:
    # USE CATALOG is only supported in databricks sql but not local pyspark
    # so we'd have to tweak for local integration tests to use "USE" sql statement
    # this means customers won't be able to use a unity catalog named "TECTON_LOCAL_INTEGRATION_TEST_ONLY_UNITY_CATALOG"
    if catalog == TEST_ONLY_UNITY_CATALOG_NAME:
        spark.sql(f"USE {catalog}")
    else:
        spark.sql(f"USE CATALOG {catalog}")
    spark.sql(f"USE {schema}")
    return spark.table(table)


@typechecked
def get_non_dsf_raw_dataframe(
    spark: PySparkSession,
    data_source: specs.BatchSourceSpec,
    called_for_schema_computation: bool = False,
) -> PySparkDataFrame:
    """Returns a DataFrame of the raw, untranslated data defined by the given BatchDataSource proto.

    :param spark: Spark session.
    :param data_source: BatchDataSource proto. BatchDataSource must not be a data source function (spark_batch_config).
    :param called_for_schema_computation: If set, optimizations are applied for faster schema computations.
                                          i.e. FileDSConfig.schema_uri is used to avoid expensive partition discovery.

    :return: The DataFrame for the raw data.
    """

    assert not isinstance(data_source, specs.SparkBatchSourceSpec), (
        "get_raw_dataframe can not be used with data source function (spark_batch_config)."
    )

    if isinstance(data_source, specs.HiveSourceSpec):
        df = _get_raw_hive_table_dataframe(spark, data_source.database, data_source.table)
    elif isinstance(data_source, specs.UnitySourceSpec):
        df = _get_raw_unity_table_dataframe(spark, data_source.catalog, data_source.schema, data_source.table)
    elif isinstance(data_source, specs.RedshiftSourceSpec):
        df = get_redshift_dataframe(
            spark,
            data_source.endpoint,
            data_source.temp_s3,
            data_source.table,
            data_source.query,
        )
    elif isinstance(data_source, specs.SnowflakeSourceSpec):
        df = get_snowflake_dataframe(
            spark,
            data_source.url,
            data_source.database,
            data_source.schema,
            data_source.warehouse,
            data_source.role,
            data_source.table,
            data_source.query,
        )
    elif isinstance(data_source, specs.FileSourceSpec):
        # FileDataSource
        reader = spark.read
        uri = data_source.uri
        if called_for_schema_computation and data_source.schema_uri:
            # Setting basePath includes the path-based partitions in the DataFrame schema.
            # https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#partition-discovery
            reader = reader.option("basePath", data_source.uri)
            uri = data_source.schema_uri

        if data_source.schema_override:
            schema = SparkSchemaWrapper.from_proto(data_source.schema_override)
            reader = reader.schema(schema.unwrap())

        if data_source.file_format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_JSON:

            def action():
                return reader.json(uri)

        elif data_source.file_format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_PARQUET:

            def action():
                return reader.parquet(uri)

        elif data_source.file_format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_CSV:

            def action():
                return reader.csv(uri, header=True)

        else:
            msg = f"Unsupported file format '{data_source.file_format}'"
            raise AssertionError(msg)

        df = tecton_spark.errors_spark.handleDataAccessErrors(action, data_source.uri)
        if data_source.convert_to_glue_format:
            df = convert_json_like_schema_to_glue_format(spark, df)
    elif isinstance(data_source, specs.PushTableSourceSpec):
        df = spark.read.format("delta").load(data_source.ingested_data_location)
    else:
        msg = f"Unexpected data source type for source {data_source}"
        raise ValueError(msg)

    return df


@typechecked
def get_table_dataframe(
    spark: PySparkSession,
    data_source: specs.BatchSourceSpec,
    called_for_schema_computation: bool = False,
) -> PySparkDataFrame:
    """Returns a DataFrame for a table defined by given BatchDataSource proto.

    :param spark: Spark session.
    :param data_source: BatchDataSource proto. BatchDataSource must not be a data source function (spark_batch_config).
    :param called_for_schema_computation: If set, optimizations are applied for faster schema computations.
                                          i.e. FileDSConfig.schema_uri is used to avoid expensive partition discovery.

    :return: The DataFrame created from the data source.
    """
    assert not isinstance(data_source, specs.SparkBatchSourceSpec), (
        f"get_table_dataframe can not be used with data source function (spark_batch_config). Data source: {data_source}"
    )

    df = get_non_dsf_raw_dataframe(spark, data_source, called_for_schema_computation)
    if data_source.post_processor:
        df = data_source.post_processor(df)
    if data_source.timestamp_field:
        df = apply_timestamp_column(df, data_source.timestamp_field, data_source.timestamp_format)

    return df


def get_redshift_dataframe(
    spark: PySparkSession, endpoint: str, temp_s3: str, table: Optional[str] = None, query: Optional[str] = None
) -> PySparkDataFrame:
    """Returns a DataFrame for a Redshift table defined by given RedshiftDataSource proto.

    :param table: The table name in redshift
    :param temp_s3: The s3 URI for temp data
    :param endpoint: The connection endpoint for redshift (without user or password)
    :param spark: Spark session.

    :return: The DataFrame created from the data source.
    """

    if _is_running_on_emr():
        spark_format = "io.github.spark_redshift_community.spark.redshift"
    else:
        spark_format = "com.databricks.spark.redshift"

    params = {"user": conf.get_or_raise("REDSHIFT_USER"), "password": conf.get_or_raise("REDSHIFT_PASSWORD")}
    full_connection_string = f"jdbc:redshift://{endpoint};user={params['user']};password={params['password']}"

    df_reader = (
        spark.read.format(spark_format)
        .option("url", full_connection_string)
        .option("tempdir", temp_s3)
        .option("forward_spark_s3_credentials", "true")
    )

    if table and query:
        msg = "Should only specify one of table and query sources for redshift"
        raise AssertionError(msg)
    if not table and not query:
        msg = "Missing both table and query sources for redshift, exactly one must be present"
        raise AssertionError(msg)

    if table:
        df_reader = df_reader.option("dbtable", table)
    else:
        df_reader = df_reader.option("query", query)

    df = df_reader.load()
    return df


CONNECTING_SNOWFLAKE_USING_SPARK_INSTRUCTIONS = "https://docs.tecton.ai/docs/setting-up-tecton/connecting-data-sources/connect-data-sources-to-spark/connecting-to-snowflake-using-spark"


def get_snowflake_dataframe(
    spark: PySparkSession,
    url: str,
    database: str,
    schema: str,
    warehouse: str,
    role: Optional[str] = None,
    table: Optional[str] = None,
    query: Optional[str] = None,
    spark_schema: Optional[StructType] = None,
) -> PySparkDataFrame:
    """Returns a Spark DataFrame from a Snowflake table or query.

    Casts the DataFrame to match spark_schema if it is specified.

    Requires the Spark-Snowflake connector JAR to be installed. See https://docs.snowflake.com/en/user-guide/spark-connector.
    """

    if (table and query) or (not table and not query):
        msg = "Exactly one of table and query must be specified."
        raise ValueError(msg)

    user = conf.get_or_none("SNOWFLAKE_USER")
    password = conf.get_or_none("SNOWFLAKE_PASSWORD")
    private_key = conf.get_or_none("SNOWFLAKE_PRIVATE_KEY")
    private_key_passphrase = conf.get_or_none("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
    missing_password_or_private_key = not (password or private_key)
    if not user or missing_password_or_private_key:
        msg = f"Snowflake user and private key not configured. Instructions at {CONNECTING_SNOWFLAKE_USING_SPARK_INSTRUCTIONS}"
        raise ValueError(msg)
    if password is not None and private_key is None:
        logger.warning(
            f"Snowflake will deprecate use of password authentication. Please use private key instead. Instructions at {CONNECTING_SNOWFLAKE_USING_SPARK_INSTRUCTIONS}"
        )

    options = {
        "sfUrl": url,
        "sfUser": user,
        "sfDatabase": database,
        "sfSchema": schema,
        "sfWarehouse": warehouse,
        "APPLICATION": "tecton-ai",
    }

    # let private_key take priority over password
    if private_key:
        pem_private_key = decrypt_private_key(private_key, private_key_passphrase)
        options["pem_private_key"] = base64.b64encode(pem_private_key).decode("utf-8")
    elif password:
        options["sfPassword"] = password

    if role:
        options["sfRole"] = role

    df_reader = spark.read.format("snowflake").options(**options)

    if table:
        df_reader = df_reader.option("dbtable", table)
    else:
        df_reader = df_reader.option("query", query)

    df = df_reader.load()
    if spark_schema is not None:
        for field in spark_schema:
            df = df.withColumn(field.name, functions.col(field.name).cast(field.dataType))
    return df


def apply_timestamp_column(df: PySparkDataFrame, ts_column: str, ts_format: Optional[str]) -> PySparkDataFrame:
    # Verify the raw source's timestamp column is of type "string"
    column_names = df.schema.names
    if ts_column not in column_names:
        msg = f"Timestamp Column '{ts_column}' not found in schema. Found: {column_names}"
        raise AssertionError(msg)

    ts_type = df.schema[ts_column].dataType.jsonValue()
    if ts_type != "timestamp":
        assert ts_type == "string", (
            f"Timestamp Column '{ts_column}' has type '{ts_type}', expected 'string' or 'timestamp'"
        )
        # Apply timestamp transform

        # Here we use coalesce to first try transforming string to timestamp using the user provided format,
        # and if it doesn't work we'll instead let Spark figure it out.
        # Ideally, if the user provided format didn't work, we would not fallback to the Spark default. However, it
        # would be difficult to remove this behavior, and it's hard to imagine a scenario where this would be a problem
        # other than being a bit too "magical". Ref: https://tecton.atlassian.net/browse/TEC-6611
        df = df.withColumn(ts_column, coalesce(to_timestamp(df[ts_column], ts_format), to_timestamp(df[ts_column])))

    return df


@typechecked
def apply_partition_and_timestamp_filter(
    df: PySparkDataFrame,
    batch_source: specs.BatchSourceSpec,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
) -> PySparkDataFrame:
    """Applies a partition and timestamp filters if the respective column names are set.

    :return: The DataFrame with filter applied.
    """

    # add datetime partition filters
    if isinstance(batch_source, specs.HiveSourceSpec) and batch_source.datetime_partition_columns:
        partition_filter = _build_partition_filter(batch_source.datetime_partition_columns, start_time, end_time)
        if partition_filter is not None:
            df = df.where(partition_filter)

    # add timestamp filter
    if batch_source.timestamp_field:
        ts_column = functions.col(batch_source.timestamp_field)
        if start_time:
            df = df.where(ts_column >= start_time)
        if end_time:
            df = df.where(ts_column < end_time)

    return df


# Generate filter on time_range with at most OR of 2 filters.
# This means we could end up scanning more partitions than necessary, but number extra scanned will be at most
# 3x.
# Worst case: time_range = 367 days across 3 years, we scan entire 3 years.
#             time_range = 365 days, we scan up to 2 years including that 1 year range
#             time_range = 28.1 days, we could scan all of January + February + March = 90 days
#
# 2 cases to consider
# Example: partition cols y, m, d, h: in both examples, the time range is between day and month, so we don't add any
# filters on hour, even though it would be possible to scan some fewer partitions if we did
# (A)Time range: 2020 Jan 10 10:00:00 AM - 2020 Jan 15 5:00:00 AM
#  --> (y = start.year & m = start.month & d >= start.day & d <= end.day)
# (B)Time range: 2019 Dec 21 10:00:00 AM - 2020 Jan 10 5:00:00 AM
#  --> ((y = start.year & m = start.month & d >= start.day) | (y = end.year & m = end.month & d <= end.day))
def _build_partition_filter(
    datetime_partition_columns: specs.DatetimePartitionColumnSpec,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
) -> PySparkColumn:
    if not start_time and not end_time:
        return None

    range_duration = end_time - start_time if start_time and end_time else None

    # Filters relating to start_time and end_time
    start_filters = []
    end_filters = []
    # Common filter that applies to the entire range
    common_filters = []

    # sort partition columns by the number of seconds they represent from highest to lowest
    partitions_high_to_low = sorted(datetime_partition_columns, key=lambda c: c.minimum_seconds, reverse=True)
    for partition in partitions_high_to_low:
        partition_col = functions.col(partition.column_name)
        partition_value_at_start = _partition_value_for_time(partition, start_time) if start_time else None
        partition_value_at_end = _partition_value_for_time(partition, end_time) if end_time else None
        # If partition's datepart minimum length is >= range_duration secs, we can be sure that 2 or fewer equality filters are enough to cover all possible times in time_limits
        # If range_duration is None/unbounded, always use range filter
        if range_duration and partition.minimum_seconds >= range_duration.total_seconds():
            if partition_value_at_start == partition_value_at_end:
                common_filters.append(partition_col == partition_value_at_start)
            else:
                start_filters.append(partition_col == partition_value_at_start)
                end_filters.append(partition_col == partition_value_at_end)
        # Otherwise, we need to use a range filter
        else:
            start_range_filter = partition_col >= partition_value_at_start if partition_value_at_start else None
            end_range_filter = partition_col <= partition_value_at_end if partition_value_at_end else None

            # Case A: there are only common filters
            if len(start_filters) == 0:
                if start_range_filter is not None:
                    common_filters.append(start_range_filter)
                if end_range_filter is not None:
                    common_filters.append(end_range_filter)
                # we can't combine range filters on multiple columns, so break and ignore any smaller columns
                break
            # Case B
            else:
                if start_range_filter is not None:
                    start_filters.append(start_range_filter)
                if end_range_filter is not None:
                    end_filters.append(end_range_filter)
                # we can't combine range filters on multiple columns, so break and ignore any smaller columns
                break

    common_filter = _and_filters_in_list(common_filters)
    start_filter = _and_filters_in_list(start_filters)
    end_filter = _and_filters_in_list(end_filters)
    return common_filter & (start_filter | end_filter)


def _partition_value_for_time(partition, time):
    fmt = partition.format_string
    # On mac/linux strftime supports these formats, but
    # Windows python does not
    # Zero-padded formats are safe for a string comparison. Otherwise we need to compare ints
    # As long as the values returned here are ints, the column will be implicitly converted if needed.
    if fmt == "%-Y":
        return time.year
    elif fmt == "%-m":
        return time.month
    elif fmt == "%-d":
        return time.day
    elif fmt == "%-H":
        return time.hour
    return time.strftime(fmt)


def _and_filters_in_list(filter_list):
    if len(filter_list) == 0:
        return functions.lit(True)
    else:
        from functools import reduce

        return reduce(lambda x, y: x & y, filter_list)


def create_kinesis_stream_reader(
    spark: PySparkSession,
    stream_source: specs.KinesisSourceSpec,
    option_overrides: Optional[Dict[str, str]],
) -> PySparkDataFrame:
    """
    Returns a DataFrame representing a Kinesis stream reader.

    :param option_overrides: Spark options that should override options set implicitly (e.g. ``stream_name``) or
        explicitly  (e.g. ``options``) by the data source definition.
    """
    options = {"streamName": stream_source.stream_name}
    initial_stream_position = _get_initial_stream_position(stream_source)
    if _is_running_on_emr():
        options.update(
            {
                "endpointUrl": f"https://kinesis.{stream_source.region}.amazonaws.com",
                "kinesis.client.describeShardInterval": "30s",
                "startingPosition": initial_stream_position,
            }
        )
    else:
        options.update(
            {"region": stream_source.region, "shardFetchInterval": "30s", "initialPosition": initial_stream_position}
        )

    databricks_to_qubole_map = {
        "awsaccesskey": "awsAccessKeyId",
        "rolearn": "awsSTSRoleARN",
        "rolesessionname": "awsSTSSessionName",
    }
    lowercase_data_source_options = {option.key.lower(): option.value for option in stream_source.options}
    for option in stream_source.options:
        if option.key.lower() in databricks_to_qubole_map and _is_running_on_emr():
            if option.key.lower() == "rolearn" and "rolesessionname" not in lowercase_data_source_options:
                # this field must be supplied if we use roleArn for qubole kinesis reader
                options["awsSTSSessionName"] = "tecton-materialization"
            options[databricks_to_qubole_map[option.key.lower()]] = option.value
        else:
            options[option.key] = option.value

    if option_overrides:
        options.update(option_overrides)

    reader = spark.readStream.format("kinesis").options(**options)
    return reader.load()


def create_kafka_stream_reader(
    spark: PySparkSession,
    stream_source: specs.KafkaSourceSpec,
    option_overrides: Optional[Dict[str, str]],
) -> PySparkDataFrame:
    """Returns a Kafka stream reader.

    :param data_source_options: Spark options specified in the data source definition.
    :param option_overrides: Spark options that should override options set implicitly (e.g. ``topics``) or explicitly
        (e.g. ``options``) by the data source definition.
    """
    options = {o.key: o.value for o in stream_source.options}
    options["kafka.bootstrap.servers"] = stream_source.bootstrap_servers
    options["subscribe"] = stream_source.topics

    if all(key not in options for key in KAFKA_STARTING_OFFSET_CONFIG_KEYS):
        # Don't override startingOffsets if it or similar option is set
        # explicitly in the data source definition.
        options["startingOffsets"] = "earliest"
        # Kafka by default consumes all the exisitng data into a single micro-batch, that can overwhelm
        # the Spark cluster during backfilling from a stream for the first time.
        # Set the default number of records to be read per micro-batch (across all partitions).
        options["maxOffsetsPerTrigger"] = str(KAFKA_DEFAULT_MAX_OFFSETS_PER_TRIGGER)
    options = _populate_kafka_consumer_options(stream_source.topics, options)

    if stream_source.ssl_keystore_location:
        local_keystore_loc, local_keystore_password = get_kafka_secrets(
            stream_source.ssl_keystore_location, stream_source.ssl_keystore_password_secret_id
        )
        options["kafka.ssl.keystore.location"] = local_keystore_loc
        if local_keystore_password:
            options["kafka.ssl.keystore.password"] = local_keystore_password
    if stream_source.ssl_truststore_location:
        local_truststore_loc, local_truststore_password = get_kafka_secrets(
            stream_source.ssl_truststore_location, stream_source.ssl_truststore_password_secret_id
        )
        options["kafka.ssl.truststore.location"] = local_truststore_loc
        if local_truststore_password:
            options["kafka.ssl.truststore.password"] = local_truststore_password
    if stream_source.security_protocol:
        options["kafka.security.protocol"] = stream_source.security_protocol

        # Hack: dynamic PLAIN SASL_SSL authentication when the
        # authentication is unset. Approved usage for Square until Data Source
        # Functions is launched.
        # TODO(TEC-9976): remove once Square is on Data Source Functions.
        if (
            stream_source.security_protocol == "SASL_SSL"
            and options.get("kafka.sasl.mechanism") == "PLAIN"
            and options.get("kafka.sasl.jaas.config") is None
        ):
            sasl_username = conf.get_or_none("SECRET_TECTON_KAFKA_SASL_USERNAME")
            sasl_password = conf.get_or_none("SECRET_TECTON_KAFKA_SASL_PASSWORD")
            kafka_sasl_jaas_config = f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username='{sasl_username}' password='{sasl_password}';"
            options["kafka.sasl.jaas.config"] = kafka_sasl_jaas_config

    if option_overrides:
        options.update(option_overrides)

    reader = spark.readStream.format("kafka").options(**options)
    return reader.load()


# This is a short term fix to unblock Kafka customers. We will replace these with proper FCO configurations.
# This function sets 2 Kafka consumer options `maxOffsetsPerTrigger` and `startingOffsetsByTimestamp` that
# are gatekept by the Environment variables set into the Spark cluster.
#  - The `maxOffsetsPerTrigger` represents the max number of records read into a SSS micro-batch.
#  - The `startingOffsetsByTimestamp` dynamically overrides the starting timestamps on the Kafka partitions
#    to limit the amount of data read from the Kafka data source.
def _populate_kafka_consumer_options(topics: str, kafka_options: Dict[str, Any]) -> Dict[str, Any]:
    max_offsets = os.environ.get(KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV)
    if max_offsets is not None:
        assert str.isdigit(max_offsets), f"{KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV} must be a string encoded integer"
        kafka_options["maxOffsetsPerTrigger"] = max_offsets

    num_hours_to_process = os.environ.get(KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV)
    if num_hours_to_process is not None:
        assert str.isdigit(num_hours_to_process), (
            f"{KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV} must be a string encoded integer"
        )
        num_partitions = os.environ.get(KAFKA_NUM_PARTITIONS_ENV)
        assert num_partitions is not None and str.isdigit(num_partitions), (
            f"{KAFKA_NUM_PARTITIONS_ENV} missing/invalid when {KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV} is set"
        )
        # `startingOffsetsByTimestamp` needs unix timestamps in millis per partition number.
        current_ts = int(time.time())
        starting_ts = (current_ts - int(num_hours_to_process) * 3600) * 1000
        ts_per_partition = {str(partition): starting_ts for partition in range(int(num_partitions))}
        topic_names = topics.split(",")
        starting_offsets_by_ts = dict.fromkeys(topic_names, ts_per_partition)
        kafka_options["startingOffsetsByTimestamp"] = json.dumps(starting_offsets_by_ts)

    return kafka_options


def get_non_dsf_raw_stream_dataframe(
    spark: PySparkSession, stream_data_source: specs.StreamSourceSpec, option_overrides: Optional[Dict[str, str]] = None
) -> PySparkDataFrame:
    """Returns a DataFrame representing the raw stream data.

    :param spark: Spark session.
    :param stream_data_source: StreamDataSource proto. StreamDataSource must not be a data source function (spark_stream_config).
    :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set by
        the data source.

    :return: The DataFrame for the raw stream data source.
    """
    if isinstance(stream_data_source, specs.KinesisSourceSpec):
        df = create_kinesis_stream_reader(
            spark,
            stream_data_source,
            option_overrides,
        )
    elif isinstance(stream_data_source, specs.KafkaSourceSpec):
        df = create_kafka_stream_reader(
            spark,
            stream_data_source,
            option_overrides,
        )
    else:
        msg = f"Unknown stream data source type: {stream_data_source}"
        raise ValueError(msg)
    return df


def get_stream_dataframe(
    spark: PySparkSession, stream_data_source: specs.StreamSourceSpec, option_overrides: Optional[Dict[str, str]] = None
) -> PySparkDataFrame:
    """Returns a DataFrame representing a stream data source *without* any options specified.
    Use get_stream_dataframe_with_options to get a DataFrame with stream-specific options.

    :param spark: Spark session.
    :param stream_data_source: StreamDataSource proto. StreamDataSource must not be a data source function (spark_stream_config).
    :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set by
        the data source.

    :return: The DataFrame created from the data source.
    """
    assert isinstance(stream_data_source, (specs.KinesisSourceSpec, specs.KafkaSourceSpec)), (
        "get_stream_dataframe can not be used with data source function (spark_stream_config)."
    )

    df = get_non_dsf_raw_stream_dataframe(spark, stream_data_source, option_overrides)
    return stream_data_source.post_processor(df)


def get_stream_dataframe_with_options(
    spark: PySparkSession, stream_data_source: specs.StreamSourceSpec, option_overrides: Optional[Dict[str, str]] = None
) -> PySparkDataFrame:
    """Returns a DataFrame representing a stream data source with additional options:
        - drop duplicate column names
        - initial stream position

    :param spark: Spark session.
    :param stream_data_source: StreamDataSource proto. StreamDataSource must not be a data source function (spark_stream_config).
    :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set by
        the data source.

    :return: The DataFrame created from the data source.
    """
    assert not isinstance(stream_data_source, specs.SparkStreamSourceSpec), (
        "get_stream_dataframe_with_options can not be used with data source function (spark_stream_config)."
    )

    df = get_stream_dataframe(spark, stream_data_source, option_overrides)

    dedup_columns = list(stream_data_source.deduplication_column_names)
    if dedup_columns:
        df = df.dropDuplicates(dedup_columns)

    return df


def _get_initial_stream_position(stream_data_source: specs.StreamSourceSpec) -> Optional[str]:
    """Returns initial stream position as a string (e.g. "latest") for the streaming data source.

    :param stream_data_source: StreamDataSource proto.

    :return: The initial stream position in string format.
    """
    if isinstance(stream_data_source, specs.KinesisSourceSpec):
        return INITIAL_STREAM_POSITION_ENUM_TO_STR[stream_data_source.initial_stream_position]
    else:
        return None


@typechecked
def get_ds_dataframe(
    spark: PySparkSession,
    data_source: specs.DataSourceSpec,
    consume_streaming_data_source: bool,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    called_for_schema_computation: bool = False,
    stream_option_overrides: Optional[Dict[str, str]] = None,
) -> PySparkDataFrame:
    if consume_streaming_data_source and (start_time or end_time):
        msg = "Can't specify start or end time when consuming streaming data source"
        raise AssertionError(msg)

    if consume_streaming_data_source:
        assert data_source.stream_source, (
            f"Can't consume streaming data source from the data source: {data_source.name}."
        )

        if isinstance(data_source.stream_source, specs.SparkStreamSourceSpec):
            df = data_source.stream_source.function(spark)
        else:
            df = get_stream_dataframe_with_options(spark, data_source.stream_source, stream_option_overrides)
    else:
        if isinstance(data_source.batch_source, specs.SparkBatchSourceSpec):
            df = get_data_source_function_batch_dataframe(
                spark, data_source.batch_source, start_time=start_time, end_time=end_time
            )
        else:
            df = get_table_dataframe(
                spark, data_source.batch_source, called_for_schema_computation=called_for_schema_computation
            )
            if start_time or end_time:
                df = apply_partition_and_timestamp_filter(df, data_source.batch_source, start_time, end_time)

        if data_source.type == DataSourceType.STREAM_WITH_BATCH:
            schema = data_source.stream_source.spark_schema
            # Since 0.8, data source schema is optionally derived. If all feature views that depends on a data source have `run_transformation_validation=False`, the data source schema is not derived.
            if schema.fields:
                cols = [field.name for field in schema.fields]
                df = df.select(*cols)
        elif data_source.type in (DataSourceType.PUSH_NO_BATCH, DataSourceType.PUSH_WITH_BATCH):
            schema = data_source.schema.tecton_schema
            cols = [f"`{c.name}`" for c in schema.columns]
            df = df.select(*cols)

    return df


def convert_json_like_schema_to_glue_format(spark: PySparkSession, df: PySparkDataFrame) -> PySparkDataFrame:
    """
    Converts a DataFrame schema to lowercase. This assumes JSON so
    MapTypes or Arrays of non-StructTypes are not allowed.

    :param spark: Spark session.
    :param df: DataFrame input.
    :return: DataFrame with lowercase schema.
    """

    def _get_lowercase_schema(datatype: DataType) -> DataType:
        if isinstance(datatype, ArrayType):
            return _get_lowercase_array_schema(datatype)
        elif isinstance(datatype, StructType):
            return _get_lowercase_structtype_schema(datatype)
        elif isinstance(col.dataType, MapType):
            msg = "MapType not supported in JSON schema"
            raise TypeError(msg)
        return datatype

    def _get_lowercase_structtype_schema(s: StructType) -> StructType:
        assert isinstance(s, StructType), f"Invalid argument type {type(s)}, expected StructType"
        struct_fields = []
        for col in s:
            datatype = _get_lowercase_schema(col.dataType)
            struct_fields.append(StructField(col.name.lower(), datatype))
        return StructType(struct_fields)

    def _get_lowercase_array_schema(c: ArrayType) -> ArrayType:
        assert isinstance(c.elementType, StructType), (
            f"Invalid ArrayType element type {type(c)}, expected StructType for valid JSON arrays."
        )
        datatype = c.elementType
        struct_schema = _get_lowercase_structtype_schema(datatype)
        return ArrayType(struct_schema)

    # Simple columns (LongType, StringType, etc) can just be renamed without
    # casting schema.
    # Nested fields within complex columns (ArrayType, StructType) must also be recursively converted
    # to lowercase names, so they must be casted.
    # DateType columns should be converted to StringType to match Glue schemas.
    new_fields = []
    for col in df.schema:
        if type(col.dataType) in [ArrayType, StructType, MapType]:
            t = _get_lowercase_schema(col.dataType)
            new_fields.append(functions.col(col.name).cast(t).alias(col.name.lower()))
        elif type(col.dataType) is DateType:
            new_fields.append(functions.col(col.name).cast(StringType()).alias(col.name.lower()))
        else:
            new_fields.append(functions.col(col.name).alias(col.name.lower()))
    return df.select(new_fields)


def get_data_source_function_batch_dataframe(
    spark: PySparkSession,
    data_source: specs.SparkBatchSourceSpec,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
) -> PySparkDataFrame:
    if data_source.supports_time_filtering:
        filter_context = FilterContext(start_time, end_time)
        return data_source.function(spark, filter_context)
    return data_source.function(spark)
