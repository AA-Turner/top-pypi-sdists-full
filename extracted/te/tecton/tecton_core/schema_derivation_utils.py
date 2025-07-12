import datetime
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional

from tecton_core import aggregation_utils
from tecton_core import data_types as tecton_types
from tecton_core import errors
from tecton_core import query_consts
from tecton_core import schema as core_schema
from tecton_core import specs
from tecton_core.aggregation_utils import get_aggregation_function_result_type
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.specs import LifetimeWindowSpec
from tecton_core.specs import RelativeTimeWindowSpec
from tecton_core.specs import utils
from tecton_core.specs import window_spec_to_window_data_proto
from tecton_proto.args import feature_view__client_pb2 as feature_view__args_pb2
from tecton_proto.args import feature_view__client_pb2 as feature_view_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.modelartifactservice import model_artifact_data__client_pb2 as model_artifact_service_pb2


def _get_timestamp_field(feature_view_args: feature_view_pb2.FeatureViewArgs, view_schema: schema_pb2.Schema) -> str:
    if feature_view_args.materialized_feature_view_args.HasField("timestamp_field"):
        timestamp_key = feature_view_args.materialized_feature_view_args.timestamp_field
    else:
        timestamp_fields = [
            column for column in view_schema.columns if column.offline_data_type == tecton_types.TimestampType().proto
        ]

        if len(timestamp_fields) != 1:
            msg = "The timestamp_field must be set on the Feature View or the feature view transformation output should contain only one and only one column of type Timestamp"
            raise errors.TectonValidationError(msg)
        timestamp_key = timestamp_fields[0].name

    view_schema_column_names = [column.name for column in view_schema.columns]
    if timestamp_key not in view_schema_column_names:
        msg = f"Timestamp key '{timestamp_key}' not found in view schema. View schema has columns: {', '.join(view_schema_column_names)}"
        raise errors.TectonValidationError(msg)
    return timestamp_key


def populate_schema_with_derived_fields(schema: schema_pb2.Schema) -> None:
    """Copies the behavior of populateSchemaWithDerivedFields in FeatureViewUtils.kt.

    Should only be applied to feature views w/ push sources or explicit schemas in NDD,
    which are expected to only have the offline_data_type field set.
    """
    for column in schema.columns:
        assert column.offline_data_type is not None
        offline_data_type = tecton_types.data_type_from_proto(column.offline_data_type)
        feature_server_data_type = core_schema.get_feature_server_data_type(offline_data_type)
        column.feature_server_data_type.CopyFrom(feature_server_data_type.proto)


def _get_aggregation_columns(
    view_schema_column_map: Dict[str, schema_pb2.Column],
    aggregation: feature_view_pb2.FeatureAggregation,
    is_continuous: bool,
) -> List[schema_pb2.Column]:
    input_column = view_schema_column_map[aggregation.column]
    prefixes = aggregation_utils.get_materialization_aggregation_column_prefixes(
        aggregation_utils.get_aggregation_enum_from_string(aggregation.function.lower()),
        aggregation.function_params,
        is_continuous,
    )
    columns = []
    for prefix in prefixes:
        materialization_column_name = aggregation_utils.get_materialization_column_name(prefix, input_column.name)

        tecton_type = aggregation_utils.aggregation_prefix_to_tecton_type(
            prefix, tecton_types.data_type_from_proto(input_column.offline_data_type)
        )
        if tecton_type is None:
            tecton_type = tecton_types.data_type_from_proto(input_column.offline_data_type)

        column_proto = schema_pb2.Column()
        column_proto.CopyFrom(core_schema.column_from_tecton_data_type(tecton_type))
        column_proto.name = materialization_column_name
        columns.append(column_proto)

    return columns


def compute_features_schema_from_feature_definition(
    fd: FeatureDefinitionWrapper,
) -> schema_pb2.Schema:
    if not fd.is_temporal_aggregate:
        return fd.materialization_schema.proto

    materialization_schema_columns = []
    view_schema_column_map = {column.name: column for column in fd.view_schema.proto.columns}

    for join_key in fd.join_keys:
        materialization_schema_columns.append(view_schema_column_map[join_key])

    if fd.aggregation_secondary_key:
        materialization_schema_columns.append(view_schema_column_map[fd.aggregation_secondary_key])

    for aggregation in fd.fv_spec.aggregate_features:
        input_column = view_schema_column_map[aggregation.input_feature_name]
        input_type = tecton_types.data_type_from_proto(input_column.offline_data_type)
        tecton_type = get_aggregation_function_result_type(aggregation, input_type)

        column_proto = schema_pb2.Column()
        column_proto.CopyFrom(core_schema.column_from_tecton_data_type(tecton_type))
        column_proto.name = aggregation.output_feature_name
        materialization_schema_columns.append(column_proto)

    column_proto = schema_pb2.Column()
    column_proto.CopyFrom(core_schema.column_from_tecton_data_type(tecton_types.Int64Type()))
    column_proto.name = query_consts.anchor_time()
    materialization_schema_columns.append(column_proto)

    return schema_pb2.Schema(columns=materialization_schema_columns)


def compute_aggregate_materialization_schema_from_view_schema(
    view_schema: schema_pb2.Schema,
    feature_view_args: feature_view_pb2.FeatureViewArgs,
    model_artifacts: Optional[Dict[str, model_artifact_service_pb2.ModelArtifactInfo]] = None,
) -> schema_pb2.Schema:
    is_aggregate = len(feature_view_args.materialized_feature_view_args.aggregations) > 0
    has_embeddings = len(feature_view_args.materialized_feature_view_args.embeddings) > 0
    has_inferences = len(feature_view_args.materialized_feature_view_args.inferences) > 0
    if not (is_aggregate or has_embeddings or has_inferences):
        return view_schema

    materialization_schema_columns = []
    view_schema_column_map = {column.name: column for column in view_schema.columns}

    # Add join key columns from view schema to materialization schema.
    join_keys = specs.get_join_keys_from_feature_view_args(feature_view_args)
    for join_key in join_keys:
        if join_key not in view_schema_column_map:
            msg = f"Join key {join_key} not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
            raise errors.TectonValidationError(msg)
        materialization_schema_columns.append(view_schema_column_map[join_key])

    if is_aggregate:
        if feature_view_args.materialized_feature_view_args.aggregation_secondary_key:
            materialization_schema_columns.append(
                view_schema_column_map[feature_view_args.materialized_feature_view_args.aggregation_secondary_key]
            )

        # Add columns for aggregate features.
        added = []
        for aggregation in feature_view_args.materialized_feature_view_args.aggregations:
            if aggregation.column not in view_schema_column_map:
                msg = f"Column {aggregation.column} used for aggregations not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
                raise errors.TectonValidationError(msg)

            is_continuous = specs.get_is_continuous_from_feature_view_args(feature_view_args)

            columns = _get_aggregation_columns(view_schema_column_map, aggregation, is_continuous)

            for col in columns:
                if col.name not in added:
                    materialization_schema_columns.append(col)
                    added.append(col.name)

        # Add column for timestamp.
        column_proto = schema_pb2.Column()
        column_proto.CopyFrom(core_schema.column_from_tecton_data_type(tecton_types.Int64Type()))
        column_proto.name = query_consts.anchor_time()
        materialization_schema_columns.append(column_proto)
    elif has_embeddings or has_inferences:
        for attribute in feature_view_args.materialized_feature_view_args.attributes:
            if attribute.name not in view_schema_column_map:
                msg = f"Attribute {attribute.name} not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
                raise errors.TectonValidationError(msg)
            materialization_schema_columns.append(view_schema_column_map[attribute.name])

        timestamp_key = _get_timestamp_field(feature_view_args, view_schema)
        materialization_schema_columns.append(view_schema_column_map[timestamp_key])

        for f in feature_view_args.materialized_feature_view_args.embeddings:
            column_proto = schema_pb2.Column()
            column_proto.CopyFrom(
                core_schema.column_from_tecton_data_type(tecton_types.ArrayType(tecton_types.Float32Type()))
            )
            column_proto.name = f.name
            materialization_schema_columns.append(column_proto)

        for f in feature_view_args.materialized_feature_view_args.inferences:
            if model_artifacts and f.model in model_artifacts:
                model_artifact_info = model_artifacts[f.model]
                column_proto = schema_pb2.Column(
                    name=f.name, offline_data_type=model_artifact_info.output_schema.columns[0].offline_data_type
                )
                materialization_schema_columns.append(column_proto)

    return schema_pb2.Schema(columns=materialization_schema_columns)


def compute_batch_table_format_for_compaction(
    feature_view_args: feature_view_pb2.FeatureViewArgs,
    view_schema: schema_pb2.Schema,
) -> schema_pb2.OnlineBatchTableFormat:
    aggregations = feature_view_args.materialized_feature_view_args.aggregations
    if aggregations:
        has_time_window_series = any(aggregation.HasField("time_window_series") for aggregation in aggregations)
        if has_time_window_series:
            msg = "Time Window Series aggregations are not supported when compaction is enabled."
            raise errors.TectonValidationError(msg)

        is_continuous = (
            feature_view_args.materialized_feature_view_args.stream_processing_mode
            == feature_view_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
        )
        return _compute_batch_table_schema_for_aggregate_feature_view(view_schema, aggregations, is_continuous)

    join_keys = specs.get_join_keys_from_feature_view_args(feature_view_args)
    ttl = utils.get_duration_field_or_none(feature_view_args.materialized_feature_view_args, "serving_ttl")
    timestamp_field = specs.resolve_timestamp_field_for_materialized_feature_view(feature_view_args, view_schema)
    return _compute_batch_table_schema_for_temporal_feature_view(view_schema, join_keys, timestamp_field, ttl)


def _compute_batch_table_schema_for_temporal_feature_view(
    view_schema: schema_pb2.Schema,
    join_keys: List[str],
    timestamp_key: str,
    serving_ttl: Optional[datetime.timedelta],
) -> schema_pb2.OnlineBatchTableFormat:
    if serving_ttl is None:
        window = LifetimeWindowSpec()
    else:
        window = RelativeTimeWindowSpec(-1 * serving_ttl, datetime.timedelta())
    output_columns = (col for col in view_schema.columns if col.name not in join_keys and col.name != timestamp_key)
    output_schema = schema_pb2.Schema(columns=sorted(output_columns, key=lambda col: col.name))
    part = schema_pb2.OnlineBatchTablePart(
        window_index=0, time_window=window_spec_to_window_data_proto(window), schema=output_schema
    )
    return schema_pb2.OnlineBatchTableFormat(online_batch_table_parts=[part])


def _compute_batch_table_schema_for_aggregate_feature_view(
    view_schema: schema_pb2.Schema,
    aggregations: List[feature_view__args_pb2.FeatureAggregation],
    is_continuous: bool,
) -> schema_pb2.OnlineBatchTableFormat:
    view_schema_column_map = {column.name: column for column in view_schema.columns}

    grouped_aggs = defaultdict(list)

    # Group by
    for aggregation in aggregations:
        if aggregation.HasField("time_window"):
            key = RelativeTimeWindowSpec.from_args_proto(aggregation.time_window)
        elif aggregation.HasField("lifetime_window"):
            key = LifetimeWindowSpec()
        else:
            msg = f"Unexpected time window type in aggregation args proto: {aggregation}"
            raise ValueError(msg)

        grouped_aggs[key].append(aggregation)

    # Sort by two keys
    sorted_grouped_aggs = sorted(grouped_aggs.items(), key=lambda item: item[0].to_sort_tuple())

    parts = []

    for index, (window, sub_aggs) in enumerate(sorted_grouped_aggs):
        added = set()
        columns = []
        for aggregation in sub_aggs:
            aggregation_columns = _get_aggregation_columns(
                view_schema_column_map, aggregation, is_continuous=is_continuous
            )
            for col in aggregation_columns:
                if col.name not in added:
                    columns.append(col)
                    added.add(col.name)

        output_schema = schema_pb2.Schema(columns=sorted(columns, key=lambda col: col.name))
        # We are NOT computing the OnlineBatchTablePartTiles here since they are not used during local development.
        part = schema_pb2.OnlineBatchTablePart(
            window_index=index, time_window=window_spec_to_window_data_proto(window), schema=output_schema
        )
        parts.append(part)

    return schema_pb2.OnlineBatchTableFormat(online_batch_table_parts=parts)
