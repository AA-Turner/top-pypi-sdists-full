"""Client-side resolution of filesystem audit events to tool spans."""

from __future__ import annotations

from datetime import datetime

from plato.chronos.models import AttributionKind, AuditEventInput
from plato.utils.audit import AuditScopeContext
from plato.utils.tool_execution import ToolExecutionRecord


def _event_in_window(event_time: datetime, record: ToolExecutionRecord) -> bool:
    return record.started_at <= event_time <= record.ended_at


def _resolve_tool_records(
    event: AuditEventInput,
    records: list[ToolExecutionRecord],
) -> list[tuple[ToolExecutionRecord, AttributionKind]]:
    """Resolve an audit event to one or more tool records.

    Returns all matching records so that an event occurring during multiple
    parallel tool calls appears under every overlapping tool span.
    """
    pid_matches = [
        record
        for record in records
        if event.pid is not None and record.pid == event.pid and _event_in_window(event.timestamp, record)
    ]
    if pid_matches:
        return [(r, AttributionKind.pid) for r in pid_matches]

    child_pid_matches = [
        record
        for record in records
        if event.pid is not None and event.pid in record.child_pids and _event_in_window(event.timestamp, record)
    ]
    if child_pid_matches:
        return [(r, AttributionKind.child_pid) for r in child_pid_matches]

    window_matches = [record for record in records if _event_in_window(event.timestamp, record)]

    if not window_matches:
        return []

    if len(window_matches) == 1:
        return [(window_matches[0], AttributionKind.time_window)]

    # Multiple window matches — check if they're genuinely parallel (overlapping)
    # or sequential (one just happens to contain the event's timestamp).
    # Pick the narrowest window(s) to avoid greedy attribution.
    durations = [(r.ended_at - r.started_at).total_seconds() for r in window_matches]
    min_dur = min(durations)

    # If the narrowest window is ≤2x the shortest, treat them as parallel
    # (similar-length overlapping calls). Otherwise pick only the narrowest.
    parallel_threshold = min_dur * 2
    narrow = [r for r, d in zip(window_matches, durations) if d <= parallel_threshold]

    return [(r, AttributionKind.time_window) for r in narrow]


def _apply_attribution(
    event: AuditEventInput,
    matched_record: ToolExecutionRecord,
    attribution_kind: AttributionKind,
    scope_context: AuditScopeContext,
) -> AuditEventInput:
    return event.model_copy(
        update={
            "trace_id": matched_record.trace_id,
            "span_id": matched_record.span_id,
            "agent_id": matched_record.agent_id or scope_context.agent_id or None,
            "agent_name": matched_record.agent_name or scope_context.agent_name or None,
            "display_name": matched_record.display_name or scope_context.display_name or None,
            "audit_run_id": scope_context.audit_run_id or None,
            "tool_name": matched_record.tool_name,
            "attribution_kind": attribution_kind,
        }
    )


def _apply_fallback(
    event: AuditEventInput,
    scope_context: AuditScopeContext,
) -> AuditEventInput:
    return event.model_copy(
        update={
            "trace_id": scope_context.trace_id or None,
            "span_id": scope_context.span_id or None,
            "agent_id": scope_context.agent_id or None,
            "agent_name": scope_context.agent_name or None,
            "display_name": scope_context.display_name or None,
            "audit_run_id": scope_context.audit_run_id or None,
            "tool_name": None,
            "attribution_kind": AttributionKind.agent_span,
        }
    )


def resolve_audit_events_for_scope(
    events: list[AuditEventInput],
    *,
    scope_context: AuditScopeContext,
    tool_records: list[ToolExecutionRecord],
) -> list[AuditEventInput]:
    """Resolve each audit event to the strongest available tool span(s).

    Tool records are NOT pre-filtered by mount path.  A single tool span can
    touch multiple tracked workspaces, so every scope must resolve against the
    full run-global tool execution set.

    When an event falls within multiple overlapping tool windows (and cannot be
    disambiguated by PID), the event is duplicated across all matching spans so
    each tool call's audit view is complete.
    """
    resolved: list[AuditEventInput] = []
    for event in events:
        matches = _resolve_tool_records(event, tool_records)
        if not matches:
            resolved.append(_apply_fallback(event, scope_context))
            continue

        for matched_record, attribution_kind in matches:
            resolved.append(_apply_attribution(event, matched_record, attribution_kind, scope_context))

    return resolved
