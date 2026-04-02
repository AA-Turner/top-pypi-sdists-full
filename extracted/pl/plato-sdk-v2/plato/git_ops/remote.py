"""Remote git operation helpers over SSH."""

from __future__ import annotations

from pathlib import Path

from plato.git_ops.client import RemoteGitClient
from plato.git_ops.models import GitOpRequest, GitOpResult

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
