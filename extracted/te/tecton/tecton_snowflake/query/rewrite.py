from tecton_core.query import node_interface
from tecton_core.query import nodes
from tecton_core.query import rewrite
from tecton_snowflake.query import nodes as snowflake_nodes


class SnowflakeRewrite(rewrite.Rewrite):
    """
    Replace with Snowflake specific node.
    """

    node_mapping = {
        nodes.PartialAggNode: snowflake_nodes.PartialAggSnowflakeNode,
        nodes.AsofJoinFullAggNode: snowflake_nodes.AsofJoinFullAggSnowflakeNode,
    }

    def rewrite(self, tree: node_interface.NodeRef) -> node_interface.NodeRef:
        for i in tree.inputs:
            self.rewrite(i)
        if tree.node.__class__ in self.node_mapping:
            tree.node = self.node_mapping[tree.node.__class__].from_query_node(tree.node)
