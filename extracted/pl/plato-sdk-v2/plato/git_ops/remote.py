"""Remote git operation helpers.

Callers are transport-agnostic: ``run_remote_git_op`` routes each op through
the agent daemon's git service when the flag + handshake allow it (typed
transport, idempotency-key dedupe on resend), and otherwise falls back to the
original SSH-stdio ``RemoteGitClient`` path, unchanged.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from plato.git_ops.client import RemoteGitClient
from plato.git_ops.models import GitOpRequest, GitOpResult
from plato.rpc.client.connection import AgentDaemonClient
from plato.rpc.client.fallback import rpc_or_ssh
from plato.rpc.protocol import CAP_GIT

_CLIENTS: dict[tuple[str, str], RemoteGitClient] = {}


def _client_key(ssh_key_path: Path, hostname: str) -> tuple[str, str]:
    return (str(ssh_key_path.resolve()), hostname)


async def run_remote_git_op(
    ssh_key_path: Path,
    hostname: str,
    request: GitOpRequest,
    *,
    timeout: int,
) -> GitOpResult:
    async def _rpc(client: AgentDaemonClient) -> GitOpResult:
        return await client.post(
            "git/op",
            request,
            GitOpResult,
            deadline_s=float(timeout),
            idempotency_key=uuid.uuid4().hex,
        )

    async def _ssh() -> GitOpResult:
        return await _run_stdio_git_op(ssh_key_path, hostname, request, timeout=timeout)

    return await rpc_or_ssh(hostname, ssh_key_path, CAP_GIT, _rpc, _ssh)


async def _run_stdio_git_op(
    ssh_key_path: Path,
    hostname: str,
    request: GitOpRequest,
    *,
    timeout: int,
) -> GitOpResult:
    """Original SSH-stdio path: cached persistent client, close-recreate-resend
    once on any failure."""
    key = _client_key(ssh_key_path, hostname)
    client = _CLIENTS.get(key)
    if client is None:
        client = RemoteGitClient(ssh_key_path, hostname)
        _CLIENTS[key] = client
    try:
        return await client.run(request, timeout=timeout)
    except Exception:
        await client.close()
        _CLIENTS.pop(key, None)
        retry_client = RemoteGitClient(ssh_key_path, hostname)
        _CLIENTS[key] = retry_client
        try:
            return await retry_client.run(request, timeout=timeout)
        except Exception:
            await retry_client.close()
            _CLIENTS.pop(key, None)
            raise


async def run_remote_git_checked(
    ssh_key_path: Path,
    hostname: str,
    request: GitOpRequest,
    *,
    timeout: int,
    error_context: str,
) -> GitOpResult:
    result = await run_remote_git_op(ssh_key_path, hostname, request, timeout=timeout)
    if not result.ok:
        detail = result.stderr or result.stdout or "unknown error"
        raise RuntimeError(f"{error_context}: {detail}")
    return result


async def ensure_remote_git_server(
    ssh_key_path: Path,
    hostname: str,
    *,
    timeout: int = 10,
) -> None:
    await run_remote_git_checked(
        ssh_key_path,
        hostname,
        GitOpRequest.ping(),
        timeout=timeout,
        error_context=f"Failed to start git ops server on {hostname}",
    )
