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
from typing import Annotated, Any, Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from plato.agents.schema import get_agent_config_schema, get_field_secrets
from plato.markers import Secret
from plato.tools.mcp import EnvMcpUrl


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
    browser_tooling: bool = False
    """Opt-in flag: when True, the agent runtime injects the ``agent-browser``
    CLI command reference into its system prompt and prepends ``$HOME/.bun/bin``
    to its shell PATH. Defaults ``False`` so no behavior change for agents that
    don't want browser tooling — worlds must explicitly set this on the agent
    config when they want the model to use ``agent-browser``."""

    computer_use_mcp_enabled: bool = False
    """Opt-in flag: when True, the agent runtime starts a local MCP server
    exposing computer-use tools (screenshot, click, type_text, key, scroll,
    drag, bash, ...) that drive a REMOTE ubuntu-vm desktop, attaches it to the
    agent's MCP config, and injects a short system-prompt block describing it.
    Requires ``computer_use_vm_url``. The tools never target the agent VM
    itself — MCP computer use is remote-desktop only."""

    computer_use_vm_url: str | EnvMcpUrl | None = None
    """Remote ubuntu-vm desktop the computer-use MCP tools drive. Either the
    literal desktop_agent HTTP base URL (the ``{job_id}--9000.connect.plato.so``
    connect-gateway form), or an ``{env: <alias>}`` reference the world resolves
    to the booted sim's desktop URL at launch (same pattern as ``mcp_servers``
    env aliases). Worlds that boot an ubuntu-vm env (e.g. cua-benchmark) also
    inject it automatically when unset. Required when
    ``computer_use_mcp_enabled`` is True; an alias that no world resolves fails
    loudly at agent startup."""

    computer_use_ssh_host: str | None = None
    """Mesh address of the remote desktop VM for the ``computer`` server's
    ``bash`` / ``read_file`` / ``write_file`` / ``edit_file`` tools. When set
    (with ``computer_use_ssh_key``), those tools run over one persistent ssh
    session on the session mesh instead of the desktop agent's HTTP API; the
    screen tools keep using ``computer_use_vm_url``. Worlds fill it from the
    env's ``get_mesh_ip()``."""

    computer_use_ssh_key: Annotated[str | None, Secret(description="Private key authorized on the desktop VM")] = None
    """Private key for ``computer_use_ssh_host`` — a per-run key the world
    generates and authorizes on the desktop VM only (never the world's own
    runner key, which also opens the world VM)."""

    computer_use_ssh_user: str = "root"

    sandbox_tools_only: bool = False
    """Opt-in flag: when True, the harness's own shell and file tools are
    removed from the model, so every command and file operation goes through
    the ``computer`` MCP server and runs on the remote ubuntu-vm sandbox. The
    agent VM (which holds the run's credentials) is then unreachable from the
    model's tools. Turns on ``computer_use_mcp_enabled`` by itself (an explicit
    ``false`` alongside it is rejected); the world still supplies
    ``computer_use_vm_url``. Benchmarks set this for the task agent; validators
    that write reports to a mounted workspace on their own VM leave it off."""

    sandbox_extra_builtin_tools: list[str] = []
    """Harness built-ins to keep alongside the sandbox tools under
    ``sandbox_tools_only``. The allow-list is empty of work tools by design - a
    built-in acts on the agent VM, where the run's credentials live - but a tool
    that touches neither that filesystem nor its shell cannot leak them, so
    web search and fetch, a todo list and the like are safe to name here. Names
    are the harness's own (e.g. ``WebSearch``); an unknown one is ignored rather
    than opening anything.

    Claude Code only. Codex reaches the sandbox through an exec-server
    environment with ``include_local = false``, so it has no local built-in set
    to widen and this field does nothing there."""

    @model_validator(mode="after")
    def _sandbox_tools_only_enables_computer_use(self) -> AgentConfig:
        """The ``computer`` server is all a sandbox_tools_only agent has, so the flag turns it on."""
        if self.sandbox_tools_only:
            if "computer_use_mcp_enabled" in self.model_fields_set and not self.computer_use_mcp_enabled:
                raise ValueError(
                    "sandbox_tools_only requires the computer server; remove computer_use_mcp_enabled: false "
                    "(the flag turns the server on by itself)"
                )
            self.computer_use_mcp_enabled = True
        return self

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
