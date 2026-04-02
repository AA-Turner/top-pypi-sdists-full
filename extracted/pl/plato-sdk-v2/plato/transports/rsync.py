"""Rsync-based transport helpers and implementation."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from plato.transports.base import Transport

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)


async def rsync_to(
    ssh_key_path: Path,
    local_path: Path,
    remote_path: str,
    hostname: str,
    chown: str | None = None,
    max_retries: int = 3,
    retry_delay: float = 5.0,
) -> None:
    """Rsync a directory to a remote VM."""
    ssh_cmd = f"ssh -i {ssh_key_path} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"

    cmd = [
        "rsync",
        "-az",
        "--delete",
        "--rsync-path",
        f"mkdir -p {remote_path} && rsync",
        "-e",
        ssh_cmd,
    ]
    if chown:
        cmd.extend(["--chown", chown])
    cmd.extend([f"{local_path}/", f"root@{hostname}:{remote_path}/"])

    last_error = ""
    for attempt in range(1, max_retries + 1):
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode == 0:
            return

        last_error = stderr.decode()
        if attempt < max_retries:
            logger.warning(
                f"rsync to VM failed (attempt {attempt}/{max_retries}), "
                f"retrying in {retry_delay}s: {last_error.strip()}"
            )
            await asyncio.sleep(retry_delay)

    raise RuntimeError(f"rsync to VM failed after {max_retries} attempts: {last_error}")


async def rsync_from(
    ssh_key_path: Path,
    remote_path: str,
    local_path: Path,
    hostname: str,
    max_retries: int = 3,
    retry_delay: float = 5.0,
) -> None:
    """Rsync a directory from a remote VM back to local."""
    ssh_cmd = f"ssh -i {ssh_key_path} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"

    local_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "rsync",
        "-az",
        "-e",
        ssh_cmd,
        f"root@{hostname}:{remote_path}/",
        f"{local_path}/",
    ]

    last_error = ""
    for attempt in range(1, max_retries + 1):
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode == 0:
            return

        last_error = stderr.decode()
        if attempt < max_retries:
            logger.warning(
                f"rsync from VM failed (attempt {attempt}/{max_retries}), "
                f"retrying in {retry_delay}s: {last_error.strip()}"
            )
            await asyncio.sleep(retry_delay)

    raise RuntimeError(f"rsync from VM failed after {max_retries} attempts: {last_error}")


class RsyncTransport(Transport):
    """Transport via rsync over SSH."""

    def __init__(self, path: str, ssh_key_path: Path, mount_path: str | None = None) -> None:
        self.path = path
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        self.configure_workspace(name=None, repo_root=None, tracked=False)
        self.configure_audit_scope(audit_run_id=None, audit_key=None)

    async def initialize(self) -> None:
        pass

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        workspace_path = Path(self.path)
        if not workspace_path.exists():
            logger.debug(f"Workspace path {self.path} does not exist, skipping rsync")
            return
        remote = self.agent_mount_path
        logger.debug(f"Syncing workspace: {self.path} -> {remote}")
        await rsync_to(
            self.ssh_key_path,
            workspace_path,
            remote,
            hostname,
            chown=None,
        )

    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        workspace_path = Path(self.path)
        remote = self.agent_mount_path
        logger.debug(f"Syncing workspace back: {remote} -> {self.path}")
        await rsync_from(
            self.ssh_key_path,
            remote,
            workspace_path,
            hostname,
        )

    def with_path(self, path: str) -> RsyncTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        transport = RsyncTransport(path, self.ssh_key_path, sub_mount)
        transport.configure_workspace(
            name=self.workspace_name,
            repo_root=self.workspace_repo_root,
            tracked=self.workspace_tracked,
        )
        transport.configure_audit_scope(
            audit_run_id=self.audit_run_id,
            audit_key=self.audit_key,
        )
        return transport
