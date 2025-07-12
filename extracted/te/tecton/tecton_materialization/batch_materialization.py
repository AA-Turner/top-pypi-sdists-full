import datetime
import logging
import time
from typing import List

from google.protobuf.timestamp_pb2 import Timestamp
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import explode
from pyspark.sql.functions import expr
from pyspark.sql.functions import lit
from pyspark.sql.functions import row_number
from pyspark.sql.types import LongType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.utils import AnalysisException
from pyspark.sql.window import Window

import tecton_core.tecton_pendulum as pendulum
from tecton_core import specs
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.id_helper import IdHelper
from tecton_core.offline_store import OfflineStoreType
from tecton_core.offline_store import get_offline_store_partition_params
from tecton_core.offline_store import get_offline_store_type
from tecton_core.offline_store import get_time_column_for_offline_writer
from tecton_core.query_consts import anchor_time
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.common.task_params import job_query_intervals
from tecton_materialization.consumption import export_consumption_debug_metrics
from tecton_materialization.consumption import export_consumption_metrics
from tecton_materialization.job_metadata import is_checkpoint_complete
from tecton_materialization.job_metadata import write_checkpoint
from tecton_materialization.materialization_utils import MaterializationResourceContainer
from tecton_materialization.materialization_utils import batch_write_to_online_store
from tecton_materialization.materialization_utils import df_to_online_store_msg
from tecton_materialization.materialization_utils import has_prior_delta_commit
from tecton_materialization.materialization_utils import wait_for_metric_scrape
from tecton_proto.materialization.job_metadata__client_pb2 import OnlineStoreType
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_spark import materialization_plan
from tecton_spark.data_observability import create_feature_metrics_collector
from tecton_spark.materialization_plan import MATERIALIZED_RAW_DATA_END_TIME
from tecton_spark.materialization_plan import MaterializationPlan
from tecton_spark.offline_store import OfflineStoreWriterParams
from tecton_spark.offline_store import get_offline_store_reader
from tecton_spark.offline_store import get_offline_store_writer
from tecton_spark.time_utils import convert_timestamp_to_epoch


logger = logging.getLogger(__name__)

# Partitions being written to S3 should be small to minimize number of parquet files.
COALESCE_FOR_SMALL_PARTITIONS = 1
DEFAULT_COALESCE_FOR_S3 = 10
# Partitions being written to OSW can be higher to better utilize available executors.
DEFAULT_COALESCE_FOR_OSW = 64

idempotence_key = "featureStartTime"


def _construct_anchor_times(
    fdw: FeatureDefinitionWrapper, start_time: datetime.datetime, num_tiles: int, version: int
) -> List[int]:
    """Creates `num_tiles` consecutive anchor_times starting from `start_time`.

    :return: An increasing list of consecutive anchor times.
    """
    anchor_times = []
    for i in range(num_tiles):
        anchor_time = start_time + i * fdw.get_tile_interval
        anchor_time_val = convert_timestamp_to_epoch(anchor_time, version)
        anchor_times.append(anchor_time_val)

    return anchor_times


def _construct_tile_end_times(
    fdw: FeatureDefinitionWrapper, latest_tile_end_time: datetime.datetime, num_tiles: int, version: int
) -> List[int]:
    """Creates `num_tiles` consecutive tile_end_times where latest one ends at `latest_tile_end_time`.

    :return: An increasing list of consecutive tile end times.
    """
    tile_end_times = []
    for i in range(num_tiles):
        tile_end_time = latest_tile_end_time - i * fdw.batch_materialization_schedule
        time_val = convert_timestamp_to_epoch(tile_end_time, version)
        tile_end_times.append(time_val)

    tile_end_times.reverse()
    return tile_end_times


def _dedupe_online_store_writes(
    fd: FeatureDefinitionWrapper,
    df: DataFrame,
) -> DataFrame:
    # this mimics the conditional writes in the OnlineStoreWriter
    if fd.is_temporal:
        # we take the latest record for each entity for temporal FVs
        window = Window.partitionBy(fd.join_keys).orderBy(col(fd.time_key).desc())
        row_number_col = "__tecton_row_num"
        assert row_number_col not in df.columns
        df = df.withColumn(row_number_col, row_number().over(window))
        df = df.filter(col(row_number_col) == 1).drop(row_number_col)
        return df
    else:
        return df


def _make_dynamodb_json_dataframe(
    spark: SparkSession,
    fd: FeatureDefinitionWrapper,
    materialization_task_params: MaterializationTaskParams,
    df: DataFrame,
) -> DataFrame:
    df = df_to_online_store_msg(
        df,
        fd.id,
        is_batch=True,
        is_status=False,
        canary_id=None,
        is_compaction_job=fd.compaction_enabled,
    )
    udf_name = f"to_dynamodb_json_{fd.id}"
    if fd.compaction_enabled:
        # UDF used for compaction jobs. Compatible with TableFormatVersionV3
        spark._jvm.com.tecton.onlinestorewriter.RegisterFeatureToDynamoDbJsonUDFV2().register(
            udf_name, materialization_task_params.SerializeToString()
        )
        udf_column_name = "dynamodb_json"
        df = df.select(expr(f"{udf_name}(value) as {udf_column_name}"))
        return df.select(explode(udf_column_name))
    else:
        # UDF used by bulk backfill jobs for non-compaction fvs.
        spark._jvm.com.tecton.onlinestorewriter.RegisterFeatureToDynamoDbJsonUDF().register(
            udf_name, materialization_task_params.SerializeToString()
        )
        return df.select(expr(f"{udf_name}(value)"))


def _write_dynamodb_json(
    spark: SparkSession,
    fd: FeatureDefinitionWrapper,
    materialization_task_params: MaterializationTaskParams,
    df: DataFrame,
) -> int:
    dynamodb_json_df = _make_dynamodb_json_dataframe(spark, fd, materialization_task_params, df)
    output_path = materialization_task_params.batch_task_info.dynamodb_json_output_path
    # we repartition the rows to avoid hot partitions (as recommended by AWS for dynamodb:importtable) and generate
    # enough output files to get good parallelism on the dynamo side
    # 128 is a magic number that should work well for large files but not too much overhead for small files; but it
    # is merely theoretical, feel free to change
    dynamodb_json_df.repartition(128).write.format("text").option("compression", "gzip").mode("overwrite").save(
        output_path
    )
    return dynamodb_json_df.count()


def _make_batch_status_dataframe(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinitionWrapper,
    feature_start_time: datetime.datetime,
    feature_end_time: datetime.datetime,
) -> DataFrame:
    # For continuous aggregation when writing uncompacted data we will default to writing
    # tile end times
    version = fd.get_feature_store_format_version
    batch_params = materialization_task_params.batch_task_info.batch_parameters
    if fd.is_temporal_aggregate and not fd.is_continuous:
        # For BWAFVs, write all materialized anchor times in the status table
        anchor_times = _construct_anchor_times(fd, feature_start_time, batch_params.tile_count, version)
        anchor_times_df_format = [[x] for x in anchor_times]
        schema = StructType([StructField(anchor_time(), LongType())])
        return spark.createDataFrame(anchor_times_df_format, schema=schema)
    else:
        # For BFVs, write materialized tile end times in the status table
        tile_end_times = _construct_tile_end_times(fd, feature_end_time, batch_params.tile_count, version)
        tile_end_times_df_format = [[x] for x in tile_end_times]
        schema = StructType([StructField(MATERIALIZED_RAW_DATA_END_TIME, LongType())])
        return spark.createDataFrame(tile_end_times_df_format, schema=schema)


def _write_batch_to_hdfs(plan: MaterializationPlan, hdfs_output_path: str):
    plan.base_data_frame.write.parquet(hdfs_output_path)


def _materialize_batch_to_offline(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    feature_start_time: datetime.datetime,
    feature_end_time: datetime.datetime,
    plan: MaterializationPlan,
    job_metadata_client: JobMetadataClient,
):
    fd = feature_definition_from_task_params(materialization_task_params)
    version = fd.get_feature_store_format_version
    coalesce = (
        COALESCE_FOR_SMALL_PARTITIONS
        if get_offline_store_partition_params(fd).partition_interval.as_timedelta() <= datetime.timedelta(hours=1)
        else DEFAULT_COALESCE_FOR_S3
    )
    batch_task_info = materialization_task_params.batch_task_info
    should_avoid_coalesce = batch_task_info.should_avoid_coalesce
    offline_store_df = (
        plan.offline_store_data_frame if should_avoid_coalesce else plan.offline_store_data_frame.coalesce(coalesce)
    )

    offline_store_params = OfflineStoreWriterParams(
        s3_path=materialization_task_params.offline_store_path,
        always_store_anchor_column=True,
        time_column=get_time_column_for_offline_writer(fd),
        join_key_columns=fd.join_keys,
        is_continuous=fd.is_continuous,
        upsert_by_batch_publish_timestamp=fd.batch_publish_timestamp is not None,
    )

    logger.info(f"Writing to offline store for FV {fd.id} for interval {feature_start_time} to {feature_end_time}")
    start = time.time()

    store_writer = get_offline_store_writer(offline_store_params, fd, version, spark)

    # Replace previous the time range if doing a retry of a past job or if prev attempt already wrote data
    start_time_proto = Timestamp()
    start_time_proto.FromDatetime(feature_start_time)
    offline_store_type = get_offline_store_type(fd)
    is_overwrite_task = materialization_task_params.batch_task_info.batch_parameters.is_overwrite
    write_tile = pendulum.period(feature_start_time, feature_end_time)
    if offline_store_type == OfflineStoreType.DELTA and (
        has_prior_delta_commit(spark, materialization_task_params, idempotence_key, start_time_proto.ToJsonString())
        or is_overwrite_task
    ):
        store_writer.overwrite_dataframe_in_tile(offline_store_df, write_tile)
    elif offline_store_type == OfflineStoreType.ICEBERG and is_overwrite_task:
        store_writer.overwrite_dataframe_in_tile(offline_store_df, write_tile)
    else:
        store_writer.append_dataframe(offline_store_df)

    store_reader = get_offline_store_reader(spark, fd, path=materialization_task_params.offline_store_path)
    unhandled_analysis_exception = False
    try:
        start_time_col = convert_timestamp_for_version(feature_start_time, version)
        end_time_col = convert_timestamp_for_version(feature_end_time, version)
        # We need to subtract 1 microsecond from the end time to ensure that we don't
        # read the next tile
        offline_store_count = (
            store_reader.read(
                pendulum.period(feature_start_time, feature_end_time - datetime.timedelta(microseconds=1))
            )
            .filter((col(anchor_time()) >= lit(start_time_col)) & (col(anchor_time()) < lit(end_time_col)))
            .count()
        )
    except AnalysisException as e:
        is_df_empty = len(offline_store_df.take(1)) == 0
        if not is_df_empty:
            unhandled_analysis_exception = True
            logger.info(f"Unhandled AnalysisException checking Dataframe size: {e}")
        offline_store_count = 0
    export_consumption_debug_metrics(spark, offline_store_count, plan.cached_count(), unhandled_analysis_exception)

    latency = time.time() - start
    logger.info(f"Finished writing to offline store ({latency}s)")

    export_consumption_metrics(
        spark,
        fd,
        plan.cached_count(),
        materialization_task_params,
        store_type="offline",
        job_metadata_client=job_metadata_client,
    )


def _materialize_batch_to_online(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    feature_start_time: datetime.datetime,
    feature_end_time: datetime.datetime,
    plan: MaterializationPlan,
    resources,
    job_metadata_client: JobMetadataClient,
):
    batch_task_info = materialization_task_params.batch_task_info
    batch_params = batch_task_info.batch_parameters
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = feature_definition_from_task_params(materialization_task_params)
    online_store_df = plan.online_store_data_frame
    start = time.time()

    write_type_detail = "bulk load intermediate storage" if batch_params.create_online_table else "online store"
    logger.info(
        f"Writing to {write_type_detail} for FV {fd.id} for interval {feature_start_time} to {feature_end_time}"
    )
    if batch_task_info.should_dedupe_online_store_writes:
        online_store_df = _dedupe_online_store_writes(fd, online_store_df)

    if batch_params.create_online_table:
        # note that it's okay to write the status table entries here ahead of time, because it won't be
        # marked as servable until the import table is complete
        # additionally, the status table range never shrinks, so even if we retry, it will be okay
        dynamo_import_row_count = _write_dynamodb_json(
            spark,
            fd,
            materialization_task_params,
            online_store_df,
        )
        # we export consumption metrics here for dynamo import instead of OSW because we don't use OSW
        export_consumption_metrics(
            spark,
            fd,
            dynamo_import_row_count,
            materialization_task_params,
            store_type="online",
            online_store_type=OnlineStoreType.ONLINE_STORE_TYPE_DYNAMO,
            job_metadata_client=job_metadata_client,
        )
        logger.info(f"Wrote {dynamo_import_row_count} rows to bulk load intermediate storage")
    else:
        assert not fv_spec.compaction_enabled, "Batch compaction must use create_online_table"
        # Write materialized features to the online feature store
        online_store_df = online_store_df.coalesce(DEFAULT_COALESCE_FOR_OSW)
        batch_write_to_online_store(
            online_store_df, materialization_task_params, resources.get_online_store_sink(), fd.id, is_status=False
        )
        export_consumption_metrics(
            spark,
            fd,
            plan.cached_count(),
            materialization_task_params,
            store_type="online",
            job_metadata_client=job_metadata_client,
            online_store_type=OnlineStoreType.ONLINE_STORE_TYPE_DYNAMO,
            only_new_consumption=True,
        )
    status_df = _make_batch_status_dataframe(
        spark, materialization_task_params, fd, feature_start_time, feature_end_time
    )

    batch_write_to_online_store(
        status_df, materialization_task_params, resources.get_online_store_sink(), fd.id, is_status=True
    )
    latency = time.time() - start
    logger.info(f"Finished writing to {write_type_detail} ({latency}s)")


def _get_hdfs_path(materialization_task_params: MaterializationTaskParams, end_time):
    hdfs_path_base = f"transformed_data_{IdHelper.to_string(materialization_task_params.attempt_id)}"
    formatted_time = end_time.strftime("%Y_%m_%d_%H_%M_%S")
    return f"{hdfs_path_base}_{formatted_time}"


def batch_materialize_from_params(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    run_id,
    job_metadata_client: JobMetadataClient,
    step=None,
):
    batch_params = materialization_task_params.batch_task_info.batch_parameters
    resources = MaterializationResourceContainer(spark, materialization_task_params)
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"{idempotence_key}":"{batch_params.feature_start_time.ToJsonString()}"}}',
    )
    fd = feature_definition_from_task_params(materialization_task_params)
    task_feature_start_time = batch_params.feature_start_time.ToDatetime()
    task_feature_end_time = batch_params.feature_end_time.ToDatetime()

    is_plan_integration_test = materialization_task_params.HasField("plan_id")
    write_to_intermediate_store_only = step == 1 or is_plan_integration_test
    # we only use checkpoints in steps that write to actual stores and have multiple intervals to write
    use_checkpoints = (
        not write_to_intermediate_store_only
        and not materialization_task_params.HasField("canary_id")
        and fd.is_incremental_backfill
    )

    write_to_offline_store_from_source = batch_params.write_to_offline_feature_store
    # if we are reading from the offline store, we don't need to split up the query, like we do from source
    # we actually don't want to, because dynamo json will not support this
    write_to_online_from_source = (
        batch_params.write_to_online_feature_store and not batch_params.read_from_offline_store_for_online_write
    )
    write_to_online_from_offline_store = (
        batch_params.write_to_online_feature_store and batch_params.read_from_offline_store_for_online_write
    )

    reads_data_from_source = write_to_offline_store_from_source or write_to_online_from_source
    if step == 1 and not reads_data_from_source:
        # we only need step 1 if we are reading data from source (which executes transformations)
        logger.info("Skipping step 1 since no data is read from source")
        return

    should_run_transformation = (
        write_to_offline_store_from_source or write_to_online_from_source or is_plan_integration_test
    )

    if should_run_transformation:
        total_rows = 0
        # when reading from source, we must split the queries up into intervals based on incremental_backfills
        # note that we don't need to do this for 2 step materialization, but we keep it here to preserve old behavior
        # and not break existing customer jobs
        for query_feature_start_time, query_feature_end_time in job_query_intervals(materialization_task_params):
            if use_checkpoints and is_checkpoint_complete(spark, materialization_task_params, query_feature_start_time):
                logger.info(
                    "Checkpoint complete for interval %s to %s; skipping",
                    query_feature_start_time,
                    query_feature_end_time,
                )
                continue
            query_feature_time_limits = pendulum.instance(query_feature_end_time) - pendulum.instance(
                query_feature_start_time
            )
            if step in (1, None):
                metrics_collector = create_feature_metrics_collector(
                    spark,
                    materialization_task_params,
                    feature_start_time=query_feature_start_time,
                    feature_end_time=query_feature_end_time,
                )
                plan = materialization_plan.get_batch_materialization_plan(
                    spark=spark,
                    feature_definition=fd,
                    feature_data_time_limits=query_feature_time_limits,
                    metrics_collector=metrics_collector,
                )
                # we must cache here so metrics_collector does not double-count rows. However, this is not
                # as the cache is subject to eviction
                # TODO(dataobs): fix this
                plan.base_data_frame.cache()
            else:
                assert step == 2
                if is_plan_integration_test:
                    # Skip for plan integration tests since data is not actually materialized to offline store
                    return
                # we don't collect metrics in step 2, since they are already collected in step 1
                metrics_collector = None
                # for step 2, we read from the transformed data written in step 1
                plan = MaterializationPlan.from_parquet(
                    spark=spark, fd=fd, path=_get_hdfs_path(materialization_task_params, query_feature_end_time)
                )
            if write_to_intermediate_store_only:
                # for step 1, we write the transformed data to hdfs, to be read in step 2
                # for plan integration tests, we skip actual persistent writes but only write to hdfs for data validation purposes
                _write_batch_to_hdfs(plan, _get_hdfs_path(materialization_task_params, query_feature_end_time))
                logger.info(
                    f"Generated {plan.cached_count()} rows for interval {query_feature_start_time} to {query_feature_end_time}"
                )
            else:
                if write_to_offline_store_from_source:
                    _materialize_batch_to_offline(
                        spark,
                        materialization_task_params,
                        query_feature_start_time,
                        query_feature_end_time,
                        plan,
                        job_metadata_client=job_metadata_client,
                    )
                if write_to_online_from_source:
                    _materialize_batch_to_online(
                        spark,
                        materialization_task_params,
                        query_feature_start_time,
                        query_feature_end_time,
                        plan,
                        resources,
                        job_metadata_client=job_metadata_client,
                    )
            if metrics_collector:
                try:
                    metrics_collector.publish()
                except Exception as e:
                    logger.error(f"Metrics publishing failed: {e}")
            if not write_to_intermediate_store_only:
                logger.info(
                    f"Wrote {plan.cached_count()} rows for interval {query_feature_start_time} to {query_feature_end_time}"
                )
                total_rows += plan.cached_count()
            if use_checkpoints:
                write_checkpoint(spark, materialization_task_params, query_feature_start_time, run_id)

        logger.info(f"Wrote {total_rows} total rows")
        # Print this line too since occasionally the logger library doesn't work (BAT-15553)
        print(f"Wrote {total_rows} total rows")

    if write_to_online_from_offline_store and not write_to_intermediate_store_only:
        assert not materialization_task_params.HasField("canary_id")
        # we don't do metrics collection here, because they already got collected in the jobs writing to the offline store
        if fd.compaction_enabled:
            plan = materialization_plan.get_batch_compaction_online_materialization_plan(
                spark=spark, feature_definition=fd, compaction_job_end_time=task_feature_end_time
            )
        else:
            # used for bootstrap bulk backfill jobs
            plan = MaterializationPlan.from_offline_store(fd, task_feature_start_time, task_feature_end_time, spark)
        if plan is not None:
            _materialize_batch_to_online(
                spark,
                materialization_task_params,
                task_feature_start_time,
                task_feature_end_time,
                plan,
                resources,
                job_metadata_client=job_metadata_client,
            )
        else:
            logger.info("Offline store empty; skipping write to online store")

    wait_for_metric_scrape()
    resources.close()
