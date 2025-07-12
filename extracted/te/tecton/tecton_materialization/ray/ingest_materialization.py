import contextlib
import logging
from typing import List
from typing import Optional

import pyarrow
import pyarrow.compute as pc
import pyarrow.parquet as pq
from google.protobuf import timestamp_pb2

from tecton_core import duckdb_factory
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.schema_validation import cast
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_writer_for_fd
from tecton_materialization.ray.materialization_utils import write_to_online_store
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.offline_store_writer import OfflineStoreWriter
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.offlinestore.delta import metadata__client_pb2 as metadata_pb2


logger = logging.getLogger(__name__)


def _write_to_offline_store(
    writer: OfflineStoreWriter, materialized_data: pyarrow.Table, ingest_path: str
) -> Optional[List[str]]:
    transaction_metadata = metadata_pb2.TectonDeltaMetadata(ingest_path=ingest_path)
    if writer.transaction_exists(transaction_metadata):
        return None

    @writer.transaction(transaction_metadata)
    def txn():
        return writer.write(materialized_data)

    return txn()


def _maybe_add_partition_node(fd: FeatureDefinition, staging_node: NodeRef) -> NodeRef:
    if fd.has_iceberg_offline_store:
        # We don't need time partition in the iceberg offline store setup
        return staging_node
    else:
        # Add partition column. It needs to be present before sending the data over to the offline store writer.
        return AddTimePartitionNode.for_feature_definition(fd, staging_node)


def ingest_pushed_df(
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinition,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
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
    if not (fd.has_delta_offline_store or fd.has_iceberg_offline_store):
        msg = f"Delta or Iceberg offline store format is required for FeatureTables {fd.id} ({fd.name})"
        raise Exception(msg)

    table_for_ingest = pq.read_table(ingest_path)

    timestamp_key = fd.timestamp_key
    assert timestamp_key is not None

    if timestamp_key not in table_for_ingest.column_names:
        msg = f"Timestamp column {timestamp_key} was not present in the ingested dataframe"
        raise TectonValidationError(msg)

    writer = get_writer_for_fd(materialization_task_params)
    conn = duckdb_factory.create_connection(executor.duckdb_config)

    # Validate the schema and normalize types
    staging_table = cast(table_for_ingest, fd.view_schema)

    staging_node = ConvertTimestampToUTCNode(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        input_node=StagedTableScanNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            staged_schema=fd.view_schema,
            staging_table_name="staging_table",
        ).as_ref(),
        timestamp_key=timestamp_key,
    ).as_ref()

    tree = _maybe_add_partition_node(fd, staging_node)

    table_with_partition_column = conn.sql(tree.to_sql()).arrow()

    assert ingest_task_info.ingest_parameters.write_to_offline_feature_store, "must write to the offline feature store"
    logger.info(f"Ingesting to the OfflineStore FT: {fd.id}")
    offline_stage_monitor = job_status_client.create_stage_monitor(
        "Write features to offline store",
    )
    with offline_stage_monitor():
        parts = _write_to_offline_store(writer, table_with_partition_column, ingest_path)

    if ingest_task_info.ingest_parameters.write_to_online_feature_store:
        max_timestamp = pc.max(table_with_partition_column[timestamp_key]).as_py()
        raw_data_end_time_epoch = timestamp_pb2.Timestamp()
        raw_data_end_time_epoch.FromDatetime(max_timestamp)

        logger.info(f"Ingesting to the OnlineStore FT: {fd.id}")
        online_stage_monitor = job_status_client.create_stage_monitor(
            "Write features to online store",
        )
        with online_stage_monitor(), contextlib.ExitStack() as stack:
            if parts is None:
                parts = writer.write(table_with_partition_column)
                stack.callback(writer.abort)
            for uri in parts:
                write_to_online_store(
                    materialization_task_params.online_store_writer_config,
                    materialization_task_params.feature_view,
                    raw_data_end_time_epoch,
                    fd,
                    uri,
                )
