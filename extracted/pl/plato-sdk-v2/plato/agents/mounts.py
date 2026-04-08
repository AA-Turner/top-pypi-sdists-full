"""Workspace mount models for agent execution."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from plato.transports import NFSTransport, RsyncTransport, SSHFSTransport, Transport
from plato.transports.git import GitTransport
from plato.utils.tool_execution import tool_execution_spool_path

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.worlds.workspace import Workspace


TransportKind = Literal["git", "nfs", "sshfs", "rsync"]
GitSyncMode = Literal["merge_to_main", "push_branch", "publish_ref"]


@dataclass(frozen=True, slots=True)
class GitCheckoutPolicy:
    """Checkout configuration for a git-backed agent mount."""

    ref: str | None = None
    branch_name: str | None = None


@dataclass(frozen=True, slots=True)
class GitSyncPolicy:
    """Sync-back behavior for a git-backed agent mount."""

    mode: GitSyncMode = "merge_to_main"
    target: str | None = None
    exact: bool = False

    @classmethod
    def merge_to_main(cls) -> GitSyncPolicy:
        return cls(mode="merge_to_main")

    @classmethod
    def push_branch(cls, branch_name: str) -> GitSyncPolicy:
        return cls(mode="push_branch", target=branch_name, exact=True)

    @classmethod
    def publish_ref(cls, ref: str, *, exact: bool = False) -> GitSyncPolicy:
        return cls(mode="publish_ref", target=ref, exact=exact)


class AgentWorkspaceMountGitPayload(BaseModel):
    """Serializable git-specific mount metadata exposed to agents."""

    checkout_ref: str | None = None
    branch_name: str | None = None
    sync_mode: GitSyncMode | None = None
    sync_target: str | None = None
    sync_exact: bool = False


class AgentWorkspaceMountPayload(BaseModel):
    """Serializable agent mount metadata exposed to agents."""

    workspace_name: str
    world_path: str
    world_root_path: str
    agent_path: str
    tracked: bool
    transport_kind: TransportKind
    git: AgentWorkspaceMountGitPayload | None = None

    @property
    def name(self) -> str:
        return self.workspace_name

    @property
    def path(self) -> str:
        return self.world_path

    @property
    def root_path(self) -> str:
        return self.world_root_path

    @property
    def mount_path(self) -> str:
        return self.agent_path


@dataclass(slots=True)
class AgentWorkspaceMount:
    """A world-owned workspace mounted into an agent runtime."""

    workspace_name: str
    world_path: Path
    world_root_path: Path
    agent_path: str
    tracked: bool
    transport_kind: TransportKind
    transport: Transport
    git_checkout: GitCheckoutPolicy | None = None
    git_sync: GitSyncPolicy | None = None
    git_raise_on_conflict: bool = False
    audit_run_id: str | None = None
    audit_key: str | None = None

    @classmethod
    def from_workspace(cls, workspace: Workspace) -> AgentWorkspaceMount:
        if workspace.transport is None:
            raise RuntimeError(f"Workspace '{workspace.name}' has not been started")
        transport = workspace.transport.with_path(str(workspace.path))
        transport_kind = _transport_kind(transport)
        git_sync = GitSyncPolicy.merge_to_main() if transport_kind == "git" else None
        return cls(
            workspace_name=workspace.name,
            world_path=workspace.path,
            world_root_path=workspace.root_path,
            agent_path=workspace.mount_path,
            tracked=workspace.tracked,
            transport_kind=transport_kind,
            transport=transport,
            git_sync=git_sync,
        )

    @property
    def mount_path(self) -> str:
        return self.agent_path

    @property
    def path(self) -> Path:
        return self.world_path

    @property
    def root_path(self) -> Path:
        return self.world_root_path

    def with_agent_path(self, agent_path: str) -> AgentWorkspaceMount:
        return replace(self, agent_path=agent_path)

    def with_git_options(
        self,
        *,
        checkout: GitCheckoutPolicy | None = None,
        sync: GitSyncPolicy | None = None,
        raise_on_conflict: bool | None = None,
    ) -> AgentWorkspaceMount:
        if self.transport_kind != "git":
            raise TypeError(f"Workspace '{self.workspace_name}' does not use git transport")
        return replace(
            self,
            git_checkout=checkout if checkout is not None else self.git_checkout,
            git_sync=sync if sync is not None else self.git_sync,
            git_raise_on_conflict=raise_on_conflict if raise_on_conflict is not None else self.git_raise_on_conflict,
        )

    async def setup_agent(self, agent_env: Environment | None, hostname: str) -> None:
        await self.transport.setup_agent(agent_env, hostname, self)

    async def sync_back(self, agent_env: Environment | None, hostname: str) -> None:
        await self.transport.sync_back(agent_env, hostname, self)

    def clone_for_run(self) -> AgentWorkspaceMount:
        """Copy the transport so per-run state does not mutate the shared mount."""
        return replace(
            self,
            transport=self.transport.with_path(str(self.world_path)),
        )

    def to_payload(self) -> AgentWorkspaceMountPayload:
        return AgentWorkspaceMountPayload(
            workspace_name=self.workspace_name,
            world_path=str(self.world_path),
            world_root_path=str(self.world_root_path),
            agent_path=self.agent_path,
            tracked=self.tracked,
            transport_kind=self.transport_kind,
            git=(
                AgentWorkspaceMountGitPayload(
                    checkout_ref=self.git_checkout.ref if self.git_checkout else None,
                    branch_name=self.git_checkout.branch_name if self.git_checkout else None,
                    sync_mode=self.git_sync.mode if self.git_sync else None,
                    sync_target=self.git_sync.target if self.git_sync else None,
                    sync_exact=self.git_sync.exact if self.git_sync else False,
                )
                if self.transport_kind == "git"
                else None
            ),
        )


@dataclass(slots=True)
class AuditedMount:
    """Per-run audit metadata derived from a mounted workspace."""

    mount: AgentWorkspaceMount
    audit_run_id: str
    audit_key: str

    @property
    def workspace_name(self) -> str:
        return self.mount.workspace_name

    @property
    def root_path(self) -> Path:
        return self.mount.world_root_path

    @property
    def mount_path(self) -> str:
        return self.mount.agent_path

    @property
    def transport(self) -> Transport:
        return self.mount.transport

    @property
    def spool_path(self) -> Path:
        return self.root_path / ".plato" / "audit" / self.workspace_name / f"{self.audit_run_id}.jsonl"

    @property
    def tool_spool_path(self) -> Path:
        return tool_execution_spool_path(
            self.root_path / ".plato",
            workspace_name=self.workspace_name,
            audit_run_id=self.audit_run_id,
        )


def _transport_kind(transport: Transport) -> TransportKind:
    if isinstance(transport, GitTransport):
        return "git"
    if isinstance(transport, NFSTransport):
        return "nfs"
    if isinstance(transport, SSHFSTransport):
        return "sshfs"
    if isinstance(transport, RsyncTransport):
        return "rsync"
    raise TypeError(f"Unsupported transport type: {type(transport).__name__}")
