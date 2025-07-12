import logging
import time
from typing import Optional

import pyspark
from pyspark.sql import SparkSession

from tecton_core.id_helper import IdHelper
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.materialization_utils import df_to_online_store_msg
from tecton_materialization.materialization_utils import set_up_online_store_sink
from tecton_proto.materialization.job_metadata__client_pb2 import JobMetadata
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_spark import materialization_plan


logger = logging.getLogger(__name__)


def _get_query_name(is_plan_integration_test: bool = False):
    if is_plan_integration_test:
        return "tecton_osw_sink_plan_integration_test"
    return "tecton_osw_sink"


def _start_stream_job_with_online_store_sink(
    spark: SparkSession, dataframe, materialization_task_params, sink
) -> "pyspark.sql.streaming.StreamingQuery":
    canary_id = materialization_task_params.canary_id if materialization_task_params.HasField("canary_id") else None
    # TODO(amargvela): For SFV add feature timestamp as MATERIALIZED_RAW_DATA_END_TIME column.
    fd = feature_definition_from_task_params(materialization_task_params)

    stream_task_info = materialization_task_params.stream_task_info

    # Check if realtime mode is enabled
    use_realtime_trigger = (
        stream_task_info.HasField("streaming_trigger_realtime_mode")
        and stream_task_info.streaming_trigger_realtime_mode
    )

    if use_realtime_trigger:
        if stream_task_info.HasField("streaming_trigger_interval_override"):
            processing_time = stream_task_info.streaming_trigger_interval_override
        else:
            processing_time = "5 minutes"

        logger.info(f"Using RealTimeTrigger with interval {processing_time} for FV {fd.id}")
        trigger = spark._jvm.org.apache.spark.sql.execution.streaming.RealTimeTrigger.apply(processing_time)
    else:
        if stream_task_info.HasField("streaming_trigger_interval_override"):
            processing_time = stream_task_info.streaming_trigger_interval_override
        elif fd.is_continuous:
            processing_time = "0 seconds"
        else:
            processing_time = "30 seconds"

        logger.info(f"Using ProcessingTimeTrigger with interval {processing_time} for FV {fd.id}")
        trigger = spark._jvm.org.apache.spark.sql.streaming.Trigger.ProcessingTime(processing_time)

    write_df = df_to_online_store_msg(dataframe, fd.id, is_batch=False, is_status=False, canary_id=canary_id)

    logger.info(f"Starting stream write to Tecton Online Store for FV {fd.id}")
    writer = (
        write_df._jdf.writeStream()
        .queryName(_get_query_name(materialization_task_params.HasField("plan_id")))
        .option(
            "checkpointLocation", f"{stream_task_info.streaming_checkpoint_path}-k"
        )  # append -k to differentiate from Dynamo checkpoint path; keep this in sync with the Canary process.
        .outputMode("update")
        .trigger(trigger)
    )
    # we don't materialize to sinks to not override prod data
    if materialization_task_params.HasField("plan_id"):
        writer = writer.option("startingOffsets", "earliest").format("memory")
    else:
        writer = writer.foreach(sink)
    return writer.start()


def _start_stream_materialization(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    sink,
    job_metadata_client: JobMetadataClient,
) -> "pyspark.sql.streaming.StreamingQuery":
    logger.info(
        f"Starting materialization task {materialization_task_params.materialization_task_id} for feature view {IdHelper.to_string(materialization_task_params.feature_view.feature_view_id)}"
    )

    fd = feature_definition_from_task_params(materialization_task_params)

    plan = materialization_plan.get_stream_materialization_plan(
        spark=spark,
        feature_definition=fd,
    )
    spark_df = plan.online_store_data_frame

    if materialization_task_params.stream_task_info.stream_parameters.stream_handoff_config.enabled:
        _handle_stream_handoff(job_metadata_client)

    online_store_query = _start_stream_job_with_online_store_sink(spark, spark_df, materialization_task_params, sink)

    return online_store_query


def _watch_stream_query(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    stream_query: "pyspark.sql.streaming.StreamingQuery",
    job_metadata_client: JobMetadataClient,
):
    def set_terminated_state(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        new_proto.spark_execution_info.stream_handoff_synchronization_info.query_cancellation_complete = True
        return new_proto

    def check_memory_output():
        return (
            spark.sql("SELECT * FROM " + _get_query_name(materialization_task_params.HasField("plan_id"))).count() > 0
        )

    stream_params = materialization_task_params.stream_task_info.stream_parameters
    if materialization_task_params.HasField("plan_id"):
        start_time = time.time()
        plan_integration_test_job_timeout = 10 * 60  # 10 minutes in seconds

        while stream_query.isActive():
            if check_memory_output():
                logger.info("Stream query output generated. Stopping stream query.")
                stream_query.stop()
                stream_query.awaitTermination()
                return
            elapsed_time = time.time() - start_time
            if elapsed_time > plan_integration_test_job_timeout:
                logger.info(
                    f"Stream query ran over timeout of {plan_integration_test_job_timeout} seconds. Stopping stream query."
                )
                stream_query.stop()
                stream_query.awaitTermination()
                return
            time.sleep(60)
        # returns immediately or throws exception, given thzat isActive() is false
        stream_query.awaitTermination()
    elif stream_params.stream_handoff_config.enabled:
        while stream_query.isActive():
            job_metadata, _ = job_metadata_client.get()
            # check if the materialization task has been cancelled
            if job_metadata.spark_execution_info.stream_handoff_synchronization_info.query_cancellation_requested:
                logger.info("Stream query cancellation requested. Stopping stream query.")
                try:
                    stream_query.stop()
                    stream_query.awaitTermination()
                finally:
                    logger.info("Query cancellation complete")
                    job_metadata_client.update(set_terminated_state)
                return
            time.sleep(60)
        # returns immediately or throws exception, given that isActive() is false
        stream_query.awaitTermination()
    else:
        stream_query.awaitTermination()


def _handle_stream_handoff(job_metadata_client: JobMetadataClient):
    """
    If stream handoff is enabled, we need to wait for the previous job to finish before starting the next one.
    """

    def set_ready_state(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        new_proto.spark_execution_info.stream_handoff_synchronization_info.new_cluster_started = True
        return new_proto

    start_time = time.time()
    job_metadata_client.update(set_ready_state)
    logger.info("Using stream handoff; waiting for ready state...")
    job_metadata, _ = job_metadata_client.get()
    while not job_metadata.spark_execution_info.stream_handoff_synchronization_info.stream_query_start_allowed:
        if time.time() - start_time > 3600.0:
            msg = "Timed out waiting for ready state"
            raise Exception(msg)
        time.sleep(1)
        job_metadata, _ = job_metadata_client.get()
    logger.info("Ready state reached; starting streaming query")


def stream_materialize_from_params(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    job_metadata_client: JobMetadataClient,
):
    sink = set_up_online_store_sink(spark, materialization_task_params)
    online_store_sink = _start_stream_materialization(
        spark, materialization_task_params, sink, job_metadata_client=job_metadata_client
    )

    should_publish_stream_metrics = spark.conf.get("spark.tecton.publish_stream_metrics", "true") == "true"

    if should_publish_stream_metrics:
        metricsReportingListener = spark._jvm.com.tecton.onlinestorewriter.MetricsReportingListener(
            materialization_task_params.SerializeToString()
        )
        spark.streams._jsqm.addListener(metricsReportingListener)

    _watch_stream_query(spark, materialization_task_params, online_store_sink, job_metadata_client=job_metadata_client)
    if sink is not None:
        sink.closeGlobalResources()
