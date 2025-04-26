import attrs
import pandas

from tecton_athena.athena_session import AthenaSession
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import tree_contains
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.pandas.node import ArrowExecNode
from tecton_core.query.pandas.node import SqlExecNode
from tecton_core.query.pandas.nodes import PandasMultiOdfvPipelineNode
from tecton_core.query.pandas.nodes import PandasRenameColsNode
from tecton_core.query.pandas.sql import SqlExecutor


@attrs.frozen
class AthenaSqlExecutor(SqlExecutor):
    session: AthenaSession

    def read_sql(self, sql: str) -> pandas.DataFrame:
        pandas_df = self.session.read_sql(sql)
        return pandas_df


# Converts a logical querytree to a physical Athena querytree by converting the RenameColsNodes and
# MultiOdfvPipelineNode at the top of the tree to ArrowExecNodes and the input node directly below these nodes to an
# Athena SqlExecNode that will execute the SQL in an Athena session. The requirement here is that ODFVPipelineNodes will
# not appear in a middle of a querytree and will only ever appear at the top of the querytree.
def athena_convert(node_ref: NodeRef, sql_executor: AthenaSqlExecutor, pretty_sql: bool) -> ArrowExecNode:
    if tree_contains(node_ref, MultiOdfvPipelineNode):
        return _convert_to_pandas_nodes(node_ref, sql_executor, pretty_sql)
    else:
        return SqlExecNode.from_sql_inputs(node_ref.node, sql_executor, pretty_sql)


def _convert_to_pandas_nodes(tree: NodeRef, sql_executor, pretty_sql: bool):
    # Recurses over RenameColsNodes and MultiOdfvPipelineNode at the top of the tree and converts them to
    # ArrowExecNodes and converts only the node immediately below these nodes to a SqlExecNode
    logical_tree_node = tree.node
    node_mapping = {
        MultiOdfvPipelineNode: PandasMultiOdfvPipelineNode,
        RenameColsNode: PandasRenameColsNode,
    }
    if logical_tree_node.__class__ in node_mapping:
        input_node = _convert_to_pandas_nodes(logical_tree_node.input_node, sql_executor, pretty_sql)
        return node_mapping[logical_tree_node.__class__].from_node_inputs(logical_tree_node, input_node)
    else:
        return SqlExecNode.from_sql_inputs(logical_tree_node, sql_executor, pretty_sql)
