import logging

from pyspark.sql import SparkSession

from tecton_core.offline_store import get_time_column_for_offline_writer
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_spark.offline_store import OfflineStoreWriterParams
from tecton_spark.offline_store import get_offline_store_writer


logger = logging.getLogger(__name__)


def run_iceberg_maintenance(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    fd = feature_definition_from_task_params(materialization_task_params)
    offline_store_params = OfflineStoreWriterParams(
        s3_path=materialization_task_params.offline_store_path,
        always_store_anchor_column=True,
        time_column=get_time_column_for_offline_writer(fd),
        join_key_columns=fd.join_keys,
        is_continuous=fd.is_continuous,
        upsert_by_batch_publish_timestamp=fd.batch_publish_timestamp is not None,
    )
    store_writer = get_offline_store_writer(offline_store_params, fd, fd.get_feature_store_format_version, spark)
    iceberg_maintenance_params = (
        materialization_task_params.iceberg_maintenance_task_info.iceberg_maintenance_parameters
    )
    if iceberg_maintenance_params.execute_compaction:
        store_writer.compact_files()
