import logging
import signal
import time
from typing import Optional

from pyspark.sql import SparkSession
from pyspark.sql.functions import concat
from pyspark.sql.functions import from_json
from pyspark.sql.functions import lit
from pyspark.sql.functions import struct
from pyspark.sql.functions import to_json
from pyspark.sql.types import StringType
from pyspark.sql.types import StructType

from tecton_core.query_consts import anchor_time
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_spark.materialization_plan import MATERIALIZED_RAW_DATA_END_TIME


logger = logging.getLogger(__name__)

WRITTEN_BY_BATCH = "written_by_batch"
BATCH_STATUS_ENTRY = "update_status_only"
COLUMNS = "columns"
CANARY_ID_COLUMN = "canary_id"


def batch_write_to_online_store(
    dataframe,
    materialization_task_params: MaterializationTaskParams,
    sink,
    fv_id: str,
    is_status: bool,
):
    start = time.time()
    canary_id = materialization_task_params.canary_id if materialization_task_params.HasField("canary_id") else None
    write_df = df_to_online_store_msg(dataframe, fv_id, is_batch=True, is_status=is_status, canary_id=canary_id)

    logger.info(f"Starting batch write to Tecton Online Store for the FV '{fv_id}'")
    write_df._jdf.foreachPartition(sink)

    latency = time.time() - start
    logger.info(f"Finished batch write for the FV '{fv_id}' ({latency}s)")


def df_to_online_store_msg(
    dataframe,
    feature_view_id_str: str,
    is_batch: bool,
    is_status: bool,
    is_compaction_job: bool = False,
    canary_id: Optional[str] = None,
):
    """Produces a dataframe to be written to the online store.

    The dataframe will have two columns: 'key' and 'value'. The 'key' column will look like:

    feature_view_id_str # for SFVs and SWAFVs
    or
    feature_view_id_str + "|" + _anchor_time # for BWAFVs
    or
    feature_view_id_str + "|" + _materialized_raw_data_end_time # for batch BFVs

    In order to construct these keys, the input dataframe must have a column named `_anchor_time` for BWAFVs or a column
    named `_materialized_raw_data_end_time` for BFVs. It does not need to have either for SFVs or SWAFVs.

    For BWAFVs, the 'value' column will look like:
        value = {WRITTEN_BY_BATCH: true, "_anchor_time": 196000, COLUMNS: {"num_users": 1, ...}} # `is_status` is False
        or
        value = {BATCH_STATUS_ENTRY: true, WRITTEN_BY_BATCH: true, "_anchor_time": 196000} # `is_status` is True
    For BFVs, the 'value' column will look like:
        value = {WRITTEN_BY_BATCH: true, "_materialized_raw_data_end_time": 196000, COLUMNS: {"num_users": 1, ...}} # `is_status` is False
        or
        value = {BATCH_STATUS_ENTRY: true, WRITTEN_BY_BATCH: true, "_materialized_raw_data_end_time": 196000} # `is_status` is True
    For SFVs and SWAFVs, the 'value' column will look like:
        value = {COLUMNS: {"num_users": 1, ...}} # `is_status` must be False when `is_batch` is False
    """
    # only batch sends data and status separately
    assert not is_status or is_batch or is_compaction_job

    # add additional columns if needed; wrap original columns except anchor time in COLUMNS struct
    payload_schema = dataframe.schema.fieldNames()
    key = lit(feature_view_id_str)
    if is_compaction_job:
        return dataframe.select(key.alias("key"), to_json(struct(payload_schema)).alias("value"))

    # Only used when `is_batch` is True.
    is_temporal_aggregate = False

    if anchor_time() in payload_schema:
        is_temporal_aggregate = True
        payload_schema.remove(anchor_time())
    elif is_batch:
        payload_schema.remove(MATERIALIZED_RAW_DATA_END_TIME)

    if is_status:
        dataframe = dataframe.withColumn(BATCH_STATUS_ENTRY, lit(True))
    else:
        dataframe = dataframe.withColumn(COLUMNS, struct(payload_schema))
    if is_batch:
        dataframe = dataframe.withColumn(WRITTEN_BY_BATCH, lit(True))
    if canary_id:
        dataframe = dataframe.withColumn(CANARY_ID_COLUMN, lit(canary_id))

    # Remove original columns (except anchor_time or materialized_raw_data_end_time) from
    # a top-level dataframe
    for col_name in payload_schema:
        dataframe = dataframe.drop(col_name)

    # wrap all columns in json object as `value`
    row_schema = dataframe.schema.fieldNames()
    if is_batch:
        if is_temporal_aggregate:
            key = concat(key, lit("|"), anchor_time())
        else:
            key = concat(key, lit("|"), MATERIALIZED_RAW_DATA_END_TIME)

    dataframe = dataframe.select(key.alias("key"), to_json(struct(row_schema)).alias("value"))
    if is_batch and is_status and not is_temporal_aggregate:
        logger.info(f"Writing status table update for BFV: {feature_view_id_str}")

    return dataframe


def set_up_online_store_sink(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    sink = spark._jvm.com.tecton.onlinestorewriter.SparkOnlineStoreSinkFactory.fromMaterializationTaskParams(
        materialization_task_params.SerializeToString()
    )
    signal.signal(signal.SIGINT, lambda signum, frame: sink.closeGlobalResources())
    signal.signal(signal.SIGTERM, lambda signum, frame: sink.closeGlobalResources())
    return sink


class MaterializationResourceContainer:
    def __init__(self, spark: SparkSession, materialization_task_params: MaterializationTaskParams):
        self.spark = spark
        self.materialization_task_params = materialization_task_params
        self.online_store_sink = None
        self.materialization_plan = {}

    def get_online_store_sink(self):
        if self.online_store_sink is None:
            self.online_store_sink = set_up_online_store_sink(self.spark, self.materialization_task_params)
        return self.online_store_sink

    def close(self):
        if self.online_store_sink is not None:
            self.online_store_sink.closeGlobalResources()


def _set_statsd_client_prefix(statsd_client, spark):
    # Calling the statsd client directly will always emit metrics from the driver.
    app_name = spark.conf.get("spark.app.name")
    statsd_client._prefix = f"spark.{app_name}.driver"


def get_statsd_client(spark: SparkSession):
    # TEMPORARY: statsd is a new library and requires restarting the internal
    # cluster, so we import it here and gate it behind a flag. This will allow
    # us to gradually roll it out to customers, so we don't have to restart all
    # clusters upon a single release.
    import statsd

    statsd_client = statsd.StatsClient("0.0.0.0", 3031)
    _set_statsd_client_prefix(statsd_client, spark)
    return statsd_client


def wait_for_metric_scrape():
    # Sleep for 1 minute before closing to ensure metrics are collected by Chronosphere (30 second
    # scrape interval).
    sleep_time = 60  # 1 minute
    logger.info(f"Waiting {sleep_time}s for metrics to be scraped.")
    time.sleep(sleep_time)


def has_prior_delta_commit(spark, materialization_params, idempotence_key, idempotence_value):
    assert materialization_params.HasField("offline_store_path"), "definition must have offline_store_path set"

    from delta.tables import DeltaTable
    from pyspark.sql.utils import AnalysisException

    try:
        delta_table = DeltaTable.forPath(spark, materialization_params.offline_store_path)
    except AnalysisException:
        # no prior commits if table doesn't exist yet
        return False

    metadata_schema = StructType().add(f"{idempotence_key}", StringType())
    commit_count = (
        delta_table.history()
        .select(from_json("userMetadata", metadata_schema).alias("metadataJson"))
        .filter(f"metadataJson.{idempotence_key} = '{idempotence_value}'")
        .count()
    )
    return commit_count != 0
