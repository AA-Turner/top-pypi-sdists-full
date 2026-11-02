"""LLM provider configuration dataclass for orchestration.

Provides ``LLMProviderConfig`` — a frozen dataclass that serves as the
user-facing YAML surface for LLM provider settings.  Includes conversion
methods to internal types (``ProviderConfig``, ``NodeConfig``, ``RetryConfig``)
and validation of retry-related fields.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentic_devtools.orchestration.llm.retry import RetryConfig
from agentic_devtools.orchestration.llm.types import NodeConfig, ProviderConfig, ProviderType


@dataclass(frozen=True)
class LLMProviderConfig:
    """User-facing LLM provider configuration loaded from YAML.

    Combines provider identification, model settings, and retry parameters
    into a single frozen dataclass.  Use the conversion methods to obtain
    internal types consumed by the orchestration infrastructure.

    Attributes:
        provider_id: Unique identifier for this provider configuration.
        provider_type: Backend type (azure_openai, openai_direct, local_model).
        model: Model identifier (e.g., "gpt-4o", "claude-3-opus").
        endpoint: Provider endpoint URL (required for Azure OpenAI).
        api_version: API version string (Azure OpenAI).
        api_key_env: Environment variable name containing the API key.
        max_tokens: Maximum tokens for completion responses.
        temperature: Sampling temperature.
        timeout_seconds: Per-request timeout in seconds.
        max_attempts: Total attempts (initial + retries). Default 4 (3 retries).
        base_delay_seconds: Initial retry delay.
        max_delay_seconds: Maximum retry delay cap.
        jitter_factor: Jitter multiplier for backoff randomisation.
        total_timeout_seconds: Overall timeout across all retry attempts.
    """

    provider_id: str
    provider_type: ProviderType
    model: str
    endpoint: str | None = None
    api_version: str | None = None
    api_key_env: str | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    timeout_seconds: int | None = None
    max_attempts: int = 4
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    jitter_factor: float = 0.5
    total_timeout_seconds: float = 120.0

    def __post_init__(self) -> None:
        """Validate retry-related field constraints."""
        if self.max_attempts < 1:
            raise ValueError(f"max_attempts must be >= 1, got {self.max_attempts}")
        if self.base_delay_seconds < 0:
            raise ValueError(f"base_delay_seconds must be >= 0, got {self.base_delay_seconds}")
        if self.max_delay_seconds < 0:
            raise ValueError(f"max_delay_seconds must be >= 0, got {self.max_delay_seconds}")
        if self.jitter_factor < 0:
            raise ValueError(f"jitter_factor must be >= 0, got {self.jitter_factor}")
        if self.total_timeout_seconds < 0:
            raise ValueError(f"total_timeout_seconds must be >= 0, got {self.total_timeout_seconds}")

    def to_provider_config(self) -> ProviderConfig:
        """Convert to internal ``ProviderConfig``."""
        return ProviderConfig(
            provider_id=self.provider_id,
            provider_type=self.provider_type,
            model=self.model,
            endpoint=self.endpoint,
            api_version=self.api_version,
            api_key_env=self.api_key_env,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout_seconds=self.timeout_seconds,
        )

    def to_node_config(self) -> NodeConfig:
        """Convert to internal ``NodeConfig``."""
        return NodeConfig(
            provider_id=self.provider_id,
            provider_type=self.provider_type,
            model=self.model,
            endpoint=self.endpoint,
            api_version=self.api_version,
            api_key_env=self.api_key_env,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout_seconds=self.timeout_seconds,
        )

    def to_retry_config(self) -> RetryConfig:
        """Convert retry fields to ``RetryConfig``."""
        return RetryConfig(
            max_attempts=self.max_attempts,
            base_delay_seconds=self.base_delay_seconds,
            max_delay_seconds=self.max_delay_seconds,
            jitter_factor=self.jitter_factor,
            total_timeout_seconds=self.total_timeout_seconds,
        )
