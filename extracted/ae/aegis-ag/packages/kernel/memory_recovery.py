from __future__ import annotations

from packages.contracts.runtime import (
    ActivityGraph,
    IntentDecision,
    RelationshipMemoryRecord,
    SessionContinuityState,
    SessionState,
)

from .runtime_support import KernelTurnRequest


def memory_query(
    request: KernelTurnRequest,
    *,
    goal_graph: ActivityGraph,
    relationship: RelationshipMemoryRecord | None,
    intent: IntentDecision,
) -> str:
    focus_titles = tuple(
        goal.title
        for goal_id in intent.focus_activity_ids
        if (goal := goal_graph.goal(goal_id)) is not None and goal.title.strip()
    )
    query = request.goal_query or request.prompt or request.event.payload.get("message", "")
    if not query.strip():
        if focus_titles:
            prefix = "resume" if intent.resume_signal != "none" else ""
            query = " ".join(part for part in (prefix, *focus_titles[:2]) if part)
        elif goal_graph.goals:
            query = " ".join(goal.title for goal in goal_graph.goals[:3])
    elif focus_titles:
        focus_seed = " ".join(focus_titles[:2])
        if focus_seed and focus_seed.lower() not in query.lower():
            query = " | ".join(part for part in (query, focus_seed) if part)
    continuity_seed = " ".join(relationship.continuity_notes[:2]) if relationship is not None else ""
    intent_seed = ""
    if intent.resume_signal != "none":
        intent_seed = " ".join(part for part in ("resume", intent.resume_signal.replace("_", " "), *focus_titles[:2]) if part)
    elif focus_titles:
        intent_seed = " ".join(focus_titles[:2])
    parts = [part.strip() for part in (query, intent_seed, continuity_seed) if part and part.strip()]
    return " | ".join(parts)


def memory_goal_ids(goal_graph: ActivityGraph, *, intent: IntentDecision) -> tuple[str, ...]:
    goal_ids: list[str] = list(intent.focus_activity_ids)
    if goal_graph.active_goal_id is not None and goal_graph.active_goal_id not in goal_ids:
        goal_ids.append(goal_graph.active_goal_id)
    active_goal = goal_graph.active_goal()
    if active_goal is not None and active_goal.parent_goal_id is not None:
        goal_ids.append(active_goal.parent_goal_id)
    for goal in goal_graph.goals:
        if goal.status in {"active", "blocked", "queued", "proposed"}:
            goal_ids.append(goal.goal_id)
        if len(goal_ids) >= 5:
            break
    return tuple(dict.fromkeys(goal_ids))


def memory_scope_session_ids(
    session: SessionState,
    *,
    continuity: SessionContinuityState,
    intent: IntentDecision,
) -> tuple[str, ...]:
    if intent.scope_suggestion == "session":
        return (session.session_id,)
    if continuity.lineage_session_ids:
        return tuple(dict.fromkeys(continuity.lineage_session_ids))
    return (session.session_id,)


def memory_retrieval_scopes(
    session: SessionState,
    *,
    continuity: SessionContinuityState,
    intent: IntentDecision,
) -> tuple[str, ...]:
    scopes: list[str] = ["session"]
    if intent.resume_signal == "resume" or intent.scope_suggestion == "lineage":
        scopes.append("lineage")
    if intent.scope_suggestion == "workspace" and session.workspace_id is not None:
        scopes.append("workspace")
    if intent.scope_suggestion == "profile":
        scopes.append("profile")
    if continuity.requires_recovery and intent.scope_suggestion != "session" and "lineage" not in scopes:
        scopes.append("lineage")
    return tuple(dict.fromkeys(scopes))


def memory_replay_mode(intent: IntentDecision) -> str:
    if intent.intent == "resume" or intent.resume_signal != "none":
        return "episode"
    return "off"


def memory_scope_reason(
    *,
    session: SessionState,
    goal_graph: ActivityGraph,
    intent: IntentDecision,
    relationship: RelationshipMemoryRecord | None,
    continuity: SessionContinuityState,
    scope_session_ids: tuple[str, ...],
) -> str:
    reasons: list[str] = []
    if continuity.requires_recovery and len(scope_session_ids) > 1:
        reasons.append("resume recovery expands recall across the durable session lineage")
    else:
        reasons.append("recovery stays inside the active session scope")
    if intent.resume_signal != "none":
        reasons.append(f"intent signaled {intent.resume_signal} recovery handling")
    if intent.focus_activity_ids:
        reasons.append(f"intent focus {','.join(intent.focus_activity_ids[:2])} narrows recall")
    if goal_graph.active_goal_id is not None:
        reasons.append(f"active goal {goal_graph.active_goal_id} outranks generic recall")
    if relationship is not None and relationship.continuity_notes:
        reasons.append("relationship continuity stays separate and only contributes continuity cues")
    if session.interruption_state:
        reasons.append(f"interruption state {session.interruption_state} keeps recovery explicit")
    return "; ".join(reasons)
