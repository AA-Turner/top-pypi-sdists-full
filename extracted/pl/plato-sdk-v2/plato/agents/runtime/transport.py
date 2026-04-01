"""Transport layer for sharing files between world and agent VMs (NFS, SSHFS, git, or rsync)."""

from __future__ import annotations

import asyncio
import logging
import shlex
import time as _time
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.worlds.config import GitTransportConfig, MergeAgentConfig

logger = logging.getLogger(__name__)


class GitPushConflict(RuntimeError):
    """Raised when a git push loses a race and the caller should resolve it centrally."""

    def __init__(self, *, commit_sha: str, conflict_ref: str) -> None:
        super().__init__(f"Git push conflict for commit {commit_sha}")
        self.commit_sha = commit_sha
        self.conflict_ref = conflict_ref


@dataclass(slots=True)
class GitPublishedRef:
    """Published hidden ref produced by a git transport sync."""

    commit_sha: str
    ref: str


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
    workspace_name: str | None = None
    workspace_repo_root: str | None = None
    workspace_tracked: bool = False
    audit_run_id: str | None = None
    audit_key: str | None = None

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

    def configure_workspace(
        self,
        *,
        name: str | None,
        repo_root: str | None,
        tracked: bool,
    ) -> None:
        """Attach workspace metadata to the transport for downstream integration."""
        self.workspace_name = name
        self.workspace_repo_root = repo_root
        self.workspace_tracked = tracked

    def configure_audit_scope(
        self,
        *,
        audit_run_id: str | None,
        audit_key: str | None,
    ) -> None:
        """Attach per-run audit scope metadata."""
        self.audit_run_id = audit_run_id
        self.audit_key = audit_key

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


# ---------------------------------------------------------------------------
# NFS Transport
# ---------------------------------------------------------------------------


class NFSTransport(Transport):
    """Transport via kernel NFS mount from world VM.

    Each workspace is exported independently with its own fsid.
    No pseudo-root or crossmnt — avoids ESTALE when FUSE sub-mounts
    have different inode lifetimes.
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
        self.configure_workspace(name=None, repo_root=None, tracked=False)
        self.configure_audit_scope(audit_run_id=None, audit_key=None)

    async def initialize(self) -> None:
        """Install kernel NFS server, write exports, and start the service."""
        await run_local(
            "which exportfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-kernel-server)",
            timeout=120,
        )
        await self._setup_workspace_path(self.path)

        # Tune VM memory to prevent NFS page cache from exhausting free memory.
        # All values scale with total RAM. See: docs/chronos/nfs-oom-analysis.md
        exit_code, total_kb_str, _ = await run_local(
            "awk '/MemTotal/{print $2}' /proc/meminfo",
            timeout=5,
        )
        total_kb = int(total_kb_str.strip()) if exit_code == 0 and total_kb_str.strip().isdigit() else 4194304
        total_mb = total_kb // 1024

        # Scale tuning parameters with VM size
        min_free_kb = max(131072, total_kb * 10 // 100)  # 10% of RAM, min 128MB
        dirty_bytes = max(33554432, (total_kb * 1024) // 32)  # 3% of RAM, min 32MB
        dirty_bg_bytes = dirty_bytes // 2
        logger.info(
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
            logger.info("VM memory tuning applied: %s", stdout.strip())

        # Each workspace is exported independently with its own fsid.
        # No pseudo-root or crossmnt — avoids ESTALE when FUSE sub-mounts
        # have different inode lifetimes (e.g. empty vs populated workspaces).
        # sync: server acks writes only after disk flush. Slower (3s overhead per
        # write-heavy cycle) but stable — async causes NFS3ERR_IO under heavy
        # concurrent writes from 10+ agents even with sysctl memory caps.
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

        # Scale nfsd threads conservatively: 1 per 256MB, min 8, max 32.
        # Each thread consumes kernel memory for socket buffers. On small VMs
        # (2GB) extra threads just waste RAM waiting on sync disk I/O.
        nfsd_threads = max(8, min(32, total_mb // 256))
        logger.info("Setting nfsd threads: %d (for %dMB RAM)", nfsd_threads, total_mb)
        exit_code, _, _ = await run_local(
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
            # Ensure thread count takes effect even if config file wasn't read
            f"rpc.nfsd {nfsd_threads} 2>/dev/null; true",
            timeout=30,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to start NFS server: {stderr}")

        # Verify nfsd thread count
        exit_code, nfsd_threads_actual, _ = await run_local(
            "cat /proc/fs/nfsd/threads 2>/dev/null || rpcinfo -p 2>/dev/null | grep nfs | head -1",
            timeout=5,
        )
        logger.info("nfsd threads: %s", nfsd_threads_actual.strip())

        exit_code, exports, _ = await run_local("exportfs -s", timeout=5)
        logger.info(f"NFS server running. Exports:\n{exports.strip()}")

    async def add_export(self, path: str, fsid: int) -> None:
        """Add an additional NFS export line for a workspace path.

        Raises RuntimeError if the path can't be NFS-exported (e.g. overlayfs).
        """
        await self._setup_workspace_path(path)
        export_line = f"{path} *(rw,sync,fsid={fsid},no_subtree_check,no_root_squash)"
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
            f"chown 1000:1000 {path} 2>/dev/null; chmod 1777 {path} 2>/dev/null; true",
            timeout=10,
        )
        logger.info(f"Workspace path ready: {path}")

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Mount the world VM's NFS export on an agent VM via SSH."""
        await self._setup_workspace_path(self.path)

        remote = self.agent_mount_path
        remote_quoted = shlex.quote(remote)
        nfs_src = f"{self.world_vm_ip}:{self.path}"

        # Single SSH command: install nfs-common if needed, mount, verify, and set up audit.
        # Subshells for || patterns prevent them from swallowing earlier && failures.
        # NFS options: hard (retry indefinitely), rsize/wsize=32KB (small files),
        # timeo=300 (30s initial timeout), retrans=5, nolock.
        parts = [
            "(which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common))",
            f"mkdir -p {remote}",
            (f"mount -t nfs -o vers=3,hard,timeo=300,retrans=5,nolock,rsize=32768,wsize=32768 {nfs_src} {remote}"),
            f"echo \"NFS_MOUNT_INFO=$(mount | grep '{remote}')\"",
        ]

        # Append audit setup if workspace is tracked
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

        # Extract mount info from output
        for line in stdout.splitlines():
            if line.startswith("NFS_MOUNT_INFO="):
                logger.info("NFS mounted on %s: %s", hostname, line[15:])
                break

        if self.workspace_tracked and audit_key:
            logger.info(
                "Filesystem audit enabled on agent VM for %s (key=%s)",
                remote,
                audit_key,
            )

    async def collect_audit_log(
        self,
        hostname: str,
        audit_key: str | None = None,
    ) -> str | None:
        """Collect filesystem audit log from agent VM.

        Returns ``ausearch --format raw`` output, or None if empty/failed.
        """
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
        """NFS writes are immediate — nothing to do."""
        pass

    async def prepare(self) -> None:
        """Ensure workspace directory exists."""
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> NFSTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        transport = NFSTransport(
            path,
            self.world_vm_ip,
            self.ssh_key_path,
            sub_mount,
        )
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


# ---------------------------------------------------------------------------
# SSHFS Transport
# ---------------------------------------------------------------------------


class SSHFSTransport(Transport):
    """Transport via SSHFS (FUSE over SSH) from world VM.

    Each agent VM mounts the world's workspace via SSHFS.  The world VM runs
    only ``sftp-server`` (part of openssh, already installed) — no kernel
    filesystem server, no page cache explosion, no nfsd threads.

    Memory footprint on the world VM is ~5-10 MB per connected agent (one
    sftp-server process each), compared to ~1.5 GB for kernel NFS.

    FUSE sub-mounts (e.g. plato-fuse for lazy DVC) are traversed transparently
    because sftp-server does normal ``open()/read()`` syscalls on the local
    filesystem.
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
        self.configure_workspace(name=None, repo_root=None, tracked=False)
        self.configure_audit_scope(audit_run_id=None, audit_key=None)

    async def initialize(self) -> None:
        """Ensure workspace directory exists and tune VM memory.

        SSHFS doesn't run a kernel filesystem server, but sftp-server reads
        still get cached in page cache. On small VMs this can exhaust free
        memory, so we apply the same min_free_kbytes reservation.
        """
        await self._setup_workspace_path(self.path)

        # Tune page cache — sftp-server reads are cached by the kernel
        exit_code, total_kb_str, _ = await run_local(
            "awk '/MemTotal/{print $2}' /proc/meminfo",
            timeout=5,
        )
        total_kb = int(total_kb_str.strip()) if exit_code == 0 and total_kb_str.strip().isdigit() else 4194304
        total_mb = total_kb // 1024
        min_free_kb = max(131072, total_kb * 10 // 100)  # 10% of RAM, min 128MB

        exit_code, stdout, stderr = await run_local(
            f"sysctl -w vm.min_free_kbytes={min_free_kb} && sysctl -w vm.vfs_cache_pressure=500",
            timeout=10,
        )
        if exit_code != 0:
            logger.warning("sysctl tuning failed (exit=%d): %s", exit_code, stderr.strip())
        else:
            logger.info(
                "SSHFS memory tuning: total=%dMB min_free=%dMB",
                total_mb,
                min_free_kb // 1024,
            )

        logger.info("SSHFS transport initialized: %s", self.path)

    async def _setup_workspace_path(self, path: str) -> None:
        """Create workspace directory with correct ownership."""
        exit_code, _, stderr = await run_local(f"mkdir -p {path}", timeout=10)
        if exit_code != 0:
            raise RuntimeError(f"Failed to create workspace path {path}: {stderr}")
        await run_local(
            f"chown 1000:1000 {path} 2>/dev/null; chmod 1777 {path} 2>/dev/null; true",
            timeout=10,
        )

    async def add_export(self, path: str, fsid: int) -> None:
        """No-op for exports — just ensure path exists."""
        await self._setup_workspace_path(path)

    async def refresh_exports(self) -> None:
        """No-op — SSHFS traverses FUSE sub-mounts automatically."""

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Mount the world VM's workspace on an agent VM via SSHFS."""
        await self._setup_workspace_path(self.path)

        remote = self.agent_mount_path
        remote_quoted = shlex.quote(remote)
        agent_key_path = "/root/.ssh/world_key"

        # Copy the SSH private key to the agent VM so it can authenticate
        # back to the world VM for the SSHFS mount.
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

        # Single SSH call: install sshfs, chmod key, mkdir, mount, verify, and set up audit.
        # Subshells for || patterns prevent them from swallowing earlier && failures.
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

        # Append audit setup if workspace is tracked
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
            logger.info(
                "Filesystem audit enabled on agent VM for %s (key=%s)",
                remote,
                audit_key,
            )

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
        """SSHFS writes are immediate — nothing to do."""

    async def prepare(self) -> None:
        """Ensure workspace directory exists."""
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> SSHFSTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        transport = SSHFSTransport(
            path,
            self.world_vm_ip,
            self.ssh_key_path,
            sub_mount,
        )
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


# ---------------------------------------------------------------------------
# Git Transport
# ---------------------------------------------------------------------------


class GitTransport(Transport):
    """Transport via git clone/push over SSH.

    The world VM hosts a bare git repo at ``{path}/.git-bare``.  Agents clone
    over SSH on setup, work on an isolated local copy, and push changes back
    via ``sync_back()``.  A ``post-receive`` hook keeps the world VM working
    tree at ``{path}`` up to date after each push.

    Concurrent pushes are handled with configurable merge strategies:
    ``"theirs"`` (accept incoming), ``"ours"`` (keep existing), or ``"agent"``
    (invoke an LLM merge agent to resolve conflicts).
    """

    def __init__(
        self,
        path: str,
        world_vm_ip: str,
        ssh_key_path: Path,
        mount_path: str | None = None,
        git_config: GitTransportConfig | None = None,
        raise_on_conflict: bool = False,
        publish_ref_prefix: str | None = None,
    ) -> None:
        self.path = path
        self.world_vm_ip = world_vm_ip
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        self._bare_repo_path = f"{path}/.git-bare"
        self._raise_on_conflict = raise_on_conflict
        self._publish_ref_prefix = publish_ref_prefix
        self._publish_ref_exact = False
        self._published_ref: GitPublishedRef | None = None
        self._checkout_base_ref: str | None = None
        self._checkout_branch_name: str | None = None

        # Lazy import to avoid circular dependency at module level
        from plato.worlds.config import GitTransportConfig as _GTC

        self._git_config = git_config or _GTC()
        # Callback: (hostname, ssh_key_path, workspace_path, conflicted_files) -> None
        self._merge_resolver: Callable[[str, Path, str, list[str]], Awaitable[None]] | None = None
        self._sync_lock = asyncio.Lock() if self._git_config.serialize_sync else None
        self.configure_workspace(name=None, repo_root=None, tracked=False)
        self.configure_audit_scope(audit_run_id=None, audit_key=None)

    @property
    def bare_repo_path(self) -> str:
        """Path to the world's bare repository backing this workspace."""
        return self._bare_repo_path

    @property
    def merge_config(self) -> GitTransportConfig:
        """Git transport configuration for this workspace."""
        return self._git_config

    @property
    def sync_lock(self) -> asyncio.Lock | None:
        """Lock guarding serialized sync/push operations for this workspace."""
        return self._sync_lock

    @property
    def raise_on_conflict(self) -> bool:
        """Whether to surface push conflicts instead of resolving them on the agent VM."""
        return self._raise_on_conflict

    @property
    def publish_ref_prefix(self) -> str | None:
        """Hidden ref prefix used for publish-only orchestrated syncs."""
        return self._publish_ref_prefix

    @property
    def published_ref(self) -> GitPublishedRef | None:
        """Last hidden ref published by this transport instance."""
        return self._published_ref

    @property
    def checkout_base_ref(self) -> str | None:
        """Pinned ref or SHA to check out after cloning on the agent VM."""
        return self._checkout_base_ref

    def set_raise_on_conflict(self, enabled: bool) -> None:
        """Enable or disable conflict reporting mode for orchestrated runs."""
        self._raise_on_conflict = enabled

    def set_publish_ref_prefix(self, prefix: str | None, *, exact: bool = False) -> None:
        """Enable publish-only sync mode for this transport instance.

        Args:
            prefix: Ref prefix (e.g. ``refs/plato/tasks/slug`` or ``refs/heads/pr/slug``).
            exact: When True, publish to exactly *prefix* instead of appending
                ``/{sha}``.  Use this to create named branches (e.g. ``pr/slug``).
        """
        self._publish_ref_prefix = prefix
        self._publish_ref_exact = exact
        self._published_ref = None

    def set_checkout_base_ref(self, ref: str | None, *, branch_name: str | None = None) -> None:
        """Pin agent clones to a specific base ref/SHA after cloning."""
        self._checkout_base_ref = ref
        self._checkout_branch_name = branch_name

    def set_merge_resolver(
        self,
        resolver: Callable[[str, Path, str, list[str]], Awaitable[None]],
    ) -> None:
        """Set a callback for agent-based merge conflict resolution.

        The resolver receives ``(hostname, ssh_key_path, workspace_path,
        conflicted_files)``.  The hostname and ssh_key_path allow the
        resolver to pull conflicted files from the agent VM, run a merge
        agent, and push resolved files back.  The resolver must stage and
        commit the resolution on the agent VM.
        """
        self._merge_resolver = resolver

    # -- helpers -------------------------------------------------------------

    async def _setup_workspace_path(self, path: str) -> None:
        """Create workspace directory."""
        quoted = shlex.quote(path)
        exit_code, _, stderr = await run_local(f"mkdir -p {quoted}", timeout=10)
        if exit_code != 0:
            raise RuntimeError(f"Failed to create workspace path {path}: {stderr}")

    async def _init_bare_repo(self, workspace_path: str, bare_path: str) -> None:
        """Initialize a bare repo and seed it from the workspace contents."""
        # Install git if needed (TODO: pre-install in plato-world-base Dockerfile)
        await run_local(
            "which git > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq git)",
            timeout=120,
        )

        # Mark all directories as safe (world VM is single-tenant, ownership
        # may differ between root and uid 1000 due to workspace setup)
        await run_local(
            "git config --global --add safe.directory '*'",
            timeout=10,
        )

        # Init bare repo with explicit main branch.
        # Remove any stale bare repo left by DVC checkpoint restore to avoid
        # corrupt packfile errors.
        q_bare = shlex.quote(bare_path)
        q_ws = shlex.quote(workspace_path)
        exit_code, _, stderr = await run_local(
            f"rm -rf {q_bare} && "
            f"git init --bare -b main {q_bare} && "
            # Store received objects as loose files instead of packfiles.
            # On FUSE-backed workspaces, packfile verification fails due to
            # read-after-write inconsistency.  Loose objects also deduplicate
            # better under DVC (which hashes files individually).
            f"git -C {q_bare} config transfer.unpackLimit 99999",
            timeout=30,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to init bare repo at {bare_path}: {stderr}")

        # Write default .gitignore from WorkspaceMarker.DEFAULT_DVCIGNORE
        from plato.markers import WorkspaceMarker

        gitignore_lines = list(WorkspaceMarker.DEFAULT_DVCIGNORE) + [".git-bare"]
        gitignore_content = "\n".join(gitignore_lines) + "\n"
        q_gitignore = shlex.quote(f"{workspace_path}/.gitignore")
        exit_code, _, stderr = await run_local(
            f"cat > {q_gitignore} << 'GITIGNORE_EOF'\n{gitignore_content}GITIGNORE_EOF",
            timeout=10,
        )
        if exit_code != 0:
            logger.warning("Failed to write .gitignore: %s", stderr.strip())

        # Seed bare repo with initial commit from workspace contents.
        # Clean any stale .git first to avoid re-init issues on resume.
        await run_local(f"rm -rf {q_ws}/.git", timeout=10)

        exit_code, _, stderr = await run_local(
            f"cd {q_ws} && "
            "rm -rf .git && "
            "git init -b main && "
            "git add -A && "
            "git -c user.email=plato@plato.dev -c user.name=Plato "
            "commit -m 'Initial workspace state' --allow-empty && "
            # Verify files were staged — fail loudly if workspace is empty
            "{ git log --oneline -1 --stat | grep -q 'file' || "
            "  echo 'WARNING: no files staged in initial commit' >&2; } && "
            f"git remote add origin {q_bare} && "
            "git push origin main && "
            # Remove the temporary .git — the bare repo is the source of truth
            f"rm -rf {q_ws}/.git",
            timeout=self._git_config.seed_timeout,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to seed bare repo: {stderr}")

        # Install post-receive hook to update working tree on push.
        # flock prevents concurrent checkouts from corrupting the working tree.
        lock_name = bare_path.replace("/", "_")
        hook_content = (
            "#!/bin/bash\n"
            f"exec 200>/tmp/git-transport-{lock_name}.lock\n"
            "flock 200\n"
            "git config --global --add safe.directory '*' 2>/dev/null\n"
            f"GIT_WORK_TREE={workspace_path} git checkout -f main\n"
        )
        q_hook = shlex.quote(f"{bare_path}/hooks/post-receive")
        exit_code, _, stderr = await run_local(
            f"cat > {q_hook} << 'HOOK_EOF'\n{hook_content}HOOK_EOF\nchmod +x {q_hook}",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to install post-receive hook: {stderr}")

        logger.info("Git bare repo initialized at %s (workspace: %s)", bare_path, workspace_path)

    async def _copy_ssh_key_to_agent(self, hostname: str) -> str:
        """Copy the session SSH key to the agent VM. Returns the remote key path."""
        agent_key_path = "/root/.ssh/world_key"
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "mkdir -p /root/.ssh && chmod 700 /root/.ssh",
            timeout=10,
        )
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
        await run_ssh(
            self.ssh_key_path,
            hostname,
            f"chmod 600 {agent_key_path}",
            timeout=10,
        )
        return agent_key_path

    async def _head_commit_sha(self, workspace_path: str, hostname: str) -> str:
        """Return the current HEAD commit SHA from an agent clone."""
        return await self._git_rev_parse(workspace_path, hostname, "HEAD")

    async def _git_rev_parse(self, workspace_path: str, hostname: str, ref: str) -> str:
        """Resolve a git ref inside an agent clone."""
        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && git rev-parse {shlex.quote(ref)}",
            timeout=10,
        )
        if exit_code != 0 or not stdout.strip():
            raise RuntimeError(f"Failed to resolve git ref {ref} on agent {hostname}: {stderr.strip()}")
        return stdout.strip()

    async def _git_output(self, workspace_path: str, hostname: str, command: str, timeout: int = 10) -> str:
        """Run a git subcommand inside an agent clone and return stdout."""
        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && {command}",
            timeout=timeout,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to run '{command}' on agent {hostname}: {stderr.strip()}")
        return stdout.strip()

    async def _auto_commit_changes(self, workspace_path: str, hostname: str, commit_message: str) -> None:
        """Stage and auto-commit any agent changes, raising on commit failures."""
        quoted_message = shlex.quote(commit_message)
        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && git add -A && (git diff --cached --quiet || git commit -m {quoted_message})",
            timeout=60,
        )
        logger.info(
            "GitTransport auto-commit hostname=%s exit_code=%s stdout=%s stderr=%s",
            hostname,
            exit_code,
            stdout.strip(),
            stderr.strip(),
        )
        if exit_code != 0:
            status = await self._git_output(workspace_path, hostname, "git status --short", timeout=10)
            raise RuntimeError(
                f"Auto-commit failed on agent {hostname}: {stderr.strip() or stdout.strip()} (status={status})"
            )

    async def _publish_conflict_ref(self, workspace_path: str, hostname: str, commit_sha: str) -> str:
        """Publish the conflicting commit under a hidden ref so the world VM can fetch it."""
        conflict_ref = f"refs/plato/conflicts/{commit_sha}"
        await self._push_head_to_ref(workspace_path, hostname, conflict_ref)
        return conflict_ref

    async def _push_head_to_ref(self, workspace_path: str, hostname: str, ref: str) -> None:
        """Push the current HEAD to an arbitrary ref on the world bare repo."""
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && git push --force origin HEAD:{ref}",
            timeout=60,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to push ref {ref} from agent {hostname}: {stderr.strip()}")

    @staticmethod
    def _is_push_conflict(stderr: str) -> bool:
        """Return True when git reports a non-fast-forward style push race."""
        lowered = stderr.lower()
        return "non-fast-forward" in lowered or "[rejected]" in lowered or "fetch first" in lowered

    # -- Transport interface -------------------------------------------------

    async def initialize(self) -> None:
        """Set up bare git repo on the world VM and seed it from workspace contents."""
        await self._setup_workspace_path(self.path)
        await self._init_bare_repo(self.path, self._bare_repo_path)

    async def update_bare_repo(self, message: str = "Update workspace") -> None:
        """Commit current workspace contents to the bare repo.

        Call this after writing files to the workspace directory so that
        agents will see them when they clone.
        """
        msg = shlex.quote(message)
        q_ws = shlex.quote(self.path)
        q_bare = shlex.quote(self._bare_repo_path)
        exit_code, _, stderr = await run_local(
            f"cd {q_ws} && "
            "git init -b main && "
            "git add -A && "
            f"git -c user.email=plato@plato.dev -c user.name=Plato "
            f"commit -m {msg} --allow-empty && "
            f"git push {q_bare} main --force && "
            f"rm -rf {q_ws}/.git",
            timeout=60,
        )
        if exit_code != 0:
            logger.warning("Failed to update bare repo: %s", stderr.strip())

    async def setup_agent(self, agent_env: Environment, hostname: str) -> None:
        """Clone the workspace repo onto the agent VM."""
        t0 = _time.monotonic()
        # Install git on agent VM
        logger.info("GitTransport.setup_agent: installing git on %s", hostname)
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which git > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq git)",
            timeout=180,
        )
        logger.info("GitTransport.setup_agent: git installed on %s (%.1fs)", hostname, _time.monotonic() - t0)

        # Copy SSH key and configure SSH for git-over-SSH back to world VM
        t1 = _time.monotonic()
        logger.info("GitTransport.setup_agent: copying SSH key to %s", hostname)
        agent_key_path = await self._copy_ssh_key_to_agent(hostname)
        ssh_config = (
            f"Host world-git\n"
            f"    HostName {self.world_vm_ip}\n"
            f"    User root\n"
            f"    IdentityFile {agent_key_path}\n"
            f"    StrictHostKeyChecking no\n"
            f"    UserKnownHostsFile /dev/null\n"
            f"    LogLevel ERROR\n"
        )
        await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cat > /root/.ssh/config << 'SSHCFG'\n{ssh_config}SSHCFG",
            timeout=10,
        )
        logger.info("GitTransport.setup_agent: SSH key configured on %s (%.1fs)", hostname, _time.monotonic() - t1)

        # Clone bare repo to agent mount path
        remote = self.agent_mount_path
        t2 = _time.monotonic()
        logger.info(
            "GitTransport.setup_agent: cloning %s -> %s on %s",
            self._bare_repo_path,
            remote,
            hostname,
        )
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            "git config --global --add safe.directory '*' && "
            f"rm -rf {remote} && "
            f"git clone world-git:{self._bare_repo_path} {remote} && "
            f"cd {remote} && "
            f"git config user.email agent@plato.dev && "
            f"git config user.name 'Plato Agent'"
            + (
                " && "
                f"git checkout -B {shlex.quote(self._checkout_branch_name or 'plato-task')} "
                f"{shlex.quote(self._checkout_base_ref)}"
                if self._checkout_base_ref is not None
                else ""
            ),
            timeout=120,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to clone git repo on agent VM: {stderr}")

        logger.info(
            "GitTransport.setup_agent: done on %s (clone=%.1fs, total=%.1fs): %s -> %s",
            hostname,
            _time.monotonic() - t2,
            _time.monotonic() - t0,
            self._bare_repo_path,
            remote,
        )

    async def sync_back(self, agent_env: Environment, hostname: str) -> None:
        """Commit and push agent changes back to the world's bare repo.

        When ``serialize_sync`` is enabled (default), concurrent calls are
        queued so only one agent pushes at a time — avoiding thundering-herd
        retries when many agents finish simultaneously.
        """
        logger.info(
            "GitTransport.sync_back hostname=%s publish_ref_prefix=%s transport_id=%s",
            hostname,
            self._publish_ref_prefix,
            id(self),
        )
        if self._publish_ref_prefix:
            await self._publish_sync_back_impl(agent_env, hostname)
            return
        if self._sync_lock:
            async with self._sync_lock:
                await self._sync_back_impl(agent_env, hostname)
        else:
            await self._sync_back_impl(agent_env, hostname)

    async def _sync_back_impl(self, agent_env: Environment, hostname: str) -> None:
        """Inner sync_back implementation."""
        self._published_ref = None
        cfg = self._git_config
        remote = self.agent_mount_path

        # Auto-commit if configured
        if cfg.commit_on_sync:
            await self._auto_commit_changes(remote, hostname, cfg.auto_commit_message)

        # Check if there's anything to push
        exit_code, stdout, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {remote} && git diff --quiet origin/main..HEAD && echo NOOP || echo PUSH",
            timeout=10,
        )
        if stdout.strip() == "NOOP":
            logger.debug("No changes to push from agent %s", hostname)
            return

        # Try push with retries for conflict resolution
        merge_cfg = cfg.merge_agent
        for attempt in range(1, merge_cfg.max_retries + 1):
            exit_code, _, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                f"cd {remote} && git push origin main",
                timeout=60,
            )
            if exit_code == 0:
                logger.info("Git push succeeded from agent %s (attempt %d)", hostname, attempt)
                return

            logger.warning(
                "Git push failed from agent %s (attempt %d/%d): %s",
                hostname,
                attempt,
                merge_cfg.max_retries,
                stderr.strip(),
            )

            if self._raise_on_conflict and self._is_push_conflict(stderr):
                await run_ssh(
                    self.ssh_key_path,
                    hostname,
                    f"cd {remote} && git fetch origin",
                    timeout=30,
                )
                commit_sha = await self._head_commit_sha(remote, hostname)
                conflict_ref = await self._publish_conflict_ref(remote, hostname, commit_sha)
                raise GitPushConflict(commit_sha=commit_sha, conflict_ref=conflict_ref)

            if attempt == merge_cfg.max_retries:
                break

            # Resolve based on strategy
            resolved = await self._resolve_and_retry(agent_env, hostname, remote, merge_cfg)
            if resolved:
                logger.info("Git conflict resolved for agent %s without another retry push", hostname)
                return

        raise RuntimeError(f"Git push failed from agent {hostname} after {merge_cfg.max_retries} attempts")

    async def _publish_sync_back_impl(self, agent_env: Environment, hostname: str) -> None:
        """Commit and publish agent changes to a hidden ref instead of pushing main."""
        del agent_env
        self._published_ref = None
        cfg = self._git_config
        remote = self.agent_mount_path

        if cfg.commit_on_sync:
            await self._auto_commit_changes(remote, hostname, cfg.auto_commit_message)

        head_sha = await self._git_rev_parse(remote, hostname, "HEAD")
        compare_ref = self._checkout_base_ref or "origin/main"
        compare_sha = await self._git_rev_parse(remote, hostname, compare_ref)
        status = await self._git_output(remote, hostname, "git status --short", timeout=10)
        ahead_behind = await self._git_output(
            remote,
            hostname,
            f"git rev-list --left-right --count {shlex.quote(compare_ref)}...HEAD",
            timeout=10,
        )
        logger.info(
            "GitTransport publish state hostname=%s head=%s compare_ref=%s compare_sha=%s status=%s ahead_behind=%s",
            hostname,
            head_sha,
            compare_ref,
            compare_sha,
            status or "<clean>",
            ahead_behind,
        )

        if head_sha == compare_sha:
            if status:
                raise RuntimeError(
                    f"Agent {hostname} has uncommitted changes after sync but HEAD still matches {compare_ref}: {status}"
                )
            logger.info("No committed changes to publish from agent %s", hostname)
            return

        if not self._publish_ref_prefix:
            raise RuntimeError("publish_ref_prefix must be set for publish-only sync mode")

        published_ref = (
            self._publish_ref_prefix if self._publish_ref_exact else f"{self._publish_ref_prefix}/{head_sha}"
        )
        logger.info("Publishing agent %s commit %s to hidden ref %s", hostname, head_sha, published_ref)

        retries = max(1, cfg.merge_agent.max_retries)
        for attempt in range(1, retries + 1):
            try:
                await self._push_head_to_ref(remote, hostname, published_ref)
                self._published_ref = GitPublishedRef(commit_sha=head_sha, ref=published_ref)
                logger.info("Published agent %s commit %s to %s", hostname, head_sha, published_ref)
                return
            except RuntimeError:
                if attempt == retries:
                    raise
                logger.warning(
                    "Publishing hidden ref failed from agent %s (attempt %d/%d)",
                    hostname,
                    attempt,
                    retries,
                    exc_info=True,
                )

    async def _resolve_and_retry(
        self,
        agent_env: Environment,
        hostname: str,
        workspace_path: str,
        merge_cfg: MergeAgentConfig,
    ) -> bool:
        """Fetch remote changes and resolve conflicts based on the configured strategy."""
        if merge_cfg.strategy == "theirs":
            # Rebase with -X ours: during rebase, "ours" means the upstream
            # (remote) side, so this auto-resolves conflicts in favor of remote.
            exit_code, _, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                f"cd {workspace_path} && git fetch origin && git rebase -X ours origin/main",
                timeout=60,
            )
            if exit_code != 0:
                # Rebase still failed — abort and accept theirs entirely
                logger.warning("Rebase failed, accepting theirs: %s", stderr.strip())
                await run_ssh(
                    self.ssh_key_path,
                    hostname,
                    f"cd {workspace_path} && "
                    "git rebase --abort 2>/dev/null; "
                    "git fetch origin && "
                    "git reset --hard origin/main",
                    timeout=30,
                )
            return False

        if merge_cfg.strategy == "ours":
            # Keep the agent's local commit and overwrite remote main.
            exit_code, _, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                f"cd {workspace_path} && git fetch origin && git push --force origin HEAD:main",
                timeout=60,
            )
            if exit_code != 0:
                raise RuntimeError(f"Failed to force-push local changes for agent {hostname}: {stderr.strip()}")
            return True

        # strategy == "agent": try auto-merge, invoke agent on conflicts
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && git fetch origin && git merge origin/main -m 'Merge remote changes'",
            timeout=60,
        )
        if exit_code == 0:
            return False  # Auto-merge succeeded

        # Conflicts exist — resolve them
        await self._resolve_merge_conflicts(agent_env, hostname, workspace_path, merge_cfg)
        return False

    async def _resolve_merge_conflicts(
        self,
        agent_env: Environment,
        hostname: str,
        workspace_path: str,
        merge_cfg: MergeAgentConfig,
    ) -> None:
        """Resolve git merge conflicts, either automatically or via a merge agent."""
        # Get list of conflicted files
        _, stdout, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && git diff --name-only --diff-filter=U",
            timeout=10,
        )
        conflicted_files = [f for f in stdout.strip().split("\n") if f]
        logger.info("Merge conflicts in %d files: %s", len(conflicted_files), conflicted_files)

        if not self._merge_resolver:
            # No merge resolver set — fall back to accept-theirs
            logger.warning("No merge resolver configured, resolving conflicts with 'accept theirs'")
            await self._accept_theirs(hostname, workspace_path, "Auto-resolved conflicts (accept theirs)")
            return

        # Invoke the merge resolver callback (typically spawns a proper agent via the world)
        logger.info("Invoking merge resolver for %d conflicts", len(conflicted_files))
        try:
            await self._merge_resolver(hostname, self.ssh_key_path, workspace_path, conflicted_files)
        except Exception:
            logger.warning("Merge resolver failed, falling back to accept-theirs", exc_info=True)
            await self._accept_theirs(hostname, workspace_path, "Auto-resolved conflicts (agent failed, accept theirs)")
            return

        # Verify no remaining conflicts
        exit_code, remaining, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && git diff --name-only --diff-filter=U",
            timeout=10,
        )
        if remaining.strip():
            logger.warning(
                "Merge resolver left unresolved conflicts: %s — falling back to accept-theirs",
                remaining.strip(),
            )
            await self._accept_theirs(hostname, workspace_path, "Resolved merge conflicts (with fallback)")

    async def _accept_theirs(self, hostname: str, workspace_path: str, message: str) -> None:
        """Resolve all conflicts by accepting the remote version."""
        await run_ssh(
            self.ssh_key_path,
            hostname,
            f"cd {workspace_path} && "
            "git checkout --theirs . && "
            "git add -A && "
            "git -c user.email=plato@plato.dev -c user.name=Plato "
            f"commit -m {shlex.quote(message)}",
            timeout=30,
        )

    async def add_export(self, path: str, fsid: int) -> None:
        """Initialize an additional bare repo for another workspace."""
        await self._setup_workspace_path(path)
        bare_path = f"{path}/.git-bare"
        await self._init_bare_repo(path, bare_path)

    async def refresh_exports(self) -> None:
        """No-op for git transport — each repo is independent."""

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

    async def prepare(self) -> None:
        """Ensure workspace directory exists."""
        await self._setup_workspace_path(self.path)

    def with_path(self, path: str) -> GitTransport:
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        transport = GitTransport(
            path,
            self.world_vm_ip,
            self.ssh_key_path,
            sub_mount,
            self._git_config,
            self._raise_on_conflict,
            self._publish_ref_prefix,
        )
        transport._merge_resolver = self._merge_resolver
        transport._sync_lock = self._sync_lock
        transport._published_ref = None
        transport._checkout_base_ref = self._checkout_base_ref
        transport._checkout_branch_name = self._checkout_branch_name
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
