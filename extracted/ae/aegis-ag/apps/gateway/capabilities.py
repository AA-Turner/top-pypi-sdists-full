"""Gateway capability adapters and provider bridges."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime
from typing import Any
from uuid import uuid4

from apps.provider_runtime import SurfaceModelProviderCapability
from packages.auth import AuthProfile
from packages.capabilities.runtime import (
    CapabilityDescriptor,
    ContextCapability,
    MemoryCapability,
    ModelProviderCapability,
    PlanningCapability,
    TelemetrySinkCapability,
)
from packages.context import ContextRuntime
from packages.contracts.runtime import (
    ContextBundle,
    EventEnvelope,
    ExecutionResult,
    GoalNode,
    IntentDecision,
    MemoryRecord,
    ProfileState,
    SessionState,
    ActivityGraph,
)
from packages.evidence import MemoryRuntime
from packages.planning import PlanningDecision, PlanningMode, PlanningService
from packages.state import LoadedProfile, build_prompt_contract
from packages.storage import RuntimeStorageRepository


class GatewayTelemetrySink(TelemetrySinkCapability):
    def __init__(self) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="gateway.telemetry",
            kind="telemetry_sink",
            version="1.0.0",
            metadata={"description": "In-process telemetry sink for gateway shared-runtime turns."},
        )
        self._events: list[dict[str, Any]] = []

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._events)

    def emit(self, event: Mapping[str, Any]) -> None:
        self._events.append(dict(event))


class GatewayMemoryCapability(MemoryCapability):
    def __init__(self, runtime: MemoryRuntime) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="gateway.memory",
            kind="memory",
            version="1.0.0",
            metadata={"description": "Shared memory adapter for gateway turns."},
        )
        self.runtime = runtime

    def record(self, memory: MemoryRecord) -> None:
        self.runtime.store.upsert(memory)

    def search(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> tuple[MemoryRecord, ...]:
        result = self.runtime.retrieve(
            session_id,
            query,
            goal_ids=goal_ids,
            scope_session_ids=scope_session_ids,
            scope_reason=scope_reason,
        )
        return tuple(candidate.record for candidate in result.candidates)


class GatewayContextCapability(ContextCapability):
    def __init__(self, profile: LoadedProfile, *, total_tokens: int = 3072) -> None:
        self.prompt_contract = build_prompt_contract(profile, prompt_mode="full")
        self.descriptor = CapabilityDescriptor(
            capability_id="gateway.context",
            kind="context",
            version="1.0.0",
            metadata={"description": "Prompt-contract-aware context adapter for gateway turns."},
        )
        self.runtime = ContextRuntime(
            instruction_refs=self.prompt_contract.instruction_refs,
            total_tokens=total_tokens,
        )

    def assemble(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        intent: IntentDecision | None = None,
    ) -> ContextBundle:
        bundle = self.runtime.assemble(session, goals, memories, intent=intent)
        return replace(
            bundle,
            bundle_id=f"bundle:{session.session_id}:{len(goals)}:{len(memories)}",
            instruction_refs=self.prompt_contract.instruction_refs,
        )


class GatewayPlanningCapability(PlanningCapability):
    def __init__(self, service: PlanningService) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="gateway.planning",
            kind="planning",
            version="1.0.0",
            metadata={"description": "Shared planning adapter for gateway turns."},
        )
        self.service = service

    def choose_next_step(
        self,
        *,
        session: SessionState,
        graph: ActivityGraph,
        memories: tuple[MemoryRecord, ...] = (),
        mode: PlanningMode = "guided",
        now: datetime | None = None,
    ) -> PlanningDecision:
        return self.service.choose_next_step(
            session=session,
            graph=graph,
            memories=memories,
            mode=mode,
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
        return self.service.maintain_goal_graph(
            session=session,
            graph=graph,
            prompt=prompt,
            goal_query=goal_query,
            event=event,
            now=now,
        )

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
        return self.service.reconcile_goal_graph(
            session=session,
            graph=graph,
            prompt=prompt,
            execution=execution,
            decision=decision,
            event=event,
            now=now,
        )


class GatewayPreviewModelProvider(ModelProviderCapability):
    def __init__(self) -> None:
        self.descriptor = CapabilityDescriptor(
            capability_id="gateway.model.preview",
            kind="model_provider",
            version="1.0.0",
            metadata={"description": "Deterministic conversational fallback for gateway turns."},
        )

    def generate(
        self,
        *,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        prompt: str,
    ) -> ExecutionResult:
        normalized = prompt.strip()
        lowered = normalized.lower()
        if not normalized:
            summary = "I'm here with you."
        elif "who are you" in lowered:
            summary = "I'm Aegis, your persistent AI, staying with the thread across time."
        elif normalized.endswith("?"):
            summary = f"I’m tracking this with you: {normalized}"
        else:
            summary = f"I’m with you on this: {normalized}"
        return ExecutionResult(
            execution_id=f"gateway.model:{session.session_id}:{uuid4().hex}",
            session_id=session.session_id,
            outcome="ok",
            summary=summary,
            side_effects=("gateway-preview-provider", profile.mode),
        )


class GatewaySurfaceModelProvider(ModelProviderCapability):
    def __init__(
        self,
        *,
        repository: RuntimeStorageRepository,
        fallback: ModelProviderCapability,
        active_provider_profile: AuthProfile | None,
    ) -> None:
        profile_id = active_provider_profile.profile_id if active_provider_profile is not None else None
        provider_id = active_provider_profile.provider_id if active_provider_profile is not None else None
        self.surface = SurfaceModelProviderCapability(
            repository=repository,
            secret_key_path=repository.database_path.parent / "provider-secrets.key",
            fallback=fallback,
            strong_provider_profile_id=profile_id,
            weak_provider_profile_id=profile_id,
            active_provider_id=provider_id,
            capability_id="gateway.model.runtime",
            surface_label="gateway",
        )
        self.descriptor = self.surface.descriptor
        self.fallback = fallback

    def describe(self) -> Mapping[str, object]:
        return self.surface.describe()

    def selection_state(self) -> MixtureModelSelection:
        return self.surface.selection_state()

    def generate(
        self,
        *,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        prompt: str,
        model_role: str = "strong",
    ) -> ExecutionResult:
        try:
            return self.surface.generate(
                profile=profile,
                session=session,
                context=context,
                prompt=prompt,
                model_role=model_role,
            )
        except LookupError:
            return self.fallback.generate(
                profile=profile,
                session=session,
                context=context,
                prompt=prompt,
                model_role=model_role,
            )
