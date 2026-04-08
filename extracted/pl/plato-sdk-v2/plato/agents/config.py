"""Typed configuration for Plato agents.

Provides base configuration classes that agents extend with their specific fields.
Secret fields are automatically loaded from environment variables using pydantic-settings.

Example:
    from plato.agents import AgentConfig, Secret
    from typing import Annotated

    class OpenHandsConfig(AgentConfig):
        model_name: str = "anthropic/claude-sonnet-4"
        anthropic_api_key: Annotated[str | None, Secret(description="API key")] = None

    # Secrets auto-loaded from env vars (ANTHROPIC_API_KEY -> anthropic_api_key)
    config = OpenHandsConfig.from_file("/config.json")
"""

from __future__ import annotations

import os
from typing import Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from plato.agents.schema import get_agent_config_schema, get_field_secrets
from plato.markers import Secret


class AgentConfig(BaseSettings):
    """Base configuration for agents.

    Extends pydantic-settings BaseSettings, so secret fields are automatically loaded
    from environment variables. The env var name is the uppercase field name.

    Subclass with agent-specific fields:

        class OpenHandsConfig(AgentConfig):
            model_name: str = "anthropic/claude-sonnet-4"
            anthropic_api_key: Annotated[str | None, Secret(description="API key")] = None

        # ANTHROPIC_API_KEY env var is automatically loaded into anthropic_api_key
        config = OpenHandsConfig.from_file("/config.json")

    Attributes:
        runtime: Execution environment. Agents run in Firecracker VMs.
    """

    model_config = SettingsConfigDict(
        env_prefix="",  # No prefix - ANTHROPIC_API_KEY maps to anthropic_api_key
        extra="allow",
        env_ignore_empty=True,
    )

    runtime: Literal["vm", "apple"] = "vm"

    @classmethod
    def get_field_secrets(cls) -> dict[str, Secret]:
        """Get Secret annotations for each field."""
        return get_field_secrets(cls)

    @classmethod
    def get_json_schema(cls) -> dict:
        """Get JSON schema with secrets separated."""
        return get_agent_config_schema(cls)

    def get_secrets_dict(self) -> dict[str, str]:
        """Extract secret values as a dict for environment variables."""
        secrets_map = self.get_field_secrets()
        result: dict[str, str] = {}

        for field_name in secrets_map:
            value = getattr(self, field_name, None)
            if value is not None:
                result[field_name] = value

        return result

    def get_config_dict(self) -> dict[str, Any]:
        """Extract non-secret config values as a dict."""
        secrets_map = self.get_field_secrets()

        result: dict[str, Any] = {}
        for field_name in self.__class__.model_fields:
            if field_name not in secrets_map:
                value = getattr(self, field_name, None)
                if value is not None:
                    result[field_name] = value

        return result

    @classmethod
    def from_env(cls) -> AgentConfig:
        """Load config from AGENT_CONFIG_B64 environment variable.

        The runner passes config as base64-encoded JSON in the
        AGENT_CONFIG_B64 environment variable.
        """
        config_b64 = os.environ.get("AGENT_CONFIG_B64")
        if not config_b64:
            raise ValueError("AGENT_CONFIG_B64 environment variable not set")
        from plato.utils.encoding import decode_b64_json

        data = decode_b64_json(config_b64)
        return cls(**data)
