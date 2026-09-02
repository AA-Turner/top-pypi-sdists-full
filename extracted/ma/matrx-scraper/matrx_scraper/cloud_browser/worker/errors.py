"""Typed error / conflict catalogue — S2 §9.

The distinction between the two failure planes is load-bearing (S2 §9.1):

  * **Result-level** — the browser tried and the page said no (selector missing,
    timeout, SSRF gate). Reported as ``ok=true`` + ``result.success=false`` +
    ``result.error_type`` from the existing ``actions.py`` set. Handled inside the
    command executor, never here.
  * **Envelope-level** — the protocol or state said no (stale token, wrong order,
    human in control, draining, shutting down). This module owns it: a
    ``WorkerProtocolError`` carrying a literal ``code`` from the catalogue.

A worker that turns a selector-not-found into an envelope error, or a stale token
into a ``success=false`` result, fails conformance. Mixing the planes is how a
control plane ends up retrying things it must never retry.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

# The complete literal set from S2 §9.2. A ``code`` is never free text.
WorkerErrorCode = Literal[
    "browser_controlled_by_human",
    "stale_fencing_token",
    "unknown_fencing_revision",
    "queue_draining",
    "worker_shutting_down",
    "not_bootstrapped",
    "already_bootstrapped",
    "run_mismatch",
    "profile_mismatch",
    "lease_expired",
    "access_revoked",
    "sequence_out_of_order",
    "sequence_conflict",
    "sequence_too_old",
    "sequence_required",
    "sequence_not_permitted",
    "illegal_controller_transition",
    "controller_transition_conflict",
    "command_not_supported",
    "invalid_command_arguments",
    "parameter_not_available_on_persistent_run",
    "eval_js_not_permitted",
    "unknown_page",
    "unknown_dialog",
    "command_deadline_exceeded",
    "capture_target_missing",
    "capture_upload_failed",
    "checkpoint_in_progress",
    "checkpoint_failed",
    "chromium_unclean_exit",
    "profile_locked_locally",
    "browser_crashed",
    "worker_degraded",
    "reopen_required",
    "unauthorized_worker_call",
    "audience_mismatch",
    "credential_expired",
    "credential_replayed",
]


# HTTP status + retryability, straight from S2 §9.2. The worker itself is
# transport-agnostic, but the manager needs the status, so it rides the error.
_ERROR_META: dict[str, tuple[int, bool]] = {
    "browser_controlled_by_human": (409, False),
    "stale_fencing_token": (409, False),
    "unknown_fencing_revision": (409, False),
    "queue_draining": (409, True),
    "worker_shutting_down": (409, False),
    "not_bootstrapped": (409, True),
    "already_bootstrapped": (409, False),
    "run_mismatch": (409, False),
    "profile_mismatch": (409, False),
    "lease_expired": (409, False),
    "access_revoked": (403, False),
    "sequence_out_of_order": (409, False),
    "sequence_conflict": (409, False),
    "sequence_too_old": (409, False),
    "sequence_required": (422, False),
    "sequence_not_permitted": (422, False),
    "illegal_controller_transition": (409, False),
    "controller_transition_conflict": (409, False),
    "command_not_supported": (422, False),
    "invalid_command_arguments": (422, False),
    "parameter_not_available_on_persistent_run": (422, False),
    "eval_js_not_permitted": (403, False),
    "unknown_page": (422, False),
    "unknown_dialog": (422, False),
    "command_deadline_exceeded": (504, True),
    "capture_target_missing": (422, False),
    "capture_upload_failed": (502, True),
    "checkpoint_in_progress": (409, True),
    "checkpoint_failed": (500, True),
    "chromium_unclean_exit": (500, False),
    "profile_locked_locally": (409, False),
    "browser_crashed": (503, False),
    "worker_degraded": (503, True),
    "reopen_required": (409, False),
    "unauthorized_worker_call": (401, False),
    "audience_mismatch": (401, False),
    "credential_expired": (401, True),
    "credential_replayed": (401, False),
}


def http_status_for(code: str) -> int:
    return _ERROR_META.get(code, (409, False))[0]


def retryable_for(code: str) -> bool:
    return _ERROR_META.get(code, (409, False))[1]


class WorkerError(BaseModel):
    """S2 §9.1. Carries NO resolver detail and NO page content — the same rule the
    url_guard rejections follow, extended to every error. The human-readable
    ``message`` is a fixed phrase, never a page body, dialog text, or query string."""

    model_config = ConfigDict(extra="forbid")

    code: WorkerErrorCode
    message: str
    retryable: bool
    retry_after_ms: int | None = None
    current_fencing_revision: int | None = None
    current_controller: str | None = None
    last_sequence_applied: int | None = None
    conflicting_handoff_id: str | None = None


class WorkerProtocolError(Exception):
    """An envelope-level refusal. Raised inside an operation; the operation's
    boundary converts it to the op-specific typed response with ``ok=False``.

    ``message`` defaults to the code so no caller can accidentally attach page
    content — a real message must be a fixed phrase passed deliberately.
    """

    def __init__(
        self,
        code: WorkerErrorCode,
        *,
        message: str | None = None,
        retry_after_ms: int | None = None,
        current_fencing_revision: int | None = None,
        current_controller: str | None = None,
        last_sequence_applied: int | None = None,
        conflicting_handoff_id: str | None = None,
    ) -> None:
        self.code = code
        self.http_status = http_status_for(code)
        self.retryable = retryable_for(code)
        self.message = message or code
        self.retry_after_ms = retry_after_ms
        self.current_fencing_revision = current_fencing_revision
        self.current_controller = current_controller
        self.last_sequence_applied = last_sequence_applied
        self.conflicting_handoff_id = conflicting_handoff_id
        super().__init__(f"{code}: {self.message}")

    def to_error(self) -> WorkerError:
        return WorkerError(
            code=self.code,
            message=self.message,
            retryable=self.retryable,
            retry_after_ms=self.retry_after_ms,
            current_fencing_revision=self.current_fencing_revision,
            current_controller=self.current_controller,
            last_sequence_applied=self.last_sequence_applied,
            conflicting_handoff_id=self.conflicting_handoff_id,
        )
