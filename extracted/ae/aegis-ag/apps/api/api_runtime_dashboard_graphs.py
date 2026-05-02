"""Graph-focused dashboard projections."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from packages.contracts import ActivityGraph, GoalNode
from packages.operator import DashboardDetailItem, DashboardGraphRecord


def _count_label(count: int, singular: str, plural: str | None = None) -> str:
    noun = singular if count == 1 else (plural or f"{singular}s")
    return f"{count} {noun}"


def _goal_status_rollup(goals: tuple[GoalNode, ...]) -> str:
    if not goals:
        return "0 goals"
    counts: dict[str, int] = {}
    for goal in goals:
        counts[goal.status] = counts.get(goal.status, 0) + 1
    parts = [f"{count} {status}" for status, count in sorted(counts.items())]
    return ", ".join(parts)


def _first_non_empty(*values: str | None, fallback: str) -> str:
    for value in values:
        if value is None:
            continue
        normalized = str(value).strip()
        if normalized:
            return normalized
    return fallback


def _joined(values: tuple[str, ...], *, fallback: str) -> str:
    cleaned = tuple(item for item in values if str(item).strip())
    return ", ".join(cleaned) if cleaned else fallback


def _first_retrieval_note(context_result: Any) -> str | None:
    request = next(iter(context_result.plan.retrieval_requests), None)
    if request is None:
        return None
    return f"{request.request_id}: {', '.join(request.memory_ids) or 'none'} | {request.reason}"


def _procedure_overlay_reason(context_result: Any) -> str | None:
    for trace in context_result.source_trace:
        if trace.layer_name == "procedure_overlay":
            return trace.reason
    return None


def _graph_lane_label(app: Any, *, session_id: str, session: Any) -> str:
    profile = app.repository.load_profile(session.profile_id)
    display_name = _first_non_empty(
        getattr(profile, "display_name", None),
        getattr(session, "profile_id", None),
        fallback=f"session:{session_id}",
    )
    return f"{display_name} / {session_id}"


@dataclass(frozen=True, slots=True)
class DashboardActivityGraphIssue:
    session_id: str
    detail: str


def load_dashboard_activity_graph(
    app: Any,
    *,
    session_id: str,
) -> tuple[ActivityGraph | None, DashboardActivityGraphIssue | None]:
    try:
        return app.repository.load_activity_graph(session_id), None
    except ValueError as error:
        return None, DashboardActivityGraphIssue(
            session_id=session_id,
            detail=str(error).strip() or "persisted activity graph failed validation",
        )


def _build_invalid_graph_record(
    app: Any,
    *,
    session_id: str,
    session: Any,
    lane: str,
    issue: DashboardActivityGraphIssue,
    open_run: Any | None,
) -> DashboardGraphRecord:
    open_run_status = str(getattr(open_run, "status", "") or "").strip() or "none"
    return DashboardGraphRecord(
        lane=lane,
        graph="ActivityGraph",
        anchor=f"session:{session_id}",
        focus="Persisted activity graph needs repair before deep route drilldowns can resume.",
        state="invalid",
        blocker=issue.detail,
        support_path=(
            f"session_status={session.status}; "
            f"interruption={session.interruption_state or 'none'}; "
            f"open_run={open_run_status}"
        ),
        projection_health=(
            "graph validation failed before the dashboard could safely read goals, "
            "anchors, or downstream frame context"
        ),
        note=(
            "The dashboard keeps the invalid persisted graph explicit and degrades the affected "
            "lane instead of failing the entire operator projection."
        ),
        tone="critical",
        stats=(
            DashboardDetailItem("Session", session.session_id),
            DashboardDetailItem("Status", session.status),
            DashboardDetailItem("Interruption", session.interruption_state or "none"),
            DashboardDetailItem("Open run", open_run_status),
        ),
        sources=("ActivityGraph", "RuntimeStorageRepository", "SessionContinuityState"),
    )


def _build_session_graph_records(
    app: Any,
    *,
    session_id: str,
    open_run: Any | None,
) -> tuple[DashboardGraphRecord, ...]:
    session = app.repository.load_session(session_id)
    if session is None:
        return ()
    lane = _graph_lane_label(app, session_id=session_id, session=session)

    graph, graph_issue = load_dashboard_activity_graph(app, session_id=session_id)
    if graph_issue is not None:
        return (
            _build_invalid_graph_record(
                app,
                session_id=session_id,
                session=session,
                lane=lane,
                issue=graph_issue,
                open_run=open_run,
            ),
        )
    goals = graph.goals if graph is not None else ()
    goal_counts = graph.status_counts() if graph is not None else {}
    active_goal = (
        graph.goal(graph.active_goal_id)
        if graph is not None and graph.active_goal_id is not None
        else None
    )

    activity = app.inspect_activity_surface(session_id)
    context_result = app.inspect_context_frame(session_id)
    frame = context_result.frame
    trace_layers = tuple(dict.fromkeys(trace.layer_name for trace in context_result.source_trace))
    retrieval_requests = context_result.plan.retrieval_requests
    retrieval_layers = tuple(dict.fromkeys(request.layer_name for request in retrieval_requests))
    index_policy = app.memory_runtime.index_policy()

    open_run_status = str(getattr(open_run, "status", "") or "").strip()
    open_run_waiting_reason = str(getattr(open_run, "waiting_reason", "") or "").strip()
    active_goal_count = goal_counts.get("active", 0)
    focus_label = active_goal.title if active_goal is not None else activity.active_goal_reason

    activity_state = "idle"
    activity_blocker = "none"
    activity_tone = "neutral"
    if session.interruption_state:
        activity_state = "interrupted"
        activity_blocker = session.interruption_state
        activity_tone = "attention"
    elif open_run_status == "pending":
        activity_state = "queued"
        activity_blocker = open_run_waiting_reason or "wake queue is waiting for a retry condition"
        activity_tone = "attention"
    elif activity.wake_action in {"resume", "recover"}:
        activity_state = "recovery"
        activity_tone = "attention"
    elif active_goal is not None:
        activity_state = "focused"
        activity_tone = "healthy"
    elif goals:
        activity_state = "seeded"
        activity_blocker = "no active goal is selected"
        activity_tone = "attention"
    else:
        activity_blocker = "no goals are materialized yet"

    activity_record = DashboardGraphRecord(
        lane=lane,
        graph="ActivityGraph",
        anchor=_first_non_empty(
            active_goal.title if active_goal is not None else None,
            activity.active_goal_id,
            fallback=f"session:{session_id}",
        ),
        focus=_first_non_empty(focus_label, fallback="No active focus is projected yet."),
        state=activity_state,
        blocker=activity_blocker,
        support_path=(
            f"wake_action={activity.wake_action}; "
            f"wake_factors={len(activity.wake_factors)}; "
            f"revision={activity.goal_graph_revision or 'none'}"
        ),
        projection_health=(
            f"{_count_label(len(goals), 'goal')} projected, "
            f"{_count_label(active_goal_count, 'active goal')}, "
            f"statuses: {_goal_status_rollup(goals)}"
        ),
        note=activity.active_goal_reason,
        tone=activity_tone,
        stats=(
            DashboardDetailItem("Goal revision", activity.goal_graph_revision or "none"),
            DashboardDetailItem("Goals", str(len(goals))),
            DashboardDetailItem("Active goals", str(active_goal_count)),
            DashboardDetailItem("Wake factors", str(len(activity.wake_factors))),
        ),
        sources=("ActivityGraph", "SessionContinuityState", "AgentRunState"),
    )

    if activity.intent is None:
        intent_record = DashboardGraphRecord(
            lane=lane,
            graph="IntentProjection",
            anchor=activity.active_goal_id or f"session:{session_id}",
            focus="No resolved intent is recorded for the current focus lane yet.",
            state="awaiting turn",
            blocker="no turn-time intent decision is available",
            support_path=(
                f"opened_scopes={_joined(('session',), fallback='session')}; "
                "intent audit becomes available after the next recorded turn"
            ),
            projection_health="Intent audit has not been emitted for this session yet.",
            note="The dashboard keeps missing intent state explicit instead of inventing a synthetic decision.",
            tone="neutral",
            stats=(
                DashboardDetailItem("Focus ids", "0"),
                DashboardDetailItem("Opened scopes", "1"),
                DashboardDetailItem("Audit reasons", "0"),
                DashboardDetailItem("Embedding", "unknown"),
            ),
            sources=("IntentDecision", "memory_retrieval_scopes", "ActivityGraph"),
        )
    else:
        intent_detail = activity.intent
        intent_state = "resolved"
        intent_blocker = "none"
        intent_tone = "healthy"
        if intent_detail.embedding_status in {"failed", "unavailable"}:
            intent_state = "degraded"
            intent_blocker = f"embedding {intent_detail.embedding_status}"
            intent_tone = "critical"
        elif intent_detail.degradation_mode != "none":
            intent_state = "degraded"
            intent_blocker = intent_detail.degradation_mode
            intent_tone = "attention"
        elif intent_detail.fallback_path != "direct":
            intent_state = "fallback"
            intent_blocker = intent_detail.fallback_path
            intent_tone = "attention"
        elif intent_detail.confidence < 0.75:
            intent_state = "low confidence"
            intent_blocker = "confidence is below the steady-state threshold"
            intent_tone = "attention"
        focus_activity = _joined(intent_detail.focus_activity_ids, fallback="current activity")
        top_reason = (
            intent_detail.top_audit_reasons[0]
            if intent_detail.top_audit_reasons
            else "no audit reason captured"
        )
        intent_record = DashboardGraphRecord(
            lane=lane,
            graph="IntentProjection",
            anchor=intent_detail.focus_activity_ids[0] if intent_detail.focus_activity_ids else (activity.active_goal_id or f"session:{session_id}"),
            focus=f"{intent_detail.resolved_intent} -> {focus_activity}",
            state=intent_state,
            blocker=intent_blocker,
            support_path=(
                f"opened_scopes={_joined(intent_detail.opened_scopes, fallback='session')}; "
                f"resume={intent_detail.resume_signal}; "
                f"budget={intent_detail.budget_class}"
            ),
            projection_health=f"confidence={intent_detail.confidence:.2f}; {top_reason}",
            note=(
                f"fallback={intent_detail.fallback_path}; "
                f"embedding={intent_detail.embedding_status}; "
                f"weak_assist={intent_detail.weak_assist_state}"
            ),
            tone=intent_tone,
            stats=(
                DashboardDetailItem("Focus ids", str(len(intent_detail.focus_activity_ids))),
                DashboardDetailItem("Opened scopes", str(len(intent_detail.opened_scopes))),
                DashboardDetailItem("Confidence", f"{intent_detail.confidence:.2f}"),
                DashboardDetailItem("Embedding", intent_detail.embedding_status),
            ),
            sources=("IntentDecision", "memory_retrieval_scopes", "ActivityGraph"),
        )

    frame_layers = frame.layers() if frame is not None else ()
    frame_state = "assembled"
    frame_blocker = "none"
    frame_tone = "healthy" if frame is not None else "attention"
    if frame is None:
        frame_state = "missing"
        frame_blocker = "session frame did not materialize"
    elif frame.replay_packet is not None and context_result.retrieved_memory_ids:
        frame_state = "replay ready"
    elif retrieval_requests and not context_result.retrieved_memory_ids:
        frame_state = "thin recall"
        frame_blocker = "retrieval requests resolved without recalled memory ids"
        frame_tone = "attention"
    elif not retrieval_requests:
        frame_state = "snapshot ready"
        frame_tone = "neutral"

    frame_focus = _first_non_empty(
        frame.session_snapshot.summary if frame is not None else None,
        frame.replay_packet.summary if frame is not None and frame.replay_packet is not None else None,
        activity.active_goal_reason,
        fallback="No session-frame focus summary is available yet.",
    )
    frame_record = DashboardGraphRecord(
        lane=lane,
        graph="SessionFrame",
        anchor=f"session:{session_id}",
        focus=frame_focus,
        state=frame_state,
        blocker=frame_blocker,
        support_path=(
            f"trace_layers={_joined(trace_layers, fallback='none')}; "
            f"retrieval_layers={_joined(retrieval_layers, fallback='none')}"
        ),
        projection_health=(
            f"{_count_label(len(frame_layers), 'frame layer')}, "
            f"{_count_label(len(retrieval_requests), 'retrieval request')}, "
            f"{_count_label(len(context_result.retrieved_memory_ids), 'recalled memory id')}"
        ),
        note=_first_non_empty(
            context_result.plan.rationale,
            _procedure_overlay_reason(context_result),
            fallback="The session frame is assembled from stable prefix, session snapshot, replay, turn, and overlay layers.",
        ),
        tone=frame_tone,
        stats=(
            DashboardDetailItem("Frame layers", str(len(frame_layers))),
            DashboardDetailItem("Retrieval requests", str(len(retrieval_requests))),
            DashboardDetailItem("Recalled ids", str(len(context_result.retrieved_memory_ids))),
            DashboardDetailItem("Source trace", str(len(context_result.source_trace))),
        ),
        sources=("SessionFrame", "ContextAssemblyPlan", "ContextSourceTrace"),
    )

    evidence_state = "idle"
    evidence_blocker = "no recall request is open"
    evidence_tone = "neutral"
    if index_policy.rebuild_required:
        evidence_state = "rebuild required"
        evidence_blocker = index_policy.invalidation_reason or "derived evidence views are stale"
        evidence_tone = "attention"
    elif retrieval_requests or context_result.retrieved_memory_ids:
        evidence_state = "aligned"
        evidence_blocker = "none"
        evidence_tone = "healthy"

    evidence_record = DashboardGraphRecord(
        lane=lane,
        graph="EvidenceGraph",
        anchor=_count_label(index_policy.tracked_evidence_count, "tracked evidence row"),
        focus=(
            _count_label(len(context_result.retrieved_memory_ids), "recalled memory id")
            if context_result.retrieved_memory_ids
            else "No evidence rows were recalled for the current focus."
        ),
        state=evidence_state,
        blocker=evidence_blocker,
        support_path=(
            f"retrieval_layers={_joined(retrieval_layers, fallback='none')}; "
            f"opened_scopes={_joined(activity.intent.opened_scopes if activity.intent is not None else ('session',), fallback='session')}"
        ),
        projection_health=(
            index_policy.rebuild_plan.summary
            if index_policy.rebuild_plan is not None
            else (index_policy.invalidation_reason or "derived lexical and vector views are aligned with active evidence rows")
        ),
        note=_first_non_empty(
            _first_retrieval_note(context_result),
            fallback="Recall support remains explicit even when no retrieval request is open.",
        ),
        tone=evidence_tone,
        stats=(
            DashboardDetailItem("Tracked evidence", str(index_policy.tracked_evidence_count)),
            DashboardDetailItem("Invalidated ids", str(len(index_policy.invalidated_evidence_ids))),
            DashboardDetailItem("Recalled ids", str(len(context_result.retrieved_memory_ids))),
            DashboardDetailItem(
                "Dimensions",
                ", ".join(str(value) for value in index_policy.active_dimensions) or "n/a",
            ),
        ),
        sources=("EmbeddingIndexPolicy", "ContextRetrievalRequest", "EvidenceGraph"),
    )

    return (
        activity_record,
        intent_record,
        frame_record,
        evidence_record,
    )


def build_dashboard_graphs(
    app: Any,
    *,
    session_ids: tuple[str, ...],
    open_runs_by_session: Mapping[str, Any] | None = None,
) -> tuple[DashboardGraphRecord, ...]:
    records: list[DashboardGraphRecord] = []
    seen: set[str] = set()
    for raw_session_id in session_ids:
        session_id = str(raw_session_id or "").strip()
        if not session_id or session_id in seen:
            continue
        seen.add(session_id)
        records.extend(
            _build_session_graph_records(
                app,
                session_id=session_id,
                open_run=(open_runs_by_session or {}).get(session_id),
            )
        )
    return tuple(records)
