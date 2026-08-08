"""``rpc_or_ssh`` — the per-capability gate every migrated call site goes through.

Decision order for one operation:

1. Flag off for this capability → run the SSH body. (Operator KILL SWITCH — flag is on unless PLATO_AGENT_RPC_CAPS=none.)
2. Flag on → ensure the daemon is up (bootstrap once if the host is unknown).
3. Daemon up AND advertises the capability → run the RPC body. Its errors
   (auth, unreachable, reclaimed, remote-op-failed) propagate as typed
   exceptions; they are NEVER retried over SSH — that would double-execute a
   possibly-completed op. Retry is the caller's job (fresh VM).
4. Otherwise (daemon absent / old / capability missing) → run the SSH body.

So SSH fallback happens ONLY before an RPC op is submitted. This is the whole
safety argument for mixing the two transports during rollout.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TypeVar

from plato.rpc.client.bootstrap import ensure_daemon
from plato.rpc.client.connection import AgentDaemonClient
from plato.rpc.client.flags import flag_enables
from plato.rpc.client.manager import get_agent_client, get_host_state, session_token
from plato.rpc.errors import AgentUnreachableError
from plato.rpc.protocol import DEFAULT_PORT

_T = TypeVar("_T")


async def rpc_or_ssh(
    hostname: str,
    ssh_key_path: Path,
    capability: str,
    rpc_fn: Callable[[AgentDaemonClient], Awaitable[_T]],
    ssh_fn: Callable[[], Awaitable[_T]],
    *,
    port: int = DEFAULT_PORT,
) -> _T:
    if not flag_enables(capability):
        return await ssh_fn()

    await ensure_daemon(hostname, ssh_key_path, port=port)
    state = get_host_state(hostname)
    if state.has_capability(capability):
        token = state.token or session_token()
        client = get_agent_client(hostname, token, port=port)
        try:
            return await rpc_fn(client)
        except AgentUnreachableError:
            # The daemon stopped answering (crashed, or a fresh VM inherited
            # this mesh IP without a daemon). This op still fails — never
            # re-run over SSH — but reset the host to "unknown" so the NEXT
            # op re-bootstraps (idempotent) instead of failing forever.
            state.mode = "unknown"
            state.handshake = None
            raise

    return await ssh_fn()
