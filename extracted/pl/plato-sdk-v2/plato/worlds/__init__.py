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

from plato.markers import Agent, Env, EnvList
from plato.markers import WorkspaceMarker as Workspace
from plato.markers import WorldSecret as Secret
from plato.worlds.base import (
    BaseWorld,
    ConfigT,
    StateT,
    get_registered_worlds,
    get_world,
    register_world,
)
from plato.worlds.checkpoint import checkpoint
from plato.worlds.config import (
    AgentConfig,
    CheckpointConfig,
    ChronosConfig,
    DevConfig,
    EnvConfig,
    LLMConfig,
    RunConfig,
    StateConfig,
)
from plato.worlds.durable import (
    DependencyMissing,
    DurableOutputs,
    DurablePath,
    FromArg,
    Requires,
    durable,
    load_durable,
    load_durable_path,
)
from plato.worlds.launcher import (
    WorldLauncher,
    WorldLaunchMode,
    WorldLaunchResult,
)
from plato.worlds.models import Observation, StepResult
from plato.worlds.result_store import ResultStore
from plato.worlds.review.result import ReviewFinding, ReviewResult, ReviewSignal, SessionData
from plato.worlds.review.spec import ReviewSpec
from plato.worlds.review.world import BaseReviewWorld, ReviewWorldConfig
from plato.worlds.runner import run_world
from plato.worlds.session_review_models import (
    DEFAULT_REVIEW_MODELS,
    SessionReviewIssue,
    SessionReviewSummary,
)
from plato.worlds.slack import disable_slack_notifications, enable_slack_notifications
from plato.worlds.stage_tracking import disable_stage_tracking, enable_stage_tracking


def __getattr__(name: str):
    if name in ("EnvFromArtifact", "EnvFromResource", "EnvFromSimulator"):
        from plato._generated.models import EnvFromArtifact, EnvFromResource, EnvFromSimulator

        _lazy = {
            "EnvFromArtifact": EnvFromArtifact,
            "EnvFromResource": EnvFromResource,
            "EnvFromSimulator": EnvFromSimulator,
        }
        globals().update(_lazy)
        return _lazy[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BaseWorld",
    "ConfigT",
    "StateT",
    "Observation",
    "StepResult",
    "register_world",
    "get_registered_worlds",
    "get_world",
    "RunConfig",
    "LLMConfig",
    "CheckpointConfig",
    "DevConfig",
    "ChronosConfig",
    "StateConfig",
    "AgentConfig",
    "Agent",
    "Secret",
    "Env",
    "EnvList",
    "Workspace",
    "EnvConfig",
    "EnvFromArtifact",
    "EnvFromSimulator",
    "EnvFromResource",
    "checkpoint",
    "durable",
    "Requires",
    "DependencyMissing",
    "DurablePath",
    "DurableOutputs",
    "FromArg",
    "load_durable",
    "load_durable_path",
    "enable_stage_tracking",
    "disable_stage_tracking",
    "enable_slack_notifications",
    "disable_slack_notifications",
    "ResultStore",
    "ReviewSpec",
    "BaseReviewWorld",
    "ReviewWorldConfig",
    "ReviewSignal",
    "ReviewFinding",
    "ReviewResult",
    "SessionData",
    "run_world",
    "WorldLauncher",
    "WorldLaunchMode",
    "WorldLaunchResult",
    "DEFAULT_REVIEW_MODELS",
    "SessionReviewIssue",
    "SessionReviewSummary",
]
