"""Tests for LLMProviderConfig frozen dataclass."""

from __future__ import annotations

from typing import Any

import pytest

from agentic_devtools.orchestration.llm.provider_config import LLMProviderConfig
from agentic_devtools.orchestration.llm.retry import RetryConfig
from agentic_devtools.orchestration.llm.types import NodeConfig, ProviderConfig, ProviderType


class TestLLMProviderConfig:
    """Tests for LLMProviderConfig construction and conversion."""

    def _make_config(self, **overrides: Any) -> LLMProviderConfig:
        """Helper to create a config with sensible defaults."""
        defaults: dict[str, Any] = {
            "provider_id": "test-provider",
            "provider_type": ProviderType.AZURE_OPENAI,
            "model": "gpt-4o",
            "endpoint": "https://example.openai.azure.com",
            "api_version": "2024-02-15-preview",
            "api_key_env": "AZURE_OPENAI_KEY",
            "max_tokens": 4096,
            "temperature": 0.1,
            "timeout_seconds": 30,
        }
        defaults.update(overrides)
        return LLMProviderConfig(**defaults)  # type: ignore[arg-type]

    def test_construction_happy_path(self) -> None:
        """Config created with valid fields stores all values correctly."""
        config = self._make_config()
        assert config.provider_id == "test-provider"
        assert config.provider_type == ProviderType.AZURE_OPENAI
        assert config.model == "gpt-4o"
        assert config.endpoint == "https://example.openai.azure.com"
        assert config.api_version == "2024-02-15-preview"
        assert config.api_key_env == "AZURE_OPENAI_KEY"
        assert config.max_tokens == 4096
        assert config.temperature == 0.1
        assert config.timeout_seconds == 30

    def test_default_retry_values(self) -> None:
        """Default retry fields match expected values (4 attempts = 3 retries)."""
        config = self._make_config()
        assert config.max_attempts == 4
        assert config.base_delay_seconds == 1.0
        assert config.max_delay_seconds == 60.0
        assert config.jitter_factor == 0.5
        assert config.total_timeout_seconds == 120.0

    def test_frozen_immutability(self) -> None:
        """Config is frozen — attribute assignment raises."""
        config = self._make_config()
        with pytest.raises(AttributeError):
            config.model = "other-model"  # type: ignore[misc]

    def test_to_provider_config(self) -> None:
        """to_provider_config() returns a ProviderConfig with matching fields."""
        config = self._make_config()
        pc = config.to_provider_config()
        assert isinstance(pc, ProviderConfig)
        assert pc.provider_id == "test-provider"
        assert pc.provider_type == ProviderType.AZURE_OPENAI
        assert pc.model == "gpt-4o"
        assert pc.endpoint == "https://example.openai.azure.com"
        assert pc.api_version == "2024-02-15-preview"
        assert pc.api_key_env == "AZURE_OPENAI_KEY"
        assert pc.max_tokens == 4096
        assert pc.temperature == 0.1
        assert pc.timeout_seconds == 30

    def test_to_node_config(self) -> None:
        """to_node_config() returns a NodeConfig with matching fields."""
        config = self._make_config()
        nc = config.to_node_config()
        assert isinstance(nc, NodeConfig)
        assert nc.provider_id == "test-provider"
        assert nc.model == "gpt-4o"

    def test_to_retry_config(self) -> None:
        """to_retry_config() returns a RetryConfig with matching fields."""
        config = self._make_config(
            max_attempts=3,
            base_delay_seconds=2.0,
            max_delay_seconds=30.0,
            jitter_factor=0.3,
            total_timeout_seconds=60.0,
        )
        rc = config.to_retry_config()
        assert isinstance(rc, RetryConfig)
        assert rc.max_attempts == 3
        assert rc.base_delay_seconds == 2.0
        assert rc.max_delay_seconds == 30.0
        assert rc.jitter_factor == 0.3
        assert rc.total_timeout_seconds == 60.0

    def test_validation_max_attempts_too_low(self) -> None:
        """max_attempts < 1 raises ValueError."""
        with pytest.raises(ValueError, match="max_attempts must be >= 1"):
            self._make_config(max_attempts=0)

    def test_validation_base_delay_negative(self) -> None:
        """Negative base_delay_seconds raises ValueError."""
        with pytest.raises(ValueError, match="base_delay_seconds must be >= 0"):
            self._make_config(base_delay_seconds=-1.0)

    def test_validation_max_delay_negative(self) -> None:
        """Negative max_delay_seconds raises ValueError."""
        with pytest.raises(ValueError, match="max_delay_seconds must be >= 0"):
            self._make_config(max_delay_seconds=-1.0)

    def test_validation_jitter_negative(self) -> None:
        """Negative jitter_factor raises ValueError."""
        with pytest.raises(ValueError, match="jitter_factor must be >= 0"):
            self._make_config(jitter_factor=-0.1)

    def test_validation_total_timeout_negative(self) -> None:
        """Negative total_timeout_seconds raises ValueError."""
        with pytest.raises(ValueError, match="total_timeout_seconds must be >= 0"):
            self._make_config(total_timeout_seconds=-1.0)

    def test_optional_fields_none(self) -> None:
        """Optional fields default to None when not provided."""
        config = LLMProviderConfig(
            provider_id="minimal",
            provider_type=ProviderType.OPENAI_DIRECT,
            model="gpt-4o-mini",
        )
        assert config.endpoint is None
        assert config.api_version is None
        assert config.api_key_env is None
        assert config.max_tokens is None
        assert config.temperature is None
        assert config.timeout_seconds is None
