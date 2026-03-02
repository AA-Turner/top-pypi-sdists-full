"""Base agent class and registry for Plato agents."""

from __future__ import annotations

import base64
import importlib.metadata
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar, get_args, get_origin

from pydantic import TypeAdapter

from plato.agents.config import AgentConfig
from plato.agents.schema import get_agent_schema
from plato.runtime import RuntimeConfig, VMRuntimeConfig

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
    default_runtime: ClassVar[VMRuntimeConfig | None] = None

    # Instance attributes
    config: ConfigT
    runtime: RuntimeConfig | None = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"plato.agents.{self.name}")
        self._load_runtime()

    def _load_runtime(self) -> None:
        """Load runtime config from AGENT_RUNTIME_B64 env var if available."""
        runtime_b64 = os.environ.get("AGENT_RUNTIME_B64")
        if runtime_b64:
            try:
                data = json.loads(base64.b64decode(runtime_b64).decode())
                adapter = TypeAdapter(RuntimeConfig)
                self.runtime = adapter.validate_python(data)
            except Exception as e:
                logger.warning(f"Failed to parse AGENT_RUNTIME_B64: {e}")

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

    @abstractmethod
    async def run(self, instruction: str, tools_path: str | None = None) -> None:
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
