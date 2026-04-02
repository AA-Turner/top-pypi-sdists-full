"""Base transport interfaces for sharing files between world and agent VMs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment


class Transport(ABC):
    """Abstract transport for sharing files between world VM and agent VMs."""

    path: str
    mount_path: str | None = None
    workspace_name: str | None = None
    workspace_repo_root: str | None = None
    workspace_tracked: bool = False
    audit_run_id: str | None = None
    audit_key: str | None = None

    @abstractmethod
    async def initialize(self) -> None:
        """One-time setup on the world VM (e.g., start NFS server)."""

    @abstractmethod
    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Make workspace available on an agent VM."""

    @abstractmethod
    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        """Sync changes back from agent VM to world VM."""

    @abstractmethod
    def with_path(self, path: str) -> Transport:
        """Return a copy of this transport with a different path."""

    @property
    def agent_mount_path(self) -> str:
        """Path where this workspace appears on the agent VM."""
        return self.mount_path or self.path

    def configure_workspace(
        self,
        *,
        name: str | None,
        repo_root: str | None,
        tracked: bool,
    ) -> None:
        """Attach workspace metadata to the transport for downstream integration."""
        self.workspace_name = name
        self.workspace_repo_root = repo_root
        self.workspace_tracked = tracked

    def configure_audit_scope(
        self,
        *,
        audit_run_id: str | None,
        audit_key: str | None,
    ) -> None:
        """Attach per-run audit scope metadata."""
        self.audit_run_id = audit_run_id
        self.audit_key = audit_key

    async def prepare(self) -> None:
        """Prepare this workspace's path on the world VM (e.g., NFS bind mount)."""

    def mount_at(self, remote_path: str) -> Transport:
        """Return a copy that mounts at a custom path on the agent VM."""
        transport = self.with_path(self.path)
        transport.mount_path = remote_path
        return transport
