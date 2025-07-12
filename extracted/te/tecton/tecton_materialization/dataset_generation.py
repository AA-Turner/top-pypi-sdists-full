import logging

from tecton_core.compute_mode import ComputeMode
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.query.rewrite import rewrite_tree_for_spine
from tecton_core.query_consts import valid_to
from tecton_materialization.common.dataset_generation import get_features_from_params
from tecton_materialization.common.task_params import get_features_params_from_task_params
from tecton_spark.offline_store import OfflineStoreWriterParams
from tecton_spark.offline_store import get_dataset_generation_writer
from tecton_spark.query import translate
from tecton_spark.query.translate import SparkDataFrame


logger = logging.getLogger(__name__)

# Maximum number of output partitions to control the number of output files. This limits Spark partitions to control
# total file count to improve read performance.
# The context is: For each Spark partition, one file will be written per time partition. E.g. with 100 Spark partitions
# and 100 time partitions, up to 10_000 files could be written.
DEFAULT_MAX_PARTITIONS = 10


def dataset_generation_from_params(spark, materialization_task_params):
    dataset_generation_params = materialization_task_params.dataset_generation_task_info.dataset_generation_parameters
    params = get_features_params_from_task_params(materialization_task_params, compute_mode=ComputeMode.SPARK)
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"datasetPath":"{dataset_generation_params.result_path}"}}',
    )
    if isinstance(params, GetFeaturesForEventsParams):
        time_column = params.timestamp_key
        spine = SparkDataFrame(spark.read.parquet(params.events))
        qt = get_features_from_params(params, spine=spine)
    elif isinstance(params, GetFeaturesInRangeParams):
        time_column = valid_to()
        entities = SparkDataFrame(spark.read.parquet(params.entities)) if params.entities is not None else None
        qt = get_features_from_params(params, entities=entities)
    else:
        error = f"Unsupported params type: {type(params)}"
        raise ValueError(error)

    rewrite_tree_for_spine(qt)
    logger.info(f"Starting dataset generation job for '{params.fco.name}'")
    logger.info(f"QT: \n{qt.pretty_str(columns=True)}")

    spark_df = translate.spark_convert(qt, spark).to_dataframe(spark)

    spark_df = _reduce_spark_partitions(spark_df)

    writer_params = OfflineStoreWriterParams(
        s3_path=dataset_generation_params.result_path,
        always_store_anchor_column=False,
        time_column=time_column,
        join_key_columns=params.join_keys,
        is_continuous=False,
        upsert_by_batch_publish_timestamp=False,
    )

    logger.info("Writing results to %s", dataset_generation_params.result_path)

    delta_writer = get_dataset_generation_writer(writer_params, spark)
    delta_writer.append_dataframe(spark_df)


def _reduce_spark_partitions(spark_df):
    current_partitions = spark_df.rdd.getNumPartitions()
    reduced_partitions = min(DEFAULT_MAX_PARTITIONS, current_partitions)
    logger.info(f"Reducing partitions from {current_partitions} to {reduced_partitions}")
    return spark_df.coalesce(reduced_partitions)
