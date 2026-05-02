"""Gateway runtime adapter registration and app factory."""


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
    load_provider_selection,
    provider_selection_from_payload,
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

from .runtime_adapters import ChatBotMessagingAdapter, DiscordMessagingAdapter, FeishuMessagingAdapter, TelegramMessagingAdapter, WebhookMessagingAdapter
from .runtime_app import GatewayApp
from .runtime_capabilities import GatewayContextCapability, GatewayMemoryCapability, GatewayPlanningCapability, GatewayPreviewModelProvider, GatewaySurfaceModelProvider, GatewayTelemetrySink
from .runtime_support import *  # noqa: F401,F403

def register_builtin_gateway_adapters(registry: GatewayPluginRegistry) -> GatewayPluginRegistry:
    registry.register_adapter(
        GatewayAdapterDescriptor(
            key="chat_bot",
            adapter_id=CHAT_BOT_ADAPTER_ID,
            surface="local-chat",
            default_account_id=DEFAULT_GATEWAY_ACCOUNT_ID,
            operator_action="none",
        ),
        factory=lambda app: ChatBotMessagingAdapter(app=app),
    )
    registry.register_adapter(
        GatewayAdapterDescriptor(
            key="webhook",
            adapter_id=WEBHOOK_ADAPTER_ID,
            surface="generic-webhook",
            default_account_id=DEFAULT_GATEWAY_ACCOUNT_ID,
            operator_action="supply callback_url in inbound payload",
        ),
        factory=lambda app: WebhookMessagingAdapter(app=app),
    )
    registry.register_adapter(
        GatewayAdapterDescriptor(
            key="telegram",
            adapter_id=TELEGRAM_ADAPTER_ID,
            surface="telegram-bot-api",
            default_account_id=DEFAULT_GATEWAY_ACCOUNT_ID,
            operator_action="configure TELEGRAM_BOT_TOKEN and forward Bot API updates into the gateway",
            identity_mapping="account_id + chat.id + from.id (+ message_thread_id when present)",
            supported_updates=("message", "edited_message", "callback_query"),
            delivery_defaults={
                "private": "allow",
                "group": "review",
                "supergroup": "review",
                "channel": "review",
            },
        ),
        factory=lambda app: TelegramMessagingAdapter(app=app),
    )
    registry.register_adapter(
        GatewayAdapterDescriptor(
            key="discord",
            adapter_id=DISCORD_ADAPTER_ID,
            surface="discord-gateway",
            default_account_id=DEFAULT_GATEWAY_ACCOUNT_ID,
            operator_action="configure AEGIS_DISCORD_BOT_TOKEN, enable the MESSAGE_CONTENT intent, and run the managed Discord gateway service",
            identity_mapping="account_id + channel_id + author.id (+ thread_id when present)",
            preferred_transport="gateway",
            implemented_transports=("discord.py-gateway",),
            supported_events=("MESSAGE_CREATE", "THREAD_CREATE", "THREAD_UPDATE"),
            delivery_defaults={
                "direct": "allow",
                "channel": "review",
                "topic": "review",
            },
            delivery_api="/channels/{channel_id}/messages",
        ),
        factory=lambda app: DiscordMessagingAdapter(app=app),
    )
    registry.register_adapter(
        GatewayAdapterDescriptor(
            key="feishu",
            adapter_id=FEISHU_ADAPTER_ID,
            surface="feishu-messaging",
            default_account_id=DEFAULT_GATEWAY_ACCOUNT_ID,
            operator_action="configure gateway.adapters.feishu account env refs for the SDK long-connection path used by im.message.receive_v1",
            identity_mapping="account_id + chat_id + sender_id (+ root_id when replying in thread)",
            preferred_transport="long-connection",
            implemented_transports=(
                "python-sdk-long-connection",
            ),
            supported_events=("im.message.receive_v1",),
            delivery_defaults={
                "p2p": "allow",
                "group": "review",
            },
            delivery_api="/open-apis/im/v1/messages/:message_id/reply",
        ),
        factory=lambda app: FeishuMessagingAdapter(app=app),
    )
    return registry

def _builtin_gateway_plugin_registry() -> GatewayPluginRegistry:
    registry = GatewayPluginRegistry()
    return register_builtin_gateway_adapters(registry)

def build_gateway_app(
    *,
    profile_id: str = "profile:default",
    workspace_id: str | None = None,
    provider_profile: Mapping[str, Any] | None = None,
    profile_dir: str | Path | None = None,
    state_dir: str | Path | None = None,
    runtime_environ: Mapping[str, str] | None = None,
    plugin_registry: GatewayPluginRegistry | None = None,
) -> tuple[GatewayApp, ChatBotMessagingAdapter, WebhookMessagingAdapter]:
    registry = plugin_registry or _builtin_gateway_plugin_registry()
    resolved_profile_dir = Path(profile_dir) if profile_dir is not None else None
    resolved_state_dir = Path(state_dir) if state_dir is not None else None
    loaded_profile: LoadedProfile | None = None

    if resolved_profile_dir is not None:
        loader = ProfileLoader(resolved_profile_dir)
        loaded_profile = (
            loader.load()
            if profile_id == "profile:default"
            else loader.load(profile_id=profile_id)
        )
        profile_id = loaded_profile.state.profile_id
    else:
        loaded_profile = _default_loaded_profile(profile_id)

    if resolved_state_dir is None:
        identity_store = InMemoryGatewayIdentityStore()
        session_store = InMemoryGatewaySessionStore()
    else:
        identity_store = FileGatewayIdentityStore(
            resolved_state_dir / "gateway-identities.json"
        )
        session_store = FileGatewaySessionStore(
            resolved_state_dir / "gateway-sessions.json"
        )

    telemetry = GatewayTelemetrySink()
    core = GatewayCoreService(
        GatewayCoreDependencies(
            identity_store=identity_store,
            session_store=session_store,
            security_policy=SecurityPolicy.default(),
            default_profile_id=profile_id,
            default_workspace_id=workspace_id,
            telemetry_sink=telemetry,
        )
    )
    runtime_repository = RuntimeStorageRepository(_runtime_database_path(resolved_state_dir))
    runtime_repository.bootstrap()
    runtime_repository.upsert_profile(loaded_profile.state)
    auth_store = PersistentAuthProfileStore(runtime_repository)

    strong_provider_profile: AuthProfile | None = None
    weak_provider_profile: AuthProfile | None = None
    intent_mode = "skip"
    if provider_profile is None and resolved_profile_dir is not None:
        selection = load_provider_selection(resolved_profile_dir)
        strong_provider_profile = selection.strong_profile
        weak_provider_profile = selection.weak_profile
        intent_mode = selection.intent_mode
    elif provider_profile is not None:
        selection = provider_selection_from_payload(provider_profile)
        strong_provider_profile = selection.strong_profile
        weak_provider_profile = selection.weak_profile
        intent_mode = selection.intent_mode
    if strong_provider_profile is not None:
        auth_store.register(strong_provider_profile)
    if weak_provider_profile is not None:
        auth_store.register(weak_provider_profile)

    preview_model_provider = GatewayPreviewModelProvider()
    model_provider = GatewaySurfaceModelProvider(
        repository=runtime_repository,
        fallback=preview_model_provider,
        active_provider_profile=strong_provider_profile,
        weak_provider_profile=weak_provider_profile,
        intent_mode=intent_mode,
        runtime_environ=runtime_environ,
    )
    provider_runtime = dict(model_provider.describe())
    memory_runtime = MemoryRuntime.from_repository(runtime_repository)
    kernel = KernelService(
        dependencies=KernelDependencies(
            storage=runtime_repository,
            context=GatewayContextCapability(loaded_profile),
            planning=GatewayPlanningCapability(PlanningService()),
            memory=GatewayMemoryCapability(memory_runtime),
            model_provider=model_provider,
            telemetry=telemetry,
            embedding_service=memory_runtime.retriever.evidence_retriever.embedding_service,
        )
    )

    app = GatewayApp(
        core=core,
        profile_id=profile_id,
        workspace_id=workspace_id,
        provider_runtime=provider_runtime,
        repository=runtime_repository,
        auth_store=auth_store,
        memory_runtime=memory_runtime,
        kernel=kernel,
        telemetry=telemetry,
        model_provider=model_provider,
        plugin_registry=registry,
        profile_dir=str(resolved_profile_dir) if resolved_profile_dir is not None else None,
        state_dir=str(resolved_state_dir) if resolved_state_dir is not None else None,
        loaded_profile=loaded_profile,
        provider_profile=strong_provider_profile,
    )
    chat_adapter = registry.create_adapter("chat_bot", app)
    webhook_adapter = registry.create_adapter("webhook", app)
    if not isinstance(chat_adapter, ChatBotMessagingAdapter):
        raise TypeError("gateway adapter plugin 'chat_bot' must build ChatBotMessagingAdapter")
    if not isinstance(webhook_adapter, WebhookMessagingAdapter):
        raise TypeError("gateway adapter plugin 'webhook' must build WebhookMessagingAdapter")
    return (
        app,
        chat_adapter,
        webhook_adapter,
    )
