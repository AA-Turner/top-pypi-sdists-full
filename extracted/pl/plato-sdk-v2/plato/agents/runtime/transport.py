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


class NFSTransport(Transport):
    """Transport via kernel NFSv4 mount from world VM.

    Exports the workspace path directly via kernel NFS with ``crossmnt`` so
    that FUSE sub-mounts (lazy DVC) are automatically traversed.  No loopback
    ext4, no bind mounts — the workspace directory is the NFS pseudo-root.
    """

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

        # Export the workspace path directly as the NFSv4 pseudo-root.
        # crossmnt: automatically traverse FUSE sub-mounts (lazy DVC).
        export_line = f"{self.path} *(rw,sync,fsid=0,crossmnt,no_subtree_check,all_squash,anonuid=1000,anongid=1000)"
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

    async def add_export(self, path: str, fsid: int) -> None:
        """Add an additional NFS export line for a workspace path.

        Raises RuntimeError if the path can't be NFS-exported (e.g. overlayfs).
        """
        await self._setup_workspace_path(path)
        export_line = f"{path} *(rw,sync,fsid={fsid},crossmnt,no_subtree_check,all_squash,anonuid=1000,anongid=1000)"
        exit_code, _, stderr = await run_local(
            f"printf '%s\\n' '{export_line}' >> /etc/exports",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to add NFS export for {path}: {stderr}")

        # Verify the export actually works
        exit_code, _, stderr = await run_local("exportfs -ra", timeout=10)
        if exit_code != 0:
            # Remove the bad export line and re-export
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
            f"chown 1000:1000 {path} 2>/dev/null; "
            f"chmod 1777 {path} 2>/dev/null; "
            f"setfacl -dm u:1000:rwx,g:1000:rwx {path} 2>/dev/null; "
            f"true",
            timeout=10,
        )
        logger.info(f"Workspace path ready: {path}")

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Mount the world VM's NFS export on an agent VM via SSH."""
        await self._setup_workspace_path(self.path)
        await run_local(
            f"setfacl -Rm u:1000:rwx,g:1000:rwx {self.path} 2>/dev/null; chown -R 1000:1000 {self.path}",
            timeout=120,
        )

        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common)",
            timeout=180,
        )

        remote = self.agent_mount_path
        nfs_src = f"{self.world_vm_ip}:{self.path}"
        mount_cmd = f"mkdir -p {remote} && mount -t nfs -o vers=3,soft,timeo=150,retrans=3,nolock {nfs_src} {remote}"
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
        """Ensure workspace directory exists."""
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> NFSTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        return NFSTransport(
            path,
            self.world_vm_ip,
            self.ssh_key_path,
            sub_mount,
        )
