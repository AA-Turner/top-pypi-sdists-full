import logging

import py4j.protocol
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.types import LongType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType

from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.materialization_utils import batch_write_to_online_store
from tecton_materialization.materialization_utils import has_prior_delta_commit
from tecton_materialization.materialization_utils import set_up_online_store_sink
from tecton_materialization.materialization_utils import wait_for_metric_scrape
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_spark import feature_view_spark_utils
from tecton_spark.data_observability import create_feature_metrics_collector
from tecton_spark.materialization_plan import MATERIALIZED_RAW_DATA_END_TIME
from tecton_spark.offline_store import OfflineStoreWriterParams
from tecton_spark.offline_store import get_offline_store_writer
from tecton_spark.time_utils import convert_timestamp_to_epoch


logger = logging.getLogger(__name__)

idempotence_key = "ingestPath"


def ingest_pushed_df(spark: SparkSession, raw_df: DataFrame, materialization_task_params: MaterializationTaskParams):
    ingest_task_info = materialization_task_params.ingest_task_info
    ingest_path = ingest_task_info.ingest_parameters.ingest_path
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"{idempotence_key}":"{ingest_path}"}}',
    )
    fd = feature_definition_from_task_params(materialization_task_params)

    feature_view_spark_utils.validate_df_columns_and_feature_types(raw_df, fd.view_schema)

    # Drop extra columns
    df = raw_df.select(*fd.view_schema.column_names())

    timestamp_key = fd.timestamp_key
    assert timestamp_key is not None
    version = fd.get_feature_store_format_version

    if ingest_task_info.ingest_parameters.write_to_online_feature_store:
        logger.info(f"Ingesting to the OnlineStore FT: {fd.id}")
        # Find the last timestamp
        raw_data_end_time_ts = df.agg({timestamp_key: "max"}).collect()[0][0]
        raw_data_end_time_epoch = convert_timestamp_to_epoch(raw_data_end_time_ts, version)

        online_df = df.withColumn(MATERIALIZED_RAW_DATA_END_TIME, lit(raw_data_end_time_epoch))

        sink = set_up_online_store_sink(spark, materialization_task_params)
        metrics_collector = create_feature_metrics_collector(spark, materialization_task_params)

        # collect metrics
        online_df = metrics_collector.observe(online_df)

        # TODO: For large DFs consider splitting into "chunks" to load balance across partitions and FSW instances
        batch_write_to_online_store(online_df, materialization_task_params, sink, fd.id, is_status=False)

        # Status table
        status_df = [[raw_data_end_time_epoch]]
        schema = StructType([StructField(MATERIALIZED_RAW_DATA_END_TIME, LongType())])
        status_df = spark.createDataFrame(status_df, schema=schema)
        batch_write_to_online_store(status_df, materialization_task_params, sink, fd.id, is_status=True)
        if sink is not None:
            # Temporarily wrap closeGlobalResources() for ingest since this
            # runs in the internal cluster. This is because we may run this
            # code before the new OSW jar is installed on the internal cluster.
            # This isn't a problem for other types of materialization since
            # they use short-lived clusters that use materialization library
            # and OSW from the same release.
            #
            # TODO(brian): remove try/except after all validation clusters are
            # restarted.
            try:
                sink.closeGlobalResources()
            except py4j.protocol.Py4JError:
                pass

        # publish metrics
        try:
            metrics_collector.publish()
        except Exception as e:
            logger.error(f"Metrics publishing failed: {e}")

    # skip delta write if we detect a prior job has successfully committed the data already
    if ingest_task_info.ingest_parameters.write_to_offline_feature_store and not has_prior_delta_commit(
        spark, materialization_task_params, idempotence_key, ingest_path
    ):
        logger.info(f"Ingesting to the OfflineStore FT: {fd.id}")
        offline_store_params = OfflineStoreWriterParams(
            s3_path=materialization_task_params.offline_store_path,
            always_store_anchor_column=False,
            time_column=timestamp_key,
            join_key_columns=fd.join_keys,
            is_continuous=False,
        )
        offline_store_config = fd.offline_store_config
        assert offline_store_config.HasField("delta"), "FeatureTables do not support Parquet-based Offline storage"
        store_writer = get_offline_store_writer(offline_store_params, fd, version, spark)
        store_writer.upsert_dataframe(df)

    wait_for_metric_scrape()
