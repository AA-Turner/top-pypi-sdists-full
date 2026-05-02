"""Layered context runtime implementation assembled from smaller modules."""


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Any, Mapping, Protocol, runtime_checkable

from packages.capabilities.runtime import CapabilityDescriptor, ContextCapability
from packages.contracts.runtime import ContextBundle, GoalNode, IntentDecision, MemoryRecord, SessionState, StructuredTurnSlot
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
from .runtime_layers import (
    BudgetManager,
    ContextPlanner,
    DeterministicBudgetManager,
    DeterministicRetrievalScheduler,
    DeterministicSummaryHook,
    MarkdownPromptRenderer,
    PromptRenderer,
    RetrievalScheduler,
    SessionFrameBuilder,
    SummaryHook,
    build_prompt_envelope,
)
from .runtime_support import (
    _budget_for,
    _goal_line,
    _memory_line,
    _select_warm_memories,
    _warm_memory_refs,
    _goal_trace_reason,
    _derived_source_refs,
    _turn_packet_trace_reason,
    _session_snapshot_trace_reason,
    _procedure_overlay_trace_reason,
    _workspace_attachment_trace_reason,
    _session_snapshot_lines,
    _build_retrieval_query,
    _build_retrieval_reason,
    _estimate_tokens,
    _intent_budget_multiplier,
    _truncate_lines,
    _summary_content_for_layer,
    _retrieval_lines,
    _ReplayIntent,
    _split_retrieval_requests,
    _infer_replay_intents,
    _schedule_replay_requests,
    _select_replay_memory,
    _replay_rank,
    _project_replay_slot,
    _replay_lines,
    _replay_summary_lines,
    _replay_packet_trace_reason,
    _tokenize,
    _thematic_tokens,
    _continuity_marker_tokens,
    _context_memory_score,
    _retrieval_priority_bucket,
    _plan_rationale,
    _snapshot_goals,
)

class LayeredContextPlanner:
    """Plan the layered context structure from runtime state."""

    def __init__(
        self,
        budget_manager: BudgetManager | None = None,
        summary_hook: SummaryHook | None = None,
        retrieval_scheduler: RetrievalScheduler | None = None,
    ) -> None:
        self._budget_manager = budget_manager or DeterministicBudgetManager()
        self._summary_hook = summary_hook or DeterministicSummaryHook()
        self._retrieval_scheduler = retrieval_scheduler or DeterministicRetrievalScheduler()

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
        requests = self._build_budget_requests(
            session,
            goals,
            memories,
            instruction_refs,
            hot_turns,
            intent,
            profile_snapshot_refs,
            procedure_overlays,
            artifacts,
        )
        budgets = self._budget_manager.allocate(total_tokens, requests)
        retrieval_requests = self._retrieval_scheduler.schedule(
            session=session,
            goals=goals,
            memories=memories,
            hot_turns=hot_turns,
            token_budget=max(
                self._snapshot_retrieval_budget(budgets, intent=intent),
                self._suggest_retrieval_budget(memories, intent=intent),
                max(total_tokens - budgets.allocated_tokens, 0),
            ),
            budget_plan=budgets,
            intent=intent,
        )
        summary_requests = self._build_summary_requests(
            session,
            budgets,
            goals,
            memories,
            hot_turns,
            intent,
            profile_snapshot_refs,
            retrieval_requests,
        )
        source_trace = self._build_source_trace(
            session=session,
            goals=goals,
            memories=memories,
            instruction_refs=instruction_refs,
            intent=intent,
            profile_snapshot_refs=profile_snapshot_refs,
            hot_turns=hot_turns,
            procedure_overlays=procedure_overlays,
            artifacts=artifacts,
            summary_requests=summary_requests,
            retrieval_requests=retrieval_requests,
        )
        rationale = _plan_rationale(session, goals, memories, budgets, retrieval_requests, intent=intent)
        frame = SessionFrameBuilder().build(
            session=session,
            instruction_refs=instruction_refs,
            profile_snapshot_refs=profile_snapshot_refs,
            goals=goals,
            memories=memories,
            hot_turns=hot_turns,
            procedure_overlays=procedure_overlays,
            workspace_attachments=artifacts,
            budgets=budgets,
            summary_requests=summary_requests,
            retrieval_requests=retrieval_requests,
            rationale=rationale,
            source_trace=source_trace,
            intent=intent,
        )
        return ContextAssemblyPlan(
            session_id=session.session_id,
            profile_id=session.profile_id,
            total_tokens=total_tokens,
            layers=frame.layers(),
            budgets=budgets,
            summary_requests=summary_requests,
            retrieval_requests=retrieval_requests,
            frame=frame,
            rationale=rationale,
            source_trace=source_trace,
        )

    def _build_budget_requests(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        instruction_refs: tuple[str, ...],
        hot_turns: tuple[str, ...],
        intent: IntentDecision | None,
        profile_snapshot_refs: tuple[str, ...],
        procedure_overlays: tuple[str, ...],
        artifacts: tuple[str, ...],
    ) -> tuple[ContextBudgetRequest, ...]:
        stable_prefix_tokens = max(48, len(instruction_refs) * 8)
        snapshot_goals = _snapshot_goals(goals, intent=intent)
        snapshot_tokens = max(
            96,
            int(
                max(144, len(profile_snapshot_refs) * 6 + len(snapshot_goals) * 28 + min(len(memories), 6) * 24)
                * _intent_budget_multiplier(intent)
            ),
        )
        turn_packet_tokens = max(64, len(hot_turns) * 18)
        overlay_tokens = sum(_estimate_tokens(line) for line in procedure_overlays)
        attachment_tokens = sum(_estimate_tokens(line) for line in artifacts)
        replay_intents = _infer_replay_intents(hot_turns, intent=intent)
        requests: list[ContextBudgetRequest] = [
            ContextBudgetRequest(
                layer_name="stable_prefix",
                desired_tokens=stable_prefix_tokens,
                minimum_tokens=24,
                required=True,
                priority=100,
                source_refs=instruction_refs,
            ),
            ContextBudgetRequest(
                layer_name="session_snapshot",
                desired_tokens=snapshot_tokens,
                minimum_tokens=64,
                required=True,
                priority=90,
                source_refs=tuple(
                    dict.fromkeys(
                        (
                            *profile_snapshot_refs,
                            *(goal.goal_id for goal in snapshot_goals),
                            *(memory.memory_id for memory in memories),
                        )
                    )
                ),
            ),
            ContextBudgetRequest(
                layer_name="turn_packet",
                desired_tokens=turn_packet_tokens,
                minimum_tokens=24,
                required=True,
                priority=80,
                source_refs=tuple(f"turn:{index}" for index, _ in enumerate(hot_turns, start=1)),
            ),
        ]
        if replay_intents:
            requests.append(
                ContextBudgetRequest(
                    layer_name="replay_packet",
                    desired_tokens=sum(intent.desired_tokens for intent in replay_intents),
                    minimum_tokens=min(48, sum(intent.minimum_tokens for intent in replay_intents)),
                    required=False,
                    priority=70,
                    source_refs=tuple(goal.goal_id for goal in snapshot_goals)
                    or tuple(intent.slot_name for intent in replay_intents),
                )
            )
        requests.extend(
            (
                ContextBudgetRequest(
                    layer_name="procedure_overlay",
                    desired_tokens=overlay_tokens,
                    minimum_tokens=0,
                    required=False,
                    priority=40,
                    source_refs=_derived_source_refs("procedure", procedure_overlays),
                ),
                ContextBudgetRequest(
                    layer_name="workspace_attachments",
                    desired_tokens=attachment_tokens,
                    minimum_tokens=0,
                    required=False,
                    priority=20,
                    source_refs=_derived_source_refs("attachment", artifacts),
                ),
            )
        )
        return tuple(requests)

    def _build_summary_requests(
        self,
        session: SessionState,
        budgets: ContextBudgetPlan,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        hot_turns: tuple[str, ...],
        intent: IntentDecision | None,
        profile_snapshot_refs: tuple[str, ...],
        retrieval_requests: tuple[ContextRetrievalRequest, ...],
    ) -> tuple[ContextSummaryRequest, ...]:
        requests: list[ContextSummaryRequest] = []
        snapshot_goals = _snapshot_goals(goals, intent=intent)
        snapshot_retrieval_requests, replay_retrieval_requests = _split_retrieval_requests(retrieval_requests)
        snapshot_budget = budgets.allocation_for("session_snapshot")
        if snapshot_budget:
            requests.append(
                ContextSummaryRequest(
                    layer_name="session_snapshot",
                    source_refs=tuple(
                        dict.fromkeys(
                            (
                                *profile_snapshot_refs,
                                *(goal.goal_id for goal in snapshot_goals),
                                *(memory.memory_id for memory in memories),
                            )
                        )
                    ),
                    token_budget=snapshot_budget.allocated_tokens,
                    reason="compress the rebuildable session snapshot while keeping profile, work, and evidence slices inspectable",
                    required=True,
                )
            )
        replay_budget = budgets.allocation_for("replay_packet")
        if replay_budget and replay_retrieval_requests and (
            replay_budget.allocated_tokens < replay_budget.requested_tokens or len(replay_retrieval_requests) > 1
        ):
            requests.append(
                ContextSummaryRequest(
                    layer_name="replay_packet",
                    source_refs=tuple(
                        dict.fromkeys(
                            memory_id
                            for request in replay_retrieval_requests
                            for memory_id in request.memory_ids
                        )
                    ),
                    token_budget=replay_budget.allocated_tokens,
                    reason="summarize targeted replay slices while keeping slot and compression choices inspectable",
                    required=False,
                )
            )
        return tuple(requests)

    def _snapshot_retrieval_budget(
        self,
        budgets: ContextBudgetPlan,
        *,
        intent: IntentDecision | None,
    ) -> int:
        snapshot = budgets.allocation_for("session_snapshot")
        if snapshot is None:
            return 0
        if intent is not None and intent.budget_class == "narrow":
            return max(32, snapshot.allocated_tokens // 4)
        if intent is not None and intent.budget_class == "broad":
            return max(64, snapshot.allocated_tokens // 2)
        return max(48, snapshot.allocated_tokens // 3)

    def _suggest_retrieval_budget(
        self,
        memories: tuple[MemoryRecord, ...],
        *,
        intent: IntentDecision | None,
    ) -> int:
        if not memories:
            return 0
        base = min(128, max(24, len(memories) * 24))
        if intent is not None and intent.budget_class == "narrow":
            return max(24, base - 24)
        if intent is not None and intent.budget_class == "broad":
            return min(192, base + 48)
        return base

    def _build_source_trace(
        self,
        *,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        instruction_refs: tuple[str, ...],
        intent: IntentDecision | None,
        profile_snapshot_refs: tuple[str, ...],
        hot_turns: tuple[str, ...],
        procedure_overlays: tuple[str, ...],
        artifacts: tuple[str, ...],
        summary_requests: tuple[ContextSummaryRequest, ...],
        retrieval_requests: tuple[ContextRetrievalRequest, ...],
    ) -> tuple[ContextSourceTrace, ...]:
        warm_memories = _select_warm_memories(memories, session=session, goals=goals, intent=intent)
        snapshot_goals = _snapshot_goals(goals, intent=intent)
        warm_refs = tuple(memory.memory_id for memory in warm_memories)
        snapshot_retrieval_requests, replay_retrieval_requests = _split_retrieval_requests(retrieval_requests)
        retrieved_memory_ids = tuple(
            dict.fromkeys(memory_id for request in snapshot_retrieval_requests for memory_id in request.memory_ids)
        )
        replay_memory_ids = tuple(
            dict.fromkeys(memory_id for request in replay_retrieval_requests for memory_id in request.memory_ids)
        )
        omitted_snapshot_refs = tuple(
            memory.memory_id
            for memory in memories
            if memory.memory_id not in warm_refs and memory.memory_id not in retrieved_memory_ids and memory.memory_id not in replay_memory_ids
        )
        traces: list[ContextSourceTrace] = [
            ContextSourceTrace(
                layer_name="stable_prefix",
                selected_refs=instruction_refs,
                reason="stable policy and runtime guardrails stay in a dedicated prefix instead of mixing with volatile recall",
            ),
            ContextSourceTrace(
                layer_name="session_snapshot",
                selected_refs=tuple(
                    dict.fromkeys(
                        (
                            *profile_snapshot_refs,
                            *(goal.goal_id for goal in snapshot_goals),
                            *warm_refs,
                            *retrieved_memory_ids,
                        )
                    )
                ),
                reason=_session_snapshot_trace_reason(
                    session,
                    goals,
                    memories,
                    intent=intent,
                    profile_snapshot_refs=profile_snapshot_refs,
                    warm_memories=warm_memories,
                    retrieval_requests=snapshot_retrieval_requests,
                    summary_requests=summary_requests,
                ),
                omitted_refs=omitted_snapshot_refs,
            ),
        ]
        if replay_retrieval_requests:
            structured_turn_refs = tuple(memory.memory_id for memory in memories if parse_structured_turn_memory(memory) is not None)
            traces.append(
                ContextSourceTrace(
                    layer_name="replay_packet",
                    selected_refs=replay_memory_ids,
                    reason=_replay_packet_trace_reason(replay_retrieval_requests),
                    omitted_refs=tuple(
                        memory_id for memory_id in structured_turn_refs if memory_id not in replay_memory_ids
                    ),
                )
            )
        traces.extend(
            (
                ContextSourceTrace(
                    layer_name="turn_packet",
                    selected_refs=tuple(f"turn:{index}" for index, _ in enumerate(hot_turns, start=1)),
                    reason=_turn_packet_trace_reason(session, hot_turns),
                ),
                ContextSourceTrace(
                    layer_name="procedure_overlay",
                    selected_refs=_derived_source_refs("procedure", procedure_overlays),
                    reason=_procedure_overlay_trace_reason(procedure_overlays),
                ),
                ContextSourceTrace(
                    layer_name="workspace_attachments",
                    selected_refs=_derived_source_refs("attachment", artifacts),
                    reason=_workspace_attachment_trace_reason(artifacts),
                ),
            )
        )
        return tuple(traces)

class ContextRuntime(ContextCapability):
    """Capability adapter for layered context assembly."""

    def __init__(
        self,
        planner: ContextPlanner | None = None,
        renderer: PromptRenderer | None = None,
        instruction_refs: tuple[str, ...] = (),
        total_tokens: int = 2048,
    ) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="context.runtime",
            kind="context_assembler",
            version="1.0.0",
            metadata={"description": "Layered context assembly adapter."},
        )
        self._planner = planner or LayeredContextPlanner()
        self._renderer = renderer or MarkdownPromptRenderer()
        self._instruction_refs = instruction_refs
        self._total_tokens = total_tokens

    def plan(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        hot_turns: tuple[str, ...] = (),
        intent: IntentDecision | None = None,
        profile_snapshot_refs: tuple[str, ...] = (),
        procedure_overlays: tuple[str, ...] = (),
        artifacts: tuple[str, ...] = (),
        total_tokens: int | None = None,
    ) -> ContextAssemblyPlan:
        return self._planner.plan(
            session=session,
            goals=goals,
            memories=memories,
            total_tokens=total_tokens if total_tokens is not None else self._total_tokens,
            instruction_refs=self._instruction_refs,
            hot_turns=hot_turns,
            intent=intent,
            profile_snapshot_refs=profile_snapshot_refs,
            procedure_overlays=procedure_overlays,
            artifacts=artifacts,
        )

    def assemble(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        intent: IntentDecision | None = None,
    ) -> ContextBundle:
        plan = self.plan(session, goals, memories, intent=intent)
        rendered = self._renderer.render(plan)
        prompt_envelope = build_prompt_envelope(plan.frame)
        return ContextBundle(
            bundle_id=f"{session.session_id}:context",
            session_id=session.session_id,
            instruction_refs=self._instruction_refs,
            goal_ids=tuple(goal.goal_id for goal in goals),
            memory_ids=tuple(memory.memory_id for memory in memories),
            artifact_ids=(),
            token_budget=plan.total_tokens,
            prompt_envelope=prompt_envelope,
            rendered_prompt=rendered,
        )

    def assemble_detailed(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        hot_turns: tuple[str, ...] = (),
        intent: IntentDecision | None = None,
        profile_snapshot_refs: tuple[str, ...] = (),
        procedure_overlays: tuple[str, ...] = (),
        artifacts: tuple[str, ...] = (),
        total_tokens: int | None = None,
    ) -> ContextAssemblyResult:
        plan = self.plan(
            session,
            goals,
            memories,
            hot_turns=hot_turns,
            intent=intent,
            profile_snapshot_refs=profile_snapshot_refs,
            procedure_overlays=procedure_overlays,
            artifacts=artifacts,
            total_tokens=total_tokens,
        )
        rendered = self._renderer.render(plan)
        prompt_envelope = build_prompt_envelope(plan.frame)
        summary_by_layer = {
            layer.layer_name: layer.summary
            for layer in plan.layers
            if layer.summary is not None
        }
        retrieved_memory_ids = tuple(
            memory_id
            for request in plan.retrieval_requests
            for memory_id in request.memory_ids
        )
        bundle = ContextBundle(
            bundle_id=f"{session.session_id}:context",
            session_id=session.session_id,
            instruction_refs=self._instruction_refs,
            goal_ids=tuple(goal.goal_id for goal in goals),
            memory_ids=tuple(memory.memory_id for memory in memories),
            artifact_ids=artifacts,
            token_budget=plan.total_tokens,
            prompt_envelope=prompt_envelope,
            rendered_prompt=rendered,
        )
        return ContextAssemblyResult(
            bundle=bundle,
            plan=plan,
            rendered_prompt=rendered,
            summary_by_layer=summary_by_layer,
            retrieved_memory_ids=retrieved_memory_ids,
            source_trace=plan.source_trace,
            frame=plan.frame,
        )

__all__ = [
    "BudgetManager",
    "ContextAssemblyPlan",
    "ContextAssemblyResult",
    "ContextBudgetPlan",
    "ContextBudgetRequest",
    "ContextLayerBudget",
    "ContextLayerSnapshot",
    "ContextPlanner",
    "ContextRetrievalRequest",
    "ContextRuntime",
    "ContextSummaryRequest",
    "ContextSourceTrace",
    "DeterministicBudgetManager",
    "DeterministicRetrievalScheduler",
    "DeterministicSummaryHook",
    "LayeredContextPlanner",
    "MarkdownPromptRenderer",
    "ProcedureOverlay",
    "PromptRenderer",
    "ReplayPacket",
    "RetrievalScheduler",
    "SessionFrame",
    "SessionFrameBuilder",
    "SessionSnapshot",
    "StablePrefix",
    "SummaryHook",
    "TurnPacket",
    "WorkspaceAttachments",
]
