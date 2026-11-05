"""Report MistralSandbox creates and command executions to an observer.

A worker supplies one that records runtime metrics. In-process runs keep the default, which records nothing.
"""

import asyncio
from typing import Literal, Protocol

from temporalio.exceptions import CancelledError

from mistralai.vibe_agents.sdk.sandbox.refusal import (
    KOYEB_SANDBOX_DEPLOYMENT_FAILED_ERROR_TYPE,
    MISTRAL_SANDBOX_ACCESS_DENIED_ERROR_TYPE,
    MISTRAL_SANDBOX_QUOTA_EXCEEDED_ERROR_TYPE,
    cause_chain,
    sandbox_create_refusal_error,
)

SandboxKind = Literal["mistral"]
SandboxCreateSource = Literal["fresh", "pool", "unknown"]
"""``pool``: a pre-warmed sandbox was claimed. ``unknown``: the create failed before that was known."""
SandboxCreateOutcome = Literal["success", "failure"]
SandboxCreateReason = Literal["none", "access_denied", "quota_exceeded", "deployment_failed", "other"]
SandboxExecOutcome = Literal["success", "nonzero_exit", "error"]
"""``error``: the command produced no exit code, e.g. the execution failed or timed out."""

_REFUSAL_REASONS: dict[str, SandboxCreateReason] = {
    MISTRAL_SANDBOX_ACCESS_DENIED_ERROR_TYPE: "access_denied",
    MISTRAL_SANDBOX_QUOTA_EXCEEDED_ERROR_TYPE: "quota_exceeded",
    KOYEB_SANDBOX_DEPLOYMENT_FAILED_ERROR_TYPE: "deployment_failed",
}


class SandboxMetrics(Protocol):
    """Observe sandbox creates and executions. An implementation never raises."""

    def record_sandbox_create(
        self,
        *,
        sandbox: SandboxKind,
        source: SandboxCreateSource,
        outcome: SandboxCreateOutcome,
        reason: SandboxCreateReason,
        duration_seconds: float,
    ) -> None: ...

    def record_sandbox_exec(
        self, *, sandbox: SandboxKind, outcome: SandboxExecOutcome, duration_seconds: float
    ) -> None: ...


class _NoopSandboxMetrics:
    def record_sandbox_create(
        self,
        *,
        sandbox: SandboxKind,
        source: SandboxCreateSource,
        outcome: SandboxCreateOutcome,
        reason: SandboxCreateReason,
        duration_seconds: float,
    ) -> None:
        pass

    def record_sandbox_exec(
        self, *, sandbox: SandboxKind, outcome: SandboxExecOutcome, duration_seconds: float
    ) -> None:
        pass


NOOP_SANDBOX_METRICS: SandboxMetrics = _NoopSandboxMetrics()


def sandbox_create_failure_reason(error: BaseException) -> SandboxCreateReason:
    """Classify a failed create by its refusal type, unwrapping Activity errors."""

    refused = sandbox_create_refusal_error(error)
    if refused is None or refused.type is None:
        return "other"
    return _REFUSAL_REASONS[refused.type]


def is_cancellation(error: BaseException) -> bool:
    """Whether `error` is a cancellation, possibly wrapped in an Activity error."""

    return any(isinstance(cause, asyncio.CancelledError | CancelledError) for cause in cause_chain(error))


__all__ = [
    "NOOP_SANDBOX_METRICS",
    "SandboxCreateOutcome",
    "SandboxCreateReason",
    "SandboxCreateSource",
    "SandboxExecOutcome",
    "SandboxKind",
    "SandboxMetrics",
    "is_cancellation",
    "sandbox_create_failure_reason",
]
