import contextlib
import logging
from typing import List
from typing import Tuple

import pyarrow
import ray

from tecton_core import offline_store
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.common.task_params import job_query_intervals
from tecton_materialization.ray.bulk_backfill import get_bootstrap_bulk_backfill_qt
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer_for_fd
from tecton_materialization.ray.materialization_utils import update_status_table
from tecton_materialization.ray.materialization_utils import write_to_online_store
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_proto.data.feature_view__client_pb2 import FeatureView
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.offlinestore.delta import metadata__client_pb2 as metadata_pb2


logger = logging.getLogger(__name__)

PYARROW_ASC = "ascending"
PYARROW_DESC = "descending"


def run_batch_materialization(
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    batch_params = materialization_task_params.batch_task_info.batch_parameters
    is_plan_integration_test_job = materialization_task_params.HasField("plan_id")
    # Bulk Backfill jobs (i.e. read_from_offline_store_for_online_write is true) don't need to break up the time
    # intervals since it reads from the offline store instead of the data source.
    if (
        batch_params.write_to_offline_feature_store
        or (batch_params.write_to_online_feature_store and not batch_params.read_from_offline_store_for_online_write)
        or is_plan_integration_test_job
    ):
        intervals = job_query_intervals(materialization_task_params)
        for idx, interval in enumerate(intervals):
            job_status_client.set_query_index(idx, len(intervals))
            if is_plan_integration_test_job:
                materialize_interval_for_plan_integration_test(
                    interval=interval,
                    materialization_task_params=materialization_task_params,
                    executor=executor,
                )
            else:
                materialize_interval(
                    interval=interval,
                    materialization_task_params=materialization_task_params,
                    job_status_client=job_status_client,
                    executor=executor,
                )

    # For Bulk Backfill, we need to export data from offline store to the intermediate store here. And then we have a
    # separate job to import the data from the intermediate store to the online store.
    should_write_to_online_from_offline_store = (
        batch_params.write_to_online_feature_store
        and batch_params.read_from_offline_store_for_online_write
        and not is_plan_integration_test_job
    )
    if should_write_to_online_from_offline_store:
        fd = feature_definition_from_task_params(materialization_task_params)
        qt = get_bootstrap_bulk_backfill_qt(
            fd, batch_params.feature_start_time.ToDatetime(), batch_params.feature_end_time.ToDatetime()
        )
        bulk_backfill_data = executor.exec_qt(qt).result_table

        bulk_backfill_stage_monitor = job_status_client.create_stage_monitor(
            TectonManagedStage.StageType.BULK_LOAD,
            "Upload Backfill data to the intermediate Bulk Load store",
        )
        with bulk_backfill_stage_monitor():
            output_arrow_data_as_json(
                bulk_backfill_data,
                materialization_task_params.batch_task_info.dynamodb_json_output_path,
                materialization_task_params.feature_view,
            )

        update_status_table(
            materialization_task_params.online_store_writer_config,
            materialization_task_params.feature_view,
            fd,
            materialization_task_params.batch_task_info.batch_parameters.feature_end_time,
        )


def output_arrow_data_as_json(bulk_backfill_data: pyarrow.RecordBatchReader, output_path: str, fv: FeatureView):
    # Encode the bulk backfill data to Json and write to the intermediate store
    while True:
        try:
            next_batch = bulk_backfill_data.read_next_batch()
        except StopIteration:
            return
        batch_bytes = serialize_pyarrow_batch(next_batch)
        output_arrow_record_batch(batch_bytes, fv, output_path)


def serialize_pyarrow_batch(next_batch) -> bytes:
    sink = pyarrow.BufferOutputStream()
    with pyarrow.ipc.new_stream(sink, next_batch.schema) as writer:
        writer.write_batch(next_batch)
    return sink.getvalue().to_pybytes()


def output_arrow_record_batch(batch_bytes: bytes, fv: FeatureView, output_path: str):
    runner_function = ray.cross_language.java_function(
        "com.tecton.onlinestorewriter.OutputArrowBatchAsDynamoJson", "runFromArrowRecordBatch"
    )
    job = runner_function.remote(batch_bytes, fv.SerializeToString(), output_path)
    ray.get(job)


def materialize_interval_for_plan_integration_test(
    interval: TimeInterval,
    materialization_task_params: MaterializationTaskParams,
    executor: QueryTreeExecutor,
):
    # skip writing to offline store to not overwrite prod data
    fd = feature_definition_from_task_params(materialization_task_params)
    qt = _get_batch_materialization_plan(fd, interval)
    materialized_data = executor.exec_qt(qt).result_table
    num_rows = sum(batch.num_rows for batch in materialized_data)
    logger.info(f"Generated {num_rows} rows for FV {fd.name} for interval from {interval.start} to {interval.end}")


def _calculate_materialized_data(
    executor: QueryTreeExecutor,
    fd: FeatureDefinitionWrapper,
    interval: TimeInterval,
) -> pyarrow.RecordBatchReader:
    qt = _get_batch_materialization_plan(fd, interval)
    materialized_data = executor.exec_qt(qt).result_table

    # Sorting rows withing batches helps improve writing parquet files: fewer partitions are written in parallel.
    # Also, secondary sorting by join keys can improve reading performance (if filter by join key will be pushed down to arrow reader).
    return sort_rows_in_batches(
        materialized_data,
        by=[(offline_store.TIME_PARTITION, PYARROW_ASC), *[(key, PYARROW_ASC) for key in fd.join_keys]],
    )


def materialize_interval(
    interval: TimeInterval,
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    fd = feature_definition_from_task_params(materialization_task_params)
    assert fd.writes_to_offline_store, f"Offline materialization is required for FeatureView {fd.id} ({fd.name})"
    assert fd.has_delta_offline_store, f"Delta is required for FeatureView {fd.id} ({fd.name})"

    batch_params = materialization_task_params.batch_task_info.batch_parameters
    should_write_to_online_store_from_source = (
        batch_params.write_to_online_feature_store and not batch_params.read_from_offline_store_for_online_write
    )

    is_overwrite = materialization_task_params.batch_task_info.batch_parameters.is_overwrite

    delta_writer = get_delta_writer_for_fd(materialization_task_params)
    parts = None

    transaction_metadata = metadata_pb2.TectonDeltaMetadata()
    transaction_metadata.feature_start_time.FromDatetime(interval.start)
    transaction_exists = delta_writer.transaction_exists(transaction_metadata)
    if not is_overwrite and transaction_exists:
        offline_stage_monitor = job_status_client.create_stage_monitor(
            TectonManagedStage.StageType.OFFLINE_STORE,
            f"Skipping writing to offline store. Found previous commit in range {interval.start} - {interval.end}",
        )
        with offline_stage_monitor():
            logger.info(
                f"Found previous commit with metadata {transaction_metadata} for data in range {interval.start} - {interval.end}. Skipping writing to delta table."
            )
    else:

        @delta_writer.transaction(transaction_metadata)
        def txn() -> List[str]:
            if is_overwrite:
                delta_writer.delete_time_range(interval)
            materialized_data = _calculate_materialized_data(executor, fd, interval)
            offline_stage_monitor = job_status_client.create_stage_monitor(
                TectonManagedStage.StageType.OFFLINE_STORE,
                "Unload features to offline store",
            )
            with offline_stage_monitor():
                return delta_writer.write(materialized_data)

        parts = txn()

    if should_write_to_online_store_from_source:
        online_stage_monitor = job_status_client.create_stage_monitor(
            TectonManagedStage.StageType.ONLINE_STORE,
            "Unload features to online store",
        )
        with online_stage_monitor(), contextlib.ExitStack() as stack:
            if parts is None:
                # We skipped the txn because of matching metadata, but we still need to write out the parquet files for
                # the online store writer. We can accomplish this by using write() and then later abort() to delete
                # the files when we're done with them.
                materialized_data = _calculate_materialized_data(executor, fd, interval)

                parts = delta_writer.write(materialized_data)
                stack.callback(delta_writer.abort)

            # TODO(meastham): Probably should send these all at once to the online store copier
            for uri in parts:
                write_to_online_store(
                    materialization_task_params.online_store_writer_config,
                    materialization_task_params.feature_view,
                    materialization_task_params.batch_task_info.batch_parameters.feature_end_time,
                    fd,
                    uri,
                )


def _get_batch_materialization_plan(fd: FeatureDefinitionWrapper, interval: TimeInterval) -> NodeRef:
    tree = build_materialization_querytree(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        fdw=fd,
        for_stream=False,
        feature_data_time_limits=interval.to_pendulum(),
    )
    return AddTimePartitionNode.for_feature_definition(fd, tree)


def sort_rows_in_batches(reader: pyarrow.RecordBatchReader, by: List[Tuple[str, str]]) -> pyarrow.RecordBatchReader:
    """
    Create new RecordBatchReader with rows sorted within each batch.

    :param reader: iterator over record batches
    :param by: sorting conditions - list of tuple(name, order)
    """

    def batch_iter():
        while True:
            try:
                next_batch = reader.read_next_batch()
            except StopIteration:
                return

            yield next_batch.sort_by(by)

    return pyarrow.RecordBatchReader.from_batches(reader.schema, batch_iter())
