"""Gateway runtime factory helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import tempfile
from typing import Any

from apps.provider_runtime import (
    load_provider_profile,
    provider_fallback_summary,
    provider_profile_from_payload,
    provider_profile_summary,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore
from packages.gateway_core import (
    FileGatewayIdentityStore,
    FileGatewaySessionStore,
    GatewayCoreDependencies,
    GatewayCoreService,
    InMemoryGatewayIdentityStore,
    InMemoryGatewaySessionStore,
)
from packages.kernel import KernelDependencies, KernelService
from packages.evidence import MemoryRuntime
from packages.planning import PlanningService
from packages.state import DEFAULT_CLONE_TEXT, LoadedProfile, ProfileLoader
from packages.security.runtime import SecurityPolicy
from packages.contracts.runtime import ProfileState
from packages.storage import RuntimeStorageRepository

from .capabilities import (
    GatewayContextCapability,
    GatewayMemoryCapability,
    GatewayPlanningCapability,
    GatewayPreviewModelProvider,
    GatewaySurfaceModelProvider,
    GatewayTelemetrySink,
)
from .runtime import (
    ChatBotMessagingAdapter,
    GatewayApp,
    WebhookMessagingAdapter,
)


@dataclass(frozen=True, slots=True)
class GatewayStorageBundle:
    identity_store: InMemoryGatewayIdentityStore | FileGatewayIdentityStore
    session_store: InMemoryGatewaySessionStore | FileGatewaySessionStore


@dataclass(frozen=True, slots=True)
class GatewayProviderBundle:
    provider_runtime: Mapping[str, object]
    provider_profile: AuthProfile | None


def _runtime_database_path(state_dir: Path | None) -> Path:
    if state_dir is not None:
        state_dir.mkdir(parents=True, exist_ok=True)
        return state_dir / "gateway-runtime.sqlite3"
    return Path(tempfile.mkdtemp(prefix="aegis-gateway-runtime-")) / "gateway-runtime.sqlite3"


def _default_loaded_profile(profile_id: str) -> LoadedProfile:
    state = ProfileState(
        profile_id=profile_id,
        display_name="Aegis",
        mode="companion",
    )
    return LoadedProfile(
        state=state,
        companion=None,
        profile_dir="",
        manifest_path=None,
        clone_text=DEFAULT_CLONE_TEXT,
    )


def build_gateway_app(
    *,
    profile_id: str = "profile:default",
    workspace_id: str | None = None,
    provider_profile: Mapping[str, Any] | None = None,
    profile_dir: str | Path | None = None,
    state_dir: str | Path | None = None,
) -> tuple[GatewayApp, ChatBotMessagingAdapter, WebhookMessagingAdapter]:
    resolved_profile_dir = Path(profile_dir) if profile_dir is not None else None
    resolved_state_dir = Path(state_dir) if state_dir is not None else None
    loaded_profile = _resolve_loaded_profile(profile_id=profile_id, profile_dir=resolved_profile_dir)
    storage = _build_gateway_storage(resolved_state_dir)

    telemetry = GatewayTelemetrySink()
    core = GatewayCoreService(
        GatewayCoreDependencies(
            identity_store=storage.identity_store,
            session_store=storage.session_store,
            security_policy=SecurityPolicy.default(),
            default_profile_id=loaded_profile.state.profile_id,
            default_workspace_id=workspace_id,
            telemetry_sink=telemetry,
        )
    )
    runtime_repository = RuntimeStorageRepository(_runtime_database_path(resolved_state_dir))
    runtime_repository.bootstrap()
    runtime_repository.upsert_profile(loaded_profile.state)
    auth_store = PersistentAuthProfileStore(runtime_repository)

    provider_bundle = _resolve_provider_bundle(
        provider_profile=provider_profile,
        profile_dir=resolved_profile_dir,
    )
    if provider_bundle.provider_profile is not None:
        auth_store.register(provider_bundle.provider_profile)

    preview_model_provider = GatewayPreviewModelProvider()
    model_provider = GatewaySurfaceModelProvider(
        repository=runtime_repository,
        fallback=preview_model_provider,
        active_provider_profile=provider_bundle.provider_profile,
    )
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
        profile_id=loaded_profile.state.profile_id,
        workspace_id=workspace_id,
        provider_runtime=provider_bundle.provider_runtime,
        repository=runtime_repository,
        auth_store=auth_store,
        memory_runtime=memory_runtime,
        kernel=kernel,
        telemetry=telemetry,
        model_provider=model_provider,
        profile_dir=str(resolved_profile_dir) if resolved_profile_dir is not None else None,
        state_dir=str(resolved_state_dir) if resolved_state_dir is not None else None,
        loaded_profile=loaded_profile,
        provider_profile=provider_bundle.provider_profile,
    )
    return app, ChatBotMessagingAdapter(app=app), WebhookMessagingAdapter(app=app)


def _build_gateway_storage(state_dir: Path | None) -> GatewayStorageBundle:
    if state_dir is None:
        return GatewayStorageBundle(
            identity_store=InMemoryGatewayIdentityStore(),
            session_store=InMemoryGatewaySessionStore(),
        )
    return GatewayStorageBundle(
        identity_store=FileGatewayIdentityStore(state_dir / "gateway-identities.json"),
        session_store=FileGatewaySessionStore(state_dir / "gateway-sessions.json"),
    )


def _resolve_loaded_profile(*, profile_id: str, profile_dir: Path | None) -> LoadedProfile:
    if profile_dir is None:
        return _default_loaded_profile(profile_id)
    loader = ProfileLoader(profile_dir)
    if profile_id == "profile:default":
        return loader.load()
    return loader.load(profile_id=profile_id)


def _resolve_provider_bundle(
    *,
    provider_profile: Mapping[str, Any] | None,
    profile_dir: Path | None,
) -> GatewayProviderBundle:
    if provider_profile is not None:
        loaded_provider_profile = provider_profile_from_payload(provider_profile)
        return GatewayProviderBundle(
            provider_profile=loaded_provider_profile,
            provider_runtime=provider_profile_summary(loaded_provider_profile),
        )
    if profile_dir is None:
        return GatewayProviderBundle(
            provider_profile=None,
            provider_runtime=provider_fallback_summary(),
        )
    loaded_provider_profile = load_provider_profile(profile_dir)
    if loaded_provider_profile is None:
        return GatewayProviderBundle(
            provider_profile=None,
            provider_runtime=provider_fallback_summary(),
        )
    return GatewayProviderBundle(
        provider_profile=loaded_provider_profile,
        provider_runtime=provider_profile_summary(loaded_provider_profile),
    )
