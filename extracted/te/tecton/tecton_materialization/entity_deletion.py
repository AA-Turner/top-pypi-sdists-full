import logging
import time
from typing import Optional

from pyspark.sql import SparkSession

from tecton_core.query_consts import anchor_time
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.materialization_utils import get_statsd_client
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_spark.offline_store import OfflineStoreWriterParams
from tecton_spark.offline_store import get_offline_store_writer


logger = logging.getLogger(__name__)


def _export_deletion_metrics(
    spark: SparkSession,
    store_type: str,
    metric_source: str,
    requested_num_keys: int,
    deleted_num_keys: int,
    latency: Optional[float] = None,
):
    statsd_client = get_statsd_client(spark)

    statsd_client.incr(f"{metric_source}.{store_type}.num_keys_deletion_requested", requested_num_keys)
    statsd_client.incr(f"{metric_source}.{store_type}.num_keys_deletion_success", deleted_num_keys)

    if latency:
        # timing expects number of milliseconds
        statsd_client.timing(f"{metric_source}.{store_type}.deletion_latency", latency * 1000)


def run_online_store_deleter(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    start = time.time()
    report = spark._jvm.com.tecton.onlinestorewriter.deleter.OnlineStoreDeleter.fromMaterializationTaskParams(
        materialization_task_params.SerializeToString()
    ).run()
    latency = time.time() - start

    if materialization_task_params.HasField("online_store_writer_config"):
        store_type = materialization_task_params.online_store_writer_config.online_store_params.WhichOneof("store_type")
    else:
        store_type = "dynamo"

    _export_deletion_metrics(
        spark,
        store_type,
        metric_source="tecton-online-store-deleter",
        requested_num_keys=report.getRequestedNumKeys(),
        deleted_num_keys=report.getDeletedNumKeys(),
        latency=latency,
    )

    if report.getError():
        msg = f"Deletion was interrupted due to the error received from storage: {report.getError()}"
        raise RuntimeError(msg)


def run_offline_store_deleter(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    deletion_params = materialization_task_params.deletion_task_info.deletion_parameters
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"deletionPath":"{deletion_params.offline_join_keys_path}"}}',
    )
    fd = feature_definition_from_task_params(materialization_task_params)
    if fd.is_temporal_aggregate:
        time_column = anchor_time()
    else:
        time_column = fd.time_key
    offline_store_params = OfflineStoreWriterParams(
        s3_path=materialization_task_params.offline_store_path,
        always_store_anchor_column=False,
        time_column=time_column,
        join_key_columns=fd.join_keys,
        is_continuous=False,
    )
    store_writer = get_offline_store_writer(offline_store_params, fd, fd.get_feature_store_format_version, spark)
    keys = spark.read.parquet(deletion_params.offline_join_keys_path)
    keys = keys.distinct()
    requested_num_keys = keys.count()
    start = time.time()
    deleted_num_keys = store_writer.delete_keys(keys)
    latency = time.time() - start

    store_type = fd.offline_store_config.WhichOneof("store_type") if fd.offline_store_config else None
    store_type = store_type or "delta"

    _export_deletion_metrics(
        spark,
        store_type=store_type,
        metric_source="tecton-offline-store-deleter",
        requested_num_keys=requested_num_keys,
        deleted_num_keys=deleted_num_keys,
        latency=latency,
    )
