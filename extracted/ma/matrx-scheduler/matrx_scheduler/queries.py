"""
matrx-orm access for the sch_* tables, used by the SCANNER.

The scanner reads across ALL users (finds due tasks / queued runs for every
surface) and writes lease/status state on their behalf -- this is
privileged, cross-tenant access by design, exactly like the SERVICE-ROLE
Supabase client this module used before conversion. matrx-orm's Model calls
run as the ``postgres`` role (no RLS applied) by default, which is the
IDENTICAL trust level the old service-role PostgREST client had (the
service-role key also bypasses RLS entirely). No ownership predicate is
narrowed or widened by this conversion -- the scanner was never row-scoped
and still isn't.

User-initiated writes (the HTTP API) go through ``api.user_queries``
instead, which runs every query inside ``matrx_orm.rls_session`` scoped to
the caller's own claims. That module's docstring has the full RLS
rationale; this one intentionally has none because the scanner has none
to preserve.

Package boundary: matrx-scheduler is NOT a declared dependent of
matrx-orm -- this module never imports it. DB models (``SchTask`` etc.)
are injected declaratively via ``get_db_model`` (wired by the generated
``aidream/_generated/package_db_wiring.py`` from this package's
``db_requirements.py``); see ``_ext.py``.

Hydration note: the old PostgREST queries used embedded-resource JOINs
(``sch_task(*, agent:sch_agent_task(...), triggers:sch_trigger(...))``) to
fetch a task/run plus its related rows in one round trip. This module does
the equivalent hydration as a small, bounded number of separate queries
(at most 2 extra per candidate row) rather than one dynamic JOIN -- the
OUTPUT is unchanged (same LEFT-join semantics: a row's ``agent_task`` is
None when no ``sch_agent_task`` row exists, ``trigger`` is the first
enabled trigger or None), only the transport differs.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from ._ext import get_db_model, get_ext, get_optional_ext
from .models import (
    RUN_STOPPED_EARLY_KEY,
    RUN_UNITS_DONE_KEY,
    HydratedTask,
    SchAgentTask,
    SchRun,
    SchTask,
    SchTrigger,
)

log = logging.getLogger("matrx_scheduler.queries")

# Every transition into an executing state carries this protocol marker.
# scheduler.sch_run enforces it with TWO validated, null-safe CHECK constraints
# -- sch_run_claim_protocol_chk (status in claimed|running) and
# sch_run_claim_protocol_by_claimed_at_chk (claimed_at IS NOT NULL, for rows
# created after the 2026-07-26 02:23:01.773117+00 cutover) -- which make a stale
# server generation physically unable to claim work after the scheduler contract
# changes. Bump this value only with the matching DB migration, and grandfather
# existing rows with a NEW created_at cutover, never with NOT VALID: a NOT VALID
# CHECK is still evaluated against the NEW row of every UPDATE, so it freezes
# legacy rows instead of exempting them (see the package CLAUDE.md rule 6 and
# db/migrations/0483_scheduler_claim_protocol_fence_grandfather_cutover.sql).
CLAIM_PROTOCOL: int = 2


# Fields selected for the embedded ``agent`` join -- matches the old
# ``SELECT_HYDRATED`` projection exactly (never ``id``; ``SchAgentTask.id``
# is always stamped from the parent task's id, never read off this row).
_AGENT_HYDRATE_FIELDS = (
    "agent_id",
    "mandate_key",
    "prompt",
    "variables",
    "persistent_conversation_id",
    "auth_mode",
    "max_runtime_seconds",
    "max_concurrent",
)


def _surface() -> str:
    return get_ext("surface")


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


async def _hydrate_agent_task(task_id: str) -> SchAgentTask | None:
    """LEFT-join equivalent: None when the task has no sch_agent_task row
    (non-agent kinds -- ping/tool -- never get one)."""
    SchAgentTaskModel = get_db_model("SchAgentTask")
    rows = await SchAgentTaskModel.filter(id=task_id).limit(1).values(*_AGENT_HYDRATE_FIELDS)
    return SchAgentTask(id=task_id, **rows[0]) if rows else None


async def _hydrate_active_trigger(task_id: str) -> SchTrigger | None:
    """LEFT-join equivalent: the first enabled trigger for the task, or
    None. Matches the old `next((t for t in triggers if t.enabled), None)`
    semantics exactly (order among enabled triggers was never guaranteed
    by the old PostgREST embed either)."""
    SchTriggerModel = get_db_model("SchTrigger")
    # A soft-deleted trigger is GONE: it must never be hydrated as the task's
    # clock, or a schedule the person removed keeps firing (user_queries.
    # delete_trigger).
    rows = await SchTriggerModel.filter(
        task_id=task_id, deleted_at__isnull=True
    ).values()
    triggers = [SchTrigger(**t) for t in rows]
    return next((t for t in triggers if t.enabled), None)


# ── Read candidates due for claim ───────────────────────────────────────────


async def find_dark_tasks(limit: int = 200) -> list[dict[str, Any]]:
    """Tasks that READ enabled but can never fire — THE DARK SCHEDULE.

    A task is the firing gate and a trigger is the clock. Disable the clock and
    leave the gate open and every surface says "enabled" while the schedule
    fires nothing, forever, and nothing anywhere says otherwise. It is the same
    silent-failure class as a suspension nobody can see, and it is reachable
    three ways: a partial re-enable (task flipped, trigger forgotten), a
    partial suspend (``_auto_suspend`` disables the task first, then loops the
    triggers — its own docstring admits the trigger leg may need a retry), and
    any direct row edit.

    A task with NO trigger rows at all is NOT dark: that is a
    dispatch-on-demand job, fired by a caller rather than a clock. Only a task
    that HAS clocks and has switched all of them off is lying.

    Bounded by ``limit`` — this is an alarm, not an inventory.
    """
    SchTaskModel = get_db_model("SchTask")
    SchTriggerModel = get_db_model("SchTrigger")
    tasks = await (
        SchTaskModel.filter(enabled=True, deleted_at=None)
        .limit(limit)
        .values("id", "title")
    )
    if not tasks:
        return []
    task_ids = [str(t["id"]) for t in tasks]
    triggers = await SchTriggerModel.filter(task_id__in=task_ids).values(
        "task_id", "enabled"
    )
    has_trigger: set[str] = set()
    has_live_trigger: set[str] = set()
    for row in triggers:
        tid = str(row.get("task_id") or "")
        has_trigger.add(tid)
        if row.get("enabled"):
            has_live_trigger.add(tid)
    return [
        {"id": str(t["id"]), "title": t.get("title") or "<untitled>"}
        for t in tasks
        if str(t["id"]) in has_trigger and str(t["id"]) not in has_live_trigger
    ]


async def find_due_tasks(limit: int = 20) -> list[HydratedTask]:
    """
    Returns enabled tasks where next_due_at <= now AND this host's
    surface is allowed AND the task hasn't expired.

    Kind dispatch is the RUNNER's responsibility (see runner.py:
    run_claimed_task). The scanner intentionally does NOT filter on
    ``kind`` so non-agent kinds (``tool``, ``ping``, and future
    additions) flow through the same claim/lease/finalize plumbing.
    Tasks whose kind has no registered handler fail cleanly with a
    structured error_message; they never block the scanner.

    The surface filter uses the ``__overlap`` array lookup (Postgres
    ``&&``) -- true when ``surfaces`` shares an element with
    ``['any', <surface>]``, the ORM equivalent of the old PostgREST
    ``surfaces.cs.{any},surfaces.cs.{<surface>}`` OR'd contains-filter
    (a single-element array-contains check OR'd across two candidates is
    exactly what array-overlap against the union set means).

    Tasks with ``expires_at`` in the past are excluded.

    The hydrated join on ``sch_agent_task`` is a LEFT join (see
    ``_hydrate_agent_task``); the agent blob is None for non-agent kinds.
    The runner's per-kind dispatch enforces presence — ``agent`` and
    ``tool`` paths require a non-null ``agent_task`` and fail cleanly
    when it's missing; ``ping`` ignores it.
    """
    SchTaskModel = get_db_model("SchTask")
    now_dt = datetime.now(UTC)
    surface = _surface()

    # Defensive: soft_delete_task always flips enabled=false alongside
    # stamping deleted_at, so the enabled=True filter alone catches user-
    # deleted rows. The deleted_at IS NULL clause is belt-and-suspenders
    # against any future code path that forgets to flip enabled.
    rows = await (
        SchTaskModel.filter(
            enabled=True,
            deleted_at__isnull=True,
            next_due_at__lte=now_dt,
            surfaces__overlap=["any", surface],
        )
        .order_by("next_due_at")
        .limit(limit)
        .values()
    )

    out: list[HydratedTask] = []
    for row in rows:
        # Exclude expired tasks.
        expires_at = row.get("expires_at")
        if expires_at and expires_at < now_dt:
            continue
        task_id = row["id"]
        agent_task = await _hydrate_agent_task(task_id)
        active_trigger = await _hydrate_active_trigger(task_id)
        task = SchTask(**row)
        out.append(HydratedTask(task=task, agent_task=agent_task, trigger=active_trigger))
    return out


async def find_queued_runs(limit: int = 20) -> list[tuple[SchRun, HydratedTask]]:
    """
    Manual runs ("Run now") are inserted via sch_enqueue_manual_run with
    surface=NULL. The scanner picks them up alongside scheduled runs. We
    only return rows whose parent task targets our surface (or 'any').

    The parent-task lookup is the INNER-join equivalent (old query used
    ``task:sch_task!inner(...)``) -- a queued run whose parent task is
    missing (should never happen; task_id is a FK) is skipped, matching
    the old inner-join semantics of silently dropping unmatched rows.

    The ``sch_agent_task`` hydration is a LEFT join so manual runs of
    non-agent kinds (``ping``, ``tool``) flow through the same
    queued-pass plumbing. Agent-specific fields are None for those rows;
    the runner's kind dispatch handles a missing ``agent_task`` per kind.
    """
    SchRunModel = get_db_model("SchRun")
    SchTaskModel = get_db_model("SchTask")

    now = datetime.now(UTC)
    run_rows = (
        await SchRunModel.filter(status="queued", due_at__lte=now)
        .order_by("due_at")
        .limit(limit)
        .values()
    )
    surface = _surface()
    out: list[tuple[SchRun, HydratedTask]] = []
    for row in run_rows:
        # An archived (soft-deleted) schedule never fires — not even a queued
        # "Run now" row enqueued before the person moved it to Trash.
        task_rows = await (
            SchTaskModel.filter(id=row["task_id"], deleted_at__isnull=True)
            .limit(1)
            .values()
        )
        if not task_rows:
            continue
        task_row = task_rows[0]
        surfaces = task_row.get("surfaces") or []
        if "any" not in surfaces and surface not in surfaces:
            continue
        task_id = task_row["id"]
        agent_task = await _hydrate_agent_task(task_id)
        active_trigger = await _hydrate_active_trigger(task_id)
        run = SchRun(**row)
        task = SchTask(**task_row)
        hydrated = HydratedTask(task=task, agent_task=agent_task, trigger=active_trigger)
        out.append((run, hydrated))
    return out


# ── Claim ───────────────────────────────────────────────────────────────────


async def claim_task(
    task: SchTask,
    trigger: SchTrigger | None,
    agent_task: SchAgentTask | None,
    lease_seconds: int,
) -> SchRun | None:
    """
    Atomic claim: INSERT into sch_run. The partial unique index
    `sch_run_unique_active_per_task` (status IN queued|claimed|running) raises
    a unique violation on the second concurrent claimer — we catch it and
    return None. matrx-orm surfaces this as ``IntegrityError`` whose message
    embeds the underlying Postgres error text (constraint name / SQLSTATE);
    string-matching on the exception text (rather than importing the ORM's
    exception class) keeps this module off the ``matrx_orm`` package
    boundary, same approach ``api.user_queries``/``api.router_scheduler``
    use for classifying errors.

    Lease length = ``lease_seconds`` — the HEARTBEAT TIMEOUT, not the run
    ceiling. The runner renews ``claim_expires_at`` every third of it while the
    handler is alive (``lease.heartbeat_until_stopped``) and cancels the handler
    at ``agent_task.max_runtime_seconds`` (the schedule's "Max runtime", the
    hard deadline). Until 2026-09-13 the claim was written ONCE for
    ``max(lease, max_runtime + 60)`` and never renewed, so a dead worker was
    noticed only after the whole ceiling, and a live handler that outran the
    number was stamped ``failed / lease expired`` while it kept running as a
    zombie (see ``lease.py``). Non-agent kinds (``ping``, ``tool`` w/o a child
    row) have no ``agent_task``; the runner falls back to the SchAgentTask
    default (600s) for the deadline.
    """
    try:
        organization_id = str(uuid.UUID(task.organization_id))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError(
            f"refusing to claim task {task.id}: task has no valid organization_id"
        ) from exc

    SchRunModel = get_db_model("SchRun")
    surface = _surface()
    claim_token = str(uuid.uuid4())
    now = datetime.now(UTC)
    expires = now + timedelta(seconds=max(1, int(lease_seconds)))

    payload = {
        "id": str(uuid.uuid4()),
        "task_id": task.id,
        "trigger_id": trigger.id if trigger else None,
        "user_id": task.user_id,
        "organization_id": organization_id,
        "status": "claimed",
        "surface": surface,
        "queue": task.queue,
        "due_at": task.next_due_at or now,
        "claimed_at": now,
        "claim_token": claim_token,
        "claim_expires_at": expires,
        "metadata": {"claim_protocol": CLAIM_PROTOCOL},
    }
    try:
        instance = await SchRunModel.create(**payload)
    except Exception as exc:
        msg = str(exc)
        # Unique-violation = another scanner won the race. Expected; log at debug.
        if (
            "23505" in msg
            or "sch_run_unique_active_per_task" in msg
            or "duplicate key" in msg.lower()
        ):
            log.debug("claim race lost on task %s", task.id)
            return None
        raise
    return SchRun(**instance.to_dict())


async def claim_queued_run(
    run: SchRun, lease_seconds: int, max_runtime_seconds: int
) -> SchRun | None:
    """
    Promote a due 'queued' run to 'claimed' atomically. Uses an UPDATE with a
    WHERE that asserts the row is still 'queued' and due — if the row has
    already moved on or was rescheduled into the future after the scanner's
    candidate read, no rows match.

    ``max_runtime_seconds`` is accepted for signature stability and is the
    runner's deadline, not the lease: see ``claim_task``.
    """
    SchRunModel = get_db_model("SchRun")
    surface = _surface()
    claim_token = str(uuid.uuid4())
    now = datetime.now(UTC)
    expires = now + timedelta(seconds=max(1, int(lease_seconds)))

    result = await SchRunModel.update_where(
        {"id": run.id, "status": "queued", "due_at__lte": now},
        status="claimed",
        surface=surface,
        claimed_at=now,
        claim_token=claim_token,
        claim_expires_at=expires,
        metadata={**(run.metadata or {}), "claim_protocol": CLAIM_PROTOCOL},
    )
    if not result.updated_rows:
        return None
    return SchRun(**result.updated_rows[0])


# ── Status transitions for an in-flight run ────────────────────────────────


async def mark_run_running(
    run_id: str,
    claim_token: str,
    output_ref: dict[str, Any] | None = None,
) -> bool:
    """
    Update status='running'. Returns False if the row's claim_token no
    longer matches (lease lapsed; another claimer took over).
    """
    SchRunModel = get_db_model("SchRun")
    patch: dict[str, Any] = {
        "status": "running",
        "started_at": _now_iso(),
    }
    if output_ref is not None:
        patch["output_ref"] = output_ref
    result = await SchRunModel.update_where({"id": run_id, "claim_token": claim_token}, **patch)
    return bool(result.updated_rows)


async def renew_run_lease(run_id: str, claim_token: str, lease_seconds: int) -> bool:
    """THE HEARTBEAT. Push ``claim_expires_at`` out by one lease, gated by the
    claim token AND by the row still being in flight. Returns False when the
    row is no longer ours — expired by the sweep, finalized, or re-claimed —
    which is the runner's signal to stop the handler rather than let it zombie.
    """
    SchRunModel = get_db_model("SchRun")
    expires = datetime.now(UTC) + timedelta(seconds=max(1, int(lease_seconds)))
    result = await SchRunModel.update_where(
        {"id": run_id, "claim_token": claim_token, "status__in": ["claimed", "running"]},
        claim_expires_at=expires,
    )
    return bool(result.updated_rows)


async def record_run_progress(
    run_id: str, claim_token: str, result_metadata: dict[str, Any]
) -> bool:
    """Write the handler's progress so far onto the in-flight row, under the
    claim token. The row then carries ``units_done`` BEFORE any terminal write,
    so an expiry, a cancel, or a crash never erases the work that landed.
    Returns False when the lease is lost."""
    SchRunModel = get_db_model("SchRun")
    result = await SchRunModel.update_where(
        {"id": run_id, "claim_token": claim_token, "status__in": ["claimed", "running"]},
        result_metadata=result_metadata,
    )
    return bool(result.updated_rows)


# Terminal statuses that are eligible for post-commit reporting.  The public
# model names the current statuses; abandoned/expired remain supported ledger
# verdicts because historic rows and lifecycle repair can still write them.
_FAILED_STATUSES = frozenset({"failed", "cancelled", "abandoned", "expired"})
_REPORTABLE_TERMINAL_STATUSES = _FAILED_STATUSES | frozenset({"success", "skipped", "interrupted"})


async def finalize_run(
    run_id: str,
    claim_token: str,
    *,
    status: str,
    result_summary: str | None = None,
    error_message: str | None = None,
    output_ref: dict[str, Any] | None = None,
    result_metadata: dict[str, Any] | None = None,
) -> bool:
    """
    Write terminal state, gated by claim_token. Returns False if the lease
    was lost (the runner shouldn't write — another claimer owns this run).
    """
    SchRunModel = get_db_model("SchRun")
    patch: dict[str, Any] = {
        "status": status,
        "finished_at": _now_iso(),
        "claim_token": None,
    }
    if result_summary is not None:
        patch["result_summary"] = result_summary[:2000]
    if error_message is not None:
        # Batch dispatchers must retain the exact per-item failures. Twenty
        # thousand characters covers the scheduler's bounded batch sizes while
        # still preventing an unbounded provider response from becoming a row.
        patch["error_message"] = error_message[:20_000]
    if output_ref is not None:
        patch["output_ref"] = output_ref
    if result_metadata is not None:
        patch["result_metadata"] = result_metadata
    result = await SchRunModel.update_where({"id": run_id, "claim_token": claim_token}, **patch)
    persisted = bool(result.updated_rows)

    # Finalization is the durable boundary.  Reporting begins only after the
    # conditional terminal write has landed, so a lost claim cannot update
    # task bookkeeping, page a failure sink, or affect the repeat guard.
    if persisted:
        await report_finalized_run(
            run_id,
            status=status,
            error_message=error_message,
            result_metadata=result_metadata,
        )
    return persisted


async def report_finalized_run(
    run_id: str,
    *,
    status: str,
    error_message: str | None = None,
    result_metadata: dict[str, Any] | None = None,
) -> None:
    """Perform best-effort bookkeeping for a terminal run already persisted.

    This contains no terminal write.  Hosts that complete an atomic terminal
    operation themselves can call it only after their transaction commits.
    Reporting failures are deliberately contained: the ledger row is the
    source of truth and must never be rolled back by an observer.
    """
    SchRunModel = get_db_model("SchRun")

    # THE CHOKEPOINT. Every terminal write in the scheduler lands here — the
    # normal path, each kind-dispatch early-exit, the shielded
    # finalize-on-cancel, and (since 2026-09-13) the lease-expiry sweep.
    # Checking the repeat streak here (rather than at the ~9 call sites) is why
    # "a task failed N times the same way" cannot be missed by a future code
    # path that forgets to call the guard — and stamping ``sch_task.last_run_at``
    # here is why a run that ran for 31 minutes and then failed still reads as
    # "ran": before this the stamp lived on the success path alone, so a task
    # whose only runs expired showed a last_run_at weeks stale.
    # Re-read before any observer work.  The caller's status and result values
    # are compatibility inputs only: the committed row is the sole authority
    # for reporting, so a stale host cannot fabricate an error or metadata.
    try:
        rows = await SchRunModel.filter(id=run_id).limit(1).values(
            "task_id",
            "trigger_id",
            "user_id",
            "organization_id",
            "surface",
            "queue",
            "status",
            "error_message",
            "result_metadata",
        )
    except Exception:  # noqa: BLE001 -- bookkeeping can never break finalization
        log.exception("run %s: could not read committed terminal row for reporting", run_id)
        return
    if not rows:
        log.warning("run %s: refusing post-commit reporting because the ledger row is missing", run_id)
        return

    run = rows[0]
    committed_status = str(run.get("status") or "")
    if committed_status not in _REPORTABLE_TERMINAL_STATUSES:
        log.warning(
            "run %s: refusing post-commit reporting because ledger status %r is nonterminal",
            run_id,
            committed_status,
        )
        return
    if committed_status != status:
        log.warning(
            "run %s: refusing post-commit reporting because expected status %r differs from ledger status %r",
            run_id,
            status,
            committed_status,
        )
        return

    task_id = str(run.get("task_id") or "") or None
    committed_error = run.get("error_message")
    if not isinstance(committed_error, str):
        committed_error = None
    committed_metadata = run.get("result_metadata")
    if not isinstance(committed_metadata, dict):
        committed_metadata = {}
    try:
        if task_id:
            await update_last_run_at(task_id)
    except Exception:  # noqa: BLE001 -- bookkeeping can never break finalization
        log.exception("run %s: could not stamp sch_task.last_run_at", run_id)
    if committed_status in _FAILED_STATUSES:
        failure_sink = get_optional_ext("failure_sink")
        try:
            if run:
                if failure_sink is not None:
                    await failure_sink(
                        {
                            "run_id": run_id,
                            "task_id": task_id,
                            "trigger_id": str(run.get("trigger_id") or "") or None,
                            "user_id": str(run.get("user_id") or "") or None,
                            "organization_id": str(run.get("organization_id") or "") or None,
                            "surface": run.get("surface"),
                            "queue": run.get("queue"),
                            "status": committed_status,
                            "error_message": (committed_error or "")[:20_000],
                            "result_metadata": committed_metadata,
                        }
                    )
        except Exception:  # noqa: BLE001 -- reporting can never break finalization
            log.exception(
                "scheduled failure sink failed for persisted run %s; ledger is intact",
                run_id,
            )
        from .repeat_guard import note_failed_run

        await note_failed_run(run_id, task_id=task_id)
# ── Trigger / task post-run bookkeeping ────────────────────────────────────


async def advance_trigger_next_due_at(trigger_id: str, next_due_at: datetime | None) -> None:
    SchTriggerModel = get_db_model("SchTrigger")
    patch: dict[str, Any] = {
        "last_fired_at": _now_iso(),
        "next_due_at": next_due_at,
    }
    await SchTriggerModel.update_where({"id": trigger_id}, **patch)


#: Public name for the failed terminal verdicts (the one-shot settlement reads it).
FAILED_RUN_STATUSES = _FAILED_STATUSES


async def mark_trigger_fired(trigger_id: str) -> None:
    """Stamp ``last_fired_at`` and leave ``next_due_at`` as it is.

    For a one-shot whose single fire failed: it DID fire (a trigger that reads
    "never fired" after its run failed is how the "learn" one-shot looked stalled
    for 12 days), and keeping its instant lets a deliberate re-enable retry it."""
    SchTriggerModel = get_db_model("SchTrigger")
    await SchTriggerModel.update_where({"id": trigger_id}, last_fired_at=_now_iso())


async def read_run_status(run_id: str) -> str | None:
    SchRunModel = get_db_model("SchRun")
    rows = await SchRunModel.filter(id=run_id).limit(1).values("status")
    return str(rows[0].get("status") or "") or None if rows else None


async def disable_task(task_id: str) -> None:
    """For one-shot triggers — auto-disable after fire."""
    SchTaskModel = get_db_model("SchTask")
    await SchTaskModel.update_where({"id": task_id}, enabled=False)


async def update_last_run_at(task_id: str) -> None:
    SchTaskModel = get_db_model("SchTask")
    await SchTaskModel.update_where({"id": task_id}, last_run_at=_now_iso())


async def set_persistent_conversation(task_id: str, conversation_id: str) -> str:
    """
    Heartbeat first-run binding. Uses a conditional update — only sets the
    column when it's still NULL. Returns the canonical conversation_id (the
    one that won the race, which may not be ours).
    """
    SchAgentTaskModel = get_db_model("SchAgentTask")
    result = await SchAgentTaskModel.update_where(
        {"id": task_id, "persistent_conversation_id__isnull": True},
        persistent_conversation_id=conversation_id,
    )
    if result.updated_rows:
        return conversation_id
    # We lost the race — read back the canonical id.
    rows = await SchAgentTaskModel.filter(id=task_id).limit(1).values(
        "persistent_conversation_id"
    )
    if rows and rows[0].get("persistent_conversation_id"):
        return rows[0]["persistent_conversation_id"]
    return conversation_id


# ── Lease expiry sweep ─────────────────────────────────────────────────────


async def sweep_expired_leases() -> int:
    """Close every in-flight row whose ``claim_expires_at`` has passed.

    An expired lease means the worker stopped heartbeating — its process died or
    was killed (a live handler renews every third of a lease, each renewal
    bounded; see ``lease.py``). That is not a verdict on the WORK, so each such
    row is closed through ``continuation.interrupt_run``: ``interrupted``, the
    ``result_metadata`` the handler wrote through ``RunLease.progress`` PRESERVED
    with ``units_done`` carried and the stop named, and a continuation queued due
    now with what is left of the fire's run ceiling. Continuations per fire are
    bounded by a knob; exhausting it — or a ceiling already spent — closes the
    row through ``finalize_run`` (THE CHOKEPOINT) with a real verdict.

    History. Before 2026-09-13 this was one bulk UPDATE to ``failed / lease
    expired`` that left ``result_metadata`` NULL, so 638 classified keywords read
    as "did nothing". From 2026-09-13 it preserved the work but still closed the
    run ``failed``, so when a deploy killed the approved facet backfill after
    1,593 keywords (2026-09-14, ``sch_run e6daa2aa…``) the rest of the day's
    approved work simply never happened.

    A row without a claim token (legacy, or hand-edited) predates the claim
    protocol and cannot be continued; it is closed ``failed`` ungated, so it
    cannot sit in flight forever.
    """
    from .continuation import VERDICT_LOST, interrupt_run

    SchRunModel = get_db_model("SchRun")
    now_dt = datetime.now(UTC)
    rows = await SchRunModel.filter(
        status__in=["claimed", "running"], claim_expires_at__lt=now_dt
    ).values("id", "claim_token", "result_metadata", "claim_expires_at", "task_id")
    swept = 0
    for row in rows:
        run_id = str(row["id"])
        meta_raw = row.get("result_metadata")
        meta: dict[str, Any] = dict(meta_raw) if isinstance(meta_raw, dict) else {}
        try:
            units = max(0, int(meta.get(RUN_UNITS_DONE_KEY) or 0))
        except (TypeError, ValueError):
            units = 0
        meta[RUN_UNITS_DONE_KEY] = units
        expired_at = row.get("claim_expires_at")
        expired_text = (
            expired_at.isoformat() if isinstance(expired_at, datetime) else str(expired_at)
        )
        reason = (
            f"lease expired at {expired_text}: the worker stopped heartbeating "
            "(process died or was killed)"
        )
        token = row.get("claim_token")
        verdict = "failed"
        if token:
            task_id = str(row.get("task_id") or "")
            try:
                agent_task = await _hydrate_agent_task(task_id) if task_id else None
            except Exception:  # noqa: BLE001 — one bad child row never stops the sweep
                log.exception(
                    "[scheduler-lease-expired] run %s: its sch_agent_task row would not load; "
                    "continuing it under the 600s default run ceiling",
                    run_id,
                )
                agent_task = None
            verdict = await interrupt_run(
                run_id=run_id,
                claim_token=str(token),
                reason=reason,
                result_metadata=meta,
                max_runtime_seconds=(
                    agent_task.max_runtime_seconds if agent_task is not None else 600
                ),
            )
            persisted = verdict != VERDICT_LOST
        else:
            meta[RUN_STOPPED_EARLY_KEY] = f"{reason} after committing {units} unit(s)"
            result = await SchRunModel.update_where(
                {"id": run_id, "status__in": ["claimed", "running"]},
                status="failed",
                finished_at=now_dt,
                error_message="lease expired",
                result_metadata=meta,
            )
            persisted = bool(result.updated_rows)
            task_id = str(row.get("task_id") or "") or None
            if persisted and task_id:
                await update_last_run_at(task_id)
        if persisted:
            swept += 1
            log.error(
                "[scheduler-lease-expired] run %s (task %s) expired at %s with %d unit(s) "
                "already committed — the worker stopped heartbeating. The work is on the "
                "row; the run is closed as failed so the failure sink and repeat guard see it.",
                run_id,
                row.get("task_id"),
                expired_at,
                units,
            )
    return swept
