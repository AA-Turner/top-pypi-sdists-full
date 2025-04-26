from datetime import datetime
from datetime import timedelta
from typing import Tuple

import boto3

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import query_consts
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.builder import build_aggregated_time_range_validity_query
from tecton_core.query.builder import build_temporal_time_range_validity_query
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query_consts import valid_from
from tecton_core.query_consts import valid_to
from tecton_core.schema_derivation_utils import compute_features_schema_from_feature_definition
from tecton_core.time_utils import convert_to_effective_timestamp
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.nodes import TimeSpec
from tecton_proto.common import data_type__client_pb2 as data_type_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2


def get_feature_export_qt(
    fd: FeatureDefinitionWrapper, materialization_start_time: datetime, materialization_end_time: datetime
) -> Tuple[NodeRef, TimeInterval]:
    # retrieve current region
    conf.set("CLUSTER_REGION", boto3.Session().region_name)

    # read api uses effective timestamps for querying time ranges
    effective_start_time = datetime.fromtimestamp(
        convert_to_effective_timestamp(
            int(materialization_start_time.timestamp()),
            fd.batch_materialization_schedule.in_seconds(),
            fd.max_source_data_delay.in_seconds(),
        ),
        pendulum.tz.UTC,
    )
    effective_end_time = datetime.fromtimestamp(
        convert_to_effective_timestamp(
            int(materialization_end_time.timestamp()),
            fd.batch_materialization_schedule.in_seconds(),
            fd.max_source_data_delay.in_seconds(),
        ),
        pendulum.tz.UTC,
    )

    # TODO (TEC-18861): this is temporary pending getting tecton sdk into anyscale/ray cluster environment
    # will switch to `fv.get_features_in_range()` instead
    query_time_range = pendulum.Period(effective_start_time, effective_end_time)
    if fd.is_temporal:
        start_lookback = pendulum.from_timestamp(0)
        end_lookback = query_time_range.end + fd.batch_materialization_schedule
        if fd.serving_ttl:
            start_lookback = query_time_range.start - fd.serving_ttl - fd.max_source_data_delay
        if fd.feature_start_timestamp:
            start_lookback = max(start_lookback, fd.feature_start_timestamp)
        lookback_time_range = pendulum.Period(start_lookback, end_lookback)
        qt = build_temporal_time_range_validity_query(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            fd=fd,
            from_source=False,
            query_time_range=query_time_range,
            lookback_time_range=lookback_time_range,
            entities=None,
        )
    elif fd.is_temporal_aggregate:
        feature_data_start_limit = query_time_range.start - fd.max_source_data_delay
        feature_data_end_limit = query_time_range.end + fd.batch_materialization_schedule
        if fd.feature_start_timestamp:
            feature_data_start_limit = max(feature_data_start_limit, fd.feature_start_timestamp)
        if fd.has_lifetime_aggregate:
            feature_data_start_limit = pendulum.from_timestamp(0)
        else:
            feature_data_start_limit = feature_data_start_limit + fd.earliest_window_start
        if fd.materialization_start_timestamp:
            feature_data_start_limit = max(feature_data_start_limit, fd.materialization_start_timestamp)

        feature_data_time_limits = pendulum.Period(feature_data_start_limit, feature_data_end_limit)
        qt = build_aggregated_time_range_validity_query(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            fdw=fd,
            from_source=False,
            query_time_range=query_time_range,
            feature_data_time_limits=feature_data_time_limits,
            entities=None,
        )
    else:
        msg = "FV type not supported for feature export."
        raise ValueError(msg)

    # add partition column, partitioned on _valid_from timestamp
    qt = AddTimePartitionNode(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        input_node=qt,
        time_spec=feature_export_time_spec(),
    ).as_ref()

    # return the interval we queried
    interval = TimeInterval(effective_start_time, effective_end_time)

    return qt, interval


def get_feature_export_store_params(fd: FeatureDefinitionWrapper) -> OfflineStoreParams:
    schema = schema_pb2.Schema(columns=compute_features_schema_from_feature_definition(fd).columns)
    to_remove = [col for col in schema.columns if col.name in (fd.timestamp_key, query_consts.anchor_time())]
    for col in to_remove:
        schema.columns.remove(col)

    valid_from_column = schema_pb2.Column(
        name=valid_from(),
        offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_TIMESTAMP),
    )
    valid_to_column = schema_pb2.Column(
        name=valid_to(),
        offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_TIMESTAMP),
    )
    schema.columns.append(valid_from_column)
    schema.columns.append(valid_to_column)
    feature_params = OfflineStoreParams(
        feature_view_id=fd.id,
        feature_view_name=fd.name,
        schema=schema,
        time_spec=feature_export_time_spec(),
        feature_store_format_version=fd.get_feature_store_format_version,
        batch_schedule=fd.get_batch_schedule_for_version,
    )
    return feature_params


def feature_export_time_spec():
    return TimeSpec(
        timestamp_key=valid_from(),
        partition_size=timedelta(days=1),
        time_column=valid_from(),
        partition_is_anchor=False,
    )
