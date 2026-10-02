"""Managers for the :class:`~istari.IstariIntegrations` client.

The integrations surface — what the Integrations SDK and ``stari`` CLI use to talk
to the registry: agents, modules, tools, functions, and the operating-system
reference data. Method bodies land in Phase 4 (see SDK_REDESIGN.md §3).
"""

from __future__ import annotations

from istari_digital_client.sdk._integrations.agent_pools import AgentPools
from istari_digital_client.sdk._integrations.agents import Agents
from istari_digital_client.sdk._integrations.function_auth_secrets import FunctionAuthSecrets
from istari_digital_client.sdk._integrations.functions import Functions
from istari_digital_client.sdk._integrations.modules import Modules
from istari_digital_client.sdk._integrations.operating_systems import OperatingSystems
from istari_digital_client.sdk._integrations.tools import Tools


__all__ = [
    "AgentPools",
    "Agents",
    "FunctionAuthSecrets",
    "Functions",
    "Modules",
    "OperatingSystems",
    "Tools",
]
