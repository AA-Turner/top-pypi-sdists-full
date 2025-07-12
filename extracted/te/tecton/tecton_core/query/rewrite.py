from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional

import attrs
import pandas

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import TectonValidationError
from tecton_core.pipeline.pipeline_common import get_start_end_from_feature_time_limits
from tecton_core.pipeline.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query.builder import _should_account_for_batch_publish_timestamp
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.nodes import AddAnchorTimeColumnsForSawtoothIntervalsNode
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddBooleanPartitionColumnsNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import AsofJoinReducePartialAggNode
from tecton_core.query.nodes import AsofJoinSawtoothAggNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import UnionNode
from tecton_core.query.nodes import UserSpecifiedDataNode


if TYPE_CHECKING:
    import pyspark.sql


class Rewrite(ABC):
    @abstractmethod
    def rewrite(self, node: NodeRef) -> None:
        raise NotImplementedError


class MockDataRewrite(Rewrite):
    """
    Replace DataSourceScanNode with MockDataSourceScanNode based on DataSource ID map.
    """

    def __init__(self, mock_data: Dict[str, NodeRef]) -> None:
        self.mock_data = mock_data

    def rewrite(self, tree: NodeRef) -> None:
        if isinstance(tree.node, DataSourceScanNode):
            node = tree.node
            if node.ds.id in self.mock_data:
                # Replace with mock data
                tree.node = MockDataSourceScanNode(
                    node.dialect,
                    node.compute_mode,
                    self.mock_data[node.ds.id],
                    node.ds,
                    self.mock_data[node.ds.id].columns,
                    node.start_time,
                    node.end_time,
                )
        else:
            for i in tree.inputs:
                self.rewrite(i)


class SpineEntityPushdown(Rewrite):
    """Filters the original feature data with respect to the entities contained in a spine.

    This should be applied to AsofJoinNodes and AsofJoinFullAggNodes since both of have sorts (as part of windows), for
    which we would like to minimize memory usage.
    """

    def __init__(self):
        pass

    def rewrite(self, tree: NodeRef) -> None:
        if isinstance(tree.node, AsofJoinNode):
            self.rewrite_asof(tree)
        elif isinstance(tree.node, (AsofJoinFullAggNode, AsofJoinReducePartialAggNode)):
            self.rewrite_asof_full_agg(tree)
        elif isinstance(tree.node, AsofJoinSawtoothAggNode):
            self.rewrite_asof_sawtooth_agg(tree)
        else:
            for i in tree.inputs:
                self.rewrite(i)

    def rewrite_asof(self, tree: NodeRef) -> None:
        node = tree.node
        # In our current usage of AsofJoinNode, we always pass in the spine on the left.
        spine_df = node.left_container.node.deepcopy()
        self.pushdown_entities(node.right_container.node, spine_df, node.join_cols)

    def rewrite_asof_full_agg(self, tree: NodeRef) -> None:
        node = tree.node

        if not node.enable_spine_entity_pushdown_rewrite:
            return

        # cannot use the user_provided_spine_node_ref because there are various RenameCols on top of the UserSpecifiedDataNode
        if isinstance(node, (AsofJoinFullAggNode, AsofJoinReducePartialAggNode)):
            spine_to_use = node.spine
        else:
            msg = f"Unhandled node type {node.__class__.__name__}"
            raise ValueError(msg)

        user_provided_spine_node_ref = get_first_input_node_of_class(node.spine, UserSpecifiedDataNode).as_ref()

        # Note: we can't simply using join keys to pushdown entity because wildcard FV can have a spine missing wildcard
        # key, so we need to check what exact entities are used in spine if wildcard key is present, and only push those
        # entities down.
        entities_to_push_down = node.fdw.join_keys
        if node.fdw.wildcard_join_key and node.fdw.wildcard_join_key not in user_provided_spine_node_ref.columns:
            entities_to_push_down = set(entities_to_push_down) - {node.fdw.wildcard_join_key}

        # entity_rewritable ensures there is a UserSpecifiedDataNode in the spine.
        self.pushdown_entities(node.partial_agg_node, spine_to_use.deepcopy(), list(entities_to_push_down))

    def rewrite_asof_sawtooth_agg(self, tree: NodeRef) -> None:
        node = tree.node
        if not node.enable_spine_entity_pushdown_rewrite:
            return

        # cannot use the user_provided_spine_node_ref because there are various RenameCols on top of the UserSpecifiedDataNode
        if not isinstance(node, AsofJoinSawtoothAggNode):
            msg = f"Unhandled node type {node.__class__.__name__}"
            raise ValueError(msg)

        spine_to_use = node.spine_input_node
        user_provided_spine_node_ref = get_first_input_node_of_class(
            node.spine_input_node, UserSpecifiedDataNode
        ).as_ref()

        # Note: we can't simply using join keys to pushdown entity because wildcard FV can have a spine missing wildcard
        # key, so we need to check what exact entities are used in spine if wildcard key is present, and only push those
        # entities down.
        entities_to_push_down = node.fdw.join_keys
        if node.fdw.wildcard_join_key and node.fdw.wildcard_join_key not in user_provided_spine_node_ref.columns:
            entities_to_push_down = set(entities_to_push_down) - {node.fdw.wildcard_join_key}
        self.pushdown_entities(node.stream_input_node, spine_to_use.deepcopy(), list(entities_to_push_down))
        self.rewrite(node.batch_input_node)  # Batch input node contains a full agg node.

    def pushdown_entities(self, tree: NodeRef, spine: NodeRef, join_cols: List[str]) -> None:
        node = tree.node
        can_be_pushed_down = (
            RespectFeatureStartTimeNode,
            RenameColsNode,
            FeatureTimeFilterNode,
            AddAnchorTimeNode,
            AddDurationNode,
            AddEffectiveTimestampNode,
            PartialAggNode,
            StagingNode,
            ConvertTimestampToUTCNode,
            TextEmbeddingInferenceNode,
            AddAnchorTimeColumnsForSawtoothIntervalsNode,
            AddBooleanPartitionColumnsNode,
            UnionNode,
        )
        if isinstance(node, can_be_pushed_down):
            if isinstance(node, UnionNode):
                self.pushdown_entities(node.left, spine, join_cols)
                self.pushdown_entities(node.right, spine, join_cols)
            else:
                self.pushdown_entities(node.input_node, spine, join_cols)
        else:
            entities_node = SelectDistinctNode(node.dialect, node.compute_mode, spine, join_cols).as_ref()
            if isinstance(node, OfflineStoreScanNode) and node.compute_mode == ComputeMode.RIFT:
                entities_node = StagingNode(
                    dialect=node.dialect,
                    compute_mode=node.compute_mode,
                    input_node=entities_node,
                    staging_table_name="unique_entities",
                ).as_ref()
                tree.node = attrs.evolve(node, entity_filter=entities_node)

            else:
                tree.node = EntityFilterNode(node.dialect, node.compute_mode, node.as_ref(), entities_node, join_cols)


class SpineTimePushdown(Rewrite):
    """
    Adds time filter ranges based on the time limits of the spine.

    For example, if the spine in a fv.gffe() has time range [start, end], then the rewrite might apply that time range
    as a filter to any FeatureViewPipelineNodes, OfflineStoreScanNodes, or DataSourceScanNodes that are part of the
    feature data (with the appropriate modifications to the time range to account for factors such as batch schedule,
    data delay, etc.).
    """

    def __init__(self):
        # The spine time limits are the same for all spines used throughout the query, so we only calculate once.
        self.spine_time_limits: Optional[pendulum.Period] = None

    def rewrite(self, tree: NodeRef) -> None:
        if isinstance(tree.node, AsofJoinNode):
            self.rewrite_asof(tree)
        elif isinstance(tree.node, (AsofJoinFullAggNode, AsofJoinReducePartialAggNode)):
            self.rewrite_asof_full_agg(tree)
        elif isinstance(tree.node, AsofJoinSawtoothAggNode):
            self.rewrite_asof_sawtooth_agg(tree)
        else:
            for i in tree.inputs:
                self.rewrite(i)

    def rewrite_asof(self, tree: NodeRef) -> None:
        node = tree.node
        # In our current usage of the code, we always pass in the spine on the left side of the asof join.
        # This rewrite is still applicable for any type of dataframe on the left, but referring to it as spine
        # to make the naming match up with the aggregate case (in which the spine is not on the left).
        if self.spine_time_limits is None:
            cur_node = node.left_container.node.node
            self.spine_time_limits = _get_spine_time_limits(cur_node)

        self.pushdown_time_range(node.right_container.node, self.spine_time_limits)

    def rewrite_asof_full_agg(self, tree: NodeRef) -> None:
        """Computes the spine time limits and pushes them down to all relevant nodes in the partial aggregates."""
        node = tree.node

        if not node.enable_spine_time_pushdown_rewrite:
            return

        if self.spine_time_limits is None:
            self.spine_time_limits = _get_spine_time_limits(node)
        self.pushdown_time_range(node.partial_agg_node, self.spine_time_limits)

    def rewrite_asof_sawtooth_agg(self, tree: NodeRef) -> None:
        """Computes the spine time limits and pushes them down to all relevant nodes in the partial aggregates."""
        node = tree.node
        if not node.enable_spine_time_pushdown_rewrite:
            return
        if self.spine_time_limits is None:
            spine_node = node.spine_input_node
            self.spine_time_limits = _get_spine_time_limits(spine_node.node)

        # The stream part uses a smaller time range filter since it only needs data within the same day as the spine timestamp.
        # We look back 2 days to account for any continuous aggregations that do not use sawtoothing (aka < 2d aggs).
        self.pushdown_time_range(
            node.stream_input_node, self.spine_time_limits, look_back_duration=pendulum.duration(days=2)
        )
        # The batch part will use a larger filter containing the total ttl/aggregation window.
        self.rewrite(node.batch_input_node)

    # Push down and convert spine time filter to either raw data or feature time filter at the DataSourceScanNode or OfflineStoreScanNode.
    # Nodes that do not affect the correlation with the spine time range are enumerated in the can_be_pushed_down list.
    def pushdown_time_range(
        self, tree: NodeRef, spine_time_limits: pendulum.Period, look_back_duration: Optional[pendulum.Duration] = None
    ) -> None:
        node = tree.node
        can_be_pushed_down = (
            RespectFeatureStartTimeNode,
            RenameColsNode,
            PartialAggNode,
            FeatureTimeFilterNode,
            AddAnchorTimeNode,
            AddDurationNode,
            AddEffectiveTimestampNode,
            StagingNode,
            ConvertTimestampToUTCNode,
            AddAnchorTimeColumnsForSawtoothIntervalsNode,
            AddBooleanPartitionColumnsNode,
            UnionNode,
        )
        if isinstance(node, can_be_pushed_down):
            if isinstance(node, UnionNode):
                self.pushdown_time_range(node.left, spine_time_limits, look_back_duration=look_back_duration)
                self.pushdown_time_range(node.right, spine_time_limits, look_back_duration=look_back_duration)
            else:
                self.pushdown_time_range(node.input_node, spine_time_limits, look_back_duration=look_back_duration)
        elif isinstance(node, (OfflineStoreScanNode, FeatureViewPipelineNode)):
            if look_back_duration:
                feature_time_limits = time_utils.get_feature_data_time_limits_for_lookback(
                    fd=node.feature_definition_wrapper,
                    spine_time_limits=spine_time_limits,
                    max_lookback_duration=look_back_duration,
                )
            else:
                feature_time_limits = time_utils.get_feature_data_time_limits(
                    fd=node.feature_definition_wrapper, spine_time_limits=spine_time_limits
                )
            if isinstance(node, FeatureViewPipelineNode):
                # swap the pipeline node to add new time limits
                node = FeatureViewPipelineNode(
                    node.dialect,
                    node.compute_mode,
                    node.inputs_map,
                    node.feature_definition_wrapper,
                    feature_time_limits,
                    node.check_view_schema,
                    node.mock_context,
                )

                skew_config = None
                for n in node.inputs:
                    data_source_scan_node_ref = get_first_input_node_of_class(n, DataSourceScanNode, as_node_ref=True)
                    if data_source_scan_node_ref is None:
                        continue
                    data_source_scan_node = data_source_scan_node_ref.node
                    if data_source_scan_node is not None:
                        skew_config = data_source_scan_node.skew_config

                        # this method will convert aligned_feature_time_limits to raw data time limits by accounting for FilteredSource offsets etc.
                        data_time_filter = get_time_window_from_data_source_node(
                            feature_time_limits,
                            node.feature_definition_wrapper.batch_materialization_schedule,
                            data_source_scan_node.ds_node,
                            data_source_scan_node.skew_config,
                        )
                        if data_time_filter is not None:
                            data_source_scan_node_ref.node = attrs.evolve(
                                data_source_scan_node_ref.node,
                                start_time=data_time_filter.start,
                                end_time=data_time_filter.end,
                            )

                timestamp_field = (
                    node.feature_definition_wrapper.materialization_job_partition_timestamp
                    if _should_account_for_batch_publish_timestamp(
                        fdw=node.feature_definition_wrapper, skew_config=skew_config
                    )
                    else node.feature_definition_wrapper.timestamp_key
                )
                tree.node = FeatureTimeFilterNode(
                    dialect=node.dialect,
                    compute_mode=node.compute_mode,
                    input_node=ConvertTimestampToUTCNode.for_feature_definition(
                        node.dialect, node.compute_mode, node.feature_definition_wrapper, node.as_ref()
                    ),
                    feature_data_time_limits=feature_time_limits,
                    policy=node.feature_definition_wrapper.time_range_policy,
                    start_timestamp_field=timestamp_field,
                    end_timestamp_field=timestamp_field,
                )
            elif isinstance(node, OfflineStoreScanNode):
                tree.node = attrs.evolve(node, partition_time_filter=feature_time_limits)
                if node.skew_config is not None:
                    timestamp_field = (
                        node.feature_definition_wrapper.materialization_job_partition_timestamp
                        if _should_account_for_batch_publish_timestamp(
                            fdw=node.feature_definition_wrapper, skew_config=node.skew_config
                        )
                        else node.feature_definition_wrapper.timestamp_key
                    )
                    ftl_start, ftl_end = get_start_end_from_feature_time_limits(feature_time_limits, node.skew_config)
                    tree.node = FeatureTimeFilterNode(
                        dialect=node.dialect,
                        compute_mode=node.compute_mode,
                        input_node=ConvertTimestampToUTCNode.for_feature_definition(
                            node.dialect, node.compute_mode, node.feature_definition_wrapper, node.as_ref()
                        ),
                        feature_data_time_limits=pendulum.Period(
                            start=ftl_start,
                            end=ftl_end,
                        ),
                        policy=node.feature_definition_wrapper.time_range_policy,
                        start_timestamp_field=timestamp_field,
                        end_timestamp_field=timestamp_field,
                    )


# Mutates the input
def rewrite_tree_for_spine(tree: NodeRef) -> None:
    if not conf.get_bool("QUERY_REWRITE_ENABLED"):
        return
    rewrites = [SpineTimePushdown(), SpineEntityPushdown()]
    for rewrite in rewrites:
        rewrite.rewrite(tree)


def _get_spine_time_limits(cur_node: QueryNode) -> pendulum.Period:
    user_specified_data_node = get_first_input_node_of_class(cur_node.as_ref(), UserSpecifiedDataNode)
    if not user_specified_data_node:
        # We don't expect this to occur
        msg = "Expected spine to contain a UserSpecifiedDataNode, but it did not."
        raise ValueError(msg)
    timestamp_key = user_specified_data_node.metadata["timestamp_key"]
    data = user_specified_data_node.data
    if cur_node.compute_mode == ComputeMode.SPARK:
        limits = get_time_limits_of_spark_dataframe(data.to_spark(), timestamp_key)
    else:
        limits = get_time_limits_of_pandas_dataframe(data.to_pandas(), timestamp_key)
    if limits is None:
        msg = "Unable to infer the time range of the events dataframe. This typically occurs when all the timestamps in the dataframe are null."
        raise TectonValidationError(msg)
    return limits


def get_time_limits_of_spark_dataframe(df: "pyspark.sql.DataFrame", time_key: str) -> Optional[pendulum.Period]:
    from pyspark.sql import functions

    """The returned range is inclusive at the beginning & exclusive at the end: [start, end)."""
    # Fetch lower and upper time bound of the spine so that we can demand the individual feature definitions
    # to limit the amount of data they fetch from the raw data sources.
    # Returns None if df is empty.
    min_max_df = df.select(
        functions.min(df[time_key]).alias("time_start"), functions.max(df[time_key]).alias("time_end")
    )
    # convert to pandas in order to leverage Spark to pandas time conversion, which will produce the most
    # 'correct' timestamp / timezone conversion behavior for Spark users
    pd_min_max_df = min_max_df.toPandas()
    time_start = pd_min_max_df.loc[0]["time_start"]
    time_end = pd_min_max_df.loc[0]["time_end"]
    if pandas.isnull(time_start) or pandas.isnull(time_end):
        return None

    # Need to add 1 microsecond to the end time, since the range is exclusive at the end, and we need
    # to make sure to include the very last feature value (in terms of the event timestamp).
    return pendulum.instance(time_end.to_pydatetime()).add(microseconds=1) - pendulum.instance(
        time_start.to_pydatetime()
    )


def get_time_limits_of_pandas_dataframe(df: pandas.DataFrame, time_key: str) -> Optional[pendulum.Period]:
    time_start = df[time_key].min()
    time_end = df[time_key].max()
    if pandas.isnull(time_start) or pandas.isnull(time_end):
        return None
    # Need to add 1 microsecond to the end time, since the range is exclusive at the end, and we need
    # to make sure to include the very last feature value (in terms of the event timestamp).
    return pendulum.instance(time_end).add(microseconds=1) - pendulum.instance(time_start)
