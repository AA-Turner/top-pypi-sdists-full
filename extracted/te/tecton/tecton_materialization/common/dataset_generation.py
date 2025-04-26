from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Union

import tecton_core.tecton_pendulum as pendulum
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.query import builder
from tecton_core.query import nodes
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams


def get_features_from_params(
    params: Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams],
    spine: Optional[DataframeWrapper] = None,
    entities: Optional[DataframeWrapper] = None,
) -> NodeRef:
    # Spine is required for GetFeaturesForEventsParams, it needs to be in a DataframeWrapper
    if isinstance(params, GetFeaturesForEventsParams):
        if spine is None:
            error = "Spine is required for GetFeaturesForEventsParams"
            raise ValueError(error)
        if isinstance(params.fco, specs.FeatureServiceSpec):
            return get_features_for_events_for_feature_service_qt(
                dialect=params.compute_mode.default_dialect(),
                compute_mode=params.compute_mode,
                feature_set_config=params.feature_set_config,
                spine=spine,
                timestamp_key=params.timestamp_key,
                from_source=params.from_source,
            )
        elif isinstance(params.fco, FeatureDefinitionWrapper):
            return get_features_for_events_qt(
                dialect=params.compute_mode.default_dialect(),
                compute_mode=params.compute_mode,
                feature_definition=params.fco,
                spine=spine,
                timestamp_key=params.timestamp_key,
                from_source=params.from_source,
            )
    elif isinstance(params, GetFeaturesInRangeParams):
        return get_features_in_range_qt(
            dialect=params.compute_mode.default_dialect(),
            compute_mode=params.compute_mode,
            feature_definition=params.fco,
            start_time=params.start_time,
            end_time=params.end_time,
            max_lookback=params.max_lookback,
            entities=entities,
            from_source=params.from_source,
        )
    else:
        error = f"Unsupported params type: {type(params)}"
        raise ValueError(error)


def get_features_in_range_qt(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    start_time: Union[pendulum.DateTime, datetime],
    end_time: Union[pendulum.DateTime, datetime],
    max_lookback: Optional[timedelta],
    entities: Optional[DataframeWrapper],
    from_source: Optional[bool],
) -> NodeRef:
    start_time = pendulum.instance(start_time)
    if feature_definition.feature_start_timestamp is not None:
        start_time = max(start_time, feature_definition.feature_start_timestamp)
    query_time_range = pendulum.Period(start_time, pendulum.instance(end_time))

    if feature_definition.is_temporal or feature_definition.is_feature_table:
        lookback_time_range = time_utils.temporal_fv_get_feature_data_time_limits(
            feature_definition, query_time_range, max_lookback
        )
        qt = builder.build_temporal_time_range_validity_query(
            dialect=dialect,
            compute_mode=compute_mode,
            fd=feature_definition,
            from_source=from_source,
            query_time_range=query_time_range,
            lookback_time_range=lookback_time_range,
            entities=entities,
        )
    else:
        feature_data_time_limits = time_utils.get_feature_data_time_limits(
            fd=feature_definition,
            spine_time_limits=query_time_range,
        )
        qt = builder.build_aggregated_time_range_validity_query(
            dialect=dialect,
            compute_mode=compute_mode,
            fdw=feature_definition,
            feature_data_time_limits=feature_data_time_limits,
            query_time_range=query_time_range,
            from_source=from_source,
            entities=entities,
        )
    return qt


def get_features_for_events_for_feature_service_qt(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_set_config: FeatureSetConfig,
    spine: DataframeWrapper,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> NodeRef:
    return _get_historical_features_for_feature_set(
        dialect, compute_mode, feature_set_config, spine, timestamp_key, from_source
    )


def _get_historical_features_for_feature_set(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_set_config: FeatureSetConfig,
    spine: DataframeWrapper,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> NodeRef:
    user_data_node = nodes.UserSpecifiedDataNode(dialect, compute_mode, spine, {"timestamp_key": timestamp_key})
    user_data_node = nodes.ConvertTimestampToUTCNode(dialect, compute_mode, user_data_node.as_ref(), timestamp_key)

    tree = builder.build_feature_set_config_querytree(
        dialect,
        compute_mode,
        feature_set_config,
        user_data_node.as_ref(),
        timestamp_key,
        from_source,
    )
    return tree


def get_features_for_events_qt(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    spine: DataframeWrapper,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> NodeRef:
    return _point_in_time_get_historical_features_for_feature_definition(
        dialect, compute_mode, feature_definition, spine, timestamp_key, from_source
    )


def _point_in_time_get_historical_features_for_feature_definition(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    spine: DataframeWrapper,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> NodeRef:
    dac = FeatureDefinitionAndJoinConfig.from_feature_definition(feature_definition)
    user_data_node_metadata = {}
    user_data_node = nodes.UserSpecifiedDataNode(dialect, compute_mode, spine, user_data_node_metadata)

    if timestamp_key:
        user_data_node_metadata["timestamp_key"] = timestamp_key
        user_data_node = nodes.ConvertTimestampToUTCNode(dialect, compute_mode, user_data_node.as_ref(), timestamp_key)

    qt = builder.build_spine_join_querytree(
        dialect=dialect,
        compute_mode=compute_mode,
        dac=dac,
        spine_node=user_data_node.as_ref(),
        spine_time_field=timestamp_key,
        from_source=from_source,
        use_namespace_feature_prefix=True,
    )

    return qt
