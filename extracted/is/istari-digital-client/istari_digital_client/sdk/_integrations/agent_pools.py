"""Agent Pools manager (IstariIntegrations surface)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import AgentPool as AgentPoolType
from istari_digital_client.sdk._generated.v2.models.new_agent_pool import NewAgentPool
from istari_digital_client.sdk._generated.v2.models.archive_status import ArchiveStatus
from istari_digital_client.sdk._generated.v2.models.archive import Archive
from istari_digital_client.sdk._generated.v2.models.restore import Restore


class AgentPools(_Manager):
    """Manager for agent pools: create / get / list / update."""

    def create(self, *, name: str, description: str | None = None) -> AgentPoolType:
        """Create a new agent pool.

        Mutates: true
        """
        dto = self._call(
            self._engine.v2_api.create_agent_pool,
            NewAgentPool(name=name, description=description),
        )
        return AgentPoolType._bind(dto, mgr=self)

    def get(self, agent_pool_id: str) -> AgentPoolType:
        """Fetch an agent pool by UUID."""
        dto = self._call(self._engine.v2_api.get_agent_pool, agent_pool_id)
        return AgentPoolType._bind(dto, mgr=self)

    def list(
        self,
        *,
        all_users: bool | None = None,
        page: int | None = None,
        size: int | None = None,
        archive_status: ArchiveStatus | None = None,
        sort: str | None = None,
    ) -> Page[AgentPoolType]:
        """List agent pools."""

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_agent_pools,
                all_users=all_users,
                page=page_num,
                size=size,
                archive_status=archive_status,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: AgentPoolType._bind(d, mgr=self), start_page=page or 1
        )

    def update(
        self, agent_pool_id: str, *, name: str, description: str | None = None
    ) -> AgentPoolType:
        """Update an agent pool's name and/or description.

        Mutates: true
        """
        dto = self._call(
            self._engine.v2_api.update_agent_pool,
            agent_pool_id,
            NewAgentPool(name=name, description=description),
        )
        return AgentPoolType._bind(dto, mgr=self)

    def archive(
        self, agent_pool_id: str, *, reason: str | None = None
    ) -> AgentPoolType:
        """Archive (soft-delete) an agent pool.

        Mutates: true

        Jobs assigned to this pool will not be dispatched until the pool is restored.

        Args:
            agent_pool_id: The UUID of the agent pool to archive.
            reason: Optional reason for archiving.

        Returns:
            The archived AgentPool.

        Raises:
            NotFoundError: If no agent pool with that id exists.
        """
        archive_body = Archive(reason=reason) if reason else None
        dto = self._call(
            self._engine.v2_api.archive_agent_pool,
            agent_pool_id,
            archive_body,
        )
        return AgentPoolType._bind(dto, mgr=self)

    def restore(
        self, agent_pool_id: str, *, reason: str | None = None
    ) -> AgentPoolType:
        """Restore a previously archived agent pool.

        Mutates: true

        After restoration, jobs can again be dispatched to agents in this pool.

        Args:
            agent_pool_id: The UUID of the agent pool to restore.
            reason: Optional reason for restoring.

        Returns:
            The restored AgentPool.

        Raises:
            NotFoundError: If no agent pool with that id exists.
        """
        restore_body = Restore(reason=reason) if reason else None
        dto = self._call(
            self._engine.v2_api.restore_agent_pool,
            agent_pool_id,
            restore_body,
        )
        return AgentPoolType._bind(dto, mgr=self)
