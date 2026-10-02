"""Agents manager (IstariIntegrations surface).

``Agents`` does ``register`` / ``get`` / ``list`` / ``update_*``
against the v2 API, returning rich Agent objects.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import Agent as AgentType
from istari_digital_client.sdk._generated.v2.models.agent_status_name import AgentStatusName
from istari_digital_client.sdk._generated.v2.models.archive_status import ArchiveStatus
from istari_digital_client.sdk._generated.v2.models.new_agent import NewAgent
from istari_digital_client.sdk._generated.v2.models.new_agent_display_name import NewAgentDisplayName
from istari_digital_client.sdk._generated.v2.models.new_agent_information import NewAgentInformation
from istari_digital_client.sdk._generated.v2.models.new_agent_status import NewAgentStatus
from istari_digital_client.sdk._generated.v2.models.archive import Archive
from istari_digital_client.sdk._generated.v2.models.restore import Restore


class Agents(_Manager):
    """Manager for agents: register / get / list / update.

    Reached via ``integrations.agents``. Agents are execution workers that
    claim jobs from the registry (e.g., CAD tool wrappers, compute nodes).

    Sub-managers: none (Agents is a leaf collection).

    Usage::

        # 1. Register a new agent
        agent = integrations.agents.register(
            agent_version="1.0.0",
            host_os="Ubuntu 22.04",
        )

        # 2. Update agent status
        updated = integrations.agents.update_status(
            agent.id,
            status="ONLINE",
        )

        # 3. List all agents
        for agent in integrations.agents.list():
            print(agent.id, agent.created)
    """

    def register(
        self,
        *,
        agent_version: str,
        host_os: str,
        api_hashes: str | None = None,
    ) -> AgentType:
        """Register (create/enroll) a new agent — a worker that runs jobs.

        Mutates: true

        Aliases: create add enroll worker runner

        Args:
            agent_version: The agent software version (e.g., "1.0.0").
            host_os: The host operating system (e.g., "Ubuntu 22.04").
            api_hashes: Optional API compatibility hashes.

        Returns:
            An Agent with fields: id, created, display_name_history, information_history,
            status_history, modules_history, agent_pools, archive_status, created_by_id,
            compatibility_status, incompatible_tags, deprecated_tags.
        """
        dto = self._call(
            self._engine.v2_api.register_agent,
            NewAgent(
                agent_version=agent_version,
                host_os=host_os,
                api_hashes=api_hashes,
            ),
        )
        return AgentType._bind(dto, mgr=self)

    def get(self, agent_id: str) -> AgentType:
        """Fetch an agent by its UUID.

        Args:
            agent_id: The UUID of the agent to fetch.

        Returns:
            An Agent with all fields populated.

        Raises:
            NotFoundError: If no agent with that id exists.
        """
        dto = self._call(self._engine.v2_api.get_agent, agent_id)
        return AgentType._bind(dto, mgr=self)

    def list(
        self,
        *,
        agent_version: str | None = None,
        host_os: str | None = None,
        updated_since: datetime | None = None,
        module_name: str | None = None,
        module_version: str | None = None,
        status_name: AgentStatusName | None = None,
        tenant_id: str | None = None,
        all_tenants: bool | None = None,
        in_agent_pools: bool | None = None,
        page: int | None = None,
        size: int | None = None,
        archive_status: ArchiveStatus | None = None,
        sort: str | None = None,
    ) -> Page[AgentType]:
        """List agents, returning an auto-paging sequence.

        Iterating the returned Page automatically fetches subsequent pages.

        Args:
            agent_version: Filter by the agent version.
            host_os: Filter by the host OS.
            updated_since: Filter by last update time of agent.
            module_name: Filter by name of module loaded on the agent.
            module_version: Filter by version of module loaded on the agent.
            status_name: Filter by the agent status name.
            tenant_id: Filter by tenant ID.
            all_tenants: Show agents across all tenants (customer admin only).
            in_agent_pools: Filter results by (non-)membership in an active agent pool (customer admins only).
            page: Optional page number (1-indexed).
            size: Optional page size.
            archive_status: Filter results by archive status (active, archived, all).
            sort: Sort field and order.

        Returns:
            A Page of Agent objects.
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_agents,
                agent_version=agent_version,
                host_os=host_os,
                updated_since=updated_since,
                module_name=module_name,
                module_version=module_version,
                status_name=status_name,
                tenant_id=tenant_id,
                all_tenants=all_tenants,
                in_agent_pools=in_agent_pools,
                page=page_num,
                size=size,
                archive_status=archive_status,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: AgentType._bind(d, mgr=self), start_page=page or 1
        )

    def update_display_name(self, agent_id: str, *, display_name: str) -> AgentType:
        """Update an agent's display name.

        Mutates: true

        Args:
            agent_id: The UUID of the agent to update.
            display_name: The new display name.

        Returns:
            The updated Agent.

        Raises:
            NotFoundError: If no agent with that id exists.
        """
        dto = self._call(
            self._engine.v2_api.update_agent_display_name,
            agent_id,
            NewAgentDisplayName(display_name=display_name),
        )
        return AgentType._bind(dto, mgr=self)

    def update_status(
        self, agent_id: str, *, status: str | AgentStatusName
    ) -> AgentType:
        """Update an agent's status.

        Mutates: true

        Args:
            agent_id: The UUID of the agent to update.
            status: The new status (AgentStatusName enum or string value).

        Returns:
            The updated Agent.

        Raises:
            NotFoundError: If no agent with that id exists.
        """
        dto = self._call(
            self._engine.v2_api.update_agent_status,
            agent_id,
            NewAgentStatus(
                name=AgentStatusName(status) if isinstance(status, str) else status
            ),
        )
        return AgentType._bind(dto, mgr=self)

    def update_information(
        self,
        agent_id: str,
        *,
        agent_version: str,
        host_os: str,
        api_hashes: str | None = None,
    ) -> AgentType:
        """Update an agent's information (version, OS, API hashes).

        Mutates: true

        Args:
            agent_id: The UUID of the agent to update.
            agent_version: The agent software version.
            host_os: The host operating system.
            api_hashes: Optional API compatibility hashes.

        Returns:
            The updated Agent.

        Raises:
            NotFoundError: If no agent with that id exists.
        """
        dto = self._call(
            self._engine.v2_api.update_agent_information,
            agent_id,
            NewAgentInformation(
                agent_version=agent_version,
                host_os=host_os,
                api_hashes=api_hashes,
            ),
        )
        return AgentType._bind(dto, mgr=self)

    def archive(self, agent_id: str, *, reason: str | None = None) -> AgentType:
        """Archive (soft-delete) an agent, preventing it from accepting new jobs.

        Mutates: true

        Existing in-progress jobs are not affected. The agent can be restored
        later using restore().

        Args:
            agent_id: The UUID of the agent to archive.
            reason: Optional reason for archiving.

        Returns:
            The archived Agent.

        Raises:
            NotFoundError: If no agent with that id exists.
        """
        archive_body = Archive(reason=reason) if reason else None
        dto = self._call(
            self._engine.v2_api.archive_agent,
            agent_id,
            archive_body,
        )
        return AgentType._bind(dto, mgr=self)

    def restore(self, agent_id: str, *, reason: str | None = None) -> AgentType:
        """Restore a previously archived agent, allowing it to accept jobs again.

        Mutates: true

        Args:
            agent_id: The UUID of the agent to restore.
            reason: Optional reason for restoring.

        Returns:
            The restored Agent.

        Raises:
            NotFoundError: If no agent with that id exists.
        """
        restore_body = Restore(reason=reason) if reason else None
        dto = self._call(
            self._engine.v2_api.restore_agent,
            agent_id,
            restore_body,
        )
        return AgentType._bind(dto, mgr=self)
