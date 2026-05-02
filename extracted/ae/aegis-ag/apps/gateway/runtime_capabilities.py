"""Gateway runtime capabilities."""


from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import tempfile
from typing import Any
from uuid import uuid4

from apps.provider_runtime import (
    EnvironmentSecretStore,
    SurfaceModelProviderCapability,
    load_provider_profile,
    provider_fallback_summary,
    provider_profile_from_payload,
    provider_profile_summary,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore, ProfileCredentialResolver
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
from packages.gateway_core import (
    DEFAULT_GATEWAY_ACCOUNT_ID,
    FileGatewayIdentityStore,
    FileGatewaySessionStore,
    GatewayAccountRef,
    GatewayAttachmentRef,
    GatewayConversationRef,
    GatewayCoreDependencies,
    GatewayCoreService,
    GatewayExchange,
    GatewayIdentityRecord,
    GatewayInboundMessage,
    GatewayOutboundMessage,
    GatewayPolicyHint,
    GatewaySenderRef,
    InMemoryGatewayIdentityStore,
    InMemoryGatewaySessionStore,
)
from packages.kernel import KernelDependencies, KernelService, KernelTurnRequest, ObservationPipeline, StateReconciler
from packages.evidence import MemoryRuntime
from packages.planning import PlanningDecision, PlanningMode, PlanningService
from packages.state import DEFAULT_CLONE_TEXT, LoadedProfile, ProfileLoader, build_prompt_contract
from packages.security.runtime import SecurityPolicy
from packages.storage import RuntimeStorageRepository
from packages.voice import VoiceInputRequest, VoiceInputResolution, VoiceTurnResult, build_provider_voice_service

from .plugins import GatewayAdapterDescriptor, GatewayPluginRegistry

CHAT_BOT_ADAPTER_ID = "messaging.chat-bot"
WEBHOOK_ADAPTER_ID = "messaging.webhook"
TELEGRAM_ADAPTER_ID = "messaging.telegram"
FEISHU_ADAPTER_ID = "messaging.feishu"
DISCORD_ADAPTER_ID = "messaging.discord"

from .runtime_support import *  # noqa: F401,F403

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
        initiative_hint: str | None = None,
        continuity_notes: tuple[str, ...] = (),
        now: datetime | None = None,
    ) -> PlanningDecision:
        return self.service.choose_next_step(
            session=session,
            graph=graph,
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

    def selection_state(self) -> MixtureModelSelection:
        return MixtureModelSelection(
            strong_model=StrongModelProfile(
                profile_id="gateway-preview:strong",
                provider_id="gateway-preview",
                model_id="gateway-preview-strong",
            ),
            weak_model=WeakModelProfile(
                profile_id="gateway-preview:weak",
                provider_id="gateway-preview",
                model_id="gateway-preview-weak",
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
            side_effects=("gateway-preview-provider", profile.mode, f"model_role={model_role}"),
        )

class GatewaySurfaceModelProvider(ModelProviderCapability):
    def __init__(
        self,
        *,
        repository: RuntimeStorageRepository,
        fallback: ModelProviderCapability,
        active_provider_profile: AuthProfile | None,
        weak_provider_profile: AuthProfile | None = None,
        intent_mode: str = "skip",
        runtime_environ: Mapping[str, str] | None = None,
    ) -> None:
        credential_resolver = None
        if runtime_environ is not None:
            credential_resolver = ProfileCredentialResolver(EnvironmentSecretStore(runtime_environ))
        strong_profile_id = active_provider_profile.profile_id if active_provider_profile is not None else None
        weak_profile_id = weak_provider_profile.profile_id if weak_provider_profile is not None else strong_profile_id
        provider_id = active_provider_profile.provider_id if active_provider_profile is not None else None
        self.surface = SurfaceModelProviderCapability(
            repository=repository,
            secret_key_path=repository.database_path.parent / "provider-secrets.key",
            fallback=fallback,
            credential_resolver=credential_resolver,
            strong_provider_profile_id=strong_profile_id,
            weak_provider_profile_id=weak_profile_id,
            active_provider_id=provider_id,
            capability_id="gateway.model.runtime",
            surface_label="gateway",
            intent_mode=intent_mode,
            bootstrap_state_dir=repository.database_path.parent,
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
