import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Union

import httpx

from .db import (
    get_pinned_traces,
    list_traces_with_data_from_db,
    load_trace_with_size_from_db,
)
from .local_node_bridge import (
    process_node_data_with_local_node,
    process_trace_with_local_node,
    process_tree_with_local_node,
)
from .serialize import load_msgpack
from .trace import Trace
from .utils import pretty_byte_size, relative_time


def format_trace_for_display(
    trace_id: str,
    timestamp: datetime,
    size: int,
    trace_name: Optional[str],
    now: Optional[datetime] = None,
) -> str:
    """Format a trace for display in CLI or MCP."""
    if now is None:
        now = datetime.now(timezone.utc)

    rel_time = relative_time(timestamp)

    size_str = pretty_byte_size(size)

    # Format output with trace_id at the end if we have a name
    if trace_name:
        return f"{trace_name} ({rel_time}, {size_str}, {trace_id})"
    return f"{trace_id} ({rel_time}, {size_str})"


def get_formatted_traces(
    db_path, count: int = 500, reverse: bool = False
) -> Iterator[str]:
    """Get formatted traces from the database, yielding one at a time."""
    now = datetime.now(timezone.utc)
    traces = list_traces_with_data_from_db(db_path, count=count, reverse=reverse)

    for trace_id, timestamp_str, size, msgpack_data, auto_generated_name in traces:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f").replace(
            tzinfo=timezone.utc
        )

        trace_name = Trace.resolve_display_name(
            msgpack_data, auto_generated_name, db_path, trace_id
        )

        yield format_trace_for_display(trace_id, timestamp, size, trace_name, now)


local_cf_worker_endpoint = "http://localhost:8787"
prod_cf_worker_endpoint = "https://worker.kolo.app"
worker_endpoint = prod_cf_worker_endpoint


async def get_compact_trace(
    trace_id: str,
    trace_data: bytes,
    timestamp_str: str,
    size: int,
    include_returns: bool = False,
    use_js: bool = False,
) -> str:
    """Get compact representation of a trace."""

    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f").replace(
        tzinfo=timezone.utc
    )

    prefix = f"=== Kolo Trace {trace_id} ===\n{relative_time(timestamp)}, {pretty_byte_size(size)}"

    if use_js:
        compact_trace_text = process_trace_with_local_node(trace_data, include_returns)

        if compact_trace_text is None:
            # Fall back to remote worker if local processing failed
            compact_trace_text = await fetch_compact_trace(
                trace_id, trace_data, include_returns
            )
        return prefix + "\n\n" + compact_trace_text
    else:
        return get_compact_trace_sync(trace_data, size, include_returns)


def get_compact_trace_sync(
    trace_data: bytes,
    size: int,
    include_returns: bool = False,
) -> str:
    """Get compact representation of a trace (synchronous, Python-only)."""

    data = load_msgpack(trace_data)
    trace = Trace(unprocessed_data=data, size=size)
    return trace.compact(include_returns)


async def fetch_compact_trace(
    trace_id: str, trace_data: bytes, include_returns: bool = False
) -> str:
    """Get compact representation of a trace from the worker."""

    async with httpx.AsyncClient() as client:
        url = f"{worker_endpoint}/traces/{trace_id}/compact"
        if include_returns:
            url += "?returns=1"

        response = await client.post(
            url, headers={"Content-Type": "application/msgpack"}, content=trace_data
        )
        response.raise_for_status()
        return response.text


async def get_node_data(
    trace_id: str, node_index: int, trace_data: bytes, use_js: bool = False
) -> dict:
    """Get node data for a specific node index."""

    if use_js:
        node_data = process_node_data_with_local_node(trace_data, node_index)

        if node_data is None:
            # Fall back to remote worker if local processing failed
            node_data = await fetch_node_data(trace_id, node_index, trace_data)

        return node_data
    else:
        data = load_msgpack(trace_data)
        trace = Trace(unprocessed_data=data, size=len(trace_data))

        node = trace.main_tree.find_node_by_index(node_index)
        if node is None:
            raise ValueError(f"Node {node_index} not found in trace {trace_id}")

        return {
            "index": node.index,
            "type": node.type,
            "name": node.name,
            "frame_id": node.frame_id,
            "data": node.data,
            "ancestor_count": node.ancestor_count,
            "all_children_count": node.all_children_count,
            "duration_ms": node.duration_ms,
        }


async def fetch_node_data(trace_id: str, node_index: int, trace_data: bytes) -> dict:
    """Get node data from the remote worker for a specific node index."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{worker_endpoint}/traces/{trace_id}/tree/{node_index}",
            headers={"Content-Type": "application/msgpack"},
            content=trace_data,
        )
        response.raise_for_status()
        return response.json()


async def get_execution_tree(
    trace_id: str, trace_data: bytes, use_js: bool = False
) -> dict:
    """Get execution tree for a trace."""

    # TODO: Do we still need this now that we're not having to serilize to json anymore?

    if use_js:
        tree_data = process_tree_with_local_node(trace_data)

        if tree_data is None:
            # Fall back to remote worker if local processing failed
            tree_data = await fetch_execution_tree(trace_id, trace_data)

        return tree_data
    else:
        data = load_msgpack(trace_data)
        trace = Trace(unprocessed_data=data, size=len(trace_data))

        # Get the basic execution tree
        tree_info = trace.main_tree.basic_execution_tree

        # Convert to dict format for JSON serialization
        def make_json_serializable(obj):
            """Convert Python objects to JSON-serializable types."""
            if isinstance(obj, (set, frozenset)):
                return list(obj)
            elif isinstance(obj, dict):
                # Convert dict keys to strings if they're not JSON-compatible
                result = {}
                for k, v in obj.items():
                    if isinstance(k, (str, int, float, bool, type(None))):
                        result[k] = make_json_serializable(v)
                    else:
                        # Convert non-JSON-compatible keys to string
                        result[str(k)] = make_json_serializable(v)
                return result
            elif isinstance(obj, (list, tuple)):
                return [make_json_serializable(item) for item in obj]
            else:
                # Handle any other non-serializable types
                try:
                    # Try to serialize it (will work for primitives)
                    json.dumps(obj)
                    return obj
                except (TypeError, ValueError):
                    # If it can't be serialized, convert to string
                    return str(obj)

        def node_to_dict(node):
            return {
                "index": node.index,
                "type": node.type,
                "name": node.name,
                "frame_id": node.frame_id,
                "data": make_json_serializable(node.data),
                "all_children_count": node.all_children_count,
                "children": [node_to_dict(child) for child in node.children],
            }

        return {
            "execution_tree_nodes": [
                node_to_dict(node) for node in tree_info.execution_tree_nodes
            ],
            "total_execution_tree_node_count": tree_info.total_execution_tree_node_count,
            "sql_queries": [node_to_dict(node) for node in tree_info.sql_queries],
            "outbound_http_requests": [
                node_to_dict(node) for node in tree_info.outbound_http_requests
            ],
            "background_jobs": [
                node_to_dict(node) for node in tree_info.background_jobs
            ],
            "log_messages": [node_to_dict(node) for node in tree_info.log_messages],
        }


async def fetch_execution_tree(trace_id: str, trace_data: bytes) -> dict:
    """Get execution tree from the remote worker."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{worker_endpoint}/traces/{trace_id}/tree",
            headers={"Content-Type": "application/msgpack"},
            content=trace_data,
        )
        response.raise_for_status()
        return response.json()


async def get_compact_traces(
    db_path: Path,
    trace_id: Union[str, None] = None,
    *,
    pinned: bool = False,
    returns: bool = False,
    recent: int = 0,
    use_js: bool = False,
) -> List[Tuple[str, str]]:
    """Get compact representation of traces.

    Args:
        db_path: Path to the database
        trace_id: Specific trace ID to get, ignored if pinned=True or recent>0
        pinned: If True, get all pinned traces
        returns: Include return values in compact representation
        recent: If > 0, get the N most recent traces
        use_js: If True, use Node.js implementation; if False, use Python

    Returns:
        List of tuples (trace_id, compact_representation)

    Raises:
        TraceNotFoundError: If trace_id is not found in the database
        ValueError: If no valid selection criteria provided
    """
    if not any([pinned, trace_id, recent > 0]):
        raise ValueError("Either trace_id, --pinned, or --recent must be provided")
    results = []

    if pinned:
        for trace_id, timestamp_str, size, trace_data, _ in get_pinned_traces(db_path):
            try:
                compact_repr = await get_compact_trace(
                    trace_id, trace_data, timestamp_str, size, returns, use_js
                )
                results.append((trace_id, compact_repr))
            except Exception as e:
                # For pinned traces, we want to continue even if one fails
                results.append((trace_id, f"Error: {e}"))
    elif recent > 0:
        for (
            trace_id,
            timestamp_str,
            size,
            trace_data,
            _,
        ) in list_traces_with_data_from_db(db_path, count=recent):
            assert trace_id is not None
            try:
                compact_repr = await get_compact_trace(
                    trace_id, trace_data, timestamp_str, size, returns, use_js
                )
                results.append((trace_id, compact_repr))
            except Exception as e:
                # For multiple traces, we want to continue even if one fails
                results.append((trace_id, f"Error: {e}"))
    else:
        # Single trace - let errors propagate naturally
        assert trace_id is not None
        _, timestamp_str, size, trace_data = load_trace_with_size_from_db(
            db_path, trace_id
        )
        compact_repr = await get_compact_trace(
            trace_id, trace_data, timestamp_str, size, returns, use_js
        )
        results.append((trace_id, compact_repr))

    return results
