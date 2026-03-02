"""Configuration models for Plato worlds."""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from plato._generated.models import (
    EnvFromArtifact,
    EnvFromResource,
    EnvFromSimulator,
)
from plato.markers import FieldMarker
from plato.runtime import (
    DockerRuntimeConfig,
    RuntimeConfig,
    VMResources,
    VMRuntimeConfig,
)
from plato.v2.async_.session import SerializedSession
from plato.worlds.schema import get_field_annotations, get_world_config_schema

# Union type for environment configurations
EnvConfig = EnvFromArtifact | EnvFromSimulator | EnvFromResource

# Re-export for backwards compatibility
__all__ = [
    "DevConfig",
    "DockerRuntimeConfig",
    "RuntimeConfig",
    "SessionConfig",
    "VMResources",
    "VMRuntimeConfig",
    "WorkspaceConfig",
    "WorkspaceMode",
]


class LLMConfig(BaseModel):
    """Configuration for an LLM used by a world.

    Attributes:
        model: Model identifier in litellm format (e.g. "anthropic/claude-sonnet-4-5-20250514")
        api_key: API key passed directly to litellm (works for any provider)
        max_tokens: Default max output tokens
        temperature: Default sampling temperature (None = provider default)
    """

    model: str
    api_key: str = ""
    max_tokens: int = 4096
    temperature: float | None = None


class DevConfig(BaseModel):
    """Dev mode configuration for code syncing.

    In dev mode, local code is synced to VMs for hot-reload development.

    Example:
        dev:
          world: ./worlds/my-world
          agents:
            skill_runner: ./agents/claude-code
          sync_sdk: true
    """

    world: Path | None = None
    agents: dict[str, Path] = Field(default_factory=dict)
    sync_sdk: bool = True
    ssh_key_path: Path | None = None


class SessionConfig(BaseModel):
    """Session and telemetry configuration.

    Contains session identifiers and endpoints for OTel tracing.
    The world VM uses chronos_url to request presigned URLs for
    state persistence from the Chronos API.

    For cross-world trace propagation, parent_trace_id and parent_span_id
    can be set so that this session's spans appear under the parent's trace.
    These are populated by Chronos when the parent session's trace context
    is available.
    """

    session_id: str = ""
    otel_url: str = ""
    chronos_url: str = ""  # Base URL for Chronos API (presigned URL requests)
    plato_session: SerializedSession | None = None
    parent_trace_id: str | None = None  # Parent trace ID (hex) for cross-world linking
    parent_span_id: str | None = None  # Parent span ID (hex) for cross-world linking


# =============================================================================
# Agent Configuration
# =============================================================================


class AgentConfig(BaseModel):
    """Configuration for an agent.

    Attributes:
        image: Docker image URI for the agent
        runtime: Runtime configuration (docker or vm with resources)
        config: Agent-specific configuration passed to the agent
    """

    image: str
    runtime: RuntimeConfig = Field(default_factory=VMRuntimeConfig)
    config: dict[str, Any] = Field(default_factory=dict)


# =============================================================================
# World Configuration
# =============================================================================


class StateConfig(BaseModel):
    """Configuration for world state persistence.

    State is persisted as a JSON file uploaded to S3 via Chronos presigned URLs.
    At each checkpoint, state is uploaded. On restore, state is downloaded from
    the specified resume session.

    Attributes:
        enabled: Whether to enable state persistence (default: True).
        path: Path to the local state directory (default: /state).
        resume: Whether to load saved state on startup (default: True).
        resume_session: Session ID to resume from. State will be downloaded
            from that session before the world starts.
    """

    enabled: bool = True
    path: str = "/state"
    resume: bool = True
    resume_session: str = ""
    resume_step: int | None = None


class WorkspaceMode(str, Enum):
    """How the workspace is shared with agent VMs."""

    rsync = "rsync"
    nfs = "nfs"


class WorkspaceConfig(BaseModel):
    """Configuration for the workspace shared across VMs in a session.

    Attributes:
        path: Path to the workspace directory on the world VM (default: /workspace).
        mode: How the workspace is shared with agent VMs.
              'rsync': rsync to/from agent VMs before/after each agent run.
              'nfs' (default): agent VMs mount workspace via NFSv4; writes are immediate.
    """

    path: str = "/workspace"
    mode: WorkspaceMode = WorkspaceMode.nfs


class CheckpointConfig(BaseModel):
    """Configuration for automatic checkpointing during world execution.

    Attributes:
        enabled: Whether to enable automatic checkpoints after steps (default: False).
        interval: Create checkpoint every N steps (default: 1 = every step).
        exclude_envs: Environment aliases to exclude from checkpoints (default: ["runtime"]).
    """

    enabled: bool = False
    interval: int = 1
    exclude_envs: list[str] = Field(default_factory=lambda: ["runtime"])


class RunConfig(BaseModel):
    """Base configuration for running a world.

    Subclass this with your world-specific fields, agents, secrets, and envs:

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

    Note: runtime, dev, session are passed separately to BaseWorld.run(), not as part of config.
    """

    # Checkpoint configuration for automatic snapshots after steps
    checkpoint: CheckpointConfig = Field(default_factory=CheckpointConfig)

    # State persistence configuration
    state: StateConfig = Field(default_factory=StateConfig)

    # Workspace configuration
    workspace: WorkspaceConfig = Field(default_factory=WorkspaceConfig)

    model_config = {"extra": "allow"}

    @classmethod
    def get_field_annotations(cls) -> dict[str, FieldMarker | None]:
        """Get FieldMarker annotations for each field."""
        return get_field_annotations(cls)

    @classmethod
    def get_json_schema(cls) -> dict:
        """Get JSON schema with agents, secrets, and envs separated."""
        return get_world_config_schema(cls)

    def get_envs(self) -> list[EnvConfig]:
        """Get all environment configurations from this config.

        Returns:
            List of EnvConfig objects (EnvFromArtifact, EnvFromSimulator, or EnvFromResource)
        """
        annotations = self.get_field_annotations()
        envs: list[EnvConfig] = []

        for field_name, marker in annotations.items():
            if marker is not None and marker.kind == "env":
                value = getattr(self, field_name, None)
                if value is not None:
                    envs.append(value)

        return envs

    @classmethod
    def from_file(cls, path: str | Path) -> RunConfig:
        """Load config from a JSON file.

        Reads from world.config if present (Chronos config structure).
        """
        path = Path(path)
        with open(path) as f:
            data = json.load(f)

        # Read from world.config if present
        if "world" in data and isinstance(data["world"], dict) and "config" in data["world"]:
            data = data["world"]["config"]

        return cls.model_validate(data)
