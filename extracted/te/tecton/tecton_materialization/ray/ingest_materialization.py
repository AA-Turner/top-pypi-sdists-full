import contextlib
import logging
from typing import List
from typing import Optional

import pyarrow
import pyarrow.compute as pc
import pyarrow.parquet as pq
from google.protobuf import timestamp_pb2

from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.offline_store import TIME_PARTITION
from tecton_core.offline_store import partition_size_for_delta
from tecton_core.offline_store import timestamp_formats
from tecton_core.schema_validation import cast
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer_for_fd
from tecton_materialization.ray.materialization_utils import write_to_online_store
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.offlinestore.delta import metadata__client_pb2 as metadata_pb2


logger = logging.getLogger(__name__)


def _write_to_offline_store(
    delta_writer: DeltaWriter, materialized_data: pyarrow.Table, ingest_path: str
) -> Optional[List[str]]:
    transaction_metadata = metadata_pb2.TectonDeltaMetadata(ingest_path=ingest_path)
    if delta_writer.transaction_exists(transaction_metadata):
        return None

    @delta_writer.transaction(transaction_metadata)
    def txn():
        return delta_writer.write(materialized_data)

    return txn()


def ingest_pushed_df(
    materialization_task_params: MaterializationTaskParams, fd: FeatureDefinition, job_status_client: JobStatusClient
):
    """
    Triggers materialization from the specified parquet file.

    # NOTE: The Rift version of this job is a bit different compared to Spark:
    - Spark does not require writing to the offline store first.
    - For the offline store, we're currently appending the rows. Spark overwrites existing rows and only inserts new ones.
    """
    ingest_task_info = materialization_task_params.ingest_task_info
    ingest_path = ingest_task_info.ingest_parameters.ingest_path

    if not fd.writes_to_offline_store:
        msg = f"Offline materialization is required for FeatureTables on Rift {fd.id} ({fd.name})"
        raise Exception(msg)
    if not fd.has_delta_offline_store:
        msg = f"Delta is required for FeatureTables {fd.id} ({fd.name})"
        raise Exception(msg)

    table_for_ingest = pq.read_table(ingest_path)

    timestamp_key = fd.timestamp_key
    assert timestamp_key is not None

    if timestamp_key not in table_for_ingest.column_names:
        msg = f"Timestamp column {timestamp_key} was not present in the ingested dataframe"
        raise TectonValidationError(msg)

    # Validate the schema and normalize types
    table_for_ingest = cast(table_for_ingest, fd.view_schema)

    # Add partition column. It needs to be present before sending the data over to the offline store writer.
    # TODO: switch to DuckDB - https://tecton.atlassian.net/browse/TEC-18995
    partition_size = partition_size_for_delta(fd).as_timedelta()
    ts_format = timestamp_formats(partition_size).python_format
    partition_column = pc.strftime(table_for_ingest[timestamp_key], format=ts_format)
    table_for_ingest = table_for_ingest.append_column(pyarrow.field(TIME_PARTITION, pyarrow.string()), partition_column)

    delta_writer = get_delta_writer_for_fd(materialization_task_params)
    assert ingest_task_info.ingest_parameters.write_to_offline_feature_store, "must write to the offline feature store"
    logger.info(f"Ingesting to the OfflineStore FT: {fd.id}")
    offline_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE,
        "Unload features to offline store",
    )
    with offline_stage_monitor():
        parts = _write_to_offline_store(delta_writer, table_for_ingest, ingest_path)

    if ingest_task_info.ingest_parameters.write_to_online_feature_store:
        max_timestamp = pc.max(table_for_ingest[timestamp_key]).as_py()
        raw_data_end_time_epoch = timestamp_pb2.Timestamp()
        raw_data_end_time_epoch.FromDatetime(max_timestamp)

        logger.info(f"Ingesting to the OnlineStore FT: {fd.id}")
        online_stage_monitor = job_status_client.create_stage_monitor(
            TectonManagedStage.StageType.ONLINE_STORE,
            "Unload features to online store",
        )
        with online_stage_monitor(), contextlib.ExitStack() as stack:
            if parts is None:
                parts = delta_writer.write(table_for_ingest)
                stack.callback(delta_writer.abort)
            for uri in parts:
                write_to_online_store(
                    materialization_task_params.online_store_writer_config,
                    materialization_task_params.feature_view,
                    raw_data_end_time_epoch,
                    fd,
                    uri,
                )
