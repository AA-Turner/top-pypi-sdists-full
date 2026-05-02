"""Planning service and scoring helpers."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from uuid import uuid4

from packages.contracts import (
    EventEnvelope,
    ExecutionResult,
    MemoryRecord,
    PlanDraft,
    PlanStep,
    SessionState,
    StructuredTurnRecord,
    StructuredTurnSlot,
    ActivityGraph,
)

from .model import (
    CandidateMove,
    ExecutionTracker,
    GoalGraph,
    GoalGraphLifecycleUpdate,
    GoalGraphNode,
    GoalStatus,
    goal_graph_to_activity_graph,
    activity_graph_to_goal_graph,
    MoveKind,
    PlanningDecision,
    PlanningMode,
    PlanningRationale,
    TemporalContext,
    _INITIATIVE_CONTINUITY_BONUS,
    _PRIORITY_POINTS,
    _STATUS_POINTS,
    _TIME_SENSITIVITY_POINTS,
    _continuity_note_bonus,
    _continuity_note_factors,
    _dedupe_strings,
    _dependencies_satisfied,
    _format_delta,
    _goal_similarity,
    _normalize_initiative,
    _now,
    _stringify,
)
from .signals import (
    _analyze_goal_signal,
    _goal_seed_text,
    _match_goal_for_signal,
    _new_goal_node,
    _status_for_signal,
)


_REPLAY_BLOCKER_MARKERS = (
    "blocked",
    "blocker",
    "blocking",
    "dependency",
    "failed",
    "failure",
    "missing",
    "retry",
    "stalled",
    "stuck",
    "wait on",
    "waiting on",
)
_REPLAY_CORRECTION_MARKERS = (
    "corrected",
    "correction",
    "fixed",
    "revised",
    "updated after correction",
)
_REPLAY_REJECTION_MARKERS = (
    "avoid",
    "instead of",
    "not chosen",
    "rather than",
    "reject",
    "rejected",
    "skip",
)
_REPLAY_SUCCESS_MARKERS = (
    "completed",
    "done",
    "outcome:ok",
    "passed",
    "resolved",
    "safe",
    "succeeded",
    "success",
)
_REPLAY_FAILURE_MARKERS = (
    "blocked",
    "error",
    "failed",
    "failure",
    "outcome:error",
    "outcome:failed",
    "paused",
)


@dataclass(frozen=True, slots=True)
class _ReplayFeedback:
    score: float = 0.0
    refs: tuple[str, ...] = ()
    factors: tuple[str, ...] = ()
    summary: str = ""


def _contains_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)



def _tuple_from_metadata(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item))
    if value is None:
        return ()
    cleaned = str(value).strip()
    return (cleaned,) if cleaned else ()



def _slot_from_metadata(value: object) -> StructuredTurnSlot:
    if not isinstance(value, dict):
        return StructuredTurnSlot()
    return StructuredTurnSlot(
        summary=str(value.get("summary", "")),
        detail=_tuple_from_metadata(value.get("detail")),
        compression=str(value.get("compression", "structured")),
        provenance=str(value.get("provenance", "")),
        source_refs=_tuple_from_metadata(value.get("source_refs")),
        linkage_refs=_tuple_from_metadata(value.get("linkage_refs")),
    )



def _structured_turn_from_memory(record: MemoryRecord | None) -> StructuredTurnRecord | None:
    if record is None or record.kind != "structured_turn":
        return None
    payload = record.metadata.get("structured_turn")
    if not isinstance(payload, dict):
        return None
    return StructuredTurnRecord(
        turn_id=str(payload.get("turn_id", record.memory_id)),
        session_id=str(payload.get("session_id", record.session_id)),
        source=str(payload.get("source", "runtime")),
        observation=_slot_from_metadata(payload.get("observation")),
        reasoning=_slot_from_metadata(payload.get("reasoning")),
        action=_slot_from_metadata(payload.get("action")),
        outcome=_slot_from_metadata(payload.get("outcome")),
        profile_id=str(payload.get("profile_id")) if payload.get("profile_id") is not None else None,
        workspace_id=str(payload.get("workspace_id")) if payload.get("workspace_id") is not None else None,
        source_event_id=str(payload.get("source_event_id")) if payload.get("source_event_id") is not None else record.source_event_id,
        reasoning_availability=str(payload.get("reasoning_availability", "summary_only")),
        reasoning_provenance=str(payload.get("reasoning_provenance", "runtime.decision_summary")),
        compression_tier=str(payload.get("compression_tier", "raw_turn")),
        work_item_ids=_tuple_from_metadata(payload.get("work_item_ids") or record.goal_refs),
        source_turn_ids=_tuple_from_metadata(payload.get("source_turn_ids")),
        correction_memory_ids=_tuple_from_metadata(payload.get("correction_memory_ids")),
        artifact_ids=_tuple_from_metadata(payload.get("artifact_ids")),
        created_at=record.created_at,
    )



def _replay_text(memory: MemoryRecord, goal: GoalGraphNode) -> str:
    turn = _structured_turn_from_memory(memory)
    if turn is None:
        return memory.content.lower()
    parts = [
        goal.title,
        memory.content,
        turn.observation.summary,
        turn.reasoning.summary,
        " ".join(turn.reasoning.detail),
        turn.action.summary,
        " ".join(turn.action.detail),
        turn.outcome.summary,
        " ".join(turn.outcome.detail),
        " ".join(turn.artifact_ids),
        " ".join(memory.tags),
    ]
    return " ".join(part.strip().lower() for part in parts if part and part.strip())



def _replay_match_weight(goal: GoalGraphNode, memory: MemoryRecord) -> float:
    turn = _structured_turn_from_memory(memory)
    if turn is None:
        return 0.0
    if goal.goal_id in turn.work_item_ids or goal.goal_id in memory.goal_refs:
        return 1.0
    if goal.parent_goal_id is not None and goal.parent_goal_id in turn.work_item_ids:
        return 0.65
    similarity = max(
        _goal_similarity(goal.title, turn.observation.summary),
        _goal_similarity(goal.title, turn.reasoning.summary),
        _goal_similarity(goal.title, turn.action.summary),
        _goal_similarity(goal.title, turn.outcome.summary),
        _goal_similarity(goal.title, memory.content),
    )
    if similarity >= 0.35:
        return max(0.45, similarity)
    return 0.0



def _replay_feedback_for(
    goal: GoalGraphNode,
    *,
    kind: MoveKind,
    memories: tuple[MemoryRecord, ...],
    temporal: TemporalContext,
) -> _ReplayFeedback:
    score = 0.0
    refs: list[str] = []
    factors: list[str] = []
    clauses: list[str] = []
    for memory in memories:
        weight = _replay_match_weight(goal, memory)
        if weight <= 0.0:
            continue
        turn = _structured_turn_from_memory(memory)
        if turn is None:
            continue
        text = _replay_text(memory, goal)
        blocker = _contains_marker(text, _REPLAY_BLOCKER_MARKERS)
        rejection = _contains_marker(text, _REPLAY_REJECTION_MARKERS)
        correction = bool(turn.correction_memory_ids) or "corrected" in memory.tags or _contains_marker(text, _REPLAY_CORRECTION_MARKERS)
        success = _contains_marker(text, _REPLAY_SUCCESS_MARKERS)
        failure = _contains_marker(text, _REPLAY_FAILURE_MARKERS)
        action_detail = bool(turn.action.summary or turn.action.detail)
        delta = 0.2 * weight
        memory_factors: list[str] = []
        memory_clauses: list[str] = []

        if blocker:
            memory_factors.append("replay-blocker-history")
            if correction or success:
                if kind in {"act_on_task", "update_plan"}:
                    delta += 0.35 * weight
                memory_clauses.append(f"{memory.memory_id} carries the earlier blocker analysis into the recovery path")
            elif kind == "update_plan":
                delta += 0.9 * weight
                memory_clauses.append(f"{memory.memory_id} preserved the earlier blocker analysis")
            elif kind == "ask_for_information":
                delta += 0.65 * weight
                memory_clauses.append(f"{memory.memory_id} shows the missing dependency still matters")
            else:
                delta -= 0.95 * weight
                memory_factors.append("replay-blocker-caution")
                memory_clauses.append(f"{memory.memory_id} warns against repeating the blocked path")

        if rejection:
            memory_factors.append("replay-rejected-option")
            if correction or success:
                delta += 0.35 * weight
                memory_clauses.append(f"{memory.memory_id} steers away from the previously rejected option")
            elif kind in {"update_plan", "ask_for_information"}:
                delta += 0.55 * weight
                memory_clauses.append(f"{memory.memory_id} kept a rejected option visible for re-planning")
            else:
                delta -= 0.45 * weight
                memory_clauses.append(f"{memory.memory_id} shows this option was previously rejected")

        if correction:
            memory_factors.append("replay-correction-history")
            if kind in {"update_plan", "ask_for_information"}:
                delta += 0.45 * weight
            else:
                delta += 0.45 * weight
            if turn.correction_memory_ids and kind == "act_on_task":
                delta += 0.55 * weight
                memory_factors.append("replay-corrected-path")
            memory_clauses.append(f"{memory.memory_id} records the corrected path instead of the stale one")

        if success and action_detail:
            memory_factors.append("replay-success-path")
            if kind == "act_on_task":
                delta += 1.15 * weight
            else:
                delta += 0.2 * weight
            memory_clauses.append(f"{memory.memory_id} retains a successful action chain for this goal")
        elif action_detail and failure and kind == "act_on_task":
            memory_factors.append("replay-action-gap")
            delta += 0.15 * weight
            memory_clauses.append(f"{memory.memory_id} keeps the unfinished action chain visible")

        if temporal.resumed and weight >= 1.0:
            delta += 0.15
            memory_factors.append("replay-resume-link")

        if delta == 0.0:
            continue
        score += delta
        refs.append(memory.memory_id)
        factors.extend(memory_factors)
        clauses.extend(memory_clauses)

    if not refs:
        return _ReplayFeedback()
    ordered_clauses = tuple(dict.fromkeys(clause for clause in clauses if clause))
    summary = ""
    if ordered_clauses:
        summary = "Replay evidence " + "; ".join(ordered_clauses[:3]) + "."
    return _ReplayFeedback(
        score=round(score, 3),
        refs=tuple(dict.fromkeys(refs)),
        factors=tuple(dict.fromkeys(factors)),
        summary=summary,
    )


def _deadline_score(deadline: datetime | None, now: datetime) -> float:
    if deadline is None:
        return 0.0
    delta = deadline - now
    hours = delta.total_seconds() / 3600.0
    if hours <= 0:
        return 1.4
    if hours <= 4:
        return 1.1
    if hours <= 24:
        return 0.7
    if hours <= 72:
        return 0.35
    return 0.1


def _staleness_score(goal: GoalGraphNode, temporal: TemporalContext, now: datetime) -> float:
    goal_idle_for = now - goal.updated_at
    if goal_idle_for < timedelta(0):
        goal_idle_for = timedelta(0)
    effective_idle = goal_idle_for
    if temporal.idle_for is not None and temporal.idle_for > effective_idle:
        effective_idle = temporal.idle_for
    if effective_idle < timedelta(hours=12):
        return 0.0
    severe = effective_idle >= timedelta(days=2)
    if goal.goal_id == temporal.active_goal_id and goal.status == "blocked":
        return 0.6 if severe else 0.35
    if goal.goal_id == temporal.active_goal_id:
        return 0.75 if severe else 0.4
    if goal.status == "blocked":
        return 0.45 if severe else 0.2
    if goal.goal_id in temporal.ready_goal_ids:
        return 0.2 if severe else 0.1
    return 0.0


def _continuity_score(goal: GoalGraphNode, graph: GoalGraph, temporal: TemporalContext) -> float:
    active_goal = graph.active_goal()
    if goal.goal_id == graph.active_goal_id:
        return 0.9
    if graph.active_goal_id is not None and goal.parent_goal_id == graph.active_goal_id:
        return 0.45
    if active_goal is not None and active_goal.parent_goal_id is not None and goal.parent_goal_id == active_goal.parent_goal_id:
        return 0.2
    if goal.goal_id == graph.root_goal_id:
        return 0.15
    if graph.root_goal_id is not None and goal.parent_goal_id == graph.root_goal_id:
        return 0.1
    if temporal.resumed and goal.goal_id in temporal.ready_goal_ids:
        return 0.1
    return 0.0


def _blocked_recovery_goal_ids(graph: GoalGraph, ready_goal_ids: tuple[str, ...]) -> tuple[str, ...]:
    active_goal = graph.active_goal()
    if active_goal is None or active_goal.status != "blocked":
        return ()
    ready = set(ready_goal_ids)
    recovery_goal_ids: list[str] = []
    for goal in graph.nodes:
        if goal.goal_id == active_goal.goal_id or goal.goal_id not in ready:
            continue
        if active_goal.parent_goal_id is not None and goal.parent_goal_id == active_goal.parent_goal_id:
            recovery_goal_ids.append(goal.goal_id)
            continue
        if goal.parent_goal_id == active_goal.goal_id:
            recovery_goal_ids.append(goal.goal_id)
            continue
        if graph.root_goal_id is not None and goal.parent_goal_id == graph.root_goal_id:
            recovery_goal_ids.append(goal.goal_id)
    return tuple(dict.fromkeys(recovery_goal_ids))


def _project_graph_surface(source_graph: GoalGraph | ActivityGraph, graph: GoalGraph) -> GoalGraph | ActivityGraph:
    if isinstance(source_graph, ActivityGraph):
        return goal_graph_to_activity_graph(graph)
    return graph


def _repair_score(goal: GoalGraphNode, temporal: TemporalContext) -> float:
    if temporal.blocked_active_goal_id is None:
        return 0.0
    if goal.goal_id == temporal.blocked_active_goal_id and temporal.recovery_goal_ids:
        return -1.4
    if goal.goal_id in temporal.recovery_goal_ids:
        return 1.2
    if goal.goal_id in temporal.ready_goal_ids:
        return 0.2
    return 0.0


def _kind_for_goal(goal: GoalGraphNode, temporal: TemporalContext, execution_tracker: ExecutionTracker | None) -> MoveKind:
    if goal.status == "blocked" or goal.goal_id in temporal.blocked_goal_ids:
        return "update_plan"
    if goal.status in {"deferred", "completed", "done", "failed", "dropped"}:
        return "defer_or_schedule"
    if goal.goal_id in temporal.overdue_goal_ids:
        return "act_on_task"
    if goal.goal_id in temporal.ready_goal_ids:
        if temporal.resumed and goal.goal_id == temporal.active_goal_id:
            return "act_on_task"
        if goal.status == "active":
            return "act_on_task"
        if execution_tracker and goal.goal_id in execution_tracker.in_flight_goal_ids:
            return "act_on_task"
        return "act_on_task"
    if goal.dependency_refs:
        return "ask_for_information"
    return "defer_or_schedule"


def _rationale_for(
    goal: GoalGraphNode,
    temporal: TemporalContext,
    kind: MoveKind,
    tracker: ExecutionTracker | None,
    *,
    now: datetime,
) -> tuple[str, tuple[str, ...]]:
    factors: list[str] = []
    sentences: list[str] = []

    if temporal.resumed:
        factors.append("session-resumed")
        if temporal.session_resume_reason:
            sentences.append(temporal.session_resume_reason)
        else:
            sentences.append("The session resumed from durable state.")

    if goal.status == "active":
        factors.append("active-goal")
        sentences.append("The active goal is already in progress, so continuing it preserves continuity.")
    elif goal.status == "queued":
        factors.append("queued-goal")
        sentences.append("The goal is queued and ready to be advanced.")
    elif goal.status == "proposed":
        factors.append("proposed-goal")
        sentences.append("The goal is proposed and available for selection.")
    elif goal.status == "blocked":
        factors.append("blocked-goal")
        sentences.append("The goal is blocked, so the planner should surface the blocker or re-plan.")
    elif goal.status == "deferred":
        factors.append("deferred-goal")
        sentences.append("The goal is deferred and should remain durable until a later resume or explicit reactivation.")
    elif goal.status in {"completed", "done"}:
        factors.append("completed-goal")
        sentences.append("The goal is completed and remains durable for inspection and handoff.")

    if temporal.blocked_active_goal_id is not None:
        if goal.goal_id in temporal.recovery_goal_ids:
            factors.append("blocked-goal-recovery")
            sentences.append(
                "The active goal is blocked, so the planner should recover through a ready adjacent goal instead of repeating the blocked step."
            )
        elif goal.goal_id == temporal.blocked_active_goal_id and temporal.recovery_goal_ids:
            factors.append("blocked-goal-suppressed")
            sentences.append(
                "A ready recovery path exists elsewhere in the graph, so the blocked active goal should not be selected again immediately."
            )

    if goal.deadline is not None:
        factors.append("deadline")
        if goal.deadline <= now:
            sentences.append("The deadline has passed, which raises urgency.")
        else:
            sentences.append(f"The deadline is approaching in {_format_delta(goal.deadline - now)}.")

    if goal.dependency_refs:
        factors.append("dependencies")
        if kind == "ask_for_information":
            sentences.append("One or more dependencies are still unresolved.")
        else:
            sentences.append("Its dependencies appear satisfiable from the current graph.")

    if tracker and goal.goal_id in tracker.in_flight_goal_ids:
        factors.append("in-flight")
        sentences.append("The execution tracker shows this goal is still in flight.")

    if goal.evidence_refs:
        factors.append("evidence")
        sentences.append("Durable evidence is attached to the goal, so the next step can stay grounded.")

    staleness_score = _staleness_score(goal, temporal, now)
    if staleness_score > 0:
        if goal.goal_id == temporal.active_goal_id and goal.status == "blocked":
            factors.append("stale-blocked-goal")
            sentences.append("The blocked active goal has sat idle long enough that the planner should force a visible re-plan.")
        elif goal.goal_id == temporal.active_goal_id:
            factors.append("stale-active-goal")
            sentences.append("The active goal has remained idle long enough that the planner should re-engage it explicitly.")
        elif goal.status == "blocked":
            factors.append("stale-blocked-goal")
            sentences.append("The blocked goal has lingered in the graph, so the planner should resolve it instead of letting it silently decay.")
        else:
            factors.append("stale-ready-goal")
            sentences.append("The ready goal has been waiting in durable state and deserves a fresh decision.")

    if not sentences:
        sentences.append("The selected move best balances priority, readiness, and continuity.")

    if kind == "act_on_task":
        sentences.append("The planner advances the work because the durable graph shows a ready goal.")
    elif kind == "update_plan":
        sentences.append("The planner updates the plan instead of advancing because blockers still need attention.")
    elif kind == "defer_or_schedule":
        sentences.append("The planner defers the goal so the wake loop can return to it later without losing state.")
    elif kind == "ask_for_information":
        sentences.append("The planner pauses to gather the missing information before advancing.")

    summary = " ".join(sentences)
    return summary, tuple(dict.fromkeys(factors))


def _progression_action_for(kind: MoveKind) -> str:
    if kind in {"act_on_task", "answer_directly"}:
        return "advance"
    if kind == "update_plan":
        return "replan"
    if kind == "ask_for_information":
        return "gather_information"
    return "defer"


def _planned_progression(
    graph: GoalGraph,
    goal: GoalGraphNode | None,
    kind: MoveKind,
) -> tuple[GoalStatus | None, str | None]:
    if goal is None:
        return None, graph.active_goal_id
    if kind in {"act_on_task", "answer_directly"}:
        return "active", goal.goal_id
    if kind == "defer_or_schedule":
        if goal.status in {"completed", "done"}:
            next_status = goal.status
        else:
            next_status = "deferred"
        next_active_goal_id = None if graph.active_goal_id == goal.goal_id else graph.active_goal_id
        return next_status, next_active_goal_id
    if kind == "update_plan":
        next_active_goal_id = None if graph.active_goal_id == goal.goal_id and goal.status == "blocked" else graph.active_goal_id
        return goal.status, next_active_goal_id
    return goal.status, graph.active_goal_id


def _progression_sentence(
    goal: GoalGraphNode | None,
    *,
    action: str,
    planned_status: GoalStatus | None,
    planned_active_goal_id: str | None,
) -> str:
    if goal is None:
        if action == "defer":
            return "The durable graph defers the goal set and keeps the active slot clear until a later wake cycle."
        return "No durable goal state changed because no actionable goal was selected."
    if action == "advance":
        return f'The durable graph keeps "{goal.title}" active as the next step.'
    if action == "replan":
        return f'The durable graph keeps "{goal.title}" {planned_status or goal.status} until the blocker is cleared.'
    if action == "gather_information":
        return f'The durable graph leaves "{goal.title}" {planned_status or goal.status} until missing information arrives.'
    if planned_active_goal_id is None:
        return f'The durable graph records "{goal.title}" as {planned_status or goal.status} and clears the active slot.'
    return f'The durable graph records "{goal.title}" as {planned_status or goal.status} while preserving active goal {planned_active_goal_id}.'


def _fallback_active_goal_id(graph: GoalGraph, *, exclude_goal_id: str | None = None) -> str | None:
    ready = [
        goal
        for goal in graph.ready_goals()
        if goal.goal_id != exclude_goal_id
    ]
    if not ready:
        return None
    ordered = sorted(
        ready,
        key=lambda goal: (
            _PRIORITY_POINTS[goal.priority],
            _STATUS_POINTS[goal.status],
            goal.updated_at,
        ),
        reverse=True,
    )
    return ordered[0].goal_id


def _reassign_active_goal(
    graph: GoalGraph,
    *,
    active_goal_id: str | None,
    revision_id: str,
    updated_at: datetime,
) -> GoalGraph:
    if graph.active_goal_id == active_goal_id and graph.revision_id == revision_id:
        return graph
    return replace(
        graph,
        active_goal_id=active_goal_id,
        revision_id=revision_id,
        updated_at=updated_at,
    )


def _ensure_single_active_goal(
    graph: GoalGraph,
    *,
    goal_id: str,
    revision_id: str,
    updated_at: datetime,
) -> GoalGraph:
    active = graph.active_goal()
    next_graph = graph
    if active is not None and active.goal_id != goal_id and active.status == "active":
        next_graph = next_graph.transition_goal(
            active.goal_id,
            status="queued",
            revision_id=revision_id,
            updated_at=updated_at,
            active_goal_id=active.goal_id,
        )
    focused = next_graph.goal(goal_id)
    if focused is None:
        return next_graph
    if focused.status != "active":
        next_graph = next_graph.transition_goal(
            goal_id,
            status="active",
            revision_id=revision_id,
            updated_at=updated_at,
            active_goal_id=goal_id,
        )
    return _reassign_active_goal(next_graph, active_goal_id=goal_id, revision_id=revision_id, updated_at=updated_at)


class TemporalReasoner:
    """Inspect the graph for time pressure and resume signals."""

    resume_gap: timedelta
    due_soon_window: timedelta

    def __init__(
        self,
        *,
        resume_gap: timedelta | None = None,
        due_soon_window: timedelta | None = None,
    ) -> None:
        self.resume_gap = timedelta(hours=6) if resume_gap is None else resume_gap
        self.due_soon_window = timedelta(days=1) if due_soon_window is None else due_soon_window

    def analyze(
        self,
        session: SessionState,
        graph: GoalGraph,
        *,
        now: datetime | None = None,
    ) -> TemporalContext:
        current = _now() if now is None else now
        resumed = session.interruption_state is not None or session.parent_session_id is not None
        session_resume_reason = None
        if resumed:
            session_resume_reason = "The session resumed from a prior collaboration and should continue the durable goal graph."

        ready_goal_ids: list[str] = []
        blocked_goal_ids: list[str] = []
        overdue_goal_ids: list[str] = []
        due_soon_goal_ids: list[str] = []

        indexed = graph.index()
        for goal in graph.nodes:
            dependencies_ready = _dependencies_satisfied(goal, indexed)
            if goal.status in {"proposed", "queued", "active"} and dependencies_ready:
                ready_goal_ids.append(goal.goal_id)
            if goal.status == "blocked" or (
                goal.status not in {"deferred", "completed", "done", "failed", "dropped"}
                and not dependencies_ready
            ):
                blocked_goal_ids.append(goal.goal_id)
            if goal.deadline is not None:
                delta = goal.deadline - current
                if delta <= timedelta(0):
                    overdue_goal_ids.append(goal.goal_id)
                elif delta <= self.due_soon_window:
                    due_soon_goal_ids.append(goal.goal_id)

        idle_for = None
        if session.interruption_state is not None:
            idle_for = current - session.updated_at
            if idle_for < timedelta(0):
                idle_for = None

        ordered_ready_goal_ids = tuple(dict.fromkeys(ready_goal_ids))
        ordered_blocked_goal_ids = tuple(dict.fromkeys(blocked_goal_ids))
        blocked_active_goal_id = graph.active_goal_id if graph.active_goal_id in ordered_blocked_goal_ids else None
        recovery_goal_ids = _blocked_recovery_goal_ids(graph, ordered_ready_goal_ids)

        return TemporalContext(
            resumed=resumed,
            session_resume_reason=session_resume_reason,
            active_goal_id=graph.active_goal_id,
            ready_goal_ids=ordered_ready_goal_ids,
            blocked_goal_ids=ordered_blocked_goal_ids,
            recovery_goal_ids=recovery_goal_ids,
            blocked_active_goal_id=blocked_active_goal_id,
            overdue_goal_ids=tuple(dict.fromkeys(overdue_goal_ids)),
            due_soon_goal_ids=tuple(dict.fromkeys(due_soon_goal_ids)),
            idle_for=idle_for,
        )




def build_plan_draft_from_decision(decision: PlanningDecision) -> PlanDraft | None:
    """Convert a planning decision into a thin plan draft."""

    selected_goal_id = decision.selected_move.goal_id
    if selected_goal_id is None:
        return None

    return PlanDraft(
        plan_id=f"plan:{decision.decision_id}",
        goal_id=selected_goal_id,
        session_id=decision.session_id,
        steps=(
            PlanStep(
                step_id=f"step:{decision.decision_id}:1",
                title=decision.selected_move.title,
                rationale=decision.rationale.summary,
                dependency_refs=decision.selected_move.dependency_refs,
            ),
        ),
        rationale=decision.rationale.summary,
    )


def apply_decision_to_goal_graph(
    graph: GoalGraph,
    decision: PlanningDecision,
    *,
    updated_at: datetime | None = None,
) -> GoalGraph:
    """Persist the planning choice back into the legacy goal-graph adapter."""

    selected_goal_id = decision.selected_move.goal_id
    if selected_goal_id is None:
        return graph

    goal = graph.goal(selected_goal_id)
    if goal is None:
        return graph

    next_status, next_active_goal_id = _planned_progression(graph, goal, decision.selected_move.kind)
    if next_status is None:
        return graph

    timestamp = decision.selected_at if updated_at is None else updated_at
    return graph.transition_goal(
        selected_goal_id,
        status=next_status,
        revision_id=decision.decision_id,
        updated_at=timestamp,
        active_goal_id=next_active_goal_id,
    )


def apply_decision_to_activity_graph(
    graph: GoalGraph | ActivityGraph,
    decision: PlanningDecision,
    *,
    updated_at: datetime | None = None,
) -> ActivityGraph:
    """Persist the planning choice back into the canonical activity graph."""

    goal_graph = activity_graph_to_goal_graph(graph)
    next_graph = apply_decision_to_goal_graph(goal_graph, decision, updated_at=updated_at)
    return goal_graph_to_activity_graph(next_graph)


__all__ = [name for name in globals() if not name.startswith("__")]
