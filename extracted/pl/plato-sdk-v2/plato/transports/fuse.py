"""Direct per-agent-VM plato-fuse transport for read-only dataset workspaces.

The NFS transport funnels every agent's dataset reads through the world VM's
single-threaded fuse loop and adds a fixed ~26 ms network round-trip per
metadata op. This transport instead launches ``plato-fuse`` ON the agent VM
itself: each agent gets a private lazy-hydrating S3 mount of the dataset's
immutable manifest, so metadata ops are local (µs-grade), directory
enumeration never fans out into per-entry NFS LOOKUPs, and one agent's load
cannot degrade the others. Datasets are immutable refs, so there is no
cross-VM coherence concern — writable/shared workspaces must stay on
coherent transports (NFS/git/rsync).

Setup per agent VM (all idempotent):

1. Ensure fuse3 userspace tools.
2. Ensure the ``plato-fuse`` binary: reuse one already on the VM unless the
   world runs with a ``PLATO_FUSE_BINARY`` override, otherwise push the
   world's resolved binary (PATH / override / S3 download) over SSH. The
   chosen source is logged.
3. Probe the binary's ``--capabilities`` and push the gzipped fuse worker
   config: a ~1 KB manifest-by-reference config when the binary can fetch
   the manifest from S3 itself (``manifest-ref`` capability), else the full
   inline manifest (~30 MB gz for an 835k-file dataset). Both carry the S3
   config with STS credentials and a credential-refresh block. Then launch
   ``plato-fuse`` detached, waiting for the mountpoint to appear.
4. For read-only workspaces, remount the mountpoint ``ro`` at the VFS level
   so writes fail loudly with EROFS instead of landing in the (discarded)
   local overlay.

The hydration cache lands on the agent VM's local disk under
``/tmp/plato-lazy-cache/agent/`` and is wiped by the warm-pool reset between
runs.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import shlex
import time as _time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING

from plato.transports.base import Transport
from plato.utils.fuse_binary import (
    ENSURE_FUSE3_COMMAND,
    PLATO_FUSE_INSTALL_PATH,
    ensure_plato_fuse,
)
from plato.utils.subprocess import run_ssh, scp_content_to_vm

if TYPE_CHECKING:
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)

# builder(mountpoint, cache_dir, manifest_by_ref) -> gzipped fuse worker
# config.json bytes. manifest_by_ref may only be True when the remote binary
# advertises the "manifest-ref" capability.
FuseConfigBuilder = Callable[[str, str, bool], Awaitable[bytes]]

AGENT_FUSE_STATE_DIR = "/tmp/plato-fuse-agent"
AGENT_FUSE_CACHE_ROOT = "/tmp/plato-lazy-cache/agent"

_MOUNT_WAIT_S = 180
_CONFIG_SCP_TIMEOUT_S = 600

# Cache of local plato-fuse binary md5 keyed by (path, mtime, size) so the
# ~15 MB binary is hashed once per process, not once per agent VM.
_binary_md5_cache: dict[tuple[str, float, int], str] = {}


def _local_binary_md5(path: str) -> str:
    stat = os.stat(path)
    key = (path, stat.st_mtime, stat.st_size)
    cached = _binary_md5_cache.get(key)
    if cached is not None:
        return cached
    digest = hashlib.md5()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    md5 = digest.hexdigest()
    _binary_md5_cache[key] = md5
    return md5


def _sanitize_mount_name(agent_path: str) -> str:
    return agent_path.strip("/").replace("/", "__") or "root"


class FuseDirectTransport(Transport):
    """Transport that lazy-mounts an immutable dataset manifest per agent VM."""

    def __init__(
        self,
        path: str,
        ssh_key_path: Path,
        config_builder: FuseConfigBuilder,
        *,
        mount_path: str | None = None,
        workspace_name: str = "",
        readonly: bool = True,
    ) -> None:
        self.path = path
        self.ssh_key_path = ssh_key_path
        self.mount_path = mount_path
        self.workspace_name = workspace_name
        self._config_builder = config_builder
        # Read-only is enforced on the agent VM via `mount -o remount,ro`:
        # the fuse overlay would silently discard writes anyway (it is local
        # scratch, never committed), but EROFS keeps misuse loud.
        self.readonly = readonly

    async def initialize(self) -> None:
        """No world-side server to start — each agent VM mounts independently."""

    async def setup_agent(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        """Launch a private plato-fuse mount of the dataset on the agent VM."""
        del agent_env
        t0 = _time.monotonic()
        remote = mount.agent_path
        name = _sanitize_mount_name(remote)
        cache_dir = f"{AGENT_FUSE_CACHE_ROOT}/{name}"
        config_gz = f"{AGENT_FUSE_STATE_DIR}/{name}.json.gz"
        config_json = f"{AGENT_FUSE_STATE_DIR}/{name}.json"
        log_path = f"{AGENT_FUSE_STATE_DIR}/{name}.log"

        # Prep dirs/fuse3 and resolve the plato-fuse binary concurrently —
        # both are independent. The fuse3 install must fail the prep loudly
        # (its own output is redirected to /dev/null): chained with `;` a
        # failed install would be masked by mkdir's exit 0 and only surface
        # ~3 minutes later as an opaque mount-wait timeout. The config build
        # comes AFTER the binary is known: its shape depends on whether the
        # remote binary can fetch the manifest from S3 itself
        # (--capabilities probe), which shrinks the per-agent push from
        # ~30 MB gz to ~1 KB for large datasets.
        prep_cmd = (
            f'({ENSURE_FUSE3_COMMAND}) || {{ echo "fuse3 userspace tools install failed" >&2; exit 1; }}; '
            f"mkdir -p {shlex.quote(remote)} {shlex.quote(cache_dir)} {AGENT_FUSE_STATE_DIR}"
        )
        (prep_code, _, prep_err), binary = await asyncio.gather(
            run_ssh(self.ssh_key_path, hostname, prep_cmd, timeout=180),
            self._ensure_remote_binary(hostname),
        )
        if prep_code != 0:
            raise RuntimeError(f"Failed to prepare fuse mount dirs/fuse3 on agent VM {hostname}: {prep_err.strip()}")

        manifest_by_ref = "manifest-ref" in await self._probe_capabilities(hostname, binary)
        config_bytes = await self._config_builder(remote, cache_dir, manifest_by_ref)

        await scp_content_to_vm(
            self.ssh_key_path,
            hostname,
            config_gz,
            config_bytes,
            timeout=_CONFIG_SCP_TIMEOUT_S,
        )

        pid_file = f"{AGENT_FUSE_STATE_DIR}/{name}.pid"
        start_cmd = self._build_start_command(
            binary=binary,
            remote=remote,
            config_gz=config_gz,
            config_json=config_json,
            log_path=log_path,
            pid_file=pid_file,
        )
        exit_code, start_out, start_err = await run_ssh(
            self.ssh_key_path,
            hostname,
            start_cmd,
            timeout=120,
        )
        if exit_code != 0:
            raise RuntimeError(
                f"Failed to start plato-fuse for {remote} on agent VM {hostname}: "
                f"{start_err.strip() or start_out.strip() or f'exit_code={exit_code}'}"
            )

        already = "FUSE_ALREADY_MOUNTED" in start_out
        if not already:
            wait_cmd = self._build_wait_command(remote=remote, log_path=log_path, pid_file=pid_file)
            exit_code, stdout, stderr = await run_ssh(
                self.ssh_key_path,
                hostname,
                wait_cmd,
                timeout=_MOUNT_WAIT_S + 120,
            )
            if exit_code != 0:
                raise RuntimeError(
                    f"plato-fuse mount at {remote} failed on agent VM {hostname}: "
                    f"{stderr.strip() or stdout.strip() or f'exit_code={exit_code}'}"
                )

        if self.readonly:
            # -i (no mount helpers) is required: plain `mount -o remount` on an
            # fstype-fuse entry delegates to mount.fuse, which tries to exec
            # the mount source ("lazydvc") as a program and fails with 127.
            ro_code, _, ro_err = await run_ssh(
                self.ssh_key_path,
                hostname,
                f"mount -i -o remount,ro {shlex.quote(remote)}",
                timeout=30,
            )
            if ro_code != 0:
                # Non-fatal: the overlay is local scratch that is never
                # committed, so data integrity does not depend on EROFS —
                # only loud misuse detection does.
                logger.warning(
                    "Could not remount %s read-only on %s (writes will land in the discarded overlay): %s",
                    remote,
                    hostname,
                    ro_err.strip(),
                )

        logger.info(
            "FuseDirectTransport: %s at %s on %s in %.1fs (config %.2f MB gz, manifest %s, workspace=%s)",
            "reused live mount" if already else "mounted",
            remote,
            hostname,
            _time.monotonic() - t0,
            len(config_bytes) / (1024 * 1024),
            "by-ref" if manifest_by_ref else "inline",
            self.workspace_name,
        )

    async def _probe_capabilities(self, hostname: str, binary: str) -> frozenset[str]:
        """Feature probe of the remote plato-fuse binary.

        New binaries print one capability token per line for
        ``--capabilities``; older ones treat the flag as a config path and
        exit non-zero, which probes as no capabilities — the transport then
        falls back to inline-manifest configs, so no binary rollout
        coordination is needed.
        """
        exit_code, stdout, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"{shlex.quote(binary)} --capabilities 2>/dev/null",
            timeout=30,
        )
        if exit_code != 0:
            return frozenset()
        return frozenset(line.strip() for line in stdout.splitlines() if line.strip())

    async def _ensure_remote_binary(self, hostname: str) -> str:
        """Ensure a plato-fuse binary on the agent VM; return its path.

        Reuses a binary already on the VM (image-baked) unless the world runs
        with a ``PLATO_FUSE_BINARY`` override, in which case the override is
        pushed (md5-gated) so dev/test binaries win over stale baked ones.
        Otherwise the world's resolved binary (PATH / S3 download) is pushed.
        Logs which source the agent VM ends up using.
        """
        probe_cmd = 'command -v plato-fuse 2>/dev/null || echo ""'
        _, probe_out, _ = await run_ssh(self.ssh_key_path, hostname, probe_cmd, timeout=30)
        remote_existing = probe_out.strip().splitlines()[-1].strip() if probe_out.strip() else ""

        override_active = bool(os.environ.get("PLATO_FUSE_BINARY"))
        if remote_existing and not override_active:
            logger.info("plato-fuse on agent VM %s: using preinstalled %s", hostname, remote_existing)
            return remote_existing

        local_binary, source = await ensure_plato_fuse()
        local_md5 = await asyncio.to_thread(_local_binary_md5, local_binary)

        target = remote_existing or PLATO_FUSE_INSTALL_PATH
        _, md5_out, _ = await run_ssh(
            self.ssh_key_path,
            hostname,
            f"md5sum {shlex.quote(target)} 2>/dev/null | awk '{{print $1}}'",
            timeout=30,
        )
        if md5_out.strip() == local_md5:
            logger.info(
                "plato-fuse on agent VM %s: %s already matches local %s binary (md5 %s)",
                hostname,
                target,
                source,
                local_md5,
            )
            return target

        binary_bytes = await asyncio.to_thread(Path(local_binary).read_bytes)
        staging = f"{target}.tmp-{local_md5[:8]}"
        await scp_content_to_vm(
            self.ssh_key_path,
            hostname,
            staging,
            binary_bytes,
            timeout=_CONFIG_SCP_TIMEOUT_S,
        )
        # Atomic rename so a concurrent workspace setup on the same VM never
        # sees (or execs) a half-written binary.
        install_cmd = f"chmod 755 {shlex.quote(staging)} && mv -f {shlex.quote(staging)} {shlex.quote(target)}"
        exit_code, _, stderr = await run_ssh(self.ssh_key_path, hostname, install_cmd, timeout=30)
        if exit_code != 0:
            raise RuntimeError(f"Failed to install plato-fuse on agent VM {hostname}: {stderr.strip()}")
        logger.info(
            "plato-fuse on agent VM %s: pushed local %s binary (%s, %.1f MB, md5 %s) to %s",
            hostname,
            source,
            local_binary,
            len(binary_bytes) / (1024 * 1024),
            local_md5,
            target,
        )
        return target

    @staticmethod
    def _build_start_command(
        *,
        binary: str,
        remote: str,
        config_gz: str,
        config_json: str,
        log_path: str,
        pid_file: str,
    ) -> str:
        """Shell script that launches plato-fuse detached (does not wait).

        Idempotent: a live mount at the target is reused (warm-pool resets
        unmount between runs; within a run the mount list is deduped anyway),
        and a stale/dead mountpoint is lazily unmounted first. The liveness
        probe is wrapped in ``timeout`` because ``mountpoint``/``stat`` on a
        wedged fuse mountpoint can block in D-state indefinitely.

        The daemon spawn is wrapped in a subshell ``( setsid … & )`` with all
        three FDs redirected — SSH keeps the session channel open as long as
        any descendant is attached to it, so a bare ``nohup … &`` blocks the
        calling ``run_ssh`` until its timeout (same gotcha, and same fix, as
        the remote chromium spawn in ``plato.v2.async_.cdp_bridge``).
        """
        q_remote = shlex.quote(remote)
        q_binary = shlex.quote(binary)
        q_gz = shlex.quote(config_gz)
        q_json = shlex.quote(config_json)
        q_log = shlex.quote(log_path)
        q_pid = shlex.quote(pid_file)
        return (
            f"if timeout 10 mountpoint -q {q_remote}; then echo FUSE_ALREADY_MOUNTED; exit 0; fi; "
            f"fusermount3 -uz {q_remote} 2>/dev/null; "
            f"gunzip -cf {q_gz} > {q_json} || exit 1; "
            f"rm -f {q_gz} {q_log}; "
            f'( setsid {q_binary} {q_json} </dev/null > {q_log} 2>&1 & echo "$!" > {q_pid} ); '
            f'echo "FUSE_STARTED pid=$(cat {q_pid})"'
        )

    @staticmethod
    def _build_wait_command(*, remote: str, log_path: str, pid_file: str) -> str:
        """Shell script that waits for the mount and dumps diagnostics on failure.

        Every mountpoint probe is bounded with ``timeout`` (a not-yet-serving
        fuse mount blocks stat in D-state), and the failure path reports the
        daemon's process state (stat/wchan/rss), the fuse-ish mount table
        entries, and the worker log tail so a wedged mount is debuggable from
        the world-side logs alone.
        """
        q_remote = shlex.quote(remote)
        q_log = shlex.quote(log_path)
        q_pid = shlex.quote(pid_file)
        return (
            f'FUSE_PID="$(cat {q_pid} 2>/dev/null)"; '
            f"DEADLINE=$(($(date +%s) + {_MOUNT_WAIT_S})); "
            "while [ $(date +%s) -lt $DEADLINE ]; do "
            f"  if timeout 5 mountpoint -q {q_remote}; then echo FUSE_MOUNTED; exit 0; fi; "
            '  if ! kill -0 "$FUSE_PID" 2>/dev/null; then break; fi; '
            "  sleep 0.5; "
            "done; "
            f"if timeout 5 mountpoint -q {q_remote}; then echo FUSE_MOUNTED; exit 0; fi; "
            'echo "FUSE_MOUNT_FAILED diagnostics:" >&2; '
            'echo "--- daemon ---" >&2; ps -o pid,stat,wchan:32,etime,rss,args -p "$FUSE_PID" >&2; '
            'echo "--- mounts ---" >&2; grep -iE "fuse|lazydvc" /proc/mounts >&2; '
            f'echo "--- worker log tail ---" >&2; tail -n 80 {q_log} >&2; exit 1'
        )

    async def sync_back(
        self,
        agent_env: Environment | None,
        hostname: str,
        mount: AgentWorkspaceMount,
    ) -> None:
        """Read-only dataset mount — nothing to sync back."""
        del agent_env, hostname, mount

    def with_path(self, path: str) -> FuseDirectTransport:
        """Clone for a sub-path, mirroring the NFS mount-path mapping."""
        sub_mount = None
        if self.mount_path and path.startswith(self.path + "/"):
            sub_mount = self.mount_path + path[len(self.path) :]
        return FuseDirectTransport(
            path,
            self.ssh_key_path,
            self._config_builder,
            mount_path=sub_mount or self.mount_path,
            workspace_name=self.workspace_name,
            readonly=self.readonly,
        )
