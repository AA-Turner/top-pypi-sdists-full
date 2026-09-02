"""The Browser Manager ↔ matrx-runtime coordination code — the exact park,
resume, and reconcile protocols of S5.

This is the WS-6 core. It drives the REAL ``matrx-runtime`` ``ExecutionEngine``
(lease / checkpoint / park / resume) and the REAL pending-call ledger seam,
adding only the human-episode orchestration. It contains, deliberately, NO:

  * ``asyncio.sleep`` / ``Future`` / ``Event`` / in-process dict that tracks a
    pending handoff (S5 §9 invariant 1) — the frontier lives in the DB;
  * new abandonment constant (invariant 2) — timing rides
    ``DELEGATED_CALL_ABANDON_AFTER_SECONDS``;
  * write to ``browser.run`` without a ``controller_revision`` predicate
    (invariant 3) — that CAS lives in the Browser Manager / HandoffSource;
  * update to the pending-tool ledger except through the seam (invariant 4).

Every park writes a checkpoint whose kind is ``browser_handoff`` (invariant 5);
the parked state is ``waiting_input``, never ``paused`` (invariant 6).

A killed process is a NON-EVENT: continuity lives entirely in three durable
stores (the runtime ``ExecutionStore``, the ``chat.tool_call`` ledger behind
the seam, and the Browser Manager's ``browser.handoff`` rows). ``Reconciler``
rebuilds every in-flight sequence from those rows alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from enum import StrEnum

from matrx_runtime import (
    ConcurrentTransition,
    ExecutionEngine,
    ExecutionError,
    ExecutionStatus,
)

from matrx_ai.browser_handoff.models import (
    CHECKPOINT_KIND,
    SUSPEND_REASON,
    HandoffOpenRequest,
    HandoffReason,
    HandoffResolution,
    HandoffResolutionKind,
    HandoffSource,
    ParkOutcome,
    WorkerQuiesced,
)
from matrx_ai.browser_handoff.seam import get_handoff_ledger


def _now() -> datetime:
    return datetime.now(UTC)


def resolution_key(handoff_id: str, pending_call_id: str) -> str:
    """The idempotency key (S5 §4.4). Derivable from durable state alone, stable
    across restarts, unique across handoffs on the same run — NEVER a random
    per-attempt id (a per-attempt id makes a retry look like a new operation,
    which is the whole bug)."""
    return f"{handoff_id}:{pending_call_id}"


# Pending-call abandonment window — the SINGLE source of truth (S5 §6). No new
# constant is introduced; a per-tool override rides tools.max_client_wait_seconds.
def _default_expires_at(now: datetime, max_wait_seconds: int | None) -> datetime:
    from matrx_ai.tools.executor import DELEGATED_CALL_ABANDON_AFTER_SECONDS

    return now + timedelta(
        seconds=max_wait_seconds or DELEGATED_CALL_ABANDON_AFTER_SECONDS
    )


@dataclass(frozen=True, slots=True)
class ParkReceipt:
    outcome: ParkOutcome
    handoff_id: str | None = None
    run_id: str | None = None
    resolution_key: str | None = None
    controller_revision: int | None = None
    refusal_reason: str | None = None


@dataclass(frozen=True, slots=True)
class ResumeReceipt:
    resolved: bool  # a pending-call completion happened this call or earlier
    already_resolved: bool
    resume_driven: bool  # this call won the resume-driver CAS (engine.start)
    kind: HandoffResolutionKind
    handoff_id: str
    idempotent: bool = False  # a duplicate that safely no-op'd


class ReconcileActionKind(StrEnum):
    RESUMED_RETURN = "resumed_return"  # died between 4.1 and 4.3
    DISPATCHED_RESUME = "dispatched_resume"  # died between 4.3 and R5
    DROVE_EXPIRY = "drove_expiry"  # claim/claimless window elapsed
    ORPHAN_ALARM = "orphan_alarm"  # park with no handoff row — SCREAM


@dataclass(frozen=True, slots=True)
class ReconcileAction:
    kind: ReconcileActionKind
    execution_id: str
    handoff_id: str | None = None
    detail: str = ""


class BrowserHandoffCoordinator:
    """Drives the park and resume sequences against the real engine + ledger.

    It is stateless beyond its collaborators: a fresh coordinator built after a
    process restart, over the same durable stores, drives every sequence to the
    same terminal state.
    """

    def __init__(self, engine: ExecutionEngine, source: HandoffSource) -> None:
        self._engine = engine
        self._source = source

    # -- PARK (S5 §2) -----------------------------------------------------

    async def park(
        self,
        req: HandoffOpenRequest,
        quiesced: WorkerQuiesced,
        *,
        holder: str | None = None,
        max_wait_seconds: int | None = None,
        now: datetime | None = None,
    ) -> ParkReceipt:
        """P1–P5. On success the caller (the browser tool) ends the stream and
        returns ``delegated_pending`` (P6). Everything here is durable before
        that stream end — the whole point.
        """
        at = now or _now()

        # P1 — a failed drain is a PARK REFUSAL, never a park: no handoff row, no
        # delegated row, no park (S5 §8 #10).
        if not quiesced.queue_drained:
            return ParkReceipt(
                outcome=ParkOutcome.REFUSED,
                refusal_reason="worker_queue_not_drained",
            )

        # P2 — handoff row + controller CAS, in the Browser Manager. A controller
        # conflict (someone else transitioned the run) surfaces as an exception
        # from the source; the tool maps it to browser_controlled_by_human.
        ticket = await self._source.open_handoff(req)
        rkey = resolution_key(ticket.handoff_id, req.pending_call_id)

        # P3 — delegate the pending tool call through the EXISTING path. A
        # PersistenceBarrierError inside finalize aborts the handoff (raises);
        # better a loud failure than a human told to act against a ledger that
        # does not exist. We do NOT catch it here.
        await get_handoff_ledger().delegate(
            call_id=req.pending_call_id,
            conversation_id=req.conversation_id,
            execution_id=req.requested_by_execution_id,
            handoff_id=ticket.handoff_id,
            expires_at=_default_expires_at(at, max_wait_seconds),
        )

        # P4 — checkpoint the pending-tool relationship (recovery input, never
        # authority). kind is exactly CHECKPOINT_KIND (invariant 5).
        await self._engine.save_checkpoint(
            req.requested_by_execution_id,
            {
                "kind": CHECKPOINT_KIND,
                "handoff_id": ticket.handoff_id,
                "run_id": req.run_id,
                "profile_id": req.profile_id,
                "pending_call_id": req.pending_call_id,
                "conversation_id": req.conversation_id,
                "controller_revision": ticket.controller_revision,
                "reason": req.reason.value,
                "suspend_reason": SUSPEND_REASON,
                "resolution_key": rkey,
                "parked_at": at.isoformat(),
            },
        )

        # P5 — holder-verified release to WAITING_INPUT (never PAUSED, invariant 6).
        # When we hold the lease, release_to_waiting honours a False return (we
        # lost the lease to a takeover — must NOT park the new owner's run).
        if holder is not None:
            parked = await self._engine.release_to_waiting(
                req.requested_by_execution_id, holder=holder
            )
            if not parked:
                # Lease lost mid-park; do not park the new owner's live run.
                return ParkReceipt(
                    outcome=ParkOutcome.REFUSED,
                    refusal_reason="lease_lost_during_park",
                    handoff_id=ticket.handoff_id,
                )
        else:
            await self._engine.request_input(req.requested_by_execution_id)

        return ParkReceipt(
            outcome=ParkOutcome.PARKED,
            handoff_id=ticket.handoff_id,
            run_id=ticket.run_id,
            resolution_key=rkey,
            controller_revision=ticket.controller_revision,
        )

    # -- RESUME (S5 §3) ---------------------------------------------------

    async def resume(
        self,
        handoff_id: str,
        *,
        user_id: str,
        outcome_label: str | None = None,
        holder: str,
        lease_seconds: float | None = None,
    ) -> ResumeReceipt:
        """R1–R5, driven by a human clicking Return control. Safe under N
        concurrent callers: the human-episode CAS elects one closer, the ledger
        CAS elects one tool-completer, and ``engine.start`` elects one resume
        driver — every loser returns a success-shaped idempotent result."""
        # R1–R3 happen inside the Browser Manager: disable input, capture page
        # inventory with input off, mint the fresh fencing token, and CAS the
        # human episode closed. A duplicate return re-reads the same stored
        # resolution (idempotent replay, S5 §4.4) rather than re-driving.
        resolution = await self._source.return_control(
            handoff_id, user_id=user_id, outcome_label=outcome_label
        )
        return await self._drive_resolution(
            resolution, holder=holder, lease_seconds=lease_seconds
        )

    async def _drive_resolution(
        self,
        resolution: HandoffResolution,
        *,
        holder: str,
        lease_seconds: float | None = None,
    ) -> ResumeReceipt:
        # R4 — complete the pending tool call EXACTLY ONCE via the seam CAS.
        receipt = await get_handoff_ledger().resolve(resolution)

        if receipt.not_found:
            # An unknown call is a real defect — surface loudly (S5 §9 #8).
            await self._engine.record_note(
                resolution.execution_id,
                label="browser_handoff_resolution_not_found",
                detail={"handoff_id": resolution.handoff_id},
            )

        # On the winning tool-completion, stamp the episode returned (S5 R4).
        if receipt.resolved:
            await self._source.mark_tool_resolved(resolution.handoff_id)

        # R5 — claim the resume: WAITING_INPUT → RUNNING is itself a CAS in the
        # engine, so N duplicate resumes elect exactly one driver; the losers get
        # ConcurrentTransition and return an idempotent success.
        resume_driven = False
        if receipt.continuation_needed or resolution.kind is HandoffResolutionKind.EXPIRED:
            resume_driven = await self._claim_resume(
                resolution.execution_id, holder=holder, lease_seconds=lease_seconds
            )
            if resume_driven:
                await self._source.mark_resume_dispatched(resolution.handoff_id)

        return ResumeReceipt(
            resolved=receipt.resolved or receipt.already_resolved,
            already_resolved=receipt.already_resolved,
            resume_driven=resume_driven,
            kind=resolution.kind,
            handoff_id=resolution.handoff_id,
            idempotent=receipt.already_resolved and not resume_driven,
        )

    async def _claim_resume(
        self, execution_id: str, *, holder: str, lease_seconds: float | None
    ) -> bool:
        ex = await self._engine.get_execution(execution_id)
        if ex is None or ex.status is not ExecutionStatus.WAITING_INPUT:
            # Already resumed / completed by another driver — idempotent.
            return False
        try:
            await self._engine.start(
                execution_id, holder=holder, lease_seconds=lease_seconds
            )
        except ConcurrentTransition:
            return False
        return True


class Reconciler:
    """The boot-time + interval sweep that makes a manager restart mid-sequence
    a non-event (S5 §4.4). It re-drives every in-flight sequence from durable
    rows alone — no in-memory map, no per-handoff timer, no process-local
    'already resumed' set. Every step it re-drives is CAS-guarded, so an
    optional per-row lease would be throughput, not correctness."""

    def __init__(
        self, engine: ExecutionEngine, source: HandoffSource, *, holder: str
    ) -> None:
        self._engine = engine
        self._source = source
        self._holder = holder
        self._coord = BrowserHandoffCoordinator(engine, source)

    async def run(
        self, *, now: datetime | None = None, scan_limit: int = 500
    ) -> list[ReconcileAction]:
        at = now or _now()
        actions: list[ReconcileAction] = []
        parked = await self._engine.list_recent(
            status=ExecutionStatus.WAITING_INPUT, limit=scan_limit
        )
        for ex in parked:
            cp = await self._engine.latest_checkpoint(ex.id)
            if cp is None or cp.state.get("kind") != CHECKPOINT_KIND:
                continue
            handoff_id = cp.state.get("handoff_id")
            record = await self._source.get_handoff_or_none(handoff_id)

            if record is None:
                # Orphaned park — should be impossible (P2 precedes P3). SCREAM,
                # then close the execution so it is never stranded (S5 §4.4).
                await self._engine.record_note(
                    ex.id,
                    label="browser_handoff_orphaned_park",
                    detail={"handoff_id": handoff_id},
                )
                await self._engine.fail(
                    ex.id,
                    error=ExecutionError(
                        error_type="browser_handoff_orphaned_park",
                        message=(
                            f"execution {ex.id} parked on browser handoff "
                            f"{handoff_id!r} with no matching handoff row."
                        ),
                    ),
                    cost=ex.cost,
                )
                actions.append(
                    ReconcileAction(
                        ReconcileActionKind.ORPHAN_ALARM,
                        execution_id=ex.id,
                        handoff_id=handoff_id,
                    )
                )
                continue

            action = await self._reconcile_one(ex, record, at=at)
            if action is not None:
                actions.append(action)
        return actions

    async def _reconcile_one(self, ex, record, *, at: datetime):
        state = record.state

        # died between 4.1 and 4.3 — re-run R4–R5 from the row.
        if state == "returning" and record.tool_resolved_at is None:
            resolution = await self._source.resolution_for(record.handoff_id)
            await self._coord._drive_resolution(resolution, holder=self._holder)
            return ReconcileAction(
                ReconcileActionKind.RESUMED_RETURN,
                execution_id=ex.id,
                handoff_id=record.handoff_id,
            )

        # died between 4.3 and R5 — just open the resume.
        if (
            state == "returned"
            and record.resume_dispatched_at is None
            and ex.status is ExecutionStatus.WAITING_INPUT
        ):
            driven = await self._coord._claim_resume(ex.id, holder=self._holder, lease_seconds=None)
            if driven:
                await self._source.mark_resume_dispatched(record.handoff_id)
            return ReconcileAction(
                ReconcileActionKind.DISPATCHED_RESUME,
                execution_id=ex.id,
                handoff_id=record.handoff_id,
            )

        # claimed-but-disconnected human past the reconnect window → expiry.
        if (
            state == "claimed"
            and record.reconnect_deadline is not None
            and at >= record.reconnect_deadline
        ):
            return await self._drive_expiry(ex, record)

        # nobody ever claimed past the claim window → expiry.
        if (
            state == "requested"
            and record.expires_at is not None
            and at >= record.expires_at
        ):
            return await self._drive_expiry(ex, record)

        return None

    async def _drive_expiry(self, ex, record) -> ReconcileAction:
        resolution = await self._source.expire(record.handoff_id)
        await self._coord._drive_resolution(resolution, holder=self._holder)
        return ReconcileAction(
            ReconcileActionKind.DROVE_EXPIRY,
            execution_id=ex.id,
            handoff_id=record.handoff_id,
        )
