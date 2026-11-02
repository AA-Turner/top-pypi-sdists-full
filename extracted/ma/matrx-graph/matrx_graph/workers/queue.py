"""Thin work queue over wf_job.

Uses plain Postgres (FOR UPDATE SKIP LOCKED, via matrx-orm's ``claim_batch``
primitive) for portability. If the pgmq extension is installed, swap
``claim_one`` / ``enqueue`` bodies for pgmq calls — the public surface here
stays identical.

Workers call ``claim_one``, process the returned ``Job`` via
``matrx_graph.workers.runner``, then call ``complete`` / ``fail`` / ``release``.
Terminal rows are retained as the queue's audit record and as the prerequisite
for a storage-enforced idempotency guard. The
current schema has no explicit state column, so terminal state is encoded in
``last_error.queue_state`` and made non-claimable through ``visible_at`` while
the linked run's terminal status provides an independent claim guard.

All DB access goes through matrx-orm Models resolved via
``matrx_graph.db._registry.get_model`` — the same host-injected ``WfJob``
model the scheduler + checkpointer already share.
"""

from __future__ import annotations

import json
import logging
import os
import socket
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from matrx_utils import compute_backoff_ms

from matrx_graph.failure import classification_text

log = logging.getLogger("matrx_graph.workers.queue")

JobKind = Literal["start", "resume"]
_RETRYABLE_HTTP_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})
_FAR_FUTURE_DAYS = 36_500
_RETRY_INITIAL_MS = 30_000
_RETRY_MAX_MS = 300_000


class FailureClass(StrEnum):
    """Worker-level failure disposition."""

    RETRYABLE = "retryable"
    TERMINAL = "terminal"


class FailureDisposition(BaseModel):
    """Classified worker failure used by queue retry policy and audit rows."""

    model_config = ConfigDict(frozen=True)

    failure_class: FailureClass
    reason: str
    status_code: int | None = None

    @property
    def retryable(self) -> bool:
        return self.failure_class is FailureClass.RETRYABLE


class Job(BaseModel):
    """One workflow execution unit in the queue."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    run_id: str
    kind: JobKind
    checkpoint_id: str | None = None
    resume_value: dict[str, Any] = Field(default_factory=dict)
    inputs: dict[str, Any] = Field(default_factory=dict)
    max_steps: int = 1000
    attempt: int = 0
    max_attempts: int = 3
    claimed_by: str | None = None
    # WHO answered, stamped by the trusted seam that queued this resume (``enqueue(decision=...)``,
    # stored in the job row's ``metadata.decision``). Never read from ``resume_value``.
    decision: dict[str, Any] | None = None


def classify_failure(error: BaseException) -> FailureDisposition:
    """Classify a worker-level exception as retryable or terminal.

    Only infrastructure failures with a concrete transient signal are retried.
    Programming/configuration failures default to terminal instead of consuming
    the retry budget three times. HTTP 408/425/429/5xx and timeout/connection
    families are retryable; other HTTP 4xx responses are terminal.
    """
    current: BaseException | None = error
    seen: set[int] = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        status_code = _status_code(current)
        if status_code is not None:
            if status_code in _RETRYABLE_HTTP_STATUSES:
                return FailureDisposition(
                    failure_class=FailureClass.RETRYABLE,
                    reason=f"http_{status_code}",
                    status_code=status_code,
                )
            if 400 <= status_code < 500:
                return FailureDisposition(
                    failure_class=FailureClass.TERMINAL,
                    reason=f"http_{status_code}",
                    status_code=status_code,
                )

        if isinstance(current, TimeoutError | ConnectionError):
            return FailureDisposition(
                failure_class=FailureClass.RETRYABLE,
                reason=type(current).__name__,
                status_code=status_code,
            )

        type_name = type(current).__name__.lower()
        # THE SAME RULE AS matrx_graph.failure: a classifier reads the
        # exception's own diagnosis, never the payload the ORM renders after
        # "Args:" — which is the run's data, i.e. what a person wrote. A
        # document that says "connection refused" must not decide whether we
        # burn this job's retry budget (2026-09-12, run 053e8b72).
        message = classification_text(str(current)).lower()
        if any(
            token in type_name
            for token in (
                "timeout",
                "connection",
                "connecterror",
                "network",
                "transporterror",
                "readerror",
                "writeerror",
                "protocolerror",
                "ratelimit",
                "serviceunavailable",
                "temporar",
                "transient",
            )
        ) or any(
            token in message
            for token in (
                "connection reset",
                "connection refused",
                "server closed the connection",
                "too many requests",
                "rate limit",
                "deadlock detected",
                "serialization failure",
                "pool timeout",
                "temporarily unavailable",
            )
        ):
            return FailureDisposition(
                failure_class=FailureClass.RETRYABLE,
                reason=type(current).__name__,
                status_code=status_code,
            )
        current = current.__cause__ or current.__context__

    return FailureDisposition(
        failure_class=FailureClass.TERMINAL,
        reason=type(error).__name__,
        status_code=_status_code(error),
    )


def retry_delay_seconds(attempt: int) -> int:
    """Bounded exponential backoff with jitter for a failed queue attempt."""
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    delay_ms = compute_backoff_ms(
        attempt,
        initial_ms=_RETRY_INITIAL_MS,
        max_ms=_RETRY_MAX_MS,
        strategy="exponential_jitter",
    )
    return max(1, (delay_ms + 999) // 1000)


def _status_code(error: BaseException) -> int | None:
    raw = getattr(error, "status_code", None)
    if raw is None:
        raw = getattr(getattr(error, "response", None), "status_code", None)
    return raw if isinstance(raw, int) else None


_SETTLED_STATES = ("succeeded", "dead_letter")


def _terminal_marker(queue_state: str, **details: Any) -> dict[str, Any]:
    return {"queue_state": queue_state, **details}


def _far_future() -> datetime:
    return datetime.now(UTC) + timedelta(days=_FAR_FUTURE_DAYS)


def _worker_id() -> str:
    return f"{socket.gethostname()}:{os.getpid()}"


def _claim_token(worker_id: str | None = None) -> str:
    return f"{worker_id or _worker_id()}:{uuid4()}"


async def enqueue(
    *,
    run_id: str,
    kind: JobKind,
    inputs: dict[str, Any] | None = None,
    checkpoint_id: str | None = None,
    resume_value: dict[str, Any] | None = None,
    max_steps: int = 1000,
    priority: int = 0,
    visible_at: datetime | None = None,
    required_node_types: list[str] | None = None,
    decision: Any = None,
) -> str:
    """Enqueue a new job. Returns the job_id.

    ``decision`` (a ``DecisionProvenance``): WHO answered, for a resume admitted by a
    trusted seam (the signed-in person's route, the escalation sweeper). It is stored in the
    job row's ``metadata.decision`` and handed to ``Scheduler.resume(decision=...)``; a
    ``matrx_decision`` inside ``resume_value`` is caller data and is always stripped.

    The run row (wf_run) must exist — foreign-key enforced. The router
    creates the run row first, then calls enqueue.

    ``required_node_types`` — the node types the run's graph needs (see
    ``workers/capability.py``); omitted → read from the run's stored
    definition. Only a worker that has every one of them claims the job.
    """
    from matrx_graph.db._registry import get_model
    from matrx_utils import refuse_detached_work_if_forbidden

    # A queued job runs on a worker process: the caller's request-scoped checks cannot follow it
    # (matrx-ai's request firewall refuses here while one is open).
    refuse_detached_work_if_forbidden("a queued workflow job")

    # workflow.job.organization_id is NOT NULL. A job is a CHILD of its run
    # (FK-enforced — the row must already exist), so carry the parent's
    # organization rather than a default or the caller's ambient context.
    run_uuid = str(UUID(run_id))
    run_rows = await get_model("WfRun").filter(id=run_uuid).values("organization_id")
    organization_id = run_rows[0].get("organization_id") if run_rows else None
    if not organization_id:
        raise ValueError(
            f"enqueue: run {run_id!r} has no resolvable organization_id — "
            "refusing to enqueue a job with no organization"
        )

    job_id = str(uuid4())
    await get_model("WfJob").create(
        id=job_id,
        run_id=run_uuid,
        organization_id=organization_id,
        kind=kind,
        checkpoint_id=str(UUID(checkpoint_id)) if checkpoint_id else None,
        resume_value=resume_value or {},
        inputs=inputs or {},
        max_steps=max_steps,
        priority=priority,
        visible_at=visible_at or datetime.now(UTC),
        metadata={
            **await _requirement_metadata(run_uuid, required_node_types),
            **({DECISION_METADATA_KEY: _decision_json(decision)} if decision is not None else {}),
        },
    )
    return job_id


#: The job row's metadata key holding the trusted seam's decision stamp.
DECISION_METADATA_KEY = "decision"


def _decision_json(decision: Any) -> dict[str, Any]:
    from matrx_graph.decisions import DecisionProvenance

    return DecisionProvenance.model_validate(decision).model_dump(mode="json")


async def _requirement_metadata(run_id: str, required: list[str] | None) -> dict[str, Any]:
    from matrx_graph.workers.capability import (
        REQUIRED_NODE_TYPES_KEY,
        required_node_types_for_run,
    )

    if required is None:
        required = await required_node_types_for_run(run_id)
    return {REQUIRED_NODE_TYPES_KEY: sorted(set(required))}


async def enqueue_claimed(
    *,
    run_id: str,
    kind: JobKind,
    inputs: dict[str, Any] | None = None,
    max_steps: int = 1000,
    worker_id: str | None = None,
    visibility_timeout_seconds: int = 600,
    required_node_types: list[str] | None = None,
) -> Job:
    """Enqueue a job ALREADY CLAIMED by this worker, under a lease (lane 11 round 5).

    For a caller that runs the job in its own process right now (a verified store-trigger
    fire's first leg) but must keep the queue's guarantees: the row exists, leased to this
    worker, BEFORE the work starts. If this process dies, the lease expires,
    ``reap_expired_leases`` releases it, and any worker's ``claim_one`` runs it as an
    ordinary job. The caller must settle it like ``WorkerRunner._process`` does.
    """
    from matrx_graph.db._registry import get_model

    run_uuid = str(UUID(run_id))
    run_rows = await get_model("WfRun").filter(id=run_uuid).values("organization_id")
    organization_id = run_rows[0].get("organization_id") if run_rows else None
    if not organization_id:
        raise ValueError(
            f"enqueue_claimed: run {run_id!r} has no resolvable organization_id — "
            "refusing to enqueue a job with no organization"
        )
    job_id = str(uuid4())
    worker = _claim_token(worker_id)
    now = datetime.now(UTC)
    await get_model("WfJob").create(
        id=job_id,
        run_id=run_uuid,
        organization_id=organization_id,
        kind=kind,
        checkpoint_id=None,
        resume_value={},
        inputs=inputs or {},
        max_steps=max_steps,
        priority=0,
        claimed_at=now,
        claimed_by=worker,
        visible_at=now + timedelta(seconds=visibility_timeout_seconds),
        attempt=1,
        # Stamped even though THIS worker runs it: if it dies, the reaped job
        # must only go to a worker that can run it too.
        metadata=await _requirement_metadata(run_uuid, required_node_types),
    )
    return Job(
        job_id=job_id,
        run_id=run_uuid,
        kind=kind,
        inputs=inputs or {},
        max_steps=max_steps,
        attempt=1,
        claimed_by=worker,
    )


async def claim_one(
    *,
    worker_id: str | None = None,
    visibility_timeout_seconds: int = 600,
    capabilities: list[str] | None = None,
) -> Job | None:
    """Claim the next ready job (highest priority, oldest visible_at first).

    ``capabilities`` — the node types this worker can execute. When given,
    only a job whose ``metadata.required_node_types`` is contained in it is
    claimable (a job with no stamped requirement is claimable by anyone);
    see ``workers/capability.py``. ``None`` claims without the filter.

    Only unclaimed rows are eligible (``claimed_at IS NULL``) — an expired
    lease is NOT re-claimed here. Worker-crash recovery is the reaper's job:
    ``reap_expired_leases`` nulls ``claimed_at`` on dead leases, after which
    this claim picks them up normally. Healthy long-running jobs stay safe
    because ``WorkerRunner`` renews the lease while executing.
    Returns None if the queue is empty.
    """
    from matrx_orm import (
        ArrayAny,
        ColumnComparison,
        Compare,
        Exists,
        F,
        Now,
        OuterRef,
    )

    from matrx_graph.db._registry import get_model
    from matrx_graph.workers.capability import capability_predicate

    # ``claimed_by`` is a per-CLAIM fencing token, not merely a process label.
    # The stable prefix keeps operator logs readable; the UUID prevents two
    # runner loops in one process (or PID reuse) from settling each other's
    # reclaimed lease.
    worker = _claim_token(worker_id)
    lease_until = datetime.now(UTC) + timedelta(seconds=visibility_timeout_seconds)

    # Single-statement atomic claim via matrx-orm's claim_batch primitive:
    # UPDATE ... WHERE pk IN (SELECT ... FOR UPDATE SKIP LOCKED) RETURNING.
    # The join against workflow.run is expressed as a typed correlated Exists,
    # rather than an actual JOIN, so the inner claim
    # SELECT stays single-table and FOR UPDATE SKIP LOCKED unambiguously
    # targets only workflow.job — splitting this into a SELECT-then-UPDATE
    # would reopen the double-claim race SKIP LOCKED exists to close.
    predicate = Compare(F("j.visible_at"), "<=", Now()) & Exists(
        get_model("WfRun").filter(
            ColumnComparison(F("id"), "=", OuterRef("run_id")),
            ~ArrayAny(
                F("status"),
                ["completed", "failed", "cancelled", "errored"],
                cast="text[]",
            ),
        )
    )
    if capabilities is not None:
        # CAPABILITY-AWARE CLAIM: never hand this worker a graph it cannot run.
        predicate = predicate & capability_predicate(capabilities, metadata_column="j.metadata")
    rows = await get_model("WfJob").claim_batch(
        set_fields={
            "claimed_at": Now(),
            "claimed_by": worker,
            "visible_at": lease_until,
            "attempt": F("attempt") + 1,
        },
        filters={"claimed_at": None},
        predicate=predicate,
        order_by=["-priority", "visible_at"],
        limit=1,
        alias="j",
        returning=[
            "id",
            "run_id",
            "kind",
            "checkpoint_id",
            "resume_value",
            "inputs",
            "max_steps",
            "attempt",
            "max_attempts",
            "claimed_by",
            "metadata",
        ],
    )

    row = rows[0] if rows else None
    if row is None:
        return None
    return Job(
        job_id=str(row["id"]),
        run_id=str(row["run_id"]),
        kind=row["kind"],
        checkpoint_id=str(row["checkpoint_id"]) if row["checkpoint_id"] else None,
        resume_value=_parse_json(row["resume_value"]) or {},
        inputs=_parse_json(row["inputs"]) or {},
        max_steps=row["max_steps"],
        attempt=row["attempt"],
        max_attempts=row["max_attempts"],
        claimed_by=row["claimed_by"],
        decision=(_parse_json(row.get("metadata")) or {}).get(DECISION_METADATA_KEY),
    )


async def complete(job_id: str, *, claimed_by: str | None = None) -> None:
    """Retain a successful row as terminal audit state. Idempotent.

    ``claimed_by`` fences the transition against an expired lease that another
    worker already reclaimed. Legacy callers may omit it; WorkerRunner never
    does. ``visible_at`` plus the linked terminal run make the retained row
    unclaimable under the current no-status-column schema.
    """
    try:
        from matrx_graph.db._registry import get_model

        filters: dict[str, Any] = {"id": str(UUID(job_id))}
        if claimed_by is not None:
            filters["claimed_by"] = claimed_by
        result = await get_model("WfJob").update_where(
            filters,
            claimed_at=None,
            claimed_by=None,
            visible_at=_far_future(),
            last_error=_terminal_marker("succeeded", type="terminal_success"),
        )
        if claimed_by is not None and result.rows_affected == 0:
            log.error(
                "wf_job.complete: ownership fence rejected job %s for worker %s; "
                "another worker may own the reclaimed lease",
                job_id,
                claimed_by,
            )
    except Exception as exc:
        log.warning(
            "wf_job.complete: terminal UPDATE failed for %s — %s: %s. "
            "wf_run status is already terminal; alerting via watchdog.",
            job_id,
            type(exc).__name__,
            exc,
        )


async def discard_for_run(run_id: str) -> int:
    """Retain every UNCLAIMED queued job for a terminal run. Returns rows marked.

    Called when a run reaches a terminal state through a path OTHER than a
    worker draining its own (claimed) job — force-fail, the stranded-run
    watchdog, an inline run that finished, or a cancel that landed before any
    worker claimed the job. Those paths set ``wf_run.status`` terminal but
    historically left the queued ``wf_job`` row behind, where it sat forever
    as a false "pending work" signal (the 2026-06 zombie-job incident: 3
    'start' jobs whose runs were force-failed two months earlier).

    Scoped to ``claimed_at IS NULL`` so it can NEVER yank a job out from under
    a live worker that is mid-finalize (that worker owns the claim and settles
    its own row via ``complete`` / dead-letters via ``fail``). Idempotent and
    failure-swallowing for the same reason ``complete`` is: terminal cleanup of
    a secondary row must never block or crash the caller's terminal write.
    """
    try:
        from matrx_graph.db._registry import get_model

        model = get_model("WfJob")
        # A row already settled (``complete`` marked it succeeded, ``fail`` dead-lettered it) keeps its marker: a
        # parked run's start job succeeded when it parked, and must not read "dead letter" once the run ends.
        rows = await model.filter(run_id=str(UUID(run_id)), claimed_at__isnull=True).values("id", "last_error")
        ids = [
            str(r["id"])
            for r in rows
            if not (isinstance(r.get("last_error"), dict) and r["last_error"].get("queue_state") in _SETTLED_STATES)
        ]
        if not ids:
            return 0
        result = await model.update_where(
            {
                "id__in": ids,
                "claimed_at__isnull": True,
            },
            visible_at=_far_future(),
            last_error=_terminal_marker(
                "dead_letter",
                type="run_terminal_before_claim",
                retryable=False,
            ),
        )
        return result.rows_affected
    except Exception as exc:
        log.warning(
            "wf_job.discard_for_run: terminal UPDATE failed for run %s — %s: %s. "
            "wf_run is already terminal and claim_one refuses terminal-run "
            "jobs, so a lingering row is harmless; alerting via watchdog.",
            run_id,
            type(exc).__name__,
            exc,
        )
        return 0


async def fail(
    job_id: str,
    *,
    error: dict[str, Any],
    retry_in_seconds: int | None = None,
    retryable: bool = True,
    attempt: int | None = None,
    max_attempts: int | None = None,
    claimed_by: str | None = None,
) -> None:
    """Release the job with a failure payload.

    If the failure is retryable, the linked run remains claimable, and attempt
    < max_attempts, the job reappears after explicit ``retry_in_seconds`` or the
    canonical bounded exponential backoff with jitter. Terminal failures
    dead-letter immediately.
    Otherwise it is dead-lettered: visible_at is pushed to the far future so
    claim_one can never pick it up again (operators inspect and decide).
    Leaving visible_at at the old lease deadline — the previous behavior —
    silently re-queued "exhausted" jobs once that timestamp passed, an
    infinite retry loop with a lease-length period.

    ``attempt`` / ``max_attempts`` come from the row returned by the atomic
    claim; a caller that omits them gets the row's REAL counters, never an
    assumed first attempt. A fixed ``attempt=1`` default silently resurrected
    an exhausted job on every such call — the same infinite-retry class this
    function exists to kill, just with a backoff-length period instead of a
    lease-length one.
    """
    from matrx_graph.db._registry import get_model

    far_future = _far_future()
    filters: dict[str, Any] = {"id": str(UUID(job_id))}
    if claimed_by is not None:
        filters["claimed_by"] = claimed_by

    # A terminal failure dead-letters regardless of the counters, so it never
    # pays for the lookup below. Only the retry decision needs to know how many
    # attempts this row has actually burned.
    if retryable and (attempt is None or max_attempts is None):
        row = await get_model("WfJob").get_or_none(id=str(UUID(job_id)))
        if attempt is None:
            attempt = int(getattr(row, "attempt", 0) or 0) if row is not None else 0
        if max_attempts is None:
            max_attempts = int(getattr(row, "max_attempts", 3) or 3) if row is not None else 3

    if not retryable or attempt >= max_attempts:
        terminal_error = {
            **error,
            "queue_state": "dead_letter",
            "retryable": retryable,
        }
        if retryable:
            terminal_error["retry_exhausted"] = True
        result = await get_model("WfJob").update_where(
            filters,
            claimed_at=None,
            claimed_by=None,
            last_error=terminal_error,
            visible_at=far_future,
        )
        if claimed_by is not None and result.rows_affected == 0:
            log.error(
                "wf_job.fail: ownership fence rejected terminal failure for job %s / worker %s",
                job_id,
                claimed_by,
            )
        return

    # The attempt/max_attempts values come from the row returned by the atomic
    # claim (or, for a caller that omitted them, from the row itself above).
    # Ownership fencing prevents a stale claimant from applying this
    # transition after another worker has reclaimed the row.
    delay_seconds = (
        retry_in_seconds if retry_in_seconds is not None else retry_delay_seconds(attempt)
    )
    next_visible = datetime.now(UTC) + timedelta(seconds=delay_seconds)
    retry_error = {
        **error,
        "queue_state": "pending",
        "retryable": True,
        "retry_delay_seconds": delay_seconds,
    }
    result = await get_model("WfJob").update_where(
        filters,
        claimed_at=None,
        claimed_by=None,
        last_error=retry_error,
        visible_at=next_visible,
    )
    if claimed_by is not None and result.rows_affected == 0:
        log.error(
            "wf_job.fail: ownership fence rejected retry transition for job %s / worker %s",
            job_id,
            claimed_by,
        )


async def defer_for_capability(
    job_id: str,
    *,
    required_node_types: list[str],
    claimed_by: str | None = None,
) -> None:
    """Hand a claimed job back because THIS worker cannot run its graph.

    Not a failure and not an attempt: the claim's attempt bump is undone, the
    job is immediately visible again, and its requirement is stamped so a
    capability-filtered ``claim_one`` never offers it to this worker again.
    """
    from matrx_orm import F, JsonbMerge

    from matrx_graph.db._registry import get_model
    from matrx_graph.workers.capability import REQUIRED_NODE_TYPES_KEY

    filters: dict[str, Any] = {"id": str(UUID(job_id))}
    if claimed_by is not None:
        filters["claimed_by"] = claimed_by
    result = await get_model("WfJob").update_where(
        filters,
        claimed_at=None,
        claimed_by=None,
        visible_at=datetime.now(UTC),
        attempt=F("attempt") - 1,
        metadata=JsonbMerge(
            "metadata", {REQUIRED_NODE_TYPES_KEY: sorted(set(required_node_types))}
        ),
    )
    if claimed_by is not None and result.rows_affected == 0:
        log.error(
            "wf_job.defer_for_capability: ownership fence rejected job %s for worker %s",
            job_id,
            claimed_by,
        )


async def release(job_id: str, *, claimed_by: str | None = None) -> None:
    """Release without failure — used when a worker shuts down mid-job."""
    from matrx_graph.db._registry import get_model

    filters: dict[str, Any] = {"id": str(UUID(job_id))}
    if claimed_by is not None:
        filters["claimed_by"] = claimed_by
    result = await get_model("WfJob").update_where(
        filters,
        claimed_at=None,
        claimed_by=None,
    )
    if claimed_by is not None and result.rows_affected == 0:
        log.error(
            "wf_job.release: ownership fence rejected job %s for worker %s",
            job_id,
            claimed_by,
        )


class JobHandedBack(Exception):  # noqa: N818 — a hand-back, not an error
    """The job runner stopped because its process is being replaced, and the run is
    already parked resumable. The runner turns the SAME job row into the run's
    continuation (``hand_back``) instead of failing it: one row, so a deploy can never
    leave two jobs able to drive one run (live 2026-10-27, five runs ran twice)."""

    def __init__(
        self,
        *,
        kind: JobKind,
        checkpoint_id: str | None,
        resume_value: dict[str, Any] | None = None,
        reason: str = "deploy_drain",
    ) -> None:
        super().__init__(f"job handed back ({reason}) as {kind} from {checkpoint_id or 'its inputs'}")
        self.kind: JobKind = kind
        self.checkpoint_id = checkpoint_id
        self.resume_value = resume_value or {}
        self.reason = reason


async def hand_back(
    job_id: str,
    *,
    claimed_by: str | None,
    kind: JobKind,
    checkpoint_id: str | None,
    resume_value: dict[str, Any] | None = None,
    reason: str = "deploy_drain",
    attempt: int | None = None,
) -> bool:
    """Release a claimed job AS its run's continuation, visible now, no attempt spent.

    The draining process's lease ends here (durable-work-queue standard, Phase 4:
    "On SIGTERM ... release held leases before exit"), and the row becomes the job
    another worker claims to continue the run from ``checkpoint_id`` (or start it
    again from its inputs when ``kind='start'``). Fenced by ``claimed_by``: a copy
    that no longer owns the job changes nothing. Returns whether the row moved.
    ``attempt`` is the claim's attempt (the row's counter after the claim's bump); the
    row goes back to one less, so a deploy never spends an attempt.
    """
    from matrx_orm import F

    from matrx_graph.db._registry import get_model

    filters: dict[str, Any] = {"id": str(UUID(job_id))}
    if claimed_by is not None:
        filters["claimed_by"] = claimed_by
    result = await get_model("WfJob").update_where(
        filters,
        claimed_at=None,
        claimed_by=None,
        visible_at=datetime.now(UTC),
        attempt=max(int(attempt) - 1, 0) if attempt is not None else F("attempt") - 1,
        kind=kind,
        checkpoint_id=str(UUID(checkpoint_id)) if checkpoint_id else None,
        resume_value=resume_value or {},
        last_error={"queue_state": "pending", "type": "handed_back", "reason": reason},
    )
    if result.rows_affected == 0:
        log.error(
            "wf_job.hand_back: ownership fence rejected job %s for worker %s; the run "
            "it was handing back is parked and the lease reaper will release the job",
            job_id,
            claimed_by,
        )
        return False
    return True


async def superseded_by(job: Job) -> str | None:
    """The id of a NEWER job for the same run, or None when this job is the newest.

    Every job after the first is a continuation decision (a recovery resume, a person's
    retry, a hand-back) that replaces whatever came before it, so an older job that is
    still claimable is stale and must never drive the run: it would run a second
    scheduler beside the newer one. Live 2026-10-27: a deploy-drained START job came
    back on its retry after the recovery sweep had already queued the RESUME, and both
    ran each of five runs to the end.
    """
    from matrx_orm import Compare, F

    from matrx_graph.db._registry import get_model

    model = get_model("WfJob")
    own = await model.filter(id=str(UUID(job.job_id))).values("created_at")
    if not own or own[0].get("created_at") is None:
        return None
    newer = await (
        model.filter(Compare(F("created_at"), ">", own[0]["created_at"]), run_id=str(UUID(job.run_id)))
        .order_by("-created_at")
        .limit(1)
        .values("id")
    )
    return str(newer[0]["id"]) if newer else None


async def renew_lease(
    job_id: str,
    *,
    visibility_timeout_seconds: int = 600,
    claimed_by: str | None = None,
) -> bool:
    """Extend a claimed job's lease. Returns False if the row is no longer
    claimed (completed, reaped, or released) — the caller lost ownership.
    """
    from matrx_graph.db._registry import get_model

    lease_until = datetime.now(UTC) + timedelta(seconds=visibility_timeout_seconds)
    filters: dict[str, Any] = {
        "id": str(UUID(job_id)),
        "claimed_at__isnull": False,
    }
    if claimed_by is not None:
        filters["claimed_by"] = claimed_by
    result = await get_model("WfJob").update_where(
        filters,
        visible_at=lease_until,
    )
    return result.rows_affected > 0


async def take_back_false_dead_letter(
    job_id: str,
    *,
    claimed_by: str | None,
    visibility_timeout_seconds: int = 600,
) -> bool:
    """A live copy whose job the reaper DEAD-LETTERED (a false "dead": an outage outlasted the lease on the job's last
    attempt) takes the job back, so it finishes the run and writes its terminal status (lane K1b, B1, 2026-10-21).

    Without this the live copy read "not ours", cancelled itself and skipped its terminal write, and no other copy would
    ever claim a dead-lettered job: the run stayed non-terminal (stranded) for every job kind. A dead-lettered job has
    no other owner, so taking it back can never run two copies. Compare-and-set: only a row that is still unclaimed,
    still dead-lettered BY THE REAPER (``last_error.type == 'lease_expired'``) and still parked in the far future
    (an operator's retry moves ``visible_at`` back) is taken; anything else answers False and the copy stops.
    """
    from matrx_graph.db._registry import get_model

    model = get_model("WfJob")
    try:
        rows = await model.filter(id=str(UUID(job_id))).all(use_cache=False)
    except Exception:  # noqa: BLE001 — unreadable: not taken back (the caller decides on the renewal's answer)
        log.warning("could not read job %s to see whether the reaper dead-lettered it", job_id[:8], exc_info=True)
        return False
    if not rows:
        return False
    row = rows[0]
    get = row.get if isinstance(row, dict) else lambda k: getattr(row, k, None)
    note = _parse_json(get("last_error")) or {}
    if get("claimed_at") is not None or not isinstance(note, dict):
        return False
    if note.get("queue_state") != "dead_letter" or note.get("type") != "lease_expired":
        return False
    now = datetime.now(UTC)
    taken = (
        await model.filter(
            id=str(UUID(job_id)),
            claimed_at__isnull=True,
            visible_at__gt=now + timedelta(days=_FAR_FUTURE_DAYS // 2),
        ).update(
            claimed_at=now,
            claimed_by=claimed_by,
            visible_at=now + timedelta(seconds=visibility_timeout_seconds),
            last_error={
                "queue_state": "in_progress",
                "type": "false_dead_taken_back",
                "message": "the reaper dead-lettered a job its worker was still running (an outage outlasted the "
                "lease); the live copy took it back to finish the run",
            },
        )
    ).updated_rows
    if taken:
        log.warning("job %s: the reaper dead-lettered it while this worker still ran it; taken back to finish the run",
                    job_id[:8])
    return bool(taken)


async def reap_expired_leases(*, grace_seconds: int = 120) -> int:
    """Requeue jobs whose lease expired ≥ ``grace_seconds`` ago (audit P1-14).

    A worker that dies mid-job leaves ``claimed_at`` set forever — only
    complete/fail/release null it — so the job is orphaned: never re-run,
    never dead-lettered, invisible to claim_one. This reaper is the one
    mechanism that recovers those rows. WorkerRunner renews the lease every
    lease/3 seconds while a job executes, so an expired-by-more-than-grace
    lease USUALLY means the worker is dead — but not always: a database
    outage longer than the lease fails every renewal of every live worker
    at once (live 2026-10-21, 15:49–15:59Z: job c1d89868 was requeued from
    a worker that was alive).

    Decision (lane K1, 2026-10-21): the reaper does NOT try to tell an outage
    from a death (an outage-detection rule would itself have to read a store
    that just failed, and would delay real recovery); instead a false "dead"
    is made HARMLESS by the copies themselves: a copy whose renewal answers
    "not ours" marks its lease lost, is cancelled and skips its terminal
    write (``runner._renew_loop`` + ``job_lease``); many-item work checks the
    lease before each item and each store attempt; and a slot held for the
    run (``work_claims.hold_work_slot(holder=run_id)``) is taken over by the
    new copy at once, so the run never waits on its own earlier copy.

    Jobs with attempts left are requeued (claim_one re-claims and bumps
    ``attempt``); exhausted jobs are dead-lettered (a live copy whose job was
    falsely dead-lettered takes it back, ``take_back_false_dead_letter``, lane
    K1b, so its run is never stranded) with the same far-future
    visible_at shape ``fail()`` uses. Returns how many rows were touched.
    """
    from matrx_graph.db._registry import get_model

    cutoff = datetime.now(UTC) - timedelta(seconds=grace_seconds)
    retry_note = {
        "queue_state": "pending",
        "type": "lease_expired",
        "message": (
            "worker lease expired without complete/fail/release — "
            "worker presumed dead; reaped by reap_expired_leases"
        ),
    }
    dead_note = {
        **retry_note,
        "queue_state": "dead_letter",
        "retry_exhausted": True,
    }
    from matrx_orm import Compare, F

    requeued = (
        await get_model("WfJob")
        .filter(
            Compare(F("attempt"), "<", F("max_attempts")),
            claimed_at__isnull=False,
            visible_at__lt=cutoff,
        )
        .update(claimed_at=None, claimed_by=None, last_error=retry_note)
    ).updated_rows
    dead = (
        await get_model("WfJob")
        .filter(
            Compare(F("attempt"), ">=", F("max_attempts")),
            claimed_at__isnull=False,
            visible_at__lt=cutoff,
        )
        .update(
            claimed_at=None,
            claimed_by=None,
            last_error=dead_note,
            visible_at=_far_future(),
        )
    ).updated_rows
    for row in requeued:
        log.warning(
            "wf_job reaper: requeued job %s (run %s, attempt %s) — lease held by dead worker %s",
            row["id"],
            row["run_id"],
            row["attempt"],
            row["claimed_by"],
        )
    for row in dead:
        log.error(
            "wf_job reaper: job %s (run %s) DEAD-LETTERED — worker %s died "
            "and attempts are exhausted (%s); operator inspection required",
            row["id"],
            row["run_id"],
            row["claimed_by"],
            row["attempt"],
        )
    return len(requeued) + len(dead)


def _parse_json(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return value
