import logging
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
from pyspark import sql as pyspark_sql

import tecton_core.query.dialect
import tecton_core.tecton_pendulum as pendulum
from tecton import types as sdk_types
from tecton._internals import errors
from tecton._internals import type_utils
from tecton._internals import utils
from tecton._internals.utils import get_mocked_feature_view_columns
from tecton.framework.data_frame import TectonDataFrame
from tecton_core import conf
from tecton_core import data_types
from tecton_core import errors as core_errors
from tecton_core import feature_set_config
from tecton_core import schema
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_processing_utils import should_infer_timestamp_of_spine
from tecton_core.data_processing_utils import split_range
from tecton_core.data_processing_utils import split_spine
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.mock_context import MockContext
from tecton_core.query import builder
from tecton_core.query import node_interface
from tecton_core.query import nodes
from tecton_core.query import rewrite
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.builder import build_pipeline_querytree
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import DatasetScanNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.query.rewrite import MockDataRewrite
from tecton_core.schema import Schema
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.skew_config import SkewConfig
from tecton_core.time_utils import align_time_downwards
from tecton_core.time_utils import temporal_fv_get_feature_data_time_limits
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.data.saved_feature_data_frame__client_pb2 import SavedFeatureDataFrame
from tecton_spark.spark_helper import check_spark_version
from tecton_spark.time_utils import convert_epoch_to_datetime
from tecton_spark.time_utils import convert_timestamp_to_epoch


logger = logging.getLogger(__name__)


def get_features_from_params(
    params: Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams],
):
    if isinstance(params, GetFeaturesForEventsParams):
        if isinstance(params.fco, specs.FeatureServiceSpec):
            if conf.DUCKDB_ENABLE_SPINE_SPLIT_FF.enabled() and params.compute_mode == ComputeMode.RIFT:
                df = get_historical_features_for_feature_service_with_spine_split(
                    dialect=params.compute_mode.default_dialect(),
                    compute_mode=params.compute_mode,
                    feature_set_config=params.feature_set_config,
                    spine=params.events,
                    timestamp_key=params.timestamp_key,
                    from_source=params.from_source,
                    skew_config=params.skew_config,
                )
            else:
                df = get_historical_features_for_feature_service(
                    dialect=params.compute_mode.default_dialect(),
                    compute_mode=params.compute_mode,
                    feature_set_config=params.feature_set_config,
                    spine=params.events,
                    timestamp_key=params.timestamp_key,
                    from_source=params.from_source,
                    skew_config=params.skew_config,
                )
        elif isinstance(params.fco, FeatureDefinitionWrapper):
            df = get_features_for_events(
                dialect=params.compute_mode.default_dialect(),
                compute_mode=params.compute_mode,
                feature_definition=params.fco,
                spine=params.events,
                timestamp_key=params.timestamp_key,
                from_source=params.from_source,
                mock_data_sources=params.mock_data_sources,
                mock_context=params.mock_context,
                skew_config=params.skew_config,
            )
    elif isinstance(params, GetFeaturesInRangeParams):
        if conf.get_bool("DUCKDB_ENABLE_RANGE_SPLIT") and params.compute_mode == ComputeMode.RIFT:
            ranges = split_range(params.start_time, params.end_time, params.fco.min_scheduling_interval)
            dfs = []
            for start, end in ranges:
                df = get_features_in_range(
                    dialect=params.compute_mode.default_dialect(),
                    compute_mode=params.compute_mode,
                    feature_definition=params.fco,
                    start_time=start,
                    end_time=end,
                    max_lookback=params.max_lookback,
                    entities=params.entities,
                    from_source=params.from_source,
                    mock_data_sources=params.mock_data_sources,
                    valid_from=params.start_time,
                    valid_to=params.end_time,
                    mock_context=params.mock_context,
                    skew_config=params.skew_config,
                )
                dfs.append(df)
            df = TectonDataFrame._create_from_dataframes(dfs)
        else:
            df = get_features_in_range(
                dialect=params.compute_mode.default_dialect(),
                compute_mode=params.compute_mode,
                feature_definition=params.fco,
                start_time=params.start_time,
                end_time=params.end_time,
                max_lookback=params.max_lookback,
                entities=params.entities,
                from_source=params.from_source,
                mock_data_sources=params.mock_data_sources,
                mock_context=params.mock_context,
                skew_config=params.skew_config,
            )
    else:
        error = f"Unsupported params type: {type(params)}"
        raise ValueError(error)

    df._request_params = params
    return df


def get_historical_features_for_feature_service_with_spine_split(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_set_config: feature_set_config.FeatureSetConfig,
    spine: Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame, str],
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    skew_config: SkewConfig,
) -> TectonDataFrame:
    spine_split = split_spine(spine, feature_set_config.join_keys)
    dfs = []
    for spine_df in spine_split:
        df = get_historical_features_for_feature_service(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_set_config=feature_set_config,
            spine=spine_df,
            timestamp_key=timestamp_key,
            from_source=from_source,
            skew_config=skew_config,
        )
        dfs.append(df)
    return TectonDataFrame._create_from_dataframes(dfs)


def get_historical_features_for_feature_service(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_set_config: feature_set_config.FeatureSetConfig,
    spine: Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame, str],
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    skew_config: SkewConfig,
) -> TectonDataFrame:
    timestamp_required = spine is not None and any(
        should_infer_timestamp_of_spine(fd, timestamp_key) for fd in feature_set_config.feature_definitions
    )

    _validate_sql_string_support(dialect, spine)

    if timestamp_required:
        timestamp_key = timestamp_key or utils.infer_timestamp(spine)

    spine = _create_tecton_df_spine(
        spine_schema=feature_set_config.spine_schema, spine=spine, timestamp_key=timestamp_key
    )

    if spine:
        utils.validate_spine_dataframe(spine, timestamp_key, feature_set_config.request_context_keys)

    user_data_node_metadata = {}
    # TODO: Create a SpineNode with a param of timestamp_key instead of using UserSpecifiedNode.
    user_data_node = nodes.UserSpecifiedDataNode(dialect, compute_mode, spine, user_data_node_metadata)

    if timestamp_key:
        user_data_node_metadata["timestamp_key"] = timestamp_key
        user_data_node = nodes.ConvertTimestampToUTCNode(dialect, compute_mode, user_data_node.as_ref(), timestamp_key)

    tree = builder.build_feature_set_config_querytree(
        dialect=dialect,
        compute_mode=compute_mode,
        fsc=feature_set_config,
        spine_node=user_data_node.as_ref(),
        spine_time_field=timestamp_key,
        from_source=from_source,
        skew_config=skew_config,
    )

    df = TectonDataFrame._create(tree)
    return df


def get_features_in_range(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    start_time: Union[pendulum.DateTime, datetime],
    end_time: Union[pendulum.DateTime, datetime],
    max_lookback: Optional[timedelta],
    entities: Optional[Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame]],
    from_source: Optional[bool],
    mock_data_sources: Dict[str, NodeRef],
    valid_from: Optional[Union[pendulum.DateTime, datetime]] = None,
    valid_to: Optional[Union[pendulum.DateTime, datetime]] = None,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> TectonDataFrame:
    """
    Returns a TectonDataFrame of historical values for this feature view which were valid within
    the input time range. A feature value is considered to be valid at a specific point in time if the Online Store
    would have returned that value if queried at that moment in time.

    The DataFrame returned by this method contains the following:
    - Entity Join Key Columns
    - Feature Value Columns
    - The columns _valid_from and _valid_to that specify the time range for which the row of features values is
    valid. The time range defined by [_valid_from, _valid_to) will never intersect with any other rows for the same
    join keys.

    _valid_from (Inclusive) is the timestamp from which feature values were valid and returned from the Online Feature
    Store for the corresponding set of join keys. _valid_from will never be less than end_time.
    Values for which _valid_from is equal to start_time may have been valid prior to start_time.

    _valid_to (Exclusive) is the timestamp from which feature values are invalid and no longer returned from the
    Online Feature Store for the corresponding set of join keys. _valid_to will never be greater than end_time.
    Values for which _valid_to is equal to end_time may be valid beyond end_time.

    By default, (i.e. from_source=None), this method fetches feature values from the Offline Store for
    Feature Views that have offline materialization enabled. Otherwise, this method computes feature values directly
    from the original data source.

    :param start_time: The interval start time from when we want to retrieve features.
    :param end_time:  The interval end time until when we want to retrieve features.
    :param max_lookback: [Non-Aggregate Feature Views Only] A performance optimization that configures how far back
    before start_time to look for events in the raw data. If set, get_features_in_range() may not include all
    entities with valid feature values in the specified time range, but get_features_in_range() will never
    return invalid values.
    :param entities: A DataFrame that is used to filter down feature values.
        If specified, this DataFrame should only contain join key columns.
    :param from_source: Whether feature values should be recomputed from the original data source. If None,
    feature values will be fetched from the Offline Store for Feature Views that have offline materialization enabled
    and otherwise computes feature values on the fly from raw data. Use from_source=True to force computing from raw
    data and from_source=False to error if any Feature Views are not materialized. (Default: None)
    :param compute_mode: Compute mode to use to produce the data frame.
    :param mock_data_sources: Mock sources that should be used instead of fetching directly from raw data
        sources. The keys of the dictionary should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.
    :param valid_from: The start time for which the feature values are valid. If not provided, defaults to start_time.
    :param valid_to: The end time for which the feature values are valid. If not provided, defaults to end_time.
    :param skew_config: Configuration with levers to tune historical feature calculation. defaults to settings that minimize online/offline skew.

    :return: A TectonDataFrame with Feature Values for the requested time range in the format specified above.
    """
    if not feature_definition.is_rtfv:
        check_spark_version(feature_definition.fv_spec.batch_cluster_config)

    if entities is not None:
        if not isinstance(entities, TectonDataFrame):
            entities = TectonDataFrame._create(entities)
        assert set(entities._dataframe.columns).issubset(set(feature_definition.join_keys)), (
            f"Entities should only contain columns that can be used as Join Keys: {feature_definition.join_keys}"
        )

    start_time = pendulum.instance(start_time)
    end_time = pendulum.instance(end_time)
    if feature_definition.feature_start_timestamp is not None:
        start_time = max(start_time, feature_definition.feature_start_timestamp)
    query_time_range = pendulum.Period(start_time, end_time)
    valid_from = valid_from or start_time
    valid_to = valid_to or end_time
    # The bounds of the time range for which the feature values are valid, valid_to and valid_from values will be capped by the valid_time_range
    valid_time_range = pendulum.Period(valid_from, valid_to)

    if feature_definition.is_temporal or feature_definition.is_feature_table:
        lookback_time_range = temporal_fv_get_feature_data_time_limits(
            feature_definition, query_time_range, max_lookback
        )
        qt = builder.build_temporal_time_range_validity_query(
            dialect=dialect,
            compute_mode=compute_mode,
            fd=feature_definition,
            from_source=from_source,
            lookback_time_range=lookback_time_range,
            entities=entities,
            query_time_range=valid_time_range,
            skew_config=skew_config,
        )
    else:
        feature_data_time_limits = time_utils.get_feature_data_time_limits(
            fd=feature_definition,
            spine_time_limits=query_time_range,
        )
        qt = builder.build_aggregated_time_range_validity_query(
            dialect,
            compute_mode,
            feature_definition,
            feature_data_time_limits=feature_data_time_limits,
            query_time_range=query_time_range,
            from_source=from_source,
            entities=entities,
            skew_config=skew_config,
        )

    rewrite.MockDataRewrite(mock_data_sources).rewrite(qt)

    df = TectonDataFrame._create(qt)

    return df


def get_partial_aggregates(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    start_time: Union[pendulum.DateTime, datetime],
    end_time: Union[pendulum.DateTime, datetime],
    entities: Optional[TectonDataFrame],
    from_source: Optional[bool],
    mock_data_sources: Dict[str, NodeRef],
) -> TectonDataFrame:
    check_spark_version(feature_definition.fv_spec.batch_cluster_config)

    start_time = pendulum.instance(start_time)
    if feature_definition.feature_start_timestamp is not None:
        start_time = max(start_time, feature_definition.feature_start_timestamp)

    start_time = align_time_downwards(start_time, feature_definition.min_scheduling_interval)
    end_time = (
        align_time_downwards(end_time, feature_definition.min_scheduling_interval)
        + feature_definition.min_scheduling_interval
    )
    limits = pendulum.Period(start_time, end_time)

    qt = builder.build_get_partial_aggregates_query(
        dialect,
        compute_mode,
        feature_definition,
        limits=limits,
        from_source=from_source,
        entities=entities,
    )

    rewrite.MockDataRewrite(mock_data_sources).rewrite(qt)

    df = TectonDataFrame._create(qt)

    return df


def get_features_for_events(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    spine: Optional[Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame, str]],
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    mock_data_sources: Dict[str, NodeRef],
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
):
    if not feature_definition.is_rtfv:
        check_spark_version(feature_definition.fv_spec.batch_cluster_config)

    _validate_sql_string_support(dialect, spine)

    if should_infer_timestamp_of_spine(feature_definition, timestamp_key):
        timestamp_key = utils.infer_timestamp(spine)

    if conf.DUCKDB_ENABLE_SPINE_SPLIT_FF.enabled() and compute_mode == ComputeMode.RIFT:
        spine_split = split_spine(spine, feature_definition.join_keys)
        dfs = []
        for spine_df in spine_split:
            tecton_spine_df = _create_tecton_df_spine(
                spine_schema=feature_definition.spine_schema, spine=spine_df, timestamp_key=timestamp_key
            )

            qt = _point_in_time_get_historical_features_for_feature_definition(
                dialect, compute_mode, feature_definition, tecton_spine_df, timestamp_key, from_source, mock_context
            )

            rewrite.MockDataRewrite(mock_data_sources).rewrite(qt)

            df = TectonDataFrame._create(qt)
            dfs.append(df)

        return TectonDataFrame._create_from_dataframes(dfs)

    tecton_spine_df = _create_tecton_df_spine(
        spine_schema=feature_definition.spine_schema, spine=spine, timestamp_key=timestamp_key
    )

    qt = _point_in_time_get_historical_features_for_feature_definition(
        dialect,
        compute_mode,
        feature_definition,
        tecton_spine_df,
        timestamp_key,
        from_source,
        mock_context,
        skew_config,
    )

    rewrite.MockDataRewrite(mock_data_sources).rewrite(qt)

    df = TectonDataFrame._create(qt)
    return df


def get_historical_features_for_feature_definition(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    spine: Optional[Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame, str]],
    timestamp_key: Optional[str],
    start_time: Optional[Union[pendulum.DateTime, datetime]],
    end_time: Optional[Union[pendulum.DateTime, datetime]],
    entities: Optional[Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame]],
    from_source: Optional[bool],
    mock_data_sources: Dict[str, NodeRef],
) -> TectonDataFrame:
    if not feature_definition.is_rtfv:
        check_spark_version(feature_definition.fv_spec.batch_cluster_config)

    if spine is not None:
        logger.warning(errors.GET_HISTORICAL_FEATURES_DEPRECATED_SPINE)

        _validate_sql_string_support(dialect, spine)

        if should_infer_timestamp_of_spine(feature_definition, timestamp_key):
            timestamp_key = utils.infer_timestamp(spine)

        tecton_spine_df = _create_tecton_df_spine(
            spine_schema=feature_definition.spine_schema, spine=spine, timestamp_key=timestamp_key
        )
        qt = _point_in_time_get_historical_features_for_feature_definition(
            dialect, compute_mode, feature_definition, tecton_spine_df, timestamp_key, from_source
        )
    else:
        logger.warning(errors.GET_HISTORICAL_FEATURES_DEPRECATED_TIME_RANGE)

        if entities is not None:
            if not isinstance(entities, TectonDataFrame):
                entities = TectonDataFrame._create(entities)
            assert set(entities._dataframe.columns).issubset(set(feature_definition.join_keys)), (
                f"Entities should only contain columns that can be used as Join Keys: {feature_definition.join_keys}"
            )

        query_time_range = _get_feature_data_time_range(feature_definition, start_time, end_time)
        tecton_spine_df = None

        if feature_definition.is_temporal or feature_definition.is_feature_table:
            qt = builder.build_temporal_time_range_query(
                dialect=dialect,
                compute_mode=compute_mode,
                fd=feature_definition,
                from_source=from_source,
                query_time_range=query_time_range,
                entities=entities,
            )
        else:
            feature_data_time_limits = time_utils.get_feature_data_time_limits(
                fd=feature_definition,
                spine_time_limits=query_time_range,
            )
            qt = builder.build_aggregated_time_range_ghf_query(
                dialect,
                compute_mode,
                feature_definition,
                from_source=from_source,
                feature_data_time_limits=feature_data_time_limits,
                query_time_range=query_time_range,
                entities=entities,
            )

    rewrite.MockDataRewrite(mock_data_sources).rewrite(qt)

    df = TectonDataFrame._create(qt)
    return df


def _validate_sql_string_support(dialect: Dialect, spine):
    """
    Checks that the spine is a supported type for the given dialect.
    """
    if (
        isinstance(spine, str)
        and not _spine_is_uri(spine)
        and dialect
        not in (
            tecton_core.query.dialect.Dialect.SNOWFLAKE,
            tecton_core.query.dialect.Dialect.DUCKDB,
        )
    ):
        msg = "Using SQL str as `spine` is only supported with Snowflake."
        raise TypeError(msg)


def _point_in_time_get_historical_features_for_feature_definition(
    dialect: Dialect,
    compute_mode: ComputeMode,
    feature_definition: FeatureDefinitionWrapper,
    spine: TectonDataFrame,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> node_interface.NodeRef:
    if feature_definition.is_rtfv:
        utils.validate_spine_dataframe(spine, timestamp_key, feature_definition.request_context_keys)
    else:
        utils.validate_spine_dataframe(spine, timestamp_key)

    dac = FeatureDefinitionAndJoinConfig.from_feature_definition(feature_definition)
    user_data_node_metadata = {}
    user_data_node = nodes.UserSpecifiedDataNode(dialect, compute_mode, spine, user_data_node_metadata)
    mocked_fv_columns = get_mocked_feature_view_columns(list(spine._dataframe.columns))

    if timestamp_key:
        user_data_node_metadata["timestamp_key"] = timestamp_key
        user_data_node = nodes.ConvertTimestampToUTCNode(dialect, compute_mode, user_data_node.as_ref(), timestamp_key)

    qt = builder.build_spine_join_querytree(
        dialect,
        compute_mode,
        dac,
        user_data_node.as_ref(),
        timestamp_key,
        from_source,
        use_namespace_feature_prefix=dialect != tecton_core.query.dialect.Dialect.SNOWFLAKE,
        mock_context=mock_context,
        skew_config=skew_config,
        mocked_fv_columns=mocked_fv_columns,
    )

    return qt


def _most_recent_tile_end_time(fd: FeatureDefinitionWrapper, timestamp: datetime) -> int:
    """Computes the most recent tile end time which is ready to be computed.

    :param timestamp: The timestamp in python datetime format
    :return: The timestamp in seconds of the greatest ready tile end time <= timestamp.
    """
    # Account for data delay
    timestamp = timestamp - fd.max_source_data_delay
    if fd.min_scheduling_interval:
        timestamp = align_time_downwards(timestamp, fd.min_scheduling_interval)
    return convert_timestamp_to_epoch(timestamp, fd.get_feature_store_format_version)


def _get_feature_data_time_range(
    fd: FeatureDefinitionWrapper,
    start_time: Optional[Union[pendulum.DateTime, datetime]],
    end_time: Optional[Union[pendulum.DateTime, datetime]],
) -> pendulum.Period:
    if start_time is not None and isinstance(start_time, datetime):
        start_time = pendulum.instance(start_time)

    if end_time is not None and isinstance(end_time, datetime):
        end_time = pendulum.instance(end_time)

    if start_time is not None and fd.feature_start_timestamp is not None and start_time < fd.feature_start_timestamp:
        logger.warning(
            f'The provided start_time ({start_time}) is before "{fd.name}"\'s feature_start_time ({fd.feature_start_timestamp}). No feature values will be returned before the feature_start_time.'
        )
        start_time = fd.feature_start_timestamp

    # TODO(brian): construct the timestamps a bit more directly. This code in
    # general reuses utilities not really meant for the semantics of this API.
    if fd.is_temporal_aggregate or fd.is_temporal:
        # Feature views where materialization is not enabled may not have a feature_start_time.
        _start = start_time or fd.feature_start_timestamp or pendulum.datetime(1970, 1, 1)
        # we need to add 1 to most_recent_anchor since we filter end_time exclusively
        if end_time:
            _end = end_time
        else:
            anchor_time = _most_recent_tile_end_time(fd, pendulum.now("UTC") - fd.min_scheduling_interval)
            _end = convert_epoch_to_datetime(anchor_time, fd.get_feature_store_format_version) + pendulum.duration(
                microseconds=1
            )
    else:
        _start = start_time or pendulum.datetime(1970, 1, 1)
        _end = end_time or pendulum.now("UTC")

    if _start >= _end:
        # TODO(felix): Move this and other instances of validating user inputs to top-level get_historical_features() methods.
        raise core_errors.START_TIME_NOT_BEFORE_END_TIME(_start, _end)

    return pendulum.Period(_start, _end)


def get_fields_list_from_tecton_schema(tecton_schema: schema_pb2.Schema) -> List[sdk_types.Field]:
    """Convert TectonSchema into a list of Tecton Fields."""
    columns_and_types = schema.Schema(tecton_schema).column_name_and_data_types()
    request_schema = []
    for c_and_t in columns_and_types:
        name = c_and_t[0]
        data_type = type_utils.sdk_type_from_tecton_type(c_and_t[1])
        request_schema.append(sdk_types.Field(name, data_type))
    return request_schema


def _spine_is_uri(s: str) -> bool:
    return s.startswith(("s3://", "file://"))


def _create_tecton_df_spine(
    spine_schema: Schema,
    spine: Optional[Union[pyspark_sql.DataFrame, pandas.DataFrame, TectonDataFrame, str]],
    timestamp_key: Optional[str],
) -> TectonDataFrame:
    if isinstance(spine, pandas.DataFrame):
        if timestamp_key is not None:
            spine_schema += schema.Schema.from_dict({timestamp_key: data_types.TimestampType()})
        spine = TectonDataFrame._create_from_pandas_with_schema(spine, schema=spine_schema)
    elif isinstance(spine, str):
        if _spine_is_uri(spine):
            # this branch is for Remote Dataset Generation only
            # so locally we use empty dataframe
            # it's needed for QT schema inference
            spine_schema += schema.Schema.from_dict({timestamp_key: data_types.TimestampType()})
            empty_df = tecton_schema_to_arrow_schema(spine_schema).empty_table().to_pandas()
            return TectonDataFrame._create_from_pandas_with_schema(empty_df, schema=spine_schema)
        else:
            raise core_errors.SPINE_INVALID_FORMAT(spine)
    elif not isinstance(spine, TectonDataFrame):
        spine = TectonDataFrame._create(spine)

    return spine


def get_dataframe_for_data_source(
    dialect: Dialect,
    compute_mode: ComputeMode,
    data_source: specs.DataSourceSpec,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    apply_translator: bool,
) -> TectonDataFrame:
    if isinstance(
        data_source.batch_source,
        (specs.SparkBatchSourceSpec, specs.PandasBatchSourceSpec, specs.PyArrowBatchSourceSpec),
    ):
        if not data_source.batch_source.supports_time_filtering and (start_time or end_time):
            raise errors.DS_INCORRECT_SUPPORTS_TIME_FILTERING

        node = builder.build_datasource_scan_node(
            dialect=dialect,
            compute_mode=compute_mode,
            ds=data_source,
            for_stream=False,
            start_time=start_time,
            end_time=end_time,
            skew_config=None,  # skew config only used for fetching data sources within feature views
        )
        return TectonDataFrame._create(node)
    elif apply_translator:
        timestamp_key = data_source.batch_source.timestamp_field
        if not timestamp_key and (start_time or end_time):
            raise errors.DS_DATAFRAME_NO_TIMESTAMP

        node = builder.build_datasource_scan_node(
            dialect=dialect,
            compute_mode=compute_mode,
            ds=data_source,
            for_stream=False,
            start_time=start_time,
            end_time=end_time,
        )
        return TectonDataFrame._create(node)
    else:
        if start_time is not None or end_time is not None:
            raise errors.DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER

        node = nodes.RawDataSourceScanNode(dialect, compute_mode, data_source).as_ref()
        return TectonDataFrame._create(node)


def run_transformation_batch(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: FeatureDefinitionWrapper,
    feature_start_time: datetime,
    feature_end_time: datetime,
    mock_data_sources: Dict[str, NodeRef],
    mock_context: Optional[MockContext] = None,
) -> TectonDataFrame:
    if not fd.is_rtfv:
        check_spark_version(fd.fv_spec.batch_cluster_config)

    feature_time_limits_aligned = pendulum.period(feature_start_time, feature_end_time)

    if fd.is_temporal:
        qt = build_materialization_querytree(
            dialect,
            compute_mode,
            fd,
            for_stream=False,
            feature_data_time_limits=feature_time_limits_aligned,
            use_timestamp_key=True,
            mock_context=mock_context,
        )
    elif fd.is_temporal_aggregate:
        qt = build_pipeline_querytree(
            dialect,
            compute_mode,
            fd,
            for_stream=False,
            feature_data_time_limits=feature_time_limits_aligned,
            mock_context=mock_context,
        )
    else:
        msg = "Unsupported FV Type"
        raise Exception(msg)

    MockDataRewrite(mock_data_sources).rewrite(qt)

    return TectonDataFrame._create(qt)


def scan_dataset(
    dataset: SavedFeatureDataFrame,
    compute_mode: ComputeMode,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
) -> TectonDataFrame:
    time_filter = pendulum.Period(start_time, end_time) if start_time and end_time else None
    qt = DatasetScanNode(
        dialect=Dialect.ARROW,  # Spark will ignore this, so this is only for Rift
        compute_mode=compute_mode,
        dataset=dataset,
        time_filter=time_filter,
    ).as_ref()
    qt = StagingNode(
        dialect=Dialect.ARROW,
        compute_mode=compute_mode,
        input_node=qt,
        staging_table_name=f"{dataset.info.name}",
        query_tree_step=QueryTreeStep.AGGREGATION,
    ).as_ref()
    return TectonDataFrame._create(qt)
