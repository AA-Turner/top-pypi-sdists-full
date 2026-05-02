"""Gateway runtime application and voice exchange."""


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
    ContextBundle,
    EventEnvelope,
    ExecutionResult,
    GoalNode,
    MemoryRecord,
    ProfileState,
    SessionState,
    ActivityGraph,
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
from packages.kernel.context_compaction import (
    flush_projection_memory,
    projection_compaction_detail,
)
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
from .runtime_capabilities import GatewayContextCapability, GatewayMemoryCapability, GatewayPlanningCapability, GatewayPreviewModelProvider, GatewaySurfaceModelProvider, GatewayTelemetrySink

@dataclass(frozen=True, slots=True)
class GatewayApp:
    core: GatewayCoreService
    profile_id: str
    provider_runtime: Mapping[str, object]
    repository: RuntimeStorageRepository
    auth_store: PersistentAuthProfileStore
    memory_runtime: MemoryRuntime
    kernel: KernelService
    telemetry: GatewayTelemetrySink
    model_provider: GatewaySurfaceModelProvider
    plugin_registry: GatewayPluginRegistry | None = None
    workspace_id: str | None = None
    profile_dir: str | None = None
    state_dir: str | None = None
    loaded_profile: LoadedProfile | None = None
    provider_profile: AuthProfile | None = None

    def handle_message(
        self,
        inbound: GatewayInboundMessage,
        *,
        reply_body: str | None = None,
        reply_to_message_id: str | None = None,
        attachment_refs: tuple[GatewayAttachmentRef, ...] = (),
        metadata: Mapping[str, object] | None = None,
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
    ) -> GatewayExchange:
        route = self.core.route_inbound(
            inbound,
            profile_id=self.profile_id,
            workspace_id=self.workspace_id,
        )
        session = self._ensure_runtime_session(route.session)
        event = self._event_for_inbound(inbound, session_id=session.session_id)
        self.memory_runtime.append_event(event)
        outcome = self.kernel.run(
            KernelTurnRequest(
                event=event,
                prompt=inbound.body,
            )
        )
        self._run_context_hygiene(outcome.session.session_id, event_id=event.event_id)
        refreshed_session = outcome.session
        self.core.dependencies.session_store.save(refreshed_session)
        route = replace(route, session=refreshed_session)
        provider_summary = self.model_provider.describe()
        delivery = self.core.deliver(
            route,
            body=reply_body or outcome.execution.summary,
            reply_to_message_id=reply_to_message_id
            or inbound.reply_to_message_id
            or inbound.event_id,
            attachment_refs=attachment_refs,
            metadata={
                **dict(metadata or {}),
                "runtime_surface": "gateway.shared-runtime",
                "context_bundle_id": outcome.context.bundle_id,
                "execution_id": outcome.execution.execution_id,
                "provider_id": str(provider_summary.get("provider_id") or "preview"),
            },
            target_trusted=target_trusted,
            consent_given=consent_given,
            is_external=is_external,
        )
        return GatewayExchange(route=route, delivery=delivery)

    def _run_context_hygiene(self, session_id: str, *, event_id: str) -> None:
        compact = getattr(self.kernel.dependencies.context, "force_projection_compaction", None)
        if not callable(compact):
            return
        result = compact(reason="gateway-hygiene", session_id=session_id)
        if result is None or not bool(getattr(result, "compacted", False)):
            return
        recorded_at = datetime.now(timezone.utc).isoformat()
        self.telemetry.emit(
            {
                "event_id": f"telemetry:{session_id}:context-compact:{uuid4().hex}",
                "event_type": "kernel.stage",
                "session_id": session_id,
                "source": "gateway",
                "payload": {
                    "stage": "context-compact",
                    "detail": projection_compaction_detail(result),
                    "recorded_at": recorded_at,
                    "event_id": event_id,
                },
            }
        )
        flush_projection_memory(self.kernel.dependencies.context)

    def provider_summary(self) -> Mapping[str, object]:
        return dict(self.model_provider.describe())

    def voice_summary(self) -> Mapping[str, object]:
        return self._build_voice_service().provider_summary()

    def voice_doctor(self) -> Mapping[str, object]:
        if self.loaded_profile is None:
            return {
                "status": "not-ready",
                "checks": (
                    {"check": "profile_bundle", "status": "missing"},
                ),
                "supported_path": "one-shot gateway voice remains subordinate to the text delivery path",
                "non_goals": (
                    "always-on duplex voice",
                    "provider-specific delivery forks in the gateway layer",
                ),
                "provider": self.voice_summary(),
            }
        return self._build_voice_service().doctor(self.loaded_profile)

    def setup_summary(self) -> Mapping[str, object]:
        registry = self.plugin_registry or _builtin_gateway_plugin_registry()
        return {
            "profile_id": self.profile_id,
            "profile_dir": self.profile_dir,
            "state_dir": self.state_dir,
            "workspace_id": self.workspace_id,
            "adapters": registry.adapter_id_map(),
            "adapter_setup": registry.adapter_setup_payload(),
            "provider": dict(self.model_provider.describe()),
            "voice": dict(self.voice_summary()),
        }

    def identity_records(self) -> tuple[GatewayIdentityRecord, ...]:
        return self.core.dependencies.identity_store.list_records()

    def session_records(self) -> tuple[SessionState, ...]:
        return self.core.dependencies.session_store.list_records()

    def memory_records(self, session_id: str | None = None) -> tuple[MemoryRecord, ...]:
        return self.memory_runtime.store.list(session_id=session_id)

    def interrupt_session(
        self,
        session_id: str,
        *,
        interruption_state: str,
        interrupted_at: datetime | None = None,
    ) -> SessionState:
        session = self.core.dependencies.session_store.lookup(session_id)
        if session is None:
            raise KeyError(session_id)
        updated = replace(
            session,
            status="interrupted",
            interruption_state=interruption_state,
            updated_at=interrupted_at or _utc_now(),
        )
        self.core.dependencies.session_store.save(updated)
        self.repository.upsert_session(updated)
        return updated

    def handle_voice_message(
        self,
        inbound: GatewayInboundMessage,
        *,
        audio_bytes: bytes,
        audio_name: str,
        audio_format: str | None = None,
        reply_body: str | None = None,
        reply_to_message_id: str | None = None,
        attachment_refs: tuple[GatewayAttachmentRef, ...] = (),
        metadata: Mapping[str, object] | None = None,
        target_trusted: bool | None = None,
        consent_given: bool | None = None,
        is_external: bool | None = None,
        voice_output_enabled: bool = False,
        output_audio_format: str = "mp3",
    ) -> "GatewayVoiceExchange":
        if self.loaded_profile is None:
            raise ValueError("gateway voice mode requires a loaded profile bundle")
        voice_service = self._build_voice_service()
        resolved_consent_given = (
            inbound.policy_hint.consent_default
            if consent_given is None
            else consent_given
        )
        voice_session = voice_service.open_session(
            self.loaded_profile,
            f"session:{inbound.adapter_id}:{inbound.account_id}:{inbound.conversation_id}",
        )
        resolution = voice_service.resolve_input(
            self.loaded_profile,
            voice_session,
            VoiceInputRequest(
                request_id=f"{inbound.event_id}:voice",
                session_id=voice_session.session_id,
                profile_id=self.profile_id,
                source="provider-backed",
                consent_given=resolved_consent_given,
                recording_enabled=False,
                metadata={
                    "adapter_id": inbound.adapter_id,
                    "account_id": inbound.account_id,
                },
                audio_bytes=audio_bytes,
                audio_format=audio_format,
                audio_name=audio_name,
            ),
        )
        normalized_inbound = GatewayInboundMessage(
            event_id=inbound.event_id,
            account=inbound.account,
            conversation=inbound.conversation,
            sender=inbound.sender,
            body=resolution.transcript or inbound.body,
            body_format=inbound.body_format,
            reply_to_message_id=inbound.reply_to_message_id,
            attachment_refs=inbound.attachment_refs,
            policy_hint=inbound.policy_hint,
            received_at=inbound.received_at,
            metadata={
                **dict(inbound.metadata),
                "voice_input_source": resolution.request.source,
                **{key: value for key, value in resolution.metadata.items() if value},
            },
        )
        exchange = self.handle_message(
            normalized_inbound,
            reply_body=reply_body,
            reply_to_message_id=reply_to_message_id,
            attachment_refs=attachment_refs,
            metadata=metadata,
            target_trusted=target_trusted,
            consent_given=consent_given,
            is_external=is_external,
        )
        voice_turn = voice_service.complete_output(
            self.loaded_profile,
            voice_session,
            resolution,
            response_transcript=exchange.delivery.summary,
            voice_output_enabled=voice_output_enabled,
            audio_format=output_audio_format,
        )
        if exchange.delivery.outbound is not None:
            outbound = replace(
                exchange.delivery.outbound,
                metadata={
                    **dict(exchange.delivery.outbound.metadata),
                    **(
                        dict(voice_turn.output.metadata)
                        if voice_turn.output is not None and voice_turn.output.metadata is not None
                        else {}
                    ),
                    "voice_output_mode": voice_turn.output.delivery_mode if voice_turn.output is not None else "text",
                    "voice_output_provider_id": (
                        voice_turn.output.provider_id
                        if voice_turn.output is not None and voice_turn.output.provider_id is not None
                        else ""
                    ),
                },
            )
            exchange = GatewayExchange(
                route=exchange.route,
                delivery=replace(exchange.delivery, outbound=outbound),
            )
        return GatewayVoiceExchange(
            exchange=exchange,
            input_resolution=resolution,
            voice_turn=voice_turn,
        )

    def _build_voice_service(self):
        return build_provider_voice_service(provider_profile=self.provider_profile)

    def _ensure_runtime_session(self, session: SessionState) -> SessionState:
        existing = self.repository.load_session(session.session_id)
        if existing is None:
            resolved = session
        else:
            resolved = replace(
                existing,
                workspace_id=session.workspace_id,
                status=session.status,
                updated_at=session.updated_at,
                interruption_state=session.interruption_state,
            )
        self.repository.upsert_session(resolved)
        return resolved

    def _event_for_inbound(
        self,
        inbound: GatewayInboundMessage,
        *,
        session_id: str,
    ) -> EventEnvelope:
        payload = {
            "message": inbound.body,
            "content": inbound.body,
            "summary": inbound.body,
            "adapter_id": inbound.adapter_id,
            "account_id": inbound.account_id,
            "delivery_surface": inbound.account.surface or "",
            "conversation_id": inbound.conversation_id,
            "parent_conversation_id": inbound.parent_conversation_id or "",
            "thread_id": inbound.thread_id or "",
            "chat_type": inbound.chat_type or "",
            "external_user_id": inbound.external_user_id,
            "display_name": inbound.display_name or "",
            "attachments": ",".join(inbound.attachments),
            **_string_payload(inbound.metadata),
        }
        return EventEnvelope(
            event_id=f"gateway:{inbound.event_id}",
            event_type="turn.received",
            session_id=session_id,
            source=f"gateway:{inbound.adapter_id}",
            payload=payload,
        )

@dataclass(frozen=True, slots=True)
class GatewayVoiceExchange:
    exchange: GatewayExchange
    input_resolution: VoiceInputResolution
    voice_turn: VoiceTurnResult
