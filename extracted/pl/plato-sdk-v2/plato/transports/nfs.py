"""Kernel NFS transport implementation."""

from __future__ import annotations

import asyncio
import logging
import shlex
import time as _time
from pathlib import Path
from typing import TYPE_CHECKING

from plato.transports.base import Transport, build_auditctl_commands
from plato.utils.subprocess import run_local, run_ssh

if TYPE_CHECKING:
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)

_MOUNT_MAX_ATTEMPTS = 3
_MOUNT_RETRY_DELAY_S = 5.0
_MOUNT_PER_ATTEMPT_TIMEOUT_S = 35  # `timeout 30 mount …` + small SSH overhead


def _is_transient_mount_failure(exit_code: int, stderr: str) -> bool:
    """Return True if a failed mount looks like a retryable transient (timeout, EIO).

    `timeout` exits 124 when it kills the child; mount.nfs exits 32 on most
    failures and prints a human reason on stderr. Connection/portmap timeouts
    are the only ones we want to retry — auth/permission failures are not."""
    if exit_code == 124:
        return True
    err = stderr.lower()
    transient_markers = (
        "connection timed out",
        "timed out",
        "no route to host",
        "connection refused",
        "portmap",
        "rpc: timed out",
    )
    return any(marker in err for marker in transient_markers)


class NFSTransport(Transport):
    """Transport via kernel NFS mount from world VM."""

    def __init__(
        self,
        path: str,
        world_vm_ip: str,
        ssh_key_path: Path,
        mount_path: str | None = None,
        readonly: bool = False,
        mount_options: str = "",
    ) -> None:
        self.path = path
        self.world_vm_ip = world_vm_ip
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        # Read-only workspaces are enforced at BOTH ends: the server export
        # line uses `ro` and the agent-side mount adds `-o ro`, so a
        # misconfigured client cannot write even if it drops the mount flag.
        self.readonly = readonly
        # Extra client-side mount options appended to the default -o string,
        # e.g. "sync" for write-through workspaces that another VM tails live.
        self.mount_options = mount_options

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

        perms = "ro" if self.readonly else "rw"
        export_line = f"{self.path} *({perms},sync,fsid=0,no_subtree_check,no_root_squash)"
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

    async def add_export(self, path: str, fsid: int, readonly: bool = False) -> None:
        """Add an additional NFS export line for a workspace path."""
        await self._setup_workspace_path(path)
        perms = "ro" if readonly else "rw"
        export_line = f"{path} *({perms},sync,fsid={fsid},no_subtree_check,no_root_squash)"
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
        """Mount the world VM's NFS export on an agent VM via SSH.

        The mount step is retried up to ``_MOUNT_MAX_ATTEMPTS`` times on
        transient connection-timeout failures (intermittent rpcbind/mountd
        races and overlay-network packet loss show up here). Each attempt is
        wrapped in `timeout 30 mount …` so it fails fast instead of waiting
        ~130s for the kernel's own retrans loop."""
        await self._setup_workspace_path(self.path)

        del agent_env
        remote = mount.agent_path
        nfs_src = f"{self.world_vm_ip}:{self.path}"

        # Step 1: install nfs-common and create the mountpoint. Idempotent;
        # only run once even if mount retries.
        prep_cmd = (
            "(which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common))"
            f" && mkdir -p {remote}"
        )
        exit_code, _, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            prep_cmd,
            timeout=120,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to prepare NFS mount on agent VM: {stderr}")

        # Step 2: mount with bounded per-attempt timeout and retries.
        ro_opt = ",ro" if self.readonly else ""
        extra_opt = f",{self.mount_options}" if self.mount_options else ""
        # Idempotent for reused VMs (runtime leases skip the pool reset that
        # used to unmount workspaces): an already-mounted path is success, not
        # a second stacked mount. A genuine mount failure still exits non-zero
        # so the retry loop below is unaffected.
        mount_cmd = (
            f"mountpoint -q {remote} || "
            f"timeout 30 mount -t nfs -o vers=3,hard,timeo=300,retrans=5,nolock,"
            f"rsize=32768,wsize=32768{ro_opt}{extra_opt} {nfs_src} {remote}"
        )
        t0 = _time.monotonic()
        last_err = ""
        for attempt in range(1, _MOUNT_MAX_ATTEMPTS + 1):
            logger.info(
                "NFSTransport.setup_agent: mounting %s -> %s on %s (attempt %d/%d)",
                nfs_src,
                remote,
                hostname,
                attempt,
                _MOUNT_MAX_ATTEMPTS,
            )
            exit_code, _, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                mount_cmd,
                timeout=_MOUNT_PER_ATTEMPT_TIMEOUT_S,
            )
            if exit_code == 0:
                break
            last_err = stderr.strip() or f"exit_code={exit_code}"
            if not _is_transient_mount_failure(exit_code, stderr):
                raise RuntimeError(f"Failed to mount NFS on agent VM: {last_err}")
            if attempt < _MOUNT_MAX_ATTEMPTS:
                logger.warning(
                    "NFS mount attempt %d/%d failed on %s (%s); retrying in %.1fs",
                    attempt,
                    _MOUNT_MAX_ATTEMPTS,
                    hostname,
                    last_err,
                    _MOUNT_RETRY_DELAY_S,
                )
                await asyncio.sleep(_MOUNT_RETRY_DELAY_S)
        else:
            raise RuntimeError(f"Failed to mount NFS on agent VM after {_MOUNT_MAX_ATTEMPTS} attempts: {last_err}")
        logger.info(
            "NFSTransport.setup_agent: mounted in %.1fs on %s (attempt %d)",
            _time.monotonic() - t0,
            hostname,
            attempt,
        )

        # Step 3: post-mount steps (mount info log + optional audit rules).
        post_parts = [f"echo \"NFS_MOUNT_INFO=$(mount | grep '{remote}')\""]
        audit_key = mount.audit_key
        tracked = mount.tracked
        if tracked and audit_key:
            post_parts.extend(build_auditctl_commands(remote, audit_key))

        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            " && ".join(post_parts),
            timeout=60,
        )
        post_ok = exit_code == 0
        if not post_ok:
            logger.warning(
                "NFS post-mount setup returned non-zero on %s: %s",
                hostname,
                stderr.strip(),
            )

        for line in stdout.splitlines():
            if line.startswith("NFS_MOUNT_INFO="):
                logger.info("NFS mounted on %s: %s", hostname, line[15:])
                break

        if tracked and audit_key:
            if post_ok:
                logger.info("Filesystem audit enabled on agent VM for %s (key=%s)", remote, audit_key)
            else:
                logger.warning(
                    "Filesystem audit may NOT be active on agent VM for %s (key=%s) — "
                    "post-mount auditctl setup failed; tool attribution will be incomplete",
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

    def with_path(
        self,
        path: str,
        readonly: bool | None = None,
        mount_options: str | None = None,
    ) -> NFSTransport:
        """Clone for a sub-path. ``readonly`` and ``mount_options`` INHERIT from
        this transport unless explicitly overridden — per-agent mount clones
        (mounts.py, base.py) call this without the flags, and dropping them
        would strip ``-o ro`` (or a workspace's write-through options) from the
        client mount, silently degrading enforcement to export-only."""
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        effective_readonly = self.readonly if readonly is None else readonly
        effective_options = self.mount_options if mount_options is None else mount_options
        return NFSTransport(
            path,
            self.world_vm_ip,
            self.ssh_key_path,
            sub_mount,
            readonly=effective_readonly,
            mount_options=effective_options,
        )
