"""Named OpenAI-compatible provider presets with isolated credential lookup."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from ..errors import ProviderConfigurationError
from .base import HttpTransport, RequestPolicy
from .openai_compatible import OpenAICompatibleProvider


@dataclass(frozen=True, slots=True)
class _Preset:
    base_url: str
    base_url_env: tuple[str, ...]
    api_key_env: tuple[str, ...]
    requires_api_key: bool
    max_tokens_field: str = "max_tokens"


_PRESETS = {
    "llamacpp": _Preset(
        base_url="http://127.0.0.1:8080/v1",
        base_url_env=("LOCALARENA_LLAMACPP_BASE_URL",),
        api_key_env=("LOCALARENA_LLAMACPP_API_KEY",),
        requires_api_key=False,
    ),
    "ollama": _Preset(
        base_url="http://127.0.0.1:11434/v1",
        base_url_env=("LOCALARENA_OLLAMA_BASE_URL",),
        api_key_env=("LOCALARENA_OLLAMA_API_KEY",),
        requires_api_key=False,
    ),
    "lmstudio": _Preset(
        base_url="http://127.0.0.1:1234/v1",
        base_url_env=("LOCALARENA_LMSTUDIO_BASE_URL",),
        api_key_env=("LOCALARENA_LMSTUDIO_API_KEY",),
        requires_api_key=False,
    ),
    "openrouter": _Preset(
        base_url="https://openrouter.ai/api/v1",
        base_url_env=(
            "LOCALARENA_OPENROUTER_BASE_URL",
            "OPENROUTER_BASE_URL",
        ),
        api_key_env=(
            "LOCALARENA_OPENROUTER_API_KEY",
            "OPENROUTER_API_KEY",
        ),
        requires_api_key=True,
    ),
    "openai": _Preset(
        base_url="https://api.openai.com/v1",
        base_url_env=("LOCALARENA_OPENAI_BASE_URL", "OPENAI_BASE_URL"),
        api_key_env=("LOCALARENA_OPENAI_API_KEY", "OPENAI_API_KEY"),
        requires_api_key=True,
        max_tokens_field="max_completion_tokens",
    ),
}
_ALIASES = {
    "llama.cpp": "llamacpp",
    "llama-cpp": "llamacpp",
    "lm-studio": "lmstudio",
}


def create_provider(
    profile: str,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    headers: Mapping[str, str] | None = None,
    policy: RequestPolicy | None = None,
    transport: HttpTransport | None = None,
    env: Mapping[str, str] | None = None,
) -> OpenAICompatibleProvider:
    """Create one of five named profiles, or a generic ``custom`` provider.

    Explicit values win over environment values. Local and custom profiles
    never read cloud-provider API key variables.
    """

    if type(profile) is not str:
        raise TypeError("profile must be a string")
    normalized_profile = _ALIASES.get(profile.strip().lower(), profile.strip().lower())
    environment = os.environ if env is None else env
    if not isinstance(environment, Mapping):
        raise TypeError("env must be a mapping or None")

    if normalized_profile == "custom":
        if base_url is None:
            raise ProviderConfigurationError(
                "custom providers require an explicit base_url",
                provider="custom",
            )
        return OpenAICompatibleProvider(
            base_url=base_url,
            api_key=api_key,
            name="custom",
            headers=headers,
            policy=policy,
            transport=transport,
        )

    try:
        preset = _PRESETS[normalized_profile]
    except KeyError:
        choices = ", ".join([*_PRESETS, "custom"])
        raise ProviderConfigurationError(
            f"unknown provider profile; expected one of {choices}",
            provider=normalized_profile or "provider",
        ) from None

    resolved_base_url = (
        base_url
        if base_url is not None
        else _first_env(environment, preset.base_url_env)
    )
    if resolved_base_url is None:
        resolved_base_url = preset.base_url
    resolved_api_key = api_key
    if resolved_api_key is None:
        key_names = preset.api_key_env
        if (
            resolved_base_url.rstrip("/") != preset.base_url.rstrip("/")
            and preset.requires_api_key
        ):
            # A standard cloud key is never forwarded to a custom endpoint
            # merely because that provider's usual environment variable exists.
            key_names = tuple(
                name for name in key_names if name.startswith("LOCALARENA_")
            )
        resolved_api_key = _first_env(environment, key_names)
    if preset.requires_api_key and not resolved_api_key:
        variable = (
            preset.api_key_env[0]
            if resolved_base_url.rstrip("/") != preset.base_url.rstrip("/")
            else preset.api_key_env[-1]
        )
        raise ProviderConfigurationError(
            f"API key required; pass api_key or set {variable}",
            provider=normalized_profile,
        )

    return OpenAICompatibleProvider(
        base_url=resolved_base_url,
        api_key=resolved_api_key,
        name=normalized_profile,
        headers=headers,
        policy=policy,
        transport=transport,
        max_tokens_field=preset.max_tokens_field,
    )


def provider_names() -> tuple[str, ...]:
    """Return the stable named profiles accepted by :func:`create_provider`."""

    return (*_PRESETS, "custom")


def _first_env(
    environment: Mapping[str, str],
    names: tuple[str, ...],
) -> str | None:
    for name in names:
        value = environment.get(name)
        if value:
            return value
    return None
