"""Transport layer for sharing files between world and agent VMs (NFS or rsync)."""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Rsync helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Transport ABC and implementations
# ---------------------------------------------------------------------------


class Transport(ABC):
    """Abstract transport for sharing files between world VM and agent VMs."""

    path: str
    mount_path: str | None = None

    @abstractmethod
    async def initialize(self) -> None:
        """One-time setup on the world VM (e.g., start NFS server)."""

    @abstractmethod
    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Make workspace available on an agent VM."""

    @abstractmethod
    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        """Sync changes back from agent VM to world VM."""

    @abstractmethod
    def with_path(self, path: str) -> Transport:
        """Return a copy of this transport with a different path."""

    @property
    def agent_mount_path(self) -> str:
        """Path where this workspace appears on the agent VM."""
        return self.mount_path or self.path

    async def prepare(self) -> None:
        """Prepare this workspace's path on the world VM (e.g., NFS bind mount)."""

    def mount_at(self, remote_path: str) -> Transport:
        """Return a copy that mounts at a custom path on the agent VM."""
        t = self.with_path(self.path)
        t.mount_path = remote_path
        return t


class RsyncTransport(Transport):
    """Transport via rsync over SSH."""

    def __init__(self, path: str, ssh_key_path: Path, mount_path: str | None = None) -> None:
        self.path = path
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path

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
        return RsyncTransport(path, self.ssh_key_path, sub_mount)


# ---------------------------------------------------------------------------
# NFS Transport
# ---------------------------------------------------------------------------

NFS_ROOT = "/srv/nfs"


class NFSTransport(Transport):
    """Transport via NFSv4 mount from world VM.

    All workspace data lives on a loopback ext4 filesystem mounted at
    /srv/nfs (the NFSv4 pseudo-root). This uses real disk instead of tmpfs
    to avoid eating RAM, while still being exportable via NFS (overlayfs
    cannot be exported). The world VM's workspace path (e.g. /workspace)
    is bind-mounted to /srv/nfs/workspace so both world code and NFS clients
    see the same data.
    """

    def __init__(self, path: str, world_vm_ip: str, ssh_key_path: Path, mount_path: str | None = None) -> None:
        self.path = path
        self.world_vm_ip = world_vm_ip
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path

    async def initialize(self) -> None:
        """Set up NFS server with disk-backed workspace on the world VM."""
        await run_local(
            "which exportfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-kernel-server)",
            timeout=120,
        )

        loop_file = "/var/lib/nfs-workspace.img"
        exit_code, _, _ = await run_local(f"mountpoint -q {NFS_ROOT}", timeout=5)
        if exit_code != 0:
            _, df_out, _ = await run_local("df --output=avail -B1 / | tail -1", timeout=5)
            avail_bytes = int(df_out.strip())
            loop_size = int(avail_bytes * 0.8)
            loop_size = max(loop_size, 1 * 1024**3)
            loop_size = min(loop_size, 50 * 1024**3)
            loop_size_mb = loop_size // (1024 * 1024)

            exit_code, _, stderr = await run_local(
                f"mkdir -p {NFS_ROOT} && "
                f"truncate -s {loop_size_mb}M {loop_file} && "
                f"mkfs.ext4 -q -F {loop_file} && "
                f"mount -o loop {loop_file} {NFS_ROOT}",
                timeout=60,
            )
            if exit_code != 0:
                logger.warning("Loopback mount failed (%s), falling back to tmpfs", stderr.strip())
                exit_code, _, stderr = await run_local(
                    f"mkdir -p {NFS_ROOT} && mount -t tmpfs tmpfs {NFS_ROOT}",
                    timeout=10,
                )
                if exit_code != 0:
                    raise RuntimeError(f"Failed to create workspace filesystem at {NFS_ROOT}: {stderr}")
            else:
                logger.info("Workspace: loopback ext4 (%dMB) mounted at %s", loop_size_mb, NFS_ROOT)

        await run_local(f"chown 1000:1000 {NFS_ROOT} && chmod 1777 {NFS_ROOT}", timeout=5)
        await run_local(
            f"setfacl -Rdm u:1000:rwx,g:1000:rwx {NFS_ROOT} 2>/dev/null; "
            f"setfacl -Rm u:1000:rwx,g:1000:rwx {NFS_ROOT} 2>/dev/null; "
            f"true",
            timeout=30,
        )

        await self._setup_workspace_path(self.path)

        exit_code, _, stderr = await run_local(
            f"printf '%s\\n' '{NFS_ROOT} *(rw,sync,fsid=0,no_subtree_check,all_squash,anonuid=1000,anongid=1000)' > /etc/exports",
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

        exit_code, _, stderr = await run_local(
            "systemctl start rpcbind && "
            "systemctl reset-failed proc-fs-nfsd.mount 2>/dev/null; "
            "exportfs -ra && "
            "systemctl start nfs-kernel-server",
            timeout=30,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to start NFS server: {stderr}")

        exit_code, exports, _ = await run_local("exportfs -s", timeout=5)
        logger.info(f"NFS server running. Exports:\n{exports.strip()}")

    async def _setup_workspace_path(self, path: str) -> None:
        """Create workspace dir on the NFS filesystem and bind-mount the world path to it."""
        nfs_path = f"{NFS_ROOT}{path}"
        exit_code, _, stderr = await run_local(
            f"mkdir -p {nfs_path} && mkdir -p {path} && mountpoint -q {path} || mount --bind {nfs_path} {path}",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to setup workspace path {path}: {stderr}")
        await run_local(
            f"chown 1000:1000 {nfs_path} 2>/dev/null; "
            f"chmod 1777 {nfs_path} 2>/dev/null; "
            f"setfacl -dm u:1000:rwx,g:1000:rwx {nfs_path} 2>/dev/null; "
            f"true",
            timeout=10,
        )
        logger.info(f"Workspace {path} -> {nfs_path} (bind mount)")

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Mount the world VM's NFS export on an agent VM via SSH."""
        await self._setup_workspace_path(self.path)

        nfs_path = f"{NFS_ROOT}{self.path}"
        await run_local(
            f"setfacl -Rm u:1000:rwx,g:1000:rwx {nfs_path} 2>/dev/null; chown -R 1000:1000 {nfs_path}",
            timeout=120,
        )

        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common)",
            timeout=60,
        )

        remote = self.agent_mount_path
        mount_cmd = f"mkdir -p {remote} && mount -t nfs4 -o soft,timeo=30 {self.world_vm_ip}:{self.path} {remote}"
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            mount_cmd,
            timeout=30,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to mount NFS on agent VM: {stderr}")

        logger.debug(f"NFS mounted {self.path} -> {remote} on agent VM ({hostname})")

    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        """NFS writes are immediate — nothing to do."""
        pass

    async def prepare(self) -> None:
        """Set up the NFS bind mount for this workspace path."""
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> NFSTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        return NFSTransport(path, self.world_vm_ip, self.ssh_key_path, sub_mount)
