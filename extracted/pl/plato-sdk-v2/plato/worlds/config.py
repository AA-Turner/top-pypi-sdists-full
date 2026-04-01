"""Configuration models for Plato worlds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from plato._generated.models import (
    EnvFromArtifact,
    EnvFromResource,
    EnvFromSimulator,
)
from plato.markers import FieldMarker, WorkspaceMarker
from plato.runtime import (
    DockerRuntimeConfig,
    RuntimeConfig,
    VMResources,
    VMRuntimeConfig,
)
from plato.v2.async_.session import SerializedSession
from plato.worlds.review.spec import ReviewSpec
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
    "WorkspaceSourceSpec",
]


class LLMConfig(BaseModel):
    """Configuration for an LLM used by a world.

    Attributes:
        model: Model identifier in litellm format (e.g. "anthropic/claude-sonnet-4-5-20250514")
        api_key: API key passed directly to litellm (works for any provider)
        max_tokens: Default max output tokens
        temperature: Default sampling temperature (None = provider default)
        concurrency: Max concurrent requests for this model (0 = unlimited).
            The limit is enforced per (model, api_base) pair globally in acompletion.
    """

    model: str
    api_base: str = ""
    api_key: str = ""
    max_tokens: int = 4096
    temperature: float | None = None
    concurrency: int = 0


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
    extra_sync: dict[str, Path] = Field(
        default_factory=dict,
        description="Extra paths to sync to VM at /extra/{name}",
    )
    sync_sdk: bool | Path = True
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


class PreviewConfig(BaseModel):
    """Configuration for world preview mode.

    Preview restores workspaces and calls the world's preview() method
    instead of the normal reset/step loop, then idles until timeout.
    """

    enabled: bool = False
    timeout_seconds: int = Field(
        default=600,
        ge=1,
        description="Preview lifetime in seconds (default: 10 minutes).",
    )


# =============================================================================
# Agent Configuration
# =============================================================================


class AgentConfig(BaseModel):
    """Configuration for an agent.

    Provide either ``package`` (resolved to an image at launch time) or
    ``image`` (direct ECR URI).  When both are absent the config is treated
    as an empty/unconfigured agent placeholder.

    Attributes:
        package: Agent package name with optional version (e.g. "claude-code:latest").
            Resolved to a Docker image URI by the Chronos backend before launch.
        image: Docker image URI for the agent (set by Chronos after resolving package,
            or provided directly for local/test runs).
        runtime: Runtime configuration (docker or vm with resources)
        config: Agent-specific configuration passed to the agent
        max_parallel: Maximum number of concurrent agent VMs for this config.
            When set, the world enforces a shared semaphore across all calls
            to ``world.agent()`` with the same config.  Applies globally —
            all pipeline stages sharing this agent config compete for the
            same pool of slots.
    """

    package: str | None = None
    image: str = ""
    runtime: RuntimeConfig = Field(default_factory=VMRuntimeConfig)
    config: dict[str, Any] = Field(default_factory=dict)
    max_parallel: int | None = Field(
        default=None,
        ge=1,
        description="Max concurrent agent VMs for this config. None = unlimited.",
    )


# =============================================================================
# World Configuration
# =============================================================================


class MergeAgentConfig(BaseModel):
    """Configuration for the agent that resolves git merge conflicts.

    When ``strategy`` is ``"agent"``, the merge agent package/image is invoked
    on the agent VM to resolve conflicts.  ``"theirs"`` and ``"ours"`` use
    deterministic git strategies without an LLM.
    """

    package: str = ""
    image: str = ""
    strategy: Literal["theirs", "ours", "agent"] = "agent"
    max_retries: int = Field(
        default=3,
        description="Max merge+push retry attempts before giving up.",
    )
    instruction_template: str = Field(
        default=(
            "Resolve the git merge conflicts in the workspace. "
            "Review both sides and produce a correct merged result. "
            "Stage and commit the resolution."
        ),
        description="Instruction sent to the merge agent when strategy is 'agent'.",
    )


class GitTransportConfig(BaseModel):
    """Configuration for git-based workspace transport.

    Used when a workspace declares ``transport="git"`` in its WorkspaceMarker.
    """

    merge_agent: MergeAgentConfig = Field(default_factory=MergeAgentConfig)
    auto_commit_message: str = Field(
        default="Agent workspace changes",
        description="Default commit message when auto-committing agent changes.",
    )
    commit_on_sync: bool = Field(
        default=True,
        description="Automatically commit all changes before pushing in sync_back.",
    )
    serialize_sync: bool = Field(
        default=True,
        description="Queue sync_back calls so only one agent pushes at a time. "
        "Prevents thundering-herd retries when many agents finish concurrently.",
    )
    seed_timeout: int = Field(
        default=60,
        description="Timeout in seconds for seeding the bare repo with initial workspace contents. "
        "Increase for large workspaces (e.g., 1000+ files over FUSE).",
    )


class WorkspaceSourceSpec(BaseModel):
    """Explicit workspace source for cross-world restore.

    Allows mounting workspaces from a different world by specifying the
    full source repo name alongside the resume ref.
    """

    repo: str = Field(description="Full source repo name, e.g. 'webclone/stripe/code'")
    ref: str = Field(description="Resume ref in 'session_id:step_name' format")


class StateConfig(BaseModel):
    """Configuration for world state persistence.

    State is persisted to the Chronos DB after each step. Worlds can call
    ``load_state()`` to fetch the latest state for the current session
    or a different session (cross-session resume).

    Attributes:
        enabled: Whether to enable state persistence (default: True).
        path: Path to the local state/workspace directory (default: /state).
    """

    enabled: bool = True
    path: str = "/state"
    resume_from: str = ""  # session_id to load pipeline state from (cross-session resume)
    resume_workspaces: dict[str, str] = Field(
        default_factory=dict,
        description="Map workspace name → repo name for cross-session resume, "
        "e.g. {'recordings': 'webclone/recordings'}",
    )
    workspaces: dict[str, str | WorkspaceSourceSpec] = Field(
        default_factory=dict,
        description="Per-workspace resume spec. Value can be a string 'session_id:step_name' "
        "(uses world's repo name) or a WorkspaceSourceSpec {repo, ref} for cross-world restore.",
    )
    checkpoint_interval_s: int = 300  # background checkpoint interval in seconds (0 = disabled)


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


class TailscaleConfig(BaseModel):
    """Optional Tailscale VPN configuration.

    When ``enabled`` is True, the world VM joins the specified tailnet before
    ``reset()`` runs.  This allows worlds to reach machines on the tailnet
    (e.g. GPU servers) by hostname.

    Uses ``api_key`` (a Tailscale API key) to generate a short-lived auth key
    automatically via the Tailscale API.

    Example YAML::

        tailscale:
          enabled: true
          api_key: "tskey-api-..."
    """

    enabled: bool = False
    api_key: str = ""


class ChildWorldConfig(BaseModel):
    """Pre-defined config for a child world, run inline or as a separate session.

    Used in the top-level ``child_worlds`` block of a launch config JSON::

        {
          "world": { "package": "plato-world-foo:1.0", "config": { ... } },
          "child_worlds": {
            "my-reviewer": {
              "mode": "inline",
              "world_name": "foo-review",
              "config": { "scoring_llm": { "model": "gemini/gemini-2.5-pro" } }
            }
          }
        }

    Modes:
        - ``"inline"``: instantiate the world in-process on the same VM,
          sharing the parent's workspaces, agents, and services.
        - ``"session"``: launch as a new Chronos child session on a separate VM.
    """

    mode: Literal["inline", "session"] = "session"
    package: str | None = None
    world_name: str
    config: dict[str, Any] = Field(default_factory=dict)
    runtime: dict[str, Any] | None = None
    tags: list[str] = Field(default_factory=list)


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

    # Transport mode for sharing workspaces with agent VMs
    transport_mode: Literal["nfs_kernel", "sshfs"] = Field(
        default="nfs_kernel",
        description="Default file-sharing transport between world and agent VMs. "
        "Individual workspaces can override via WorkspaceMarker(transport=...). "
        "Options: 'nfs_kernel' (default), 'sshfs'.",
    )

    # Slack notifications on session completion (requires Chronos org setting to be enabled)
    slack_notifications_enabled: bool = Field(
        default=False,
        description="Send Slack notifications when this session completes, fails, or is cancelled.",
    )

    # Checkpoint configuration for automatic snapshots after steps
    checkpoint: CheckpointConfig = Field(default_factory=CheckpointConfig)

    # State persistence configuration
    state: StateConfig = Field(default_factory=StateConfig)

    # Preview mode settings
    preview: PreviewConfig = Field(default_factory=PreviewConfig)

    # Review specification — defines how this session should be reviewed.
    # When set, the world runs verify() instead of the normal reset/step loop.
    # The spec is recursive: the reviewer can itself have a review spec.
    review: ReviewSpec | None = Field(
        default=None,
        description="How this session should be reviewed. None = no auto-review.",
    )

    # E2E test mode — when set, runs test functions from this directory after
    # reset() instead of the normal step() loop.  Tests receive the fully
    # initialized world instance (with workspaces, agents, etc.).
    e2e_test_dir: str | None = Field(
        default=None,
        description=(
            "Path to a directory of test_*.py files.  When set, the world runs "
            "reset() normally, then discovers and executes test functions instead "
            "of the step() loop.  Each test_*(world) receives the live world."
        ),
    )
    e2e_test_filter: str = Field(
        default="",
        description="Only run tests whose names contain this substring.",
    )

    # Optional Tailscale VPN — joins the tailnet before reset() if auth_key is set
    tailscale: TailscaleConfig = Field(default_factory=TailscaleConfig)

    model_config = {"extra": "allow"}

    # Child world configs — populated by the runner from the top-level
    # ``child_worlds`` block in the launch JSON.  Not intended to be set
    # directly in world-specific config classes.
    child_worlds: dict[str, ChildWorldConfig] = Field(default_factory=dict, exclude=True)

    @classmethod
    def get_field_annotations(cls) -> dict[str, FieldMarker | WorkspaceMarker | None]:
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
        Also parses top-level ``child_worlds`` and attaches them to the config.
        """
        path = Path(path)
        with open(path) as f:
            full = json.load(f)

        # Parse child_worlds from top-level before narrowing to world.config
        child_worlds_raw = full.get("child_worlds", {})
        child_worlds = {k: ChildWorldConfig.model_validate(v) for k, v in child_worlds_raw.items()}

        # Read from world.config if present
        data = full
        if "world" in data and isinstance(data["world"], dict) and "config" in data["world"]:
            data = data["world"]["config"]

        instance = cls.model_validate(data)
        instance.child_worlds = child_worlds
        return instance
