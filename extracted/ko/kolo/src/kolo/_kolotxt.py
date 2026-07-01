"""
Generate the kolo.txt file.

This module is designed to be imported with minimal overhead - it only uses
stdlib imports and lazy-loads heavy dependencies. Used by both core.py
(KOLO=1 activation) and _emit_auto.py (auto-emit subprocess).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

KOLOTXT_HEADER = """\
================================================================================
KOLO - Trace your Python code
================================================================================

GUIDANCE
--------
`KOLO=1 python myprogram.py` - run with kolo enabled or capture in another way: docs.kolo.app/capture
`kolo trace list` - list recent kolo traces
`kolo cat TRACE_ID` - show trace output. run with `--returns` to include input and return values
`kolo trace node TRACE_ID NODE_INDEX` - get the FULL details of a specific node, incl locals

RECENT TRACES (the latest 5 traces are auto-emitted to .kolo/traces/ and appear in search results)
-------------"""


def format_trace_line(
    trace_id: str,
    timestamp: "datetime",
    size: int,
    trace_name: str | None,
) -> str:
    """Format a single trace for the kolo.txt listing."""
    from .utils import pretty_byte_size, relative_time

    rel_time = relative_time(timestamp)
    size_str = pretty_byte_size(size)

    if trace_name:
        return f"{trace_name} ({rel_time}, {size_str}, {trace_id})"
    return f"{trace_id} ({rel_time}, {size_str})"


def generate_kolotxt_content(db_path: Path) -> str:
    """
    Generate the full kolo.txt content.

    Args:
        db_path: Path to the kolo database

    Returns:
        The full kolo.txt content as a string
    """
    from .cli_mcp_shared import parse_trace_timestamp
    from .db import list_traces_with_data_from_db
    from .serialize import load_msgpack
    from .trace import Trace

    lines = [KOLOTXT_HEADER]

    traces = list(list_traces_with_data_from_db(db_path, count=5, reverse=False))

    if not traces:
        lines.append(
            "No traces found. Run your Python code with KOLO=1 to capture traces."
        )
    else:
        for trace_id, timestamp_str, size, msgpack_data, auto_generated_name in traces:
            timestamp = parse_trace_timestamp(timestamp_str)
            trace_name = Trace.resolve_display_name(
                msgpack_data, auto_generated_name, db_path, trace_id
            )
            lines.append(format_trace_line(trace_id, timestamp, size, trace_name))

    lines.append("")
    lines.append("")

    # Latest trace section
    if traces:
        trace_id, timestamp_str, size, msgpack_data, _ = traces[0]
        try:
            data = load_msgpack(msgpack_data)
            trace = Trace(unprocessed_data=data, size=size)

            # Build LATEST TRACE header in the same style as other sections
            lines.append(f"LATEST TRACE ({trace_id})")
            lines.append("-" * len(f"LATEST TRACE ({trace_id})"))
            lines.append(trace.compact_metadata())
            lines.append("")
            lines.append(trace.compact_tree_only(include_return_value=False))
        except Exception as e:  # pragma: no cover
            lines.append("LATEST TRACE")
            lines.append("------------")
            lines.append(f"Error loading trace: {e}")
    else:
        lines.append("LATEST TRACE")
        lines.append("------------")
        lines.append("No traces available.")

    return "\n".join(lines)


def update_kolotxt(db_path: Path) -> Path:
    """
    Update the kolo.txt file.

    Args:
        db_path: Path to the kolo database (.kolo/.internal/db.sqlite3)

    Returns:
        Path to the kolo.txt file
    """
    # db is at .kolo/.internal/db.sqlite3, kolo.txt goes at .kolo/kolo.txt
    kolo_dir = db_path.parent.parent
    kolotxt_path = kolo_dir / "kolo.txt"
    content = generate_kolotxt_content(db_path)

    with open(kolotxt_path, "w", encoding="utf-8") as f:
        f.write(content)

    return kolotxt_path
