"""Context runtime planning protocols and deterministic implementations."""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Any, Mapping, Protocol, runtime_checkable

from packages.capabilities.runtime import CapabilityDescriptor, ContextCapability
from packages.contracts.runtime import (
    ContextBundle,
    GoalNode,
    IntentDecision,
    MemoryRecord,
    PromptEnvelope,
    SessionState,
    StructuredTurnSlot,
)
from packages.evidence import parse_structured_turn_memory



from .runtime_types import (
    ContextAssemblyPlan,
    ContextAssemblyResult,
    ContextBudgetPlan,
    ContextBudgetRequest,
    ContextLayerBudget,
    ContextLayerSnapshot,
    ContextRetrievalRequest,
    ContextSourceTrace,
    ContextSummaryRequest,
    ProcedureOverlay,
    ReplayPacket,
    SessionFrame,
    SessionSnapshot,
    StablePrefix,
    TurnPacket,
    WorkspaceAttachments,
)
from .runtime_support import (
    _budget_for,
    _build_retrieval_query,
    _build_retrieval_reason,
    _context_memory_score,
    _derived_source_refs,
    _estimate_tokens,
    _replay_lines,
    _retrieval_priority_bucket,
    _schedule_replay_requests,
    _select_warm_memories,
    _snapshot_goals,
    _session_snapshot_lines,
    _split_retrieval_requests,
    _summary_content_for_layer,
    _truncate_lines,
)

def _operational_layer_heading(layer_name: str) -> str:
    labels = {
        "stable_prefix": "StablePrefix",
        "session_snapshot": "SessionSnapshot",
        "replay_packet": "ReplayPacket",
        "turn_packet": "TurnPacket",
        "procedure_overlay": "ProcedureOverlay",
        "workspace_attachments": "WorkspaceAttachments",
    }
    return labels.get(layer_name, layer_name)


_PROMPT_SECTION_PLACEHOLDERS = frozenset(
    {
        "no stable prefix",
        "no current turn packet",
        "no active procedure overlay",
        "no workspace attachments",
    }
)


def _render_live_prompt_section(
    heading: str,
    *,
    content: tuple[str, ...],
    summary: str | None = None,
    token_budget: int | None = None,
    summary_replaces_content: bool = False,
    raw_content: bool = False,
) -> str:
    normalized_summary = str(summary or "").strip()
    if normalized_summary and summary_replaces_content:
        lines: list[str] = []
    else:
        lines = [str(line).strip() for line in content if str(line).strip()]
        if token_budget is not None:
            lines = list(_truncate_lines(tuple(lines), token_budget))
    if not lines and not normalized_summary:
        return ""
    if len(lines) == 1 and lines[0] in _PROMPT_SECTION_PLACEHOLDERS and not normalized_summary:
        return ""
    rendered = [f"## {heading}"]
    if normalized_summary:
        rendered.append(normalized_summary)
    visible_lines = [line for line in lines if line not in _PROMPT_SECTION_PLACEHOLDERS]
    if raw_content:
        rendered.extend(visible_lines)
    else:
        rendered.extend(f"- {line}" for line in visible_lines)
    return "\n".join(rendered).strip()


def build_prompt_envelope(frame: SessionFrame | None) -> PromptEnvelope:
    """Build live provider prompt sections from a session frame."""

    if frame is None:
        return PromptEnvelope()
    frozen_prefix = _render_live_prompt_section(
        "StablePrefix",
        content=frame.stable_prefix.content,
        raw_content=True,
    )
    session_parts = [
        _render_live_prompt_section(
            "SessionSnapshot",
            content=frame.session_snapshot.content,
            summary=frame.session_snapshot.summary,
            token_budget=frame.session_snapshot.token_budget,
            summary_replaces_content=True,
        )
    ]
    if frame.replay_packet is not None:
        session_parts.append(
            _render_live_prompt_section(
                "ReplayPacket",
                content=frame.replay_packet.content,
                summary=frame.replay_packet.summary,
                token_budget=frame.replay_packet.token_budget,
                summary_replaces_content=True,
            )
        )
    turn_parts = [
        _render_live_prompt_section(
            "ProcedureOverlay",
            content=frame.procedure_overlay.content,
            token_budget=frame.procedure_overlay.token_budget,
        ),
        _render_live_prompt_section(
            "WorkspaceAttachments",
            content=frame.workspace_attachments.content,
            token_budget=frame.workspace_attachments.token_budget,
        ),
    ]
    return PromptEnvelope(
        frozen_prefix=frozen_prefix,
        session_snapshot="\n\n".join(part for part in session_parts if part.strip()),
        turn_injections="\n\n".join(part for part in turn_parts if part.strip()),
    )

@runtime_checkable
class SummaryHook(Protocol):
    def summarize(
        self,
        *,
        session: SessionState,
        layer_name: str,
        content: tuple[str, ...],
        token_budget: int,
        reason: str,
    ) -> str:
        """Summarize content for a single context layer."""

@runtime_checkable
class RetrievalScheduler(Protocol):
    def schedule(
        self,
        *,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        hot_turns: tuple[str, ...] = (),
        token_budget: int,
        budget_plan: ContextBudgetPlan,
        intent: IntentDecision | None = None,
    ) -> tuple[ContextRetrievalRequest, ...]:
        """Schedule retrieval requests for the current session."""

@runtime_checkable
class BudgetManager(Protocol):
    def allocate(self, total_tokens: int, requests: tuple[ContextBudgetRequest, ...]) -> ContextBudgetPlan:
        """Allocate explicit token budgets to ordered layers."""

@runtime_checkable
class PromptRenderer(Protocol):
    def render(self, plan: ContextAssemblyPlan) -> str:
        """Render a structured prompt bundle."""

@runtime_checkable
class ContextPlanner(Protocol):
    def plan(
        self,
        *,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        total_tokens: int,
        instruction_refs: tuple[str, ...],
        hot_turns: tuple[str, ...],
        intent: IntentDecision | None = None,
        profile_snapshot_refs: tuple[str, ...] = (),
        procedure_overlays: tuple[str, ...] = (),
        artifacts: tuple[str, ...] = (),
    ) -> ContextAssemblyPlan:
        """Plan layered context from structured runtime state."""

class DeterministicBudgetManager:
    """Allocate context budgets in explicit priority order."""

    def allocate(self, total_tokens: int, requests: tuple[ContextBudgetRequest, ...]) -> ContextBudgetPlan:
        ordered = sorted(
            enumerate(requests),
            key=lambda item: (
                1 if item[1].required else 0,
                item[1].priority,
                -item[0],
            ),
            reverse=True,
        )
        remaining = max(total_tokens, 0)
        allocations: list[ContextLayerBudget] = []
        omitted: list[str] = []
        for _, request in ordered:
            requested = max(request.desired_tokens, request.minimum_tokens)
            if remaining <= 0:
                allocations.append(
                    ContextLayerBudget(
                        layer_name=request.layer_name,
                        requested_tokens=requested,
                        allocated_tokens=0,
                        required=request.required,
                        priority=request.priority,
                        omitted=True,
                        source_refs=request.source_refs,
                    )
                )
                omitted.append(request.layer_name)
                continue
            allocated = min(requested, remaining)
            if request.required and allocated < request.minimum_tokens:
                omitted.append(request.layer_name)
            elif not request.required and allocated < requested:
                omitted.append(request.layer_name)
            allocations.append(
                ContextLayerBudget(
                    layer_name=request.layer_name,
                    requested_tokens=requested,
                    allocated_tokens=allocated,
                    required=request.required,
                    priority=request.priority,
                    omitted=allocated == 0,
                    source_refs=request.source_refs,
                )
            )
            remaining -= allocated
        overflow = max(sum(request.desired_tokens for request in requests) - total_tokens, 0)
        return ContextBudgetPlan(
            total_tokens=total_tokens,
            allocations=tuple(allocations),
            overflow_tokens=overflow,
            omitted_layers=tuple(dict.fromkeys(omitted)),
        )

class DeterministicRetrievalScheduler:
    """Score memories deterministically against session goals."""

    def schedule(
        self,
        *,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        hot_turns: tuple[str, ...] = (),
        token_budget: int,
        budget_plan: ContextBudgetPlan,
        intent: IntentDecision | None = None,
    ) -> tuple[ContextRetrievalRequest, ...]:
        scored: list[tuple[int, float, float, MemoryRecord, tuple[str, ...]]] = []
        for memory in memories:
            score, reasons = _context_memory_score(
                memory,
                session=session,
                goals=goals,
                intent=intent,
                layer_name="retrieval",
                hot_turns=hot_turns,
                return_reasons=True,
            )
            bucket = _retrieval_priority_bucket(
                memory,
                session=session,
                goals=goals,
                hot_turns=hot_turns,
                intent=intent,
            )
            recency = memory.created_at.timestamp() if memory.created_at is not None else 0.0
            scored.append((bucket, score, recency, memory, reasons))

        scored.sort(key=lambda item: (-item[0], -item[1], -item[2], item[3].memory_id))
        remaining = max(token_budget, 0)
        requests: list[ContextRetrievalRequest] = []
        for index, (_, _, _, memory, reasons) in enumerate(scored):
            estimated_tokens = _estimate_tokens(memory.content)
            if remaining <= 0:
                break
            selected_tokens = min(estimated_tokens, remaining)
            if selected_tokens <= 0:
                continue
            remaining -= selected_tokens
            requests.append(
                ContextRetrievalRequest(
                    request_id=f"{session.session_id}:retrieval:{index}",
                    layer_name="session_snapshot",
                    session_id=session.session_id,
                    query=_build_retrieval_query(memory, goals, intent=intent),
                    memory_ids=(memory.memory_id,),
                    goal_ids=memory.goal_refs,
                    token_budget=selected_tokens,
                    priority=max(0, 100 - index * 10),
                    reason=_build_retrieval_reason(memory, goals, reasons, intent=intent),
                )
            )

        replay_budget = _budget_for(budget_plan, "replay_packet")
        if replay_budget <= 0:
            return tuple(requests)
        return tuple(
            requests
        ) + _schedule_replay_requests(
            session=session,
            goals=goals,
            memories=memories,
            hot_turns=hot_turns,
            token_budget=replay_budget,
            intent=intent,
        )

class DeterministicSummaryHook:
    """Summarize a layer by compressing content into inspectable bullets."""

    def summarize(
        self,
        *,
        session: SessionState,
        layer_name: str,
        content: tuple[str, ...],
        token_budget: int,
        reason: str,
    ) -> str:
        header = f"{_operational_layer_heading(layer_name)} summary for {session.session_id}"
        body = _truncate_lines(content, token_budget)
        pieces = [header, f"reason: {reason}"]
        pieces.extend(f"- {line}" for line in body)
        if session.interruption_state:
            pieces.append(f"- continuity: {session.interruption_state}")
        return "\n".join(pieces)

class MarkdownPromptRenderer:
    """Render the assembled plan as stable markdown-like text."""

    def render(self, plan: ContextAssemblyPlan) -> str:
        lines: list[str] = []
        lines.append(f"# SessionFrame {plan.session_id}")
        lines.append(f"- profile: {plan.profile_id}")
        lines.append(f"- total tokens: {plan.total_tokens}")
        if plan.rationale:
            lines.append(f"- rationale: {plan.rationale}")
        lines.append("")
        for layer in plan.layers:
            lines.append(f"## {_operational_layer_heading(layer.layer_name)}")
            lines.append(f"- token budget: {layer.token_budget}")
            if layer.source_refs:
                lines.append(f"- refs: {', '.join(layer.source_refs)}")
            if layer.summary:
                lines.append(layer.summary)
            for line in layer.content:
                lines.append(f"- {line}")
            lines.append("")
        if plan.summary_requests:
            lines.append("## Summary Requests")
            for request in plan.summary_requests:
                lines.append(
                    f"- {request.layer_name}: {request.reason} ({request.token_budget} tokens)"
                )
            lines.append("")
        if plan.retrieval_requests:
            lines.append("## Retrieval Requests")
            for request in plan.retrieval_requests:
                lines.append(
                    f"- {request.request_id}: {', '.join(request.memory_ids) or 'none'} | {request.reason}"
                )
            lines.append("")
        if plan.source_trace:
            lines.append("## Source Trace")
            for trace in plan.source_trace:
                lines.append(trace.describe())
            lines.append("")
        return "\n".join(lines).rstrip()

class SessionFrameBuilder:
    """Build the explicit CSR-3 session frame from selected runtime slices."""

    def build(
        self,
        *,
        session: SessionState,
        instruction_refs: tuple[str, ...],
        profile_snapshot_refs: tuple[str, ...],
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        hot_turns: tuple[str, ...],
        procedure_overlays: tuple[str, ...],
        workspace_attachments: tuple[str, ...],
        budgets: ContextBudgetPlan,
        summary_requests: tuple[ContextSummaryRequest, ...],
        retrieval_requests: tuple[ContextRetrievalRequest, ...],
        rationale: str,
        source_trace: tuple[ContextSourceTrace, ...],
        intent: IntentDecision | None = None,
    ) -> SessionFrame:
        snapshot_goals = _snapshot_goals(goals, intent=intent)
        warm_memories = _select_warm_memories(memories, session=session, goals=goals, intent=intent)
        memory_index = {memory.memory_id: memory for memory in memories}
        summary_by_layer = {
            request.layer_name: request
            for request in summary_requests
        }
        snapshot_retrieval_requests, replay_retrieval_requests = _split_retrieval_requests(retrieval_requests)
        snapshot_summary = None
        snapshot_request = summary_by_layer.get("session_snapshot")
        if snapshot_request is not None:
            snapshot_summary = DeterministicSummaryHook().summarize(
                session=session,
                layer_name="session_snapshot",
                content=_summary_content_for_layer(
                    "session_snapshot",
                    session,
                    goals,
                    memories,
                    hot_turns,
                    profile_snapshot_refs=profile_snapshot_refs,
                    warm_memories=warm_memories,
                    retrieval_requests=snapshot_retrieval_requests,
                    replay_requests=replay_retrieval_requests,
                    procedure_overlays=procedure_overlays,
                    workspace_attachments=workspace_attachments,
                    intent=intent,
                ),
                token_budget=snapshot_request.token_budget,
                reason=snapshot_request.reason,
            )
        retrieved_memory_ids = tuple(
            dict.fromkeys(memory_id for request in snapshot_retrieval_requests for memory_id in request.memory_ids)
        )
        replay_summary = None
        replay_request = summary_by_layer.get("replay_packet")
        if replay_request is not None and replay_retrieval_requests:
            replay_summary = DeterministicSummaryHook().summarize(
                session=session,
                layer_name="replay_packet",
                content=_summary_content_for_layer(
                    "replay_packet",
                    session,
                    goals,
                    memories,
                    hot_turns,
                    profile_snapshot_refs=profile_snapshot_refs,
                    warm_memories=warm_memories,
                    retrieval_requests=snapshot_retrieval_requests,
                    replay_requests=replay_retrieval_requests,
                    procedure_overlays=procedure_overlays,
                    workspace_attachments=workspace_attachments,
                    intent=intent,
                ),
                token_budget=replay_request.token_budget,
                reason=replay_request.reason,
            )
        replay_memory_ids = tuple(
            dict.fromkeys(memory_id for request in replay_retrieval_requests for memory_id in request.memory_ids)
        )
        replay_packet = None
        if replay_retrieval_requests:
            replay_packet = ReplayPacket(
                source_refs=replay_memory_ids,
                evidence_refs=replay_memory_ids,
                content=_replay_lines(replay_retrieval_requests, memory_index),
                token_budget=_budget_for(budgets, "replay_packet"),
                summary=replay_summary,
            )
        session_snapshot = SessionSnapshot(
            source_refs=tuple(
                dict.fromkeys(
                    (
                        *profile_snapshot_refs,
                        *(goal.goal_id for goal in snapshot_goals),
                        *(memory.memory_id for memory in warm_memories),
                        *retrieved_memory_ids,
                    )
                )
            ),
            profile_refs=profile_snapshot_refs or (f"profile:{session.profile_id}:user-snapshot",),
            work_refs=tuple(goal.goal_id for goal in snapshot_goals),
            evidence_refs=retrieved_memory_ids,
            content=_session_snapshot_lines(
                session=session,
                profile_snapshot_refs=profile_snapshot_refs,
                goals=goals,
                warm_memories=warm_memories,
                retrieval_requests=snapshot_retrieval_requests,
                memory_index=memory_index,
                workspace_attachments=workspace_attachments,
                intent=intent,
            ),
            token_budget=_budget_for(budgets, "session_snapshot"),
            summary=snapshot_summary,
        )
        return SessionFrame(
            session_id=session.session_id,
            profile_id=session.profile_id,
            stable_prefix=StablePrefix(
                source_refs=instruction_refs,
                content=instruction_refs or ("no stable prefix",),
                token_budget=_budget_for(budgets, "stable_prefix"),
            ),
            session_snapshot=session_snapshot,
            replay_packet=replay_packet,
            turn_packet=TurnPacket(
                source_refs=tuple(f"turn:{index}" for index, _ in enumerate(hot_turns, start=1)),
                content=hot_turns or ("no current turn packet",),
                token_budget=_budget_for(budgets, "turn_packet"),
            ),
            procedure_overlay=ProcedureOverlay(
                source_refs=_derived_source_refs("procedure", procedure_overlays),
                content=procedure_overlays or ("no active procedure overlay",),
                token_budget=_budget_for(budgets, "procedure_overlay"),
            ),
            workspace_attachments=WorkspaceAttachments(
                source_refs=_derived_source_refs("attachment", workspace_attachments),
                content=workspace_attachments or ("no workspace attachments",),
                token_budget=_budget_for(budgets, "workspace_attachments"),
            ),
            rationale=rationale,
            source_trace=source_trace,
        )
