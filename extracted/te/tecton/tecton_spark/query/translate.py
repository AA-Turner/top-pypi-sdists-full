import sys
import typing

import attrs
import pandas

import tecton_core.query.dialect
from tecton_core.compute_mode import ComputeMode
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_pipeline_dialect
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
from tecton_core.query.nodes import CustomFilterNode
from tecton_core.query.nodes import DataNode
from tecton_core.query.nodes import DatasetScanNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import DeriveValidityPeriodNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import ExplodeEventsByTimestampAndSelectDistinctNode
from tecton_core.query.nodes import ExplodeTimestampByTimeWindowsNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import InnerJoinOnRangeNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import MultiRtfvFeatureExtractionNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import OnlineListAggNode
from tecton_core.query.nodes import OnlinePartialAggNodeV2
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import PythonDataNode
from tecton_core.query.nodes import RawDataSourceScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import TakeLastRowNode
from tecton_core.query.nodes import TemporalBatchTableFormatNode
from tecton_core.query.nodes import TrimValidityPeriodNode
from tecton_core.query.nodes import UnionNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.nodes import WildcardJoinNode
from tecton_core.schema import Schema
from tecton_core.schema_validation import arrow_schema_to_tecton_schema
from tecton_spark.query import data_source
from tecton_spark.query import filter
from tecton_spark.query import join
from tecton_spark.query import pipeline
from tecton_spark.query import projection
from tecton_spark.query.node import SparkExecNode
from tecton_spark.schema_spark_utils import schema_to_spark


if sys.version_info >= (3, 9):
    from typing import get_args
    from typing import get_origin
else:
    from typing_extensions import get_args
    from typing_extensions import get_origin

from typing import List
from typing import Optional

import pyspark

from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_spark import data_source_helper


# NOTE: use repr=False to avoid printing out the underlying dataframes when used in REPL/notebook.
@attrs.define(repr=False)
class SparkDataFrame(DataframeWrapper):
    _dataframe: pyspark.sql.DataFrame

    @property
    def columns(self) -> List[str]:
        return self._dataframe.columns

    def to_pandas(self) -> pandas.DataFrame:
        return self._dataframe.toPandas()

    @property
    def schema(self) -> Schema:
        from tecton_spark.vendor.pyspark.sql.pandas.types import to_arrow_schema

        arrow_schema = to_arrow_schema(self._dataframe.schema)
        return arrow_schema_to_tecton_schema(arrow_schema)

    def to_spark(self) -> pyspark.sql.DataFrame:
        return self._dataframe


def _convert_snowflake_feature_views_to_spark_dataframes(qt_root: NodeRef, spark: pyspark.sql.SparkSession) -> None:
    """Finds all FeatureViewPipelineNodes, executes their subtrees, and replaces them with DataNodes.

    Assumes that all FeatureViewPipelineNodes have Snowflake SQL.
    """
    snowflake_fv_node_ref = get_first_input_node_of_class(qt_root, FeatureViewPipelineNode, as_node_ref=True)
    while snowflake_fv_node_ref is not None:
        data_node = _execute_snowflake_fv(snowflake_fv_node_ref, spark)
        snowflake_fv_node_ref.node = data_node
        snowflake_fv_node_ref = get_first_input_node_of_class(qt_root, FeatureViewPipelineNode, as_node_ref=True)


def _execute_snowflake_fv(snowflake_fv_node_ref: NodeRef, spark: pyspark.sql.SparkSession) -> DataNode:
    """Executes the FeatureViewPipelineNode and its subtree. Returns the results as a DataNode."""
    fv_node = snowflake_fv_node_ref.node
    if fv_node is None:
        msg = "The query tree must contain a FeatureViewPipelineNode with Snowflake SQL."
        raise RuntimeError(msg)

    # We compile the subtree starting at the FeatureViewPipelineNode into a SQL query and then execute it.
    fv_node = fv_node.with_dialect(Dialect.SNOWFLAKE)
    sql_string = fv_node.to_sql(pretty_sql=True)

    fv_spec = fv_node.feature_definition_wrapper.fv_spec
    spark_schema = schema_to_spark(fv_spec.view_schema)

    ds_node = get_first_input_node_of_class(snowflake_fv_node_ref, DataSourceScanNode)
    if ds_node is None:
        msg = "The query tree must contain a DataSourceScanNode with a Snowflake data source."
        raise RuntimeError(msg)
    snowflake_spec = ds_node.ds.batch_source

    snowflake_df = data_source_helper.get_snowflake_dataframe(
        spark,
        url=snowflake_spec.url,
        database=snowflake_spec.database,
        schema=snowflake_spec.schema,
        warehouse=snowflake_spec.warehouse,
        query=sql_string,
        spark_schema=spark_schema,
    )

    return DataNode(Dialect.SPARK, ComputeMode.SPARK, SparkDataFrame(snowflake_df))


# convert from logical tree to physical tree
def _spark_convert(node_ref: NodeRef) -> SparkExecNode:
    logical_tree_node = node_ref.node
    node_mapping = {
        CustomFilterNode: filter.CustomFilterSparkNode,
        DataSourceScanNode: data_source.DataSourceScanSparkNode,
        DatasetScanNode: data_source.DatasetScanSparkNode,
        RawDataSourceScanNode: data_source.RawDataSourceScanSparkNode,
        MockDataSourceScanNode: data_source.MockDataSourceScanSparkNode,
        OfflineStoreScanNode: data_source.OfflineStoreScanSparkNode,
        FeatureViewPipelineNode: pipeline.PipelineEvalSparkNode,
        MultiOdfvPipelineNode: pipeline.MultiOdfvPipelineSparkNode,
        FeatureTimeFilterNode: filter.FeatureTimeFilterSparkNode,
        EntityFilterNode: filter.EntityFilterSparkNode,
        RespectTTLNode: filter.RespectTTLSparkNode,
        RespectFeatureStartTimeNode: filter.RespectFeatureStartTimeSparkNode,
        AddAnchorTimeNode: projection.AddAnchorTimeSparkNode,
        AddRetrievalAnchorTimeNode: projection.AddRetrievalAnchorTimeSparkNode,
        StreamWatermarkNode: filter.StreamWatermarkSparkNode,
        UserSpecifiedDataNode: data_source.UserSpecifiedDataSparkNode,
        DataNode: data_source.DataSparkNode,
        PartialAggNode: pipeline.PartialAggSparkNode,
        JoinNode: join.JoinSparkNode,
        WildcardJoinNode: join.WildcardJoinSparkNode,
        AsofJoinNode: join.AsofJoinSparkNode,
        AsofJoinFullAggNode: join.AsofJoinFullAggSparkNode,
        AsofSecondaryKeyExplodeNode: join.AsofSecondaryKeyExplodeSparkNode,
        RenameColsNode: projection.RenameColsSparkNode,
        SelectDistinctNode: projection.SelectDistinctSparkNode,
        ConvertEpochToTimestampNode: projection.ConvertEpochToTimestampSparkNode,
        ConvertTimestampToUTCNode: projection.ConvertTimestampToUTCSparkNode,
        AddEffectiveTimestampNode: projection.AddEffectiveTimestampSparkNode,
        MetricsCollectorNode: pipeline.MetricsCollectorSparkNode,
        AddDurationNode: projection.AddDurationSparkNode,
        AggregationSecondaryKeyRollupNode: join.AggregationSecondaryKeyRollupSparkNode,
        AggregationSecondaryKeyExplodeNode: projection.AggregationSecondaryKeyExplodeSparkNode,
        StagingNode: pipeline.StagingSparkNode,
        AddUniqueIdNode: projection.AddUniqueIdSparkNode,
        PythonDataNode: pipeline.PythonDataSparkNode,
        InnerJoinOnRangeNode: join.InnerJoinOnRangeSparkNode,
        OnlinePartialAggNodeV2: pipeline.OnlinePartialAggSparkNodeV2,
        OnlineListAggNode: pipeline.OnlineListAggSparkNode,
        TakeLastRowNode: join.TakeLastRowSparkNode,
        TemporalBatchTableFormatNode: join.TemporalBatchTableFormatSparkNode,
        ExplodeTimestampByTimeWindowsNode: join.ExplodeTimestampByTimeWindowsSparkNode,
        DeriveValidityPeriodNode: projection.DeriveValidityPeriodSparkNode,
        TrimValidityPeriodNode: filter.TrimValidityPeriodSparkNode,
        AddAnchorTimeColumnsForSawtoothIntervalsNode: projection.AddAnchorTimeColumnsForSawtoothIntervalsSparkNode,
        ExplodeEventsByTimestampAndSelectDistinctNode: projection.ExplodeEventsByTimestampAndSelectDistinctSparkNode,
        AddBooleanPartitionColumnsNode: projection.AddBooleanPartitionColumnsSparkNode,
        AdjustAnchorTimeToWindowEndNode: projection.AdjustAnchorTimeToWindowEndSparkNode,
        AsofJoinSawtoothAggNode: join.AsofJoinSawtoothAggSparkNode,
        AsofJoinReducePartialAggNode: join.AsofJoinReducePartialAggSparkNode,
        UnionNode: join.UnionSparkNode,
        MultiRtfvFeatureExtractionNode: projection.MultiRtfvFeatureExtractionSparkNode,
        AsofBitemporalJoinFullAggNode: join.AsofBitemporalJoinFullAggSparkNode,
    }

    if logical_tree_node.__class__ in node_mapping:
        return node_mapping[logical_tree_node.__class__].from_query_node(logical_tree_node)

    msg = f"TODO: mapping for {logical_tree_node.__class__}"
    raise Exception(msg)


def spark_convert(qt_root: NodeRef, spark: Optional[pyspark.sql.SparkSession] = None) -> SparkExecNode:
    pipeline_dialect = get_pipeline_dialect(qt_root)
    if pipeline_dialect == tecton_core.query.dialect.Dialect.DUCKDB:
        msg = "Tecton on Spark does not support DuckDB."
        raise RuntimeError(msg)

    if pipeline_dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
        if spark is None:
            msg = "A SparkSession is required in order to convert this query tree. It is required to eagerly execute the Snowflake transformations."
            raise RuntimeError(msg)
        _convert_snowflake_feature_views_to_spark_dataframes(qt_root, spark)

    return _spark_convert(qt_root)


def attrs_spark_converter(
    attrs_inst: typing.Any,  # noqa: ANN401
    attr: attrs.Attribute,
    item: typing.Any,  # noqa: ANN401
) -> typing.Any:  # noqa: ANN401
    """
    This converts a NodeRef into a SparkNode if it's a NodeRef.
    """
    # Check if type is a typing wrapper.
    if get_origin(attr.type) is not None:
        if get_origin(attr.type) == typing.Union and NodeRef in get_args(attr.type) and isinstance(item, NodeRef):
            return _spark_convert(item)
        elif get_origin(attr.type) is dict and NodeRef == get_args(attr.type)[1]:
            return {k: _spark_convert(v) for k, v in item.items()}
        return item
    if attr.type == NodeRef:
        return _spark_convert(item)
    if attr.type == AsofJoinInputContainer:
        return join.AsofJoinInputSparkContainer(
            **attrs.asdict(item, value_serializer=attrs_spark_converter, recurse=False)
        )
    return item
