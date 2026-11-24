"""The closed vocabulary of ``chat.tool_trace``: every ``event`` and ``kind`` a writer may store.

The table's CHECK constraints (``cx_tool_trace_event_check``, ``cx_tool_trace_kind_check``) refuse anything else, so
a token moves in this order: widen the constraint on the database, add it here, then write it. Guard:
``scripts/check_tool_trace_events.py`` (every writer in the repo is declared here; ``--live``: everything declared
here is in the live constraints).
"""

from __future__ import annotations

TRACE_EVENTS: tuple[str, ...] = (
    "OK",
    "FAIL",
    "DELEGATED",
    "SURFACE_REJECT",
    "NO_EXECUTOR",
    "LOOP_BLOCK",
    "VARIANT_RECOVERED",
    "ALIAS_RECOVERED",
    "INFERRED",
    "COERCED",
    "CLAMPED",
    "ARGS_PINNED",
)

TRACE_KINDS: tuple[str, ...] = ("SERVER", "DELEGATE")
