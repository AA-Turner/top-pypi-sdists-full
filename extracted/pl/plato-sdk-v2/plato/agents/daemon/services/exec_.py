"""Exec service: short typed command execution.

Mutating by nature (arbitrary commands), so results are deduped by
idempotency key: the client's retry-once after a transport failure replays
the cached result instead of executing the command a second time.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import signal
import time

from aiohttp import web

from plato.agents.daemon.http_util import TypedHttpError, error_response, parse_body
from plato.agents.daemon.idempotency import ResultCache, with_idempotency
from plato.agents.daemon.spawn_env import login_env
from plato.agents.daemon.state import DaemonContext
from plato.rpc.models.exec_ import ExecRunRequest, ExecRunResponse
from plato.rpc.protocol import API_PREFIX, CAP_EXEC_RUN

# Bound on reaping a killed child's pipes: a D-state process must not pin
# the handler (and its single-flight future) forever.
_REAP_TIMEOUT_S = 5.0


def _truncate(data: bytes, limit: int) -> tuple[str, bool]:
    """Decode with head+tail truncation past ``limit`` (mirrors the SSH
    helpers' oversized-output handling and git_ops' field caps)."""
    if len(data) <= limit:
        return data.decode(errors="replace"), False
    half = limit // 2
    head = data[:half].decode(errors="replace")
    tail = data[-half:].decode(errors="replace")
    return f"{head}\n...[truncated {len(data) - limit} bytes]...\n{tail}", True


async def _execute(request: web.Request, req: ExecRunRequest) -> ExecRunResponse:
    # login_env, not os.environ: parity with SSH sessions, which re-read
    # /etc/environment via PAM at every login (the daemon's environ is frozen
    # at bootstrap time) and prepended VM_PATH_EXPORT to every command.
    env = {**login_env(), **req.env} if req.inherit_env else dict(req.env)

    start = time.monotonic()
    try:
        # start_new_session: the command gets its own process group so a
        # timeout kill takes the WHOLE tree (pipelines, grandchildren) — see
        # _kill. Same discipline as AgentJobManager.
        if req.argv:
            proc = await asyncio.create_subprocess_exec(
                *req.argv,
                cwd=req.cwd,
                env=env,
                stdin=asyncio.subprocess.PIPE if req.stdin is not None else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True,
            )
        else:
            assert req.shell is not None
            proc = await asyncio.create_subprocess_shell(
                req.shell,
                cwd=req.cwd,
                env=env,
                stdin=asyncio.subprocess.PIPE if req.stdin is not None else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True,
            )
    except (OSError, ValueError) as exc:
        # Raised (not returned) so a failed spawn is never cached as a result.
        raise TypedHttpError(request, "SPAWN_FAILED", f"Failed to spawn: {exc}") from exc

    stdin_bytes = req.stdin.encode() if req.stdin is not None else None
    timed_out = False
    try:
        out, err = await asyncio.wait_for(proc.communicate(stdin_bytes), timeout=req.timeout_s)
    except TimeoutError:
        timed_out = True
        _kill(proc)
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=_REAP_TIMEOUT_S)
        except TimeoutError:
            # Unreapable child (D-state): give up on its output rather than
            # pin this handler — and the idempotency single-flight future —
            # forever. The group is already SIGKILLed; the pool reset sweeps
            # whatever the kernel eventually releases.
            out, err = b"", b""

    stdout, trunc_out = _truncate(out or b"", req.max_output_bytes)
    stderr, trunc_err = _truncate(err or b"", req.max_output_bytes)
    return ExecRunResponse(
        rc=proc.returncode if proc.returncode is not None else -1,
        stdout=stdout,
        stderr=stderr,
        truncated_stdout=trunc_out,
        truncated_stderr=trunc_err,
        duration_s=time.monotonic() - start,
        timed_out=timed_out,
    )


def _run_handler(cache: ResultCache):
    async def run(request: web.Request) -> web.Response:
        req = await parse_body(request, ExecRunRequest)
        if not req.argv and not req.shell:
            return error_response(request, "INVALID_REQUEST", "One of argv or shell is required")
        return await with_idempotency(request, cache, lambda: _execute(request, req))

    return run


def _kill(proc: asyncio.subprocess.Process) -> None:
    """Kill the timed-out command's WHOLE process group.

    Shell pipelines and grandchildren must not survive as orphans until the
    next pool reset — same discipline as AgentJobManager (start_new_session +
    group kill). Guarded: killpg only fires when the child owns its own group,
    so a child that somehow shares the daemon's group can never take the
    daemon down with it.
    """
    with contextlib.suppress(ProcessLookupError, PermissionError):
        pgid = os.getpgid(proc.pid)
        if pgid != os.getpgid(0):
            os.killpg(pgid, signal.SIGKILL)
    with contextlib.suppress(ProcessLookupError):
        proc.kill()


def register(app: web.Application, ctx: DaemonContext) -> None:
    app.router.add_post(f"{API_PREFIX}/exec/run", _run_handler(ResultCache()))
    ctx.capabilities.append(CAP_EXEC_RUN)
