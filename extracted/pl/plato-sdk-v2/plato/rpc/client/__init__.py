"""World-side client for the agent RPC layer."""

from plato.rpc.client.connection import AgentDaemonClient
from plato.rpc.client.manager import (
    close_agent_client,
    get_agent_client,
    reset_registry,
)

__all__ = [
    "AgentDaemonClient",
    "close_agent_client",
    "get_agent_client",
    "reset_registry",
]
