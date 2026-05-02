"""Context runtime retrieval, replay, and scoring helpers."""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Any, Mapping, Protocol, runtime_checkable

from packages.capabilities.runtime import CapabilityDescriptor, ContextCapability
from packages.contracts.runtime import ContextBundle, GoalNode, IntentDecision, MemoryRecord, SessionState, StructuredTurnSlot
from packages.evidence import parse_structured_turn_memory



from .runtime_types import (
    ContextBudgetPlan,
    ContextLayerBudget,
    ContextLayerSnapshot,
    ContextRetrievalRequest,
    ContextSourceTrace,
    MemoryRecord,
    ReplayPacket,
    SessionFrame,
    SessionSnapshot,
    StructuredTurnSlot,
    TurnPacket,
)

def _budget_for(budgets: ContextBudgetPlan, layer_name: str) -> int:
    allocation = budgets.allocation_for(layer_name)
    return allocation.allocated_tokens if allocation else 0

def _goal_line(goal: GoalNode) -> str:
    dependencies = f" deps={','.join(goal.dependencies)}" if goal.dependencies else ""
    evidence = f" evidence={','.join(goal.evidence_refs)}" if goal.evidence_refs else ""
    return f"{goal.goal_id}: {goal.title} [{goal.status}/{goal.priority}]{dependencies}{evidence}"

def _memory_line(memory: MemoryRecord) -> str:
    refs = f" goals={','.join(memory.goal_refs)}" if memory.goal_refs else ""
    tags = f" tags={','.join(memory.tags)}" if memory.tags else ""
    return f"{memory.memory_id}: {memory.kind} {memory.content}{refs}{tags}"

def _intent_focus_activity_ids(
    goals: tuple[GoalNode, ...],
    *,
    intent: IntentDecision | None,
) -> tuple[str, ...]:
    if intent is None or not intent.focus_activity_ids:
        return ()
    goal_ids = {goal.goal_id for goal in goals}
    return tuple(goal_id for goal_id in intent.focus_activity_ids if goal_id in goal_ids)

def _snapshot_goals(
    goals: tuple[GoalNode, ...],
    *,
    intent: IntentDecision | None,
) -> tuple[GoalNode, ...]:
    if intent is None:
        return goals
    focus_ids = _intent_focus_activity_ids(goals, intent=intent)
    goal_index = {goal.goal_id: goal for goal in goals}
    focused = tuple(goal_index[goal_id] for goal_id in focus_ids)
    if intent.scope_suggestion == "profile" and not focused:
        return ()
    if focused:
        if intent.budget_class == "broad":
            focused_ids = set(focus_ids)
            tail = tuple(goal for goal in goals if goal.goal_id not in focused_ids)
            return focused + tail
        return focused
    return goals

def _intent_budget_multiplier(intent: IntentDecision | None) -> float:
    if intent is None:
        return 1.0
    if intent.budget_class == "narrow":
        return 0.75
    if intent.budget_class == "broad":
        return 1.35
    return 1.0

def _select_warm_memories(
    memories: tuple[MemoryRecord, ...],
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    intent: IntentDecision | None = None,
    limit: int = 3,
) -> tuple[MemoryRecord, ...]:
    if not memories:
        return ()
    scored = sorted(
        memories,
        key=lambda memory: (
            -_context_memory_score(memory, session=session, goals=goals, intent=intent, layer_name="warm"),
            -(memory.created_at.timestamp() if memory.created_at is not None else 0.0),
            memory.memory_id,
        ),
    )
    selected = scored[:limit]
    return tuple(
        sorted(
            selected,
            key=lambda memory: (
                memory.created_at.timestamp() if memory.created_at is not None else 0.0,
                memory.memory_id,
            ),
        )
    )

def _warm_memory_refs(
    memories: tuple[MemoryRecord, ...],
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    intent: IntentDecision | None = None,
) -> tuple[str, ...]:
    return tuple(
        memory.memory_id for memory in _select_warm_memories(memories, session=session, goals=goals, intent=intent)
    )

def _goal_trace_reason(goals: tuple[GoalNode, ...]) -> str:
    if not goals:
        return "no durable goals were available"
    selected = ", ".join(f"{goal.goal_id}({goal.status}/{goal.priority})" for goal in goals[:3])
    tail = " ..." if len(goals) > 3 else ""
    return f"durable goals stayed visible: {selected}{tail}"

def _derived_source_refs(prefix: str, items: tuple[str, ...]) -> tuple[str, ...]:
    refs: list[str] = []
    for index, item in enumerate(items, start=1):
        head = item.split(":", 1)[0].strip().lower().replace(" ", "-")
        if head and all(ch.isalnum() or ch in {"-", "_", "."} for ch in head):
            refs.append(head)
        else:
            refs.append(f"{prefix}:{index}")
    return tuple(refs)

def _turn_packet_trace_reason(session: SessionState, hot_turns: tuple[str, ...]) -> str:
    if hot_turns:
        return f"{len(hot_turns)} live turn packet item(s) keep the current exchange request-time only"
    if session.interruption_state:
        return f"no hot turn packet was supplied, so the frame leans on {session.interruption_state}"
    return "no hot turn packet was supplied, so the frame leans on durable snapshot state"

def _session_snapshot_trace_reason(
    session: SessionState,
    goals: tuple[GoalNode, ...],
    memories: tuple[MemoryRecord, ...],
    *,
    intent: IntentDecision | None,
    profile_snapshot_refs: tuple[str, ...],
    warm_memories: tuple[MemoryRecord, ...],
    retrieval_requests: tuple[ContextRetrievalRequest, ...],
    summary_requests: tuple[ContextSummaryRequest, ...],
) -> str:
    snapshot_goals = _snapshot_goals(goals, intent=intent)
    warm_refs = tuple(memory.memory_id for memory in warm_memories)
    goal_ids = tuple(goal.goal_id for goal in snapshot_goals)
    retrieved_memory_ids = tuple(
        dict.fromkeys(memory_id for request in retrieval_requests for memory_id in request.memory_ids)
    )
    pieces = [
        f"profile slice kept {len(profile_snapshot_refs) or 1} durable ref(s)",
        f"work slice kept {len(goal_ids)} goal ref(s)",
        f"evidence slice kept {len(retrieved_memory_ids)} retrieved memory ref(s)",
    ]
    if session.interruption_state:
        pieces.append(f"continuity recovery stayed explicit via {session.interruption_state}")
    if warm_refs:
        pieces.append(f"warm continuity refs: {', '.join(warm_refs)}")
    if summary_requests:
        pieces.append("the session snapshot was compacted instead of expanding into a blind recency slice")
    if intent is not None:
        pieces.append(f"intent scope={intent.scope_suggestion} budget={intent.budget_class}")
        focus_ids = _intent_focus_activity_ids(goals, intent=intent)
        if focus_ids:
            pieces.append(f"intent focus kept {', '.join(focus_ids[:2])} ahead of broad recall")
        if intent.scope_suggestion == "profile" and not goal_ids:
            pieces.append("profile scope suppressed unrelated work refs")
    if not memories:
        pieces.append("no durable memory records were available")
    return "; ".join(pieces)

def _procedure_overlay_trace_reason(procedure_overlays: tuple[str, ...]) -> str:
    if procedure_overlays:
        return f"{len(procedure_overlays)} bounded procedure overlay(s) were attached without changing durable truth"
    return "no procedure overlay was needed"

def _workspace_attachment_trace_reason(artifacts: tuple[str, ...]) -> str:
    if artifacts:
        return f"{len(artifacts)} workspace/runtime attachment(s) stayed visible for request-time steering"
    return "no workspace attachments were needed"

def _session_snapshot_lines(
    *,
    session: SessionState,
    profile_snapshot_refs: tuple[str, ...],
    goals: tuple[GoalNode, ...],
    warm_memories: tuple[MemoryRecord, ...],
    retrieval_requests: tuple[ContextRetrievalRequest, ...],
    memory_index: Mapping[str, MemoryRecord],
    workspace_attachments: tuple[str, ...] = (),
    intent: IntentDecision | None = None,
) -> tuple[str, ...]:
    snapshot_goals = _snapshot_goals(goals, intent=intent)
    lines: list[str] = []
    if intent is not None:
        lines.append(f"intent-shape: family={intent.intent}; scope={intent.scope_suggestion}; budget={intent.budget_class}")
        focus_ids = _intent_focus_activity_ids(goals, intent=intent)
        if focus_ids:
            lines.append("focus-slice: " + ", ".join(focus_ids))
    lines.append("profile-slice:")
    lines.extend(
        _profile_snapshot_summary_lines(
            profile_snapshot_refs,
            fallback=(f"profile:{session.profile_id}:user-snapshot",),
        )
    )
    if snapshot_goals:
        lines.append("work-slice:")
        lines.extend(_goal_line(goal) for goal in snapshot_goals)
    elif intent is not None and intent.scope_suggestion == "profile":
        lines.append("work-slice: intent scope suppressed active goals")
    else:
        lines.append("work-slice: no active goals")
    if warm_memories:
        lines.append("continuity-slice:")
        lines.extend(_memory_line(memory) for memory in warm_memories)
    retrieval_lines = _retrieval_lines(retrieval_requests, memory_index)
    if retrieval_lines:
        lines.append("evidence-slice:")
        lines.extend(retrieval_lines)
    elif not warm_memories:
        lines.append("evidence-slice: no retrieved evidence")
    if workspace_attachments:
        lines.append("workspace-slice:")
        lines.extend(workspace_attachments[:3])
    return tuple(lines)

def _build_retrieval_query(
    memory: MemoryRecord,
    goals: tuple[GoalNode, ...],
    *,
    intent: IntentDecision | None = None,
) -> str:
    goal_titles = " ".join(goal.title for goal in goals if goal.goal_id in memory.goal_refs)
    focus_titles = ""
    intent_terms = ""
    if intent is not None:
        focus_ids = _intent_focus_activity_ids(goals, intent=intent)
        focus_titles = " ".join(goal.title for goal in goals if goal.goal_id in focus_ids)
        intent_terms = " ".join((intent.intent, intent.scope_suggestion, intent.budget_class))
    query = " ".join(part for part in (intent_terms, focus_titles, memory.kind, memory.content, goal_titles) if part)
    return query[:240]

def _build_retrieval_reason(
    memory: MemoryRecord,
    goals: tuple[GoalNode, ...],
    reasons: tuple[str, ...] = (),
    *,
    intent: IntentDecision | None = None,
) -> str:
    matched_goals = [goal.goal_id for goal in goals if goal.goal_id in memory.goal_refs]
    pieces: list[str] = []
    if intent is not None:
        focus_ids = set(_intent_focus_activity_ids(goals, intent=intent))
        matched_focus = [goal_id for goal_id in matched_goals if goal_id in focus_ids]
        if matched_focus:
            pieces.append(f"intent focus kept {', '.join(matched_focus)} ahead of generic recall")
    if matched_goals:
        pieces.append(f"goal-linked memory for {', '.join(matched_goals)}")
    pieces.extend(reason for reason in reasons if reason not in pieces)
    if intent is not None:
        pieces.append(f"intent scope={intent.scope_suggestion} budget={intent.budget_class}")
    if not pieces:
        if memory.kind in {"summary", "decision", "lesson"}:
            pieces.append("high-value historical memory")
        else:
            pieces.append("supporting continuity memory")
    return "; ".join(pieces[:4])

def _estimate_tokens(content: str) -> int:
    return max(8, (len(content) // 4) + 1)

def _truncate_lines(content: tuple[str, ...], token_budget: int) -> tuple[str, ...]:
    remaining = max(token_budget, 0)
    lines: list[str] = []
    for line in content:
        if remaining <= 0:
            break
        lines.append(_truncate_text(line, limit=120))
        remaining -= _estimate_tokens(line)
    return tuple(lines) if lines else ("no content",)


def _truncate_text(value: str, *, limit: int) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    if limit <= 3:
        return text[:limit]
    cut = text[:limit]
    boundary = max(
        cut.rfind(" "),
        cut.rfind(","),
        cut.rfind(";"),
        cut.rfind("|"),
    )
    if boundary < max(32, limit // 2):
        boundary = limit
    return f"{text[:boundary].rstrip(' ,;|')}..."

def _summary_content_for_layer(
    layer_name: str,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    memories: tuple[MemoryRecord, ...],
    hot_turns: tuple[str, ...],
    *,
    profile_snapshot_refs: tuple[str, ...] = (),
    warm_memories: tuple[MemoryRecord, ...],
    retrieval_requests: tuple[ContextRetrievalRequest, ...],
    replay_requests: tuple[ContextRetrievalRequest, ...] = (),
    procedure_overlays: tuple[str, ...] = (),
    workspace_attachments: tuple[str, ...] = (),
    intent: IntentDecision | None = None,
) -> tuple[str, ...]:
    if layer_name == "session_snapshot":
        snapshot_goals = _snapshot_goals(goals, intent=intent)
        goal_ids = {goal.goal_id for goal in snapshot_goals}
        warm_refs = tuple(memory.memory_id for memory in warm_memories)
        omitted_refs = tuple(
            memory.memory_id
            for memory in memories
            if memory.memory_id not in warm_refs
            and memory.memory_id not in tuple(
                dict.fromkeys(memory_id for request in retrieval_requests for memory_id in request.memory_ids)
            )
            and memory.memory_id not in tuple(
                dict.fromkeys(memory_id for request in replay_requests for memory_id in request.memory_ids)
            )
        )
        goal_linked = tuple(
            memory.memory_id for memory in warm_memories if goal_ids.intersection(memory.goal_refs)
        )
        corrected = tuple(memory.memory_id for memory in warm_memories if "corrected" in memory.tags)
        lines: list[str] = []
        if intent is not None:
            lines.append(f"intent shape: family={intent.intent}; scope={intent.scope_suggestion}; budget={intent.budget_class}")
            focus_ids = _intent_focus_activity_ids(goals, intent=intent)
            if focus_ids:
                lines.append(f"focused work refs: {', '.join(focus_ids)}")
        lines.extend(
            _profile_snapshot_summary_lines(
                profile_snapshot_refs,
                fallback=(f"profile:{session.profile_id}:user-snapshot",),
            )
        )
        if intent is not None and intent.scope_suggestion == "profile" and not snapshot_goals:
            lines.append("work slice suppressed by profile scope")
        if goal_linked:
            lines.append(f"retained goal-linked refs: {', '.join(goal_linked)}")
        if corrected:
            lines.append(f"retained corrected refs: {', '.join(corrected)}")
        evidence_refs = tuple(dict.fromkeys(memory_id for request in retrieval_requests for memory_id in request.memory_ids))
        if evidence_refs:
            lines.append(f"selected evidence refs: {', '.join(evidence_refs)}")
        if omitted_refs:
            lines.append(f"compacted away: {', '.join(omitted_refs)}")
        if session.interruption_state:
            lines.append(f"interruption: {session.interruption_state}")
        if snapshot_goals:
            lines.append(
                "selected work refs: "
                + ", ".join(f"{goal.goal_id}({goal.status}/{goal.priority})" for goal in snapshot_goals)
            )
        if warm_memories:
            lines.append(
                "selected warm refs: "
                + ", ".join(
                    f"{memory.memory_id}({memory.kind}; goals={','.join(memory.goal_refs) or 'none'}; tags={','.join(memory.tags) or 'none'})"
                    for memory in warm_memories
                )
            )
        retrieval_refs = tuple(
            f"{memory_id}({request.reason})"
            for request in retrieval_requests
            for memory_id in request.memory_ids
        )
        if retrieval_refs:
            lines.append("selected retrieval refs: " + "; ".join(retrieval_refs))
        if workspace_attachments:
            lines.append("workspace refs: " + " | ".join(workspace_attachments[:3]))
        return tuple(lines)
    if layer_name == "replay_packet":
        lines = [
            "selected replay refs: " + ", ".join(
                dict.fromkeys(memory_id for request in replay_requests for memory_id in request.memory_ids)
            )
        ]
        lines.extend(_replay_summary_lines(replay_requests, memories))
        return tuple(lines)
    if layer_name == "procedure_overlay":
        return procedure_overlays or ("no active procedure overlay",)
    if layer_name == "workspace_attachments":
        return workspace_attachments or ("no workspace attachments",)
    return hot_turns or ("no current turn packet",)


def _profile_snapshot_summary_lines(
    profile_snapshot_refs: tuple[str, ...],
    *,
    fallback: tuple[str, ...],
) -> tuple[str, ...]:
    fields = ""
    summary = ""
    other_refs: list[str] = []
    refs = profile_snapshot_refs or fallback
    for ref in refs:
        if ref.startswith("user-known-fields="):
            fields = ref.removeprefix("user-known-fields=").strip()
        elif ref.startswith("user-summary="):
            summary = ref.removeprefix("user-summary=").strip()
        elif ref.startswith("section:user-snapshot"):
            continue
        else:
            other_refs.append(ref)

    lines: list[str] = []
    if fields:
        lines.append(f"selected profile fields: {fields}")
    if summary:
        lines.append(f"selected profile summary: {summary}")
    if not lines and other_refs:
        lines.append("selected profile refs: " + ", ".join(other_refs))
    return tuple(lines)

def _retrieval_lines(
    retrieval_requests: tuple[ContextRetrievalRequest, ...],
    memory_index: Mapping[str, MemoryRecord],
) -> tuple[str, ...]:
    lines: list[str] = []
    for request in retrieval_requests:
        for memory_id in request.memory_ids:
            memory = memory_index.get(memory_id)
            if memory is None:
                continue
            lines.append(f"{_memory_line(memory)} | why: {request.reason}")
    return tuple(lines)

@dataclass(frozen=True, slots=True)
class _ReplayIntent:
    slot_name: str
    replay_mode: str
    max_compression: str
    desired_tokens: int
    minimum_tokens: int
    reason: str


_REPLAY_COMPRESSION_RANK = {
    "episode_summary": 0,
    "structured_summary": 1,
    "raw_turn": 2,
    "raw_trace": 3,
}

def _split_retrieval_requests(
    retrieval_requests: tuple[ContextRetrievalRequest, ...],
) -> tuple[tuple[ContextRetrievalRequest, ...], tuple[ContextRetrievalRequest, ...]]:
    snapshot_requests = tuple(request for request in retrieval_requests if request.layer_name != "replay_packet")
    replay_requests = tuple(request for request in retrieval_requests if request.layer_name == "replay_packet")
    return snapshot_requests, replay_requests

def _infer_replay_intents(
    hot_turns: tuple[str, ...],
    *,
    intent: IntentDecision | None = None,
) -> tuple[_ReplayIntent, ...]:
    if not hot_turns:
        text = ""
        tokens: set[str] = set()
    else:
        text = " ".join(hot_turns).lower()
        tokens = _tokenize(text)
    explicit_replay = any(
        phrase in text
        for phrase in (
            "replay",
            "decision path",
            "reasoning chain",
            "action chain",
            "previous turn",
            "earlier turn",
            "earlier turns",
            "blocker history",
            "correction history",
            "rejected option",
        )
    )
    wants_reasoning = explicit_replay or (
        "why" in tokens and tokens.intersection({"did", "decision", "reasoning", "blocker", "because"})
    )
    wants_action = explicit_replay and tokens.intersection({"action", "step", "steps", "command", "tool", "run", "did"})
    wants_outcome = explicit_replay and tokens.intersection({"outcome", "result", "results"})
    replay_mode = "episode" if explicit_replay and tokens.intersection({"previous", "earlier", "history", "across", "episode"}) else "turn"
    wants_raw_trace = "raw trace" in text or "exact trace" in text or ("raw" in tokens and "trace" in tokens)
    intents: list[_ReplayIntent] = []
    if wants_reasoning:
        intents.append(
            _ReplayIntent(
                slot_name="reasoning",
                replay_mode=replay_mode,
                max_compression="raw_trace" if wants_raw_trace else "structured_summary",
                desired_tokens=144 if wants_raw_trace else 72,
                minimum_tokens=32,
                reason="target the earlier reasoning path without defaulting raw trace into ordinary prompts",
            )
        )
    if wants_action:
        intents.append(
            _ReplayIntent(
                slot_name="action",
                replay_mode=replay_mode,
                max_compression="raw_turn",
                desired_tokens=96,
                minimum_tokens=32,
                reason="recover the concrete action chain for the active work item",
            )
        )
    if wants_outcome:
        intents.append(
            _ReplayIntent(
                slot_name="outcome",
                replay_mode=replay_mode,
                max_compression="episode_summary" if replay_mode == "episode" else "structured_summary",
                desired_tokens=64,
                minimum_tokens=24,
                reason="surface the outcome chain that closes the earlier decision path",
            )
        )
    if intents:
        return tuple(intents)
    if intent is not None and (intent.intent == "resume" or intent.resume_signal != "none"):
        if intent.scope_suggestion in {"session", "lineage"}:
            focus_ids = intent.focus_activity_ids[:2]
            focus_suffix = f" for {', '.join(focus_ids)}" if focus_ids else ""
            return (
                _ReplayIntent(
                    slot_name="reasoning",
                    replay_mode="episode" if intent.scope_suggestion == "lineage" else "turn",
                    max_compression="structured_summary",
                    desired_tokens=64 if intent.budget_class == "narrow" else 96,
                    minimum_tokens=24,
                    reason=f"resume intent requested bounded continuity replay{focus_suffix}",
                ),
            )
    return ()

def _schedule_replay_requests(
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    memories: tuple[MemoryRecord, ...],
    hot_turns: tuple[str, ...],
    token_budget: int,
    intent: IntentDecision | None = None,
) -> tuple[ContextRetrievalRequest, ...]:
    intents = _infer_replay_intents(hot_turns, intent=intent)
    if not intents or token_budget <= 0:
        return ()
    remaining = token_budget
    requests: list[ContextRetrievalRequest] = []
    for index, replay_intent in enumerate(intents):
        candidate = _select_replay_memory(
            session=session,
            goals=goals,
            memories=memories,
            hot_turns=hot_turns,
            slot_name=replay_intent.slot_name,
            replay_mode=replay_intent.replay_mode,
            max_compression=replay_intent.max_compression,
            intent=intent,
        )
        if candidate is None:
            continue
        selected_tokens = min(replay_intent.desired_tokens, remaining)
        if selected_tokens <= 0:
            break
        remaining -= selected_tokens
        memory, detail_reason = candidate
        requests.append(
            ContextRetrievalRequest(
                request_id=f"{session.session_id}:replay:{index}",
                layer_name="replay_packet",
                session_id=session.session_id,
                query=" ".join(hot_turns)[:240],
                memory_ids=(memory.memory_id,),
                goal_ids=tuple(goal.goal_id for goal in goals if goal.goal_id in memory.goal_refs),
                token_budget=selected_tokens,
                priority=max(0, 120 - index * 10),
                reason=f"{replay_intent.reason}; {detail_reason}",
                target_slots=(replay_intent.slot_name,),
                max_compression=replay_intent.max_compression,
                replay_mode=replay_intent.replay_mode,
            )
        )
    return tuple(requests)

def _select_replay_memory(
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    memories: tuple[MemoryRecord, ...],
    hot_turns: tuple[str, ...],
    slot_name: str,
    replay_mode: str,
    max_compression: str,
    intent: IntentDecision | None = None,
) -> tuple[MemoryRecord, str] | None:
    hot_text = " ".join(hot_turns)
    hot_tokens = _tokenize(hot_text)
    best: tuple[float, MemoryRecord, str] | None = None
    for memory in memories:
        turn = parse_structured_turn_memory(memory)
        if turn is None:
            continue
        slot = getattr(turn, slot_name)
        if not slot.summary and not slot.detail:
            continue
        base_score = float(
            _context_memory_score(
                memory,
                session=session,
                goals=goals,
                intent=intent,
                layer_name="replay",
                hot_turns=hot_turns,
            )
        )
        slot_tokens = _tokenize(" ".join((slot.summary, *slot.detail, slot.provenance)))
        overlap = tuple(sorted(slot_tokens & hot_tokens))
        score = base_score + float(len(overlap)) * 2.5
        if goal_overlap := tuple(goal.goal_id for goal in goals if goal.goal_id in memory.goal_refs):
            score += float(len(goal_overlap)) * 1.5
        if replay_mode == "episode":
            if turn.compression_tier == "episode_summary" or len(turn.source_turn_ids) > 1:
                score += 3.0
            else:
                score += 0.5
        elif turn.compression_tier == "raw_turn":
            score += 1.5
        if _replay_rank(slot.compression) <= _replay_rank(max_compression):
            score += 1.25
        if "corrected" in memory.tags:
            score += 1.0
        detail_reason = (
            f"selected {memory.memory_id} for {slot_name} replay"
            f" with overlap={','.join(overlap[:4]) or 'goal-linked continuity'}"
        )
        if best is None or score > best[0]:
            best = (score, memory, detail_reason)
    if best is None:
        return None
    return best[1], best[2]

def _replay_rank(compression: str) -> int:
    return _REPLAY_COMPRESSION_RANK.get(compression.strip().lower(), _REPLAY_COMPRESSION_RANK["structured_summary"])

def _project_replay_slot(slot: StructuredTurnSlot, *, max_compression: str) -> tuple[StructuredTurnSlot, bool]:
    if _replay_rank(slot.compression) <= _replay_rank(max_compression):
        return slot, False
    return (
        StructuredTurnSlot(
            summary=slot.summary,
            detail=(),
            compression=max_compression,
            provenance=slot.provenance,
            source_refs=slot.source_refs,
            linkage_refs=slot.linkage_refs,
        ),
        True,
    )

def _replay_lines(
    replay_requests: tuple[ContextRetrievalRequest, ...],
    memory_index: Mapping[str, MemoryRecord],
) -> tuple[str, ...]:
    lines: list[str] = []
    for request in replay_requests:
        for memory_id in request.memory_ids:
            memory = memory_index.get(memory_id)
            turn = parse_structured_turn_memory(memory)
            if turn is None:
                continue
            for slot_name in request.target_slots or ("reasoning",):
                slot = getattr(turn, slot_name)
                projected, degraded = _project_replay_slot(slot, max_compression=request.max_compression)
                lines.append(
                    f"replay {request.replay_mode}/{slot_name} from {memory_id} "
                    f"[compression={projected.compression}; source={projected.provenance or 'runtime'}]"
                )
                if projected.summary:
                    lines.append(f"{slot_name}-summary: {projected.summary}")
                for detail in projected.detail:
                    lines.append(f"{slot_name}-detail: {detail}")
                if degraded:
                    lines.append(
                        f"{slot_name}-fallback: requested <= {request.max_compression}; original {slot.compression} stayed out of prompt"
                    )
                if turn.artifact_ids:
                    lines.append(f"artifact-refs: {', '.join(turn.artifact_ids)}")
                lines.append(f"why: {request.reason}")
    return tuple(lines)

def _replay_summary_lines(
    replay_requests: tuple[ContextRetrievalRequest, ...],
    memories: tuple[MemoryRecord, ...],
) -> tuple[str, ...]:
    memory_index = {memory.memory_id: memory for memory in memories}
    lines: list[str] = []
    for request in replay_requests:
        slot_summary = ", ".join(request.target_slots) or "reasoning"
        lines.append(
            f"replay request {request.request_id}: slots={slot_summary}; mode={request.replay_mode}; max_compression={request.max_compression}"
        )
        for memory_id in request.memory_ids:
            turn = parse_structured_turn_memory(memory_index.get(memory_id))
            if turn is not None:
                lines.append(
                    f"selected turn {turn.turn_id} ({turn.compression_tier}) with source turns: {', '.join(turn.source_turn_ids or (turn.turn_id,))}"
                )
    return tuple(lines)

def _replay_packet_trace_reason(replay_requests: tuple[ContextRetrievalRequest, ...]) -> str:
    parts = []
    for request in replay_requests:
        slot_summary = ", ".join(request.target_slots) or "reasoning"
        parts.append(
            f"{slot_summary} via {request.replay_mode}/{request.max_compression}"
        )
    return (
        f"targeted replay kept {len(replay_requests)} slice(s) with explicit slot budgets: {'; '.join(parts)}; "
        "stable policy stayed in StablePrefix while replay detail remained request-time only"
    )

def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9_]+", text.lower()) if token}

def _thematic_tokens(
    session: SessionState,
    goals: tuple[GoalNode, ...],
    hot_turns: tuple[str, ...],
) -> set[str]:
    tokens: set[str] = set()
    for goal in goals:
        tokens.update(_tokenize(goal.goal_id))
        tokens.update(_tokenize(goal.title))
        tokens.update(_tokenize(goal.status))
        tokens.update(_tokenize(goal.priority))
        tokens.update(_tokenize(" ".join(goal.dependencies)))
        tokens.update(_tokenize(" ".join(goal.evidence_refs)))
    tokens.update(_tokenize(" ".join(hot_turns)))
    tokens.update(_continuity_marker_tokens(session))
    return tokens

def _continuity_marker_tokens(session: SessionState) -> set[str]:
    if not session.interruption_state:
        return set()
    return _tokenize(session.interruption_state) | {"resume", "recovery", "continuity", "interruption", "gap"}

def _context_memory_score(
    memory: MemoryRecord,
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    intent: IntentDecision | None = None,
    layer_name: str,
    hot_turns: tuple[str, ...] = (),
    return_reasons: bool = False,
) -> float | tuple[float, tuple[str, ...]]:
    goal_ids = {goal.goal_id for goal in goals}
    thematic_tokens = _thematic_tokens(session, goals, hot_turns)
    continuity_markers = _continuity_marker_tokens(session)
    reasons: list[str] = []
    score = 0.0
    if memory.session_id == session.session_id:
        score += 4.0
        reasons.append("current-session memory")
    overlap = goal_ids.intersection(memory.goal_refs)
    score += float(len(overlap)) * 5.0
    if overlap:
        reasons.append(f"goal-linked: {', '.join(sorted(overlap))}")
    focus_overlap = set(_intent_focus_activity_ids(goals, intent=intent)).intersection(memory.goal_refs)
    score += float(len(focus_overlap)) * 6.0
    if focus_overlap:
        reasons.append(f"intent focus: {', '.join(sorted(focus_overlap))}")
    kind_bonus = {
        "summary": 3.0,
        "decision": 3.5,
        "lesson": 3.0,
        "semantic": 2.5,
        "procedural": 2.5,
        "artifact": 1.0,
    }
    score += kind_bonus.get(memory.kind, 0.0)
    if memory.kind in {"summary", "decision", "lesson"}:
        reasons.append(f"high-value kind: {memory.kind}")
    elif memory.kind in {"semantic", "procedural"}:
        reasons.append(f"durable kind: {memory.kind}")
    elif memory.kind == "artifact":
        reasons.append("artifact support")
    tags = set(memory.tags)
    if "corrected" in tags:
        score += 2.0
        reasons.append("corrected memory")
    if "consolidated" in tags:
        score += 1.0
        reasons.append("consolidated memory")
    if "filler" in tags:
        score -= 4.0
    if "continuity" in tags or "recovery" in tags:
        score += 1.0
    if intent is not None:
        if intent.scope_suggestion == "profile" and memory.kind in {"summary", "decision", "semantic"}:
            score += 1.5
            reasons.append("profile-scoped recall")
        if intent.scope_suggestion == "workspace" and memory.kind in {"artifact", "procedural"}:
            score += 1.0
            reasons.append("workspace-scoped recall")
        if intent.resume_signal != "none" and memory.kind in {"summary", "decision", "semantic", "procedural"}:
            score += 1.0
            reasons.append("intent resume recovery")
        if intent.budget_class == "narrow" and intent.focus_activity_ids and not focus_overlap and not overlap:
            score -= 1.5
    text_tokens = _tokenize(memory.content) | _tokenize(" ".join(memory.tags))
    thematic_overlap = tuple(sorted(text_tokens & thematic_tokens))
    if thematic_overlap:
        score += float(len(thematic_overlap)) * 1.75
        reasons.append(f"theme overlap: {', '.join(thematic_overlap[:4])}")
    if continuity_markers and (
        continuity_markers.intersection(text_tokens)
        or overlap
        or memory.kind in {"summary", "decision", "lesson", "semantic", "procedural"}
    ):
        score += 2.0
        reasons.append("continuity recovery support")
    if layer_name == "warm" and session.interruption_state:
        score += 1.5
    if memory.created_at is not None:
        score += memory.created_at.timestamp() / 10_000_000
    score += min(len(memory.tags), 4) * 0.001
    reason_tuple = tuple(dict.fromkeys(reasons))
    if return_reasons:
        return score, reason_tuple
    return score

def _retrieval_priority_bucket(
    memory: MemoryRecord,
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    hot_turns: tuple[str, ...],
    intent: IntentDecision | None = None,
) -> int:
    goal_ids = {goal.goal_id for goal in goals}
    text_tokens = _tokenize(memory.content) | _tokenize(" ".join(memory.tags))
    if set(_intent_focus_activity_ids(goals, intent=intent)).intersection(memory.goal_refs):
        return 4
    if goal_ids.intersection(memory.goal_refs):
        return 3
    if _thematic_tokens(session, goals, hot_turns).intersection(text_tokens):
        return 2
    if memory.session_id == session.session_id and memory.kind in {"summary", "decision", "lesson", "semantic", "procedural"}:
        return 1
    return 0

def _plan_rationale(
    session: SessionState,
    goals: tuple[GoalNode, ...],
    memories: tuple[MemoryRecord, ...],
    budgets: ContextBudgetPlan,
    retrieval_requests: tuple[ContextRetrievalRequest, ...],
    *,
    intent: IntentDecision | None = None,
) -> str:
    _, replay_requests = _split_retrieval_requests(retrieval_requests)
    if replay_requests:
        if intent is not None:
            return (
                f"intent {intent.intent} with scope={intent.scope_suggestion} requested bounded replay, "
                "so the frame pulls targeted reasoning/action evidence without moving stable policy out of StablePrefix"
            )
        return (
            "the current request explicitly asks for earlier decision context, so a bounded replay layer "
            "pulls targeted reasoning/action evidence without moving stable policy out of StablePrefix"
        )
    if intent is not None and intent.scope_suggestion == "profile":
        return (
            "profile-scoped intent suppresses unrelated work refs so the session snapshot stays centered on durable profile continuity"
        )
    if intent is not None and intent.budget_class == "narrow" and intent.focus_activity_ids:
        return (
            f"intent focus {', '.join(intent.focus_activity_ids[:2])} narrows the session snapshot and compacts retrieval around the active continuity slice"
        )
    if session.interruption_state:
        return (
            f"continuity recovery is prioritized because the session resumed from {session.interruption_state}; "
            "warm history is compacted and durable retrieval is reintroduced"
        )
    if len(memories) > 5 and budgets.overflow_tokens > 0:
        return (
            "long-running session overflow pushes the planner to summarize warm history "
            "and schedule goal-linked retrieval"
        )
    if goals:
        return f"active durable goal {goals[0].goal_id} is kept close to the reasoning loop"
    return "stable prompt assembly with explicit budget allocation"
