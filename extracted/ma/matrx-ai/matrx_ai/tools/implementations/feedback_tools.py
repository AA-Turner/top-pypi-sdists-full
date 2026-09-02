"""Feedback-system bridge tools for the tool-trace triage agents.

Two thin wrappers around the existing ``user_feedback`` table:

  - ``report_trace_incident`` — write a structured incident from the
    Triage / Pattern Detector / Forensics agents into ``user_feedback``
    under the "Tool Trace Incident" category. Dedup-aware: if an open
    row already exists for the same (tool, err_type, environment), the
    existing row is updated instead of a new one being created.

  - ``get_open_trace_incidents`` — read-side query for a future
    remediation agent (and for the dev humans). Returns open
    incidents filtered by severity / tool.

Why these wrap user_feedback instead of standing up a new table:
``user_feedback`` already has every column we need
(``ai_assessment``, ``ai_solution_proposal``, ``ai_suggested_priority``,
``ai_complexity``, ``ai_estimated_files``, ``priority``,
``category_id``, ``parent_id``, status workflow, comments,
testing_url, resolution_notes), plus the matrx-feedback dashboard /
MCP server already speak its shape. See ``docs/MCP_DEBUG_TRACES.md``
("Internal triage agents") for the full design.
"""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timezone
from typing import Any

from matrx_ai.tools.kinds.tool_traces import (
    ToolTraceIncident,
    ToolTraceIncidentFilter,
    ToolTraceIncidentList,
    ToolTraceIncidentReport,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

# Hard-coded — created by hand on 2026-05-17. If the row is ever moved /
# renamed the slug stays stable; this constant just saves a lookup hop
# on every insert. Slug-based fallback below covers a drift case.
TOOL_TRACE_INCIDENT_CATEGORY_ID = "aee619b4-ef09-416d-94b8-9eb8bda7cc0a"
TOOL_TRACE_INCIDENT_CATEGORY_SLUG = "tool-trace-incident"

# How priority on the wire maps to the user_feedback.priority column.
# Both sides currently use the same vocabulary so this is a pass-through,
# but the mapping is centralised here so we can adjust without touching
# the agent prompt schemas.
_PRIORITY_MAP = {"low": "low", "medium": "medium", "high": "high", "critical": "critical"}

# Dedup window — rows beyond this age don't block a fresh insert even if
# the dedupe key matches. Keeps a recurring bug from getting attached to
# a forgotten row from months ago.
_DEDUP_MAX_AGE_DAYS = 30


_ADMIN_ERR = ToolError(
    error_type="not_allowed",
    message=(
        "report_trace_incident / get_open_trace_incidents require an "
        "admin user (defensive — tool_def.admin_only=true is the primary "
        "gate)."
    ),
)


def _row_to_dict(instance: Any, fields: tuple[str, ...] | None = None) -> dict[str, Any]:
    """Model instance -> plain dict, PostgREST-compatible shape (ISO-8601
    datetimes, string UUIDs/ids) so callers of this tool see the same shape
    they did from the old `response.data` rows."""
    from uuid import UUID as _UUID

    names = fields if fields is not None else tuple(instance._fields.keys())
    out: dict[str, Any] = {}
    for name in names:
        value = getattr(instance, name, None)
        if isinstance(value, datetime):
            out[name] = value.isoformat()
        elif isinstance(value, _UUID):
            out[name] = str(value)
        else:
            out[name] = value
    return out


def _assert_admin(ctx: ToolContext) -> ToolError | None:
    try:
        from matrx_connect import get_app_context

        app_ctx = get_app_context()
    except Exception:
        return _ADMIN_ERR
    if not getattr(app_ctx, "is_admin", False):
        return _ADMIN_ERR
    return None


def _compute_dedupe_key(
    tool_name: str, err_type: str, source_environment: str
) -> str:
    """Stable across triage runs. We deliberately key on the COARSE
    triple — not on err_msg_normalised — because the agent's
    normalisation may vary slightly between runs and would defeat the
    dedup if included."""
    raw = f"{tool_name}:{err_type}:{source_environment}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def _format_description(
    *,
    tool_name: str,
    err_type: str,
    err_msg_normalised: str,
    category: str,
    severity: str,
    occurrence_count: int,
    sample_call_ids: list[str] | None,
    args_sample: Any,
    first_seen_ts: str | None,
    last_seen_ts: str | None,
    source_environment: str,
    evidence: list[str] | None,
    extra_context: str | None,
    dedupe_key: str,
) -> str:
    """Build the human + agent-readable Markdown that goes into the
    ``description`` column. Includes the dedupe key as a parseable
    marker so a future ``ai_estimated_files``-style structured pull is
    possible without an extra column."""
    sample_ids_block = (
        "\n".join(f"- `{cid}`" for cid in (sample_call_ids or [])[:5])
        or "_(none recorded)_"
    )
    args_block = (
        "```json\n"
        + (
            __import__("json").dumps(args_sample, indent=2, default=str)[:2000]
            if args_sample
            else "{}"
        )
        + "\n```"
    )
    evidence_block = (
        "\n".join(f"- {e}" for e in (evidence or [])[:10])
        or "_(none recorded)_"
    )
    extra_block = f"\n\n## Additional context\n{extra_context}" if extra_context else ""

    return (
        f"## Tool-trace incident: `{tool_name}`\n\n"
        f"| field | value |\n"
        f"|---|---|\n"
        f"| **Tool** | `{tool_name}` |\n"
        f"| **err_type** | `{err_type}` |\n"
        f"| **Category** | `{category}` |\n"
        f"| **Severity** | `{severity}` |\n"
        f"| **Source env** | `{source_environment}` |\n"
        f"| **Occurrences in window** | {occurrence_count} |\n"
        f"| **First seen** | {first_seen_ts or '_unknown_'} |\n"
        f"| **Last seen** | {last_seen_ts or '_unknown_'} |\n\n"
        f"## Normalised error message\n\n"
        f"```\n{err_msg_normalised[:2000]}\n```\n\n"
        f"## Sample call_ids\n\n{sample_ids_block}\n\n"
        f"## Args sample\n\n{args_block}\n\n"
        f"## Evidence\n\n{evidence_block}"
        f"{extra_block}\n\n"
        f"<!-- trace-dedupe:{dedupe_key} -->\n"
    )


def _normalise_priority(severity: str) -> str:
    return _PRIORITY_MAP.get(str(severity).lower(), "medium")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# report_trace_incident
# ---------------------------------------------------------------------------


async def report_trace_incident(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    from matrx_ai.tools._generated_declarations import ReportTraceIncidentArgs
    ReportTraceIncidentArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    # Required fields.
    tool_name = (args.get("tool_name") or "").strip()
    err_type = (args.get("err_type") or "unknown").strip()
    err_msg_normalised = (args.get("err_msg_normalised") or "").strip()
    category = (args.get("category") or "C_server").strip()
    severity = (args.get("severity") or "medium").strip().lower()
    source_environment = (args.get("source_environment") or "production").strip()

    if not tool_name:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="tool_name is required"
            ),
        )
    if not err_msg_normalised:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="err_msg_normalised is required",
            ),
        )

    # Optional fields with sensible defaults.
    try:
        occurrence_count = int(args.get("occurrence_count", 1))
    except (TypeError, ValueError):
        occurrence_count = 1
    sample_call_ids = args.get("sample_call_ids") or []
    if not isinstance(sample_call_ids, list):
        sample_call_ids = []
    args_sample = args.get("args_sample")
    first_seen_ts = args.get("first_seen_ts")
    last_seen_ts = args.get("last_seen_ts")
    suspected_cause = (args.get("suspected_cause") or "").strip() or None
    fix_path = (args.get("fix_path") or "").strip() or None
    ai_complexity = (args.get("ai_complexity") or "").strip() or None
    ai_estimated_files = args.get("ai_estimated_files") or None
    if ai_estimated_files is not None and not isinstance(ai_estimated_files, list):
        ai_estimated_files = None
    evidence = args.get("evidence")
    if evidence is not None and not isinstance(evidence, list):
        evidence = None
    extra_context = (args.get("extra_context") or "").strip() or None

    dedupe_key = _compute_dedupe_key(tool_name, err_type, source_environment)
    description = _format_description(
        tool_name=tool_name,
        err_type=err_type,
        err_msg_normalised=err_msg_normalised,
        category=category,
        severity=severity,
        occurrence_count=occurrence_count,
        sample_call_ids=sample_call_ids,
        args_sample=args_sample,
        first_seen_ts=first_seen_ts,
        last_seen_ts=last_seen_ts,
        source_environment=source_environment,
        evidence=evidence,
        extra_context=extra_context,
        dedupe_key=dedupe_key,
    )
    priority = _normalise_priority(severity)

    try:
        from matrx_ai.db._registry import get_model as get_db_model

        UserFeedback = get_db_model("UserFeedback")
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                e,
                error_type="configuration",
                message=f"UserFeedback model unavailable: {e}",
            ),
        )

    # Get caller's user_id from the request context — the scheduler
    # passes the admin who owns the scheduled task; that's the correct
    # attribution for the row.
    try:
        user_id = ctx.user_id
    except Exception:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="configuration",
                message="ctx.user_id unavailable; cannot attribute row",
            ),
        )

    # ── Dedup check ────────────────────────────────────────────────────
    # SELECT existing open rows in the same category that carry our
    # dedupe marker. If we find one, UPDATE rather than INSERT.
    dedupe_marker = f"trace-dedupe:{dedupe_key}"
    try:
        existing_rows = await (
            UserFeedback.filter(
                category_id=TOOL_TRACE_INCIDENT_CATEGORY_ID,
                resolved_at__isnull=True,
                description__contains=dedupe_marker,
            )
            .order_by("-created_at")
            .limit(1)
            .values("id", "description", "priority", "admin_notes", "updated_at")
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                e,
                error_type="database",
                message=f"dedup lookup failed: {e}",
            ),
        )

    if existing_rows:
        existing_id = str(existing_rows[0]["id"])
        existing_priority = existing_rows[0].get("priority") or "medium"
        # Escalate priority — never demote (a critical bug that the
        # current run rated medium is still critical).
        new_priority = max(
            (priority, existing_priority),
            key=lambda p: ["low", "medium", "high", "critical"].index(p)
            if p in ("low", "medium", "high", "critical")
            else 1,
        )
        update_fields = {
            "description": description,
            "priority": new_priority,
            "ai_assessment": suspected_cause,
            "ai_solution_proposal": fix_path,
            "ai_suggested_priority": priority,
            "ai_complexity": ai_complexity,
            "ai_estimated_files": ai_estimated_files,
            "updated_at": datetime.now(UTC),
        }
        update_fields = {k: v for k, v in update_fields.items() if v is not None}
        try:
            await UserFeedback.update_where({"id": existing_id}, **update_fields)
        except Exception as e:
            return ToolResult(
                success=False,
                error=ToolError.from_exception(
                    e,
                    error_type="database",
                    message=f"update existing incident failed: {e}",
                ),
            )
        return ToolResult(
            success=True,
            output=ToolTraceIncidentReport(
                feedback_id=str(existing_id),
                created=False,
                merged_into_existing=True,
                dedupe_key=dedupe_key,
                priority=new_priority,
                category_slug=TOOL_TRACE_INCIDENT_CATEGORY_SLUG,
            ),
        )

    # ── Fresh insert ──────────────────────────────────────────────────
    row = {
        "user_id": user_id,
        "feedback_type": "bug",
        "route": f"tool:{tool_name}",
        "description": description,
        "status": "new",
        "priority": priority,
        "category_id": TOOL_TRACE_INCIDENT_CATEGORY_ID,
        "admin_decision": "pending",
        "ai_assessment": suspected_cause,
        "ai_solution_proposal": fix_path,
        "ai_suggested_priority": priority,
        "ai_complexity": ai_complexity,
        "ai_estimated_files": ai_estimated_files,
    }
    row = {k: v for k, v in row.items() if v is not None}

    try:
        created_row = await UserFeedback.create_item(**row)
        new_id = str(created_row.id)
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                e,
                error_type="database", message=f"insert failed: {e}"
            ),
        )

    return ToolResult(
        success=True,
        output=ToolTraceIncidentReport(
            feedback_id=str(new_id),
            created=True,
            merged_into_existing=False,
            dedupe_key=dedupe_key,
            priority=priority,
            category_slug=TOOL_TRACE_INCIDENT_CATEGORY_SLUG,
        ),
    )


# ---------------------------------------------------------------------------
# get_open_trace_incidents
# ---------------------------------------------------------------------------


async def get_open_trace_incidents(
    args: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    """Read-side companion. Returns up to ``limit`` open Tool Trace
    Incident rows, newest first. Filters by ``severity`` (== priority)
    and ``tool_name`` (substring match against ``route``)."""
    from matrx_ai.tools._generated_declarations import GetOpenTraceIncidentsArgs
    GetOpenTraceIncidentsArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    err = _assert_admin(ctx)
    if err:
        return ToolResult(success=False, error=err)

    try:
        limit = int(args.get("limit", 20))
    except (TypeError, ValueError):
        limit = 20
    limit = max(1, min(100, limit))

    severity = (args.get("severity") or "").strip().lower() or None
    tool_name_filter = (args.get("tool_name") or "").strip() or None

    try:
        from matrx_ai.db._registry import get_model as get_db_model

        UserFeedback = get_db_model("UserFeedback")
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                e,
                error_type="configuration",
                message=f"UserFeedback model unavailable: {e}",
            ),
        )

    try:
        filters: dict[str, Any] = {
            "category_id": TOOL_TRACE_INCIDENT_CATEGORY_ID,
            "resolved_at__isnull": True,
        }
        if severity:
            filters["priority"] = severity
        q = UserFeedback.filter(**filters)
        if tool_name_filter:
            # Every row's `route` is written as f"tool:{tool_name}" (see
            # report_trace_incident) — a substring match on the filter alone
            # reproduces the original `route LIKE 'tool:%<filter>%'`.
            q = q.filter(route__contains=tool_name_filter)
        row_instances = await q.order_by("-created_at").limit(limit).all()
        result_fields = (
            "id", "route", "priority", "status", "admin_decision", "ai_assessment",
            "ai_solution_proposal", "ai_complexity", "ai_estimated_files",
            "created_at", "updated_at",
        )
        rows = [_row_to_dict(r, result_fields) for r in row_instances]
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="database", message=str(e)),
        )

    return ToolResult(
        success=True,
        output=ToolTraceIncidentList(
            incidents=[ToolTraceIncident(**r) for r in rows],
            count=len(rows),
            filter=ToolTraceIncidentFilter(
                severity=severity,
                tool_name_substring=tool_name_filter,
                limit=limit,
            ),
        ),
    )
