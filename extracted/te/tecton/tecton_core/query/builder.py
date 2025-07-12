import logging
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import attrs

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import data_types
from tecton_core import errors
from tecton_core import feature_definition_wrapper
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.embeddings.config import CustomModelConfig
from tecton_core.embeddings.config import TextEmbeddingInferenceConfig
from tecton_core.embeddings.config import TextEmbeddingModel
from tecton_core.embeddings.model_artifact_info import ModelArtifactInfo
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.feature_set_config import find_dependent_feature_set_items
from tecton_core.mock_context import MockContext
from tecton_core.pipeline.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query import compaction_utils
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeColumnsForSawtoothIntervalsNode
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddBooleanPartitionColumnsNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AddRetrievalAnchorTimeNode
from tecton_core.query.nodes import AddUniqueIdNode
from tecton_core.query.nodes import AdjustAnchorTimeToWindowEndNode
from tecton_core.query.nodes import AggregationSecondaryKeyExplodeNode
from tecton_core.query.nodes import AggregationSecondaryKeyRollupNode
from tecton_core.query.nodes import AsofBitemporalJoinFullAggNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinInputContainer
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import AsofJoinReducePartialAggNode
from tecton_core.query.nodes import AsofJoinSawtoothAggNode
from tecton_core.query.nodes import AsofSecondaryKeyExplodeNode
from tecton_core.query.nodes import ConvertEpochToTimestampNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import DeriveValidityPeriodNode
from tecton_core.query.nodes import ExplodeEventsByTimestampAndSelectDistinctNode
from tecton_core.query.nodes import ExplodeTimestampByTimeWindowsNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import InnerJoinOnRangeNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import MultiRtfvFeatureExtractionNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import OnlineListAggNode
from tecton_core.query.nodes import OnlinePartialAggNodeV2
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import PythonDataNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import TakeLastRowNode
from tecton_core.query.nodes import TemporalBatchTableFormatNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import TrimValidityPeriodNode
from tecton_core.query.nodes import UnionNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.nodes import WildcardJoinNode
from tecton_core.query_consts import MOCK_COLUMN_SEPARATOR
from tecton_core.query_consts import aggregation_group_id
from tecton_core.query_consts import aggregation_tile_id
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import anchor_time_for_non_sawtooth
from tecton_core.query_consts import effective_timestamp
from tecton_core.query_consts import exclusive_end_time
from tecton_core.query_consts import expiration_timestamp
from tecton_core.query_consts import inclusive_start_time
from tecton_core.query_consts import interval_end_time
from tecton_core.query_consts import interval_start_time
from tecton_core.query_consts import is_non_sawtooth
from tecton_core.query_consts import odfv_internal_staging_table
from tecton_core.query_consts import tecton_spine_row_id_col
from tecton_core.query_consts import tecton_unique_id_col
from tecton_core.query_consts import timestamp_plus_ttl
from tecton_core.query_consts import udf_internal
from tecton_core.query_consts import window_end_column_name
from tecton_core.schema import Schema
from tecton_core.skew_config import SkewConfig
from tecton_core.specs import DataSourceSpec
from tecton_proto.args.pipeline__client_pb2 import DataSourceNode as ProtoDataSourceNode
from tecton_proto.common import aggregation_function__client_pb2 as aggregation_function_pb2
from tecton_proto.data import feature_view__client_pb2 as feature_view__data_pb2


logger = logging.getLogger(__name__)


def _is_wildcard_join(fdw: feature_definition_wrapper.FeatureDefinitionWrapper, spine_node: NodeRef) -> bool:
    """Check whether this retrieval query needs to handle this FV with the "wildcard" join pattern.

    A feature view uses a wildcard join when:
      1. the FV has a wildcard join key
      2. that join key is not in the spine.

    NOTE: If the join key is in the spine, then we treat it like a standard FV (i.e. we include that spine column in the join).

    Wildcards are deprecated and only used by one customer. However, we need this code around until this functionality
    is removed from the product.
    """
    return fdw.wildcard_join_key is not None and fdw.wildcard_join_key not in spine_node.columns


def build_datasource_scan_node(
    dialect: Dialect,
    compute_mode: ComputeMode,
    ds: specs.DataSourceSpec,
    for_stream: bool,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    tree = DataSourceScanNode(
        dialect=dialect,
        compute_mode=compute_mode,
        ds=ds,
        ds_node=None,
        is_stream=for_stream,
        start_time=start_time,
        end_time=end_time,
        skew_config=skew_config,
    ).as_ref()
    return StagingNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=tree,
        staging_table_name=f"{ds.name}",
        query_tree_step=QueryTreeStep.DATA_SOURCE,
    ).as_ref()


def _get_ds_time_limits(
    feature_data_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: ProtoDataSourceNode,
    skew_config: Optional[SkewConfig],
) -> Tuple[Optional[datetime], Optional[datetime]]:
    ds_time_limits = get_time_window_from_data_source_node(
        feature_data_time_limits, schedule_interval, data_source_node, skew_config
    )
    if ds_time_limits:
        return ds_time_limits.start, ds_time_limits.end
    return None, None


def _build_datasource_input_querynodes(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    skew_config: Optional[SkewConfig] = None,
) -> Dict[str, NodeRef]:
    """
    Starting in FWV5, data sources of FVs with incremental backfills may contain transformations that are only
    correct if the data has been filtered to a specific range.
    """
    schedule_interval = fdw.get_tile_interval if fdw.is_temporal else None
    ds_inputs = feature_definition_wrapper.pipeline_to_ds_inputs(fdw.pipeline)

    input_querynodes = {}
    for input_name, node in ds_inputs.items():
        start_time, end_time = _get_ds_time_limits(feature_data_time_limits, schedule_interval, node, skew_config)
        ds = fdw.fco_container.get_by_id_proto(node.virtual_data_source_id)
        assert isinstance(ds, DataSourceSpec)
        tree = DataSourceScanNode(
            dialect=dialect,
            compute_mode=compute_mode,
            ds=ds,
            ds_node=node,
            is_stream=for_stream,
            start_time=start_time,
            end_time=end_time,
            skew_config=skew_config,
        ).as_ref()
        input_querynodes[input_name] = StagingNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            staging_table_name=f"{ds.name}",
            query_tree_step=QueryTreeStep.DATA_SOURCE,
        ).as_ref()
    return input_querynodes


def _get_stream_watermark(fdw: feature_definition_wrapper.FeatureDefinitionWrapper) -> Optional[str]:
    ds_inputs = feature_definition_wrapper.pipeline_to_ds_inputs(fdw.pipeline)
    for input_name, node in ds_inputs.items():
        ds_spec = fdw.fco_container.get_by_id_proto(node.virtual_data_source_id)
        assert isinstance(ds_spec, DataSourceSpec)
        if ds_spec.stream_source is not None:
            watermark_delay_threshold_seconds = ds_spec.stream_source.watermark_delay_threshold.total_seconds()
            # NOTE: we do not want to set an explicit '0 seconds' watermark as
            # that can lead to data loss (data source functions supports
            # user-specified watermark configuration in function).
            if watermark_delay_threshold_seconds:
                return f"{watermark_delay_threshold_seconds} seconds"
    return None


# build QueryTree that executes all transformations
def build_pipeline_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    inputs_map = _build_datasource_input_querynodes(
        dialect, compute_mode, fdw, for_stream, feature_data_time_limits, skew_config
    )
    tree = FeatureViewPipelineNode(
        dialect=dialect,
        compute_mode=compute_mode,
        inputs_map=inputs_map,
        feature_definition_wrapper=fdw,
        feature_time_limits=feature_data_time_limits,
        # FWV6 enforces explicit view schema using Features parameter.
        check_view_schema=fdw.framework_version == FrameworkVersion.FWV6,
        mock_context=mock_context,
    ).as_ref()
    tree = ConvertTimestampToUTCNode.for_feature_definition(
        dialect=dialect,
        compute_mode=compute_mode,
        fd=fdw,
        input_node=tree,
    )

    timestamp_field = (
        fdw.materialization_job_partition_timestamp
        if _should_account_for_batch_publish_timestamp(fdw=fdw, skew_config=skew_config)
        else fdw.timestamp_key
    )
    if feature_data_time_limits:
        tree = FeatureTimeFilterNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            feature_data_time_limits=feature_data_time_limits,
            policy=fdw.time_range_policy,
            start_timestamp_field=timestamp_field,
            end_timestamp_field=timestamp_field,
        ).as_ref()

    tree = StagingNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=tree,
        staging_table_name=f"{fdw.name}",
        query_tree_step=QueryTreeStep.PIPELINE,
    ).as_ref()
    return tree


def _build_core_materialization_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    enable_feature_metrics: bool = False,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    """Builds a querytree to construct a dataframe for materialization. This contains the common QT used for online and offline materialization.

    Args:
        dialect: The SQL dialect
        compute_mode: Current compute mode
        fdw: The feature view to be materialized.
        for_stream: If True, the underlying data source is a streaming source.
        feature_data_time_limits: If set, the resulting features will be filtered with respect to these time limits.
        enable_feature_metrics: If True, metrics will be collected on the querytree.
    """
    assert not for_stream or feature_data_time_limits is None, "Cannot run with time limits on a stream source"
    tree = build_pipeline_querytree(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        for_stream=for_stream,
        feature_data_time_limits=feature_data_time_limits,
        mock_context=mock_context,
        skew_config=skew_config,
    )
    if for_stream:
        watermark = _get_stream_watermark(fdw)
        if watermark:
            tree = StreamWatermarkNode(dialect, compute_mode, tree, fdw.time_key, watermark).as_ref()
    if enable_feature_metrics:
        tree = MetricsCollectorNode(dialect, compute_mode, tree).as_ref()

    if fdw.is_temporal:
        if len(fdw.fv_spec.embedding_features) or len(fdw.fv_spec.inference_features):
            tree = _add_text_embedding_inference_node(fdw=fdw, compute_mode=compute_mode, pipeline_tree=tree)
    return tree


def build_materialization_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    include_window_end_time: bool = False,
    aggregation_anchor_time: Optional[datetime] = None,
    enable_feature_metrics: bool = False,
    use_timestamp_key: bool = False,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    """Builds a querytree to construct a dataframe for batch materialization or stream materialization. This is not used by compaction jobs.

    If the Feature View uses an untiled offline store and offline=True, the resulting querytree will be the output of the pipeline querytree.
    If the Feature View uses a tiled offline store and/or online=True, we will compute the partial agg tiles.
    The resulting dataframe can also be easily modified to be used for `fv.run`.

    Args:
        dialect: The SQL dialect
        compute_mode: Current compute mode
        fdw: The feature view to be materialized.
        for_stream: If True, the underlying data source is a streaming source..
        feature_data_time_limits: If set, the resulting features will be filtered with respect to these time limits.
        include_window_end_time: If True, a tile end time column with name "tile_end_time" will be included for WAFVs.
            Should only be set for WAFVs.
        aggregation_anchor_time: If set, it will be used as the offset for aggregations. Should only be set for WAFVs.
        enable_feature_metrics: If True, metrics will be collected on the querytree.
        use_timestamp_key: If True, the timestamp key will be used instead of _ANCHOR_TIME. This is used for Snowflake Compute only.
    """
    tree = _build_core_materialization_querytree(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        for_stream=for_stream,
        feature_data_time_limits=feature_data_time_limits,
        enable_feature_metrics=enable_feature_metrics,
        mock_context=mock_context,
        skew_config=skew_config,
    )

    if not for_stream and fdw.has_untiled_offline_store:
        # As of right now, fvs with untiled offline store never run batch online materialization (they use compaction) so we can assume this function is always used for offline materialization.
        tree = ConvertTimestampToUTCNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, fd=fdw, input_node=tree
        )
        # TODO(samantha): Remove anchor time from untiled offline store schema
        return AddAnchorTimeNode.for_feature_definition(dialect, compute_mode, fdw, tree)

    # Below should only contain nodes required for online materialization and/or tiled offline store. Common nodes should be in _build_core_materialization_querytree.
    if fdw.is_temporal:
        assert not include_window_end_time, "Not supported window end time for temporal"
        if not for_stream and not use_timestamp_key:
            tree = AddAnchorTimeNode.for_feature_definition(dialect, compute_mode, fdw, tree)
    elif fdw.is_temporal_aggregate:
        anchor_time_field = anchor_time()
        end_column_name = window_end_column_name() if include_window_end_time else None
        tree = PartialAggNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            fdw=fdw,
            aggregation_tile_interval=fdw.get_tile_interval,
            window_start_column_name=anchor_time_field,
            window_end_column_name=end_column_name,
            aggregation_anchor_time=aggregation_anchor_time,
        ).as_ref()
        if use_timestamp_key:
            tree = ConvertEpochToTimestampNode(
                dialect, compute_mode, tree, {anchor_time(): fdw.get_feature_store_format_version}
            ).as_ref()
            tree = RenameColsNode(
                dialect, compute_mode, input_node=tree, mapping={anchor_time(): fdw.time_key}
            ).as_ref()
    else:
        msg = "unexpected FV type"
        raise Exception(msg)
    return tree


def _add_text_embedding_inference_node(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, compute_mode: ComputeMode, pipeline_tree: NodeRef
) -> NodeRef:
    if compute_mode != ComputeMode.RIFT:
        msg = "text embeddings are only supported on Rift"
        raise ValueError(msg)

    inference_configs = []
    if len(fdw.fv_spec.embedding_features):
        inference_configs += [
            TextEmbeddingInferenceConfig(
                input_column=e.input_column_name, output_column=e.output_column_name, model=TextEmbeddingModel(e.model)
            )
            for e in fdw.fv_spec.embedding_features
        ]

    if len(fdw.fv_spec.inference_features):
        inference_configs += [
            CustomModelConfig(
                input_columns=inference.input_columns,
                output_column=inference.output_column,
                model_artifact=ModelArtifactInfo(inference.model_artifact),
            )
            for inference in fdw.fv_spec.inference_features
        ]

    qt_node = TextEmbeddingInferenceNode(
        dialect=Dialect.ARROW,
        compute_mode=ComputeMode.RIFT,
        input_node=pipeline_tree,
        inference_configs=tuple(inference_configs),
    )

    staging_node = StagingNode(
        dialect=Dialect.ARROW,
        compute_mode=ComputeMode.RIFT,
        input_node=qt_node.as_ref(),
        staging_table_name="model_inference",
        query_tree_step=QueryTreeStep.MODEL_INFERENCE,
    )

    # NOTE: we want to drop all columns that are not in the materialization_schema (i.e. indicates that we don't have the attribute set)
    m13n_col_names = set(fdw.materialization_schema.column_names())
    cols_to_drop = [col_name for col_name in fdw.view_schema.column_names() if col_name not in m13n_col_names]

    tree = RenameColsNode(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        input_node=staging_node.as_ref(),
        drop=cols_to_drop,
    )

    return tree.as_ref()


def build_get_partial_aggregates_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    limits: pendulum.Period,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    qt = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        from_source=from_source,
        feature_data_time_limits=limits,
        include_window_end_time=True,
    )

    rename_mapping = {
        anchor_time(): interval_start_time(),
        window_end_column_name(): interval_end_time(),
    }

    qt = RenameColsNode(dialect, compute_mode, qt, mapping=rename_mapping).as_ref()

    qt = ConvertEpochToTimestampNode(
        dialect,
        compute_mode,
        qt,
        {
            interval_start_time(): fdw.get_feature_store_format_version,
            interval_end_time(): fdw.get_feature_store_format_version,
        },
    ).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    return qt


def _build_get_features(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: Optional[pendulum.Period] = None,
    aggregation_anchor_time: Optional[datetime] = None,
    include_window_end_time: Optional[bool] = False,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    # NOTE: this is ideally the *only* place where we validate
    # from_source arguments. However, until Snowflake and Athena are migrated
    # to QueryTree, we also need validations to live in the interactive/unified
    # SDK.
    #
    # Behavior:
    #   from_source is True: force compute from source
    #   from_source is False: force compute from materialized data
    #   from_source is None: compute from materialized data if feature
    #       definition offline=True, otherwise compute from source
    if from_source is None:
        from_source = not fdw.materialization_enabled or not fdw.writes_to_offline_store

    if from_source is False:
        assert not aggregation_anchor_time, "aggregation anchor time is not allowed when fetching features from source"
        if not fdw.materialization_enabled or not fdw.writes_to_offline_store:
            raise errors.FV_NEEDS_TO_BE_MATERIALIZED(fdw.name)
        tree = OfflineStoreScanNode(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition_wrapper=fdw,
            partition_time_filter=feature_data_time_limits,
            skew_config=skew_config,
        ).as_ref()
        if (
            feature_data_time_limits is not None
            and skew_config is not None
            and skew_config.simulate_offline_store_materialized_until is not None
        ):
            tree = FeatureTimeFilterNode(
                dialect=dialect,
                compute_mode=compute_mode,
                input_node=tree,
                feature_data_time_limits=pendulum.Period(
                    start=feature_data_time_limits.start,
                    end=pendulum.instance(skew_config.simulate_offline_store_materialized_until),
                ),
                policy=fdw.time_range_policy,
                start_timestamp_field=fdw.materialization_job_partition_timestamp,
                end_timestamp_field=fdw.materialization_job_partition_timestamp,
            ).as_ref()
        tree = StagingNode(
            dialect=Dialect.ARROW,
            compute_mode=compute_mode,
            input_node=tree,
            staging_table_name=f"offline_store_{fdw.name}",
            query_tree_step=QueryTreeStep.OFFLINE_STORE,
        ).as_ref()
    else:
        if dialect == "athena":
            msg = "When Athena compute is enabled, features can only be read from the offline store. Please set from_source = False"
            raise errors.TectonAthenaValidationError(msg)
        # TODO(TEC-13005)
        # TODO(pooja): raise an appropriate error here for push source
        if fdw.is_incremental_backfill:
            raise errors.FV_BFC_SINGLE_FROM_SOURCE

        tree = build_materialization_querytree(
            dialect,
            compute_mode,
            fdw,
            for_stream=False,
            feature_data_time_limits=feature_data_time_limits,
            aggregation_anchor_time=aggregation_anchor_time,
            include_window_end_time=include_window_end_time,
            mock_context=mock_context,
            skew_config=skew_config,
        )
    return tree


def build_get_features(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: Optional[pendulum.Period] = None,
    aggregation_anchor_time: Optional[datetime] = None,
    include_window_end_time: Optional[bool] = False,
    aggregation_tile_interval_override: Optional[pendulum.Duration] = None,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    """Builds a query tree to get features from the offline store or source and computes partial aggs."""
    tree = _build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        from_source=from_source,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_anchor_time=aggregation_anchor_time,
        include_window_end_time=include_window_end_time,
        mock_context=mock_context,
        skew_config=skew_config,
    )

    if fdw.compaction_enabled and fdw.is_temporal_aggregate:
        tree = AddEffectiveTimestampNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            timestamp_field=fdw.materialization_job_partition_timestamp,
            effective_timestamp_name=effective_timestamp(),
            batch_schedule_seconds=fdw.batch_materialization_schedule.in_seconds(),
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            is_stream=fdw.is_stream,
        ).as_ref()

        end_column_name = window_end_column_name() if include_window_end_time else None
        if aggregation_tile_interval_override is not None:
            aggregation_tile_interval = aggregation_tile_interval_override
        else:
            aggregation_tile_interval = fdw.get_tile_interval_duration_for_offline_store
        tree = PartialAggNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            fdw=fdw,
            window_start_column_name=anchor_time(),
            aggregation_tile_interval=aggregation_tile_interval,
            window_end_column_name=end_column_name,
            aggregation_anchor_time=aggregation_anchor_time,
        ).as_ref()

    return tree


def build_temporal_time_range_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    query_time_range: pendulum.Period,
    entities: Optional[DataframeWrapper],
    mock_context: Optional[MockContext] = None,
) -> NodeRef:
    qt = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fd,
        from_source=from_source,
        feature_data_time_limits=query_time_range,
        mock_context=mock_context,
    )
    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()
    batch_schedule_seconds = 0 if fd.is_feature_table else fd.batch_materialization_schedule.in_seconds()

    qt = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=fd.timestamp_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=fd.online_store_data_delay_seconds,
        is_stream=fd.is_stream,
    ).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    qt = _filter_by_time_range(dialect, compute_mode, qt, query_time_range, fd.timestamp_key, fd.timestamp_key)
    return qt


def build_temporal_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    lookback_time_range: pendulum.Period,
    entities: Optional[DataframeWrapper],
    query_time_range: pendulum.Period,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    qt = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fd,
        from_source=from_source,
        feature_data_time_limits=lookback_time_range,
        mock_context=mock_context,
        skew_config=skew_config,
    )
    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()
    batch_schedule_seconds = 0 if fd.is_feature_table else fd.batch_materialization_schedule.in_seconds()

    qt = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=fd.materialization_job_partition_timestamp
        if _should_account_for_batch_publish_timestamp(fd, skew_config)
        else fd.timestamp_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=fd.online_store_data_delay_seconds,
        is_stream=fd.is_stream,
    ).as_ref()

    qt = TakeLastRowNode(
        dialect,
        compute_mode,
        input_node=qt,
        partition_by_columns=(*fd.join_keys, effective_timestamp()),
        order_by_column=fd.timestamp_key,
    ).as_ref()

    qt = DeriveValidityPeriodNode(dialect, compute_mode, qt, fd, effective_timestamp()).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    qt = TrimValidityPeriodNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=qt,
        start=query_time_range.start,
        end=query_time_range.end,
    ).as_ref()

    return qt


def build_aggregated_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    # query_time_range is the validated time range passed in the query
    query_time_range: pendulum.Period,
    # feature_data_time_limits is the aligned time range after taking the spine and aggregations into account
    feature_data_time_limits: pendulum.Period,
    entities: Optional[DataframeWrapper],
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
        mock_context=mock_context,
        skew_config=skew_config,
    )
    if entities is not None:
        partial_aggs = _filter_entity_dataframe(dialect, compute_mode, partial_aggs, entities)

    if _should_use_sawtooth_aggregation_impl(fdw):
        full_aggregation_node = _build_sawtooth_full_aggs_for_time_range_validity_query(
            dialect=dialect,
            compute_mode=compute_mode,
            fdw=fdw,
            from_source=from_source,
            query_time_range=query_time_range,
            feature_data_time_limits=feature_data_time_limits,
            partial_aggs=partial_aggs,
        )
    elif _should_account_for_batch_publish_timestamp(fdw, skew_config):
        full_aggregation_node = _build_full_aggs_for_late_arriving_data_time_range_validity_query(
            dialect=dialect,
            compute_mode=compute_mode,
            fdw=fdw,
            query_time_range=query_time_range,
            partial_aggs=partial_aggs,
        )
    else:
        full_aggregation_node = _build_full_aggs_for_time_range_validity_query(
            dialect=dialect,
            compute_mode=compute_mode,
            fdw=fdw,
            query_time_range=query_time_range,
            partial_aggs=partial_aggs,
        )

    if fdw.aggregation_secondary_key:
        full_aggregation_node = AggregationSecondaryKeyRollupNode(
            dialect=dialect,
            compute_mode=compute_mode,
            full_aggregation_node=full_aggregation_node,
            fdw=fdw,
            group_by_columns=[*list(fdw.join_keys), anchor_time()],
        ).as_ref()

    # The `AsofJoinFullAggNode` returned by `build_get_full_agg_features` converts timestamps to epochs. We convert back
    # from epochs to timestamps so that we can add an effective timestamp column.
    qt = ConvertEpochToTimestampNode(
        dialect, compute_mode, full_aggregation_node, {anchor_time(): fdw.get_feature_store_format_version}
    ).as_ref()

    batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
    qt = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=anchor_time(),
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=fdw.online_store_data_delay_seconds,
        is_stream=fdw.is_stream,
    ).as_ref()

    qt = TakeLastRowNode(
        dialect,
        compute_mode,
        input_node=qt,
        partition_by_columns=(*fdw.join_keys, effective_timestamp()),
        order_by_column=anchor_time(),
    ).as_ref()

    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()

    qt = DeriveValidityPeriodNode(dialect, compute_mode, qt, fdw, effective_timestamp()).as_ref()

    qt = TrimValidityPeriodNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=qt,
        start=query_time_range.start,
        end=query_time_range.end,
    ).as_ref()

    return qt


def _build_full_aggs_for_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    # query_time_range is the validated time range passed in the query
    query_time_range: pendulum.Period,
    partial_aggs: NodeRef,
) -> NodeRef:
    spine = _build_internal_spine(
        dialect,
        compute_mode,
        fdw,
        partial_aggs,
        query_time_range=query_time_range,
        explode_anchor_time=True,
    )
    full_aggregation_node = AsofJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()
    return full_aggregation_node


def _build_full_aggs_for_late_arriving_data_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    # query_time_range is the validated time range passed in the query
    query_time_range: pendulum.Period,
    partial_aggs: NodeRef,
) -> NodeRef:
    spine = _build_internal_spine_for_late_arriving_data(
        dialect,
        compute_mode,
        fdw,
        partial_aggs,
        query_time_range=query_time_range,
    )
    full_aggregation_node = AsofBitemporalJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()
    return full_aggregation_node


def _build_sawtooth_full_aggs_for_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    # query_time_range is the validated time range passed in the query
    query_time_range: pendulum.Period,
    # feature_data_time_limits is the aligned time range after taking the spine and aggregations into account
    feature_data_time_limits: pendulum.Period,
    partial_aggs: NodeRef,
) -> NodeRef:
    sawtooth_agg_data = compaction_utils.SawtoothAggregationData.from_aggregate_features(fdw)
    spine = _build_internal_spine(
        dialect,
        compute_mode,
        fdw,
        partial_aggs,
        query_time_range=query_time_range,
        explode_anchor_time=True,
        sawtooth_aggregation_data=sawtooth_agg_data,
    )
    full_aggregation_node = _build_sawtooth_aggregation_subtree(
        dialect=dialect,
        compute_mode=compute_mode,
        spine_node=spine,
        from_source=from_source,
        feature_data_time_limits=feature_data_time_limits,
        fdw=fdw,
        sawtooth_aggregation_data=sawtooth_agg_data,
        spine_timestamp_field=anchor_time(),
        enable_rewrite=False,
    )
    return full_aggregation_node


# TODO(PRODENG-262): Remove build_aggregated_time_range_ghf_query once get_historical_features has been deprecated
def build_aggregated_time_range_ghf_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: pendulum.Period,
    query_time_range: pendulum.Period,
    entities: Optional[DataframeWrapper] = None,
) -> NodeRef:
    partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
    )
    spine = _build_internal_spine(dialect, compute_mode, fdw, partial_aggs)

    # TODO(danny): Don't represent the partial_agg node twice (in the spine + in the agg node)
    #  When this QT is compiled to SQL, the partial agg node is doubly represented and executed.
    full_aggregation_node = AsofJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()

    if fdw.aggregation_secondary_key:
        full_aggregation_node = AggregationSecondaryKeyRollupNode(
            dialect=dialect,
            compute_mode=compute_mode,
            full_aggregation_node=full_aggregation_node,
            fdw=fdw,
            group_by_columns=[*list(fdw.join_keys), anchor_time()],
        ).as_ref()

    if fdw.feature_start_timestamp:
        full_aggregation_node = RespectFeatureStartTimeNode.for_anchor_time_column(
            dialect,
            compute_mode,
            full_aggregation_node,
            anchor_time(),
            fdw,
        ).as_ref()

    qt = ConvertEpochToTimestampNode(
        dialect, compute_mode, full_aggregation_node, {anchor_time(): fdw.get_feature_store_format_version}
    ).as_ref()

    # We want the time to be on the end of the window not the start.
    qt = AddDurationNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=anchor_time(),
        duration=fdw.get_tile_interval_duration_for_offline_store,
        new_column_name=fdw.trailing_time_window_aggregation().time_key,
    ).as_ref()

    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()

    batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
    qt = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=fdw.trailing_time_window_aggregation().time_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=fdw.online_store_data_delay_seconds,
        is_stream=fdw.is_stream,
        use_legacy_temporal_aggregate_behavior=True,
    ).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    qt = _filter_by_time_range(dialect, compute_mode, qt, query_time_range, fdw.timestamp_key, fdw.timestamp_key)

    return qt


# TODO(PRODENG-262): Remove build_aggregated_time_range_run_query once .run is removed
def build_aggregated_time_range_run_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    feature_data_time_limits: pendulum.Period,
    aggregation_anchor_time: Optional[datetime] = None,
) -> NodeRef:
    partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source=True,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_anchor_time=aggregation_anchor_time,
    )
    spine = _build_internal_spine(dialect, compute_mode, fdw, partial_aggs)

    # TODO(danny): Don't represent the partial_agg node twice (in the spine + in the agg node)
    #  When this QT is compiled to SQL, the partial agg node is doubly represented and executed.
    full_aggregation_node = AsofJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()

    if fdw.aggregation_secondary_key:
        full_aggregation_node = AggregationSecondaryKeyRollupNode(
            dialect=dialect,
            compute_mode=compute_mode,
            full_aggregation_node=full_aggregation_node,
            fdw=fdw,
            group_by_columns=[*list(fdw.join_keys), anchor_time()],
        ).as_ref()

    # The `AsofJoinFullAggNode` returned by `build_get_full_agg_features` converts timestamps to epochs. We convert back
    # from epochs to timestamps so that we can add an effective timestamp column.
    qt = ConvertEpochToTimestampNode(
        dialect, compute_mode, full_aggregation_node, {anchor_time(): fdw.get_feature_store_format_version}
    ).as_ref()

    # We want the time to be on the end of the window not the start.
    qt = AddDurationNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=anchor_time(),
        duration=fdw.get_tile_interval_duration_for_offline_store,
        new_column_name=fdw.trailing_time_window_aggregation().time_key,
    ).as_ref()
    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()

    return qt


def _filter_by_time_range(
    dialect: Dialect,
    compute_mode: ComputeMode,
    qt: NodeRef,
    time_range: pendulum.Period,
    start_timestamp_field: str,
    end_timestamp_field: str,
) -> NodeRef:
    qt = FeatureTimeFilterNode(
        dialect,
        compute_mode,
        qt,
        feature_data_time_limits=time_range,
        policy=feature_view__data_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
        start_timestamp_field=start_timestamp_field,
        end_timestamp_field=end_timestamp_field,
    ).as_ref()

    return qt


def _filter_entity_dataframe(
    dialect: Dialect,
    compute_mode: ComputeMode,
    qt: NodeRef,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    columns = list(entities.columns)
    entities_df = SelectDistinctNode(
        dialect, compute_mode, UserSpecifiedDataNode(dialect, compute_mode, entities).as_ref(), columns
    ).as_ref()
    qt = JoinNode(dialect, compute_mode, qt, entities_df, columns, how="right").as_ref()
    return qt


def _build_internal_spine(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    partial_aggs: NodeRef,
    explode_anchor_time: Optional[bool] = False,
    query_time_range: Optional[pendulum.Period] = None,
    sawtooth_aggregation_data: Optional[compaction_utils.SawtoothAggregationData] = None,
) -> NodeRef:
    if fdw.aggregation_secondary_key:
        cols_to_drop = list(
            set(partial_aggs.columns) - {*list(fdw.join_keys), anchor_time(), fdw.aggregation_secondary_key}
        )
    else:
        cols_to_drop = list(set(partial_aggs.columns) - {*list(fdw.join_keys), anchor_time()})

    spine = RenameColsNode(dialect, compute_mode, partial_aggs, drop=cols_to_drop).as_ref()

    # TODO (ajeya): remove flag after GHF is deprecated
    if explode_anchor_time:
        if sawtooth_aggregation_data:
            spine = AddAnchorTimeColumnsForSawtoothIntervalsNode(
                dialect=dialect,
                compute_mode=compute_mode,
                input_node=spine,
                timestamp_field=anchor_time(),
                anchor_time_column_map=sawtooth_aggregation_data.get_anchor_time_to_timedelta_map(),
                data_delay_seconds=fdw.online_store_data_delay_seconds,
                feature_store_format_version=fdw.get_feature_store_format_version,
                aggregation_tile_interval_column_map=sawtooth_aggregation_data.get_anchor_time_to_aggregation_interval_map(
                    fdw.get_tile_interval_for_sawtooths, fdw.get_feature_store_format_version
                ),
            ).as_ref()

        earliest_valid_anchor_time = time_utils.get_nearest_anchor_time(
            timestamp=query_time_range.start,
            max_source_data_delay=fdw.max_source_data_delay,
            batch_materialization_schedule=fdw.batch_materialization_schedule,
            min_scheduling_interval=fdw.min_scheduling_interval,
        )
        spine_filter = pendulum.Period(earliest_valid_anchor_time, query_time_range.end)
        spine = ExplodeTimestampByTimeWindowsNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=spine,
            timestamp_field=anchor_time(),
            time_filter=spine_filter,
            fdw=fdw,
            sawtooth_aggregation_data=sawtooth_aggregation_data,
            include_original_anchor_time=True,
        ).as_ref()

        if sawtooth_aggregation_data:
            spine = RenameColsNode(
                dialect, compute_mode, spine, drop=sawtooth_aggregation_data.get_anchor_time_columns()
            ).as_ref()

    if fdw.aggregation_secondary_key:
        spine = AggregationSecondaryKeyExplodeNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, spine=spine, fdw=fdw
        )

    return spine


def _build_internal_spine_for_late_arriving_data(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    partial_aggs: NodeRef,
    query_time_range: Optional[pendulum.Period] = None,
) -> NodeRef:
    """
    The goal of building the spine is to include every single time that a feature can change values. This includes:
    - when events can leave an aggregation window - derived from anchor_time + all aggregation time deltas (but not the anchor time itself)
    - when events can enter an aggregation window - derived from effective_timestamp (based on batch_publish_timestamp)

    This function:
    1. gets all anchor_time + aggregation time deltas (but not the anchor time itself) from the partial_agg node and backs out equivalent effective_timestamp - these are all the times when an event can leave an aggregation window
    2. gets all the effective_timestamps from the partial_agg node and backs out equivalent anchor time - these are all the times when an event can enter an aggregation window
    3. unions the two sets together, de-duplicates, and renames the effective_timestamp column to the feature definition's timestamp key
    """
    cols_to_keep = {*list(fdw.join_keys), anchor_time()}
    if fdw.aggregation_secondary_key:
        cols_to_keep.add(fdw.aggregation_secondary_key)

    cols_to_drop = list(set(partial_aggs.columns) - cols_to_keep)

    spine = RenameColsNode(dialect, compute_mode, partial_aggs, drop=cols_to_drop).as_ref()

    earliest_valid_anchor_time = time_utils.get_nearest_anchor_time(
        timestamp=query_time_range.start,
        max_source_data_delay=fdw.max_source_data_delay,
        batch_materialization_schedule=fdw.batch_materialization_schedule,
        min_scheduling_interval=fdw.min_scheduling_interval,
    )
    spine_filter = pendulum.Period(earliest_valid_anchor_time, query_time_range.end)

    intermediate_timestamp_field = "_INTERMEDIATE_TIMESTAMP_FIELD"
    # 1. gets all anchor_time + aggregation time deltas (but not the anchor time itself) from the partial_agg node and backs out equivalent effective_timestamp - these are all the times when an event can leave an aggregation window
    # the logic here is:
    # - get all the anchor times where events leave time window (excluding original anchor time)
    # - copy those times to _INTERMEDIATE_TIMESTAMP_FIELD
    # - compute _effective_timestamp() equivalent of those anchor times by converting _INTERMEDIATE_TIMESTAMP_FIELD from epoch -> timestamp, then add effective timestamp
    # - drop _INTERMEDIATE_TIMESTAMP_FIELD
    anchor_time_spine = ExplodeTimestampByTimeWindowsNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=spine,
        timestamp_field=anchor_time(),
        time_filter=spine_filter,
        fdw=fdw,
        sawtooth_aggregation_data=None,
        include_original_anchor_time=False,
    ).as_ref()
    anchor_time_spine = RenameColsNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=anchor_time_spine,
        mapping={
            anchor_time(): intermediate_timestamp_field,
        },
        keep_original_columns_from_mapping=True,
    ).as_ref()
    anchor_time_spine = ConvertEpochToTimestampNode(
        dialect,
        compute_mode,
        anchor_time_spine,
        {intermediate_timestamp_field: fdw.get_feature_store_format_version},
    ).as_ref()
    anchor_time_spine = AddEffectiveTimestampNode(
        dialect=dialect,
        compute_mode=compute_mode,
        timestamp_field=intermediate_timestamp_field,
        input_node=anchor_time_spine,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=fdw.batch_materialization_schedule.in_seconds(),
        is_stream=fdw.is_stream,
        data_delay_seconds=fdw.online_store_data_delay_seconds,
    ).as_ref()
    anchor_time_spine = RenameColsNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=anchor_time_spine,
        drop=[intermediate_timestamp_field],
    ).as_ref()

    # 2. gets all the effective_timestamps from the partial_agg node and backs out equivalent anchor time - these are all the times when an event can enter an aggregation window
    effective_timestamp_spine = AddRetrievalAnchorTimeNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=spine,
        name=fdw.name,
        feature_store_format_version=fdw.get_feature_store_format_version,
        batch_schedule=fdw.get_batch_schedule_for_version,
        tile_interval=fdw.get_tile_interval_for_offline_store,
        timestamp_field=effective_timestamp(),
        is_stream=fdw.is_stream,
        data_delay_seconds=fdw.online_store_data_delay_seconds,
    ).as_ref()

    # 3. unions the two sets together, de-duplicates, and renames the effective_timestamp column to the feature definition's timestamp key
    spine = UnionNode(dialect, compute_mode, anchor_time_spine, effective_timestamp_spine).as_ref()
    spine = SelectDistinctNode(dialect, compute_mode, spine, [*cols_to_keep, effective_timestamp()]).as_ref()
    spine = RenameColsNode(dialect, compute_mode, spine, mapping={effective_timestamp(): fdw.timestamp_key}).as_ref()

    if fdw.aggregation_secondary_key:
        spine = AggregationSecondaryKeyExplodeNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, spine=spine, fdw=fdw
        )

    return spine


def _should_use_sawtooth_aggregation_impl(fdw: feature_definition_wrapper.FeatureDefinitionWrapper) -> bool:
    if fdw.get_min_batch_sawtooth_tile_size() is not None:
        return True
    elif fdw.is_stream and fdw.compaction_enabled and fdw.has_lifetime_aggregate:
        # Stream compaction fv with only lifetime aggs should use the sawtooth impl since it is more performant.
        if fdw.has_aggregation_function(
            aggregation_function_pb2.AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT
        ) or fdw.has_aggregation_function(
            aggregation_function_pb2.AggregationFunction.AGGREGATION_FUNCTION_APPROX_PERCENTILE
        ):
            # Approx count distinct and approx percentile are not supported for this impl so in that case use the continuous implementation.
            return False
        return True

    return False


def _should_account_for_batch_publish_timestamp(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, skew_config: Optional[SkewConfig] = None
) -> bool:
    # if batch_publish_timestamp is not set, then we should never consider it.
    if fdw.batch_publish_timestamp is None:
        return False

    # if skew_config is not set, then the QT is running for materialization purposes (i.e. not for offline retrieval)
    # during actual materialization, we should account for batch_publish_timestamp
    if skew_config is None:
        return True

    # if skew_config is set but simulate_events_published_on_time = True, then we do NOT want to account for batch_publish_timestamp
    # because we are pretending all events were published on time
    return not skew_config.simulate_events_published_on_time


def build_spine_join_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    dac: FeatureDefinitionAndJoinConfig,
    spine_node: NodeRef,
    spine_time_field: str,
    from_source: Optional[bool],
    use_namespace_feature_prefix: bool = True,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
    mocked_fv_columns: Optional[Dict[str, List[str]]] = None,
) -> NodeRef:
    fdw = dac.feature_definition
    if fdw.timestamp_key is not None and spine_time_field != fdw.timestamp_key:
        spine_node = RenameColsNode(
            dialect, compute_mode, spine_node, mapping={spine_time_field: fdw.timestamp_key}
        ).as_ref()

    if any(jk[0] != jk[1] for jk in dac.join_keys):
        spine_node = RenameColsNode(
            dialect, compute_mode, spine_node, mapping={jk[0]: jk[1] for jk in dac.join_keys if jk[0] != jk[1]}
        ).as_ref()
    if fdw.is_temporal or fdw.is_feature_table:
        ret = _build_spine_query_tree_temporal_or_feature_table(
            dialect=dialect,
            compute_mode=compute_mode,
            spine_node=spine_node,
            dac=dac,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            from_source=from_source,
            use_namespace_feature_prefix=use_namespace_feature_prefix,
            mock_context=mock_context,
            skew_config=skew_config,
        )
    elif fdw.is_temporal_aggregate:
        if _should_use_sawtooth_aggregation_impl(fdw):
            sawtooth_agg_data = compaction_utils.SawtoothAggregationData.from_aggregate_features(fdw)
            untiled_partial_aggs = build_get_features(
                dialect,
                compute_mode,
                fdw,
                from_source=from_source,
                # NOTE: feature_data_time_limits is set to None since time pushdown
                # should happen as part of a optimization rewrite.
                feature_data_time_limits=None,
                aggregation_anchor_time=None,
                aggregation_tile_interval_override=pendulum.Duration(
                    seconds=0
                ),  # Explicitly set 0 because we need the row level offline events.
                mock_context=mock_context,
                skew_config=skew_config,
            )
            spine_node = _augment_spine_for_window_aggregation(
                dialect,
                compute_mode,
                fdw,
                0,
                spine_node,
                untiled_partial_aggs,
            )
            full_agg_node = _build_sawtooth_aggregation_subtree(
                dialect=dialect,
                compute_mode=compute_mode,
                spine_node=spine_node,
                from_source=from_source,
                feature_data_time_limits=None,
                fdw=fdw,
                sawtooth_aggregation_data=sawtooth_agg_data,
                spine_timestamp_field=fdw.timestamp_key,
                enable_rewrite=True,
            )
        else:
            partial_agg_node = build_get_features(
                dialect,
                compute_mode,
                fdw,
                from_source=from_source,
                # NOTE: feature_data_time_limits is set to None since time pushdown
                # should happen as part of a optimization rewrite.
                feature_data_time_limits=None,
                aggregation_anchor_time=None,
                mock_context=mock_context,
                skew_config=skew_config,
            )
            augmented_spine = _augment_spine_for_window_aggregation(
                dialect,
                compute_mode,
                fdw,
                fdw.get_tile_interval_for_offline_store,
                spine_node,
                partial_agg_node,
            )

            if _should_account_for_batch_publish_timestamp(fdw=fdw, skew_config=skew_config):
                full_agg_node = AsofBitemporalJoinFullAggNode(
                    dialect=dialect,
                    compute_mode=compute_mode,
                    spine=augmented_spine,
                    partial_agg_node=partial_agg_node,
                    fdw=fdw,
                    # Allow timestamp push down if the spine is provided by users.
                    enable_spine_time_pushdown_rewrite=True,
                    enable_spine_entity_pushdown_rewrite=True,
                ).as_ref()
            else:
                full_agg_node = AsofJoinFullAggNode(
                    dialect=dialect,
                    compute_mode=compute_mode,
                    spine=augmented_spine,
                    partial_agg_node=partial_agg_node,
                    fdw=fdw,
                    # Allow timestamp push down if the spine is provided by users.
                    enable_spine_time_pushdown_rewrite=True,
                    enable_spine_entity_pushdown_rewrite=True,
                ).as_ref()

        if fdw.aggregation_secondary_key:
            # Beside join keys and anchor time, we need to group by timestamp_key and TECTON_UNIQUE_ID_COL because:
            #   1. Grouping by timestamp_key is required to keep the timestamp column in the result.
            #   2. Grouping by TECTON_UNIQUE_ID_COL can distinguish duplicated rows in the spine.
            group_by_columns = [*list(fdw.join_keys), anchor_time(), fdw.timestamp_key, tecton_unique_id_col()]
            if tecton_spine_row_id_col() in full_agg_node.columns:
                group_by_columns += [tecton_spine_row_id_col()]
            full_agg_node = AggregationSecondaryKeyRollupNode(
                dialect=dialect,
                compute_mode=compute_mode,
                full_aggregation_node=full_agg_node,
                fdw=fdw,
                group_by_columns=group_by_columns,
            ).as_ref()
            full_agg_node = RenameColsNode(dialect, compute_mode, full_agg_node, drop=[tecton_unique_id_col()]).as_ref()

        if fdw.feature_start_timestamp:
            full_agg_node = RespectFeatureStartTimeNode.for_anchor_time_column(
                dialect,
                compute_mode,
                full_agg_node,
                anchor_time(),
                fdw,
            ).as_ref()
        ret = _rename_feature_columns_and_drop_non_feature_columns(
            dialect,
            compute_mode,
            dac,
            full_agg_node,
            use_namespace_feature_prefix,
        )
    elif fdw.is_rtfv:
        inputs = find_dependent_feature_set_items(
            fdw.fco_container,
            fdw.pipeline.root,
            visited_inputs={},
            fv_id=fdw.id,
        )
        dac = FeatureDefinitionAndJoinConfig.from_feature_definition(fdw)
        fsc = FeatureSetConfig([*inputs, dac])
        ret = build_feature_set_config_querytree(
            dialect=dialect,
            compute_mode=compute_mode,
            fsc=fsc,
            spine_node=spine_node,
            spine_time_field=spine_time_field,
            from_source=from_source,
            skew_config=skew_config,
            use_namespace_feature_prefix=use_namespace_feature_prefix,
            mocked_fv_columns=mocked_fv_columns,
        )
    else:
        raise NotImplementedError
    if fdw.timestamp_key is not None and spine_time_field != fdw.timestamp_key:
        ret = RenameColsNode(dialect, compute_mode, ret, {fdw.timestamp_key: spine_time_field}).as_ref()
    if any(jk[0] != jk[1] for jk in dac.join_keys):
        ret = RenameColsNode(
            dialect, compute_mode, ret, {jk[1]: jk[0] for jk in dac.join_keys if jk[0] != jk[1]}
        ).as_ref()
    return ret


# Construct each wildcard materialized fvtree by joining against distinct set of join keys.
# Then, outer join these using WildcardJoinNode which performs an outer join while handling null-valued features properly.
def _build_wild_fv_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    fv_dacs: List[FeatureDefinitionAndJoinConfig],
    spine_time_field: str,
    from_source: Optional[bool],
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    newtree = None
    for dac in fv_dacs:
        fdw = dac.feature_definition

        subspine_join_keys = [jk[0] for jk in dac.join_keys if jk[0] != fdw.wildcard_join_key]
        # SelectDistinctNode is needed for correctness in order to filter out rows with duplicate join keys before
        # retrieving feature values. This avoids exploding wildcard rows when there are duplicates in both the spine and the
        # feature view tree.
        subspine = SelectDistinctNode(
            dialect, compute_mode, spine_node, [*subspine_join_keys, spine_time_field]
        ).as_ref()
        fvtree = build_spine_join_querytree(
            dialect=dialect,
            compute_mode=compute_mode,
            dac=dac,
            spine_node=subspine,
            spine_time_field=spine_time_field,
            from_source=from_source,
            skew_config=skew_config,
        )
        if len(dac.features) < len(fdw.features):
            fvtree = RenameColsNode(
                dialect,
                compute_mode,
                fvtree,
                drop=[f"{fdw.name}{fdw.namespace_separator}{f}" for f in fdw.features if f not in dac.features],
            ).as_ref()
        if newtree is None:
            newtree = fvtree
        else:
            join_cols = [*subspine_join_keys, spine_time_field, fdw.wildcard_join_key]
            newtree = WildcardJoinNode(dialect, compute_mode, newtree, fvtree, join_cols=join_cols).as_ref()
    return newtree


# Construct each non-wildcard materialized fvtree by joining against distinct set of join keys.
# Then, outer join these fvtrees together.
def _build_standard_fv_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    fv_dacs: List[FeatureDefinitionAndJoinConfig],
    spine_time_field: str,
    from_source: Optional[bool],
    skew_config: SkewConfig,
    mocked_fv_columns: Optional[Dict[str, List[str]]] = None,
) -> Tuple[NodeRef, Set[str]]:
    internal_cols: Set[str] = set()

    # We check that feature definition with the same join config is not repeated.
    # This is an optimization to avoid retrieving & processing the same feature view multiple times
    unique_fv_dacs, namespace_restore_mapping = _group_dacs_by_name_and_join_config(fv_dacs, internal_cols)
    input_name_to_namespace = {input_name: dac.namespace for dac in fv_dacs for input_name in dac.input_names}
    newtree = spine_node
    all_feature_cols_to_namespaced_cols = {}
    mock_mapping = {}
    drop_cols = set()

    for dac in unique_fv_dacs:
        fdw = dac.feature_definition

        # When we have multiple inputs that use the same FV,
        # we only run the FV once and later need to map the feature columns
        # to the namespace of each input.
        feature_column_to_namespaced_cols = {
            src: dest_list
            for src, dest_list in namespace_restore_mapping.items()
            if src.startswith(f"{dac.namespace}{dac.feature_definition.namespace_separator}")
        }

        input_name_to_mocked_columns = {}
        if mocked_fv_columns is not None:
            input_name_to_mocked_columns = {
                input_name: mocked_cols
                for input_name, mocked_cols in mocked_fv_columns.items()
                if input_name in dac.input_names
            }

        all_features_mocked = (
            input_name_to_mocked_columns
            and
            # All inputs are mocked
            all(input_name in input_name_to_mocked_columns for input_name in dac.input_names)
            and
            # All features are mocked for each input
            all(set(mocked_cols) == set(dac.features) for mocked_cols in input_name_to_mocked_columns.values())
        )

        # If all the features from the Feature View are mocked, we
        # can skip the Feature Computation for this Feature View
        if all_features_mocked:
            for input_name, mocked_cols in input_name_to_mocked_columns.items():
                for feature in mocked_cols:
                    _update_mocked_rename_map(
                        input_name=input_name,
                        feature_name=feature,
                        dac=dac,
                        feature_column_to_namespaced_cols=feature_column_to_namespaced_cols,
                        input_name_to_namespace=input_name_to_namespace,
                        mock_mapping=mock_mapping,
                        all_feature_cols_to_namespaced_cols=all_feature_cols_to_namespaced_cols,
                        internal_cols=internal_cols,
                        drop_cols=drop_cols,
                    )
            continue

        subspine_join_keys = [jk[0] for jk in dac.join_keys]
        # SelectDistinctNode is needed for correctness in the case that there are duplicate rows in the spine. The
        # alternative considered was to add a row_id as a hash of the row or a monotonically increasing id, however the
        # row_id as a hash is not unique for duplicate rows and a monotonically increasing id is non-deterministic.
        subspine = SelectDistinctNode(
            dialect, compute_mode, spine_node, [*subspine_join_keys, spine_time_field]
        ).as_ref()

        fvtree = build_spine_join_querytree(
            dialect=dialect,
            compute_mode=compute_mode,
            dac=dac,
            spine_node=subspine,
            spine_time_field=spine_time_field,
            from_source=from_source,
            skew_config=skew_config,
        )

        if len(dac.features) < len(fdw.features) or feature_column_to_namespaced_cols:
            drop_cols.update(
                feature_column
                for feature_column, namespaced_columns in feature_column_to_namespaced_cols.items()
                if feature_column not in namespaced_columns
            )
            all_feature_cols_to_namespaced_cols.update(feature_column_to_namespaced_cols)

        allow_null_features = conf.get_bool("ALLOW_NULL_FEATURES")

        newtree = JoinNode(
            dialect,
            compute_mode,
            newtree,
            fvtree,
            how="inner",
            join_cols=([*subspine_join_keys, spine_time_field]),
            allow_nulls=allow_null_features,
        ).as_ref()

        if mocked_fv_columns:
            # Rename mocked columns to appropriate namespaced FV column
            for input_name, mocked_columns in input_name_to_mocked_columns.items():
                for feature in mocked_columns:
                    _update_mocked_rename_map(
                        input_name=input_name,
                        feature_name=feature,
                        dac=dac,
                        feature_column_to_namespaced_cols=feature_column_to_namespaced_cols,
                        input_name_to_namespace=input_name_to_namespace,
                        mock_mapping=mock_mapping,
                        all_feature_cols_to_namespaced_cols=all_feature_cols_to_namespaced_cols,
                        internal_cols=internal_cols,
                        drop_cols=drop_cols,
                    )

    if all_feature_cols_to_namespaced_cols or drop_cols:
        # Separate rename node for the namespaced columns since we do not want to keep the original columns
        newtree = RenameColsNode(
            dialect,
            compute_mode,
            newtree,
            mapping=all_feature_cols_to_namespaced_cols,
            drop=drop_cols,
        ).as_ref()

    if mock_mapping:
        newtree = RenameColsNode(
            dialect,
            compute_mode,
            newtree,
            mapping=mock_mapping,
            keep_original_columns_from_mapping=True,
        ).as_ref()

    return newtree, internal_cols


def _update_mocked_rename_map(
    input_name: str,
    feature_name: str,
    dac: FeatureDefinitionAndJoinConfig,
    feature_column_to_namespaced_cols: Dict[str, List[str]],
    input_name_to_namespace: Dict[str, str],
    mock_mapping: Dict[str, str],
    drop_cols: Set[str],
    all_feature_cols_to_namespaced_cols: Dict[str, List[str]],
    internal_cols: Set[str],
) -> None:
    """
    Handles the logic for mapping a mocked feature column to its actual
    or namespaced representation.
    """
    fdw = dac.feature_definition
    mock_column_name = f"{input_name}{MOCK_COLUMN_SEPARATOR}{feature_name}"
    actual_feature_column_key = f"{dac.namespace}{fdw.namespace_separator}{feature_name}"
    internal_cols.add(actual_feature_column_key)

    if not feature_column_to_namespaced_cols:
        mock_mapping.update({mock_column_name: actual_feature_column_key})
        drop_cols.add(actual_feature_column_key)
        return

    if actual_feature_column_key not in feature_column_to_namespaced_cols:
        logger.warning(
            f"WARNING: Mocked feature column {feature_name} not found in Feature View {fdw.name}, skipping..."
        )
        return

    target_namespaced_cols = feature_column_to_namespaced_cols.get(actual_feature_column_key)
    for namespaced_col in target_namespaced_cols:
        if input_name_to_namespace[input_name] in namespaced_col:
            mock_mapping.update({mock_column_name: namespaced_col})
            drop_cols.add(actual_feature_column_key)

            if (
                actual_feature_column_key in all_feature_cols_to_namespaced_cols
                and namespaced_col in all_feature_cols_to_namespaced_cols[actual_feature_column_key]
            ):
                all_feature_cols_to_namespaced_cols[actual_feature_column_key].remove(namespaced_col)
            break


def _update_internal_cols(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    dac: FeatureDefinitionAndJoinConfig,
    internal_cols: Set[str],
) -> None:
    if dac.namespace.startswith(udf_internal()):
        for feature in fdw.features:
            internal_cols.add(dac.namespace + fdw.namespace_separator + feature)
    for feature in dac.features:
        if udf_internal() in feature:
            internal_cols.add(feature)


def _group_dacs_by_name_and_join_config(
    dacs: List[FeatureDefinitionAndJoinConfig], internal_cols: Set[str]
) -> Tuple[List[FeatureDefinitionAndJoinConfig], Dict[str, List[str]]]:
    """
    When building query tree for a feature service, we can use the same feature view multiple times (for each dependent
    RTFV plus user can explicitly include it into a feature service).

    To avoid repeating retrieval and computation we will group feature definition configs by name (refers to
    feature view name and supposed to be unique) and join config.

    We will also build a map for restoring features back to initial namespaces.

    """
    unique_fv_dacs = {}  # non-repeating FeatureDefinitionAndJoinConfigs grouped by name and join config

    # One feature can be used in multiple namespaces (ie, one per RTFV)
    # This is a map from one namespaced feature to list of namespaced features it should be renamed to
    restore_mapping: Dict[str, List[str]] = {}

    for dac in dacs:
        _update_internal_cols(dac.feature_definition, dac, internal_cols)

        key = (dac.name, tuple(dac.join_keys))
        if key not in unique_fv_dacs:
            unique_fv_dacs[key] = dac
        else:
            unique_fv_dacs[key] = attrs.evolve(
                unique_fv_dacs[key], features=list(set(unique_fv_dacs[key].features) | set(dac.features))
            )
            unique_fv_dacs[key].input_names.extend(dac.input_names)

        for f in dac.features:
            grouped_f = f"{unique_fv_dacs[key].namespace}{dac.feature_definition.namespace_separator}{f}"
            restored_f = f"{dac.namespace}{dac.feature_definition.namespace_separator}{f}"
            restore_mapping.setdefault(grouped_f, []).append(restored_f)

    if len(unique_fv_dacs) == len(dacs):
        return dacs, {}

    return list(unique_fv_dacs.values()), restore_mapping


def _dac_has_transformation(dac: FeatureDefinitionAndJoinConfig) -> bool:
    return bool(dac.feature_definition.transformations)


def _build_rtfv_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    parent_tree: NodeRef,
    rtfv_dacs: List[FeatureDefinitionAndJoinConfig],
    spine_timestamp_field: str,
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    newtree = parent_tree
    # If there are rtfvs w/o transformations (calculations), we compute them with the MultiRtfvFeatureExtractionNode
    no_transform_feature_definition_namespaces = [
        (dac.feature_definition, dac.namespace) for dac in rtfv_dacs if not _dac_has_transformation(dac)
    ]
    if no_transform_feature_definition_namespaces:
        newtree = MultiRtfvFeatureExtractionNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=newtree,
            feature_definition_namespaces=no_transform_feature_definition_namespaces,
            events_df_timestamp_field=spine_timestamp_field,
            use_namespace_feature_prefix=use_namespace_feature_prefix,
        ).as_ref()

    # if there are rtfvs with transformations, we compute them with the MultiOdfvPipelineNode
    feature_definition_namespaces_with_transforms = [
        (dac.feature_definition, dac.namespace) for dac in rtfv_dacs if _dac_has_transformation(dac)
    ]
    if feature_definition_namespaces_with_transforms:
        newtree = StagingNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=newtree,
            staging_table_name=odfv_internal_staging_table(),
            query_tree_step=QueryTreeStep.AGGREGATION,
        ).as_ref()

        newtree = MultiOdfvPipelineNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=newtree,
            feature_definition_namespaces=feature_definition_namespaces_with_transforms,
            events_df_timestamp_field=spine_timestamp_field,
            use_namespace_feature_prefix=use_namespace_feature_prefix,
        ).as_ref()

    # Compute the union of the features to be computed
    dac_features = set()
    fdw_features = set()
    for dac in rtfv_dacs:
        feature_prefix = f"{dac.namespace}{dac.feature_definition.namespace_separator}"
        dac_features.update({f"{feature_prefix}{f}" for f in dac.features})
        fdw_features.update({f"{feature_prefix}{f}" for f in dac.feature_definition.features})

    # Drop features if user queried a subset via feature services
    if len(dac_features) < len(fdw_features):
        newtree = RenameColsNode(
            dialect,
            compute_mode,
            newtree,
            drop=[namespaced_feat for namespaced_feat in fdw_features if namespaced_feat not in dac_features],
        ).as_ref()
    return newtree


# Construct each materialized fvtree by joining against distinct set of join keys.
# Then, join the full spine against each of those.
# Finally, compute odfvs via udf on top of the result (not using joins)
def build_feature_set_config_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fsc: FeatureSetConfig,
    spine_node: NodeRef,
    spine_time_field: str,
    from_source: Optional[bool],
    skew_config: Optional[SkewConfig],
    use_namespace_feature_prefix: bool = True,
    mocked_fv_columns: Optional[Dict[str, List[str]]] = None,
) -> NodeRef:
    odfv_dacs: List[FeatureDefinitionAndJoinConfig] = []
    wildcard_dacs: List[FeatureDefinitionAndJoinConfig] = []
    normal_fv_dacs: List[FeatureDefinitionAndJoinConfig] = []
    internal_cols: Set[str] = set()
    newtree = spine_node

    for dac in fsc.definitions_and_configs:
        if dac.feature_definition.is_rtfv:
            odfv_dacs.append(dac)
        elif _is_wildcard_join(dac.feature_definition, spine_node):
            wildcard_dacs.append(dac)
        else:
            normal_fv_dacs.append(dac)

    if wildcard_dacs:
        newtree = _build_wild_fv_subtree(
            dialect=dialect,
            compute_mode=compute_mode,
            spine_node=newtree,
            fv_dacs=wildcard_dacs,
            spine_time_field=spine_time_field,
            from_source=from_source,
            skew_config=skew_config,
        )

    if normal_fv_dacs:
        newtree, internal_cols = _build_standard_fv_subtree(
            dialect=dialect,
            compute_mode=compute_mode,
            spine_node=newtree,
            fv_dacs=normal_fv_dacs,
            spine_time_field=spine_time_field,
            from_source=from_source,
            skew_config=skew_config,
            mocked_fv_columns=mocked_fv_columns,
        )

    if odfv_dacs:
        newtree = _build_rtfv_subtree(
            dialect, compute_mode, newtree, odfv_dacs, spine_time_field, use_namespace_feature_prefix
        )

    # drop all internal cols
    if len(internal_cols) > 0:
        newtree = RenameColsNode(dialect, compute_mode, newtree, drop=list(internal_cols)).as_ref()

    return newtree


def _build_spine_query_tree_temporal_or_feature_table(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    dac: FeatureDefinitionAndJoinConfig,
    data_delay_seconds: int,
    from_source: Optional[bool],
    use_namespace_feature_prefix: bool = True,
    mock_context: Optional[MockContext] = None,
    skew_config: Optional[SkewConfig] = None,
) -> NodeRef:
    fdw = dac.feature_definition
    base = build_get_features(
        dialect, compute_mode, fdw, from_source=from_source, mock_context=mock_context, skew_config=skew_config
    )
    batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
    base = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        base,
        timestamp_field=fdw.materialization_job_partition_timestamp
        if _should_account_for_batch_publish_timestamp(fdw=fdw, skew_config=skew_config)
        else fdw.timestamp_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=data_delay_seconds,
        is_stream=fdw.is_stream,
    ).as_ref()
    if fdw.serving_ttl is not None:
        base = AddDurationNode(
            dialect,
            compute_mode,
            base,
            timestamp_field=fdw.materialization_job_partition_timestamp
            if _should_account_for_batch_publish_timestamp(fdw=fdw, skew_config=skew_config)
            else fdw.timestamp_key,
            duration=fdw.serving_ttl,
            new_column_name=timestamp_plus_ttl(),
        ).as_ref()
        # Calculate effective expiration time = window(feature_time + ttl, batch_schedule).end + data_delay
        batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
        base = AddEffectiveTimestampNode(
            dialect,
            compute_mode,
            base,
            timestamp_field=timestamp_plus_ttl(),
            effective_timestamp_name=expiration_timestamp(),
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=data_delay_seconds,
            is_stream=fdw.is_stream,
        ).as_ref()

    rightside_join_prefix = "_tecton_right"
    join_prefixed_feature_names = [f"{rightside_join_prefix}_{f}" for f in fdw.features]

    if fdw.feature_start_timestamp is not None:
        base = RespectFeatureStartTimeNode(
            dialect,
            compute_mode,
            base,
            fdw.timestamp_key,
            fdw.feature_start_timestamp,
            fdw.features,
            fdw.get_feature_store_format_version,
        ).as_ref()

    if _is_wildcard_join(fdw, spine_node):
        # Need to copy base so that the left and right side are separate
        base_copy = base.deepcopy()
        spine_node = AsofSecondaryKeyExplodeNode(
            dialect, compute_mode, spine_node, fdw.timestamp_key, base_copy, effective_timestamp(), fdw
        ).as_ref()

    base = AsofJoinNode(
        dialect=dialect,
        compute_mode=compute_mode,
        left_container=AsofJoinInputContainer(spine_node, fdw.timestamp_key),
        right_container=AsofJoinInputContainer(
            base,
            timestamp_field=fdw.timestamp_key,
            effective_timestamp_field=effective_timestamp(),
            prefix=rightside_join_prefix,
            schema=fdw.view_schema,
        ),
        join_cols=fdw.join_keys,
    ).as_ref()

    prefix = f"{dac.namespace}{fdw.namespace_separator}" if use_namespace_feature_prefix else ""
    # we can't just ask for the correct right_prefix to begin with because the asofJoin always sticks an extra underscore in between
    rename_map: Dict[str, Optional[str]] = {}
    cols_to_drop = []
    for f in fdw.features:
        if f not in dac.features:
            cols_to_drop.append(f"{rightside_join_prefix}_{f}")
        else:
            rename_map[f"{rightside_join_prefix}_{f}"] = f"{prefix}{f}"

    cols_to_drop.append(f"{rightside_join_prefix}_{fdw.timestamp_key}")
    cols_to_drop.append(f"{rightside_join_prefix}_{anchor_time()}")
    cols_to_drop.append(f"{rightside_join_prefix}_{effective_timestamp()}")

    expiration_timestamp_col = f"{rightside_join_prefix}_{expiration_timestamp()}"
    if fdw.serving_ttl is not None:
        base = RespectTTLNode(
            dialect, compute_mode, base, fdw.timestamp_key, expiration_timestamp_col, join_prefixed_feature_names
        ).as_ref()
        cols_to_drop.append(f"{rightside_join_prefix}_{timestamp_plus_ttl()}")
        cols_to_drop.append(expiration_timestamp_col)

    if fdw.batch_publish_timestamp is not None:
        cols_to_drop.append(f"{rightside_join_prefix}_{fdw.batch_publish_timestamp}")
    # remove anchor cols/dupe timestamp cols
    return RenameColsNode(dialect, compute_mode, base, mapping=rename_map, drop=cols_to_drop).as_ref()


def _augment_spine_for_window_aggregation(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    tile_interval: int,
    spine_node: NodeRef,
    partial_agg_node: NodeRef,
) -> NodeRef:
    augmented_spine = AddRetrievalAnchorTimeNode(
        dialect,
        compute_mode,
        spine_node,
        name=fdw.name,
        feature_store_format_version=fdw.get_feature_store_format_version,
        batch_schedule=fdw.get_batch_schedule_for_version,
        tile_interval=tile_interval,
        timestamp_field=fdw.timestamp_key,
        is_stream=fdw.is_stream,
        data_delay_seconds=fdw.online_store_data_delay_seconds,
    ).as_ref()

    # We need to explode the spine for the secondary key if:
    #     1. A Feature View with an aggregation_secondary_key: an aggregation_secondary_key is never in the spine,
    #     so we always need to explode the spine for it.
    #     2. A Feature View with a wild card join key: a wild card join key is optional in the spine, so we need to
    #     check if the wild card join key is not in the spine before exploding the spine for it.
    if fdw.aggregation_secondary_key or _is_wildcard_join(fdw, spine_node):
        # Add a unique id column if aggreagtion secondary key appears. The unique id column is used to make each spine
        # row unique so later the secondary key aggregation rollup doesn't merge duplicate rows.
        if fdw.aggregation_secondary_key:
            augmented_spine = AddUniqueIdNode(dialect, compute_mode, augmented_spine).as_ref()

        return AsofSecondaryKeyExplodeNode(
            dialect,
            compute_mode,
            augmented_spine,
            anchor_time(),
            partial_agg_node,
            anchor_time(),
            fdw,
        ).as_ref()

    return augmented_spine


def _rename_feature_columns_and_drop_non_feature_columns(
    dialect: Dialect,
    compute_mode: ComputeMode,
    dac: FeatureDefinitionAndJoinConfig,
    node: NodeRef,
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    rename_map: Dict[str, Optional[str]] = {}
    columns_to_drop = [anchor_time()]
    for f in dac.feature_definition.features:
        if f not in dac.features:
            columns_to_drop.append(f)
        elif use_namespace_feature_prefix:
            # TODO: make a helper
            rename_map[f] = f"{dac.namespace}{dac.feature_definition.namespace_separator}{f}"
    return RenameColsNode(dialect, compute_mode, node, mapping=rename_map, drop=columns_to_drop).as_ref()


def _add_sawtooth_anchor_time_and_partition_columns(
    dialect: Dialect,
    compute_mode: ComputeMode,
    input_node: NodeRef,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    sawtooth_aggregation_data: compaction_utils.SawtoothAggregationData,
    timestamp_field: str,
    should_truncate_timestamps: bool = False,
    non_sawtooth_partition_value: bool = True,
    sawtooth_partition_value: bool = True,
) -> NodeRef:
    aggregation_tile_interval_map = sawtooth_aggregation_data.get_anchor_time_to_aggregation_interval_map(
        fdw.get_tile_interval_for_sawtooths, fdw.get_feature_store_format_version
    )
    output_node = AddAnchorTimeColumnsForSawtoothIntervalsNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=input_node,
        timestamp_field=timestamp_field,
        anchor_time_column_map=sawtooth_aggregation_data.get_anchor_time_to_timedelta_map(
            use_zero_timedelta=not should_truncate_timestamps
        ),
        data_delay_seconds=fdw.online_store_data_delay_seconds,
        feature_store_format_version=fdw.get_feature_store_format_version,
        aggregation_tile_interval_column_map=aggregation_tile_interval_map,
        truncate_to_recent_complete_tile=False,
    ).as_ref()
    partial_column_to_bool_map = sawtooth_aggregation_data.get_partition_column_to_bool_map(
        sawtooth_bool_value=sawtooth_partition_value, non_sawtooth_bool_value=non_sawtooth_partition_value
    )
    output_node = AddBooleanPartitionColumnsNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=output_node,
        column_to_bool_map=partial_column_to_bool_map,
    ).as_ref()
    return output_node


def _build_partial_aggs_for_compacted_tile_rollup(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    sawtooth_aggregation_data: compaction_utils.SawtoothAggregationData,
    feature_data_time_limits: Optional[pendulum.Period],
    from_source: bool,
    mock_context: Optional[MockContext] = None,
) -> NodeRef:
    """
    Build the partial aggregate tiles that will be used to compute the compacted tiles.

    First, we read from the offline store and tile based on the smallest sawtooth size used by the aggregations (either 1d or 1hr).
    Then, we add the anchor time and partition columns use for the full aggregation roll up.
    For the special case where the fv contains < 2d aggregations with a stream tile size < 1hr, we do an extra read from the offline store and union those results with the original partial aggs.

    This is only used for sawtooth features and the result should be an input to AsofJoinReducePartialAggNode.
    """
    # Build batch partial aggregates
    tiled_partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_tile_interval_override=fdw.get_tile_interval_duration_for_sawtooths,
        mock_context=mock_context,
    )
    batch_partial_agg_subtree = _add_sawtooth_anchor_time_and_partition_columns(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=tiled_partial_aggs,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
        fdw=fdw,
        timestamp_field=anchor_time(),
        non_sawtooth_partition_value=False,
    )

    explode_partial_aggs_for_non_sawtooths = sawtooth_aggregation_data.contains_tiled_non_sawtooth_aggregations()
    if explode_partial_aggs_for_non_sawtooths:
        # If the fv contains < 2d aggregations with a stream tile size < 1hr, mimic sawtoothing behavior with the stream tile size as the sawtooth size.
        # Do an extra read from the offline store in order to achieve this, instead of doing one read and tiling based on the stream tile size (which could hurt performance of large windows).
        untiled_partial_aggs_node_for_batch = build_get_features(
            dialect=dialect,
            compute_mode=compute_mode,
            fdw=fdw,
            from_source=from_source,
            feature_data_time_limits=feature_data_time_limits,
            aggregation_tile_interval_override=pendulum.Duration(
                seconds=0
            ),  # Explicity set 0 because we need the raw offline events.
            mock_context=mock_context,
        )
        extra_batch_partial_agg_node = _add_sawtooth_anchor_time_and_partition_columns(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=untiled_partial_aggs_node_for_batch,
            # Do NOT tile the partial aggs since 5min and 1min tiles are too small and hurt performance.
            sawtooth_aggregation_data=sawtooth_aggregation_data,
            fdw=fdw,
            timestamp_field=anchor_time(),
            should_truncate_timestamps=True,
            # Since the extra partial aggs are not tiled, we need to adjust the timestamps to reflect the effective time of the event.
            non_sawtooth_partition_value=True,
            sawtooth_partition_value=False,
        )
        # TODO(compaction): To improve performance, push a smaller spine time range filter to the extra_batch_partial_aggs since it only needs to lookback max 2d.
        batch_partial_agg_subtree = UnionNode(
            dialect=dialect,
            compute_mode=compute_mode,
            left=batch_partial_agg_subtree,
            right=extra_batch_partial_agg_node,
        ).as_ref()
    return batch_partial_agg_subtree


def _build_deduped_spine_for_compacted_tile(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    sawtooth_aggregation_data: compaction_utils.SawtoothAggregationData,
    spine_timestamp_field: str,
) -> NodeRef:
    """Build the spine that will be used to compute the compacted tiles.

    Example:
        spine passed in by user =
            join_key | timestamp          |
            1        | 2021-01-01 06:00:00|
            1        | 2021-01-01 12:33:00|
            1        | 2021-01-02 04:00:00|
            1        | 2021-01-02 04:15:00|

        Assume there are 30d and 7d aggregations in the feature view.
        Output =
            join_key | _anchor_time_for_day | _anchor_time_for_hour | _is_day | _is_hour
            1        | 2021-01-01 00:00:00  | None                  | True    | False
            1        | 2021-01-02 00:00:00  | None                  | True    | False
            1        | None                 | 2021-01-01 06:00:00   | False   | True
            1        | None                 | 2021-01-01 12:00:00   | False   | True
            1        | None                 | 2021-01-02 04:00:00   | False   | True

    This is only used for sawtooth features and the result should be an input to AsofJoinReducePartialAggNode.
    """
    batch_spine_node = AddAnchorTimeColumnsForSawtoothIntervalsNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=spine_node,
        timestamp_field=spine_timestamp_field,
        anchor_time_column_map=sawtooth_aggregation_data.get_anchor_time_to_timedelta_map(),
        data_delay_seconds=fdw.online_store_data_delay_seconds,
        feature_store_format_version=fdw.get_feature_store_format_version,
        aggregation_tile_interval_column_map=sawtooth_aggregation_data.get_anchor_time_to_aggregation_interval_map(
            fdw.get_tile_interval_for_sawtooths, fdw.get_feature_store_format_version
        ),
        truncate_to_recent_complete_tile=True,
    ).as_ref()
    batch_spine_node = RenameColsNode(
        dialect,
        compute_mode,
        batch_spine_node,
        drop=[fdw.time_key],
    ).as_ref()

    if sawtooth_aggregation_data.contains_continuous_non_sawtooth_aggregations():
        # Do not explode the spine for the continuous aggregations since the FullAggNode does not compute these.
        batch_spine_node = AddBooleanPartitionColumnsNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=batch_spine_node,
            column_to_bool_map={is_non_sawtooth(): False},
        ).as_ref()

    explode_partial_aggs_for_non_sawtooths = sawtooth_aggregation_data.contains_tiled_non_sawtooth_aggregations()
    return ExplodeEventsByTimestampAndSelectDistinctNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=batch_spine_node,
        explode_columns=sawtooth_aggregation_data.get_anchor_time_columns(
            include_non_sawtooths=explode_partial_aggs_for_non_sawtooths
        ),
        explode_columns_to_boolean_columns=sawtooth_aggregation_data.get_anchor_time_to_partition_columns_map(
            include_non_sawtooths=explode_partial_aggs_for_non_sawtooths
        ),
        timestamp_column=anchor_time(),
        columns_to_ignore=[anchor_time_for_non_sawtooth()]
        if sawtooth_aggregation_data.contains_continuous_non_sawtooth_aggregations()
        else [],
    ).as_ref()


def _build_sawtooth_aggregation_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    sawtooth_aggregation_data: compaction_utils.SawtoothAggregationData,
    spine_timestamp_field: str,
    feature_data_time_limits: Optional[pendulum.Period],
    from_source: bool,
    enable_rewrite: bool,
    mock_context: Optional[MockContext] = None,
) -> NodeRef:
    """Compute the full agg rollups for aggregate fvs that use sawtoothing.

    The overall steps are:
    1. Create the compacted tiles for each spine timestamp and aggregation window.
    2. Read the stream events from offline store.
    3. Join the compacted tiles with the stream events and agg to get the full feature value.

    Only applicable to stream fvs that use compaction. https://www.notion.so/tecton/Proposed-Offline-Sawtooth-Query-c7acbb0d65564027b6bafd8eddbdcba7"""
    # 1. Create the compacted tiles for each spine timestamp and aggregation window.
    batch_partial_agg_subtree = _build_partial_aggs_for_compacted_tile_rollup(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
        feature_data_time_limits=feature_data_time_limits,
        from_source=from_source,
        mock_context=mock_context,
    )
    batch_spine_node = _build_deduped_spine_for_compacted_tile(
        dialect=dialect,
        compute_mode=compute_mode,
        spine_node=spine_node,
        fdw=fdw,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
        spine_timestamp_field=spine_timestamp_field,
    )
    batch_part_subtree = AsofJoinReducePartialAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=batch_spine_node,
        partial_agg_node=batch_partial_agg_subtree,
        fdw=fdw,
        enable_spine_time_pushdown_rewrite=enable_rewrite,
        enable_spine_entity_pushdown_rewrite=enable_rewrite,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
    ).as_ref()
    # The result of the AsofJoinReducePartialAggNode node has an anchor time that's the start of the day/hour.
    # For the AsofJoinSawtoothAggNode, this anchor time needs to be the end of the day/hour in order for the time partitioning to work correctly.
    batch_part_subtree = AdjustAnchorTimeToWindowEndNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=batch_part_subtree,
        anchor_time_columns=sawtooth_aggregation_data.get_anchor_time_columns(),
        aggregation_tile_interval_column_map=sawtooth_aggregation_data.get_anchor_time_to_aggregation_interval_map(
            fdw.get_tile_interval_for_sawtooths, fdw.get_feature_store_format_version
        ),
    ).as_ref()

    # 2. Read the stream events from offline store.
    untiled_partial_aggs_node_for_stream = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        from_source=from_source,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_tile_interval_override=pendulum.Duration(
            seconds=0
        ),  # Explicity set 0 because we need the raw offline events.
        mock_context=mock_context,
    )
    stream_partial_agg_tree = _add_sawtooth_anchor_time_and_partition_columns(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=untiled_partial_aggs_node_for_stream,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
        fdw=fdw,
        timestamp_field=anchor_time(),
    )
    sawtooth_agg_spine_tree = _add_sawtooth_anchor_time_and_partition_columns(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=spine_node,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
        fdw=fdw,
        timestamp_field=spine_timestamp_field,
    )

    # 3. Join the compacted tiles with the stream events and spine, then agg to get the full feature value.
    sawtooth_agg_node = AsofJoinSawtoothAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        batch_input_node=batch_part_subtree,
        stream_input_node=stream_partial_agg_tree,
        spine_input_node=sawtooth_agg_spine_tree,
        sawtooth_aggregation_data=sawtooth_aggregation_data,
        fdw=fdw,
        enable_spine_time_pushdown_rewrite=enable_rewrite,
        enable_spine_entity_pushdown_rewrite=enable_rewrite,
    ).as_ref()
    rename_cols_node = RenameColsNode(
        dialect,
        compute_mode,
        sawtooth_agg_node,
        drop=sawtooth_aggregation_data.get_anchor_time_columns()
        + sawtooth_aggregation_data.get_identifier_partition_columns(),
    ).as_ref()
    return rename_cols_node


def _build_aggregation_group_data_node(
    dialect: Dialect, compute_mode: ComputeMode, aggregation_groups: Tuple[compaction_utils.AggregationGroup, ...]
) -> PythonDataNode:
    data = tuple(
        (group.window_index, group.tile_index, group.inclusive_start_time, group.exclusive_end_time)
        for group in aggregation_groups
    )
    # We need to specify an explict schema since inclusive_start_time can be null.
    schema_dict = {
        aggregation_group_id(): data_types.Int64Type(),
        aggregation_tile_id(): data_types.Int64Type(),
        inclusive_start_time(): data_types.TimestampType(),
        exclusive_end_time(): data_types.TimestampType(),
    }
    return PythonDataNode.from_schema(dialect, compute_mode, schema=Schema.from_dict(schema_dict), data=data)


def build_compaction_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    compaction_job_end_time: datetime,
    enable_from_source_for_test: bool = False,
    mock_context: Optional[MockContext] = None,
) -> NodeRef:
    """Build compaction query for online materialization jobs. Only used for fvs with batch compaction enabled.

    enable_from_source_for_test=True should only be used in local integration tests!"""
    feature_data_time_limits = compaction_utils.get_data_time_limits_for_compaction(
        fdw=fdw, compaction_job_end_time=compaction_job_end_time
    )
    if enable_from_source_for_test:
        # Only used for local testing
        base_node = build_pipeline_querytree(
            dialect,
            compute_mode,
            fdw,
            for_stream=False,
            feature_data_time_limits=feature_data_time_limits,
            mock_context=mock_context,
        )
    else:
        base_node = OfflineStoreScanNode(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition_wrapper=fdw,
            partition_time_filter=feature_data_time_limits,
        ).as_ref()
        base_node = StagingNode(
            dialect=Dialect.ARROW,
            compute_mode=compute_mode,
            input_node=base_node,
            staging_table_name=f"offline_store_{fdw.name}",
        ).as_ref()
        if feature_data_time_limits:
            base_node = FeatureTimeFilterNode(
                dialect=dialect,
                compute_mode=compute_mode,
                input_node=base_node,
                feature_data_time_limits=feature_data_time_limits,
                policy=fdw.time_range_policy,
                start_timestamp_field=fdw.timestamp_key,
                end_timestamp_field=fdw.timestamp_key,
            ).as_ref()

    if fdw.is_temporal_aggregate:
        aggregation_groups = compaction_utils.aggregation_groups(fdw, compaction_job_end_time)
        compaction_ranges = _build_aggregation_group_data_node(dialect, compute_mode, aggregation_groups).as_ref()
        node = InnerJoinOnRangeNode(
            dialect=dialect,
            compute_mode=compute_mode,
            left=base_node,
            right=compaction_ranges,
            left_join_condition_column=fdw.timestamp_key,
            right_inclusive_start_column=inclusive_start_time(),
            right_exclusive_end_column=exclusive_end_time(),
        ).as_ref()
        node = OnlinePartialAggNodeV2(
            dialect,
            compute_mode,
            node,
            fdw=fdw,
            aggregation_groups=aggregation_groups,
        ).as_ref()
        node = OnlineListAggNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=node,
            fdw=fdw,
            aggregation_groups=aggregation_groups,
        ).as_ref()
        return node
    elif fdw.is_temporal:
        node = TakeLastRowNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, fdw=fdw, input_node=base_node
        )
        node = TemporalBatchTableFormatNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, fdw=fdw, input_node=node
        )
        return node

    msg = "Unexpected FV type."
    raise Exception(msg)
