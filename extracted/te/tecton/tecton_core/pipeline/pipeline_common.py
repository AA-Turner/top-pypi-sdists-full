import functools
import operator
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

import pandas

import tecton_core.tecton_pendulum as pendulum
from tecton_core import errors
from tecton_core import time_utils
from tecton_core.filter_utils import UNBOUNDED_FUTURE_TIMESTAMP
from tecton_core.filter_utils import FilterDateTime
from tecton_core.filter_utils import TectonTimeConstant
from tecton_core.id_helper import IdHelper
from tecton_core.skew_config import SkewConfig
from tecton_proto.args.pipeline__client_pb2 import ConstantNode
from tecton_proto.args.pipeline__client_pb2 import DataSourceNode as DataSourceNodeProto
from tecton_proto.args.pipeline__client_pb2 import Input as InputProto
from tecton_proto.args.pipeline__client_pb2 import Pipeline
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.args.pipeline__client_pb2 import RequestContext as RequestContextProto
from tecton_proto.args.pipeline__client_pb2 import RequestDataSourceNode
from tecton_proto.args.pipeline__client_pb2 import TransformationNode


CONSTANT_TYPE = Optional[Union[str, int, float, bool]]
CONSTANT_TYPE_OBJECTS = (str, int, float, bool)


def _make_mode_to_type() -> Dict[str, Any]:
    lookup: Dict[str, Any] = {
        "pandas": pandas.DataFrame,
        "python": Dict,
        "pipeline": PipelineNode,
        "spark_sql": str,
        "snowflake_sql": str,
    }
    try:
        # The `pyspark.sql.connect.*` classes are the default for the Notebooks on Databricks Shared Access Mode
        # Clusters of Version 14.3 or higher. That's why we need to support them.
        from pyspark.sql import DataFrame

        try:
            from pyspark.sql.connect.session import DataFrame as ConnectDataFrame
        except ImportError:
            ConnectDataFrame = DataFrame

        lookup["pyspark"] = (DataFrame, ConnectDataFrame)
    except ImportError:
        pass
    return lookup


MODE_TO_TYPE_LOOKUP: Dict[str, Any] = _make_mode_to_type()


def constant_node_to_value(constant_node: ConstantNode) -> CONSTANT_TYPE:
    if constant_node.HasField("string_const"):
        return constant_node.string_const
    elif constant_node.HasField("int_const"):
        return int(constant_node.int_const)
    elif constant_node.HasField("float_const"):
        return float(constant_node.float_const)
    elif constant_node.HasField("bool_const"):
        return constant_node.bool_const
    elif constant_node.HasField("null_const"):
        return None
    msg = f"Unknown ConstantNode type: {constant_node}"
    raise KeyError(msg)


def get_keyword_inputs(transformation_node: TransformationNode) -> Dict[str, InputProto]:
    """Returns the keyword inputs of transformation_node in a dict."""
    return {
        node_input.arg_name: node_input for node_input in transformation_node.inputs if node_input.HasField("arg_name")
    }


def positional_inputs(transformation_node: TransformationNode) -> List[InputProto]:
    """Returns the positional inputs of transformation_node in order."""
    return [node_input for node_input in transformation_node.inputs if node_input.HasField("arg_index")]


def check_transformation_type(
    object_name: str,
    result: Any,  # noqa: ANN401
    mode: str,
    supported_modes: List[str],
) -> None:
    possible_mode = None
    for candidate_mode, candidate_type in MODE_TO_TYPE_LOOKUP.items():
        if isinstance(result, candidate_type):
            possible_mode = candidate_mode
            break
    expected_type = MODE_TO_TYPE_LOOKUP[mode]
    actual_type = type(result)

    if isinstance(result, expected_type):
        return
    elif possible_mode is not None and possible_mode in supported_modes:
        msg = f"Transformation function {object_name} with mode '{mode}' is expected to return result with type {expected_type}, but returns result with type {actual_type} instead. Did you mean to set mode='{possible_mode}'?"
        raise TypeError(msg)
    else:
        msg = f"Transformation function {object_name} with mode {mode} is expected to return result with type {expected_type}, but returns result with type {actual_type} instead."
        raise TypeError(msg)


def get_start_end_from_feature_time_limits(
    feature_time_limits: pendulum.Period, skew_config: Optional[SkewConfig]
) -> Tuple[Optional[pendulum.datetime], Optional[pendulum.datetime]]:
    ftl_start = feature_time_limits.start if feature_time_limits is not None else None
    ftl_end = feature_time_limits.end if feature_time_limits is not None else None

    if skew_config is None:
        return ftl_start, ftl_end

    simulate_offline_store_materialized_until = (
        pendulum.instance(skew_config.simulate_offline_store_materialized_until)
        if skew_config.simulate_offline_store_materialized_until is not None
        else None
    )

    if (
        simulate_offline_store_materialized_until is not None
        and ftl_start is not None
        and simulate_offline_store_materialized_until < ftl_start
    ):
        msg = f"Invalid simulate_offline_store_materialized_until: {simulate_offline_store_materialized_until} is before the feature_time_limits start time: {ftl_start}."
        raise ValueError(msg)

    if skew_config.simulate_events_published_on_time:
        # if simulate_offline_store_materialized_until is None, it will be unbounded
        return ftl_start, simulate_offline_store_materialized_until or UNBOUNDED_FUTURE_TIMESTAMP
    else:
        return ftl_start, simulate_offline_store_materialized_until or ftl_end


def get_time_window_from_data_source_node(
    feature_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: DataSourceNodeProto,
    skew_config: Optional[SkewConfig],
) -> Optional[pendulum.Period]:
    using_select_range = data_source_node.HasField("filter_start_time") or data_source_node.HasField("filter_end_time")
    if using_select_range:
        start_date_time = FilterDateTime.from_proto(data_source_node.filter_start_time)
        end_date_time = FilterDateTime.from_proto(data_source_node.filter_end_time)

        # During Offline Retrieval with a spine, we pass None as the feature_time_limits and the Filter is later
        # applied as part of the Query Tree Rewrite
        if (
            start_date_time.is_materialization_limit() or end_date_time.is_materialization_limit()
        ) and feature_time_limits is None:
            return None

        # Unfiltered
        if start_date_time.is_unbounded_limit() and end_date_time.is_unbounded_limit():
            return None

        ftl_start, ftl_end = get_start_end_from_feature_time_limits(feature_time_limits, skew_config)

        new_start = start_date_time.to_datetime(exact_reference_start=ftl_start, exact_reference_end=ftl_end)
        new_end = end_date_time.to_datetime(exact_reference_start=ftl_start, exact_reference_end=ftl_end)

        if new_start and new_end and new_start > new_end:
            msg = f"Invalid Data Source Filter for {data_source_node.input_name}: start_time is after end_time. Please check your arguments to `select_range()`."
            raise ValueError(msg)

        raw_data_limits = pendulum.Period(new_start, new_end)

    # TODO(ajeya): Remove this block once we have fully migrated to `select_range` and removed FilteredSource
    else:
        if data_source_node.HasField("window") and feature_time_limits:
            new_start = feature_time_limits.start - time_utils.proto_to_duration(data_source_node.window)
            if schedule_interval:
                new_start = new_start + schedule_interval
            raw_data_limits = pendulum.Period(new_start, feature_time_limits.end)
        elif data_source_node.HasField("window_unbounded_preceding") and feature_time_limits:
            raw_data_limits = pendulum.Period(pendulum.datetime(1970, 1, 1), feature_time_limits.end)
        elif data_source_node.HasField("start_time_offset") and feature_time_limits:
            new_start = feature_time_limits.start + time_utils.proto_to_duration(data_source_node.start_time_offset)
            raw_data_limits = pendulum.Period(new_start, feature_time_limits.end)
        elif data_source_node.HasField("window_unbounded"):
            raw_data_limits = None
        else:
            # no data_source_override has been set
            raw_data_limits = feature_time_limits

    return raw_data_limits


# TODO(jiadong): Consolidate this method with `get_request_context_node` as they share similar functionality. Need to migrate off all usages of this method first.
def find_request_context(node: PipelineNode) -> Optional[RequestContextProto]:
    """Returns the request context for the pipeline. Assumes there is at most one RequestContext."""
    if node.HasField("request_data_source_node"):
        return node.request_data_source_node.request_context
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            rc = find_request_context(child.node)
            if rc is not None:
                return rc
    elif node.HasField("join_inputs_node"):
        for node in node.join_inputs_node.nodes:
            rc = find_request_context(node)
            if rc is not None:
                return rc
    return None


def get_input_name_to_ds_id_map(pipeline: Pipeline) -> Dict[str, str]:
    """Return a map from input name to data source id for the pipeline."""
    data_source_nodes = get_all_data_source_nodes(pipeline)
    return {
        node.data_source_node.input_name: IdHelper.to_string(node.data_source_node.virtual_data_source_id)
        for node in data_source_nodes
    }


def get_request_context_node(pipeline: Pipeline) -> Optional[RequestDataSourceNode]:
    """Returns the request_data_source_node for the pipeline. Assumes there is at most one RequestContext."""
    rc_node = [node for node in get_all_pipeline_nodes(pipeline.root) if node.HasField("request_data_source_node")]

    if len(rc_node) == 0:
        return None
    elif len(rc_node) == 1:
        return rc_node[0].request_data_source_node
    else:
        msg = "ODFV is not supposed to have more than 1 request_data_source_node"
        raise errors.TectonValidationError(msg)


def get_all_feature_view_nodes(pipeline: Pipeline) -> List[PipelineNode]:
    """Returns all feature view nodes from the provided pipeline."""
    return [node for node in get_all_pipeline_nodes(pipeline.root) if node.HasField("feature_view_node")]


def get_all_data_source_nodes(pipeline: Pipeline) -> List[PipelineNode]:
    """Returns all data source nodes from the provided pipeline."""
    return [node for node in get_all_pipeline_nodes(pipeline.root) if node.HasField("data_source_node")]


def get_all_pipeline_nodes(node: PipelineNode) -> List[PipelineNode]:
    """Returns all data source nodes from the provided node."""
    if node.HasField("transformation_node"):
        return functools.reduce(
            operator.iadd, [get_all_pipeline_nodes(input.node) for input in node.transformation_node.inputs], []
        )
    elif node.HasField("join_inputs_node"):
        return functools.reduce(
            operator.iadd, [get_all_pipeline_nodes(input_node) for input_node in node.join_inputs_node.nodes], []
        )
    else:
        return [node]


def get_all_input_keys(node: PipelineNode) -> Set[str]:
    names_set = set()
    _get_all_input_keys_helper(node, names_set)
    return names_set


def _get_all_input_keys_helper(node: PipelineNode, names_set: Set[str]) -> Set[str]:
    if node.HasField("request_data_source_node"):
        names_set.add(node.request_data_source_node.input_name)
    elif node.HasField("data_source_node"):
        names_set.add(node.data_source_node.input_name)
    elif node.HasField("feature_view_node"):
        names_set.add(node.feature_view_node.input_name)
    elif node.HasField("context_node"):
        names_set.add(node.context_node.input_name)
    elif node.HasField("join_inputs_node"):
        for node in node.join_inputs_node.nodes:
            _get_all_input_keys_helper(node, names_set)
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _get_all_input_keys_helper(child.node, names_set)
    return names_set


def get_fco_ids_to_input_keys(node: PipelineNode) -> Dict[str, str]:
    names_dict = {}
    _get_fco_ids_to_input_keys_helper(node, names_dict)
    return names_dict


def _get_fco_ids_to_input_keys_helper(node: PipelineNode, names_dict: Dict[str, str]) -> Dict[str, str]:
    if node.HasField("request_data_source_node"):
        # request data sources don't have fco ids
        pass
    elif node.HasField("data_source_node"):
        ds_node = node.data_source_node
        names_dict[IdHelper.to_string(ds_node.virtual_data_source_id)] = ds_node.input_name
    elif node.HasField("feature_view_node"):
        fv_node = node.feature_view_node
        names_dict[IdHelper.to_string(fv_node.feature_view_id)] = fv_node.input_name
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _get_fco_ids_to_input_keys_helper(child.node, names_dict)
    elif node.HasField("join_inputs_node"):
        for node in node.join_inputs_node.nodes:
            _get_fco_ids_to_input_keys_helper(node, names_dict)
    return names_dict


def uses_realtime_context(node: PipelineNode) -> bool:
    """Returns true if a Transformation with a RealtimeContext input exists in the Pipeline, or if a rtfv without a transformation has a RealtimeContext input"""
    if node.HasField("context_node"):
        return True
    elif node.HasField("transformation_node"):
        return any(uses_realtime_context(child.node) for child in node.transformation_node.inputs)
    elif node.HasField("join_inputs_node"):
        return any(uses_realtime_context(child) for child in node.join_inputs_node.nodes)


def is_filtered_datasource(node: PipelineNode) -> bool:
    """Returns true if a DataSourceNode is filtered according to the MaterializationLimits"""
    if not node.HasField("data_source_node"):
        return False

    if not node.data_source_node.HasField("filter_start_time") or not node.data_source_node.HasField("filter_end_time"):
        return False

    filter_start_time = FilterDateTime.from_proto(node.data_source_node.filter_start_time)
    filter_end_time = FilterDateTime.from_proto(node.data_source_node.filter_end_time)

    return (
        filter_start_time.time_reference == TectonTimeConstant.MATERIALIZATION_START_TIME
        and filter_start_time.offset == timedelta(0)
        and filter_end_time.time_reference == TectonTimeConstant.MATERIALIZATION_END_TIME
        and filter_end_time.offset == timedelta(0)
    )
