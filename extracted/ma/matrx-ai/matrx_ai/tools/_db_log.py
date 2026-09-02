"""DB-backed companion to ``_debug_log``.

The flat-file sink at ``.matrx-debug/tool-trace-*.log`` lives only for the
lifetime of a Python process (and a Docker container). This module mirrors
every dispatch event into the ``cx_tool_trace`` table so traces survive
deploys and become queryable by the admin API / triage agents.

Contract:
  - ``db_log_event`` queues synchronously into the active request Coordinator.
    It returns a no-op coroutine only for compatibility with existing
    ``detached_task(db_log_event(...))`` callers. Detachment therefore happens
    after the write has joined the request's transactional DAG.
  - Any exception is swallowed — telemetry must never surface as a tool error.
  - Disabled via ``MATRX_TOOL_DEBUG_DB_DISABLED=1`` (separate knob from
    the file sink's ``MATRX_TOOL_DEBUG_LOG_DISABLED=1``) so an operator
    can keep file logs while quieting DB writes — e.g. in a tight loop
    where they don't want to fill the table.

Schema lives at [db/migrations/0044_cx_tool_trace.sql](../../../../db/migrations/0044_cx_tool_trace.sql).

AMBIENT TRACE TAGS: any caller may stamp every trace row produced under its
scope by putting a dict on ``AppContext.metadata[TRACE_TAGS_CONTEXT_KEY]``.
The tags are merged into ``chat.tool_trace.metadata`` under ``matrx_trace_tags``
(never over the row's own keys). This is deliberately generic — the tool layer
must not learn what a "replay" or a "shadow run" is; it only carries whatever
label the scope declared. First consumer: Hindsight replay (aidream), which
tags every dispatch with its replay id and the database it landed on.
"""

from __future__ import annotations

import json
import os
from collections.abc import Coroutine
from datetime import datetime
from typing import Any

# Reuse the file sink's process-start timestamp so trace rows correlate with
# the file they share a process with. Lazy because ``_debug_log`` may not be
# importable in all contexts (e.g. minimal test runs).
from ._debug_log import _PROCESS_START, sinks_disabled_by_stage
from .fault import classify_fault

#: Reserved ``AppContext.metadata`` key holding a dict of labels to stamp on
#: every tool trace produced inside that context. Same name on both sides —
#: the setter (a host feature) and the reader (this sink).
TRACE_TAGS_CONTEXT_KEY = "matrx_trace_tags"


def _ambient_trace_tags() -> dict[str, Any] | None:
    # An unreadable context costs a label, never a dispatch.
    try:
        from matrx_ai.context import try_get_app_context

        app_ctx = try_get_app_context()
        if app_ctx is None:
            return None
        tags = (getattr(app_ctx, "metadata", None) or {}).get(TRACE_TAGS_CONTEXT_KEY)
        return dict(tags) if isinstance(tags, dict) and tags else None
    except Exception:
        return None


def _truncate_text(value: Any, limit: int = 4096) -> str | None:
    """Cap string fields at 4 KB. Generous enough to keep the actionable
    detail; small enough to avoid blowing up row sizes in the hot path."""
    if value is None:
        return None
    s = str(value) if not isinstance(value, str) else value
    if len(s) <= limit:
        return s
    return s[: limit - 3] + "..."


def _coerce_args(args: Any) -> dict[str, Any] | None:
    """``args`` lands here as either a dict (preferred) or a pre-serialised
    JSON string (from the executor's truncated args blob). Both are
    accepted; non-dict / non-string inputs are dropped."""
    if args is None:
        return None
    if isinstance(args, dict):
        return args
    if isinstance(args, str):
        try:
            parsed = json.loads(args)
            return parsed if isinstance(parsed, dict) else {"_raw": args}
        except (json.JSONDecodeError, ValueError):
            return {"_raw": args}
    return None


def _is_disabled() -> bool:
    # Same stage guard as the file sink — a pytest run's deliberate failure
    # fixtures must never land in `cx_tool_trace` and outnumber real traffic.
    return os.environ.get("MATRX_TOOL_DEBUG_DB_DISABLED") == "1" or sinks_disabled_by_stage()


def _queue_db_log_event(
    event: str,
    *,
    tool_name: str,
    kind: str | None = None,
    duration_ms: int | None = None,
    args: Any = None,
    result_preview: Any = None,
    err_type: str | None = None,
    err_msg: str | None = None,
    conversation_id: str | None = None,
    call_id: str | None = None,
    user_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Queue a trace into the request Coordinator before any detachment.

    The public compatibility wrapper is scheduled by the dispatch path, but
    this function itself runs immediately and performs no DB round-trip.

    Parameters mirror the file-sink ``_debug_log.log_event`` keys, plus
    full IDs (the file sink truncates ``conv`` to 8 chars; the DB stores
    the full UUID so the admin API can join cleanly).
    """
    if _is_disabled():
        return

    # Client host: cx_tool_trace is a server-DB table. A host with a
    # conversation_store configured owns its own tool telemetry through the
    # store's log_tool_call_* rows — skip cleanly instead of importing cxm
    # just to swallow a DBNotConfiguredError on every dispatch.
    try:
        from matrx_ai.client_host import get_conversation_store

        if get_conversation_store() is not None:
            return
    except Exception:
        pass

    # EPHEMERAL RUN — no conversation row exists, and tool_trace.conversation_id
    # is NOT NULL with an FK to it. Queuing this row makes the turn's commit
    # barrier fail on a foreign-key violation and KILLS the request: any
    # incognito / stateless run whose agent touched a tool died here. A durable
    # trace pointing at a conversation that will never exist is meaningless
    # anyway; the file sink still records the full dispatch.
    try:
        from matrx_ai.context import try_get_app_context

        app_ctx = try_get_app_context()
        if app_ctx is not None and getattr(app_ctx, "store", True) is False:
            return
    except Exception:
        pass

    try:
        row_metadata: dict[str, Any] = dict(metadata or {})
        tags = _ambient_trace_tags()
        if tags is not None:
            row_metadata.setdefault(TRACE_TAGS_CONTEXT_KEY, tags)
        row: dict[str, Any] = {
            "event": event,
            "tool_name": tool_name,
            "process_pid": os.getpid(),
            "process_started_at": _PROCESS_START.isoformat(),
            "ts": datetime.now(_PROCESS_START.tzinfo).isoformat(),
            "metadata": row_metadata,
        }

        if kind is not None:
            row["kind"] = kind
        if duration_ms is not None:
            row["duration_ms"] = int(duration_ms)
        if conversation_id:
            row["conversation_id"] = conversation_id
        if call_id:
            row["call_id"] = call_id
        if user_id:
            row["created_by"] = user_id
        if err_type:
            row["err_type"] = err_type
        if err_msg:
            row["err_msg"] = _truncate_text(err_msg, 4096)

        # The single field the admin dashboard uses to split "the model passed
        # bad arguments" from "the tool definition is broken". Derived from the
        # same mapping the file sink + cx_tool_call use (matrx_ai.tools.fault).
        # A DELEGATED dispatch (call handed to the client, loop suspended) is
        # not a failure — classify it 'ok' unless it carries an err_type.
        row["fault_domain"] = classify_fault(
            err_type, success=(event in ("OK", "DELEGATED") and not err_type)
        )

        coerced_args = _coerce_args(args)
        if coerced_args is not None:
            row["args"] = coerced_args

        if result_preview is not None:
            if isinstance(result_preview, str):
                row["result_preview"] = _truncate_text(result_preview, 4096)
            else:
                try:
                    row["result_preview"] = _truncate_text(
                        json.dumps(result_preview, default=str), 4096
                    )
                except Exception:
                    row["result_preview"] = _truncate_text(str(result_preview), 4096)

        from uuid import uuid4

        try:
            from matrx_ai.persistence.queue_helpers import (
                get_coordinator,
                queue_tool_trace_create,
            )
        except Exception:
            return
        if get_coordinator() is None:
            # Out-of-request telemetry has no parent DAG and is intentionally
            # not smuggled through a Session-of-one. A future caller that truly
            # needs it must use matrx-orm's reason-bearing direct-write exception.
            return
        queue_tool_trace_create(id=str(uuid4()), **row)
    except Exception:
        # Never raise from a telemetry write. The file sink is the
        # synchronous baseline; if the DB is down, we lose retention
        # but the request keeps moving.
        return


def db_log_event(event: str, **kwargs: Any) -> Coroutine[Any, Any, None]:
    """Compatibility surface that queues synchronously, before detachment.

    Existing callers pass the returned no-op coroutine to ``detached_task``.
    The important work has already entered the Coordinator by then, so clearing
    the child task's context can no longer sever the write dependency graph.
    """
    _queue_db_log_event(event, **kwargs)

    async def _queued() -> None:
        return None

    return _queued()
