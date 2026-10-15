import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Union

from .db import (
    get_pinned_traces,
    list_traces_with_data_from_db,
    load_trace_with_size_from_db,
)
from .trace_container import load_trace
from .trace import Trace
from .utils import pretty_byte_size, relative_time

logger = logging.getLogger("kolo")


class TraceUnreadableError(ValueError):
    """A stored trace that could not be decoded or rendered."""

    def __init__(self, trace_id: str, reason: str):
        super().__init__(f"Could not read trace {trace_id}: {reason}")
        self.trace_id = trace_id
        self.reason = reason


TRACE_TIMESTAMP_FORMATS = (
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
)


def parse_trace_timestamp(timestamp_str: str) -> datetime:
    for timestamp_format in TRACE_TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(timestamp_str, timestamp_format).replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
    raise ValueError(f"Unsupported trace timestamp format: {timestamp_str!r}")


def parse_trace_timestamp_or_now(
    timestamp_str: str,
) -> Tuple[datetime, Optional[str]]:
    """``parse_trace_timestamp`` for a listing: a stored timestamp that
    cannot be parsed gives ``(now, reason)`` instead of raising."""
    try:
        return parse_trace_timestamp(timestamp_str), None
    except Exception as error:
        return datetime.now(timezone.utc), unreadable_reason(error)


def make_json_serializable(obj):
    """Convert Python objects to JSON-serializable types.

    Handles:
    - Sets/frozensets -> lists
    - Dict with non-string keys -> string keys
    - Other non-serializable types -> string representation (Python repr)
    """
    if isinstance(obj, (set, frozenset)):
        return list(obj)
    elif isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if isinstance(k, (str, int, float, bool, type(None))):
                result[k] = make_json_serializable(v)
            else:
                result[str(k)] = make_json_serializable(v)
        return result
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    else:
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)


def unreadable_reason(error: BaseException) -> str:
    """Why a trace could not be read, on one line."""
    message = str(error).strip()
    first_line = message.splitlines()[0] if message else ""
    name = type(error).__name__
    return f"{name}: {first_line}" if first_line else name


def resolve_display_name(
    msgpack_data: bytes,
    auto_generated_name: Optional[str],
    db_path,
    trace_id: str,
) -> Tuple[Optional[str], Optional[str]]:
    """``Trace.resolve_display_name`` for a listing: ``(name, None)``, or
    ``(None, reason)`` for a trace that cannot be read. One unreadable trace
    must not stop the others from being listed."""
    try:
        return (
            Trace.resolve_display_name(
                msgpack_data, auto_generated_name, db_path, trace_id
            ),
            None,
        )
    except Exception as error:
        logger.debug("Could not read trace %s", trace_id, exc_info=True)
        return None, unreadable_reason(error)


def format_trace_for_display(
    trace_id: str,
    timestamp: datetime,
    size: int,
    trace_name: Optional[str],
    now: Optional[datetime] = None,
    unreadable: Optional[str] = None,
) -> str:
    """Format a trace for display in CLI or MCP."""
    if unreadable:
        return (
            f"{trace_id} ({relative_time(timestamp)}, {pretty_byte_size(size)}) "
            f"[unreadable: {unreadable}]"
        )
    if now is None:
        now = datetime.now(timezone.utc)

    rel_time = relative_time(timestamp)

    size_str = pretty_byte_size(size)

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
        timestamp, bad_timestamp = parse_trace_timestamp_or_now(timestamp_str)

        trace_name, unreadable = resolve_display_name(
            msgpack_data, auto_generated_name, db_path, trace_id
        )
        unreadable = unreadable or bad_timestamp

        yield format_trace_for_display(
            trace_id, timestamp, size, trace_name, now, unreadable=unreadable
        )


def get_compact_trace(
    trace_data: bytes,
    size: int,
    include_returns: bool = False,
) -> str:
    """Get compact representation of a trace."""
    data = load_trace(trace_data)
    trace = Trace(unprocessed_data=data, size=size)
    return trace.compact(include_returns)


def get_node_data(
    trace_id: str,
    node_index: int,
    trace_data: bytes,
    thread_id: Optional[str] = None,
) -> dict:
    """Get node data for a specific node index.

    ``thread_id`` selects which thread's tree to look the index up in.
    Indices restart at 0 per thread, so the same ``node_index`` means
    different frames in different threads. When ``thread_id`` is None
    the main thread (whichever thread was active when profiling
    started) is used, matching pre-threading behavior.
    """
    data = load_trace(trace_data)
    trace = Trace(unprocessed_data=data, size=len(trace_data))

    if thread_id is None:
        tree = trace.main_tree
    else:
        matching = [s for s in trace.threads if s.thread_id == thread_id]
        if not matching:
            known = ", ".join(s.thread_id for s in trace.threads) or "<none>"
            raise ValueError(
                f"Thread {thread_id!r} not found in trace {trace_id}. "
                f"Known thread ids: {known}"
            )
        tree = matching[0].tree

    node = tree.find_node_by_index(node_index)
    if node is None:
        where = f"thread {thread_id}" if thread_id else "main thread"
        raise ValueError(f"Node {node_index} not found in {where} of trace {trace_id}")

    return {
        "index": node.index,
        "type": node.type,
        "name": node.name,
        "frame_id": node.frame_id,
        "data": make_json_serializable(node.data),
        "ancestor_count": node.ancestor_count,
        "all_children_count": node.all_children_count,
        "duration_ms": node.duration_ms,
    }


def get_compact_traces(
    db_path: Path,
    trace_id: Union[str, None] = None,
    *,
    pinned: bool = False,
    returns: bool = False,
    recent: int = 0,
) -> List[Tuple[str, str]]:
    """Get compact representation of traces.

    Args:
        db_path: Path to the database
        trace_id: Specific trace ID to get, ignored if pinned=True or recent>0
        pinned: If True, get all pinned traces
        returns: Include return values in compact representation
        recent: If > 0, get the N most recent traces

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
                compact_repr = get_compact_trace(trace_data, size, returns)
                results.append((trace_id, compact_repr))
            except Exception as e:
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
                compact_repr = get_compact_trace(trace_data, size, returns)
                results.append((trace_id, compact_repr))
            except Exception as e:
                results.append((trace_id, f"Error: {e}"))
    else:
        assert trace_id is not None
        _, timestamp_str, size, trace_data = load_trace_with_size_from_db(
            db_path, trace_id
        )
        try:
            compact_repr = get_compact_trace(trace_data, size, returns)
        except Exception as error:
            raise TraceUnreadableError(trace_id, unreadable_reason(error)) from error
        results.append((trace_id, compact_repr))

    return results
