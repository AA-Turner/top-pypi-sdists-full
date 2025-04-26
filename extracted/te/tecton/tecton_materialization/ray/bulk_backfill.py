from datetime import datetime
from typing import Tuple

import boto3

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import query_consts
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import TakeLastRowNode
from tecton_materialization.common.task_params import TimeInterval


# TODO(liangqi): Use this function in the Spark code to unify the behaviors.
# https://tecton.atlassian.net/browse/BC-3701
def get_bootstrap_bulk_backfill_qt(
    fd: FeatureDefinitionWrapper, start_time: datetime, end_time: datetime
) -> Tuple[NodeRef, TimeInterval]:
    conf.set("CLUSTER_REGION", boto3.Session().region_name)

    tree = OfflineStoreScanNode(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        feature_definition_wrapper=fd,
        partition_time_filter=pendulum.Period(start_time, end_time),
    ).as_ref()

    tree = StagingNode(
        dialect=Dialect.ARROW,
        compute_mode=ComputeMode.RIFT,
        input_node=tree,
        staging_table_name=f"offline_store_{fd.name}",
    ).as_ref()

    tree = FeatureTimeFilterNode(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        input_node=tree,
        feature_data_time_limits=pendulum.Period(start_time, end_time),
        policy=fd.time_range_policy,
        start_timestamp_field=fd.timestamp_key if fd.is_temporal else query_consts.anchor_time(),
        end_timestamp_field=fd.timestamp_key if fd.is_temporal else query_consts.anchor_time(),
        is_timestamp_format=fd.is_temporal,
        feature_store_format_version=fd.get_feature_store_format_version,
    ).as_ref()

    if fd.is_temporal:
        tree = TakeLastRowNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=tree,
            partition_by_columns=fd.join_keys,
            order_by_column=fd.timestamp_key,
        ).as_ref()

    return tree
