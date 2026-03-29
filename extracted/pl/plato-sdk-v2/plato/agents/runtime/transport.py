"""Transport layer for sharing files between world and agent VMs (NFS, SSHFS, or rsync)."""

from __future__ import annotations

import asyncio
import logging
import shlex
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

        # Export the workspace path directly as the NFSv4 pseudo-root.
        # crossmnt: automatically traverse FUSE sub-mounts (lazy DVC).
        # sync: server acks writes only after disk flush. Slower (3s overhead per
        # write-heavy cycle) but stable — async causes NFS3ERR_IO under heavy
        # concurrent writes from 10+ agents even with sysctl memory caps.
        export_line = f"{self.path} *(rw,sync,fsid=0,crossmnt,no_subtree_check,no_root_squash)"
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
        export_line = f"{path} *(rw,sync,fsid={fsid},crossmnt,no_subtree_check,no_root_squash)"
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

        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common)",
            timeout=180,
        )

        remote = self.agent_mount_path
        nfs_src = f"{self.world_vm_ip}:{self.path}"
        # hard: retry indefinitely instead of returning EIO after retrans attempts.
        # rsize/wsize=32768: 32KB blocks minimize kernel buffer memory on the
        # NFS server. Code files are small — 32KB is plenty.
        # timeo=300: 30s initial timeout (deciseconds), retrans=5: more retries.
        mount_cmd = (
            f"mkdir -p {remote} && "
            f"mount -t nfs -o vers=3,hard,timeo=300,retrans=5,nolock,"
            f"rsize=32768,wsize=32768 {nfs_src} {remote}"
        )
        logger.info("Mounting NFS on agent VM %s: %s", hostname, mount_cmd)
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            mount_cmd,
            timeout=120,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to mount NFS on agent VM: {stderr}")

        # Verify mount options
        _, mount_info, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"mount | grep '{remote}'",
            timeout=5,
        )
        logger.info("NFS mounted on %s: %s", hostname, mount_info.strip())

        # Set up filesystem audit on agent VM (non-fatal)
        audit_key = self.audit_key
        if not self.workspace_tracked or not audit_key:
            logger.debug(
                "Skipping filesystem audit setup for workspace %s (tracked=%s, key=%s)",
                remote,
                self.workspace_tracked,
                audit_key,
            )
            return
        try:
            # Use syscall-based rules instead of -w (file watch), because
            # -w watches inodes which don't work on NFS mount points.
            remote_quoted = shlex.quote(remote)
            audit_key_quoted = shlex.quote(audit_key)
            audit_setup_cmd = (
                "which auditctl > /dev/null 2>&1 || "
                "(apt-get update -qq && apt-get install -y -qq auditd > /dev/null 2>&1) && "
                "service auditd start 2>/dev/null; "
                # Path-based rule for file read/write/attribute operations.
                # Tool-level attribution depends on read events as well as writes.
                f"auditctl -a always,exit -F arch=b64 -F dir={remote_quoted} "
                f"-F perm=rwa -k {audit_key_quoted}; "
                # Explicit syscall rule for mkdir — not reliably caught by
                # -p wa over NFS since the RPC doesn't map to a write on the
                # parent directory in the audit framework.
                f"auditctl -a always,exit -F arch=b64 -S mkdir,mkdirat "
                f"-F dir={remote_quoted} -k {audit_key_quoted}"
            )
            exit_code, _, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                audit_setup_cmd,
                timeout=120,
            )
            if exit_code != 0:
                logger.warning("Filesystem audit setup failed on agent VM: %s", stderr.strip())
            else:
                logger.info(
                    "Filesystem audit enabled on agent VM for %s (key=%s)",
                    remote,
                    audit_key,
                )
        except Exception:
            logger.warning("Failed to set up filesystem audit on agent VM", exc_info=True)

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

        # Install sshfs on agent VM
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "which sshfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq sshfs)",
            timeout=180,
        )

        remote = self.agent_mount_path

        # Copy the SSH private key to the agent VM so it can authenticate
        # back to the world VM for the SSHFS mount.
        # Security note: agents already run as root and the session SSH key is
        # added to all VMs via add_ssh_key() — this doesn't grant new access.
        agent_key_path = "/root/.ssh/world_key"
        await run_ssh(
            self.ssh_key_path,
            hostname,
            "mkdir -p /root/.ssh && chmod 700 /root/.ssh",
            timeout=10,
        )
        # Use rsync to copy the key (run_ssh can't pipe file content easily)
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

        sshfs_cmd = (
            f"mkdir -p {remote} && "
            f"sshfs -o allow_other,default_permissions,"
            f"reconnect,"
            f"ServerAliveInterval=15,ServerAliveCountMax=3,"
            f"cache=yes,cache_timeout=5,"
            f"IdentityFile={agent_key_path},"
            f"StrictHostKeyChecking=no,UserKnownHostsFile=/dev/null,LogLevel=ERROR "
            f"root@{self.world_vm_ip}:{self.path} {remote}"
        )
        logger.info("Mounting SSHFS on agent VM %s: %s", hostname, sshfs_cmd)
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            sshfs_cmd,
            timeout=60,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to mount SSHFS on agent VM: {stderr}")

        # Verify mount
        _, mount_info, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"mount | grep '{remote}'",
            timeout=5,
        )
        logger.info("SSHFS mounted on %s: %s", hostname, mount_info.strip())

        # Set up filesystem audit on agent VM (non-fatal)
        audit_key = self.audit_key
        if not self.workspace_tracked or not audit_key:
            return
        try:
            remote_quoted = shlex.quote(remote)
            audit_key_quoted = shlex.quote(audit_key)
            audit_setup_cmd = (
                "which auditctl > /dev/null 2>&1 || "
                "(apt-get update -qq && apt-get install -y -qq auditd > /dev/null 2>&1) && "
                "service auditd start 2>/dev/null; "
                f"auditctl -a always,exit -F arch=b64 -F dir={remote_quoted} "
                f"-F perm=rwa -k {audit_key_quoted}; "
                f"auditctl -a always,exit -F arch=b64 -S mkdir,mkdirat "
                f"-F dir={remote_quoted} -k {audit_key_quoted}"
            )
            exit_code, _, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                audit_setup_cmd,
                timeout=120,
            )
            if exit_code != 0:
                logger.warning("Filesystem audit setup failed on agent VM: %s", stderr.strip())
            else:
                logger.info(
                    "Filesystem audit enabled on agent VM for %s (key=%s)",
                    remote,
                    audit_key,
                )
        except Exception:
            logger.warning("Failed to set up filesystem audit on agent VM", exc_info=True)

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
