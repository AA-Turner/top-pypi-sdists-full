"""First-party OpenAI provider adapter.

This module keeps OpenAI-specific behavior behind the provider boundary while
reusing the shared runtime resolver and auth profile baseline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping

from packages.auth.runtime import (
    AuthProfile,
    ProviderProfileInput,
    SecretReference,
    profile_from_input,
)
from packages.models.provider_runtime import (
    ProviderCatalogRecord,
    ProviderManifest,
    ProviderRuntimeResolution,
    ProviderRuntimeResolver,
    ProviderSetupGuide,
)


OPENAI_PROVIDER_ID = "openai"
OPENAI_TRANSPORT_ID = "openai_responses"
OPENAI_DEFAULT_MODEL_ID = "gpt-4.1-mini"
OPENAI_DEFAULT_BASE_URL = "https://api.openai.com/v1"


@dataclass(frozen=True, slots=True)
class OpenAIProviderConfig:
    profile_id: str
    model_id: str | None = None
    base_url: str | None = None
    secret_references: tuple[SecretReference, ...] = ()
    priority: int = 0
    session_pin: str | None = None
    cooldown_until: datetime | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


class OpenAIProviderAdapter:
    """First-party OpenAI provider adapter built on the shared runtime."""

    def __init__(self, resolver: ProviderRuntimeResolver | None = None) -> None:
        self.resolver = resolver or ProviderRuntimeResolver.default()

    @property
    def manifest(self) -> ProviderManifest:
        manifest = self.resolver.manifest_registry.get(OPENAI_PROVIDER_ID)
        if manifest is None:
            raise LookupError("missing OpenAI provider manifest")
        return manifest

    def catalog_record(self) -> ProviderCatalogRecord:
        for record in self.resolver.list_catalog():
            if record.provider_id == OPENAI_PROVIDER_ID:
                return record
        raise LookupError("missing OpenAI provider catalog record")

    def setup_guide(self) -> ProviderSetupGuide:
        return self.resolver.build_setup_guide(OPENAI_PROVIDER_ID)

    def runtime_resolution(
        self,
        *,
        model_id: str | None = None,
        base_url: str | None = None,
    ) -> ProviderRuntimeResolution:
        return self.resolver.resolve(
            OPENAI_PROVIDER_ID,
            model_id=model_id,
            base_url=base_url,
        )

    def build_profile(self, config: OpenAIProviderConfig) -> AuthProfile:
        profile_input = ProviderProfileInput(
            profile_id=config.profile_id,
            provider_id=OPENAI_PROVIDER_ID,
            secret_references=config.secret_references,
            priority=config.priority,
            session_pin=config.session_pin,
            cooldown_until=config.cooldown_until,
            metadata=dict(config.metadata),
        )
        return profile_from_input(
            profile_input,
            base_url=config.base_url or OPENAI_DEFAULT_BASE_URL,
            default_model=config.model_id or OPENAI_DEFAULT_MODEL_ID,
            transport_id=OPENAI_TRANSPORT_ID,
            auth_method="api_key",
            provider_kind="first_party",
            extra_headers={},
        )

    def profile_defaults(
        self,
        *,
        profile_id: str,
        secret_references: tuple[SecretReference, ...] = (),
        priority: int = 0,
        session_pin: str | None = None,
        cooldown_until: datetime | None = None,
        metadata: Mapping[str, str] | None = None,
        base_url: str | None = None,
        model_id: str | None = None,
    ) -> AuthProfile:
        return self.build_profile(
            OpenAIProviderConfig(
                profile_id=profile_id,
                model_id=model_id,
                base_url=base_url,
                secret_references=secret_references,
                priority=priority,
                session_pin=session_pin,
                cooldown_until=cooldown_until,
                metadata=dict(metadata or {}),
            )
        )

    def metadata(self) -> dict[str, object]:
        manifest = self.manifest
        resolution = self.runtime_resolution()
        guide = self.setup_guide()
        return {
            "provider_id": manifest.provider_id,
            "display_name": manifest.display_name,
            "transport_id": resolution.transport_id,
            "request_family": resolution.request_family,
            "model_id": resolution.model_id,
            "base_url": resolution.base_url,
            "capability_flags": resolution.capability_flags,
            "required_secret_keys": manifest.required_secret_keys,
            "required_config_keys": manifest.setup_fields(),
            "setup_hint": guide.onboarding_hint,
            "quickstart_steps": guide.quickstart_steps,
            "verification_steps": guide.verification_steps,
        }
