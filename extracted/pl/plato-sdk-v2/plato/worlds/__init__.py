"""Plato Worlds - typed world definitions for agent execution.

Usage:
    from plato.worlds import BaseWorld, RunConfig, Agent, Secret, Env, AgentConfig, EnvConfig, register_world
    from plato._generated.models import EnvFromArtifact, EnvFromSimulator
    from typing import Annotated

    class CodeWorldConfig(RunConfig):
        # World-specific fields
        repository_url: str
        prompt: str

        # Agents (typed)
        coder: Annotated[AgentConfig, Agent(description="Coding agent")]

        # Secrets (typed)
        git_token: Annotated[str | None, Secret(description="GitHub token")] = None

        # Environments (typed)
        gitea: Annotated[EnvConfig, Env(description="Git server")] = EnvFromArtifact(
            artifact_id="abc123",
            alias="gitea",
        )

    @register_world("code")
    class CodeWorld(BaseWorld[CodeWorldConfig]):
        name = "code"
        description = "Run coding agents"

        async def reset(self) -> Observation:
            # Fully typed access
            url = self.config.repository_url
            agent = self.config.coder
            token = self.config.git_token
            gitea = self.config.gitea  # EnvConfig

        async def step(self) -> StepResult:
            ...
"""

from plato._generated.models import (
    EnvFromArtifact,
    EnvFromResource,
    EnvFromSimulator,
)
from plato.markers import Agent, Env, EnvList
from plato.markers import WorldSecret as Secret
from plato.worlds.base import (
    BaseWorld,
    ConfigT,
    StateT,
    get_registered_worlds,
    get_world,
    register_world,
)
from plato.worlds.config import (
    AgentConfig,
    CheckpointConfig,
    DevConfig,
    EnvConfig,
    LLMConfig,
    RunConfig,
    SessionConfig,
    StateConfig,
)
from plato.worlds.models import Observation, StepResult
from plato.worlds.result_store import ResultStore
from plato.worlds.runner import run_world

__all__ = [
    # Base
    "BaseWorld",
    "ConfigT",
    "StateT",
    "Observation",
    "StepResult",
    "register_world",
    "get_registered_worlds",
    "get_world",
    # Config
    "RunConfig",
    "LLMConfig",
    "CheckpointConfig",
    "DevConfig",
    "SessionConfig",
    "StateConfig",
    "AgentConfig",
    "Agent",
    "Secret",
    "Env",
    "EnvList",
    "EnvConfig",
    # Env types (re-exported from generated models)
    "EnvFromArtifact",
    "EnvFromSimulator",
    "EnvFromResource",
    # Result store
    "ResultStore",
    # Runner
    "run_world",
]
