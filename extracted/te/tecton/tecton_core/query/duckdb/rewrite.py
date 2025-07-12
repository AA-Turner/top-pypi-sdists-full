from tecton_core.query import nodes
from tecton_core.query.duckdb import nodes as duckdb_nodes
from tecton_core.query.node_interface import NodeRef


class DuckDBTreeRewriter:
    node_mapping = {
        nodes.PartialAggNode: duckdb_nodes.PartialAggDuckDBNode,
        nodes.AsofJoinFullAggNode: duckdb_nodes.AsofJoinFullAggNodeDuckDBNode,
        nodes.AsofJoinNode: duckdb_nodes.AsofJoinDuckDBNode,
        nodes.OnlinePartialAggNodeV2: duckdb_nodes.OnlinePartialAggNodeV2DuckDBNode,
    }

    def rewrite(
        self,
        tree: NodeRef,
        use_optimized_full_agg: bool = False,
    ) -> None:
        for i in tree.inputs:
            self.rewrite(tree=i, use_optimized_full_agg=use_optimized_full_agg)
        tree_node = tree.node
        if isinstance(tree_node, nodes.AsofJoinFullAggNode) and use_optimized_full_agg:
            tree.node = duckdb_nodes.AsofJoinFullAggDuckDBNodeV2.from_query_node(tree_node)
        elif tree_node.__class__ in self.node_mapping:
            tree.node = self.node_mapping[tree_node.__class__].from_query_node(tree_node)
