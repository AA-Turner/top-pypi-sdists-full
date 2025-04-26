import tempfile
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import pandas
from pyspark import sql as pyspark_sql
from pyspark.sql import streaming as pyspark_streaming

from tecton import tecton_context
from tecton._internals import ingest_utils
from tecton.framework.data_frame import TectonDataFrame
from tecton.tecton_context import TectonContext
from tecton_core import materialization_context
from tecton_core import schema
from tecton_core import specs
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.args import feature_view__client_pb2 as feature_view_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.common import spark_schema__client_pb2 as spark_schema_pb2
from tecton_spark import data_source_helper
from tecton_spark import feature_view_spark_utils
from tecton_spark import schema_derivation_utils
from tecton_spark import schema_spark_utils
from tecton_spark import spark_schema_wrapper


_CHECKPOINT_DIRECTORIES: List[tempfile.TemporaryDirectory] = []


def _get_checkpoint_dir_name(checkpoint_dir: Optional[str] = None) -> str:
    # Set a tempdir checkpointLocation. This is needed for the stream preview to work in EMR notebooks. The
    # TemporaryDirectory object handles cleaning up the temporary directory when it is destroyed, so add the object to
    # a global list that will be cleaned up with the program exits. (This isn't guaranteed - but it's not the end of
    # the world if we leak some temporary directories.)
    d = tempfile.TemporaryDirectory(dir=checkpoint_dir)
    _CHECKPOINT_DIRECTORIES.append(d)
    return d.name


def start_stream_preview(
    data_source: specs.DataSourceSpec,
    table_name: str,
    apply_translator: bool,
    option_overrides: Optional[Dict[str, str]],
    checkpoint_dir: Optional[str],
) -> pyspark_streaming.StreamingQuery:
    df = get_stream_preview_dataframe(data_source, apply_translator, option_overrides)
    return (
        df.writeStream.format("memory")
        .queryName(table_name)
        .option("checkpointLocation", _get_checkpoint_dir_name(checkpoint_dir))
        .outputMode("append")
        .start()
    )


def get_stream_preview_dataframe(
    data_source: specs.DataSourceSpec, apply_translator: bool, option_overrides: Optional[Dict[str, str]]
) -> pyspark_sql.DataFrame:
    """
    Helper function that allows start_stream_preview() to be unit tested, since we can't easily unit test writing
    to temporary tables.
    """
    spark = tecton_context.TectonContext.get_instance()._spark

    if apply_translator or isinstance(data_source.stream_source, specs.SparkStreamSourceSpec):
        return data_source_helper.get_ds_dataframe(
            spark, data_source, consume_streaming_data_source=True, stream_option_overrides=option_overrides
        )
    else:
        return data_source_helper.get_non_dsf_raw_stream_dataframe(spark, data_source.stream_source, option_overrides)


def derive_view_schema_for_feature_view(
    fv_args: feature_view_pb2.FeatureViewArgs,
    transformations: Sequence[specs.TransformationSpec],
    data_sources: Sequence[specs.DataSourceSpec],
) -> schema_pb2.Schema:
    spark = TectonContext.get_instance()._spark
    return schema_derivation_utils.get_feature_view_view_schema(spark, fv_args, transformations, data_sources)


def spark_schema_to_tecton_schema(spark_schema: spark_schema_pb2.SparkSchema) -> schema_pb2.Schema:
    wrapper = spark_schema_wrapper.SparkSchemaWrapper.from_proto(spark_schema)
    return schema_spark_utils.schema_from_spark(wrapper.unwrap()).proto


def derive_batch_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    batch_post_processor: Optional[Callable],
    batch_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    spark = TectonContext.get_instance()._spark
    return schema_derivation_utils.derive_batch_schema(spark, ds_args, batch_post_processor, batch_data_source_function)


def derive_stream_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    stream_post_processor: Optional[Callable],
    stream_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    spark = TectonContext.get_instance()._spark
    return schema_derivation_utils.derive_stream_schema(
        spark, ds_args, stream_post_processor, stream_data_source_function
    )


_TRANSFORMATION_RUN_TEMP_VIEW_PREFIX = "_tecton_transformation_run_"
CONST_TYPE = Union[str, int, float, bool]


def run_transformation_mode_spark_sql(
    *inputs: Union[pandas.DataFrame, pandas.Series, TectonDataFrame, pyspark_sql.DataFrame, CONST_TYPE],
    transformer: Callable,
    context: materialization_context.MaterializationContext = None,
    transformation_name: str,
) -> TectonDataFrame:
    def create_temp_view(df, dataframe_index) -> str:
        df = TectonDataFrame._create(df).to_spark()
        temp_view = f"{_TRANSFORMATION_RUN_TEMP_VIEW_PREFIX}{transformation_name}_input_{dataframe_index}"
        df.createOrReplaceTempView(temp_view)
        return temp_view

    args = [create_temp_view(v, i) if not isinstance(v, CONST_TYPE.__args__) else v for i, v in enumerate(inputs)]
    if context is not None:
        args.append(context)

    spark = TectonContext.get_instance()._get_spark()
    return TectonDataFrame._create(spark.sql(transformer(*args)))


def run_transformation_mode_pyspark(
    *inputs: Union[pandas.DataFrame, pandas.Series, TectonDataFrame, pyspark_sql.DataFrame, CONST_TYPE],
    transformer: Callable,
    context: materialization_context.MaterializationContext,
) -> TectonDataFrame:
    args = [TectonDataFrame._create(v).to_spark() if not isinstance(v, CONST_TYPE.__args__) else v for v in inputs]
    if context is not None:
        args.append(context)

    return TectonDataFrame._create(transformer(*args))


def write_dataframe_to_path_or_url(
    df: Union[pyspark_sql.DataFrame, pandas.DataFrame],
    df_path: Optional[str],
    upload_url: Optional[str],
    view_schema: schema.Schema,
    enable_schema_validation: bool = False,
):
    """Used for Feature Table ingest and deleting keys."""
    # We write in the native format and avoid converting Pandas <-> Spark due to partially incompatible
    # type system, in specifically missing Int in Pandas
    if is_pyspark_df(df):
        if enable_schema_validation:
            feature_view_spark_utils.validate_df_columns_and_feature_types(df, view_schema)
        df.write.parquet(df_path)
        return

    if upload_url:
        # Currently, we don't validate the schema for Pandas DataFrames because we don't have a good way to map Pandas
        # types to Tecton types yet. The validation is done for Spark DataFrames in
        # `feature_view_spark_utils.validate_df_columns_and_feature_types`
        ingest_utils.upload_df_pandas(upload_url, df)
    elif df_path:
        spark_df = ingest_utils.convert_pandas_to_spark_df(df, view_schema)
        if enable_schema_validation:
            feature_view_spark_utils.validate_df_columns_and_feature_types(spark_df, view_schema)
        spark_df.write.parquet(df_path)
