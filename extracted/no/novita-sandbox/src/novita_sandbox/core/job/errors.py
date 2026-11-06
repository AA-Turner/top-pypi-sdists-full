"""Exceptions raised by the migration job API, and the wire error mapping.

The platform returns a Kratos error envelope ``{code, reason, message, metadata}``
where the HTTP status equals ``code``. Properties of contract 0.2.0 that drive
the mapping below:

* A missing or invisible job is reported as **400 with
  ``reason=RESOURCE_NOT_FOUND``**, not 404. Dispatching on the status code alone
  would make ``except NotFoundException`` unreachable, so dispatch is done on
  ``reason`` with the status as a fallback.
* ``409`` is overloaded: it covers a ``template_alias`` that collides on the
  target cluster (``MIGRATION_TEMPLATE_ALIAS_CONFLICT``), a resource that is
  already part of another job (``MIGRATION_RESOURCE_ALREADY_MIGRATING``), a
  cancel that arrived after the point of no return
  (``MIGRATION_PAST_CANCEL_LINE``) and a resource that cannot be migrated
  because something else depends on it (``MIGRATION_SHARED_DEPENDENCY``). They
  share :class:`MigrationConflictError` as a base so ``except`` on the base
  still catches every flavour, and ``reason`` is preserved on the instance.
* ``501`` with ``reason=MIGRATION_NOT_SUPPORTED`` means the target cluster is a
  v1 cluster or the feature is switched off; no job was created.
* ``500`` no longer doubles as a validation channel: an out-of-range ``limit``
  is a **400 with ``reason=VALIDATOR_PARAM``**. A 500 is therefore a genuine
  server fault, and the original ``reason`` and message are preserved on the
  exception so callers triaging them keep the detail; the SDK never retries by
  itself.
* Cancel reports "no such job / all items already terminal / not yours" with a
  single code so job ids cannot be probed for existence; that collapses into
  :class:`~novita_sandbox.core.exceptions.NotFoundException` here.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from novita_sandbox.core.exceptions import (
    AuthenticationException,
    InvalidArgumentException,
    NotFoundException,
    RateLimitException,
    SandboxException,
)

from .types import JobStatus, MigrationStatus

REASON_VALIDATOR_PARAM = "VALIDATOR_PARAM"
REASON_RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
REASON_UNAUTHORIZED = "UNAUTHORIZED"
REASON_UNKNOWN = "UNKNOWN"
REASON_ALIAS_CONFLICT = "MIGRATION_TEMPLATE_ALIAS_CONFLICT"
REASON_RESOURCE_ALREADY_MIGRATING = "MIGRATION_RESOURCE_ALREADY_MIGRATING"
REASON_PAST_CANCEL_LINE = "MIGRATION_PAST_CANCEL_LINE"
REASON_SHARED_DEPENDENCY = "MIGRATION_SHARED_DEPENDENCY"
REASON_CONFLICT = "MIGRATION_CONFLICT"
REASON_NOT_SUPPORTED = "MIGRATION_NOT_SUPPORTED"


class MigrationConflictError(SandboxException):
    """A request-time 409: retrying the same request can never succeed.

    No job was created, and every subclass means "fix the request, then accept
    again". ``reason`` keeps the platform's machine-readable code so a caller
    that wants to distinguish flavours can, while ``except`` on this base still
    catches all of them.
    """

    reason: str = REASON_CONFLICT

    def __init__(self, message: str, *, reason: str | None = None) -> None:
        super().__init__(message)
        # An empty or missing reason means the platform did not name the
        # conflict, so the class-level default stands.
        if reason:
            self.reason = reason


class TemplateAliasConflictError(MigrationConflictError):
    """A ``template_alias`` is already taken on the target cluster (HTTP 409).

    No job was created. Retrying with the same alias can never succeed; accept
    again with a different alias.
    """

    reason = REASON_ALIAS_CONFLICT


class ResourceAlreadyMigratingError(MigrationConflictError):
    """A resource in the request already belongs to another live job (HTTP 409).

    A resource can only be carried by one job at a time: wait for the existing
    job, or cancel it and wait for the revert to finish, then accept again.
    """

    reason = REASON_RESOURCE_ALREADY_MIGRATING


class CancelTooLateError(MigrationConflictError):
    """``cancel()`` arrived after the point of no return (HTTP 409).

    Cancel is only possible while the job is still reversible: once the runner
    has committed the target-side resources the job must run to completion.
    """

    reason = REASON_PAST_CANCEL_LINE


class SharedDependencyError(MigrationConflictError):
    """A resource cannot move on its own because something depends on it.

    Typically another resource in the same account still references a template
    that this request would leave behind (HTTP 409). Migrate the dependent
    resources together in one job instead.
    """

    reason = REASON_SHARED_DEPENDENCY


class MigrationNotSupportedError(SandboxException):
    """The target cluster cannot migrate at all (HTTP 501).

    Raised for a v1 cluster or when the feature is switched off. No job was
    created and retrying cannot help.
    """

    reason: str = REASON_NOT_SUPPORTED

    def __init__(self, message: str, *, reason: str | None = None) -> None:
        super().__init__(message)
        # An empty or missing reason means the platform did not name the
        # condition, so the class-level default stands.
        if reason:
            self.reason = reason


class JobFailedError(SandboxException):
    """Raised by ``wait()`` when a job reaches the ``failed`` terminal status.

    Contract 0.2.0 has no per-item error detail; the job-level status — now
    including ``status.items`` — is carried on :attr:`status`.
    """

    def __init__(self, message: str, *, status: MigrationStatus) -> None:
        super().__init__(message)
        self.status = status


class JobCancelledError(SandboxException):
    """Raised by ``wait()`` when a job reaches the ``cancelled`` terminal status."""

    def __init__(self, message: str, *, status: MigrationStatus) -> None:
        super().__init__(message)
        self.status = status


def error_envelope(response: Any) -> Dict[str, Any]:
    """Extract the Kratos error envelope from a response, tolerating junk bodies."""
    payload: Any = None
    try:
        payload = response.json()
    except Exception:
        payload = None

    if not isinstance(payload, dict):
        content = getattr(response, "content", None)
        if isinstance(content, (bytes, bytearray)):
            content = content.decode("utf-8", errors="replace")
        if isinstance(content, str) and content:
            try:
                payload = json.loads(content)
            except json.JSONDecodeError:
                payload = None

    return payload if isinstance(payload, dict) else {}


def format_job_error_message(status_code: int, envelope: Dict[str, Any]) -> str:
    """Render a message that keeps ``reason`` visible for 500 triage."""
    reason = envelope.get("reason")
    message = envelope.get("message")
    if reason and message:
        return f"{status_code}: {reason} - {message}"
    if message:
        return f"{status_code}: {message}"
    if reason:
        return f"{status_code}: {reason}"
    return f"{status_code}: request failed"


#: The 409 flavours, keyed by ``reason``. 409 is overloaded, so the class has to
#: come from the reason; an unrecognised one falls back to the base class.
_CONFLICT_ERRORS: Dict[str, type] = {
    REASON_ALIAS_CONFLICT: TemplateAliasConflictError,
    REASON_RESOURCE_ALREADY_MIGRATING: ResourceAlreadyMigratingError,
    REASON_PAST_CANCEL_LINE: CancelTooLateError,
    REASON_SHARED_DEPENDENCY: SharedDependencyError,
}


def raise_for_job_error(response: Any) -> None:
    """Raise the SDK exception matching a failed migration API response.

    Dispatch is on ``reason`` first, with the HTTP status as a fallback for
    envelopes that arrive without one: the platform pairs 400 with
    ``RESOURCE_NOT_FOUND``, every 409 flavour with its own ``MIGRATION_*``
    reason and 501 with ``MIGRATION_NOT_SUPPORTED``, so an envelope whose reason
    and status disagree is honored by its reason. An unknown ``reason`` on a 409
    still raises :class:`MigrationConflictError` — with that reason preserved —
    rather than the least specific conflict subclass.
    """
    status_code = int(getattr(response, "status_code", 0) or 0)
    envelope = error_envelope(response)
    reason = envelope.get("reason") or ""
    message = format_job_error_message(status_code, envelope)

    if reason == REASON_RESOURCE_NOT_FOUND:
        # Also where cancel's indistinguishable "no such job / all terminal /
        # not yours" triad lands.
        raise NotFoundException(message)

    conflict_error = _CONFLICT_ERRORS.get(reason)
    if conflict_error is not None:
        raise conflict_error(message, reason=reason)

    if reason == REASON_CONFLICT:
        raise MigrationConflictError(message, reason=reason)

    if reason == REASON_NOT_SUPPORTED:
        raise MigrationNotSupportedError(message, reason=reason)

    if reason == REASON_UNAUTHORIZED:
        raise AuthenticationException(message)

    if status_code == 429:
        raise RateLimitException(message)

    if status_code == 401:
        raise AuthenticationException(message)

    if status_code == 501:
        raise MigrationNotSupportedError(message, reason=reason)

    if status_code == 409:
        # An unrecognised reason is still worth keeping: it is the only
        # machine-readable hint the caller gets for a 409 we do not model.
        raise MigrationConflictError(message, reason=reason)

    if status_code == 400:
        raise InvalidArgumentException(message)

    raise SandboxException(message)


def raise_for_terminal_status(status: MigrationStatus) -> MigrationStatus:
    """Return a finished status, or raise for the failed/cancelled ones.

    Only ``status=failed`` raises a failure: the contract does not define an
    aggregation rule for mixed outcomes, so a ``completed`` job with
    ``failed > 0`` (if the platform ever produces one) is returned as-is and
    the caller checks the counters.
    """
    # JobStatus subclasses str, so ``==`` also covers unknown values that were
    # passed through as plain strings by the parser.
    if status.status == JobStatus.FAILED:
        raise JobFailedError(
            f"Migration job {status.job_id} failed: "
            f"{status.failed}/{status.total} items failed "
            f"(completed={status.completed}, cancelled={status.cancelled})",
            status=status,
        )
    if status.status == JobStatus.CANCELLED:
        raise JobCancelledError(
            f"Migration job {status.job_id} was cancelled "
            f"({status.cancelled}/{status.total} items)",
            status=status,
        )
    return status


__all__ = [
    "CancelTooLateError",
    "JobCancelledError",
    "JobFailedError",
    "MigrationConflictError",
    "MigrationNotSupportedError",
    "REASON_ALIAS_CONFLICT",
    "REASON_CONFLICT",
    "REASON_NOT_SUPPORTED",
    "REASON_PAST_CANCEL_LINE",
    "REASON_RESOURCE_ALREADY_MIGRATING",
    "REASON_RESOURCE_NOT_FOUND",
    "REASON_SHARED_DEPENDENCY",
    "REASON_UNAUTHORIZED",
    "REASON_UNKNOWN",
    "REASON_VALIDATOR_PARAM",
    "ResourceAlreadyMigratingError",
    "SharedDependencyError",
    "TemplateAliasConflictError",
    "error_envelope",
    "format_job_error_message",
    "raise_for_job_error",
    "raise_for_terminal_status",
]
