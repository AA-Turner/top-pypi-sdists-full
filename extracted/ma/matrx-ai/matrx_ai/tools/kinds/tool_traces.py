"""Kinds for the trace-debugging tool results — the tool system observing itself.

Ledger rows (KIND_TOOL_LEDGER, agent ``claude-tools-02``): ``debug_traces_recent``
``debug_traces_failures_since`` ``debug_traces_by_conv`` ``debug_traces_by_call``
``debug_traces_list_files`` ``debug_traces_get_file`` ``report_trace_incident``
``get_open_trace_incidents``.

FOUR TOOLS, ONE PAGE SHAPE. The four ``cx_tool_trace`` query tools all return
through the SAME helper (``debug_traces_tools._events_result``), so they are ONE
kind — ``tool_trace_event_page`` — not four near-duplicate slugs
(NOMENCLATURE.md). What differs between them is the FILTER, and the filter is
already a field (``filter_summary``).

THE VERBOSE AXIS IS PART OF THE SHAPE, NOT A SECOND SHAPE. ``_row_to_dict``
drops ``args`` / ``result_preview`` / ``metadata`` / ``process_started_at`` and
trims ``err_msg`` unless ``verbose=True``. Those four are declared OPTIONAL on
``tool_trace_event`` and the page carries ``verbose`` so a reader knows which
projection it is holding. Splitting compact and verbose into two kinds would
make the same row two identities.

THE CAP KEYS ARE DECLARED, NOT INCIDENTAL. ``truncated`` / ``note`` /
``next_offset`` / ``detail_hint`` appear only when the output was capped. A
KindModel is ``additionalProperties: false``, so an undeclared key is a
validation failure at run time — the honest declaration includes every key the
producer can emit, on every branch (the same union rule the ``fs_*`` family
learned the hard way).

All PLACEHOLDER tier: these capture the outer structure of our own trace rows
completely, and there is no richer provider payload being flattened away. The
one genuinely opaque field is ``tool_trace_event.args`` / ``result_preview`` /
``metadata`` — arbitrary per-tool JSON by definition, not a shape we are
declining to distill.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "tool_trace_event",
    label="Tool Trace Event",
    family="tool_traces",
    example={
        "id": "6f1c2d64-0f7e-4a1a-9b8e-9a1f0c4d2e11",
        "ts": "2026-08-23T18:04:11.512000+00:00",
        "event": "error",
        "tool_name": "fs_read",
        "kind": "local",
        "duration_ms": 42,
        "err_type": "not_found",
        "err_msg": "no such file: notes/missing.md",
        "conversation_id": None,
        "call_id": "call_ah82ks",
        "user_id": None,
        "process_pid": 4711,
    },
    maturity="placeholder",
)
class ToolTraceEvent(KindModel):
    """One ``cx_tool_trace`` row as the debug tools project it."""

    id: str = ""
    #: ISO-8601; None only when the row somehow carries no timestamp.
    ts: str | None = None
    event: str | None = None
    tool_name: str | None = None
    #: The trace row's own ``kind`` column (executor kind: local / mcp / …).
    #: NOT the content-IR kind — that is ``__kind``, and the collision is the
    #: column's, inherited from cx_tool_trace.
    kind: str | None = None
    duration_ms: int | None = None
    err_type: str | None = None
    #: Trimmed to 600 chars with an ellipsis on the COMPACT projection.
    err_msg: str = ""
    conversation_id: str | None = None
    call_id: str | None = None
    #: Output key is ``user_id`` for wire stability; the column is ``created_by``.
    user_id: str | None = None
    process_pid: int | None = None
    #: VERBOSE-ONLY fields — absent entirely on the compact projection.
    args: Any | None = None
    result_preview: Any | None = None
    metadata: Any | None = None
    process_started_at: str | None = None


@kind(
    "tool_trace_event_page",
    label="Tool Trace Events",
    family="tool_traces",
    example={
        "events": [
            {
                "__kind": "tool_trace_event",
                "id": "6f1c2d64-0f7e-4a1a-9b8e-9a1f0c4d2e11",
                "ts": "2026-08-23T18:04:11.512000+00:00",
                "event": "error",
                "tool_name": "fs_read",
                "kind": "local",
                "duration_ms": 42,
                "err_type": "not_found",
                "err_msg": "no such file: notes/missing.md",
                "call_id": "call_ah82ks",
                "process_pid": 4711,
            }
        ],
        "count": 1,
        "shown": 1,
        "verbose": False,
        "filter_summary": "tool_name=fs_read, event=error, last 24h",
        "detail_hint": (
            "compact rows — call debug_traces_by_call(call_id=…) or pass "
            "verbose=true for args / result_preview / metadata."
        ),
    },
    maturity="placeholder",
)
class ToolTraceEventPage(KindModel):
    """A bounded page of trace events — the shared return of all four query tools."""

    events: list[ToolTraceEvent] = []
    #: Rows matching the filter, at least — the query asks for limit+1 so a full
    #: page can honestly say "more exist" without counting the whole table.
    count: int = 0
    shown: int = 0
    verbose: bool = False
    filter_summary: str = ""
    #: Present only when the page was capped.
    truncated: bool | None = None
    note: str | None = None
    #: Present only on the compact projection.
    detail_hint: str | None = None


@kind(
    "tool_trace_file",
    label="Tool Trace File",
    family="tool_traces",
    example={
        "name": "tool-trace-2026-08-23_18-04-11.log",
        "size_bytes": 40213,
        "modified_at": "2026-08-23T18:44:02.000000+00:00",
        "is_header_only": False,
    },
    maturity="placeholder",
)
class ToolTraceFile(KindModel):
    """One ``tool-trace-*.log`` file in the local debug sink."""

    name: str = ""
    size_bytes: int = 0
    modified_at: str = ""
    #: A file at or under 100 bytes holds only its header — no events were logged.
    is_header_only: bool = False


@kind(
    "tool_trace_file_listing",
    label="Tool Trace File Listing",
    family="tool_traces",
    example={
        "files": [
            {
                "__kind": "tool_trace_file",
                "name": "tool-trace-2026-08-23_18-04-11.log",
                "size_bytes": 40213,
                "modified_at": "2026-08-23T18:44:02.000000+00:00",
                "is_header_only": False,
            }
        ],
        "count": 1,
        "log_dir": "/srv/app/.matrx-debug",
    },
    maturity="placeholder",
)
class ToolTraceFileListing(KindModel):
    """The local trace-log directory. ``log_dir`` is None when no sink is active."""

    files: list[ToolTraceFile] = []
    count: int = 0
    log_dir: str | None = None


@kind(
    "tool_trace_file_window",
    label="Tool Trace File Window",
    family="tool_traces",
    example={
        "filename": "tool-trace-2026-08-23_18-04-11.log",
        "size_bytes": 40213,
        "total_chars": 40180,
        "offset": 0,
        "shown_chars": 12000,
        "content": "## tool-trace 2026-08-23\n[fs_read] ok 42ms\n",
        "truncated": True,
        "next_offset": 12000,
        "note": "showing chars 0-12000 of 40180; call again with offset=12000 for more.",
    },
    maturity="placeholder",
)
class ToolTraceFileWindow(KindModel):
    """A paged character window into one trace file.

    A trace file is unbounded (verbose logging grows them to many MB), so the
    tool returns a window and the caller pages with ``next_offset``. ``content``
    is raw log text — opaque by definition, not a shape being flattened.
    """

    filename: str = ""
    size_bytes: int = 0
    total_chars: int = 0
    offset: int = 0
    shown_chars: int = 0
    content: str = ""
    #: Present only when more of the file remains after this window.
    truncated: bool | None = None
    next_offset: int | None = None
    note: str | None = None


@kind(
    "tool_trace_incident_report",
    label="Tool Trace Incident Report",
    family="tool_traces",
    example={
        "feedback_id": "b2b1b0c7-8d3e-4a55-9c0f-2a1e4d6b7c88",
        "created": True,
        "merged_into_existing": False,
        "dedupe_key": "fs_read|not_found|no such file",
        "priority": "medium",
        "category_slug": "tool-trace-incident",
    },
    maturity="placeholder",
)
class ToolTraceIncidentReport(KindModel):
    """What filing an incident returns.

    ``created`` and ``merged_into_existing`` are the two halves of one fact and
    both are kept: the tool DEDUPES on ``dedupe_key``, so a caller has to be able
    to tell "I filed something new" from "I bumped an existing row's count".
    """

    feedback_id: str = ""
    created: bool = False
    merged_into_existing: bool = False
    dedupe_key: str = ""
    priority: str = ""
    category_slug: str = ""


@kind(
    "tool_trace_incident",
    label="Tool Trace Incident",
    family="tool_traces",
    example={
        "id": "b2b1b0c7-8d3e-4a55-9c0f-2a1e4d6b7c88",
        "route": "tool:fs_read",
        "priority": "medium",
        "status": "new",
        "admin_decision": "pending",
        "ai_assessment": "The VFS branch does not honour the paging arguments.",
        "ai_solution_proposal": "Thread offset/limit through vfs_filesystem.read.",
        "ai_complexity": "small",
        "ai_estimated_files": 1,
        "created_at": "2026-08-23T18:05:00.000000+00:00",
        "updated_at": "2026-08-23T18:05:00.000000+00:00",
    },
    maturity="placeholder",
)
class ToolTraceIncident(KindModel):
    """One open incident row. ``route`` is always ``tool:<tool_name>``."""

    id: str = ""
    route: str | None = None
    priority: str | None = None
    status: str | None = None
    admin_decision: str | None = None
    ai_assessment: str | None = None
    ai_solution_proposal: str | None = None
    ai_complexity: str | None = None
    ai_estimated_files: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


@kind(
    "tool_trace_incident_filter",
    label="Tool Trace Incident Filter",
    family="tool_traces",
    example={"severity": None, "tool_name_substring": "fs_", "limit": 20},
    maturity="placeholder",
)
class ToolTraceIncidentFilter(KindModel):
    """The filter a listing was produced under — echoed back so a reader knows
    what the absence of a row means. None means "not filtered on"."""

    severity: str | None = None
    tool_name_substring: str | None = None
    limit: int = 0


@kind(
    "tool_trace_incident_list",
    label="Tool Trace Incidents",
    family="tool_traces",
    example={
        "incidents": [
            {
                "__kind": "tool_trace_incident",
                "id": "b2b1b0c7-8d3e-4a55-9c0f-2a1e4d6b7c88",
                "route": "tool:fs_read",
                "priority": "medium",
                "status": "new",
                "admin_decision": "pending",
                "created_at": "2026-08-23T18:05:00.000000+00:00",
            }
        ],
        "count": 1,
        "filter": {
            "__kind": "tool_trace_incident_filter",
            "severity": None,
            "tool_name_substring": "fs_",
            "limit": 20,
        },
    },
    maturity="placeholder",
)
class ToolTraceIncidentList(KindModel):
    """Open Tool Trace incidents, newest first."""

    incidents: list[ToolTraceIncident] = []
    count: int = 0
    filter: ToolTraceIncidentFilter = ToolTraceIncidentFilter()


@kind(
    "tool_call_record",
    label="Tool Call Record",
    family="tool_traces",
    example={
        "id": "0f0a5c2e-1d3b-4c5a-8e7f-9a0b1c2d3e4f",
        "tool_name": "fs_read",
        "call_id": "call_ah82ks",
        "status": "completed",
        "success": False,
        "is_error": True,
        "error_type": "not_found",
        "error_message": "no such file: notes/missing.md",
        "arguments": {"path": "notes/missing.md"},
        "output": None,
        "output_chars": 0,
        "duration_ms": 42,
        "started_at": "2026-08-23T18:04:11.470000+00:00",
        "completed_at": "2026-08-23T18:04:11.512000+00:00",
        "iteration": 1,
        "conversation_id": None,
        "user_id": None,
    },
    maturity="placeholder",
)
class ToolCallRecord(KindModel):
    """The joined ``cx_tool_call`` row for one call_id — the CALL, where the
    trace events are the things that happened to it.

    ``output`` is the tool's own payload and is therefore any shape at all; on
    this read it may be a STRING trimmed to the soft cap, in which case
    ``output_note`` says so. Declaring it as anything narrower would be a lie
    about every other tool in the registry.
    """

    id: str = ""
    tool_name: str | None = None
    call_id: str | None = None
    status: str | None = None
    success: bool | None = None
    is_error: bool | None = None
    error_type: str | None = None
    error_message: str | None = None
    arguments: Any | None = None
    output: Any | None = None
    output_chars: int | None = None
    duration_ms: int | None = None
    started_at: str | None = None
    completed_at: str | None = None
    iteration: int | None = None
    conversation_id: str | None = None
    user_id: str | None = None
    #: Present only when ``output`` was trimmed to the soft cap.
    output_note: str | None = None


@kind(
    "tool_trace_call_detail",
    label="Tool Call Forensics",
    family="tool_traces",
    example={
        "call_id": "call_ah82ks",
        "events": [
            {
                "__kind": "tool_trace_event",
                "id": "6f1c2d64-0f7e-4a1a-9b8e-9a1f0c4d2e11",
                "ts": "2026-08-23T18:04:11.512000+00:00",
                "event": "error",
                "tool_name": "fs_read",
                "kind": "local",
                "duration_ms": 42,
                "err_type": "not_found",
                "err_msg": "no such file: notes/missing.md",
                "call_id": "call_ah82ks",
                "process_pid": 4711,
                "args": {"path": "notes/missing.md"},
                "result_preview": None,
                "metadata": None,
                "process_started_at": "2026-08-23T17:40:00.000000+00:00",
            }
        ],
        "tool_call": {
            "__kind": "tool_call_record",
            "id": "0f0a5c2e-1d3b-4c5a-8e7f-9a0b1c2d3e4f",
            "tool_name": "fs_read",
            "call_id": "call_ah82ks",
            "status": "completed",
            "success": False,
            "is_error": True,
            "error_type": "not_found",
            "error_message": "no such file: notes/missing.md",
            "arguments": {"path": "notes/missing.md"},
            "duration_ms": 42,
        },
    },
    maturity="placeholder",
)
class ToolTraceCallDetail(KindModel):
    """Everything known about ONE call_id — the forensic view.

    NOT a ``tool_trace_event_page``: this is a single call, so the events are
    always VERBOSE and unpaged, and it carries the joined call record the page
    shape has no room for. ``tool_call`` is None when trace events exist but the
    cx_tool_call row does not (the call died before the row was written — the
    exact case this tool is used to investigate).
    """

    call_id: str = ""
    events: list[ToolTraceEvent] = []
    tool_call: ToolCallRecord | None = None
