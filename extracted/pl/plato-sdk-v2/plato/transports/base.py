"""Base transport interfaces for sharing files between world and agent VMs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.v2.async_.environment import Environment


class Transport(ABC):
    """Abstract transport for sharing files between world VM and agent VMs."""

    path: str
    mount_path: str | None

    @abstractmethod
    async def initialize(self) -> None:
        """One-time setup on the world VM (e.g., start NFS server)."""

    @abstractmethod
    async def setup_agent(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        """Make workspace available on an agent VM."""

    @abstractmethod
    async def sync_back(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        """Sync changes back from agent VM to world VM."""

    @abstractmethod
    def with_path(self, path: str) -> Transport:
        """Return a copy of this transport with a different world path."""

    async def prepare(self) -> None:
        """Prepare this workspace's path on the world VM (e.g., NFS bind mount)."""

    async def collect_audit_log(
        self,
        hostname: str,
        audit_key: str | None = None,
    ) -> str | None:
        del hostname, audit_key
        return None
