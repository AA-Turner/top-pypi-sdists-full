"""Shared dashboard observability helpers for session and loop projections."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from packages.operator import DashboardDetailItem, DashboardOpsRecord, DashboardSessionRecord
from packages.security import ApprovalClass, PolicyDecision, RiskLevel, SecurityAuditEvent

from .api_runtime_support import _optional_datetime, _optional_str
from .api_runtime_dashboard_graphs import load_dashboard_activity_graph


def _relative_age(value: datetime | None, *, now: datetime) -> str:
    if value is None:
        return "n/a"
    delta_seconds = max(0, int((now - value).total_seconds()))
    if delta_seconds < 5:
        return "now"
    if delta_seconds < 3600:
        return f"{max(1, delta_seconds // 60)}m ago"
    if delta_seconds < 86_400:
        return f"{max(1, delta_seconds // 3600)}h ago"
    if delta_seconds < 604_800:
        return f"{max(1, delta_seconds // 86_400)}d ago"
    return value.astimezone().strftime("%b %d %H:%M")


def _display_timestamp(value: datetime | None, *, now: datetime) -> str:
    if value is None:
        return "n/a"
    return f"{_relative_age(value, now=now)} ({value.astimezone().strftime('%Y-%m-%d %H:%M')})"


def _tone_for_status(status: str | None) -> str:
    normalized = str(status or "").strip().casefold()
    if normalized in {"ready", "ok", "configured", "healthy", "active", "completed", "scheduled"}:
        return "healthy"
    if normalized in {"preview", "missing", "pending", "paused", "interrupted", "stale", "degraded"}:
        return "attention"
    if normalized in {"failed", "error", "not-ready", "critical"}:
        return "critical"
    return "neutral"


def _provider_tone(doctor_status: str, embedding_status: str) -> str:
    normalized_embedding = str(embedding_status or "").strip().casefold()
    if doctor_status == "not-ready" or normalized_embedding in {"failed", "error"}:
        return "critical"
    if doctor_status == "preview" or normalized_embedding in {"pending", "missing", "cold", "disabled"}:
        return "attention"
    if doctor_status == "ready":
        return "healthy"
    return _tone_for_status(doctor_status)


def _session_status_counts(app) -> dict[str, int]:
    with app.repository.connection() as connection:
        rows = connection.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM sessions
            GROUP BY status
            """
        ).fetchall()
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["status"])] = int(row["count"])
    return counts


def _dashboard_clone_rows(app, *, limit: int = 12):
    with app.repository.connection() as connection:
        rows = connection.execute(
            """
            SELECT
                ci.clone_id,
                ci.profile_id,
                ci.display_name,
                ci.updated_at AS identity_updated_at,
                s.session_id,
                s.status AS session_status,
                s.updated_at AS session_updated_at
            FROM clone_identities AS ci
            LEFT JOIN sessions AS s
                ON s.session_id = (
                    SELECT s2.session_id
                    FROM sessions AS s2
                    WHERE s2.profile_id = ci.profile_id
                    ORDER BY s2.updated_at DESC, s2.started_at DESC, s2.session_id DESC
                    LIMIT 1
                )
            ORDER BY COALESCE(s.updated_at, ci.updated_at) DESC, ci.display_name ASC, ci.clone_id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return rows


def _compact_provider_label(active_provider: Mapping[str, object]) -> str:
    provider_id = str(active_provider.get("provider_id") or active_provider.get("source") or "not configured")
    model_id = str(active_provider.get("strong_model") or "").strip()
    if model_id:
        return f"{provider_id}:{model_id}"
    return provider_id


def _is_internal_resume_text(value: object) -> bool:
    text = " ".join(str(value or "").split()).casefold()
    return text.startswith("resume durable work from session")


def _dashboard_display_text(value: object, *, fallback: str, limit: int = 180) -> str:
    if _is_internal_resume_text(value):
        return fallback
    return _dashboard_safe_text(value, fallback=fallback, limit=limit)


def _dashboard_safe_text(value: object, *, fallback: str = "n/a", limit: int = 180) -> str:
    text = " ".join(str(value or "").split())
    if not text:
        return fallback
    redacted = SecurityAuditEvent(
        event_id="audit:dashboard:projection",
        request_id="dashboard:projection",
        approval_class=ApprovalClass.READ,
        decision=PolicyDecision.ALLOW,
        risk_level=RiskLevel.LOW,
        summary=text,
    ).to_record()["summary"]
    normalized = " ".join(str(redacted or "").split())
    if not normalized:
        return fallback
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _dashboard_session_rows(app, *, limit: int = 8):
    with app.repository.connection() as connection:
        rows = connection.execute(
            """
            SELECT session_id, profile_id, status, started_at, updated_at, parent_session_id, interruption_state
            FROM sessions
            ORDER BY updated_at DESC, started_at DESC, session_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return rows


def dashboard_graph_session_ids(app, *, limit: int = 12, max_sessions: int = 4) -> tuple[str, ...]:
    session_ids: list[str] = []
    seen: set[str] = set()
    for rows in (_dashboard_clone_rows(app, limit=limit), _dashboard_session_rows(app, limit=limit)):
        for row in rows:
            session_id = str(row["session_id"]) if row["session_id"] is not None else ""
            if not session_id or session_id in seen:
                continue
            seen.add(session_id)
            session_ids.append(session_id)
    return tuple(session_ids[: max(1, min(limit, max_sessions))])


def _dashboard_token_summary(latest_turn) -> str:
    if latest_turn is None:
        return "No recorded token usage yet."
    execution = latest_turn.outcome.execution
    summary = (
        f"{execution.total_tokens} total"
        f" | {execution.prompt_tokens} in"
        f" | {execution.completion_tokens} out"
    )
    if getattr(execution, "cache_usage_reported", False):
        summary = f"{summary} | {execution.cached_prompt_tokens} cached"
    return summary


def _dashboard_usage_summary(latest_turn, latest_run) -> str:
    model_turns = latest_run.model_turn_count if latest_run is not None else (1 if latest_turn is not None else 0)
    tool_calls = latest_run.tool_call_count if latest_run is not None else (
        len(latest_turn.outcome.execution.tool_calls) if latest_turn is not None else 0
    )
    if model_turns == 0 and tool_calls == 0:
        return "No tool or model turns recorded yet."
    summary = f"{model_turns} model turn(s) | {tool_calls} tool call(s)"
    if latest_turn is not None:
        execution = latest_turn.outcome.execution
        if getattr(execution, "cache_usage_reported", False) and execution.prompt_tokens > 0:
            cache_hit_rate = (execution.cached_prompt_tokens / execution.prompt_tokens) * 100
            summary = f"{summary} | cache hit {cache_hit_rate:.1f}%"
    return summary


def _dashboard_model_label(active_provider: Mapping[str, object]) -> str:
    model = str(active_provider.get("strong_model") or active_provider.get("weak_model") or "").strip()
    return model or "not configured"


def build_dashboard_observability(
    app,
    *,
    now: datetime,
    active_provider: Mapping[str, object],
    runs,
    jobs,
    limit: int = 12,
):
    latest_run_by_session: dict[str, Any] = {}
    for run in runs:
        latest_run_by_session.setdefault(run.session_id, run)

    session_records: list[DashboardSessionRecord] = []
    session_display_names: dict[str, str] = {}
    ops_entries: list[tuple[datetime, DashboardOpsRecord]] = []

    for row in _dashboard_session_rows(app, limit=limit):
        session_id = str(row["session_id"])
        session = app.repository.load_session(session_id)
        if session is None:
            continue
        profile = app.repository.load_profile(session.profile_id)
        graph, graph_issue = load_dashboard_activity_graph(app, session_id=session_id)
        continuity_state = None if graph_issue is not None else app.inspect_continuity(session_id)
        latest_turn = app._turns.get(session_id, ())[-1] if app._turns.get(session_id) else None
        latest_run = latest_run_by_session.get(session_id)
        active_goal = (
            graph.goal(graph.active_goal_id)
            if graph is not None and graph.active_goal_id is not None
            else None
        )
        display_name = str(profile.display_name if profile is not None else session.profile_id)
        session_display_names[session_id] = display_name
        conversation = _dashboard_display_text(
            latest_turn.request.get("prompt") if latest_turn is not None else (
                latest_run.prompt if latest_run is not None else (
                    active_goal.title if active_goal is not None else (
                        continuity_state.wake_summary
                        if continuity_state is not None
                        else "Persisted activity graph failed validation."
                    )
                )
            ),
            fallback="Continuity resume recorded." if latest_run is not None else (
                active_goal.title if active_goal is not None else "No recent conversation yet."
            ),
            limit=120,
        )
        log_line = _dashboard_display_text(
            latest_turn.outcome.execution.summary if latest_turn is not None else (
                latest_run.last_summary if latest_run is not None else (
                    continuity_state.wake_summary
                    if continuity_state is not None
                    else "Persisted activity graph failed validation."
                )
            ),
            fallback=(
                "Persisted activity graph failed validation."
                if graph_issue is not None
                else ("Wake completed without a public summary." if latest_run is not None else "No recent log line yet.")
            ),
            limit=180,
        )
        continuity_label = (
            continuity_state.continuity.summary
            if continuity_state is not None
            else "graph validation failed"
        )
        tone = "neutral"
        if latest_run is not None and latest_run.status == "failed":
            continuity_label = _dashboard_display_text(
                latest_run.waiting_reason,
                fallback="wake failed",
                limit=72,
            )
            tone = "critical"
        elif latest_run is not None and latest_run.status == "pending":
            continuity_label = _dashboard_display_text(
                latest_run.waiting_reason,
                fallback="wake waiting",
                limit=72,
            )
            tone = "attention"
        elif session.status == "interrupted":
            continuity_label = _dashboard_display_text(
                session.interruption_state,
                fallback="interrupted",
                limit=72,
            )
            tone = "attention"
        elif continuity_state is not None and continuity_state.continuity.continuity.requires_recovery:
            tone = "attention"
        elif latest_turn is not None or latest_run is not None:
            tone = "healthy"
        if graph_issue is not None:
            continuity_label = "activity graph invalid"
            tone = "critical"
            if latest_turn is None and latest_run is None:
                log_line = _dashboard_safe_text(
                    graph_issue.detail,
                    fallback="Persisted activity graph failed validation.",
                    limit=180,
                )
        continuity_label = _dashboard_display_text(
            continuity_label,
            fallback="Continuity resume recorded.",
            limit=96,
        )
        last_touch = max(
            session.updated_at,
            latest_turn.recorded_at if latest_turn is not None else session.updated_at,
            latest_run.updated_at if latest_run is not None else session.updated_at,
        )
        session_details = [
            DashboardDetailItem("Session", session_id),
            DashboardDetailItem("Status", session.status),
        ]
        if row["parent_session_id"] is not None:
            session_details.append(DashboardDetailItem("Parent", str(row["parent_session_id"])))
        if graph_issue is not None:
            session_details.append(DashboardDetailItem("Graph", graph_issue.detail))
        if active_goal is not None:
            session_details.append(
                DashboardDetailItem(
                    "Goal",
                    _dashboard_safe_text(active_goal.title, fallback=active_goal.goal_id, limit=80),
                )
            )
        if latest_run is not None:
            wake_detail = latest_run.status
            if latest_run.status == "pending" and latest_run.waiting_reason:
                wake_detail = _dashboard_display_text(
                    latest_run.waiting_reason,
                    fallback="wake waiting",
                    limit=72,
                )
            elif latest_run.status == "failed" and latest_run.waiting_reason:
                wake_detail = _dashboard_display_text(
                    latest_run.waiting_reason,
                    fallback="wake failed",
                    limit=72,
                )
            session_details.append(
                DashboardDetailItem(
                    "Wake",
                    _dashboard_safe_text(wake_detail, fallback=latest_run.status, limit=72),
                )
            )
        elif session.interruption_state:
            session_details.append(
                DashboardDetailItem(
                    "Interrupt",
                    _dashboard_display_text(
                        session.interruption_state,
                        fallback="Continuity resume marker.",
                        limit=220,
                    ),
                )
            )
        session_records.append(
            DashboardSessionRecord(
                thread=display_name,
                conversation=conversation,
                log=log_line,
                model=_dashboard_model_label(active_provider),
                tokens=_dashboard_token_summary(latest_turn),
                usage=_dashboard_usage_summary(latest_turn, latest_run),
                continuity=_dashboard_safe_text(continuity_label, fallback=session.status, limit=96),
                last_touch=_relative_age(last_touch, now=now),
                tone=tone,
                details=tuple(session_details),
            )
        )

    for run in runs[:6]:
        lane = session_display_names.get(run.session_id)
        if lane is None:
            session = app.repository.load_session(run.session_id)
            profile = app.repository.load_profile(session.profile_id) if session is not None else None
            lane = str(profile.display_name if profile is not None else f"session:{run.session_id}")
        outcome = run.status if run.status != "pending" else (
            f"pending: {_dashboard_display_text(run.waiting_reason, fallback='waiting', limit=72)}"
            if run.waiting_reason
            else "pending"
        )
        ops_entries.append(
            (
                run.updated_at,
                DashboardOpsRecord(
                    lane=lane,
                    event="Wake run",
                    source="agent_runs",
                    summary=_dashboard_display_text(
                        run.last_summary or run.prompt,
                        fallback="Wake run recorded continuity progress.",
                        limit=180,
                    ),
                    outcome=outcome,
                    age=_relative_age(run.updated_at, now=now),
                    tone="critical" if run.status == "failed" else _tone_for_status(run.status),
                ),
            )
        )

    sorted_jobs = sorted(
        jobs,
        key=lambda item: (item.last_run_at or item.updated_at, item.updated_at, item.name),
        reverse=True,
    )
    for job in sorted_jobs[:4]:
        job_timestamp = job.last_run_at or job.updated_at
        ops_entries.append(
            (
                job_timestamp,
                DashboardOpsRecord(
                    lane=job.name,
                    event="Cron execution",
                    source="cron",
                    summary=_dashboard_safe_text(
                        job.last_summary or f"{job.schedule_text}; next {_display_timestamp(job.next_run_at, now=now)}",
                        fallback="Cron job has not recorded a run yet.",
                    ),
                    outcome=job.status,
                    age=_relative_age(job_timestamp, now=now),
                    tone=_tone_for_status(job.status),
                ),
            )
        )

    telemetry_count = 0
    for event in reversed(app.telemetry.events):
        if event.get("event_type") != "kernel.stage":
            continue
        payload = event.get("payload")
        if not isinstance(payload, Mapping):
            continue
        recorded_at = _optional_datetime(payload.get("recorded_at")) or now
        stage_name = _dashboard_safe_text(payload.get("stage"), fallback="stage", limit=48)
        detail = _dashboard_safe_text(payload.get("detail"), fallback="Kernel stage observed.")
        session_id = _optional_str(event.get("session_id"))
        lane = session_display_names.get(session_id or "")
        if lane is None:
            lane = f"session:{session_id}" if session_id else "kernel"
        ops_entries.append(
            (
                recorded_at,
                DashboardOpsRecord(
                    lane=lane,
                    event=f"Kernel {stage_name}",
                    source="telemetry",
                    summary=detail,
                    outcome="observed",
                    age=_relative_age(recorded_at, now=now),
                    tone="neutral",
                ),
            )
        )
        telemetry_count += 1
        if telemetry_count >= 4:
            break

    ops_entries.sort(key=lambda item: item[0], reverse=True)
    return tuple(session_records), tuple(item[1] for item in ops_entries[:10])


__all__ = [
    "_compact_provider_label",
    "_dashboard_clone_rows",
    "_display_timestamp",
    "_provider_tone",
    "_relative_age",
    "_session_status_counts",
    "_tone_for_status",
    "build_dashboard_observability",
]
