"""Atomic, opt-in completion and rearm for bounded on-demand tool work.

This is intentionally only persistence.  A host explicitly chooses which
registered tool tasks may use it and does not gain a new scheduler path merely
by configuring the package.  A successful transaction owns the terminal row,
successor, and task completion stamp; the host reports only refused outcomes.
"""

from __future__ import annotations

import hashlib
import inspect
import uuid
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._ext import get_db_model, get_ext

BACKLOG_REARM_METADATA_KEY = "backlog_rearm"
BACKLOG_REARM_VERSION = 1
_ACTIVE_STATUSES = ("queued", "claimed", "running")
_EXECUTING_STATUSES = ("claimed", "running")


class BacklogRearmRequest(BaseModel):
    """Authority and successor identity for one bounded tool execution.

    ``recovery_key`` is supplied by the durable recovery owner.  It is opaque
    to this package, but version-prefixed so future recovery contracts cannot
    accidentally coalesce with the current one.
    """

    model_config = ConfigDict(extra="forbid")

    task_id: str
    user_id: str
    organization_id: str
    predecessor_run_id: str
    claim_token: str = Field(min_length=1, max_length=512)
    recovery_key: str = Field(min_length=4, max_length=512)
    due_at: datetime
    result_summary: str | None = Field(default=None, max_length=2_000)
    error_message: str | None = Field(default=None, max_length=20_000)
    output_ref: dict[str, Any] | None = None
    result_metadata: dict[str, Any] | None = None

    @field_validator("task_id", "user_id", "organization_id", "predecessor_run_id")
    @classmethod
    def _valid_uuid(cls, value: str) -> str:
        try:
            return str(uuid.UUID(value))
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError("must be a UUID") from exc

    @field_validator("recovery_key")
    @classmethod
    def _versioned_key(cls, value: str) -> str:
        if not value.startswith("v1:"):
            raise ValueError("must be an opaque v1: recovery key")
        return value

    @field_validator("due_at")
    @classmethod
    def _aware_due_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("must be timezone-aware")
        return value.astimezone(UTC)


class BacklogRearmOutcome(BaseModel):
    """The result; committed success needs no post-commit bookkeeping."""

    status: Literal[
        "rearmed", "already_rearmed", "authority_lost", "task_ineligible", "collision_refused"
    ]
    predecessor_run_id: str
    successor_run_id: str | None = None
    reason: str | None = None


class _CollisionRefused(RuntimeError):
    pass


def _authority_digest(recovery_key: str, claim_token: str) -> str:
    return hashlib.sha256(f"{recovery_key}\x00{claim_token}".encode()).hexdigest()


def _recovery_metadata(request: BacklogRearmRequest) -> dict[str, Any]:
    return {
        "version": BACKLOG_REARM_VERSION,
        "recovery_key": request.recovery_key,
        "predecessor_run_id": request.predecessor_run_id,
        "authority_digest": _authority_digest(request.recovery_key, request.claim_token),
    }


def _same_successor(row: dict[str, Any], request: BacklogRearmRequest) -> bool:
    metadata = row.get("metadata")
    if not isinstance(metadata, dict):
        return False
    receipt = metadata.get(BACKLOG_REARM_METADATA_KEY)
    return isinstance(receipt, dict) and (
        receipt.get("version") == BACKLOG_REARM_VERSION
        and receipt.get("recovery_key") == request.recovery_key
        and receipt.get("predecessor_run_id") == request.predecessor_run_id
    )


def _valid_descriptor(value: Any) -> bool:
    """Accept only the versioned recovery descriptor this primitive writes."""
    if not isinstance(value, dict):
        return False
    if value.get("version") != BACKLOG_REARM_VERSION:
        return False
    recovery_key = value.get("recovery_key")
    predecessor_id = value.get("predecessor_run_id")
    digest = value.get("authority_digest")
    if not isinstance(recovery_key, str) or not recovery_key.startswith("v1:"):
        return False
    try:
        uuid.UUID(str(predecessor_id))
    except (TypeError, ValueError):
        return False
    if not isinstance(digest, str) or len(digest) != 64:
        return False
    try:
        int(digest, 16)
    except ValueError:
        return False
    successor_id = value.get("successor_run_id")
    if successor_id is not None:
        try:
            uuid.UUID(str(successor_id))
        except (TypeError, ValueError):
            return False
    return True


def _same_receipt(receipt: Any, request: BacklogRearmRequest) -> bool:
    return isinstance(receipt, dict) and (
        receipt.get("version") == BACKLOG_REARM_VERSION
        and receipt.get("recovery_key") == request.recovery_key
        and receipt.get("authority_digest")
        == _authority_digest(request.recovery_key, request.claim_token)
        and isinstance(receipt.get("successor_run_id"), str)
    )


async def _validate_registered_task(task: dict[str, Any], agent_task: dict[str, Any] | None) -> bool:
    validator = get_ext("backlog_task_validator")
    verdict = validator(task, agent_task)
    return bool(await verdict) if inspect.isawaitable(verdict) else bool(verdict)


def _task_reason(task: dict[str, Any], request: BacklogRearmRequest, now: datetime) -> str | None:
    if str(task.get("user_id") or "") != request.user_id or str(
        task.get("organization_id") or ""
    ) != request.organization_id:
        return "task actor or organization does not match request"
    if task.get("kind") != "tool":
        return "task is not a tool task"
    if not task.get("enabled") or task.get("deleted_at") is not None:
        return "task is disabled or deleted"
    expires_at = task.get("expires_at")
    if expires_at is not None and expires_at <= now:
        return "task is expired"
    return None


async def _locked_active_successor(
    task: dict[str, Any], predecessor: dict[str, Any], request: BacklogRearmRequest
) -> tuple[str | None, bool]:
    """Return matching active coverage, or flag a foreign active collision."""
    SchRunModel = get_db_model("SchRun")
    rows = (
        await SchRunModel.filter(task_id=task["id"], status__in=list(_ACTIVE_STATUSES))
        .select_for_update()
        .values()
    )
    others = [row for row in rows if str(row.get("id")) != request.predecessor_run_id]
    if not others:
        return None, False
    matching = [
        row
        for row in others
        if _same_successor(row, request)
        and _valid_descriptor((row.get("metadata") or {}).get(BACKLOG_REARM_METADATA_KEY))
        and str(row.get("task_id") or "") == str(task["id"])
        and str(row.get("user_id") or "") == str(task.get("user_id") or "")
        and str(row.get("organization_id") or "") == str(task.get("organization_id") or "")
        and row.get("queue") == task.get("queue") == predecessor.get("queue")
        and row.get("trigger_id") is None
    ]
    if len(matching) == 1 and len(others) == 1:
        return str(matching[0]["id"]), False
    return None, True


async def finalize_and_rearm_backlog(request: BacklogRearmRequest) -> BacklogRearmOutcome:
    """Terminalize an owned predecessor and create/reconcile its successor.

    The injected transaction factory must support nesting as a savepoint.  The
    nested insert lets the unique-active-run constraint arbitrate an external
    concurrent writer while preserving the outer predecessor row for a safe
    exact-key reconciliation or a full rollback.
    """
    transaction = get_ext("transaction")
    SchTaskModel = get_db_model("SchTask")
    SchAgentTaskModel = get_db_model("SchAgentTask")
    SchTriggerModel = get_db_model("SchTrigger")
    SchRunModel = get_db_model("SchRun")
    try:
        async with transaction():
            task_rows = await SchTaskModel.filter(id=request.task_id).select_for_update().values()
            if not task_rows:
                return BacklogRearmOutcome(
                    status="task_ineligible", predecessor_run_id=request.predecessor_run_id,
                    reason="task was not found",
                )
            task = task_rows[0]
            # Sample after the task lock.  A lock wait is elapsed authority
            # time; treating a pre-wait timestamp as current would let an
            # expired task or lease write after it had already lapsed.
            task_now = datetime.now(UTC)
            reason = _task_reason(task, request, task_now)
            if reason:
                return BacklogRearmOutcome(
                    status="task_ineligible", predecessor_run_id=request.predecessor_run_id, reason=reason
                )
            predecessor_rows = (
                await SchRunModel.filter(id=request.predecessor_run_id).select_for_update().values()
            )
            if not predecessor_rows:
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor was not found",
                )
            predecessor = predecessor_rows[0]
            now = datetime.now(UTC)
            if (
                str(predecessor.get("task_id") or "") != request.task_id
                or str(predecessor.get("user_id") or "") != request.user_id
                or str(predecessor.get("organization_id") or "") != request.organization_id
            ):
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor binding does not match request",
                )
            # Trigger provenance belongs to the locked run, not merely to the
            # task's current trigger rows. A trigger may be deleted while its
            # claimed run is still alive; that must never convert scheduled
            # execution into authority for the on-demand backlog path.
            if predecessor.get("trigger_id") is not None:
                return BacklogRearmOutcome(
                    status="task_ineligible",
                    predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor was created by a trigger",
                )
            agent_rows = await SchAgentTaskModel.filter(id=request.task_id).select_for_update().values()
            agent_task = agent_rows[0] if agent_rows else None
            trigger_rows = await SchTriggerModel.filter(task_id=request.task_id).select_for_update().values()
            if trigger_rows:
                return BacklogRearmOutcome(
                    status="task_ineligible", predecessor_run_id=request.predecessor_run_id,
                    reason="on-demand task has trigger rows",
                )
            if not await _validate_registered_task(task, agent_task):
                return BacklogRearmOutcome(
                    status="task_ineligible", predecessor_run_id=request.predecessor_run_id,
                    reason="tool task is not registered for backlog rearm",
                )
            # The validator may await.  Re-sample after it and before any
            # authority decision so a task expiring during that wait cannot
            # terminalize or rearm work.
            now = datetime.now(UTC)
            if task.get("expires_at") is not None and task["expires_at"] <= now:
                return BacklogRearmOutcome(
                    status="task_ineligible", predecessor_run_id=request.predecessor_run_id,
                    reason="task is expired",
                )
            predecessor_metadata = predecessor.get("metadata")
            has_rearm_metadata = isinstance(predecessor_metadata, dict) and (
                BACKLOG_REARM_METADATA_KEY in predecessor_metadata
            )
            existing_receipt = predecessor_metadata.get(BACKLOG_REARM_METADATA_KEY) if has_rearm_metadata else None
            if has_rearm_metadata and not _valid_descriptor(existing_receipt):
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor has malformed backlog recovery metadata",
                )
            # A queued successor carries its parent's recovery descriptor so a
            # collision can identify it.  That descriptor is not this run's
            # terminal receipt: its predecessor id names the prior run.  Only
            # a descriptor naming THIS predecessor can close this run to a
            # duplicate retry, and a malformed same-predecessor descriptor
            # fails closed rather than becoming accidental authority.
            if isinstance(existing_receipt, dict) and (
                existing_receipt.get("predecessor_run_id") == request.predecessor_run_id
            ):
                if predecessor.get("status") == "success" and _same_receipt(existing_receipt, request):
                    return BacklogRearmOutcome(
                        status="already_rearmed", predecessor_run_id=request.predecessor_run_id,
                        successor_run_id=existing_receipt["successor_run_id"],
                    )
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor does not have a committed matching backlog receipt",
                )
            if isinstance(existing_receipt, dict) and (
                existing_receipt.get("version") != BACKLOG_REARM_VERSION
                or existing_receipt.get("recovery_key") != request.recovery_key
            ):
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor recovery ancestry does not match request",
                )
            if (
                str(predecessor.get("claim_token") or "") != request.claim_token
                or predecessor.get("status") not in _EXECUTING_STATUSES
                or predecessor.get("claim_expires_at") is None
                or predecessor["claim_expires_at"] <= now
            ):
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor authority is no longer active",
                )

            if predecessor.get("queue") != task.get("queue"):
                return BacklogRearmOutcome(
                    status="authority_lost", predecessor_run_id=request.predecessor_run_id,
                    reason="predecessor queue does not match locked task",
                )
            successor_id, foreign_collision = await _locked_active_successor(task, predecessor, request)
            if foreign_collision:
                raise _CollisionRefused("active run has a different or unmarked recovery key")

            receipt = {**_recovery_metadata(request), "successor_run_id": successor_id}
            # Re-sample immediately before the conditional authority write;
            # validation may itself have waited on host registry state.
            write_now = datetime.now(UTC)
            if task.get("expires_at") is not None and task["expires_at"] <= write_now:
                return BacklogRearmOutcome(
                    status="task_ineligible", predecessor_run_id=request.predecessor_run_id,
                    reason="task expired before terminal write",
                )
            predecessor_patch = {
                "status": "success",
                "finished_at": write_now,
                "claim_token": None,
                "metadata": {
                    **(predecessor_metadata if isinstance(predecessor_metadata, dict) else {}),
                    BACKLOG_REARM_METADATA_KEY: receipt,
                },
            }
            # Result fields come from the bounded worker and are optional so
            # callers that have only a rearm receipt do not erase progress
            # written during the run. Pydantic bounds strings at the request
            # edge; unlike finalize_run, this atomic primitive never truncates
            # or invents a result.
            if request.result_summary is not None:
                predecessor_patch["result_summary"] = request.result_summary
            if request.error_message is not None:
                predecessor_patch["error_message"] = request.error_message
            if request.output_ref is not None:
                predecessor_patch["output_ref"] = request.output_ref
            if request.result_metadata is not None:
                predecessor_patch["result_metadata"] = request.result_metadata
            updated = await SchRunModel.update_where(
                {
                    "id": request.predecessor_run_id,
                    "claim_token": request.claim_token,
                    "status__in": list(_EXECUTING_STATUSES),
                    "claim_expires_at__gt": write_now,
                },
                **predecessor_patch,
            )
            if not updated.updated_rows:
                raise _CollisionRefused("predecessor authority changed while locked")

            if successor_id is None:
                successor_id = str(uuid.uuid4())
                successor_metadata = {
                    "claim_protocol": 2,
                    BACKLOG_REARM_METADATA_KEY: _recovery_metadata(request),
                }
                try:
                    async with transaction():
                        await SchRunModel.create(
                            id=successor_id,
                            task_id=request.task_id,
                            user_id=task["user_id"],
                            organization_id=task["organization_id"],
                            status="queued",
                            queue=task.get("queue"),
                            due_at=request.due_at,
                            metadata=successor_metadata,
                        )
                except Exception as exc:
                    message = str(exc).lower()
                    if "23505" not in message and "duplicate key" not in message:
                        raise
                    successor_id, foreign_collision = await _locked_active_successor(
                        task, predecessor, request
                    )
                    if foreign_collision or successor_id is None:
                        raise _CollisionRefused(
                            "active run collision is not the same recovery successor"
                        ) from exc
                # The receipt is written only after the successor exists or an
                # exact-key collision has been locked and adopted.
                patched = await SchRunModel.update_where(
                    {"id": request.predecessor_run_id, "status": "success"},
                    metadata={
                        **(predecessor_metadata if isinstance(predecessor_metadata, dict) else {}),
                        BACKLOG_REARM_METADATA_KEY: {
                            **_recovery_metadata(request), "successor_run_id": successor_id
                        },
                    },
                )
                if not patched.updated_rows:
                    raise _CollisionRefused("predecessor receipt could not be persisted")

            # This success path has only one reporting effect: stamp the task
            # with the terminal time. Keep it in the same transaction as the
            # predecessor and successor so a process crash cannot omit it and
            # a duplicate retry cannot perform it twice.
            reported = await SchTaskModel.update_where(
                {"id": request.task_id}, last_run_at=write_now
            )
            if not reported.updated_rows:
                raise _CollisionRefused("task completion stamp could not be persisted")

            return BacklogRearmOutcome(
                status="rearmed", predecessor_run_id=request.predecessor_run_id,
                successor_run_id=successor_id,
            )
    except _CollisionRefused as exc:
        return BacklogRearmOutcome(
            status="collision_refused", predecessor_run_id=request.predecessor_run_id, reason=str(exc)
        )
