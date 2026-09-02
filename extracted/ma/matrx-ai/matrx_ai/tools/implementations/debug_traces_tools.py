"""Debug-trace tools — agent-callable wrappers around the cx_tool_trace
DB sink and the local .matrx-debug file sink.

These tools are the registered counterparts of the 6 admin REST routes
in [aidream/api/routers/admin_debug_traces.py](../../../../../aidream/api/routers/admin_debug_traces.py)
and the 6 MCP tools in [aidream/api/mcp/debug_traces_server.py](../../../../../aidream/api/mcp/debug_traces_server.py).
Same logic, different surface — these run inside an agent's tool loop
via the standard matrx-ai dispatch path.

All tools are ``admin_only=true`` in ``tool_def`` so the framework gates
agent access at the registry layer; we also re-check ``ctx.is_admin``
defensively here so a misconfigured registry can't escalate privilege.

Designed to be called by the 3 internal triage agents:
  - Tool Trace Triage (5850891f-99a1-4961-b2e0-111a4d157ae9)
  - Tool Trace Pattern Detector (f62e1db4-7655-45ee-999c-7f879e549580)
  - Tool Call Forensics (f96a5ad2-9a66-419f-9c93-af56ea08124d)
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from matrx_ai.tools.kinds.tool_traces import (
    ToolCallRecord,
    ToolTraceCallDetail,
    ToolTraceEvent,
    ToolTraceEventPage,
    ToolTraceFile,
    ToolTraceFileListing,
    ToolTraceFileWindow,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

_ADMIN_ERR = ToolError(
    error_type="not_allowed",
    message=(
        "debug_traces_* tools require an admin user. The tool registry "
        "marks them admin_only=true; this fail-safe protects against a "
        "misconfigured registry."
    ),
)


def _assert_admin(ctx: ToolContext) -> ToolError | None:
    """Defensive admin gate — even though tool_def.admin_only=true should
    have stopped non-admin agents already. Returns a ``ToolError`` when
    blocked, ``None`` when allowed."""
    try:
        from matrx_connect import get_app_context

        app_ctx = get_app_context()
    except Exception:
        return _ADMIN_ERR
    if not getattr(app_ctx, "is_admin", False):
        return _ADMIN_ERR
    return None


def _parse_iso_ts(raw: str) -> datetime:
    """Accept ISO-8601 with or without trailing Z; return tz-aware datetime.
    Raises ValueError on bad input — caller turns this into ToolError."""
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


# A single cx_tool_trace row can carry up to ~13KB (args / result_preview /
# err_msg are each store-capped at 4096). At a list limit of hundreds that is
# hundreds of KB re-sent to the model on every loop iteration. So the list tools
# return COMPACT rows by default — enough to triage (which tool, which error) —
# and the agent drills into ONE call_id with debug_traces_by_call (or passes
# verbose=true) for the heavy args/result_preview/metadata fields.
_COMPACT_ERR_MSG_CAP = 600


def _row_to_dict(row: Any, *, verbose: bool = False) -> dict[str, Any]:
    """Serialise a cx_tool_trace ORM row to a plain dict for ToolResult.output.

    Compact by default (drops the heavy args/result_preview/metadata fields and
    trims err_msg). ``verbose=True`` returns the full wire shape that matches the
    admin REST routes — use it only on a narrowed query."""
    err_msg = row.err_msg or ""
    if not verbose and len(err_msg) > _COMPACT_ERR_MSG_CAP:
        err_msg = err_msg[:_COMPACT_ERR_MSG_CAP] + "…"
    out: dict[str, Any] = {
        "id": str(row.id),
        "ts": row.ts.isoformat() if row.ts else None,
        "event": row.event,
        "tool_name": row.tool_name,
        "kind": row.kind,
        "duration_ms": row.duration_ms,
        "err_type": row.err_type,
        "err_msg": err_msg,
        "conversation_id": str(row.conversation_id) if row.conversation_id else None,
        "call_id": row.call_id,
        # Output key stays `user_id` (stable tool-result name); column is created_by.
        "user_id": str(row.created_by) if row.created_by else None,
        "process_pid": row.process_pid,
    }
    if verbose:
        out["args"] = row.args
        out["result_preview"] = row.result_preview
        out["metadata"] = row.metadata
        out["process_started_at"] = (
            row.process_started_at.isoformat() if row.process_started_at else None
        )
    return out


def _events_result(
    rows: list[Any],
    *,
    verbose: bool,
    limit: int,
    filter_summary: str,
    tool_name: str,
    ctx: ToolContext,
    chronological: bool = False,
) -> ToolResult:
    """Project + count-cap a cx_tool_trace row list into a bounded ToolResult.

    ``rows`` MUST be ordered newest-first (``ORDER BY ts DESC``) so the cap
    keeps the newest events — failure-hunting cares about the END of a
    timeline. ``chronological=True`` re-sorts the kept page oldest-first for
    display (conversation timelines read causally) without changing WHICH
    rows are kept.

    Query one more than ``limit`` so a full page honestly reports "more exist".
    Compact rows are small and count-capped ⇒ the result is self-managed; verbose
    rows carry the un-capped heavy fields, so the universal size gate guards them."""
    from matrx_ai.tools.output_caps import cap_list

    events = [_row_to_dict(r, verbose=verbose) for r in rows]
    events, info = cap_list(events, limit=limit)
    if chronological:
        events = list(reversed(events))
    output: dict[str, Any] = {
        "events": [ToolTraceEvent(**e) for e in events],
        "count": info.total,
        "shown": info.shown,
        "verbose": verbose,
        "filter_summary": filter_summary,
    }
    if info.truncated:
        output["truncated"] = True
        order_note = (
            "newest kept, displayed oldest→newest"
            if chronological
            else "newest first"
        )
        output["note"] = (
            f"showing the newest {info.shown} of at least {info.total} "
            f"({order_note}); narrow the filter or raise `limit`."
        )
    if not verbose:
        output["detail_hint"] = (
            "compact rows — call debug_traces_by_call(call_id=…) or pass "
            "verbose=true for args / result_preview / metadata."
        )
    return ToolResult(
        success=True,
        output=ToolTraceEventPage(**output),
        output_self_capped=not verbose,
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


# ---------------------------------------------------------------------------
# debug_traces_list_files — local file sink directory listing
# ---------------------------------------------------------------------------


async def debug_traces_list_files(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    try:
        from matrx_ai.tools._debug_log import log_path
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="configuration", message=str(e)),
        )

    path = log_path()
    if path is None:
        return ToolResult(success=True, output=ToolTraceFileListing())
    log_dir = path.parent
    if not log_dir.exists():
        return ToolResult(
            success=True,
            output=ToolTraceFileListing(log_dir=str(log_dir)),
        )

    files: list[dict[str, Any]] = []
    for entry in sorted(log_dir.glob("tool-trace-*.log"), reverse=True):
        if entry.is_symlink():
            continue
        try:
            stat = entry.stat()
        except OSError:
            continue
        files.append(
            ToolTraceFile(
                name=entry.name,
                size_bytes=stat.st_size,
                modified_at=datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat(),
                is_header_only=stat.st_size <= 100,
            )
        )
    return ToolResult(
        success=True,
        output=ToolTraceFileListing(
            files=files, count=len(files), log_dir=str(log_dir)
        ),
    )


# ---------------------------------------------------------------------------
# debug_traces_get_file — stream one file's text
# ---------------------------------------------------------------------------


async def debug_traces_get_file(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    from matrx_ai.tools._generated_declarations import DebugTracesGetFileArgs
    DebugTracesGetFileArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    filename = (args.get("filename") or "").strip()
    if not filename:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="filename is required"),
        )
    if "/" in filename or "\\" in filename or filename.startswith("."):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="filename must be a bare basename (no path components)",
            ),
        )
    if not filename.startswith("tool-trace-") or not filename.endswith(".log"):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="filename must match tool-trace-*.log",
            ),
        )

    from matrx_ai.tools._debug_log import log_path

    path = log_path()
    if path is None:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="not_found",
                message="no active .matrx-debug directory on this server",
            ),
        )
    target = Path(path).parent / filename
    if not target.is_file():
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="not_found",
                message=f"no such trace file: {filename}",
            ),
        )

    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e)),
        )

    # A trace file is unbounded by size (verbose logging grows them to many MB).
    # Return a bounded window: `offset` chars in, up to `max_chars` (default the
    # soft cap). The agent pages through with successive offsets — it never has
    # to swallow a multi-MB file to read the part it needs.
    from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS, cap_text

    total_chars = len(text)
    try:
        offset = max(0, int(args.get("offset", 0) or 0))
        max_chars = int(args.get("max_chars") or TOOL_RESULT_SOFT_CAP_CHARS)
    except (TypeError, ValueError):
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="offset/max_chars must be int"),
        )
    max_chars = max(1, min(TOOL_RESULT_SOFT_CAP_CHARS, max_chars))
    window, info = cap_text(text[offset:], limit=max_chars)
    output: dict[str, Any] = {
        "filename": filename,
        "size_bytes": len(text.encode("utf-8")),
        "total_chars": total_chars,
        "offset": offset,
        "shown_chars": info.shown_chars,
        "content": window,
    }
    next_offset = offset + info.shown_chars
    if next_offset < total_chars:
        output["truncated"] = True
        output["next_offset"] = next_offset
        output["note"] = (
            f"showing chars {offset}-{next_offset} of {total_chars}; call again with "
            f"offset={next_offset} for more."
        )
    return ToolResult(
        success=True,
        output=ToolTraceFileWindow(**output),
        output_self_capped=True,
        tool_name="debug_traces_get_file",
        call_id=ctx.call_id,
    )


# ---------------------------------------------------------------------------
# debug_traces_recent — DB query with optional filters
# ---------------------------------------------------------------------------


async def debug_traces_recent(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    from matrx_ai.tools._generated_declarations import DebugTracesRecentArgs
    DebugTracesRecentArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    since_raw = args.get("since")
    event = args.get("event")
    tool_name_filter = args.get("tool_name")
    try:
        limit = int(args.get("limit", 200))
    except (TypeError, ValueError):
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="limit must be int"),
        )
    limit = max(1, min(1000, limit))
    verbose = bool(args.get("verbose"))

    if since_raw:
        try:
            cutoff = _parse_iso_ts(str(since_raw))
        except (ValueError, TypeError) as e:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"invalid 'since' timestamp: {e}",
                ),
            )
    else:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=1)

    try:
        from matrx_ai.db.cx_managers import cxm

        qs = cxm.tool_trace.model.filter(ts__gt=cutoff)
        if event:
            qs = qs.filter(event=event)
        if tool_name_filter:
            qs = qs.filter(tool_name=tool_name_filter)
        rows = await qs.order_by("-ts").limit(limit + 1).all()
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="database", message=str(e)),
        )

    summary_parts = [f"ts > {cutoff.isoformat()}"]
    if event:
        summary_parts.append(f"event={event}")
    if tool_name_filter:
        summary_parts.append(f"tool={tool_name_filter}")
    summary_parts.append(f"limit={limit}")
    return _events_result(
        rows,
        verbose=verbose,
        limit=limit,
        filter_summary=" ; ".join(summary_parts),
        tool_name="debug_traces_recent",
        ctx=ctx,
    )


# ---------------------------------------------------------------------------
# debug_traces_failures_since — convenience wrapper for the triage agent
# ---------------------------------------------------------------------------


async def debug_traces_failures_since(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    from matrx_ai.tools._generated_declarations import DebugTracesFailuresSinceArgs
    DebugTracesFailuresSinceArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    iso_ts = args.get("iso_ts")
    if not isinstance(iso_ts, str) or not iso_ts.strip():
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="iso_ts is required and must be an ISO-8601 string",
            ),
        )
    try:
        cutoff = _parse_iso_ts(iso_ts.strip())
    except (ValueError, TypeError) as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"invalid iso_ts: {e}",
            ),
        )
    verbose = bool(args.get("verbose"))
    try:
        limit = int(args.get("limit", 300))
    except (TypeError, ValueError):
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="limit must be int"),
        )
    limit = max(1, min(1000, limit))

    try:
        from matrx_ai.db.cx_managers import cxm

        rows = await (
            cxm.tool_trace.model.filter(ts__gt=cutoff, event="FAIL")
            .order_by("-ts")
            .limit(limit + 1)
            .all()
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="database", message=str(e)),
        )

    return _events_result(
        rows,
        verbose=verbose,
        limit=limit,
        filter_summary=f"event=FAIL ts > {cutoff.isoformat()}",
        tool_name="debug_traces_failures_since",
        ctx=ctx,
    )


# ---------------------------------------------------------------------------
# debug_traces_by_conv — full per-conversation timeline
# ---------------------------------------------------------------------------


async def debug_traces_by_conv(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    from matrx_ai.tools._generated_declarations import DebugTracesByConvArgs
    DebugTracesByConvArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    cid = args.get("conversation_id")
    if not isinstance(cid, str) or not cid.strip():
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="conversation_id is required",
            ),
        )
    try:
        limit = int(args.get("limit", 300))
    except (TypeError, ValueError):
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="limit must be int"),
        )
    limit = max(1, min(2000, limit))
    verbose = bool(args.get("verbose"))

    try:
        from matrx_ai.db.cx_managers import cxm

        # Fetch NEWEST rows (the end of the timeline is what failure-hunting
        # needs); _events_result re-sorts the kept page chronologically.
        rows = await (
            cxm.tool_trace.model.filter(conversation_id=cid.strip())
            .order_by("-ts")
            .limit(limit + 1)
            .all()
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="database", message=str(e)),
        )

    return _events_result(
        rows,
        verbose=verbose,
        limit=limit,
        filter_summary=f"conversation_id={cid.strip()} limit={limit}",
        tool_name="debug_traces_by_conv",
        ctx=ctx,
        chronological=True,
    )


# ---------------------------------------------------------------------------
# debug_traces_by_call — forensic detail for one call_id
# ---------------------------------------------------------------------------


async def debug_traces_by_call(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    from matrx_ai.tools._generated_declarations import DebugTracesByCallArgs
    DebugTracesByCallArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    call_id = args.get("call_id")
    if not isinstance(call_id, str) or not call_id.strip():
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="call_id is required",
            ),
        )
    call_id = call_id.strip()

    try:
        from matrx_ai.db.cx_managers import cxm

        # NB: .limit() is required before .all() — matrx-orm's QuerySet
        # silently returns empty without it. Mirror the other 3 handlers
        # in this module rather than rely on a default.
        trace_rows = await (
            cxm.tool_trace.model.filter(call_id=call_id)
            .order_by("ts")
            .limit(1000)
            .all()
        )
        tool_call_rows = await cxm.tool_call.filter_items(call_id=call_id)
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="database", message=str(e)),
        )

    # Forensic detail view — a SINGLE call_id, so verbose rows are appropriate.
    # The joined tool_call.output can be large (≤100K storage cap); cap it
    # surgically so this one detail read can't itself blow the model's context.
    from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS, cap_text

    events = [ToolTraceEvent(**_row_to_dict(r, verbose=True)) for r in trace_rows]
    tool_call: dict[str, Any] | None = None
    self_capped = True
    if tool_call_rows:
        r = tool_call_rows[0]
        output_val = r.output
        output_note = None
        if isinstance(output_val, str):
            output_val, info = cap_text(output_val, limit=TOOL_RESULT_SOFT_CAP_CHARS)
            if info.truncated:
                output_note = (
                    f"output trimmed to {info.shown_chars} of {info.total_chars} chars; "
                    f"read the raw trace file or cx_tool_call row for the full payload."
                )
        else:
            # A non-string (dict/list) output isn't surgically trimmable here —
            # don't falsely claim self-management; let the universal gate guard it.
            self_capped = False
        tool_call = {
            "id": str(r.id),
            "tool_name": r.tool_name,
            "call_id": r.call_id,
            "status": r.status,
            "success": r.success,
            "is_error": r.is_error,
            "error_type": r.error_type,
            "error_message": r.error_message,
            "arguments": r.arguments,
            "output": output_val,
            "output_chars": r.output_chars,
            "duration_ms": r.duration_ms,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "iteration": r.iteration,
            "conversation_id": (
                str(r.conversation_id) if r.conversation_id else None
            ),
            "user_id": str(r.created_by) if r.created_by else None,
        }
        if output_note:
            tool_call["output_note"] = output_note

    return ToolResult(
        success=True,
        output=ToolTraceCallDetail(
            call_id=call_id,
            events=events,
            tool_call=ToolCallRecord(**tool_call) if tool_call else None,
        ),
        output_self_capped=self_capped,
        tool_name="debug_traces_by_call",
        call_id=ctx.call_id,
    )
