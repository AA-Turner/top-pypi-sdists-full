"""Provider adapter factory helpers.

These helpers keep request-family specific adapter selection package-owned so
product surfaces can stay thin and declarative.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from packages.auth import AuthProfile
from packages.models.provider_runtime import ProviderRuntimeResolver
from packages.models.runtime import CredentialSource, ModelAdapter

from .anthropic import AnthropicMessagesModelAdapter
from .openai_compatible import OpenAICompatibleProviderAdapter, OpenAICompatibleProviderConfig


@dataclass(frozen=True, slots=True)
class PinnedCredentialSource(CredentialSource):
    provider_id: str
    values: Mapping[str, str]

    def resolve(self, provider_id: str) -> Mapping[str, str]:
        if provider_id != self.provider_id:
            raise LookupError(f"missing pinned credentials for provider: {provider_id}")
        return dict(self.values)


def build_model_adapter(
    profile: AuthProfile,
    *,
    runtime_resolver: ProviderRuntimeResolver,
    credentials: Mapping[str, str],
    adapter_id: str,
    stream_observer=None,
) -> ModelAdapter | None:
    resolution = runtime_resolver.resolve(
        profile.provider_id,
        model_id=profile.default_model or None,
        base_url=profile.base_url,
    )
    credential_source = PinnedCredentialSource(
        provider_id=profile.provider_id,
        values=credentials,
    )
    if resolution.request_family in {"chat_completions", "responses"}:
        return OpenAICompatibleProviderAdapter(
            config=OpenAICompatibleProviderConfig(
                provider_id=profile.provider_id,
                base_url=profile.base_url or "",
                model_id=profile.default_model or "",
                extra_headers=profile.extra_headers,
            ),
            runtime_resolver=runtime_resolver,
            credential_source=credential_source,
            adapter_id=adapter_id,
            stream_observer=stream_observer,
        )
    if resolution.request_family == "messages":
        return AnthropicMessagesModelAdapter(
            adapter_id=adapter_id,
            resolution=resolution,
            credential_source=credential_source,
            extra_headers=profile.extra_headers,
        )
    return None
