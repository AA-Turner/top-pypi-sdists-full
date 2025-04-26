from tecton_core import conf
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.specs import TimeWindowSeriesSpec
from tecton_core.specs import create_time_window_spec_from_data_proto


def should_use_optimized_full_aggregate_node(qt_root: NodeRef) -> bool:
    """
    Decides whether to use optimized Full Aggregation algorithm (group-by based query) vs standard (window-based query).
    """
    if conf.get_or_none("DUCKDB_ENABLE_OPTIMIZED_FULL_AGG") is not None:
        # user enforced
        return conf.get_bool("DUCKDB_ENABLE_OPTIMIZED_FULL_AGG")

    full_agg_node = get_first_input_node_of_class(qt_root, AsofJoinFullAggNode)
    if not full_agg_node:
        return False

    if any(
        isinstance(create_time_window_spec_from_data_proto(feature.time_window), TimeWindowSeriesSpec)
        for feature in full_agg_node.fdw.fv_spec.aggregate_features
    ):
        # TimeWindowSeriesSpec is currently not supported by the optimized version
        return False

    return True
