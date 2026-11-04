"""Job service: start / status / wait / signal — all unary HTTP.

Output is never streamed over a connection: it goes to spool files on the VM,
and callers fetch it (or its tail) through the files service after the fact.
Completion is observed via the long-poll ``wait`` endpoint — each poll is an
independent request against persisted state, so connection drops between polls
never affect the job.
"""

from __future__ import annotations

import asyncio

from aiohttp import web

from plato.agents.daemon.http_util import error_response, ok_response, parse_body
from plato.agents.daemon.jobs.manager import (
    AgentJobConflictError,
    AgentJobManager,
    AgentJobNotFoundError,
    signal_term_then_kill,
)
from plato.agents.daemon.state import DaemonContext
from plato.rpc.models.job import (
    AgentJobSignalRequest,
    AgentJobStartRequest,
    AgentJobWaitRequest,
    AgentJobWaitResponse,
)
from plato.rpc.protocol import (
    API_PREFIX,
    CAP_AGENT_JOB_SIGNAL,
    CAP_AGENT_JOB_START,
    CAP_AGENT_JOB_WAIT,
)


def _start_handler(manager: AgentJobManager):
    async def start(request: web.Request) -> web.Response:
        req = await parse_body(request, AgentJobStartRequest)
        if not req.argv and not req.shell:
            return error_response(request, "INVALID_REQUEST", "One of argv or shell is required")
        try:
            status = await manager.start(
                req.agent_job_id,
                argv=req.argv,
                shell=req.shell,
                cwd=req.cwd,
                env=req.env,
                inherit_env=req.inherit_env,
                payload_path=req.payload_path,
            )
        except AgentJobConflictError:
            return error_response(request, "JOB_ALREADY_EXISTS", f"job {req.agent_job_id} exists with a different spec")
        return ok_response(request, status)

    return start


def _status_handler(manager: AgentJobManager):
    async def status(request: web.Request) -> web.Response:
        agent_job_id = request.match_info["agent_job_id"]
        try:
            return ok_response(request, manager.status(agent_job_id))
        except AgentJobNotFoundError:
            return error_response(request, "JOB_NOT_FOUND", f"no such job {agent_job_id}")

    return status


def _wait_handler(manager: AgentJobManager):
    async def wait(request: web.Request) -> web.Response:
        agent_job_id = request.match_info["agent_job_id"]
        req = await parse_body(request, AgentJobWaitRequest)
        try:
            status = await manager.wait(agent_job_id, req.timeout_s)
        except AgentJobNotFoundError:
            return error_response(request, "JOB_NOT_FOUND", f"no such job {agent_job_id}")
        return ok_response(request, AgentJobWaitResponse(done=status.state != "running", status=status))

    return wait


# Strong refs to in-flight escalation tasks (create_task refs are weak).
_escalations: set[asyncio.Task[None]] = set()


def _signal_handler(manager: AgentJobManager):
    async def signal(request: web.Request) -> web.Response:
        agent_job_id = request.match_info["agent_job_id"]
        req = await parse_body(request, AgentJobSignalRequest)
        try:
            if req.escalate_kill_after_s is not None:
                # TERM now, KILL after the grace period if still running —
                # server-side, so the (possibly cancelling) caller returns
                # after one request. The task outlives this handler.
                task = asyncio.create_task(
                    signal_term_then_kill(manager, agent_job_id, grace_s=req.escalate_kill_after_s)
                )
                _escalations.add(task)
                task.add_done_callback(_escalations.discard)
                return ok_response(request, manager.status(agent_job_id))
            return ok_response(request, manager.signal(agent_job_id, req.signal))
        except AgentJobNotFoundError:
            return error_response(request, "JOB_NOT_FOUND", f"no such job {agent_job_id}")

    return signal


def register(app: web.Application, ctx: DaemonContext, *, manager: AgentJobManager | None = None) -> None:
    # NOTE: recovery is NOT run here — build_app schedules it on the app's
    # on_startup so create_task has a running loop. A standalone caller that
    # constructs its own manager must likewise call recover() under the loop.
    if manager is None:
        manager = AgentJobManager(ctx.jobs_dir)
    app.router.add_post(f"{API_PREFIX}/agent-job/start", _start_handler(manager))
    app.router.add_get(f"{API_PREFIX}/agent-job/{{agent_job_id}}/status", _status_handler(manager))
    app.router.add_post(f"{API_PREFIX}/agent-job/{{agent_job_id}}/wait", _wait_handler(manager))
    app.router.add_post(f"{API_PREFIX}/agent-job/{{agent_job_id}}/signal", _signal_handler(manager))
    ctx.capabilities.extend([CAP_AGENT_JOB_START, CAP_AGENT_JOB_WAIT, CAP_AGENT_JOB_SIGNAL])
