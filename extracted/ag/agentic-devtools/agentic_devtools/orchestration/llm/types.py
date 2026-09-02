"""Core data types for the LLM provider abstraction."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any


class ProviderType(StrEnum):
    """Supported LLM provider backends."""

    AZURE_OPENAI = "azure_openai"
    OPENAI_DIRECT = "openai_direct"
    LOCAL_MODEL = "local_model"
    COPILOT = "copilot"


@dataclass(frozen=True)
class TokenUsage:
    """Per-call token and cost metadata."""

    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float | None = None


@dataclass(frozen=True)
class LLMResponse:
    """Standard completion result returned to orchestration nodes."""

    text: str
    model: str
    provider_type: ProviderType
    usage: TokenUsage | None = None
    served_from_fixture: bool = False
    latency_ms: int | None = None
    finish_reason: str | None = None


@dataclass(frozen=True)
class StreamChunk:
    """Structured streaming delta payload."""

    text_delta: str
    chunk_index: int | None = None
    finish_reason: str | None = None
    token_usage: TokenUsage | None = None
    model: str | None = None


@dataclass(frozen=True)
class LLMMessage:
    """Request message payload."""

    role: str  # "system", "user", "assistant", "tool"
    content: str
    name: str | None = None


@dataclass(frozen=True)
class ModelConfig:
    """Model-level configuration parameters."""

    model: str
    temperature: float | None = None
    max_tokens: int | None = None
    response_format: dict[str, Any] | None = None


@dataclass(frozen=True)
class ProviderConfig:
    """Provider-level immutable settings loaded at workflow initialization."""

    provider_id: str
    provider_type: ProviderType
    model: str
    endpoint: str | None = None
    api_version: str | None = None
    api_key_env: str | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    timeout_seconds: int | None = None


@dataclass(frozen=True)
class NodeConfig:
    """Resolved configuration for a specific workflow node."""

    provider_id: str
    provider_type: ProviderType
    model: str
    endpoint: str | None = None
    api_version: str | None = None
    api_key_env: str | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    timeout_seconds: int | None = None
    model_override: str | None = None
    params_override: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Copy params_override into an immutable mapping."""
        object.__setattr__(self, "params_override", MappingProxyType(dict(self.params_override)))

    @property
    def effective_model(self) -> str:
        """Return model_override if set, otherwise the base model."""
        return self.model_override if self.model_override else self.model

    @property
    def effective_temperature(self) -> float | None:
        """Return temperature from params_override or base config."""
        if "temperature" in self.params_override:
            return self.params_override["temperature"]
        return self.temperature

    @property
    def effective_max_tokens(self) -> int | None:
        """Return max_tokens from params_override or base config."""
        if "max_tokens" in self.params_override:
            return self.params_override["max_tokens"]
        return self.max_tokens
