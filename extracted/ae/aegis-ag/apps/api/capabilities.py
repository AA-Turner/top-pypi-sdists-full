"""API capability adapters and deterministic preview providers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime
from typing import Any
from uuid import uuid4

from packages.capabilities.runtime import (
    CapabilityDescriptor,
    ContextCapability,
    DeliveryAdapterCapability,
    MemoryCapability,
    ModelProviderCapability,
    PlanningCapability,
    TelemetrySinkCapability,
    ToolCapability,
)
from packages.context import ContextRuntime
from packages.contracts import (
    ActivityGraph,
    ContextBundle,
    EventEnvelope,
    ExecutionResult,
    GoalNode,
    IntentDecision,
    MemoryRecord,
    MixtureModelSelection,
    ProfileState,
    SessionState,
    StrongModelProfile,
    WeakModelProfile,
)
from packages.evidence import MemoryRuntime
from packages.planning import PlanningDecision, PlanningMode, PlanningService, goal_graph_to_activity_graph, activity_graph_to_goal_graph
from packages.tools import ToolRuntime


class APITelemetrySink(TelemetrySinkCapability):
    def __init__(self) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.telemetry",
            kind="telemetry_sink",
            version="1.0.0",
            metadata={"description": "In-process telemetry sink for API wiring."},
        )
        self._events: list[dict[str, Any]] = []

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._events)

    def emit(self, event: Mapping[str, Any]) -> None:
        self._events.append(dict(event))


class APIMemoryCapability(MemoryCapability):
    def __init__(self, store: MemoryRuntime) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.memory",
            kind="memory",
            version="1.0.0",
            metadata={"description": "Memory adapter for API-backed kernel flows."},
        )
        self.store = store

    def record(self, memory: MemoryRecord) -> None:
        self.store.store.upsert(memory)

    def search(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> tuple[MemoryRecord, ...]:
        result = self.store.retrieve(
            session_id,
            query,
            goal_ids=goal_ids,
            scope_session_ids=scope_session_ids,
            scope_reason=scope_reason,
        )
        return tuple(candidate.record for candidate in result.candidates)


class APIContextCapability(ContextCapability):
    def __init__(self, runtime: ContextRuntime) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.context",
            kind="context",
            version="1.0.0",
            metadata={"description": "Layered context adapter for API flows."},
        )
        self.runtime = runtime

    def assemble(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        intent: IntentDecision | None = None,
    ) -> ContextBundle:
        return self.runtime.assemble(session, goals, memories, intent=intent)


class APIPlanningCapability(PlanningCapability):
    def __init__(self, service: PlanningService) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.planning",
            kind="planning",
            version="1.0.0",
            metadata={"description": "Plan draft adapter for API flows."},
        )
        self.service = service

    def choose_next_step(
        self,
        *,
        session: SessionState,
        graph: ActivityGraph,
        memories: tuple[MemoryRecord, ...] = (),
        mode: PlanningMode = "guided",
        initiative_hint: str | None = None,
        continuity_notes: tuple[str, ...] = (),
        now: datetime | None = None,
    ) -> PlanningDecision:
        return self.service.choose_next_step(
            session=session,
            graph=activity_graph_to_goal_graph(graph),
            memories=memories,
            mode=mode,
            initiative_hint=initiative_hint,
            continuity_notes=continuity_notes,
            now=now,
        )

    def maintain_goal_graph(
        self,
        *,
        session: SessionState,
        graph: ActivityGraph,
        prompt: str,
        goal_query: str | None = None,
        event: EventEnvelope | None = None,
        now: datetime | None = None,
    ):
        result = self.service.maintain_goal_graph(
            session=session,
            graph=activity_graph_to_goal_graph(graph),
            prompt=prompt,
            goal_query=goal_query,
            event=event,
            now=now,
        )
        return replace(result, graph=goal_graph_to_activity_graph(result.graph))

    def reconcile_goal_graph(
        self,
        *,
        session: SessionState,
        graph: ActivityGraph,
        prompt: str,
        execution: ExecutionResult,
        decision: PlanningDecision | None = None,
        event: EventEnvelope | None = None,
        now: datetime | None = None,
    ):
        result = self.service.reconcile_goal_graph(
            session=session,
            graph=activity_graph_to_goal_graph(graph),
            prompt=prompt,
            execution=execution,
            decision=decision,
            event=event,
            now=now,
        )
        return replace(result, graph=goal_graph_to_activity_graph(result.graph))


class APIDeliveryCapability(DeliveryAdapterCapability):
    def __init__(self) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.delivery",
            kind="delivery",
            version="1.0.0",
            metadata={"description": "Delivery adapter for API controlled execution."},
        )

    def deliver(self, session_id: str, payload: Mapping[str, Any]) -> ExecutionResult:
        summary = str(payload.get("summary", "delivered response"))
        return ExecutionResult(
            execution_id=f"delivery:{session_id}:{uuid4().hex}",
            session_id=session_id,
            outcome="ok",
            summary=summary,
            side_effects=("delivery",),
        )


class APIModelProvider(ModelProviderCapability):
    def __init__(self) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.model",
            kind="model_provider",
            version="1.0.0",
            metadata={"description": "Deterministic model adapter for API flows."},
        )

    def selection_state(self) -> MixtureModelSelection:
        return MixtureModelSelection(
            strong_model=StrongModelProfile(
                profile_id="api-preview:strong",
                provider_id="api-preview",
                model_id="api-preview-strong",
            ),
            weak_model=WeakModelProfile(
                profile_id="api-preview:weak",
                provider_id="api-preview",
                model_id="api-preview-weak",
            ),
            intent_mode="skip",
        )

    def generate(
        self,
        *,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        prompt: str,
        model_role: str = "strong",
    ) -> ExecutionResult:
        summary = prompt.strip() or "acknowledged"
        if context.rendered_prompt:
            summary = f"{summary} | context: {context.rendered_prompt.splitlines()[0]}"
        return ExecutionResult(
            execution_id=f"model:{session.session_id}:{uuid4().hex}",
            session_id=session.session_id,
            outcome="ok",
            summary=summary,
            side_effects=(profile.mode, f"model_role={model_role}"),
        )


class APIToolExecution(ToolCapability):
    def __init__(self, runtime: ToolRuntime) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="api.tools",
            kind="tool",
            version="1.0.0",
            metadata={"description": "API tool runtime."},
        )
        self.runtime = runtime

    def invoke(
        self,
        tool_name: str,
        arguments: Mapping[str, Any],
        *,
        session_id: str,
    ) -> ExecutionResult:
        return self.runtime.invoke(tool_name, arguments, session_id=session_id)
