"""Typed per-service stubs over an ``AgentDaemonClient``.

One stub class per service; each is a thin typed wrapper mapping call-site
ergonomics onto the connection's ``get``/``post``. Only the health stub exists
in the client-core step; exec/files/pool/agent-job/git stubs are added as their
daemon services land.
"""

from __future__ import annotations

import asyncio
import uuid

from plato.rpc.client.connection import AgentDaemonClient
from plato.rpc.errors import AgentUnreachableError
from plato.rpc.models.env import EnvSetupRequest, EnvSetupResponse
from plato.rpc.models.exec_ import ExecRunRequest, ExecRunResponse
from plato.rpc.models.files import FileStatResponse, FileWriteResponse
from plato.rpc.models.health import HandshakeResponse, HealthReport, PingResponse
from plato.rpc.models.job import (
    AgentJobSignalRequest,
    AgentJobStartRequest,
    AgentJobStatus,
    AgentJobWaitRequest,
    AgentJobWaitResponse,
)
from plato.rpc.models.pool import PoolReclaimResponse, PoolResetRequest, PoolResetResult


class HealthStub:
    def __init__(self, client: AgentDaemonClient) -> None:
        self._client = client

    async def handshake(self, *, deadline_s: float = 10.0) -> HandshakeResponse:
        return await self._client.get("handshake", HandshakeResponse, deadline_s=deadline_s)

    async def ping(self, *, deadline_s: float = 10.0) -> PingResponse:
        return await self._client.get("health/ping", PingResponse, deadline_s=deadline_s)

    async def report(self, *, deadline_s: float = 15.0) -> HealthReport:
        return await self._client.get("health/report", HealthReport, deadline_s=deadline_s)


class ExecStub:
    def __init__(self, client: AgentDaemonClient) -> None:
        self._client = client

    async def run(self, req: ExecRunRequest) -> ExecRunResponse:
        # Idempotency-keyed so a transport blip can safely resend: a command
        # like `command -v` or a stamp `cat` is read-only, and the daemon
        # dedupes by key for anything with side effects.
        return await self._client.post(
            "exec/run",
            req,
            ExecRunResponse,
            deadline_s=req.timeout_s + 5.0,
            idempotency_key=uuid.uuid4().hex,
        )


class EnvStub:
    def __init__(self, client: AgentDaemonClient) -> None:
        self._client = client

    async def setup(self, req: EnvSetupRequest) -> EnvSetupResponse:
        return await self._client.post(
            "env/setup", req, EnvSetupResponse, deadline_s=30.0, idempotency_key=uuid.uuid4().hex
        )


class FilesStub:
    def __init__(self, client: AgentDaemonClient) -> None:
        self._client = client

    async def push(self, path: str, data: bytes, *, mode: int = 0o600, deadline_s: float = 120.0) -> FileWriteResponse:
        return await self._client.put_bytes(
            "files/content",
            data,
            FileWriteResponse,
            params={"path": path, "mode": oct(mode)},
            deadline_s=deadline_s,
        )

    async def pull(self, path: str, *, deadline_s: float = 120.0) -> bytes:
        return await self._client.get_bytes("files/content", params={"path": path}, deadline_s=deadline_s)

    async def pull_tail(self, path: str, max_bytes: int, *, deadline_s: float = 120.0) -> bytes:
        """Last ``max_bytes`` of ``path``. ``tail`` is an additive param: an
        older daemon ignores it and streams the full body, so the client-side
        slice here is load-bearing, not defensive."""
        data = await self._client.get_bytes(
            "files/content", params={"path": path, "tail": str(max_bytes)}, deadline_s=deadline_s
        )
        return data[-max_bytes:] if max_bytes else b""

    async def stat(self, path: str, *, deadline_s: float = 15.0) -> FileStatResponse:
        return await self._client.get("files/stat", FileStatResponse, params={"path": path}, deadline_s=deadline_s)


class PoolStub:
    def __init__(self, client: AgentDaemonClient) -> None:
        self._client = client

    async def reset(self, workspace_paths: list[str], *, deadline_s: float = 60.0) -> PoolResetResult:
        return await self._client.post(
            "pool/reset",
            PoolResetRequest(workspace_paths=workspace_paths),
            PoolResetResult,
            deadline_s=deadline_s,
            idempotency_key=uuid.uuid4().hex,
        )

    async def reclaim(self, *, deadline_s: float = 15.0) -> PoolReclaimResponse:
        # Empty-body POST; reclaim is idempotent and always answerable.
        return await self._client.post(
            "pool/reclaim",
            PoolResetRequest(),  # body ignored by the handler
            PoolReclaimResponse,
            deadline_s=deadline_s,
            idempotency_key=uuid.uuid4().hex,
        )


class AgentJobStub:
    def __init__(self, client: AgentDaemonClient) -> None:
        self._client = client

    async def start(self, req: AgentJobStartRequest) -> AgentJobStatus:
        # agent_job_id IS the idempotency key: restarting the same id returns the
        # existing job rather than spawning a duplicate.
        return await self._client.post(
            "agent-job/start", req, AgentJobStatus, deadline_s=60.0, idempotency_key=req.agent_job_id
        )

    async def status(self, agent_job_id: str, *, deadline_s: float = 15.0) -> AgentJobStatus:
        return await self._client.get(f"agent-job/{agent_job_id}/status", AgentJobStatus, deadline_s=deadline_s)

    async def wait(self, agent_job_id: str, *, timeout_s: float = 30.0) -> AgentJobWaitResponse:
        # Long-poll; the deadline covers the server-side wait plus slack.
        return await self._client.post(
            f"agent-job/{agent_job_id}/wait",
            AgentJobWaitRequest(timeout_s=timeout_s),
            AgentJobWaitResponse,
            deadline_s=timeout_s + 10.0,
        )

    async def wait_for_exit(
        self, agent_job_id: str, *, poll_s: float = 30.0, unreachable_budget: int = 5
    ) -> AgentJobStatus:
        """Block until the job leaves the running state, surviving connection
        blips — the observation half of the exit-255 fix.

        Each poll is an independent long-poll against state persisted on the
        daemon, so the job keeps running regardless of the client connection. A
        ``wait`` is a pure idempotent read, so a transport failure on one poll
        (dropped connection, briefly unreachable VM) is NOT fatal: it is retried
        with backoff up to ``unreachable_budget`` consecutive failures. Only
        *sustained* unreachability — the VM genuinely gone — propagates as
        ``AgentUnreachableError``. A single dropped poll must never abort a
        still-running job."""
        consecutive_unreachable = 0
        while True:
            try:
                resp = await self.wait(agent_job_id, timeout_s=poll_s)
            except AgentUnreachableError:
                consecutive_unreachable += 1
                if consecutive_unreachable > unreachable_budget:
                    raise
                await asyncio.sleep(min(2.0**consecutive_unreachable, 10.0))
                continue
            consecutive_unreachable = 0
            if resp.done:
                return resp.status

    async def signal(
        self,
        agent_job_id: str,
        sig: int,
        *,
        escalate_kill_after_s: float | None = None,
        deadline_s: float = 15.0,
    ) -> AgentJobStatus:
        return await self._client.post(
            f"agent-job/{agent_job_id}/signal",
            AgentJobSignalRequest(signal=sig, escalate_kill_after_s=escalate_kill_after_s),
            AgentJobStatus,
            deadline_s=deadline_s,
        )
