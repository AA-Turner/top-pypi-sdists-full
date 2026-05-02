from __future__ import annotations

from packages.contracts.runtime import (
    EvidenceRetrievalRequest,
    EvidenceRetrievalResult,
    IntentDecision,
    MemoryRecord,
    RecallReason,
    ResumePacket,
)

_CONTINUITY_TAGS = {"continuity", "handoff", "recovery", "resume", "scope-aware"}


def intent_decision(request: EvidenceRetrievalRequest) -> IntentDecision | None:
    return request.intent_decision


def focus_work_item_ids(request: EvidenceRetrievalRequest) -> tuple[str, ...]:
    intent = intent_decision(request)
    if intent is not None and intent.focus_activity_ids:
        return intent.focus_activity_ids
    return request.work_item_ids


def intent_scope_hints(request: EvidenceRetrievalRequest) -> tuple[str, ...]:
    intent = intent_decision(request)
    if intent is None:
        return ()
    hints: list[str] = []
    if intent.resume_signal == "resume":
        hints.append("lineage")
    if intent.scope_suggestion in {"session", "lineage", "workspace", "profile"}:
        hints.append(intent.scope_suggestion)
    return tuple(dict.fromkeys(hints))


def intent_score_adjustments(
    request: EvidenceRetrievalRequest,
    *,
    record: MemoryRecord,
    goal_overlap: tuple[str, ...],
) -> tuple[float, float, tuple[RecallReason, ...]]:
    intent = intent_decision(request)
    if intent is None:
        return 0.0, 0.0, ()

    graph_score = 0.0
    continuity_score = 0.0
    reasons: list[RecallReason] = []
    if intent.focus_activity_ids:
        if goal_overlap:
            graph_score += float(len(goal_overlap)) * 1.25
            reasons.append(
                RecallReason(
                    "intent.focus",
                    f"intent focus overlap: {','.join(goal_overlap)}",
                    graph_score,
                )
            )
        elif record.goal_refs:
            graph_score -= 0.75
            reasons.append(
                RecallReason(
                    "intent.focus-miss",
                    "record stayed outside the resolved intent focus",
                    -0.75,
                )
            )
    if intent.intent == "resume":
        if record.kind in {"procedural", "summary", "decision", "structured_turn"}:
            continuity_score += 1.1
            reasons.append(
                RecallReason(
                    "intent.resume",
                    f"resolved resume intent prefers durable {record.kind} evidence",
                    1.1,
                )
            )
        if _CONTINUITY_TAGS & set(record.tags):
            continuity_score += 0.5
            reasons.append(
                RecallReason(
                    "intent.resume-tags",
                    "resume intent boosted continuity-tagged evidence",
                    0.5,
                )
            )
    return graph_score, continuity_score, tuple(reasons)


def build_resume_packet(
    request: EvidenceRetrievalRequest,
    retrieval: EvidenceRetrievalResult,
    *,
    next_move: str = "",
    artifact_ids: tuple[str, ...] = (),
    constraint_ids: tuple[str, ...] = (),
) -> ResumePacket:
    intent = intent_decision(request)
    top = retrieval.candidates[0] if retrieval.candidates else None
    evidence_ids = tuple(candidate.evidence_id for candidate in retrieval.candidates)
    if not evidence_ids and artifact_ids:
        evidence_ids = artifact_ids

    focus_ids = focus_work_item_ids(request)
    reasons: list[str] = [retrieval.scope_reason]
    if intent is not None and intent.focus_activity_ids:
        reasons.append(f"intent focus {', '.join(intent.focus_activity_ids[:2])} shaped recall")
    if intent is not None and intent.resume_signal != "none":
        reasons.append(f"intent resume signal={intent.resume_signal}")
    if intent is not None:
        reasons.append(f"intent scope={intent.scope_suggestion}")
    opener = "Resume" if intent is None or intent.intent == "resume" or intent.resume_signal != "none" else "Continue"
    if top is not None:
        reasons.extend(reason.detail for reason in top.reasons[:3])
        if top.replay_summary:
            reasons.append(top.replay_summary)
        focused_goal_ids = tuple(goal_id for goal_id in focus_ids if goal_id in top.memory.goal_refs)
        if focused_goal_ids:
            focus_ids = focused_goal_ids
        replay_clause = f" Replay: {top.replay_summary}." if top.replay_summary else ""
        lead_phrase = "inherit the resolved focus and lead with" if intent is not None and intent.focus_activity_ids else "lead with"
        summary = (
            f"{opener} {request.session_id} around {', '.join(focus_ids[:2]) or 'the active thread'}; "
            f"{lead_phrase} {top.evidence_id} because {', '.join(reason.detail for reason in top.reasons[:2])}.{replay_clause}"
        )
    elif evidence_ids:
        reasons.append("goal graph evidence fallback kept the wake packet inspectable")
        summary = (
            f"{opener} {request.session_id} around {', '.join(focus_ids[:2]) or 'the active thread'}; "
            f"lead with {evidence_ids[0]} because no durable memory survived rerank and the active activity graph still carries explicit evidence refs."
        )
    else:
        summary = (
            f"{opener} {request.session_id} with explicit scope reasoning only; "
            "no durable evidence survived rerank yet."
        )
    return ResumePacket(
        session_id=request.session_id,
        profile_id=request.profile_id,
        workspace_id=request.workspace_id,
        focus_work_item_ids=focus_ids,
        evidence_ids=evidence_ids,
        artifact_ids=artifact_ids,
        constraint_ids=constraint_ids,
        summary=summary,
        next_move=next_move,
        reasons=tuple(reason for reason in reasons if reason),
    )
