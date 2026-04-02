"""SSHFS transport implementation."""

from __future__ import annotations

import asyncio
import logging
import shlex
from pathlib import Path
from typing import TYPE_CHECKING

from plato.transports.base import Transport
from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)


class SSHFSTransport(Transport):
    """Transport via SSHFS (FUSE over SSH) from world VM."""

    def __init__(
        self,
        path: str,
        world_vm_ip: str,
        ssh_key_path: Path,
        mount_path: str | None = None,
    ) -> None:
        self.path = path
        self.world_vm_ip = world_vm_ip
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        self.configure_workspace(name=None, repo_root=None, tracked=False)
        self.configure_audit_scope(audit_run_id=None, audit_key=None)

    async def initialize(self) -> None:
        """Ensure workspace directory exists and tune VM memory."""
        await self._setup_workspace_path(self.path)

        exit_code, total_kb_str, _ = await run_local(
            "awk '/MemTotal/{print $2}' /proc/meminfo",
            timeout=5,
        )
        total_kb = int(total_kb_str.strip()) if exit_code == 0 and total_kb_str.strip().isdigit() else 4194304
        total_mb = total_kb // 1024
        min_free_kb = max(131072, total_kb * 10 // 100)

        exit_code, stdout, stderr = await run_local(
            f"sysctl -w vm.min_free_kbytes={min_free_kb} && sysctl -w vm.vfs_cache_pressure=500",
            timeout=10,
        )
        if exit_code != 0:
            logger.warning("sysctl tuning failed (exit=%d): %s", exit_code, stderr.strip())
        else:
            logger.info("SSHFS memory tuning: total=%dMB min_free=%dMB", total_mb, min_free_kb // 1024)

        logger.info("SSHFS transport initialized: %s", self.path)

    async def _setup_workspace_path(self, path: str) -> None:
        exit_code, _, stderr = await run_local(f"mkdir -p {path}", timeout=10)
        if exit_code != 0:
            raise RuntimeError(f"Failed to create workspace path {path}: {stderr}")
        await run_local(
            f"chown 1000:1000 {path} 2>/dev/null; chmod 1777 {path} 2>/dev/null; true",
            timeout=10,
        )

    async def add_export(self, path: str, fsid: int) -> None:
        del fsid
        await self._setup_workspace_path(path)

    async def refresh_exports(self) -> None:
        """No-op for SSHFS."""

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Mount the world VM's workspace on an agent VM via SSHFS."""
        await self._setup_workspace_path(self.path)

        remote = self.agent_mount_path
        remote_quoted = shlex.quote(remote)
        agent_key_path = "/root/.ssh/world_key"

        ssh_cmd = (
            f"ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
        )
        proc = await asyncio.create_subprocess_exec(
            "rsync",
            "-e",
            ssh_cmd,
            str(self.ssh_key_path),
            f"root@{hostname}:{agent_key_path}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, rsync_err = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to copy SSH key to agent VM: {rsync_err.decode()}")

        parts = [
            "(which sshfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq sshfs))",
            "mkdir -p /root/.ssh && chmod 700 /root/.ssh",
            f"chmod 600 {agent_key_path}",
            f"mkdir -p {remote}",
            (
                f"sshfs -o allow_other,default_permissions,"
                f"reconnect,"
                f"ServerAliveInterval=15,ServerAliveCountMax=3,"
                f"cache=yes,cache_timeout=5,"
                f"IdentityFile={agent_key_path},"
                f"StrictHostKeyChecking=no,UserKnownHostsFile=/dev/null,LogLevel=ERROR "
                f"root@{self.world_vm_ip}:{self.path} {remote}"
            ),
            f"echo \"SSHFS_MOUNT_INFO=$(mount | grep '{remote}')\"",
        ]

        audit_key = self.audit_key
        if self.workspace_tracked and audit_key:
            audit_key_quoted = shlex.quote(audit_key)
            parts.extend(
                [
                    "(which auditctl > /dev/null 2>&1 || "
                    "(apt-get update -qq && apt-get install -y -qq auditd > /dev/null 2>&1))",
                    "(service auditd start 2>/dev/null || true)",
                    f"auditctl -a always,exit -F arch=b64 -F dir={remote_quoted} -F perm=rwa -k {audit_key_quoted}",
                    f"auditctl -a always,exit -F arch=b64 -S mkdir,mkdirat "
                    f"-F dir={remote_quoted} -k {audit_key_quoted}",
                ]
            )

        combined_cmd = " && ".join(parts)
        logger.info("Mounting SSHFS on agent VM %s: %s -> %s", hostname, self.world_vm_ip, remote)
        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            combined_cmd,
            timeout=180,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to mount SSHFS on agent VM: {stderr}")

        for line in stdout.splitlines():
            if line.startswith("SSHFS_MOUNT_INFO="):
                logger.info("SSHFS mounted on %s: %s", hostname, line[17:])
                break

        if self.workspace_tracked and audit_key:
            logger.info("Filesystem audit enabled on agent VM for %s (key=%s)", remote, audit_key)

    async def collect_audit_log(
        self,
        hostname: str,
        audit_key: str | None = None,
    ) -> str | None:
        """Collect filesystem audit log from agent VM."""
        try:
            key = audit_key or self.audit_key or "plato_workspace"
            exit_code, stdout, _ = await run_ssh(
                self.ssh_key_path,
                hostname,
                f"ausearch -if /var/log/audit/audit.log --format raw -k {shlex.quote(key)} 2>/dev/null || true",
                timeout=30,
            )
            if exit_code != 0 or not stdout.strip():
                return None
            return stdout
        except Exception:
            logger.warning("Failed to collect audit log from agent VM", exc_info=True)
            return None

    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        del agent_env, hostname

    async def prepare(self) -> None:
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> SSHFSTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        transport = SSHFSTransport(path, self.world_vm_ip, self.ssh_key_path, sub_mount)
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
