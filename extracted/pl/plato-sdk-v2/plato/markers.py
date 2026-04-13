"""Annotation markers for Plato configurations (agents and worlds).

Provides typed annotation markers for special fields like secrets, agents,
and environments in configuration classes.

Usage (agents):
    from plato.markers import Secret
    api_key: Annotated[str, Secret(description="API key")]

Usage (worlds):
    from plato.markers import Agent, WorldSecret, Env, EnvList, FieldMarker
    coder: Annotated[AgentConfig, Agent(description="Coding agent")]
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from plato.worlds.config import GitTransportConfig


class FieldMarker:
    """Base marker for special fields in configs.

    This is the underlying implementation. Use Agent(), Secret(), Env(), or EnvList()
    for cleaner syntax.
    """

    def __init__(
        self,
        kind: Literal["agent", "secret", "env", "env_list"],
        description: str = "",
        required: bool = True,
    ):
        self.kind = kind
        self.description = description
        self.required = required


class Secret:
    """Annotation marker for secret fields in agent configs.

    Fields annotated with Secret are automatically loaded from environment variables.
    The env var name is the uppercase version of the field name (e.g., api_key -> API_KEY).

    Usage:
        api_key: Annotated[str, Secret(description="API key")]
    """

    def __init__(self, description: str = "", required: bool = False):
        self.description = description
        self.required = required


def Agent(description: str = "", required: bool = True) -> FieldMarker:
    """Marker for agent fields in world configs.

    Usage:
        coder: Annotated[AgentConfig, Agent(description="Coding agent")]
    """
    return FieldMarker("agent", description, required)


def WorldSecret(description: str = "", required: bool = False) -> FieldMarker:
    """Marker for secret fields in world configs.

    Returns a FieldMarker (unlike agent Secret which is a class), for use with
    the world schema system.

    Usage:
        git_token: Annotated[str | None, WorldSecret(description="GitHub token")] = None
    """
    return FieldMarker("secret", description, required)


def Env(description: str = "", required: bool = True) -> FieldMarker:
    """Marker for single environment fields in world configs.

    Usage:
        database: Annotated[EnvConfig, Env(description="Database server")]
    """
    return FieldMarker("env", description, required)


def EnvList(description: str = "") -> FieldMarker:
    """Marker for a list of arbitrary environments in world configs.

    Usage:
        envs: Annotated[list[EnvConfig], EnvList(description="Environments")]
    """
    return FieldMarker("env_list", description, required=False)


class WorkspaceMarker:
    """Marker for workspace fields in world configs.

    Declares a workspace directory that is automatically created, registered
    for backup, and optionally versioned with DVC. The workspace is also
    prepared as an NFS/rsync transport so agents can access it.

    Usage:
        output: Annotated[Path, WorkspaceMarker(description="Build output")]
        cache: Annotated[Path, WorkspaceMarker(description="LLM cache", tracked=False)]
        code: Annotated[Path, WorkspaceMarker(description="Code dir", mount_path="/workspace")]
        code: Annotated[Path, WorkspaceMarker(description="Code", dvcignore=["dist"])]

    Args:
        description: Human-readable description.
        tracked: If True (default), workspace is backed up and versioned with DVC.
        mount_path: Mount path on agent VMs. Defaults to the workspace content path.
            Use this when agents expect files at a specific location (e.g. "/workspace/code").
        dvcignore: Extra patterns to add to .dvcignore (merged with DEFAULT_DVCIGNORE).
        transport: Per-workspace transport override. When ``None`` (default), the
            workspace inherits the world config ``transport_mode``. Set to ``"git"`` to
            use git clone/push instead of NFS/SSHFS for this workspace.
        git_config: Git transport configuration. Only used when ``transport="git"``.
        commit_strategy: DVC commit strategy. ``"manifest"`` (default) uploads individual
            files; ``"archive"`` uploads the entire directory as a single tar.gz.
    """

    DEFAULT_DVCIGNORE: tuple[str, ...] = (
        "node_modules",
        "__pycache__",
        ".next",
        ".venv",
        "*.pyc",
        ".cache",
        ".turbo",
        ".runtime",
        ".plato",
    )

    def __init__(
        self,
        description: str = "",
        tracked: bool = True,
        mount_path: str | None = None,
        dvcignore: list[str] | None = None,
        transport: Literal["nfs_kernel", "sshfs", "git"] | None = None,
        git_config: GitTransportConfig | None = None,
        commit_strategy: Literal["manifest", "archive"] = "manifest",
    ):
        self.kind = "workspace"
        self.description = description
        self.tracked = tracked
        self.mount_path = mount_path
        self.dvcignore = dvcignore
        self.transport = transport
        self.git_config = git_config
        self.commit_strategy = commit_strategy
