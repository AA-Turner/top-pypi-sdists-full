"""Error taxonomy for the agent RPC layer.

Two strictly separated layers:

1. **Wire errors** — any non-2xx response carries an ``RpcError`` JSON body.
   ``code`` is the machine-readable contract; HTTP status is advisory.
2. **Caller-facing exceptions** — the client maps wire errors and transport
   failures onto a small exception hierarchy that call sites (execution.py,
   task.py, warmpool.py) branch on with ``isinstance``, replacing today's
   substring matching on SSH stderr ("Permission denied (publickey)",
   "lost connection", ambiguous exit 255).

Domain failure is NOT an RPC error: an exec with rc=1 or a git op with
``ok=False`` returns 200 with a typed body. ``RemoteOpFailed`` exists for call
sites that want raise-on-failure ergonomics, raised by the *stub*, not the wire.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ErrorCode = Literal[
    "UNAUTHORIZED",
    "INVALID_REQUEST",
    "NOT_FOUND",
    "PAYLOAD_TOO_LARGE",
    "DEADLINE_EXCEEDED",
    "JOB_NOT_FOUND",
    "JOB_ALREADY_EXISTS",
    "SPAWN_FAILED",
    "RECLAIMED",
    "SHUTTING_DOWN",
    "INTERNAL",
]

HTTP_STATUS_BY_CODE: dict[str, int] = {
    "UNAUTHORIZED": 401,
    "INVALID_REQUEST": 422,
    "NOT_FOUND": 404,
    "PAYLOAD_TOO_LARGE": 413,
    "DEADLINE_EXCEEDED": 504,
    "JOB_NOT_FOUND": 404,
    "JOB_ALREADY_EXISTS": 409,
    "SPAWN_FAILED": 500,
    "RECLAIMED": 409,
    "SHUTTING_DOWN": 503,
    "INTERNAL": 500,
}


class RpcError(BaseModel):
    """Structured error body carried on every non-2xx response."""

    code: ErrorCode
    message: str
    detail: dict[str, str] = Field(default_factory=dict)
    retryable: bool = False
    request_id: str = ""


# --- Caller-facing exception hierarchy ---------------------------------------


class AgentRpcError(Exception):
    """Base for every error raised by the RPC client layer."""


class RetryableInfraError(AgentRpcError):
    """Marker base: infrastructure failure where retrying (typically on a fresh
    VM) is a sane policy. Replaces execution.py's substring classification."""


class AgentdUnavailable(AgentRpcError):
    """The daemon is absent, stale, or unreachable at handshake time.

    Only ever raised BEFORE an operation is submitted — it is the one condition
    that triggers SSH fallback. Once an op has been submitted, failures surface
    as the other exceptions and are never re-run over SSH (no double-execute).
    """


class AgentAuthError(RetryableInfraError):
    """Token rejected (wire UNAUTHORIZED). SSH-era analogue: 'Permission denied
    (publickey)'. Retry policy: fresh VM, bounded attempts."""


class AgentUnreachableError(RetryableInfraError):
    """The VM stopped answering after reconnect budget was exhausted and the
    out-of-band probe also failed. SSH-era analogue: ambiguous exit 255 /
    'lost connection' — but only raised once liveness is genuinely ruled out."""

    def __init__(self, message: str, *, health_report: object | None = None) -> None:
        super().__init__(message)
        self.health_report = health_report


class VMReclaimedError(RetryableInfraError):
    """The warm pool is tearing this VM down (wire RECLAIMED). Replaces the
    exit-255 storms that pool churn caused in in-flight SSH commands."""


class AgentJobRecordLostError(RetryableInfraError):
    """The daemon restarted and could not re-adopt the job (state='lost').
    Honest, distinguishable successor of exit-255: the outcome is unknown."""


class RpcTransportError(AgentRpcError):
    """Connection-level failure (refused, reset, timeout, WS drop). Drives the
    client's reconnect policy; call sites normally never see it — the client
    converts it to one of the semantic exceptions above."""


class RemoteOpFailed(AgentRpcError):
    """A remote operation genuinely failed (nonzero rc / ok=False). Raised by
    typed stubs with raise-on-failure ergonomics; NEVER transport-retried."""

    def __init__(self, message: str, *, rc: int | None = None, stdout: str = "", stderr: str = "") -> None:
        super().__init__(message)
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr


class RpcException(AgentRpcError):
    """A structured wire error that has no more specific mapping. Carries the
    full ``RpcError`` body."""

    def __init__(self, error: RpcError) -> None:
        super().__init__(f"{error.code}: {error.message}")
        self.error = error
