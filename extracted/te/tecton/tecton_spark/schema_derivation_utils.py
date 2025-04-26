"""Utilities for deriving data source and feature view schemas. Shared by backend and local schema derivation."""

import datetime
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Sequence

import pyspark
from pyspark.sql import types as pyspark_types
from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import errors as core_errors
from tecton_core import filter_context
from tecton_core import specs
from tecton_core.id_helper import IdHelper
from tecton_core.spark_type_annotations import PySparkDataFrame
from tecton_core.spark_type_annotations import PySparkSession
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.args import feature_view__client_pb2 as feature_view_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as virtual_data_source__args_pb2
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.common import spark_schema__client_pb2 as spark_schema_pb2
from tecton_proto.common.data_source_type__client_pb2 import DataSourceType
from tecton_spark import data_source_helper
from tecton_spark import errors_spark
from tecton_spark import schema_spark_utils
from tecton_spark import spark_schema_wrapper
from tecton_spark.spark_pipeline import SparkFeaturePipeline
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


@typechecked
def get_hive_table_schema(
    spark: PySparkSession,
    database: str,
    table: str,
    post_processor: Optional[Callable],
    timestamp_field: str,
    timestamp_format: str,
) -> spark_schema_pb2.SparkSchema:
    df = data_source_helper._get_raw_hive_table_dataframe(spark, database, table)
    if post_processor is not None:
        df = post_processor(df)
    if timestamp_field:
        ts_format = None
        if timestamp_format:
            ts_format = timestamp_format
        df = data_source_helper.apply_timestamp_column(df, timestamp_field, ts_format)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


def get_unity_table_schema(
    spark: PySparkSession,
    catalog: str,
    schema: str,
    table: str,
    post_processor: Optional[Callable],
    timestamp_field: str,
    timestamp_format: str,
) -> spark_schema_pb2.SparkSchema:
    df = data_source_helper._get_raw_unity_table_dataframe(spark, catalog, schema, table)
    if post_processor is not None:
        df = post_processor(df)
    if timestamp_field:
        ts_format = None
        if timestamp_format:
            ts_format = timestamp_format
        df = data_source_helper.apply_timestamp_column(df, timestamp_field, ts_format)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_redshift_table_schema(
    spark: PySparkSession,
    endpoint: str,
    table: str,
    query: str,
    temp_s3: str,
    post_processor: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    df = data_source_helper.get_redshift_dataframe(spark, endpoint, temp_s3, table=table, query=query)
    if post_processor is not None:
        df = post_processor(df)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_snowflake_schema(
    spark: PySparkSession,
    url: str,
    database: str,
    schema: str,
    warehouse: str,
    role: Optional[str],
    table: Optional[str],
    query: Optional[str],
    post_processor: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    assert table is not None or query is not None, "Both table and query cannot be None"

    df = data_source_helper.get_snowflake_dataframe(
        spark,
        url,
        database,
        schema,
        warehouse,
        role=role,
        table=table,
        query=query,
    )
    if post_processor is not None:
        df = post_processor(df)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_batch_data_source_function_schema(
    spark: PySparkSession, data_source_function: Callable, supports_time_filtering: bool
) -> spark_schema_pb2.SparkSchema:
    if supports_time_filtering:
        df_fc_none = data_source_function(spark=spark, filter_context=None)
        df_fc_none_start_none_end = data_source_function(
            spark=spark, filter_context=filter_context.FilterContext(None, None)
        )
        df_fc_none_end = data_source_function(
            spark=spark, filter_context=filter_context.FilterContext(pendulum.datetime(1970, 1, 1), None)
        )
        df_fc_none_start = data_source_function(
            spark=spark, filter_context=filter_context.FilterContext(None, pendulum.now())
        )
        schema = df_fc_none.schema
        # Verify filter_context is handled correctly. Schema should be the same for all values of filter_context.
        filter_context_error_message = (
            f"Invalid handling of filter_context and time filtering. Data Source Function {data_source_function.__name__} "
            f"needs to return a Spark DataFrame with the same schema for all values of filter_context"
        )
        assert all(
            df.schema == schema for df in [df_fc_none_start_none_end, df_fc_none_end, df_fc_none_start]
        ), filter_context_error_message

        df = df_fc_none
    else:
        df = data_source_function(spark=spark)
    assert is_pyspark_df(df), "Data Source Function must return a Spark DataFrame"
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


def get_file_source_schema(
    spark: PySparkSession,
    file_format: str,
    file_uri: str,
    convert_to_glue: bool,
    schema_uri: Optional[str],
    schema_override: Optional[spark_schema_wrapper.SparkSchemaWrapper],
    post_processor: Optional[Callable],
    timestamp_col: Optional[str],
    timestmap_format: Optional[str],
) -> spark_schema_pb2.SparkSchema:
    reader = spark.read
    if schema_uri is not None:
        uri = schema_uri
        assert schema_uri.startswith(file_uri), f"{schema_uri} must contain {file_uri}"
        # Setting basePath includes the path-based partitions in the DataFrame schema.
        # https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#partition-discovery
        reader = reader.option("basePath", file_uri)
    else:
        uri = file_uri

    if schema_override is not None:
        reader = reader.schema(schema_override.unwrap())

    if file_format == "json":

        def action():
            return reader.json(uri)

    elif file_format == "parquet":

        def action():
            return reader.parquet(uri)

    elif file_format == "csv":

        def action():
            return reader.csv(uri, header=True)

    else:
        msg = f"Unsupported file format '{file_format}'"
        raise AssertionError(msg)

    df = errors_spark.handleDataAccessErrors(action, file_uri)

    if convert_to_glue:
        df = data_source_helper.convert_json_like_schema_to_glue_format(spark, df)
    if post_processor is not None:
        df = post_processor(df)

    if timestamp_col is not None:
        df = data_source_helper.apply_timestamp_column(df, timestamp_col, timestmap_format)

    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_kinesis_schema(
    spark: PySparkSession, stream_name: str, post_processor: Callable
) -> spark_schema_pb2.SparkSchema:
    """Compute the Kinesis schema using mock Kinesis data.

    Creates a mocked DataFrame for this stream, without actually creating a stream reader.
    This method returns a message in the Kinesis message format (below) with mocked contents.

    |-- approximateArrivalTimestamp: timestamp
    |-- data: binary
    |-- partitionKey: string
    |-- sequenceNumber: string
    |-- streamName: string
    """
    row = pyspark.Row(
        data=bytearray("no_data", "utf-8"),
        streamName=stream_name,
        partitionKey="0",
        sequenceNumber="0",
        approximateArrivalTimestamp=datetime.datetime.fromtimestamp(0),
    )
    df = spark.createDataFrame([row])

    df = post_processor(df)

    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


# https://docs.databricks.com/spark/latest/structured-streaming/kafka.html
KAFKA_SCHEMA = pyspark_types.StructType(
    [
        pyspark_types.StructField("key", pyspark_types.BinaryType(), True),
        pyspark_types.StructField("value", pyspark_types.BinaryType(), True),
        pyspark_types.StructField("topic", pyspark_types.StringType(), True),
        pyspark_types.StructField("partition", pyspark_types.IntegerType(), True),
        pyspark_types.StructField("offset", pyspark_types.LongType(), True),
        pyspark_types.StructField("timestamp", pyspark_types.TimestampType(), True),
        pyspark_types.StructField("timestampType", pyspark_types.IntegerType(), True),
    ]
)


@typechecked
def get_kafka_schema(spark: PySparkSession, post_processor: Callable) -> spark_schema_pb2.SparkSchema:
    """Compute the Kafka schema using mock Kafka data."""
    df = spark.createDataFrame([], KAFKA_SCHEMA)
    df = post_processor(df)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_stream_data_source_function_schema(
    spark: PySparkSession, data_source_fn: Callable
) -> spark_schema_pb2.SparkSchema:
    """Compute the Kafka schema using mock Kafka data."""
    df = data_source_fn(spark=spark)
    assert is_pyspark_df(df) and df.isStreaming, "Data Source Function must return a streaming Spark DataFrame"
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_feature_view_view_schema(
    spark: PySparkSession,
    feature_view: feature_view_pb2.FeatureViewArgs,
    transformations: Sequence[specs.TransformationSpec],
    data_sources: Sequence[specs.DataSourceSpec],
) -> schema_pb2.Schema:
    """Compute the Feature View view schema."""
    has_push_source = False
    for data_source in data_sources:
        if data_source.type == DataSourceType.PUSH_WITH_BATCH or data_source.type == DataSourceType.PUSH_NO_BATCH:
            has_push_source = True
            break
    # This schema is only set for Stream Feature Views with PushSources.
    if feature_view.materialized_feature_view_args.schema and has_push_source and len(transformations) > 0:
        return feature_view.materialized_feature_view_args.schema
    df = get_feature_view_empty_view_df(spark, feature_view, transformations, data_sources)
    return schema_spark_utils.schema_from_spark(df.schema).to_proto()


@typechecked
def get_feature_view_empty_view_df(
    spark: PySparkSession,
    feature_view: feature_view_pb2.FeatureViewArgs,
    transformations: Sequence[specs.TransformationSpec],
    data_sources: Sequence[specs.DataSourceSpec],
) -> PySparkDataFrame:
    """Return a pyspark dataframe for the feature view "view" (i.e. before agggregations) using mock/empty data."""
    # Create empty data frames for each DS input matching the DS schema.
    id_to_ds = {ds.id: ds for ds in data_sources}
    empty_mock_inputs = populate_empty_passed_in_inputs(feature_view.pipeline.root, id_to_ds, spark)

    spark_pipeline = SparkFeaturePipeline(
        spark,
        pipeline=feature_view.pipeline,
        transformations=transformations,
        schedule_interval=_batch_schedule_from_fv(feature_view),
        data_source_inputs=empty_mock_inputs,
    )
    return spark_pipeline.to_dataframe()


def _batch_schedule_from_fv(feature_view: feature_view_pb2.FeatureViewArgs) -> Optional[pendulum.Duration]:
    if feature_view.HasField("materialized_feature_view_args"):
        return pendulum.Duration(seconds=feature_view.materialized_feature_view_args.batch_schedule.ToSeconds())
    else:
        return None


def derive_batch_schema(
    spark: PySparkSession,
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    batch_post_processor: Optional[Callable],
    batch_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    if ds_args.HasField("hive_ds_config"):
        return get_hive_table_schema(
            spark=spark,
            table=ds_args.hive_ds_config.table,
            database=ds_args.hive_ds_config.database,
            post_processor=batch_post_processor,
            timestamp_field=ds_args.hive_ds_config.common_args.timestamp_field,
            timestamp_format=ds_args.hive_ds_config.timestamp_format,
        )
    elif ds_args.HasField("unity_ds_config"):
        return get_unity_table_schema(
            spark=spark,
            catalog=ds_args.unity_ds_config.catalog,
            schema=ds_args.unity_ds_config.schema,
            table=ds_args.unity_ds_config.table,
            post_processor=batch_post_processor,
            timestamp_field=ds_args.unity_ds_config.common_args.timestamp_field,
            timestamp_format=ds_args.unity_ds_config.timestamp_format,
        )
    elif ds_args.HasField("spark_batch_config"):
        return get_batch_data_source_function_schema(
            spark=spark,
            data_source_function=batch_data_source_function,
            supports_time_filtering=ds_args.spark_batch_config.supports_time_filtering,
        )
    elif ds_args.HasField("redshift_ds_config"):
        if not ds_args.redshift_ds_config.HasField("endpoint"):
            msg = "redshift"
            raise core_errors.DS_ARGS_MISSING_FIELD(msg, "endpoint")

        has_table = ds_args.redshift_ds_config.HasField("table") and ds_args.redshift_ds_config.table
        has_query = ds_args.redshift_ds_config.HasField("query") and ds_args.redshift_ds_config.query
        if (has_table and has_query) or (not has_table and not has_query):
            raise core_errors.REDSHIFT_DS_EITHER_TABLE_OR_QUERY
        temp_s3 = conf.get_or_none("SPARK_REDSHIFT_TEMP_DIR")
        if temp_s3 is None:
            raise core_errors.REDSHIFT_DS_MISSING_SPARK_TEMP_DIR

        return get_redshift_table_schema(
            spark=spark,
            endpoint=ds_args.redshift_ds_config.endpoint,
            table=ds_args.redshift_ds_config.table,
            query=ds_args.redshift_ds_config.query,
            temp_s3=temp_s3,
            post_processor=batch_post_processor,
        )
    elif ds_args.HasField("snowflake_ds_config"):
        if not ds_args.snowflake_ds_config.HasField("url"):
            msg = "snowflake"
            raise core_errors.DS_ARGS_MISSING_FIELD(msg, "url")
        if not ds_args.snowflake_ds_config.HasField("database"):
            msg = "snowflake"
            raise core_errors.DS_ARGS_MISSING_FIELD(msg, "database")
        if not ds_args.snowflake_ds_config.HasField("schema"):
            msg = "snowflake"
            raise core_errors.DS_ARGS_MISSING_FIELD(msg, "schema")
        if not ds_args.snowflake_ds_config.HasField("warehouse"):
            msg = "snowflake"
            raise core_errors.DS_ARGS_MISSING_FIELD(msg, "warehouse")

        return get_snowflake_schema(
            spark=spark,
            url=ds_args.snowflake_ds_config.url,
            database=ds_args.snowflake_ds_config.database,
            schema=ds_args.snowflake_ds_config.schema,
            warehouse=ds_args.snowflake_ds_config.warehouse,
            role=ds_args.snowflake_ds_config.role if ds_args.snowflake_ds_config.HasField("role") else None,
            table=ds_args.snowflake_ds_config.table if ds_args.snowflake_ds_config.HasField("table") else None,
            query=ds_args.snowflake_ds_config.query if ds_args.snowflake_ds_config.HasField("query") else None,
            post_processor=batch_post_processor,
        )
    elif ds_args.HasField("file_ds_config"):
        schema_override = None
        if ds_args.file_ds_config.HasField("schema_override"):
            schema_override = spark_schema_wrapper.SparkSchemaWrapper.from_proto(ds_args.file_ds_config.schema_override)

        schema_uri = ds_args.file_ds_config.schema_uri if ds_args.file_ds_config.HasField("schema_uri") else None
        timestamp_column = (
            ds_args.file_ds_config.common_args.timestamp_field
            if ds_args.file_ds_config.common_args.HasField("timestamp_field")
            else None
        )
        timestamp_format = (
            ds_args.file_ds_config.timestamp_format if ds_args.file_ds_config.HasField("timestamp_format") else None
        )

        return get_file_source_schema(
            spark=spark,
            file_format=ds_args.file_ds_config.file_format,
            file_uri=ds_args.file_ds_config.uri,
            convert_to_glue=ds_args.file_ds_config.convert_to_glue_format,
            schema_uri=schema_uri,
            schema_override=schema_override,
            post_processor=batch_post_processor,
            timestamp_col=timestamp_column,
            timestmap_format=timestamp_format,
        )
    else:
        msg = f"Invalid batch source args: {ds_args}"
        raise ValueError(msg)


def derive_stream_schema(
    spark: PySparkSession,
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    stream_post_processor: Optional[Callable],
    stream_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    if ds_args.HasField("kinesis_ds_config"):
        return get_kinesis_schema(spark, ds_args.kinesis_ds_config.stream_name, stream_post_processor)
    elif ds_args.HasField("kafka_ds_config"):
        return get_kafka_schema(spark, stream_post_processor)
    elif ds_args.HasField("spark_stream_config"):
        return get_stream_data_source_function_schema(spark, stream_data_source_function)
    else:
        msg = f"Invalid stream source args: {ds_args}"
        raise ValueError(msg)


# Constructs empty data frames matching schema of DS inputs for the purpose of
# schema-validating the transformation pipeline.
def populate_empty_passed_in_inputs(
    node: PipelineNode,
    ds_map: Dict[str, specs.DataSourceSpec],
    spark: PySparkSession,
) -> Dict[str, PySparkDataFrame]:
    empty_passed_in_inputs = {}
    _populate_empty_passed_in_inputs_helper(node, empty_passed_in_inputs, ds_map, spark)
    return empty_passed_in_inputs


def _populate_empty_passed_in_inputs_helper(
    node: PipelineNode,
    empty_passed_in_inputs: Dict[str, PySparkDataFrame],
    ds_map: Dict[str, specs.DataSourceSpec],
    spark: PySparkSession,
) -> None:
    if node.HasField("data_source_node"):
        ds_id = IdHelper.to_string(node.data_source_node.virtual_data_source_id)
        ds_spec = ds_map[ds_id]
        assert (
            ds_spec.type != DataSourceType.PUSH_NO_BATCH
        ), "This utility does not support FeatureView with PushSources that do not have a batch_config"
        ds_schema = ds_spec.batch_source.spark_schema
        empty_passed_in_inputs[node.data_source_node.input_name] = spark.createDataFrame(
            [], SparkSchemaWrapper.from_proto(ds_schema).unwrap()
        )
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _populate_empty_passed_in_inputs_helper(child.node, empty_passed_in_inputs, ds_map, spark)
