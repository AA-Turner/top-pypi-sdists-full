"""Pool service: in-process warm-VM reset + reclaim lifecycle.

Reset runs the scrub steps IN the daemon process, not over a self-hosting SSH
session, so the two SSH-era hazards disappear: no bash process to self-kill
(the ``[u]ser-data-dir`` bracket trick is unnecessary) and no risk of unmounting
the transport's own PrivateTmp. Each step is best-effort and reported
individually — the sentinel string parsing (``warm-pool-reset-ok``) is gone.

Reclaim flips a daemon-wide flag so every in-flight and subsequent call (except
handshake/reclaim/healthz) gets a typed RECLAIMED error instead of a dropped
connection — the fix for pool-churn exit-255 storms.
"""

from __future__ import annotations

import asyncio
import glob
import shutil
from collections.abc import Awaitable, Callable
from pathlib import Path

from aiohttp import web

from plato.agents.daemon.http_util import ok_response, parse_body
from plato.agents.daemon.idempotency import ResultCache, with_idempotency
from plato.agents.daemon.jobs.manager import AgentJobManager
from plato.agents.daemon.services.env import scrub_env_for_reset
from plato.agents.daemon.state import DaemonContext
from plato.rpc.models.pool import (
    PoolReclaimResponse,
    PoolResetRequest,
    PoolResetResult,
    PoolResetStep,
)
from plato.rpc.protocol import API_PREFIX, CAP_POOL_RECLAIM, CAP_POOL_RESET

_DEFAULT_TMP_GLOBS = ("/tmp/plato-*", "/var/tmp/plato-*")  # noqa: S108 - scrub targets
_DEFAULT_CGROUP_SETUP_GLOB = "/sys/fs/cgroup/plato-wf-setup-*"
_ETC_ENVIRONMENT = Path("/etc/environment")
_ETC_HOSTS = Path("/etc/hosts")


async def _pkill(pattern_args: list[str]) -> tuple[bool, str]:
    try:
        proc = await asyncio.create_subprocess_exec(
            "pkill", *pattern_args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
        )
        _out, err = await proc.communicate()
    except OSError as exc:
        return False, str(exc)
    # pkill rc 1 = "no processes matched" — a success for our purposes.
    return proc.returncode in (0, 1), err.decode(errors="replace").strip()


def _rm_globs(patterns: tuple[str, ...]) -> tuple[bool, str]:
    removed = 0
    errors: list[str] = []
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                p = Path(path)
                if p.is_dir() and not p.is_symlink():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink(missing_ok=True)
                removed += 1
            except OSError as exc:
                errors.append(str(exc))
    return not errors, f"removed {removed}" + (f", errors: {'; '.join(errors)}" if errors else "")


def _cgroup_kill_setup(cgroup_glob: str) -> tuple[bool, str]:
    """Kill every workflow ``setup=`` process tree via cgroup v2 ``cgroup.kill``.

    Mirrors the SSH reset step (warmpool._runtime_reset_commands): a setup
    command joins a fresh ``plato-wf-setup-*`` cgroup before exec, so its whole
    descendant tree — daemonized servers included — is kernel-tracked; writing
    ``1`` to ``cgroup.kill`` SIGKILLs the membership atomically (fork race
    handled in-kernel). rmdir is best-effort: a not-yet-reaped zombie leaves an
    empty dir, harmless and removed on the next reset.
    """
    killed = 0
    errors: list[str] = []
    for cg in glob.glob(cgroup_glob):
        p = Path(cg)
        if not p.is_dir():
            continue
        try:
            (p / "cgroup.kill").write_text("1")
            killed += 1
        except OSError as exc:
            errors.append(str(exc))
        try:
            p.rmdir()
        except OSError:
            pass  # membership not yet reaped; removed next reset
    return not errors, f"killed {killed} setup cgroup(s)" + (f", errors: {'; '.join(errors)}" if errors else "")


def _strip_env_block(env_path: Path) -> tuple[bool, str]:
    try:
        if env_path.exists():
            env_path.write_text(scrub_env_for_reset(env_path.read_text()))
        return True, "managed block + bare key lines removed (baked entries preserved)"
    except OSError as exc:
        return False, str(exc)


def _remove_hosts_entry(hosts_path: Path, hostname: str) -> tuple[bool, str]:
    try:
        if hosts_path.exists():
            kept = [
                ln
                for ln in hosts_path.read_text().splitlines()
                if not (len(ln.split()) >= 2 and ln.split()[1] == hostname)
            ]
            hosts_path.write_text("\n".join(kept) + "\n")
        return True, "ok"
    except OSError as exc:
        return False, str(exc)


async def _reset_workspace(path_str: str) -> tuple[bool, str]:
    path = Path(path_str)
    # Lazy-unmount if it's a mount point (best-effort), then wipe and recreate.
    try:
        proc = await asyncio.create_subprocess_exec(
            "umount", "-l", str(path), stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
        )
        await proc.wait()
    except OSError:
        pass

    def _wipe() -> tuple[bool, str]:
        try:
            # `rm -rf` semantics, not is_dir()-only: a regular file or
            # (dangling) symlink at the workspace path must be removed too, or
            # mkdir below raises and the workspace silently stays un-reset. A
            # symlink is unlinked — never followed — so a symlinked workspace
            # path can't wipe its target.
            if path.is_symlink() or path.is_file():
                path.unlink(missing_ok=True)
            elif path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            path.mkdir(parents=True, exist_ok=True)
            return True, "reset"
        except OSError as exc:
            return False, str(exc)

    # Workspace trees can be huge; the wipe runs off-loop (audit M4).
    return await asyncio.to_thread(_wipe)


def _reset_handler(
    env_path: Path,
    hosts_path: Path,
    tmp_globs: tuple[str, ...],
    cgroup_setup_glob: str,
    job_manager: AgentJobManager | None,
):
    cache = ResultCache()

    async def reset(request: web.Request) -> web.Response:
        req = await parse_body(request, PoolResetRequest)

        async def produce() -> PoolResetResult:
            steps: list[PoolResetStep] = []

            async def record_async(name: str, fn: Callable[[], Awaitable[tuple[bool, str]]]) -> None:
                ok, detail = await fn()
                steps.append(PoolResetStep(name=name, ok=ok, detail=detail))

            async def record(name: str, fn: Callable[[], tuple[bool, str]]) -> None:
                # Sync FS work (rmtree/glob sweeps) hops to a worker thread: a
                # multi-second delete must not freeze the event loop — a frozen
                # loop stalls /healthz, handshakes, and other tasks' wait
                # long-polls, and cannot even fire its own deadline timers
                # (audit M4; the git service set this precedent).
                ok, detail = await asyncio.to_thread(fn)
                steps.append(PoolResetStep(name=name, ok=ok, detail=detail))

            # Kill stray agent runners (daemon itself is plato-agent-daemon → safe).
            await record_async("kill_agent_runner", lambda: _pkill(["-x", "plato-agent-runner"]))
            # Kill workflow setup= process trees (cgroup.kill) — parity with the
            # SSH reset chain (warmpool._runtime_reset_commands).
            await record("kill_setup_cgroups", lambda: _cgroup_kill_setup(cgroup_setup_glob))
            await record_async("kill_chromium", lambda: _pkill(["-9", "-f", "user-data-dir=/tmp/plato-ab-"]))
            # Reap any direct-fuse dataset daemon BEFORE the workspace unmounts
            # and the /tmp wipe below: deleting a live worker's hydration
            # cache/config underneath it can wedge the fuse loop mid-request
            # (D-state) — the failure the direct mounts exist to avoid. Killed
            # first, the workspace resets detach now-dead mounts cleanly and the
            # wipe only touches orphaned state. Parity with the SSH reset chain.
            await record_async("kill_fuse", lambda: _pkill(["-x", "plato-fuse"]))
            # Workspaces MUST be unmounted before the /tmp wipe: pkill returns
            # at SIGTERM delivery, not process exit, so a fuse daemon can still
            # be unwinding here — wiping its cache while its mount is attached
            # wedges it in D-state (unkillable, accumulates across pool reuse).
            # Detaching first is the same invariant the SSH chain relied on.
            for ws in req.workspace_paths:
                await record_async(f"reset_workspace:{ws}", lambda ws=ws: _reset_workspace(ws))
            await record("rm_tmp", lambda: _rm_globs(tmp_globs))
            if job_manager is not None:
                # Prune finished-job state so spools/dirs don't accumulate across
                # the pooled VM's lifetime (running jobs untouched).
                jm = job_manager
                await record("prune_jobs", lambda: (True, f"pruned {jm.prune_finished()}"))
            await record("strip_env_block", lambda: _strip_env_block(env_path))
            await record(
                "remove_hosts_entry",
                lambda: _remove_hosts_entry(hosts_path, "runtime.plato.internal"),
            )

            return PoolResetResult(ok=True, steps=steps)

        return await with_idempotency(request, cache, produce)

    return reset


def _reclaim_handler(ctx: DaemonContext):
    async def reclaim(request: web.Request) -> web.Response:
        ctx.reclaimed = True
        return ok_response(request, PoolReclaimResponse())

    return reclaim


def register(
    app: web.Application,
    ctx: DaemonContext,
    *,
    env_path: Path = _ETC_ENVIRONMENT,
    hosts_path: Path = _ETC_HOSTS,
    tmp_globs: tuple[str, ...] = _DEFAULT_TMP_GLOBS,
    cgroup_setup_glob: str = _DEFAULT_CGROUP_SETUP_GLOB,
    job_manager: AgentJobManager | None = None,
) -> None:
    app.router.add_post(
        f"{API_PREFIX}/pool/reset",
        _reset_handler(env_path, hosts_path, tmp_globs, cgroup_setup_glob, job_manager),
    )
    app.router.add_post(f"{API_PREFIX}/pool/reclaim", _reclaim_handler(ctx))
    ctx.capabilities.append(CAP_POOL_RESET)
    ctx.capabilities.append(CAP_POOL_RECLAIM)
