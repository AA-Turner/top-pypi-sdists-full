"""Rich domain types for the :class:`~istari.IstariIntegrations` client.

These classes subclass their generated DTOs and mix in :class:`~istari.ClientHaving`
plus capability mixins. Fields are inherited from the DTO; only methods are added.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from istari_digital_client.sdk._base import ClientHaving

if TYPE_CHECKING:
    from istari_digital_client.sdk._integrations.agents import Agents
    from istari_digital_client.sdk._integrations.agent_pools import AgentPools
from istari_digital_client.sdk._generated.v2.models.agent import Agent as AgentDto
from istari_digital_client.sdk._generated.v2.models.agent_pool import AgentPool as AgentPoolDto
from istari_digital_client.sdk._generated.v2.models.function import Function as FunctionDto
from istari_digital_client.sdk._generated.v2.models.function_auth_secret import (
    FunctionAuthSecret as FunctionAuthSecretDto,
)
from istari_digital_client.sdk._generated.v2.models.module import Module as ModuleDto
from istari_digital_client.sdk._generated.v2.models.module_version import ModuleVersion as ModuleVersionDto
from istari_digital_client.sdk._generated.v2.models.operating_system import (
    OperatingSystem as OperatingSystemDto,
)
from istari_digital_client.sdk._generated.v2.models.tool import Tool as ToolDto
from istari_digital_client.sdk._generated.v2.models.tool_version import ToolVersion as ToolVersionDto


class Agent(AgentDto, ClientHaving):
    """An agent — a worker/runner that claims and executes jobs from the registry.

    Aliases: worker runner node compute execution-node


    Provides convenience properties to access the latest values from history lists.
    Supports archive/restore for soft-deletion.
    """

    if TYPE_CHECKING:
        _mgr: Agents

    @property
    def display_name(self) -> str | None:
        """The current display name (from most recent display_name_history entry)."""
        if self.display_name_history:
            return self.display_name_history[-1].display_name
        return None

    @property
    def agent_version(self) -> str | None:
        """The current agent version (from most recent information_history entry)."""
        if self.information_history:
            return self.information_history[-1].agent_version
        return None

    @property
    def host_os(self) -> str | None:
        """The current host OS (from most recent information_history entry)."""
        if self.information_history:
            return self.information_history[-1].host_os
        return None

    def archive(self, *, reason: str | None = None) -> "Agent":
        """Archive (soft-delete) this agent, preventing it from accepting new jobs.

        Mutates: true

        Existing in-progress jobs are not affected. The agent can be restored
        later using restore().

        Args:
            reason: Optional reason for archiving.

        Returns:
            The archived Agent.
        """
        return self._mgr.archive(self.id, reason=reason)

    def restore(self, *, reason: str | None = None) -> "Agent":
        """Restore this previously archived agent, allowing it to accept jobs again.

        Mutates: true

        Args:
            reason: Optional reason for restoring.

        Returns:
            The restored Agent.
        """
        return self._mgr.restore(self.id, reason=reason)


class AgentPool(AgentPoolDto, ClientHaving):
    """An agent pool (groups agents for job assignment).

    Supports archive/restore for soft-deletion.
    """

    if TYPE_CHECKING:
        _mgr: AgentPools

    def archive(self, *, reason: str | None = None) -> "AgentPool":
        """Archive (soft-delete) this agent pool.

        Mutates: true

        Jobs assigned to this pool will not be dispatched until the pool is restored.

        Args:
            reason: Optional reason for archiving.

        Returns:
            The archived AgentPool.
        """
        return self._mgr.archive(self.id, reason=reason)

    def restore(self, *, reason: str | None = None) -> "AgentPool":
        """Restore this previously archived agent pool.

        Mutates: true

        After restoration, jobs can again be dispatched to agents in this pool.

        Args:
            reason: Optional reason for restoring.

        Returns:
            The restored AgentPool.
        """
        return self._mgr.restore(self.id, reason=reason)


class Function(FunctionDto, ClientHaving):
    """A function — an executable operation (registered by a module) you run as a job.

    Aliases: operation task tool routine
    """


class FunctionAuthSecret(FunctionAuthSecretDto, ClientHaving):
    """A stored credential (function auth secret) used when running a function.

    Aliases: credential secret api-key token login password oauth
    """


class Module(ModuleDto, ClientHaving):
    """A module — a versioned software package that registers functions.

    Aliases: package library plugin bundle
    """


class ModuleVersion(ModuleVersionDto, ClientHaving):
    """A module version (specific version of a module)."""


class OperatingSystem(OperatingSystemDto, ClientHaving):
    """An operating system (OS/platform) entry — a target environment for function variants and jobs.

    Aliases: os platform environment target
    """


class Tool(ToolDto, ClientHaving):
    """A tool — a versioned application/executable a function runs in (e.g. a CAD or analysis program).

    Aliases: application software executable program cad-tool
    """


class ToolVersion(ToolVersionDto, ClientHaving):
    """A tool version (specific version of a tool)."""


__all__ = [
    "Agent",
    "AgentPool",
    "Function",
    "FunctionAuthSecret",
    "Module",
    "ModuleVersion",
    "OperatingSystem",
    "Tool",
    "ToolVersion",
]
