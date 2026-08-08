"""Job service models: long-running processes decoupled from any connection.

This is the exit-255 fix. A job's lifetime is owned by the daemon, not by the
SSH/HTTP connection that started it: output goes to spool files, the exit record
is persisted, and a reconnecting world reads the outcome. ``state`` is the
honest successor to ambiguous exit 255 — ``lost`` explicitly means "the daemon
restarted and could not determine the outcome," distinct from a real failure.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

AgentJobState = Literal["running", "exited", "signaled", "lost"]


class AgentJobStartRequest(BaseModel):
    # Client-generated; also the idempotency key. Re-starting the same agent_job_id
    # returns the existing job (409 only if argv/shell differs).
    agent_job_id: str
    argv: list[str] | None = None
    shell: str | None = None
    cwd: str | None = None
    env: dict[str, str] = Field(default_factory=dict)
    inherit_env: bool = True
    # File the instruction/payload was pushed to (via files service); recorded
    # for provenance, not interpreted by the daemon.
    payload_path: str | None = None


class AgentJobStatus(BaseModel):
    agent_job_id: str
    state: AgentJobState
    pid: int | None = None
    pgid: int | None = None
    rc: int | None = None
    term_signal: int | None = None
    started_at: datetime
    finished_at: datetime | None = None
    stdout_bytes: int = 0
    stderr_bytes: int = 0


class AgentJobWaitRequest(BaseModel):
    timeout_s: float = 30.0


class AgentJobWaitResponse(BaseModel):
    done: bool
    status: AgentJobStatus


class AgentJobSignalRequest(BaseModel):
    # Signal number (e.g. 15 SIGTERM, 9 SIGKILL). Sent to the whole process
    # group so the agent's children die with it.
    signal: int = 15
    # Additive: when set, the daemon escalates to SIGKILL after this grace
    # period if the job is still running — server-side, so a cancelling caller
    # sends ONE request and never blocks on the grace window.
    escalate_kill_after_s: float | None = None
