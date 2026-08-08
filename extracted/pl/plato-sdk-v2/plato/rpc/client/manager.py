"""Per-host client cache and RPC state registry.

Mirrors ``plato/git_ops/remote.py``'s per-host ``_CLIENTS`` cache and
``plato/utils/subprocess.py``'s ``_SSH_USER_BY_HOST`` register/unregister
pattern: one client per agent VM for the session, with ``close_agent_client``
as the teardown hook (called when a VM's mesh IP is retired so a reused IP
never inherits stale state).
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Literal

from plato.rpc.client.connection import AgentDaemonClient
from plato.rpc.models.health import HandshakeResponse
from plato.rpc.protocol import DEFAULT_PORT

HostMode = Literal["unknown", "rpc", "ssh_only"]


@dataclass
class HostRpcState:
    """What the world knows about one agent VM's RPC surface.

    ``mode`` drives the fallback gate: ``unknown`` → attempt bootstrap once;
    ``rpc`` → daemon reachable, gate features on ``handshake.capabilities``;
    ``ssh_only`` → bootstrap failed or SDK too old, use SSH for everything.
    """

    hostname: str
    token: str | None = None
    mode: HostMode = "unknown"
    handshake: HandshakeResponse | None = None

    def has_capability(self, capability: str) -> bool:
        if self.mode != "rpc" or self.handshake is None:
            return False
        return capability in self.handshake.capabilities


_CLIENTS: dict[str, AgentDaemonClient] = {}
_HOST_STATE: dict[str, HostRpcState] = {}
# One bearer token per session (world process), reused for every agent VM's
# daemon. Minted lazily on first bootstrap.
_session_token: str | None = None


def session_token() -> str:
    global _session_token
    if _session_token is None:
        _session_token = secrets.token_urlsafe(32)
    return _session_token


def get_host_state(hostname: str) -> HostRpcState:
    state = _HOST_STATE.get(hostname)
    if state is None:
        state = HostRpcState(hostname=hostname)
        _HOST_STATE[hostname] = state
    return state


def get_agent_client(hostname: str, token: str, *, port: int = DEFAULT_PORT) -> AgentDaemonClient:
    client = _CLIENTS.get(hostname)
    if client is None:
        client = AgentDaemonClient(hostname, token, port=port)
        _CLIENTS[hostname] = client
    return client


async def close_agent_client(hostname: str) -> None:
    """Drop the cached client and host state for a hostname (mesh-IP reuse
    safety). Mirrors ``unregister_ssh_user``."""
    client = _CLIENTS.pop(hostname, None)
    if client is not None:
        await client.close()
    _HOST_STATE.pop(hostname, None)


async def reset_registry() -> None:
    """Close all clients and clear state. For tests and process teardown."""
    global _session_token
    for hostname in list(_CLIENTS):
        await close_agent_client(hostname)
    _HOST_STATE.clear()
    _session_token = None
