"""Kernel NFS transport implementation."""

from __future__ import annotations

import logging
import shlex
import time as _time
from pathlib import Path
from typing import TYPE_CHECKING

from plato.transports.base import Transport
from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)


class NFSTransport(Transport):
    """Transport via kernel NFS mount from world VM."""

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

    async def initialize(self) -> None:
        """Install kernel NFS server, write exports, and start the service."""
        await run_local(
            "which exportfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-kernel-server)",
            timeout=120,
        )
        await self._setup_workspace_path(self.path)

        exit_code, total_kb_str, _ = await run_local(
            "awk '/MemTotal/{print $2}' /proc/meminfo",
            timeout=5,
        )
        total_kb = int(total_kb_str.strip()) if exit_code == 0 and total_kb_str.strip().isdigit() else 4194304
        total_mb = total_kb // 1024

        min_free_kb = max(131072, total_kb * 10 // 100)
        dirty_bytes = max(33554432, (total_kb * 1024) // 32)
        dirty_bg_bytes = dirty_bytes // 2
        logger.debug(
            "Total RAM: %dMB, min_free=%dMB, dirty=%dMB, dirty_bg=%dMB",
            total_mb,
            min_free_kb // 1024,
            dirty_bytes // 1048576,
            dirty_bg_bytes // 1048576,
        )

        exit_code, stdout, stderr = await run_local(
            f"sysctl -w vm.min_free_kbytes={min_free_kb} && "
            f"sysctl -w vm.dirty_bytes={dirty_bytes} && "
            f"sysctl -w vm.dirty_background_bytes={dirty_bg_bytes} && "
            "sysctl -w vm.dirty_expire_centisecs=500 && "
            "sysctl -w vm.vfs_cache_pressure=500",
            timeout=10,
        )
        if exit_code != 0:
            logger.warning("sysctl tuning failed (exit=%d): %s", exit_code, stderr.strip())
        else:
            logger.debug("VM memory tuning applied: %s", stdout.strip())

        export_line = f"{self.path} *(rw,sync,fsid=0,no_subtree_check,no_root_squash)"
        exit_code, _, stderr = await run_local(
            f"printf '%s\\n' '{export_line}' > /etc/exports",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to configure NFS exports: {stderr}")

        exit_code, _, stderr = await run_local(
            "modprobe nfsd 2>/dev/null; "
            "mkdir -p /proc/fs/nfsd && "
            "mountpoint -q /proc/fs/nfsd || mount -t nfsd nfsd /proc/fs/nfsd",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to mount nfsd filesystem: {stderr}")

        nfsd_threads = max(8, min(32, total_mb // 256))
        logger.debug("Setting nfsd threads: %d (for %dMB RAM)", nfsd_threads, total_mb)
        await run_local(
            "if [ -f /etc/default/nfs-kernel-server ]; then "
            f"  sed -i 's/^RPCNFSDCOUNT=.*/RPCNFSDCOUNT={nfsd_threads}/' /etc/default/nfs-kernel-server || true; "
            f"  grep -q RPCNFSDCOUNT /etc/default/nfs-kernel-server || "
            f"    echo 'RPCNFSDCOUNT={nfsd_threads}' >> /etc/default/nfs-kernel-server; "
            "fi",
            timeout=10,
        )

        exit_code, _, stderr = await run_local(
            "systemctl start rpcbind && "
            "systemctl reset-failed proc-fs-nfsd.mount 2>/dev/null; "
            "exportfs -ra && "
            "systemctl start nfs-kernel-server && "
            f"rpc.nfsd {nfsd_threads} 2>/dev/null; true",
            timeout=30,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to start NFS server: {stderr}")

        _, nfsd_threads_actual, _ = await run_local(
            "cat /proc/fs/nfsd/threads 2>/dev/null || rpcinfo -p 2>/dev/null | grep nfs | head -1",
            timeout=5,
        )
        logger.debug("nfsd threads: %s", nfsd_threads_actual.strip())

        _, exports, _ = await run_local("exportfs -s", timeout=5)
        logger.debug(f"NFS server running. Exports:\n{exports.strip()}")

    async def add_export(self, path: str, fsid: int) -> None:
        """Add an additional NFS export line for a workspace path."""
        await self._setup_workspace_path(path)
        export_line = f"{path} *(rw,sync,fsid={fsid},no_subtree_check,no_root_squash)"
        exit_code, _, stderr = await run_local(
            f"printf '%s\\n' '{export_line}' >> /etc/exports",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to add NFS export for {path}: {stderr}")

        exit_code, _, stderr = await run_local("exportfs -ra", timeout=10)
        if exit_code != 0:
            await run_local(f"sed -i '\\|^{path} |d' /etc/exports", timeout=5)
            await run_local("exportfs -ra", timeout=10)
            raise RuntimeError(f"Path {path} does not support NFS export: {stderr}")

    async def refresh_exports(self) -> None:
        """Re-export after FUSE mounts change so NFS picks up new sub-mounts."""
        exit_code, _, stderr = await run_local("exportfs -ra", timeout=10)
        if exit_code != 0:
            logger.warning("exportfs -ra failed: %s", stderr.strip())
        else:
            logger.debug("NFS exports refreshed")

    async def _setup_workspace_path(self, path: str) -> None:
        """Create workspace directory with correct ownership."""
        exit_code, _, stderr = await run_local(f"mkdir -p {path}", timeout=10)
        if exit_code != 0:
            raise RuntimeError(f"Failed to create workspace path {path}: {stderr}")
        await run_local(
            f"chown 1000:1000 {path} 2>/dev/null; chmod 1777 {path} 2>/dev/null; true",
            timeout=10,
        )
        logger.debug(f"Workspace path ready: {path}")

    async def setup_agent(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        """Mount the world VM's NFS export on an agent VM via SSH."""
        await self._setup_workspace_path(self.path)

        del agent_env
        remote = mount.agent_path
        remote_quoted = shlex.quote(remote)
        nfs_src = f"{self.world_vm_ip}:{self.path}"

        parts = [
            "(which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common))",
            f"mkdir -p {remote}",
            f"mount -t nfs -o vers=3,hard,timeo=300,retrans=5,nolock,rsize=32768,wsize=32768 {nfs_src} {remote}",
            f"echo \"NFS_MOUNT_INFO=$(mount | grep '{remote}')\"",
        ]

        audit_key = mount.audit_key
        tracked = mount.tracked
        if tracked and audit_key:
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
        t0 = _time.monotonic()
        logger.info("NFSTransport.setup_agent: mounting %s -> %s on %s", nfs_src, remote, hostname)
        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            combined_cmd,
            timeout=180,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to mount NFS on agent VM: {stderr}")
        logger.info("NFSTransport.setup_agent: mounted in %.1fs on %s", _time.monotonic() - t0, hostname)

        for line in stdout.splitlines():
            if line.startswith("NFS_MOUNT_INFO="):
                logger.info("NFS mounted on %s: %s", hostname, line[15:])
                break

        if tracked and audit_key:
            logger.info("Filesystem audit enabled on agent VM for %s (key=%s)", remote, audit_key)

    async def collect_audit_log(
        self,
        hostname: str,
        audit_key: str | None = None,
    ) -> str | None:
        """Collect filesystem audit log from agent VM."""
        try:
            key = audit_key or "plato_workspace"
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

    async def sync_back(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        """NFS writes are immediate."""
        del agent_env, hostname, mount

    async def prepare(self) -> None:
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> NFSTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        return NFSTransport(path, self.world_vm_ip, self.ssh_key_path, sub_mount)
