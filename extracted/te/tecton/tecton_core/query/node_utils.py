import typing
from collections import deque
from typing import Deque
from typing import Dict
from typing import Optional
from typing import Union

import tecton_core.query.dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.node_interface import recurse_query_tree
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import StagingNode
from tecton_proto.args.transformation__client_pb2 import TransformationMode


def get_staging_nodes(
    qt_root: NodeRef, query_tree_step: QueryTreeStep, as_ref: bool = False
) -> Dict[str, Union[StagingNode, NodeRef]]:
    """Returns all StagingNodes in the query tree that belong to the specified QueryTreeStep."""
    # Note: can have the same staging node show up multiple times in the query tree. e.g. GHF(start/end time)
    staging_nodes = {}
    queue: Deque = deque()
    queue.append(qt_root)
    while len(queue) > 0:
        curr = queue.pop()
        curr_node = curr.node
        if isinstance(curr_node, StagingNode) and curr_node.query_tree_step == query_tree_step:
            staging_nodes[curr_node.staging_table_name_unique()] = curr_node if not as_ref else curr
            continue
        for child_node_ref in curr_node.inputs:
            queue.append(child_node_ref)
    return staging_nodes


def get_first_input_node_of_class(
    qt_root: NodeRef, node_class: type, as_node_ref: bool = False
) -> Union[QueryNode, NodeRef, None]:
    """Returns the first node in the query tree that is an instance of the specified class.

    Optionally returns the NodeRef instead of the QueryNode itself.
    """
    if isinstance(qt_root.node, node_class):
        return qt_root if as_node_ref else qt_root.node

    for child in qt_root.node.inputs:
        node = get_first_input_node_of_class(child, node_class, as_node_ref=as_node_ref)
        if node is not None:
            return node
    return None


def get_pipeline_dialect(qt_root: NodeRef) -> Optional[tecton_core.query.dialect.Dialect]:
    """Returns the dialect of the query tree. Raises an error if more than one dialect is present."""
    encountered_dialects = set()

    def _extract_dialect_from_fv(node: FeatureViewPipelineNode) -> None:
        nonlocal encountered_dialects
        transform_specs = node.feature_definition_wrapper.transformations
        for transform_spec in transform_specs:
            mode = transform_spec.transformation_mode
            if mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
                encountered_dialects.add(tecton_core.query.dialect.Dialect.PANDAS)
            elif mode == TransformationMode.TRANSFORMATION_MODE_SPARK_SQL:
                encountered_dialects.add(tecton_core.query.dialect.Dialect.SPARK)
            elif mode == TransformationMode.TRANSFORMATION_MODE_PYSPARK:
                encountered_dialects.add(tecton_core.query.dialect.Dialect.SPARK)
            elif mode == TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL:
                encountered_dialects.add(tecton_core.query.dialect.Dialect.SNOWFLAKE)
            elif mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
                encountered_dialects.add(tecton_core.query.dialect.Dialect.PANDAS)
            elif mode == TransformationMode.TRANSFORMATION_MODE_BIGQUERY_SQL:
                encountered_dialects.add(tecton_core.query.dialect.Dialect.BIGQUERY)

    recurse_query_tree(
        qt_root,
        lambda node: _extract_dialect_from_fv(node) if isinstance(node, FeatureViewPipelineNode) else None,
    )

    if len(encountered_dialects) > 1:
        msg = f"Rift does not support retrieving non-materialized features from Feature Views of different transformation modes {[dialect.value for dialect in encountered_dialects]}. Please ensure that at most one transformation mode is used by non-materialized Feature Views in your Feature Service."
        raise Exception(msg)

    if len(encountered_dialects) == 0:
        return None
    return encountered_dialects.pop()


def get_batch_data_sources(qt_root: NodeRef, cls: typing.Type[typing.Any]) -> typing.List[typing.Any]:
    """Returns all BatchSourceSpecs in all DataSourceScanNodes in the tree rooted at qt_root.

    Only BatchSourceSpec subclasses of the given cls are returned.
    """

    def _get_batch_data_sources(ref: NodeRef) -> typing.Iterator[typing.Any]:
        node = ref.node
        for node_input in node.inputs:
            yield from _get_batch_data_sources(node_input)
        if isinstance(node, DataSourceScanNode):
            batch = node.ds.batch_source
            if not batch:
                return
            if isinstance(batch, cls):
                yield batch

    return list(_get_batch_data_sources(qt_root))


def tree_contains(tree: NodeRef, node_type: typing.Type[QueryNode]) -> bool:
    """Returns True if the tree contains a NodeRef of the given type, False otherwise."""
    if isinstance(tree.node, node_type):
        return True

    return any(tree_contains(subtree, node_type) for subtree in tree.inputs)


def pipeline_has_odfvs(qt_root: NodeRef) -> bool:
    return get_first_input_node_of_class(qt_root, node_class=MultiOdfvPipelineNode) is not None


def pipeline_has_aggregations(qt_root: NodeRef) -> bool:
    return any(
        (
            get_first_input_node_of_class(qt_root, node_class=AsofJoinFullAggNode),
            get_first_input_node_of_class(qt_root, node_class=PartialAggNode),
        )
    )
