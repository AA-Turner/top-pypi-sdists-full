import datetime
import logging
import os
from typing import Optional

from pyspark.sql import SparkSession

from tecton_core import feature_view_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.time_utils import align_time_downwards
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.materialization_utils import get_statsd_client
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadata
from tecton_proto.materialization.job_metadata__client_pb2 import OfflineStoreType
from tecton_proto.materialization.job_metadata__client_pb2 import OnlineStoreType
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


logger = logging.getLogger(__name__)


def get_materialized_feature_columns(fd: FeatureDefinitionWrapper):
    return feature_view_utils.get_input_feature_columns(
        fd.view_schema.to_proto(),
        fd.join_keys,
        fd.timestamp_key,
    )


def export_consumption_metrics(
    spark: SparkSession,
    fd: FeatureDefinitionWrapper,
    row_count,
    params: MaterializationTaskParams,
    store_type,
    job_metadata_client: JobMetadataClient,
    online_store_type: OnlineStoreType = None,
    only_new_consumption: bool = False,
):
    assert store_type in ("offline", "online")
    # we only use this for dynamo now. no easy way to get the online_store_type
    assert store_type != "online" or online_store_type == OnlineStoreType.ONLINE_STORE_TYPE_DYNAMO
    # Don't want to call fd.features, since in the
    # temporal aggregate case it will return a feature for each time window,
    # which is not how the data is actually materialized.
    materialized_feature_columns = get_materialized_feature_columns(fd)

    num_rows = row_count
    num_values = num_rows * len(materialized_feature_columns)

    if not only_new_consumption:
        statsd_client = get_statsd_client(spark)

        statsd_safe_fd_name = fd.name.replace(":", "__")
        statsd_safe_workspace = fd.workspace.replace(":", "__")
        statsd_client.incr(
            f"tecton-{store_type}-store.cm_feature_write_rows.{statsd_safe_workspace}.{statsd_safe_fd_name}.", num_rows
        )
        statsd_client.incr(
            f"tecton-{store_type}-store.cm_feature_write_values.{statsd_safe_workspace}.{statsd_safe_fd_name}",
            num_values,
        )

    def updater(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        aligned_bucket_start = int(
            align_time_downwards(datetime.datetime.now(), datetime.timedelta(hours=1)).timestamp()
        )
        if store_type == "offline":
            offline = new_proto.materialization_consumption_info.offline_store_consumption
            bucket = offline.consumption_info[aligned_bucket_start]

            if params.offline_store_path.startswith("s3"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_S3
            elif params.offline_store_path.startswith("dbfs"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_DBFS
            elif params.offline_store_path.startswith("gs"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_GCS
            elif os.environ.get("TEST_ONLY_TECTON_DYNAMODB_ENDPOINT_OVERRIDE"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_S3
            else:
                msg = f"Unknown offline store type path: {offline.offline_store_type}"
                raise Exception(msg)
        elif store_type == "online":
            online = new_proto.materialization_consumption_info.online_store_consumption
            bucket = online.consumption_info[aligned_bucket_start]

            online.online_store_type = online_store_type
        else:
            exc_msg = f"Unknown store type: {store_type}"
            raise Exception(exc_msg)

        bucket.rows_written += num_rows
        bucket.features_written += num_values

        return new_proto

    if params.HasField("job_metadata_table") and params.use_new_consumption_metrics:
        job_metadata_client.update(updater)

    logger.info(f"Exported {store_type} consumption metrics")


def export_consumption_debug_metrics(
    spark: SparkSession,
    offline_store_count: int,
    dataframe_count: int,
    unhandled_analysis_exception: bool,
):
    statsd_client = get_statsd_client(spark)

    if unhandled_analysis_exception:
        statsd_client.incr("consumption.unhandled_analysis_exception")
    elif offline_store_count != dataframe_count:
        statsd_client.incr("consumption.diff_rows_count", offline_store_count - dataframe_count)
    else:
        statsd_client.incr("consumption.same_rows")
