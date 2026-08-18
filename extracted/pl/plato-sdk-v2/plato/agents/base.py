"""Base agent class and registry for Plato agents."""

from __future__ import annotations

import importlib.metadata
import logging
import os
import shlex
from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError
from typing import ClassVar, Generic, TypeVar, get_args, get_origin

from pydantic import TypeAdapter

from plato.agents.browser_tooling import (
    AGENT_BROWSER_INSTRUCTIONS,
    AGENT_BROWSER_PATH_EXPORT,
)
from plato.agents.computer_use_mcp import (
    COMPUTER_USE_MCP_INSTRUCTIONS,
    ComputerUseMcp,
)
from plato.agents.config import AgentConfig
from plato.agents.schema import get_agent_schema
from plato.runtimes.config import RuntimeConfig
from plato.utils.encoding import decode_b64_json

logger = logging.getLogger(__name__)

# Global registry of agents
_AGENT_REGISTRY: dict[str, type[BaseAgent]] = {}

# Type variable for config
ConfigT = TypeVar("ConfigT", bound=AgentConfig)


def register_agent(name: str | None = None):
    """Decorator to register an agent class.

    Usage:
        @register_agent("openhands")
        class OpenHandsAgent(BaseAgent[OpenHandsConfig]):
            ...
    """

    def decorator(cls: type[BaseAgent]) -> type[BaseAgent]:
        agent_name = name or getattr(cls, "name", cls.__name__.lower().replace("agent", ""))
        _AGENT_REGISTRY[agent_name] = cls
        logger.debug(f"Registered agent: {agent_name} -> {cls.__name__}")
        return cls

    return decorator


def get_registered_agents() -> dict[str, type[BaseAgent]]:
    """Get all registered agents."""
    return _AGENT_REGISTRY.copy()


def get_agent(name: str) -> type[BaseAgent] | None:
    """Get an agent by name."""
    return _AGENT_REGISTRY.get(name)


class BaseAgent(ABC, Generic[ConfigT]):
    """Base class for Plato agents.

    Subclass with a config type parameter for fully typed config access:

        class OpenHandsConfig(AgentConfig):
            model_name: str = "anthropic/claude-sonnet-4"
            anthropic_api_key: Annotated[str | None, Secret(description="API key")] = None

        @register_agent("openhands")
        class OpenHandsAgent(BaseAgent[OpenHandsConfig]):
            name = "openhands"
            description = "OpenHands AI software engineer"

            async def run(self, instruction: str) -> None:
                # self.config is typed as OpenHandsConfig
                model = self.config.model_name
                ...
    """

    # Class attributes
    name: ClassVar[str] = "base"
    description: ClassVar[str] = ""
    default_runtime: ClassVar[RuntimeConfig | None] = None

    # Instance attributes
    config: ConfigT
    runtime: RuntimeConfig | None = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"plato.agents.{self.name}")
        self._load_runtime()

    def _load_runtime(self) -> None:
        """Load runtime config from AGENT_RUNTIME_B64 env var if available."""
        runtime_b64 = os.environ.get("AGENT_RUNTIME_B64")
        if not runtime_b64:
            raise RuntimeError("agent needs to be loaded with runtime")

        try:
            data = decode_b64_json(runtime_b64)
            self.runtime = TypeAdapter(RuntimeConfig).validate_python(data)
        except JSONDecodeError:
            raise RuntimeError("agent needs to be loaded with runtime")

    @classmethod
    def get_config_class(cls) -> type[AgentConfig]:
        """Get the config class from the generic parameter."""
        for base in getattr(cls, "__orig_bases__", []):
            origin = get_origin(base)
            if origin is BaseAgent:
                args = get_args(base)
                if args and isinstance(args[0], type) and issubclass(args[0], AgentConfig):
                    return args[0]
        return AgentConfig

    @classmethod
    def get_version(cls) -> str:
        """Get version from package metadata."""
        for pkg_name in [cls.__module__.split(".")[0], f"plato-agent-{cls.name}"]:
            try:
                return importlib.metadata.version(pkg_name)
            except importlib.metadata.PackageNotFoundError:
                continue
        return "0.0.0"

    @classmethod
    def get_schema(cls) -> dict:
        """Get full schema for the agent including config and build schemas."""
        return get_agent_schema(cls)

    _NVM_SOURCE = '. "${NVM_DIR:-/root/.nvm}/nvm.sh"'
    """Shell fragment that sources nvm. Agents run as root so nvm installs at
    ``/root/.nvm``; ``$NVM_DIR`` is set by nvm's install.sh to the same path
    and we prefer it when set in case a future base image moves it."""

    def _shell_env_prefix(self) -> str:
        """Return the shell prefix that sets up the agent subprocess PATH.

        Always sources nvm so node-based CLIs (claude, gemini, codex) resolve.
        When ``config.browser_tooling`` is set, also prepends ``$HOME/.bun/bin``
        so the ``agent-browser`` CLI (bun-installed) is on PATH.
        """
        prefix = self._NVM_SOURCE
        if self.config.browser_tooling:
            prefix = f"{prefix}; {AGENT_BROWSER_PATH_EXPORT}"
        return prefix

    def _append_browser_tooling_prompt(self, prompt: str | None) -> str | None:
        """Append the ``agent-browser`` block to a system prompt when opted in.

        Returns ``prompt`` unchanged when ``config.browser_tooling`` is False.
        When True, appends the shared command-reference block so the model
        knows which CLI calls are available.
        """
        if not self.config.browser_tooling:
            return prompt
        if not prompt:
            return AGENT_BROWSER_INSTRUCTIONS
        return f"{prompt}\n\n{AGENT_BROWSER_INSTRUCTIONS}"

    def _append_computer_use_mcp_prompt(self, prompt: str | None) -> str | None:
        """Append the computer-use MCP block to a system prompt when opted in.

        Returns ``prompt`` unchanged when ``config.computer_use_mcp_enabled``
        is False. When True, appends the shared block so the model knows the
        ``computer`` MCP server drives a separate remote Ubuntu desktop VM.
        """
        if not self.config.computer_use_mcp_enabled:
            return prompt
        if not prompt:
            return COMPUTER_USE_MCP_INSTRUCTIONS
        return f"{prompt}\n\n{COMPUTER_USE_MCP_INSTRUCTIONS}"

    async def _start_computer_use_mcp(self):
        """Boot the local computer-use MCP server when opted in.

        Returns a started ``ComputerUseMcp`` handle (close it in the agent's
        teardown path), or None when ``computer_use_mcp_enabled`` is off.
        """
        handle = ComputerUseMcp.from_config(self.config, logger=self.logger)
        if handle is not None:
            await handle.start()
        return handle

    @classmethod
    def reset_commands(cls, workspace_paths: list[str]) -> list[str]:
        """Return shell commands to reset VM state before the next pooled task."""
        commands = [
            # -x matches exact process name only, not the full command line,
            # so it cannot accidentally kill the shell running the reset commands.
            "pkill -x plato-agent-runner 2>/dev/null; true",
            "rm -rf /tmp/plato-* /var/tmp/* 2>/dev/null; true",
            ": > /etc/environment",
            # Remove stale /etc/hosts entries so _prepare_env_setup writes fresh values.
            "sed -i '/runtime\\.plato\\.internal/d' /etc/hosts 2>/dev/null; true",
        ]
        for workspace_path in workspace_paths:
            p = shlex.quote(workspace_path)
            commands.append(f"umount -l {p} 2>/dev/null; rm -rf {p} 2>/dev/null; mkdir -p {p}")
        return commands

    @abstractmethod
    async def run(self, instruction: str) -> None:
        """Run the agent with the given instruction.

        This is the main entry point for agent execution. Implementations should:
        1. Set up the environment using self.config
        2. Execute the agent's core logic

        Args:
            instruction: The task instruction/prompt for the agent.

        Raises:
            RuntimeError: If agent execution fails.
        """
        pass

    async def compact(self, instruction: str) -> None:
        """Compact the agent's live session (first-class compaction op).

        Invoked (instead of :meth:`run`) when the world requests a mid-session
        compaction — e.g. ``AgentTask`` between continuation/review cycles. The
        default delegates to :meth:`run`, which is correct for CLIs that honor a
        ``/compact <focus>`` instruction natively (e.g. Claude Code). Agents
        whose compaction is NOT message-driven (e.g. opencode, which compacts
        via a server endpoint) override this to trigger it directly.

        Args:
            instruction: The compaction request/focus. For the default
                (run-based) path this is the literal ``/compact …`` message;
                native overrides may use it as a focus hint or ignore it.
        """
        await self.run(instruction)
