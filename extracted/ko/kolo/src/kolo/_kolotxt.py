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
    from .db import list_traces_with_data_from_db, load_trace_from_db
    from .trace_container import load_trace
    from .trace import Trace

    lines = [KOLOTXT_HEADER]

    latest_trace = None
    traces = []

    for (
        trace_id,
        timestamp_str,
        size,
        msgpack_data,
        auto_generated_name,
    ) in list_traces_with_data_from_db(db_path, count=5, reverse=False):
        if latest_trace is None:
            latest_trace = (trace_id, timestamp_str, size, msgpack_data)

        # Resolving an old trace's missing auto-generated name writes a lazy
        # migration. Defer that branch until this read generator is drained so
        # rollback-journal databases do not make a second connection wait on
        # the suspended cursor held by this same thread.
        trace_name = None
        needs_name_migration = not auto_generated_name
        if not needs_name_migration:
            trace_name = Trace.resolve_display_name(
                msgpack_data, auto_generated_name, db_path, trace_id
            )
        traces.append(
            (
                trace_id,
                timestamp_str,
                size,
                trace_name,
                needs_name_migration,
            )
        )

        # Do not retain every raw trace until the latest-trace section is
        # rendered. Five 500 MiB traces otherwise mean 2.5 GiB of raw blobs in
        # memory before msgpack decoding and tree construction even begin.
        del msgpack_data

    if not traces:
        lines.append(
            "No traces found. Run your Python code with KOLO=1 to capture traces."
        )
    else:
        for trace_id, timestamp_str, size, trace_name, needs_name_migration in traces:
            if needs_name_migration:
                if latest_trace is not None and trace_id == latest_trace[0]:
                    msgpack_data = latest_trace[3]
                else:
                    msgpack_data, _ = load_trace_from_db(db_path, trace_id)
                trace_name = Trace.resolve_display_name(
                    msgpack_data, None, db_path, trace_id
                )
                del msgpack_data

            timestamp = parse_trace_timestamp(timestamp_str)
            lines.append(format_trace_line(trace_id, timestamp, size, trace_name))

    lines.append("")
    lines.append("")

    # Latest trace section
    if latest_trace is not None:
        trace_id, timestamp_str, size, msgpack_data = latest_trace
        try:
            data = load_trace(msgpack_data)
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
