"""Sandbox Proxy integrations, as the Koyeb driver persists them and the bootstrap API takes them.

Authors write `GitHubBinding`, `MistralApiBinding` and `WorkspaceHeaderBindings`; these models are their
translation, so a definition persisted by an earlier worker keeps validating.
"""

from collections.abc import Sequence
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..authoring.sandbox_policy import (
    GitHubBinding,
    MistralApiBinding,
    SandboxHeaderBinding,
    WorkspaceHeaderBindings,
)
from .proxy_lifecycle import SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS


class GitHubProxyConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["github"] = "github"
    repo_whitelist: tuple[str, ...] = ()
    all_accessible_repos: bool = False
    ttl_seconds: int = Field(default=3600, gt=SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS)
    host: str = "github.com"

    @field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        normalized = value.strip()
        if normalized != "github.com":
            raise ValueError(f"Sandbox Proxy currently supports only github.com; got {value!r}")
        return normalized


class MistralApiProxyConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["mistral-api"] = "mistral-api"
    ttl_seconds: int = Field(default=3600, gt=SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS)


class SecretInjectionProxyConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["secret-injection"] = "secret-injection"


type SandboxProxyIntegration = Annotated[
    GitHubProxyConfig | MistralApiProxyConfig | SecretInjectionProxyConfig,
    Field(discriminator="type"),
]


def proxy_integrations(header_bindings: Sequence[SandboxHeaderBinding]) -> tuple[SandboxProxyIntegration, ...]:
    """Translate the header bindings Sandbox Proxy serves into its integrations."""

    integrations: list[SandboxProxyIntegration] = []
    for injection in header_bindings:
        if isinstance(injection, GitHubBinding):
            integrations.append(
                GitHubProxyConfig(
                    repo_whitelist=() if injection.repos == "all" else injection.repos,
                    all_accessible_repos=injection.repos == "all",
                    ttl_seconds=injection.ttl_seconds,
                    host=injection.host,
                )
            )
        elif isinstance(injection, MistralApiBinding):
            integrations.append(MistralApiProxyConfig(ttl_seconds=injection.ttl_seconds))
        elif isinstance(injection, WorkspaceHeaderBindings):
            integrations.append(SecretInjectionProxyConfig())
        else:
            raise TypeError(f"Sandbox Proxy does not serve {type(injection).__name__}")
    return tuple(integrations)


__all__ = [
    "GitHubProxyConfig",
    "MistralApiProxyConfig",
    "SandboxProxyIntegration",
    "SecretInjectionProxyConfig",
    "proxy_integrations",
]
