"""
Frame tree building algorithm.

This module contains the logic to transform a flat list of frames of interest
into a hierarchical execution tree structure.
Equivalent to vscode/src/build-frame-tree.ts which is the original JS implementation.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def subtree_flushed_name(
    co_name: Optional[str],
    segment_count: Optional[int] = None,
) -> str:
    name = co_name or "<unknown>"
    if segment_count is not None and segment_count > 1:
        return f"[flushed segment] {name} +{segment_count - 1} more"
    return f"[flushed segment] {name}"


@dataclass
class ExecutionTreeNode:
    """
    Base class for execution tree nodes.

    Represents a single node in the execution tree, which could be a function call,
    SQL query, HTTP request, or other recorded event.
    """

    index: int
    type: str
    name: str
    frame_id: str
    children: List[ExecutionTreeNode] = field(default_factory=list)
    all_children_count: int = 0
    data: Dict[str, Any] = field(default_factory=dict)
    subtype: Optional[str] = None

    def dfs(self):
        """Depth-first traversal generator yielding this node and all descendants."""
        yield self
        for child in self.children:
            yield from child.dfs()


@dataclass
class ExecutionTreeInfo:
    """
    Top level container for the execution tree and associated metadata.
    """

    execution_tree_nodes: List[ExecutionTreeNode]
    total_execution_tree_node_count: int
    sql_queries: List[ExecutionTreeNode]
    outbound_http_requests: List[ExecutionTreeNode]
    background_jobs: List[ExecutionTreeNode]
    log_messages: List[ExecutionTreeNode]
    unattached_assignments: List[Dict[str, Any]] = field(default_factory=list)
    has_assignments: bool = False
    unclosed_node_count: int = 0
    unmatched_exit_count: int = 0


def is_assignment_frame(frame: Dict[str, Any]) -> bool:
    """Whether ``frame`` is a ``line_events`` assignment: a ``line`` event
    carrying ``assign: (variable, value)``."""
    if frame.get("event") != "line":
        return False
    assign = frame.get("assign")
    return isinstance(assign, (tuple, list)) and len(assign) == 2


def assignment_owner(
    open_frame_spans: List[ExecutionTreeNode], frame: Dict[str, Any]
) -> Optional[ExecutionTreeNode]:
    """The open call ``frame`` was assigned in, if this tree has it.

    An assignment carries the ``frame_id`` of the call (or resume) it ran
    in, which is the innermost open function call.
    """
    frame_id = frame.get("frame_id")
    if frame_id is None or not open_frame_spans:
        return None
    innermost = open_frame_spans[-1]
    return innermost if innermost.frame_id == frame_id else None


def calculate_all_children_count(node: ExecutionTreeNode) -> int:
    """
    Recursively calculate the total number of descendants for a node.

    Updates node.all_children_count in place and returns the count.
    """
    count = len(node.children)
    for child in node.children:
        count += calculate_all_children_count(child)
    node.all_children_count = count
    return count


def set_children_counts(nodes: List[ExecutionTreeNode]) -> None:
    """Set all_children_count for all nodes in the tree."""
    for node in nodes:
        calculate_all_children_count(node)


def renumber_indices(nodes: List[ExecutionTreeNode]) -> None:
    """
    Renumber node indices sequentially after postprocessing.

    After removing nodes during postprocessing, indices may have gaps.
    This function reassigns indices in DFS order starting from 0.
    """
    index = 0
    for root_node in nodes:
        for node in root_node.dfs():
            node.index = index
            index += 1


def total_execution_tree_node_count(nodes: List[ExecutionTreeNode]) -> int:
    """Calculate total number of nodes in the tree."""
    return sum(1 + node.all_children_count for node in nodes)


def collect_all_frame_ids(nodes: List[ExecutionTreeNode]) -> set[str]:
    """
    Collect all frame_ids from the tree (recursively).

    Used to filter metadata lists after postprocessing to ensure we only
    reference nodes that still exist in the final tree.
    """
    frame_ids = set()
    for root_node in nodes:
        for node in root_node.dfs():
            frame_ids.add(node.frame_id)
    return frame_ids


def filter_metadata_lists(
    execution_tree_nodes: List[ExecutionTreeNode],
    sql_queries: List[ExecutionTreeNode],
    outbound_http_requests: List[ExecutionTreeNode],
    background_jobs: List[ExecutionTreeNode],
    log_messages: List[ExecutionTreeNode],
) -> Dict[str, List[ExecutionTreeNode]]:
    """
    Filter metadata lists to only include nodes present in the final tree.

    After postprocessing removes subtrees (e.g., Django setup, urllib3),
    the metadata lists can contain references to nodes that no longer exist.
    This function filters them to match the final tree.
    """
    valid_frame_ids = collect_all_frame_ids(execution_tree_nodes)

    return {
        "sql_queries": [
            node for node in sql_queries if node.frame_id in valid_frame_ids
        ],
        "outbound_http_requests": [
            node for node in outbound_http_requests if node.frame_id in valid_frame_ids
        ],
        "background_jobs": [
            node for node in background_jobs if node.frame_id in valid_frame_ids
        ],
        "log_messages": [
            node for node in log_messages if node.frame_id in valid_frame_ids
        ],
    }


CALL_LIKE_FRAMES = [
    "django_request",
    "start_sql_query",
    "outbound_http_request",
    "start_test",
    "django_template_start",
    "background_job",
    "django_setup_start",
    "django_checks_start",
    "django_create_test_db_start",
]

RETURN_LIKE_FRAMES = [
    "django_response",
    "end_sql_query",
    "outbound_http_response",
    "end_test",
    "django_template_end",
    "background_job_end",
    "django_setup_end",
    "django_checks_end",
    "django_create_test_db_end",
]

LEAF_FRAMES = ["log_message", "subtree_flushed"]

RETURN_FRAME_EVENTS = ["return", "unwind", "yield"]
CALL_FRAME_EVENTS = ["call", "resume", "throw"]


def build_execution_tree(frames_of_interest: List[Dict[str, Any]]) -> ExecutionTreeInfo:
    """
    Build an execution tree from a flat list of frames of interest.

    Args:
        frames_of_interest: List of frame dictionaries from the trace

    Returns:
        ExecutionTreeInfo containing the tree structure and metadata
    """
    if not frames_of_interest:
        return ExecutionTreeInfo(
            execution_tree_nodes=[],
            total_execution_tree_node_count=0,
            sql_queries=[],
            outbound_http_requests=[],
            background_jobs=[],
            log_messages=[],
        )

    root_execution_tree_nodes: List[ExecutionTreeNode] = []
    current_ancestors: List[ExecutionTreeNode] = []
    open_frame_spans: List[ExecutionTreeNode] = []
    execution_tree_node_index = 0

    sql_queries: List[ExecutionTreeNode] = []
    outbound_http_requests: List[ExecutionTreeNode] = []
    background_jobs: List[ExecutionTreeNode] = []
    log_messages: List[ExecutionTreeNode] = []

    outbound_http_request_index = 0
    sql_query_index = 0
    log_message_index = 0
    five_hundred_exception: Optional[Dict[str, Any]] = None
    frame_id_mismatch_count = 0
    unattached_assignments: List[Dict[str, Any]] = []
    has_assignments = False
    unclosed_node_count = 0
    unmatched_exit_count = 0

    def close_innermost_without_exit(
        closed_at: Optional[float], at_trace_boundary: bool = False
    ) -> None:
        """Close the innermost open call, which has no exit event, and keep it
        (and everything recorded inside it) in the tree."""
        nonlocal unclosed_node_count, sql_query_index, outbound_http_request_index
        nonlocal five_hundred_exception
        node = current_ancestors.pop()
        if node.type == "frame_span":
            open_frame_spans.pop()
        parent = current_ancestors[-1] if current_ancestors else None
        close_without_exit(node, closed_at, at_trace_boundary)
        if node.data.get("exit_not_recorded"):
            unclosed_node_count += 1
        if node.type == "sql_query":
            node.data["index"] = sql_query_index
            sql_query_index += 1
            sql_queries.append(node)
        elif node.type == "outbound_http_request":
            if parent is None or parent.type != "outbound_http_request":
                node.data["index"] = outbound_http_request_index
                outbound_http_request_index += 1
                outbound_http_requests.append(node)
        elif node.type == "nested_background_job":
            background_jobs.append(node)
        elif node.type == "nested_served_http_request" and five_hundred_exception:
            node.data["five_hundred_exception"] = five_hundred_exception
            node.children, span_index = annotate_frame_spans_with_500_exception(
                node.children, five_hundred_exception
            )
            node.data["five_hundred_exception_frame_span_index"] = span_index
            five_hundred_exception = None
        if parent is None:
            root_execution_tree_nodes.append(node)

    frames_of_interest = preprocess_frames_of_interest(frames_of_interest)

    for frame_index, frame in enumerate(frames_of_interest):
        is_return_frame = "event" in frame and frame["event"] in RETURN_FRAME_EVENTS
        is_call_frame = "event" in frame and frame["event"] in CALL_FRAME_EVENTS

        frame_type = frame.get("type")
        is_call = is_call_frame or (frame_type and frame_type in CALL_LIKE_FRAMES)
        is_return = is_return_frame or (frame_type and frame_type in RETURN_LIKE_FRAMES)

        if is_call:
            current_tree_node = make_tree_node(frame, execution_tree_node_index)

            if not current_ancestors:
                current_ancestors.append(current_tree_node)
            else:
                current_parent = current_ancestors[-1]
                current_parent.children.append(current_tree_node)
                current_ancestors.append(current_tree_node)

            if current_tree_node.type == "frame_span":
                open_frame_spans.append(current_tree_node)
            execution_tree_node_index += 1

        elif is_return:
            if not current_ancestors:
                unmatched_exit_count += 1
                logger.warning(
                    f"Return frame with no corresponding call frame at index {frame_index}"
                )
                if frame_type == "django_response":
                    # Its 500 exception must not land on a later request.
                    five_hundred_exception = None
                continue

            # Missing events (plugin failure, process death, cut trace) are tolerated: keep what was
            # recorded rather than refusing to build the tree.
            expected_parent_type = get_expected_parent_type(frame)
            current_parent = current_ancestors[-1]
            if (
                current_parent.type == expected_parent_type
                and current_parent.frame_id == frame["frame_id"]
            ):
                match_index: Optional[int] = len(current_ancestors) - 1
            else:
                match_index = find_open_call(
                    current_ancestors, frame, expected_parent_type
                )
            if match_index is None:
                unmatched_exit_count += 1
                if frame_type == "django_response":
                    # Its 500 exception must not land on a later request.
                    five_hundred_exception = None
                logger.debug(
                    "Kolo: skipped an exit with no matching call at index %s\n%s",
                    frame_index,
                    stripped_frame_of_interest(frame),
                )
                continue
            if match_index != len(current_ancestors) - 1:
                closed_at = event_timestamp(frame)
                while len(current_ancestors) - 1 > match_index:
                    logger.debug(
                        "Kolo: call with no recorded exit: %s (%s)",
                        current_ancestors[-1].frame_id,
                        current_ancestors[-1].name,
                    )
                    close_innermost_without_exit(closed_at)

            current_parent = current_ancestors[-1]

            expected_frame_id = current_parent.frame_id
            actual_frame_id = frame["frame_id"]
            if expected_frame_id != actual_frame_id:
                frame_id_mismatch_count += 1
                # frame_mismatch_debug_info walks every frame: only pay once, as traces with dropped exits
                # can have tens of thousands of mismatches.
                if frame_id_mismatch_count == 1:
                    debug_info = frame_mismatch_debug_info(
                        current_parent, frame, frames_of_interest
                    )
                    logger.warning(
                        f"Kolo warning: frame_id mismatch. Expected {expected_frame_id} "
                        f"({current_parent.type}), got {actual_frame_id} ({frame_type})\n"
                        f"{debug_info}\n"
                        f"{debug_surrounding_frames_of_interest(frame_index, frames_of_interest)}"
                    )

            if is_return_frame:
                current_parent.data["return_frame"] = frame
            elif frame_type == "django_response":
                current_parent.data["response"] = frame

                if five_hundred_exception:
                    current_parent.data["five_hundred_exception"] = (
                        five_hundred_exception
                    )
                    annotated_children, exception_frame_span_index = (
                        annotate_frame_spans_with_500_exception(
                            current_parent.children, five_hundred_exception
                        )
                    )
                    current_parent.children = annotated_children
                    current_parent.data["five_hundred_exception_frame_span_index"] = (
                        exception_frame_span_index
                    )
                    five_hundred_exception = None

            elif frame_type == "end_sql_query":
                current_parent.data["index"] = sql_query_index
                sql_query_index += 1
                current_parent.name = frame_of_interest_name(frame)
                current_parent.data["query"] = frame["query"]
                current_parent.data["query_template"] = frame.get("query_template")
                current_parent.data["query_data"] = frame.get("query_data")
                current_parent.data["query_params"] = frame.get("query_params")
                current_parent.data["database"] = frame.get("database")
                current_parent.data["return_timestamp"] = frame["return_timestamp"]
                if frame.get("exception"):
                    current_parent.data["exception"] = frame["exception"]
                sql_queries.append(current_parent)

            elif frame_type == "outbound_http_response":
                current_parent.data["index"] = outbound_http_request_index
                outbound_http_request_index += 1
                current_parent.data["response"] = {
                    "body": frame.get("body"),
                    "headers": frame.get("headers"),
                    "timestamp": frame["timestamp"],
                    "status_code": frame["status_code"],
                }
                grandparent_index = len(current_ancestors) - 2
                if grandparent_index >= 0:
                    grandparent = current_ancestors[grandparent_index]
                    if grandparent.type != "outbound_http_request":
                        outbound_http_requests.append(current_parent)
                else:
                    outbound_http_requests.append(current_parent)

            elif frame_type == "end_test":
                current_parent.data["return_timestamp"] = frame["timestamp"]

            elif frame_type == "django_template_end":
                current_parent.data["return_timestamp"] = frame["timestamp"]
                current_parent.data["return_context"] = frame["context"]

            elif frame_type == "background_job_end":
                current_parent.data["return_timestamp"] = frame["timestamp"]
                background_jobs.append(current_parent)

            elif frame_type == "django_setup_end":
                current_parent.data["return_timestamp"] = frame["timestamp"]

            elif frame_type == "django_checks_end":
                current_parent.data["return_timestamp"] = frame["timestamp"]

            elif frame_type == "django_create_test_db_end":
                current_parent.data["return_timestamp"] = frame["timestamp"]

            else:
                raise ValueError(f"Unexpected return-like frame type: {frame_type}")

            completed_node = current_ancestors.pop()
            if completed_node.type == "frame_span":
                open_frame_spans.pop()
            if not current_ancestors:
                root_execution_tree_nodes.append(completed_node)

        elif frame_type and frame_type in LEAF_FRAMES:
            current_tree_node = make_tree_node(frame, execution_tree_node_index)

            if frame_type == "log_message":
                current_tree_node.data["index"] = log_message_index
                log_message_index += 1
                log_messages.append(current_tree_node)

            if current_ancestors:
                current_parent = current_ancestors[-1]
                current_parent.children.append(current_tree_node)
            else:
                root_execution_tree_nodes.append(current_tree_node)

            execution_tree_node_index += 1

        elif frame_type == "exception":
            five_hundred_exception = frame

        elif is_assignment_frame(frame):
            has_assignments = True
            owner = assignment_owner(open_frame_spans, frame)
            if owner is None:
                unattached_assignments.append(frame)
            else:
                owner.data.setdefault("assignments", []).append(frame)

    if current_ancestors:
        logger.debug(
            "Kolo: %s calls still open at the end of the trace",
            len(current_ancestors),
        )
        closed_at = last_event_timestamp(frames_of_interest)
        while current_ancestors:
            close_innermost_without_exit(closed_at, at_trace_boundary=True)

    if frame_id_mismatch_count > 1:
        logger.warning(
            f"Kolo warning: {frame_id_mismatch_count} frame_id mismatches in total"
        )

    execution_tree_nodes = postprocess_tree(root_execution_tree_nodes)
    renumber_indices(execution_tree_nodes)
    if unclosed_node_count:
        # Count what the tree shows: postprocessing removes some subtrees
        # (Django setup, nested module frames) whole.
        unclosed_node_count = sum(
            1
            for root in execution_tree_nodes
            for node in root.dfs()
            if node.data.get("exit_not_recorded")
        )
    set_children_counts(execution_tree_nodes)

    filtered_metadata = filter_metadata_lists(
        execution_tree_nodes,
        sql_queries,
        outbound_http_requests,
        background_jobs,
        log_messages,
    )

    return ExecutionTreeInfo(
        execution_tree_nodes=execution_tree_nodes,
        total_execution_tree_node_count=total_execution_tree_node_count(
            execution_tree_nodes
        ),
        sql_queries=filtered_metadata["sql_queries"],
        outbound_http_requests=filtered_metadata["outbound_http_requests"],
        background_jobs=filtered_metadata["background_jobs"],
        log_messages=filtered_metadata["log_messages"],
        unattached_assignments=unattached_assignments,
        has_assignments=has_assignments,
        unclosed_node_count=unclosed_node_count,
        unmatched_exit_count=unmatched_exit_count,
    )


def find_open_call(
    current_ancestors: List[ExecutionTreeNode],
    frame: Dict[str, Any],
    expected_parent_type: str,
) -> Optional[int]:
    """The index in ``current_ancestors`` of the open call that the exit
    ``frame`` closes, or None if it closes none of them.

    An exit closes the innermost open call. When that call's ``frame_id`` or
    type says otherwise, the open call with the exit's ``frame_id`` is the
    match: the calls inside it are missing their exits. An exit whose
    ``frame_id`` is not open at all is paired by position if the innermost
    open call has the right type (old traces did not always give a call and
    its exit the same id), and otherwise matches nothing.
    """
    innermost_index = len(current_ancestors) - 1
    innermost = current_ancestors[innermost_index]
    frame_id = frame.get("frame_id")
    innermost_has_type = innermost.type == expected_parent_type
    if innermost_has_type and innermost.frame_id == frame_id:
        return innermost_index
    for index in range(innermost_index - 1, -1, -1):
        candidate = current_ancestors[index]
        if candidate.frame_id == frame_id and candidate.type == expected_parent_type:
            return index
    if innermost_has_type:
        return innermost_index
    return None


def event_timestamp(frame: Dict[str, Any]) -> Optional[float]:
    """When ``frame`` was recorded: the latest of its timestamps (a plugin
    event has the tracer's and the plugin's own)."""
    values = [
        frame[key]
        for key in ("timestamp", "return_timestamp", "call_timestamp")
        if isinstance(frame.get(key), (int, float))
    ]
    return max(values) if values else None


def last_event_timestamp(frames: List[Dict[str, Any]]) -> Optional[float]:
    for frame in reversed(frames):
        timestamp = event_timestamp(frame)
        if timestamp is not None:
            return timestamp
    return None


def close_without_exit(
    node: ExecutionTreeNode,
    closed_at: Optional[float],
    at_trace_boundary: bool = False,
) -> None:
    """Give ``node``, a call the trace has no exit event for, the data its
    exit would have set, and mark it ``exit_not_recorded``.

    ``closed_at`` is the timestamp of the event that shows the call was over
    (its caller's exit), or of the last event when the trace ends first: the
    latest the call can have ended.
    """
    data = node.data
    if node.type == "outbound_http_request":
        data["response"] = None
        if at_trace_boundary:
            data["incomplete_at_trace_boundary"] = True
            return
        data["return_timestamp"] = closed_at
    elif node.type == "frame_span":
        call_frame = data["call_frame"]
        return_frame = {
            key: call_frame[key]
            for key in ("frame_id", "type", "path", "co_name", "qualname")
            if key in call_frame
        }
        if closed_at is None:
            closed_at = call_frame.get("timestamp")
        return_frame["timestamp"] = closed_at
        return_frame["exit_not_recorded"] = True
        data["return_frame"] = return_frame
    elif node.type == "nested_served_http_request":
        started_at = event_timestamp(data["request"])
        if closed_at is not None and started_at is not None:
            ms_duration = (closed_at - started_at) * 1000
        else:
            ms_duration = 0
        data["response"] = {
            "type": "django_response",
            "frame_id": node.frame_id,
            "timestamp": closed_at,
            "status_code": None,
            "content": None,
            "headers": {},
            "ms_duration": ms_duration,
            "exit_not_recorded": True,
        }
    else:
        if node.type == "sql_query":
            node.name = f"SQL query ({node.frame_id})"
            data["query"] = ""
            data["query_template"] = None
            data["query_data"] = None
            data["query_params"] = None
            data["database"] = None
        elif node.type == "django_template":
            data["return_context"] = None
        data["return_timestamp"] = closed_at
    data["exit_not_recorded"] = True


def frame_of_interest_name(frame: Dict[str, Any]) -> str:
    """Generate a human-readable name for a frame of interest."""
    frame_type = frame.get("type")

    if not frame_type or frame_type == "frame":
        qualname = frame.get("qualname")
        if qualname:
            return qualname
        path = frame["path"]
        co_name = frame["co_name"]
        return f"{path} {co_name}"

    elif frame_type in ("start_test", "end_test"):
        return frame["test_name"]

    elif frame_type in ("django_template_start", "django_template_end"):
        return frame["template"]

    elif frame_type == "django_request":
        method = frame["method"]
        path_info = frame["path_info"]
        return f"{method} {path_info}"

    elif frame_type == "log_message":
        msg = frame["msg"]
        return str(msg)[:50]

    elif frame_type == "end_sql_query":
        query = frame["query"]
        frame_id = frame["frame_id"]
        return f"{query} ({frame_id})"

    elif frame_type == "outbound_http_request":
        return frame["method_and_full_url"]

    elif frame_type in ("background_job", "background_job_end"):
        return frame["name"]

    elif frame_type == "subtree_flushed":
        co_name = frame["co_name"] if "co_name" in frame else None
        return subtree_flushed_name(co_name, frame.get("flushed_segment_count"))

    else:
        return frame_type


def make_tree_node(frame: Dict[str, Any], index: int) -> ExecutionTreeNode:
    """Create an ExecutionTreeNode from a frame of interest."""
    frame_type = frame.get("type")
    event = frame.get("event")

    base_data = {
        "index": index,
        "name": frame_of_interest_name(frame),
        "children": [],
        "all_children_count": 0,
        "frame_id": frame["frame_id"],
    }

    if event and event in CALL_FRAME_EVENTS:
        return ExecutionTreeNode(
            type="frame_span",
            data={"call_frame": frame},
            **base_data,
        )

    elif frame_type == "django_request":
        return ExecutionTreeNode(
            type="nested_served_http_request",
            data={"request": frame},
            **base_data,
        )

    elif frame_type == "start_sql_query":
        return ExecutionTreeNode(
            type="sql_query",
            data={
                "user_code_call_site": frame.get("user_code_call_site"),
                "call_timestamp": frame["call_timestamp"],
            },
            **base_data,
        )

    elif frame_type == "outbound_http_request":
        return ExecutionTreeNode(
            type="outbound_http_request",
            subtype=frame.get("subtype"),
            data={
                "request": {
                    "url": frame["url"],
                    "body": frame.get("body"),
                    "method": frame["method"],
                    "headers": frame.get("headers"),
                    "timestamp": frame["timestamp"],
                    "method_and_full_url": frame["method_and_full_url"],
                }
            },
            **base_data,
        )

    elif frame_type == "start_test":
        return ExecutionTreeNode(
            type="nested_test",
            data={
                "test_name": frame["test_name"],
                "test_class": frame["test_class"],
                "call_timestamp": frame["timestamp"],
            },
            **base_data,
        )

    elif frame_type == "django_template_start":
        return ExecutionTreeNode(
            type="django_template",
            data={
                "call_timestamp": frame["timestamp"],
                "template": frame["template"],
                "call_context": frame["context"],
            },
            **base_data,
        )

    elif frame_type == "background_job":
        return ExecutionTreeNode(
            type="nested_background_job",
            data={
                "call_timestamp": frame["timestamp"],
                "name": frame["name"],
                "args": frame["args"],
                "kwargs": frame["kwargs"],
                "subtype": frame["subtype"],
            },
            **base_data,
        )

    elif frame_type == "log_message":
        return ExecutionTreeNode(
            type="log_message",
            data={
                "level": frame["level"],
                "args": frame["args"],
                "extra": frame.get("extra"),
                "msg": frame["msg"],
                "stack": frame.get("stack"),
                "traceback": frame.get("traceback"),
                "name": frame.get("name"),
            },
            **base_data,
        )

    elif frame_type == "django_setup_start":
        return ExecutionTreeNode(type="django_setup", data={}, **base_data)

    elif frame_type == "django_checks_start":
        return ExecutionTreeNode(type="django_checks", data={}, **base_data)

    elif frame_type == "django_create_test_db_start":
        return ExecutionTreeNode(type="django_create_test_db", data={}, **base_data)

    elif frame_type == "subtree_flushed":
        co_name = frame["co_name"] if "co_name" in frame else None
        segment_count = frame.get("flushed_segment_count")
        base_data["name"] = subtree_flushed_name(co_name, segment_count)
        return ExecutionTreeNode(
            type="subtree_flushed",
            data={
                "co_name": co_name or "<unknown>",
                "flushed_trace_id": frame["flushed_trace_id"],
                "flushed_bytes": frame["flushed_bytes"],
                "flushed_segment_count": segment_count,
                "timestamp": frame["timestamp"],
            },
            **base_data,
        )

    else:
        raise ValueError(f"Unexpected frame type for node creation: {frame_type}")


def get_expected_parent_type(frame: Dict[str, Any]) -> str:
    """Determine what node type should be the parent of this return frame."""
    event = frame.get("event")
    frame_type = frame.get("type")

    if event and event in RETURN_FRAME_EVENTS:
        return "frame_span"

    if not frame_type:
        raise ValueError(f"Cannot determine expected parent for frame: {frame}")

    expected_parents = {
        "django_response": "nested_served_http_request",
        "end_sql_query": "sql_query",
        "outbound_http_response": "outbound_http_request",
        "end_test": "nested_test",
        "django_template_end": "django_template",
        "background_job_end": "nested_background_job",
        "django_setup_end": "django_setup",
        "django_checks_end": "django_checks",
        "django_create_test_db_end": "django_create_test_db",
    }

    if frame_type in expected_parents:
        return expected_parents[frame_type]

    raise ValueError(f"Cannot determine expected parent for frame type: {frame_type}")


def annotate_frame_spans_with_500_exception(
    nodes: List[ExecutionTreeNode],
    exception: Dict[str, Any],
) -> tuple[List[ExecutionTreeNode], Optional[int]]:
    """
    Annotate frame spans with 500 exception information.

    Returns the annotated nodes and the index of the bottom exception frame span.
    """
    original_nodes = nodes

    exception_frames = exception.get("exception_frames", [])
    if not exception_frames:
        return original_nodes, None

    exception_summary = exception.get("exception_summary", [])
    exception_message = exception_summary[-1] if exception_summary else ""

    for ex_index, exception_frame in enumerate(exception_frames):
        is_bottom = ex_index == len(exception_frames) - 1

        for node in nodes:
            if node.type != "frame_span":
                continue

            return_frame = node.data.get("return_frame", {})
            if return_frame.get("path") == exception_frame.get(
                "path"
            ) and return_frame.get("co_name") == exception_frame.get("co_name"):
                if is_bottom:
                    return_frame["exception"] = exception
                    return original_nodes, node.index
                else:
                    return_frame["annotatedExceptionMessage"] = exception_message

                nodes = node.children
                break

    return original_nodes, None


def remove_legacy_urllib_frames(frames: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove legacy urllib3.connectionpool.HTTPConnectionPool.urlopen frames."""
    return [
        frame
        for frame in frames
        if frame.get("qualname") != "urllib3.connectionpool.HTTPConnectionPool.urlopen"
    ]


def remove_legacy_background_job_frames(
    frames: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Remove legacy background job frames."""
    background_job_count = sum(1 for f in frames if f.get("type") == "background_job")
    background_job_end_count = sum(
        1 for f in frames if f.get("type") == "background_job_end"
    )

    if background_job_count > 0 and background_job_end_count == 0:
        return [frame for frame in frames if frame.get("type") != "background_job"]

    return [
        frame
        for frame in frames
        if frame.get("qualname") != "celery.app.task.Task.apply_async"
    ]


def remove_empty_sql_queries(frames: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove SQL query pairs where the query is None."""
    # Other events can be recorded between start and end (library frames compiling the query),
    # so pair each end with its own start rather than the previous event.
    open_starts: List[int] = []
    removed = set()
    for index, frame in enumerate(frames):
        frame_type = frame.get("type")
        if frame_type == "start_sql_query":
            open_starts.append(index)
        elif frame_type == "end_sql_query":
            start_index = None
            for position in range(len(open_starts) - 1, -1, -1):
                if frames[open_starts[position]].get("frame_id") == frame.get(
                    "frame_id"
                ):
                    start_index = open_starts.pop(position)
                    break
            else:
                if open_starts:
                    start_index = open_starts.pop()
            if frame.get("query") is None:
                removed.add(index)
                if start_index is not None:
                    removed.add(start_index)
                    if index == start_index + 2:
                        removed.add(start_index + 1)
    if not removed:
        return frames
    return [frame for index, frame in enumerate(frames) if index not in removed]


def preprocess_frames_of_interest(frames: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply all preprocessing transformations to frames."""
    frames = remove_legacy_urllib_frames(frames)
    frames = remove_legacy_background_job_frames(frames)
    frames = remove_empty_sql_queries(frames)
    return frames


def merge_duplicate_roots(nodes: List[ExecutionTreeNode]) -> List[ExecutionTreeNode]:
    """Merge root nodes that share the same frame_id.

    In trace point captures, both the CALL and RETURN frames for the root
    function can appear as separate root-level entries.  The tree builder
    creates two root nodes from them.  This function merges consecutive roots
    that share the same ``frame_id`` into a single node, keeping the first
    node's data and adopting the second node's children.
    """
    if len(nodes) <= 1:
        return nodes

    merged: List[ExecutionTreeNode] = []

    for node in nodes:
        # Merge only consecutive duplicate roots: a flush's placeholder/restore pair lands adjacent;
        # non-consecutive roots sharing a frame_id are distinct.
        if merged and merged[-1].frame_id == node.frame_id:
            existing = merged[-1]
            existing.children.extend(node.children)
            for key, value in node.data.items():
                if key not in existing.data:
                    existing.data[key] = value
                elif key == "assignments":
                    existing.data[key].extend(value)
        else:
            merged.append(node)

    return merged


def postprocess_tree(nodes: List[ExecutionTreeNode]) -> List[ExecutionTreeNode]:
    """Apply postprocessing transformations to the tree."""
    nodes = merge_duplicate_roots(nodes)
    nodes = remove_django_setup_subtrees(nodes)
    nodes = remove_module_frames(nodes)
    remove_superfluous_urllib3_frames(nodes)
    return nodes


def remove_django_setup_subtrees(
    nodes: List[ExecutionTreeNode],
) -> List[ExecutionTreeNode]:
    """Remove django_setup, django_checks, and django_create_test_db subtrees."""
    remove_types = ["django_setup", "django_checks", "django_create_test_db"]

    result = []
    for node in nodes:
        if node.type in remove_types:
            continue

        node.children = remove_django_setup_subtrees(node.children)
        result.append(node)

    return result


def remove_module_frames(nodes: List[ExecutionTreeNode]) -> List[ExecutionTreeNode]:
    """
    Remove nested module frames (where co_name is '<module>') and their children.

    Root-level frames are preserved (including __main__.<module>), but nested
    module frames from library imports are removed.
    """
    result = []
    for node in nodes:
        node.children = _remove_nested_module_frames(node.children)
        result.append(node)

    return result


def _remove_nested_module_frames(
    nodes: List[ExecutionTreeNode],
) -> List[ExecutionTreeNode]:
    """Helper function to remove module frames at non-root levels."""
    result = []
    for node in nodes:
        if node.type == "frame_span":
            call_frame = node.data.get("call_frame", {})
            if call_frame.get("co_name") == "<module>":
                continue

        node.children = _remove_nested_module_frames(node.children)
        result.append(node)

    return result


def remove_superfluous_urllib3_frames(nodes: List[ExecutionTreeNode]) -> None:
    """
    Remove urllib3 frames nested within requests frames.

    Modifies the tree in place.
    """
    for node in nodes:
        if node.type == "outbound_http_request" and node.subtype == "requests":
            new_children = []
            for child in node.children:
                if child.type == "outbound_http_request" and child.subtype == "urllib3":
                    new_children.extend(child.children)
                else:
                    new_children.append(child)
            node.children = new_children

        remove_superfluous_urllib3_frames(node.children)


def draw_tree(node: ExecutionTreeNode, prefix: str = "") -> str:
    """
    Draw an ASCII art representation of a tree starting from a node.

    Useful for debugging tree structure issues.
    """
    output = f"{prefix}{node.name}\n"
    n = len(node.children)
    for index, child in enumerate(node.children):
        new_prefix = f"{prefix}    " if index == n - 1 else f"{prefix}│   "
        output += draw_tree(child, new_prefix)
    return output


def stripped_frame_of_interest(frame: Dict[str, Any]) -> str:
    """Return a minimal JSON representation of a frame for debugging."""
    allowed_keys = [
        "frame_id",
        "type",
        "subtype",
        "event",
        "qualname",
        "path",
        "co_name",
    ]
    filtered = {k: frame.get(k) for k in allowed_keys if k in frame}
    return json.dumps(filtered)


def debug_surrounding_frames_of_interest(
    index: int, frames: List[Dict[str, Any]]
) -> str:
    """Show frames surrounding a specific index for debugging."""
    output = "flat surrounding frames of interest:\n"
    offsets = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

    for offset in offsets:
        current_index = index + offset
        if 0 <= current_index < len(frames):
            output += f"{offset} {stripped_frame_of_interest(frames[current_index])}\n"
        else:
            output += f"{offset} [out of bounds]\n"

    return output


def frame_mismatch_debug_info(
    current_parent: ExecutionTreeNode,
    frame_of_interest: Dict[str, Any],
    all_frames: List[Dict[str, Any]],
) -> str:
    """
    Generate detailed debug information for frame ID mismatches.

    Shows the tree structure with indentation marking where call/return pairs
    are expected but don't match.
    """
    current_parent_frame_id = current_parent.frame_id
    current_return_frame_id = frame_of_interest.get("frame_id")

    output_lines = []
    intermediate_frame_count = 0
    indentation_stack: list[str] = []

    for frame in all_frames:
        call_or_return = "unknown"
        frame_type = frame.get("type")
        event = frame.get("event")

        if not frame_type or frame_type == "frame":
            if event in CALL_FRAME_EVENTS:
                call_or_return = "call"
            elif event in RETURN_FRAME_EVENTS:
                call_or_return = "return"
        else:
            if frame_type in CALL_LIKE_FRAMES:
                call_or_return = "call"
            elif frame_type in RETURN_LIKE_FRAMES:
                call_or_return = "return"
            elif frame_type in LEAF_FRAMES:
                call_or_return = "leaf"

        indent = "  " * len(indentation_stack)

        if (
            frame.get("frame_id") == current_parent_frame_id
            or frame.get("frame_id") == current_return_frame_id
        ):
            if intermediate_frame_count > 0:
                output_lines.append(f"{indent}({intermediate_frame_count} frames)")
                intermediate_frame_count = 0

            if call_or_return == "call":
                output_lines.append(
                    f"{indent}{call_or_return} ({frame_type}) {{{frame.get('frame_id')}}}"
                )
                indentation_stack.append(call_or_return)
            elif call_or_return == "return":
                if indentation_stack:
                    indentation_stack.pop()
                indent = "  " * len(indentation_stack)
                output_lines.append(
                    f"{indent}{call_or_return} ({frame_type}) {{{frame.get('frame_id')}}}"
                )
        else:
            intermediate_frame_count += 1

    if intermediate_frame_count > 0:
        indent = "  " * len(indentation_stack)
        output_lines.append(f"{indent}({intermediate_frame_count} frames)")

    return "\n".join(output_lines)


def throw_missing_return_frame(
    current_parent: ExecutionTreeNode,
    frame_of_interest: Dict[str, Any],
    frame_index: int,
    all_frames: List[Dict[str, Any]],
) -> None:
    """
    Raise an error with detailed debugging information when a return frame is missing.

    This provides extensive context to help diagnose tree building issues.
    """
    debug_output = frame_mismatch_debug_info(
        current_parent, frame_of_interest, all_frames
    )

    tree_drawing = draw_tree(current_parent)

    surrounding_frames = debug_surrounding_frames_of_interest(frame_index, all_frames)

    raise ValueError(
        f"Could not build tree\n"
        f"Frame with no corresponding return: {current_parent.frame_id} ({current_parent.name})\n\n"
        f"{debug_output}\n\n"
        f"{tree_drawing}\n\n"
        f"{surrounding_frames}"
    )
