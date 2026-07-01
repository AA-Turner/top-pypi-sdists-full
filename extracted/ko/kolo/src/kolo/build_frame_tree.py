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

    index: int  # Position in the flattened tree traversal
    type: str  # "frame_span", "sql_query",  etc.
    name: str  # Human-readable name for the node
    frame_id: str  # Unique identifier for matching call/return pairs
    children: List[ExecutionTreeNode] = field(default_factory=list)
    all_children_count: int = 0  # Total count of all descendants (recursive)
    data: Dict[str, Any] = field(default_factory=dict)  # Type-specific data
    subtype: Optional[str] = None  # e.g., "requests", "urllib3"

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


# Frame type classifications
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

# With sys.monitoring, we have these new frame types in addition to call and return
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
    execution_tree_node_index = 0

    # Collections for quick access to specific node types
    sql_queries: List[ExecutionTreeNode] = []
    outbound_http_requests: List[ExecutionTreeNode] = []
    background_jobs: List[ExecutionTreeNode] = []
    log_messages: List[ExecutionTreeNode] = []

    outbound_http_request_index = 0
    sql_query_index = 0
    log_message_index = 0
    five_hundred_exception: Optional[Dict[str, Any]] = None

    # Preprocess frames to remove legacy/problematic frames
    frames_of_interest = preprocess_frames_of_interest(frames_of_interest)

    for frame_index, frame in enumerate(frames_of_interest):
        is_return_frame = "event" in frame and frame["event"] in RETURN_FRAME_EVENTS
        is_call_frame = "event" in frame and frame["event"] in CALL_FRAME_EVENTS

        frame_type = frame.get("type")  # Optional - not all frames have "type"
        is_call = is_call_frame or (frame_type and frame_type in CALL_LIKE_FRAMES)
        is_return = is_return_frame or (frame_type and frame_type in RETURN_LIKE_FRAMES)

        if is_call:
            current_tree_node = make_tree_node(frame, execution_tree_node_index)

            if not current_ancestors:
                # New root-level subtree
                current_ancestors.append(current_tree_node)
            else:
                # Child of current parent
                current_parent = current_ancestors[-1]
                current_parent.children.append(current_tree_node)
                current_ancestors.append(current_tree_node)

            execution_tree_node_index += 1

        elif is_return:
            if not current_ancestors:
                logger.warning(
                    f"Return frame with no corresponding call frame at index {frame_index}"
                )
                continue

            current_parent = current_ancestors[-1]

            # Validate frame matching
            expected_parent_type = get_expected_parent_type(frame)
            if current_parent.type != expected_parent_type:
                throw_missing_return_frame(
                    current_parent, frame, frame_index, frames_of_interest
                )

            # Check frame_id match
            expected_frame_id = current_parent.frame_id
            actual_frame_id = frame["frame_id"]
            if expected_frame_id != actual_frame_id:
                debug_info = frame_mismatch_debug_info(
                    current_parent, frame, frames_of_interest
                )
                logger.warning(
                    f"Kolo warning: frame_id mismatch. Expected {expected_frame_id} "
                    f"({current_parent.type}), got {actual_frame_id} ({frame_type})\n"
                    f"{debug_info}\n"
                    f"{debug_surrounding_frames_of_interest(frame_index, frames_of_interest)}"
                )

            # Populate return data based on frame type
            if is_return_frame:
                current_parent.data["return_frame"] = frame
            elif frame_type == "django_response":
                current_parent.data["response"] = frame

                # Handle 500 exceptions
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
                current_parent.data["query_data"] = frame.get("query_data")  # Optional
                current_parent.data["query_params"] = frame.get("query_params")
                current_parent.data["database"] = frame.get("database")  # Optional
                current_parent.data["return_timestamp"] = frame["return_timestamp"]
                sql_queries.append(current_parent)

            elif frame_type == "outbound_http_response":
                current_parent.data["index"] = outbound_http_request_index
                outbound_http_request_index += 1
                current_parent.data["response"] = {
                    "body": frame.get("body"),  # Optional
                    "headers": frame.get("headers"),  # Optional
                    "timestamp": frame["timestamp"],
                    "status_code": frame["status_code"],
                }
                # Hide urllib3 requests nested in requests
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

            # Pop completed subtree
            completed_node = current_ancestors.pop()
            if not current_ancestors:
                # Completed root-level subtree
                root_execution_tree_nodes.append(completed_node)

        elif frame_type and frame_type in LEAF_FRAMES:
            # Leaf nodes (e.g., log messages)
            current_tree_node = make_tree_node(frame, execution_tree_node_index)

            if frame_type == "log_message":
                current_tree_node.data["index"] = log_message_index
                log_message_index += 1
                log_messages.append(current_tree_node)

            if current_ancestors:
                current_parent = current_ancestors[-1]
                current_parent.children.append(current_tree_node)
            else:
                # Leaf node at root level
                root_execution_tree_nodes.append(current_tree_node)

            execution_tree_node_index += 1

        elif frame_type == "exception":
            # 500 exception - stored for later attachment to django_response
            five_hundred_exception = frame

    if current_ancestors:
        logger.warning(
            f"Incomplete subtrees exist: {len(current_ancestors)} unclosed frames"
        )

    # Postprocess and calculate counts
    execution_tree_nodes = postprocess_tree(root_execution_tree_nodes)
    renumber_indices(execution_tree_nodes)
    set_children_counts(execution_tree_nodes)

    # Filter metadata lists to only include nodes still present after postprocessing
    # This ensures that metadata lists don't reference nodes that were removed
    # during postprocessing (e.g., Django setup subtrees, urllib3 frames)
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
    )


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
        return str(msg)[:50]  # Truncate long messages

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

    # Handle sys.monitoring frames (call/return events)
    if event and event in CALL_FRAME_EVENTS:
        return ExecutionTreeNode(
            type="frame_span",
            data={"call_frame": frame},
            **base_data,
        )

    # Handle special frame types
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
                "user_code_call_site": frame.get("user_code_call_site"),  # Optional
                "call_timestamp": frame["call_timestamp"],
            },
            **base_data,
        )

    elif frame_type == "outbound_http_request":
        return ExecutionTreeNode(
            type="outbound_http_request",
            subtype=frame.get("subtype"),  # Optional
            data={
                "request": {
                    "url": frame["url"],
                    "body": frame.get("body"),  # Optional
                    "method": frame["method"],
                    "headers": frame.get("headers"),  # Optional
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
                "extra": frame.get("extra"),  # Optional
                "msg": frame["msg"],
                "stack": frame.get("stack"),  # Optional
                "traceback": frame.get("traceback"),  # Optional
                "name": frame.get("name"),  # Optional
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

    # Find matching frames in the tree
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

                # Continue searching in children
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

    # Old format: background_job frames without background_job_end
    if background_job_count > 0 and background_job_end_count == 0:
        return [frame for frame in frames if frame.get("type") != "background_job"]

    # New format: filter out celery.app.task.Task.apply_async
    return [
        frame
        for frame in frames
        if frame.get("qualname") != "celery.app.task.Task.apply_async"
    ]


def remove_empty_sql_queries(frames: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove SQL query pairs where the query is None."""
    result = []
    i = 0

    while i < len(frames):
        frame = frames[i]
        frame_type = frame.get("type")

        if frame_type == "start_sql_query":
            # Look ahead for end_sql_query
            next_frame = frames[i + 1] if i + 1 < len(frames) else None

            # Sometimes log messages can be between start and end
            if next_frame and next_frame.get("type") != "end_sql_query":
                next_frame = frames[i + 2] if i + 2 < len(frames) else None

            if next_frame and next_frame.get("type") == "end_sql_query":
                if next_frame.get("query") is None:
                    # Skip both start and end
                    i += 2
                    continue

        elif frame_type == "end_sql_query":
            if frame.get("query") is None:
                # Skip this end frame (start should have been skipped already)
                i += 1
                continue

        result.append(frame)
        i += 1

    return result


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
        # Only merge *consecutive* duplicate roots. Non-consecutive roots
        # sharing a frame_id are distinct entries and must be preserved —
        # only a placeholder-then-restore pair, which lands adjacent, is
        # actually the same frame split in two by a flush.
        if merged and merged[-1].frame_id == node.frame_id:
            existing = merged[-1]
            existing.children.extend(node.children)
            for key, value in node.data.items():
                if key not in existing.data:
                    existing.data[key] = value
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
            continue  # Skip this node entirely

        # Recursively process children
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
        # Recursively process children, removing nested module frames
        node.children = _remove_nested_module_frames(node.children)
        result.append(node)

    return result


def _remove_nested_module_frames(
    nodes: List[ExecutionTreeNode],
) -> List[ExecutionTreeNode]:
    """Helper function to remove module frames at non-root levels."""
    result = []
    for node in nodes:
        # Check if this is a module frame
        if node.type == "frame_span":
            call_frame = node.data.get("call_frame", {})
            if call_frame.get("co_name") == "<module>":
                continue  # Skip this node and all its children

        # Recursively process children
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
            # Flatten urllib3 children
            new_children = []
            for child in node.children:
                if child.type == "outbound_http_request" and child.subtype == "urllib3":
                    # Move urllib3's children up to requests level
                    new_children.extend(child.children)
                else:
                    new_children.append(child)
            node.children = new_children

        # Recursively process children
        remove_superfluous_urllib3_frames(node.children)


# Debug helpers


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
        # Determine if this is a call, return, or leaf frame
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

        # Highlight frames we're interested in
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
                indent = "  " * len(indentation_stack)  # Recalculate
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
