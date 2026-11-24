from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from matrx_orm import ArrayAny, F, JsonbMerge, JsonPath, Projection, Q

from matrx_graph.checkpoint.values import (  # noqa: F401 — re-exported for callers of load()
    RunInputValueMissingError,
    RunOutputValueMissingError,
)
from matrx_graph.db._registry import get_instance, get_model
from matrx_graph.errors import ExecutionError
from matrx_graph.failure import RunFailure, failure_from_text
from matrx_graph.types.primitives import RunControlStatus, RunStatus

logger = logging.getLogger(__name__)


class RunReattachRefused(ValueError):
    """A saved run cannot be read by the caller trying to reattach."""


class RunResumeClaimLost(RunReattachRefused):
    """The owner still matches, but the parked run is no longer claimable."""


def _reattach_owner_filters(reattach_as: tuple[str | None, str | None]) -> dict[str, Any]:
    actor_id, organization_id = reattach_as
    try:
        organization_id = str(UUID(str(organization_id)))
        actor_id = str(UUID(str(actor_id))) if actor_id else None
    except ValueError as exc:
        raise RunReattachRefused("This retry does not carry a valid caller and organization.") from exc
    actor = {"created_by__isnull": True} if actor_id is None else {"created_by": actor_id}
    return {"organization_id": organization_id, "deleted_at__isnull": True, **actor}


#: The only columns a ``workflow.run`` UPDATE hands back. A plain ``update_where`` says
#: ``RETURNING *``: the WHOLE row — and a child run seeded with a large input carries it twice
#: (``input`` + ``metadata._settings.input_values``, ~6 MB each on Smart Add's offerings units,
#: 2026-10-28). Every event, checkpoint and status write then shipped and decoded ~12 MB it never
#: read: ~1 s per write, 1–3 s per step. A caller that needs a column names it here explicitly.
RUN_UPDATE_RETURNS: tuple[str, ...] = ("id",)

#: The terminal write hands back the row it left, because every run end then needed that row twice more — the
#: run-settled hook read it (``run_end_wake._settled_row``) and the in-process caller read it again (a mandate's
#: ``finalize.reload``): ~70 ms each per run end, every lane (L-SPEED round 6l). It hands back every column EXCEPT
#: these: ``input`` is the run's whole start payload (~6 MB on Smart Add's offerings units) and no settle hook reads
#: it from the row (the one that needs it, agent_build's door, loads it itself), so ``RETURNING *`` decoded it inside
#: the terminal write for nothing (review 2026-11-10 finding 5; the 2026-11-02 whole-row class). A row handed back
#: without a column has no such key, so a reader can tell "not returned" from "null".
TERMINAL_RUN_OMITS: frozenset[str] = frozenset({"input"})


def terminal_run_returns() -> list[str] | None:
    """The columns the terminal write hands back: every column of the host's run model but ``TERMINAL_RUN_OMITS``
    (None — the whole row — only for a stand-in model that declares no columns)."""
    fields = getattr(get_model("WfRun"), "_fields", None)
    return [name for name in fields if name not in TERMINAL_RUN_OMITS] if fields else None


@dataclass(frozen=True)
class AppliedResult:
    """What :meth:`RunStore.apply_result_with_row` did: ``applied`` is :meth:`RunStore.apply_result`'s answer;
    ``row`` is the row a TERMINAL write left (unresolved: output / input values may hold references, exactly like
    ``load(resolve_output=False, resolve_inputs=False)``), None for a park or a refused write."""

    applied: bool
    row: dict[str, Any] | None = None


async def update_run(filters: dict[str, Any], *, returning: Sequence[str] = RUN_UPDATE_RETURNS, **updates: Any) -> Any:
    """``UPDATE workflow.run`` matching ``filters``, handing back only ``returning`` (never the whole row)."""
    return await get_model("WfRun").filter(**filters).returning(*returning).update(**updates)

RECOVERABLE_STATUSES: tuple[str, ...] = ("errored", "paused", "interrupted", "awaiting_input")
#: A run in one of these has ended (errored included: it wakes the chat and waits for a fix); each stamps completed_at.
ENDED_STATUSES: frozenset[str] = frozenset({"completed", "failed", "errored", "cancelled"})
"""Statuses the resume/recovery APIs may claim. Parked, awaiting a user.
``awaiting_input`` (INPUT-SURFACE.md park-not-die) is a start-time park —
the run holds BEFORE step 0 with no checkpoint, waiting for a require/ask
input; resuming it re-enters ``Scheduler.run`` fresh with the supplied
values rather than replaying a checkpoint."""

#: ``metadata`` key stamped IN THE SAME STATEMENT as every move into ``running``.
#: The lifecycle watchdog judges a run dead from ``metadata`` alone (the newest of
#: its liveness signals); a parked run's heartbeat is as old as the park, so a
#: claim that flipped the status without a fresh signal handed the next sweep a
#: 'running' row that already looked silent — any park longer than the stale
#: window minus a few seconds was stamped ``run_stranded`` the instant it was
#: claimed (live 2026-10-25, run f30299d0: parked 11:40:38, claimed 11:52:27,
#: force-failed 11:55:53). Its own top-level key so the shallow merge can never
#: clobber ``_heartbeat`` (streaming tails) or ``_recovery`` (death reasons). It
#: ages like every other signal: a claim nobody executes still strands.
RUN_CLAIM_METADATA_KEY = "_claim"


def _claim_stamp(extra: dict[str, Any] | None = None) -> JsonbMerge:
    """The claim's metadata merge; ``extra`` keys ride the same statement (the claim key always wins)."""
    return JsonbMerge("metadata", {**(extra or {}), RUN_CLAIM_METADATA_KEY: {"at": datetime.now(UTC).isoformat()}})


#: Host-injected "which server/build is this" provider (``configure_run_origin``).
#: Every server shares one database, so a run row must say where it was started
#: — the first question when a run is picked up by a different build.
_run_origin_provider: Callable[[], dict[str, Any]] | None = None


def configure_run_origin(provider: Callable[[], dict[str, Any]] | None) -> None:
    """Install the provider whose dict is stamped as ``metadata._origin`` on every
    run :meth:`RunStore.create` makes (a caller-supplied ``_origin`` wins)."""
    global _run_origin_provider
    _run_origin_provider = provider


#: Host-injected "settings every new run carries from its starter" provider
#: (``configure_run_settings``). Each create door builds its own ``_settings``; anything the host
#: knows about the STARTER that every leg must re-carry (aidream: the test stamp of the session
#: that started the run) is filled in here once, so no door can forget it.
_run_settings_provider: Callable[[], dict[str, Any]] | None = None


def configure_run_settings(provider: Callable[[], dict[str, Any]] | None) -> None:
    """Install the provider whose dict is merged into ``metadata._settings`` on every run
    :meth:`RunStore.create` makes — a key the caller already set wins. A provider that raises
    fails the create: a run whose legs would silently lose a setting is worse than no run."""
    global _run_settings_provider
    _run_settings_provider = provider


def _origin_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(metadata or {})
    if _run_origin_provider is not None and "_origin" not in merged:
        try:
            merged["_origin"] = _run_origin_provider()
        except Exception:  # noqa: BLE001 — a diagnostic stamp never blocks a run
            logger.warning("run origin provider failed", exc_info=True)
    if _run_settings_provider is not None:
        extra = _run_settings_provider() or {}
        if extra:
            settings = dict(merged.get("_settings") or {})
            for key, value in extra.items():
                settings.setdefault(key, value)
            merged["_settings"] = settings
    return merged


#: Host-injected "a run just ended" hook (``configure_run_settled``): awaited once per APPLIED terminal write
#: (completed / failed / canceled / errored), with the status written and, for a cancel, why. The ONE place every
#: lane's run end passes through, so a host feature that reacts to run ends (waking the chat that started the run)
#: never needs a per-lane copy. Never raises into the run: the end is already written.
_run_settled_hook: Callable[..., Awaitable[None]] | None = None


def configure_run_settled(hook: Callable[..., Awaitable[None]] | None) -> None:
    """Install ``hook(run_id, status, cancel_reason)``, awaited after each applied terminal status write. When the write
    handed its row back the hook is called with ``row=<that row>`` too (unresolved, like ``load(resolve_output=False,
    resolve_inputs=False)``), so a hook must accept that keyword."""
    global _run_settled_hook
    _run_settled_hook = hook


#: Host-injected settle work the caller never waits for (``configure_run_settled_after``), P8-RUNS 2026-11-15.
_run_settled_after_hook: Callable[..., Awaitable[None]] | None = None

#: The terminal write's durable "settle work after the end still owed" marker (``workflow.run.metadata``): written in
#: the SAME statement as the end, cleared once the after-work ran. A process that dies between the two leaves it set,
#: and :func:`recover_settle_after` (the worker's reconciliation pass) runs the work again — every piece is idempotent.
SETTLE_AFTER_KEY = "_settle_after"

#: The after-work in flight in this process (strong references, so a task is never collected mid-flight).
_settle_after_tasks: set[asyncio.Task[None]] = set()


def configure_run_settled_after(hook: Callable[..., Awaitable[None]] | None) -> None:
    """Install ``hook(run_id, status, cancel_reason, row=...)``: settle work that runs AFTER a terminal write without
    holding its caller (a called child's caller resumes at once). Only work the caller never reads, that is
    idempotent, and that :func:`recover_settle_after` re-runs after a crash belongs here (executor/FEATURE.md §
    The settle hooks). Never raises into the run."""
    global _run_settled_after_hook
    _run_settled_after_hook = hook


def _settle_after_owed(alongside: Callable[[], Awaitable[Any]] | None) -> bool:
    return _run_settled_after_hook is not None or _run_waiting_hook is not None or alongside is not None


async def _announce_settled(
    run_id: str,
    status: str,
    cancel_reason: str | None = None,
    *,
    row: dict[str, Any] | None = None,
    alongside: Callable[[], Awaitable[Any]] | None = None,
    never_parked: bool = False,
    after_owed: bool = False,
    marker_token: str | None = None,
) -> None:
    """The settle a terminal write's caller waits for — the settled hook only — then the after-work started beside
    the caller (P8-RUNS 2026-11-15: the requests settle, the host's after hook and the unclaimed-job discard used to
    sit between every child's end and its caller's resume).

    ``row``: the row the terminal write just handed back (``terminal_run_returns()``, no ``input`` key), passed to the
    hooks so they never read it again. ``alongside``: independent end-of-run cleanup (the unclaimed-job discard).
    ``never_parked``: the leg that wrote this end created the run and ran it to the end without a park — the settled
    hook may skip reads of what only a park leaves (a parked spine). ``after_owed``: the terminal write carried the
    durable marker, so the after-work runs off the caller's path; without it, it runs here, as before.
    ``marker_token``: the marker's unique token; the after-work clears the marker only while it still carries it."""
    from matrx_utils.diagnostics.phase_clock import timed

    await timed("settle.settled_hook", _call_settled_hook(run_id, status, cancel_reason, row, never_parked=never_parked))
    if not after_owed:
        await _settle_after(run_id, status, cancel_reason, row=row, alongside=alongside, clear_marker=False)
        return
    task = asyncio.ensure_future(
        _settle_after(run_id, status, cancel_reason, row=row, alongside=alongside, marker_token=marker_token)
    )
    _settle_after_tasks.add(task)
    task.add_done_callback(_settle_after_tasks.discard)


async def _settle_after(
    run_id: str,
    status: str,
    cancel_reason: str | None,
    *,
    row: dict[str, Any] | None = None,
    alongside: Callable[[], Awaitable[Any]] | None = None,
    clear_marker: bool = True,
    marker_token: str | None = None,
) -> None:
    """The after-work, all at once, then the marker cleared — only while it still carries ``marker_token`` (a conditional update: a run that ended
    again, e.g. a shutdown-cancelled run resumed, wrote a NEW marker the late first clear must not wipe). Each piece never raises by contract; one that does is
    logged and the marker is still cleared (as before, a failed reaction to an end is reported, not retried)."""
    from matrx_utils.diagnostics.phase_clock import timed

    work = [
        timed("settle.waiting_hook", _announce_waiting(run_id, "settled", status, None)),
        timed("settle.after_hook", _call_settled_after_hook(run_id, status, cancel_reason, row)),
    ]
    if alongside is not None:
        work.append(timed("settle.discard_jobs", alongside()))
    for outcome in await asyncio.gather(*work, return_exceptions=True):
        if isinstance(outcome, BaseException):
            logger.error("[wf:%s] settle work after the end raised", str(run_id)[:8], exc_info=outcome)
    if not clear_marker:
        return
    try:
        guard: dict[str, Any] = {"id": str(UUID(run_id))}
        if marker_token is not None:
            guard["metadata__json_contains"] = {SETTLE_AFTER_KEY: {"token": marker_token}}
        await get_model("WfRun").update_where(guard, metadata=JsonbMerge("metadata", {SETTLE_AFTER_KEY: None}))
    except Exception:  # noqa: BLE001 — the marker stays set; the reconciliation pass runs the (idempotent) work again
        logger.warning("[wf:%s] the settle-after marker could not be cleared", str(run_id)[:8], exc_info=True)


async def _call_settled_after_hook(
    run_id: str, status: str, cancel_reason: str | None, row: dict[str, Any] | None
) -> None:
    if _run_settled_after_hook is None:
        return
    try:
        await _run_settled_after_hook(str(run_id), status, cancel_reason, row=row)
    except Exception:  # noqa: BLE001 — the run already ended; a reaction to it never undoes that
        logger.exception("[wf:%s] run-settled-after hook failed (status=%s)", str(run_id)[:8], status)


async def drain_settle_after() -> None:
    """Wait for this event loop's after-work in flight (tests, a graceful shutdown). Work left by a loop that already
    closed is dropped from the set (its marker is still on the row: the recovery pass owns it)."""
    loop = asyncio.get_running_loop()
    while True:
        _settle_after_tasks.difference_update(
            [t for t in _settle_after_tasks if t.done() or (t.get_loop() is not loop and t.get_loop().is_closed())]
        )
        pending = [t for t in _settle_after_tasks if t.get_loop() is loop]
        if not pending:
            return
        await asyncio.gather(*pending, return_exceptions=True)


async def recover_settle_after(*, older_than_seconds: float = 60.0, limit: int = 200) -> int:
    """Run the after-work again for every ended run whose marker is still set ``older_than_seconds`` after its end
    (its process died before the work finished). Returns how many runs were settled. Never raises."""
    from datetime import timedelta

    try:
        cutoff = datetime.now(UTC) - timedelta(seconds=older_than_seconds)
        rows = await (
            get_model("WfRun")
            .filter(
                metadata__json_contains={SETTLE_AFTER_KEY: {"pending": True}},
                status__in=list(TERMINAL_STATUSES),
                completed_at__lt=cutoff,
                deleted_at__isnull=True,
            )
            .limit(limit)
            .values("id", "status", "metadata")
        )
    except Exception:  # noqa: BLE001 — the next pass tries again
        logger.exception("settle-after recovery: the marked runs could not be read")
        return 0
    settled = 0
    for found in rows or []:
        run_id = str(found["id"])
        metadata = found.get("metadata") if isinstance(found.get("metadata"), dict) else {}
        marker = metadata.get(SETTLE_AFTER_KEY) if isinstance(metadata.get(SETTLE_AFTER_KEY), dict) else {}

        async def _discard(rid: str = run_id) -> None:
            from matrx_graph.workers.queue import discard_for_run

            await discard_for_run(rid)

        await _settle_after(
            run_id, str(found.get("status") or ""), marker.get("cancel_reason"), alongside=_discard,
            marker_token=marker.get("token"),
        )
        settled += 1
    return settled


async def _call_settled_hook(
    run_id: str, status: str, cancel_reason: str | None, row: dict[str, Any] | None = None, *, never_parked: bool = False
) -> None:
    if _run_settled_hook is None:
        return
    try:
        extra: dict[str, Any] = {"never_parked": True} if never_parked else {}
        if row is None and not extra:
            await _run_settled_hook(str(run_id), status, cancel_reason)
        else:
            await _run_settled_hook(str(run_id), status, cancel_reason, row=row, **extra)
    except Exception:  # noqa: BLE001 — the run already ended; a reaction to it never undoes that
        logger.exception("[wf:%s] run-settled hook failed (status=%s)", str(run_id)[:8], status)


#: Host-injected "a run started / stopped waiting" hook (``configure_run_waiting``), awaited as
#: ``hook(run_id, event, status, interrupt)`` where ``event`` is:
#:   * ``"waiting"``  — the run was just parked ``interrupted`` or ``awaiting_input`` (``interrupt`` is the
#:     payload written; a timer park is included, the snapshot's ``waits_for_person`` tells them apart);
#:   * ``"resumed"``  — a parked run was just claimed back to ``running`` (``claim_for_resume``);
#:   * ``"settled"``  — the run just reached a terminal status.
#: The ONE place every lane's park and un-park passes through, so a host that keeps a record of what a
#: run is waiting on (a Request) never needs a per-lane copy. Never raises into the run.
_run_waiting_hook: Callable[[str, str, str, dict[str, Any] | None], Awaitable[None]] | None = None


def configure_run_waiting(
    hook: Callable[[str, str, str, dict[str, Any] | None], Awaitable[None]] | None,
) -> None:
    """Install ``hook(run_id, event, status, interrupt)`` — see ``_run_waiting_hook``."""
    global _run_waiting_hook
    _run_waiting_hook = hook


async def _announce_waiting(
    run_id: str, event: str, status: str, interrupt: dict[str, Any] | None
) -> None:
    if _run_waiting_hook is None:
        return
    try:
        await _run_waiting_hook(str(run_id), event, status, interrupt)
    except Exception:  # noqa: BLE001 — the status is already written; a reaction to it never undoes that
        logger.exception("[wf:%s] run-waiting hook failed (event=%s)", str(run_id)[:8], event)


_VALID_CREATE_STATUSES: frozenset[str] = frozenset({"pending", "running", "paused"})
"""Statuses a run may be BORN with. 'running' = a live run executing in-process;
'pending' = a queued-lane run waiting for a worker to claim its wf_job (the
worker's mark_running flips it on claim — 0001_wf_initial.sql designed exactly
this, and a queued run BORN 'running' was the lie that hid a never-deployed
worker for months); 'paused' = a step-mode run created at a frontier (see
RunStore.create's ``status`` arg)."""

TERMINAL_STATUSES: tuple[str, ...] = ("completed", "failed", "cancelled")
"""Immutable end states. A terminal status may never be overwritten by a
DIFFERENT terminal status — only re-written idempotently with itself."""

WAITING_STATUSES: tuple[str, ...] = ("interrupted", "awaiting_input")
"""THE "waiting on you" inbox — the two statuses that mean a run is holding
for a person. ``interrupted``: a ``control.human_input`` node asked a question
mid-run. ``awaiting_input``: a headless start parked for a missing require/ask
input (INPUT-SURFACE.md park-not-die). One inbox, two statuses — every
discovery surface lists both, never one."""


def build_interrupt_snapshot(interrupt: dict[str, Any] | None) -> dict[str, Any]:
    """The flat "what is this run waiting for" snapshot (SPEC §4.3 leg 2).

    Input is the scheduler's ``RunResult.interrupt`` —
    ``{node_id, payload, checkpoint_id}`` — or, for a pre-change run, the raw
    ``workflow.run.interrupt_payload`` column in either shape. Output is the
    row-level projection every "waiting on you" surface reads: identity
    (``node_id`` / ``checkpoint_id``), the question (``prompt`` / ``title`` /
    ``schema_hint`` / ``preset``), how to show it (``presentation``), and the
    clock (``asked_at`` / ``deadline``).

    Pure and total: an interrupt from a node that declares none of the §4.1
    block still produces a well-formed snapshot with today's defaults, which is
    what makes the projection's fallback path work on old runs."""
    from matrx_graph.workers.sleep_wake import sleep_marker_of

    interrupt = interrupt if isinstance(interrupt, dict) else {}
    inner = interrupt.get("payload")
    payload: dict[str, Any] = inner if isinstance(inner, dict) else interrupt
    escalation = payload.get("escalation")
    escalation = escalation if isinstance(escalation, dict) else {}
    return {
        # NOT every interrupt is a question. ``flow.sleep`` / ``flow.wait_until``
        # park the run INTERRUPTED too, and a sleeping run is waiting on the
        # CLOCK — Postgres already holds its wake job. Stamped here, at the one
        # place that sees the payload, so no discovery surface has to re-derive
        # it and none of them can put a timer in a person's inbox.
        "waits_for_person": sleep_marker_of(interrupt) is None,
        "node_id": interrupt.get("node_id"),
        "checkpoint_id": _to_uuid(interrupt.get("checkpoint_id")),
        "title": payload.get("title"),
        "prompt": payload.get("prompt"),
        # Defaults are the node's defaults, not a guess: a node authored before
        # the presentation block existed IS a panel-presented free-text ask.
        "presentation": payload.get("presentation") or "panel",
        "preset": payload.get("preset") or "free_text",
        "schema_hint": payload.get("schema_hint"),
        # ``waiting_since`` is the instant the node froze its deadline against;
        # without an escalation policy there is no frozen instant, so the write
        # time is the honest answer.
        "asked_at": escalation.get("waiting_since") or datetime.now(UTC).isoformat(),
        "deadline": escalation.get("deadline_at"),
        # THE HUMAN GATE: the whole decision spec rides the snapshot, so any
        # surface (the gate panel, the waiting inbox) renders it from the run
        # row alone. None for every other question.
        "decision": payload.get("decision") if isinstance(payload.get("decision"), dict) else None,
    }


def _flagged_filter(flagged: bool | None) -> dict[str, Any]:
    """The ORM filter for "raised review flags" (True), "clean" (False) or no filter (None)."""
    if flagged is None:
        return {}
    return {"review_flag_count__gt": 0} if flagged else {"review_flag_count": 0}


def _run_order(flagged_first: bool) -> tuple[str, ...]:
    """Newest first; or most review flags first, then newest."""
    return ("-review_flag_count", "-created_at") if flagged_first else ("-created_at",)


LIST_HEAVY_COLUMNS: tuple[str, ...] = ("input", "output", "interrupt_payload", "metadata")
"""Columns no runs LIST renders; ``list_for_definition(omit=...)`` leaves them unread."""


class RunStore:
    """CRUD over workflow.run — the row that tracks a single execution's lifecycle.

    Checkpoints and node outcomes are owned by the Checkpointer; this store
    only touches workflow.run (status, timestamps, final output/error). Separating
    the concerns keeps the Checkpointer protocol small and DB-agnostic.

    Status-transition discipline (audit P1-1/2/4): every status write is a
    GUARDED conditional UPDATE — never read-then-write. ``transition`` /
    ``claim_for_resume`` return whether the claim won, so concurrent
    callers (two tabs, double-click, racing schedulers) get exactly one
    winner and the losers can 409 instead of corrupting the run.
    """

    async def transition(
        self,
        run_id: str,
        *,
        from_statuses: tuple[str, ...] | list[str],
        to_status: str,
        clear_error: bool = False,
        set_error: dict[str, Any] | None = None,
        reattach_as: tuple[str | None, str | None] | None = None,
    ) -> bool:
        """Atomically move status from one of ``from_statuses`` → ``to_status``.

        Returns True iff THIS call performed the transition. One SQL
        statement — no check-then-act window.

        THE DEATH CERTIFICATE IS TORN UP ON THE WAY BACK TO LIFE. A run moving
        INTO ``running`` is alive again, so the terminal ``error`` that
        explained its previous death is cleared in the SAME statement. Without
        this, the lifecycle watchdog's ``run_stranded`` blob ("This run was
        dropped by our system before it could finish") survived the resume and
        then survived ``mark_completed`` — live 2026-09-13, runs d611933b and
        f748a361 of the Watson Parenting Adviser COMPLETED with real output
        while their row still said we had dropped them (W62). A row that says
        both "completed" and "we dropped this" is a screen that lies.

        ``clear_error=True`` drops the row's stored failure IN THE SAME
        statement. A recovery claim needs this: a run brought back from a
        terminal FAILED row would otherwise be ``running`` while still
        carrying the error that terminalized it, so every reader (the runs
        list, the run page, the next sweep) sees a live run that says it
        already failed. Clearing it separately would leave exactly that
        window open; the two facts are one transition.

        ``set_error`` is the mirror image, for the transition that gives up:
        the row goes terminal carrying the structured failure that explains
        WHY in the same statement, so a reader can never catch it terminal and
        silent. Passing both is a caller bug and raises.
        """
        if clear_error and set_error is not None:
            raise ValueError("transition(): pass clear_error OR set_error, never both")
        updates: dict[str, Any] = {"status": to_status}
        if to_status in ENDED_STATUSES:
            # Every ending stamps when it ended (the DB trigger run_stamp_completed_at is the second layer).
            updates["completed_at"] = datetime.now(UTC)
        if to_status == "running":
            # The claim IS a liveness signal (RUN_CLAIM_METADATA_KEY).
            updates["metadata"] = _claim_stamp()
        if to_status == "running" or clear_error:
            updates["error"] = None
        elif set_error is not None:
            updates["error"] = set_error
        filters: dict[str, Any] = {"id": str(UUID(run_id)), "status__in": list(from_statuses)}
        if to_status == "running":
            filters["deleted_at__isnull"] = True
        if reattach_as is not None:
            filters.update(_reattach_owner_filters(reattach_as))
        result = await get_model("WfRun").update_where(
            filters,
            returning=RUN_UPDATE_RETURNS,
            **updates,
        )
        return result.rows_affected == 1

    async def claim_for_resume(
        self,
        run_id: str,
        *,
        from_statuses: tuple[str, ...] | list[str] = RECOVERABLE_STATUSES,
    ) -> bool:
        """Atomically claim a parked run for resume (→ 'running').

        THE guard against the double-recovery race: two concurrent
        retries/resumes both pass a read-status check, but only ONE wins
        this conditional UPDATE — the loser must surface a 409, not spawn
        a second scheduler on the same run.
        """
        claimed = await self.transition(run_id, from_statuses=from_statuses, to_status="running")
        if claimed:
            await _announce_waiting(run_id, "resumed", "running", None)
        return claimed

    async def bump_recovery_counter(self, run_id: str) -> dict[str, Any]:
        """Atomically increment recovery_retry_count, enforcing the cap.

        Single UPDATE … WHERE count < max RETURNING — concurrent recovery
        requests cannot overshoot the limit (audit P1-3). Returns
        ``{"allowed": bool, "count": int, "max": int}``.
        """
        from matrx_orm import Compare, F

        result = await (
            get_model("WfRun")
            .filter(
                Compare(F("recovery_retry_count"), "<", F("max_recovery_retries")),
                id=str(UUID(run_id)),
            )
            .returning("id", "recovery_retry_count", "max_recovery_retries")
            .update(recovery_retry_count=F("recovery_retry_count") + 1)
        )
        if result.rows_affected:
            row = result.updated_rows[0]
            return {
                "allowed": True,
                "count": row["recovery_retry_count"],
                "max": row["max_recovery_retries"],
            }
        current_rows = await (
            get_model("WfRun")
            .filter(id=str(UUID(run_id)))
            .values("recovery_retry_count", "max_recovery_retries")
        )
        current = current_rows[0] if current_rows else None
        return {
            "allowed": False,
            "count": current["recovery_retry_count"] if current else -1,
            "max": current["max_recovery_retries"] if current else -1,
        }

    async def create(
        self,
        *,
        definition_id: str,
        definition_hash: str,
        thread_id: str | None = None,
        parent_run_id: str | None = None,
        definition_version_id: str | None = None,
        inputs: dict[str, Any] | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
        conversation_id: str | UUID | None = None,
        request_attribution_complete: bool | None = None,
        agent_id: str | None = None,
        agent_version_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        status: str = "running",
        run_id: str | None = None,
    ) -> str:
        # ``run_id`` (optional): callers with a DETERMINISTIC run identity —
        # durable subgraph children derive theirs from the parent invocation's
        # correlation key so crash-replay reattaches instead of duplicating —
        # pass it explicitly; the PK collision is then the (desired) guard
        # against two racing creators. Omitted → a fresh uuid4, as always.
        # ``status`` defaults to 'running' (a live run about to execute
        # in-process). A QUEUED run must pass 'pending' — it is not running
        # until a worker claims its wf_job and calls mark_running; born-
        # 'running' queued rows made a missing worker invisible. A step-mode
        # run inserts 'paused' directly so it's a recoverable frontier from
        # birth — no millisecond 'running'-with-no-task window for the
        # watchdog to flag. Guard the input so a typo can't create an invalid row.
        if status not in _VALID_CREATE_STATUSES:
            raise ValueError(
                f"RunStore.create: invalid status {status!r} "
                f"(allowed: {sorted(_VALID_CREATE_STATUSES)})"
            )
        run_id = str(UUID(run_id)) if run_id else str(uuid4())
        thread_id = thread_id or run_id

        # ── EVERY RUN BELONGS TO AN ORGANIZATION ────────────────────────────
        # Arman's ruling, 2026-08-23: **there is no such thing as a detached
        # workflow.** An org-less run is not a supported shape; if we ever
        # genuinely need one for internal work, that is a special case built
        # deliberately, never a None that slips through.
        #
        # This is the ONE boundary all twelve create-sites pass through, so the
        # rule lives here instead of in twelve `or`-chains that each drift.
        #
        # A DERIVED RUN INHERITS ITS PARENT'S ORG. Forks, durable subgraph
        # children, A/B arms and race arms are continuations of one run — their
        # org is that run's, by product rule (Arman, 2026-08-23), independent
        # of whether `ctx` happens to carry one. This is a deliberate policy,
        # not merely a ContextVar workaround: `RunStore.create` is reached
        # from twelve call sites across several lanes — some in-request with
        # an explicit `ctx` parameter (e.g. `prepare_forked_run`, no ambient
        # read at all), some detached tasks, some workers — so trusting `ctx`
        # here would mean re-litigating reliability per lane forever. Reading
        # the parent's row instead means it is correct everywhere at once.
        # (`create_streaming_response` not installing the ctx it was handed
        # was ONE instance of this class — fixed at its root by 7f3039cadc,
        # the contextvar trap `definition_run.durable_run_organization`
        # exists for, which cost a full day on 2026-08-18 — but that fix
        # only covers streaming-route legs, not every lane this runs under.)
        #
        # WHY THIS RAISES INSTEAD OF LETTING THE DATABASE COPE: the column is
        # NOT NULL, so a None here does not fail — `platform.stamp_run_org`
        # silently assigns the OWNER'S PERSONAL org. That is a *wrong* answer
        # wearing a right one's clothes: the row looks scoped, the run is
        # invisible to the org that started it, and nothing anywhere records
        # that a guess was made. A loud refusal at creation is recoverable; a
        # silently mis-scoped run is not (db-rules §0.9 — the database never
        # chooses an organization).
        if not organization_id and parent_run_id is not None:
            parent_rows = await (
                get_model("WfRun")
                .filter(id=str(UUID(str(parent_run_id))))
                .values("organization_id")
            )
            if parent_rows and parent_rows[0].get("organization_id"):
                organization_id = str(parent_rows[0]["organization_id"])
        if not organization_id:
            raise ValueError(
                "RunStore.create: this run has no organization. Every workflow "
                "run belongs to one — pass organization_id explicitly (a "
                "derived run inherits its parent's automatically). Reading it "
                "from AppContext is not reliable on a detached leg: resolve it "
                "from the run row, the trigger, or the request body."
            )

        create_fields: dict[str, Any] = {
            "id": run_id,
            "thread_id": str(UUID(thread_id)),
            "parent_run_id": _to_uuid(parent_run_id),
            "definition_id": str(UUID(definition_id)),
            "definition_version_id": _to_uuid(definition_version_id),
            "definition_hash": definition_hash,
            "status": status,
            "input": inputs or {},
            "metadata": _origin_metadata(metadata),
            "created_by": _require_optional_uuid(user_id, "user_id"),
            "organization_id": _to_uuid(organization_id),
            "project_id": _to_uuid(project_id),
            "task_id": _to_uuid(task_id),
            "conversation_id": _require_optional_uuid(conversation_id, "conversation_id"),
            "agent_id": _to_uuid(agent_id),
            "agent_version_id": _to_uuid(agent_version_id),
            "started_at": datetime.now(UTC),
        }
        if request_attribution_complete is not None:
            create_fields["request_attribution_complete"] = request_attribution_complete
        await get_model("WfRun").create(**create_fields)
        await self._input_values_by_reference(run_id, create_fields["metadata"], organization_id=organization_id)
        return run_id

    async def _input_values_by_reference(
        self, run_id: str, metadata: dict[str, Any], *, organization_id: str | None = None
    ) -> None:
        """Move the large ``metadata._settings.input_values`` of a just-written row into the run's value store.

        ``metadata`` is what the row now holds. Every heartbeat, claim stamp and status write is a
        ``jsonb_set`` / merge on ``metadata``, and Postgres rewrites the WHOLE jsonb value each time: a child
        seeded with Smart Add's ~6 MB ``evidence`` paid ~200 ms per write (vs ~1 ms on a small row, measured
        2026-10-28 on child 319da0a6) and its event writer fell 2–7 s behind. The row keeps the small values and
        a reference per large one; :meth:`load` resolves them back, so every reader sees exactly what was
        written. Values are stored BEFORE the row is rewritten (no reader ever sees a reference whose value is
        missing). A failure leaves the values inline — slower, never wrong — and says so."""
        new_settings = await input_values_settings_by_reference(run_id, metadata, organization_id=organization_id)
        if new_settings is None:
            return
        try:
            await update_run({"id": run_id}, metadata=JsonbMerge("metadata", {"_settings": new_settings}))
        except Exception:  # noqa: BLE001 — the row stays whole; only the speed-up is lost
            logger.exception("[wf:%s] input values stay INLINE on the run row (by-reference rewrite failed)", run_id[:8])

    async def merge_metadata(self, run_id: str, patch: dict[str, Any]) -> None:
        """Shallow-merge keys into workflow.run.metadata (new keys win). A ``_settings`` carrying large
        ``input_values`` (a parked run's merged inputs) lands by reference, like :meth:`create`."""
        if isinstance(patch.get("_settings"), dict):
            settings = await input_values_settings_by_reference(str(UUID(run_id)), patch)
            if settings is not None:
                patch = {**patch, "_settings": settings}
        await update_run(
            {"id": str(UUID(run_id))},
            metadata=JsonbMerge("metadata", patch),
        )

    async def mark_interrupted(
        self,
        run_id: str,
        *,
        interrupt_payload: dict[str, Any],
        last_checkpoint_id: str | None = None,
        steps_executed: int = 0,
        output: dict[str, Any] | None = None,
    ) -> None:
        """Park the run ``interrupted`` and write the "waiting on you" snapshot.

        ``interrupt_payload`` is the scheduler's ``RunResult.interrupt`` —
        ``{node_id, payload, checkpoint_id}`` — stored verbatim in the column
        (the resume path replays from it). BESIDE it, ``metadata._interrupt``
        gets the FLAT snapshot (SPEC-workflow-ui-contract §4.3 leg 2): one read
        of ``workflow.run`` answers *what is this run waiting for* — no event
        replay, no checkpoint fetch. Written in the SAME statement as the
        status, so a run is never ``interrupted`` with a stale snapshot.

        ``output`` is the scheduler's partial ``last_outputs`` at park time —
        MERGED over prior output, like mark_errored. A resume restarts its
        ``last_outputs`` empty, so without this a node that finished BEFORE the
        question (a deliverable) would be missing from the completed run row."""
        output = await _output_by_reference(run_id, output)
        updates: dict[str, Any] = {
            "status": "interrupted",
            "interrupt_payload": interrupt_payload,
            "steps_executed": steps_executed,
            "output": JsonbMerge("output", output or {}),
            "metadata": JsonbMerge(
                "metadata", {"_interrupt": build_interrupt_snapshot(interrupt_payload)}
            ),
        }
        # COALESCE($3, last_checkpoint_id) — only overwrite when provided.
        cp = _to_uuid(last_checkpoint_id)
        if cp is not None:
            updates["last_checkpoint_id"] = cp
        await get_model("WfRun").update_where({"id": str(UUID(run_id))}, returning=RUN_UPDATE_RETURNS, **updates)
        await _announce_waiting(run_id, "waiting", "interrupted", interrupt_payload)

    async def mark_awaiting_input(
        self,
        run_id: str,
        *,
        interrupt_payload: dict[str, Any],
        steps_executed: int = 0,
    ) -> None:
        """Park the run ``awaiting_input`` (INPUT-SURFACE.md park-not-die).

        A headless start missing a require/ask input holds here instead of
        dying: durable, discoverable in the same "waiting on you" inbox as
        ``interrupted`` (the status-change announce fires like any other),
        resumable the moment anyone supplies the value. ``interrupt_payload``
        carries ``{"kind": "awaiting_input", "missing": [...]}`` — the gap
        list, per-input name/kind/sourcing — so any surface can render the
        exact form. Guarded: never flips a terminal run."""
        result = await get_model("WfRun").update_where(
            {"id": str(UUID(run_id)), "status__not_in": ["completed", "failed", "cancelled"]},
            returning=RUN_UPDATE_RETURNS,
            status="awaiting_input",
            interrupt_payload=interrupt_payload,
            steps_executed=steps_executed,
        )
        if result.rows_affected:
            await _announce_waiting(run_id, "waiting", "awaiting_input", interrupt_payload)

    async def mark_completed(
        self,
        run_id: str,
        *,
        output: dict[str, Any],
        steps_executed: int,
        stopped: dict[str, Any] | None = None,
    ) -> bool:
        return (await self._mark_completed(run_id, output=output, steps_executed=steps_executed, stopped=stopped))[0]

    async def _mark_completed(
        self,
        run_id: str,
        *,
        output: dict[str, Any],
        steps_executed: int,
        stopped: dict[str, Any] | None = None,
        alongside: Callable[[], Awaitable[Any]] | None = None,
        prior_output: dict[str, Any] | None = None,
        never_parked: bool = False,
    ) -> tuple[bool, dict[str, Any] | None]:
        """Guarded: a run that already ended failed/cancelled stays that way
        (audit P1-4 — racing terminal writers must not flip each other).

        Output MERGES over any prior partial output (new keys win). The
        scheduler restarts ``last_outputs = {}`` on every resume, so a
        recovered run's completion payload only carries post-resume nodes —
        a plain overwrite would erase the pre-park (paid) nodes that
        mark_errored preserved, leaving a COMPLETED run with less data than
        its errored predecessor."""
        # Atomic jsonb merge (`output = COALESCE(output,'{}') || $2::jsonb`) —
        # matrx_orm.JsonbMerge — fused with the terminal-status CAS guard in
        # ONE statement via update_where's filters, so no read-merge-write
        # race reopens between the guard check and the write.
        # ``stopped``: why a clean finish stopped early (executor/run_stop.py), written in the
        # SAME statement as the completion. ALWAYS written — null when this finish declared no
        # stop — so a resumed run never keeps an earlier attempt's stale reason (the top-level
        # JsonbMerge replaces the key). Display only: the owner can write metadata.
        from matrx_graph.executor.run_stop import RUN_STOP_METADATA_KEY

        from matrx_utils.diagnostics.phase_clock import timed

        output = await timed(
            "settle.output_by_reference",
            _output_by_reference(run_id, output)
            if prior_output is None
            else _output_by_reference_known(run_id, output, prior_output),
        )
        return await self._write_terminal(
            run_id,
            {"id": str(UUID(run_id)), "status__not_in": ["failed", "cancelled"]},
            "completed",
            alongside=alongside,
            metadata_merge={RUN_STOP_METADATA_KEY: stopped or None},
            never_parked=never_parked,
            status="completed",
            output=JsonbMerge("output", output),
            steps_executed=steps_executed,
            completed_at=datetime.now(UTC),
            interrupt_payload=None,
            # A COMPLETED run has no error, full stop. The second half of the
            # W62 fix: a run force-failed by the watchdog and then resumed
            # reaches here carrying that ``run_stranded`` blob, and preserving
            # it published a successful answer under a failure notice.
            error=None,
        )

    async def _write_terminal(
        self,
        run_id: str,
        filters: dict[str, Any],
        settled_as: str,
        *,
        cancel_reason: str | None = None,
        alongside: Callable[[], Awaitable[Any]] | None = None,
        metadata_merge: dict[str, Any] | None = None,
        never_parked: bool = False,
        **updates: Any,
    ) -> tuple[bool, dict[str, Any] | None]:
        """THE terminal write every ending runs: one guarded UPDATE handing back the row it left
        (``terminal_run_returns()``), then both settle hooks with that row — and ``alongside`` — at once.
        Returns ``(applied, row)``; ``row`` is unresolved (output / input values may hold references) and None
        when the write was refused or the store handed back no whole row."""
        from matrx_utils.diagnostics.phase_clock import timed

        # The after-work's durable marker rides THIS statement (no round trip of its own): set, a crash before the
        # work ran is repaired by ``recover_settle_after``; cleared once it ran.
        if "metadata" in updates:
            raise TypeError("a terminal write merges metadata through metadata_merge=, never metadata=")
        after_owed = _settle_after_owed(alongside)
        marker_token: str | None = None
        merge = dict(metadata_merge or {})
        if after_owed:
            marker_token = uuid4().hex
            merge[SETTLE_AFTER_KEY] = {"pending": True, "cancel_reason": cancel_reason, "token": marker_token}
        if merge:
            updates["metadata"] = JsonbMerge("metadata", merge)
        result = await timed(
            "settle.write",
            get_model("WfRun").update_where(filters, returning=terminal_run_returns(), **updates),
        )
        if getattr(result, "rows_affected", 0) != 1:
            return False, None
        row: dict[str, Any] | None = None
        returned = getattr(result, "updated_rows", None)
        if isinstance(returned, list) and returned and isinstance(returned[0], dict) and "thread_id" in returned[0]:
            try:
                row = _row_to_run_dict(returned[0])
                for omitted in TERMINAL_RUN_OMITS:
                    if omitted not in returned[0]:
                        row.pop(omitted, None)
            except Exception:  # noqa: BLE001 — the end is written; each reader loads the row itself instead
                logger.warning("[wf:%s] the terminal write's row could not be read back", str(run_id)[:8], exc_info=True)
        await _announce_settled(
            run_id, settled_as, cancel_reason, row=row, alongside=alongside, never_parked=never_parked,
            after_owed=after_owed, marker_token=marker_token,
        )
        return True, row

    @staticmethod
    def _sanitize_error(error: dict[str, Any]) -> dict[str, Any]:
        """THE last gate before ``workflow.run.error``.

        Terminal color formatting must never be persisted as a user-facing
        error — three live rows carry ``[91m`` escapes because the matrx-orm
        IntegrityError renderer writes for a terminal and the engine
        stringified that render. ``matrx_graph.failure`` strips on the way in;
        this strips again so a payload assembled anywhere else (a host route,
        a sweeper) cannot smuggle one past. Recurses into nested structure and
        leaves non-string leaves untouched.
        """
        from matrx_graph.failure import client_safe_error_payload, strip_ansi

        def clean(value: Any) -> Any:
            if isinstance(value, str):
                return strip_ansi(value)
            if isinstance(value, dict):
                return {k: clean(v) for k, v in value.items()}
            if isinstance(value, list):
                return [clean(v) for v in value]
            return value

        # Prose keys (message / technical) are also cut before SQL, bound args,
        # tracebacks and maintainer hints — the Studio renders this column.
        return client_safe_error_payload(clean(error))

    async def mark_failed(
        self,
        run_id: str,
        *,
        error: dict[str, Any],
        steps_executed: int = 0,
    ) -> bool:
        return (await self._mark_failed(run_id, error=error, steps_executed=steps_executed))[0]

    async def _mark_failed(
        self,
        run_id: str,
        *,
        error: dict[str, Any],
        steps_executed: int = 0,
        alongside: Callable[[], Awaitable[Any]] | None = None,
        never_parked: bool = False,
    ) -> tuple[bool, dict[str, Any] | None]:
        """Guarded: never flips a completed/cancelled run to failed.

        A failed run ALWAYS records why: an empty ``error`` is replaced by an explicit marker
        naming this path (2026-10-16: 8 failed runs carried no reason at all)."""
        if not error or not any(error.values()):
            error = {
                "message": "no reason recorded by run_store.mark_failed (the caller passed an empty error)",
                "cause": "no_reason_recorded",
                "source": "run_store.mark_failed",
            }
        return await self._write_terminal(
            run_id,
            {
                "id": str(UUID(run_id)),
                "status__not_in": ["completed", "cancelled"],
            },
            "failed",
            alongside=alongside,
            never_parked=never_parked,
            status="failed",
            error=self._sanitize_error(error),
            steps_executed=steps_executed,
            completed_at=datetime.now(UTC),
        )

    async def fail_unstarted(self, run_id: str, *, error: dict[str, Any]) -> bool:
        """End FAILED a run still ``pending`` or ``running`` whose job failed terminally before the run loop owned
        it — through THE terminal write like every other ending (sanitized error, ``completed_at``, the settle hooks
        with the row). A run any other status already holds is never overwritten. True iff this call ended it."""
        applied, _row = await self._write_terminal(
            run_id,
            {"id": str(UUID(run_id)), "status__in": ["pending", "running"]},
            "failed",
            status="failed",
            error=self._sanitize_error(error),
            completed_at=datetime.now(UTC),
        )
        return applied

    async def mark_running(self, run_id: str, *, metadata_patch: dict[str, Any] | None = None) -> bool:
        """Claim execution without erasing a concurrent control request.

        A queued worker may race a pause/cancel call after claiming its job.
        Only ``pending`` or already-``running`` rows may become running; a
        ``pausing``/``cancelling`` status is authoritative and must survive
        worker startup so the scheduler can honor it.

        ``metadata_patch`` lands in the SAME statement as the claim (shallow merge beside the claim
        stamp), so a caller's claim-time facts (the executor stamp) cost no second write.
        """
        result = await get_model("WfRun").update_where(
            {"id": str(UUID(run_id)), "status__in": ["pending", "running"]},
            returning=RUN_UPDATE_RETURNS,
            status="running",
            metadata=_claim_stamp(metadata_patch),
        )
        return result.rows_affected == 1

    async def mark_paused(
        self,
        run_id: str,
        *,
        last_checkpoint_id: str | None = None,
        steps_executed: int = 0,
        output: dict[str, Any] | None = None,
    ) -> None:
        """Mark a run as paused. Mirrors mark_interrupted's shape (non-
        terminal, resumable) but carries no payload — the scheduler stopped
        cleanly at a super-step boundary, not in the middle of a node."""
        output = await _output_by_reference(run_id, output)
        updates: dict[str, Any] = {
            "status": "paused",
            "steps_executed": steps_executed,
            # Partial last_outputs merged (a resume restarts last_outputs empty).
            "output": JsonbMerge("output", output or {}),
        }
        cp = _to_uuid(last_checkpoint_id)
        if cp is not None:
            updates["last_checkpoint_id"] = cp
        await get_model("WfRun").update_where({"id": str(UUID(run_id))}, returning=RUN_UPDATE_RETURNS, **updates)

    async def mark_pausing(self, run_id: str) -> bool:
        """Mark a running run as pausing. Same idempotency contract as
        mark_cancelling — only 'pending' or 'running' → 'pausing'."""
        result = await get_model("WfRun").update_where(
            {"id": str(UUID(run_id)), "status__in": ["pending", "running"]},
            returning=RUN_UPDATE_RETURNS,
            status=RunControlStatus.PAUSING.value,
        )
        return result.rows_affected == 1

    async def is_pausing(self, run_id: str) -> bool:
        """Cheap poll for the scheduler's pause_check hook."""
        rows = await get_model("WfRun").filter(id=str(UUID(run_id))).values("status")
        return bool(rows and rows[0]["status"] == RunControlStatus.PAUSING.value)

    async def mark_errored(
        self,
        run_id: str,
        *,
        error: dict[str, Any],
        last_checkpoint_id: str | None = None,
        steps_executed: int = 0,
        output: dict[str, Any] | None = None,
    ) -> bool:
        """Mark a run as errored (recoverable). The user can recover via
        /runs/:id/nodes/:nid/{retry,skip,manual-result} and then resume.

        ``output`` is the scheduler's partial ``last_outputs`` at park time.
        Dropping it hides every COMPLETED (paid) node's result from the run
        row — a 14s LLM step read as never-ran with $0 cost (2026-07-07
        agent-plan incident). MERGES over prior output (a re-park after a
        recovery resume only carries post-resume nodes); mark_completed
        merges the same way, so the final row accumulates every leg.

        Guarded like the other terminal writers (audit P1-4): a run that
        already ended completed/failed/cancelled is never flipped back to
        errored by a zombie scheduler parking late."""
        # Atomic jsonb merge (`output = COALESCE(output,'{}') ||
        # COALESCE($5,'{}')`) — merging with an empty dict when ``output`` is
        # None is a no-op, so JsonbMerge("output", output or {}) matches the
        # original COALESCE($5::jsonb,'{}') exactly — fused with the
        # COALESCE checkpoint update and the terminal-status CAS guard in ONE
        # statement.
        output = await _output_by_reference(run_id, output)
        updates: dict[str, Any] = {
            "status": "errored",
            "error": self._sanitize_error(error),
            "steps_executed": steps_executed,
            "output": JsonbMerge("output", output or {}),
            # Every ending stamps when it ended (errored is one: it wakes the chat). Without it the
            # chat dock's "failed since you last looked" never matched 786 of 789 errored runs.
            # The DB trigger workflow.run_stamp_completed_at is the second layer for any writer.
            "completed_at": datetime.now(UTC),
        }
        cp = _to_uuid(last_checkpoint_id)
        if cp is not None:
            updates["last_checkpoint_id"] = cp
        applied, _row = await self._write_terminal(
            run_id,
            {"id": str(UUID(run_id)), "status__not_in": ["completed", "failed", "cancelled"]},
            "errored",
            **updates,
        )
        return applied

    async def mark_cancelling(self, run_id: str, *, hard: bool = False, why: str = "stop_now") -> bool:
        """Mark a live run as canceling. Returns True if the row was
        updated (was in a cancellable state), False otherwise.

        ``pausing`` is included so a later Cancel can supersede a Pause that
        has not parked yet. Parked runs have no worker to observe
        ``cancelling`` and use ``mark_parked_cancelled`` instead. Terminal
        states no-op so the endpoint stays idempotent after completion.

        GRACEFUL (the default) stops THIS run only: it sends nothing new, and a called workflow
        already working for one of its steps finishes its whole chain, saves included (G1 ruling,
        2026-11-01; packages/matrx-graph/matrx_graph/executor/FEATURE.md § Stop and Pause mid-wave). A child that has not started never starts —
        the caller's step is held. HARD (``hard=True``: "stop now", or a second Stop on a run
        already ``cancelling``) also cancels every live called workflow under it, and says so on
        each row: ``metadata._hard_stop = {why, at[, by]}`` — the run's end status names the hard
        stop. A hard stop on a run that is not live or ``cancelling`` is a no-op (False).
        """
        result = await get_model("WfRun").update_where(
            {
                "id": str(UUID(run_id)),
                "status__in": ["pending", "running", "pausing"],
            },
            returning=RUN_UPDATE_RETURNS,
            status=RunControlStatus.CANCELLING.value,
        )
        transitioned = result.rows_affected == 1
        if not hard:
            return transitioned
        if not transitioned and await self.control_status(run_id) != RunControlStatus.CANCELLING.value:
            return False
        at = datetime.now(UTC).isoformat()
        await self.merge_metadata(run_id, {"_hard_stop": {"why": why, "at": at}})
        await self._cancel_live_descendants(run_id, stamp={"_hard_stop": {"why": why, "at": at, "by": run_id}})
        return True

    async def _cancel_live_descendants(self, run_id: str, *, stamp: dict[str, Any]) -> None:
        """A HARD stop reaches every live CALLED workflow under the run (``subgraph.call`` children,
        marked by ``metadata.subgraph_parent``, down the ``parent_run_id`` chain), each stamped.

        A called workflow's control check reads only its OWN row — the status its checkpoint save
        already reads back (no round trip per step boundary, PF-WF 2026-11-02). Only called
        workflows: a fork or re-run of this run also carries ``parent_run_id`` and is a run of its
        own, never cancelled with its source. Idempotent; never raises (the run's own cancel already
        landed) — a failed walk is loud."""
        model = get_model("WfRun")
        live = ["pending", "running", "pausing"]
        frontier = [str(UUID(run_id))]
        seen: set[str] = set(frontier)
        try:
            while frontier:
                rows = await model.filter(
                    parent_run_id__in=frontier,
                    status__in=live,
                    deleted_at=None,
                    metadata__json_has_key="subgraph_parent",
                ).values("id")
                children = [str(row["id"]) for row in rows if str(row["id"]) not in seen]
                if not children:
                    return
                seen.update(children)
                await model.update_where(
                    {"id__in": children, "status__in": live},
                    returning=RUN_UPDATE_RETURNS,
                    status=RunControlStatus.CANCELLING.value,
                    metadata=JsonbMerge("metadata", stamp),
                )
                frontier = children
        except Exception:  # noqa: BLE001 — the run's cancel stands; its children are named
            logger.exception(
                "[wf:%s] cancel did not reach its called workflows — they stop at their own end",
                run_id[:8],
            )

    async def mark_parked_cancelled(self, run_id: str) -> bool:
        """Atomically cancel a run that has no active scheduler.

        A paused/interrupted/errored run cannot be left at ``cancelling``:
        there is no worker to advance it. The status guard also closes the
        cancel-vs-resume race; if resume already claimed ``running``, this
        write loses and the live-path cancellation transition handles it.
        """
        applied, _row = await self._write_terminal(
            run_id,
            {
                "id": str(UUID(run_id)),
                "status__in": ["paused", "interrupted", "errored", "awaiting_input"],
            },
            "cancelled",
            status="cancelled",
            completed_at=datetime.now(UTC),
        )
        return applied

    async def mark_cancelling_settled(self, run_id: str, *, why: str) -> bool:
        """Settle a run stuck at ``cancelling`` whose holder is gone: ``cancelling`` -> ``cancelled``.

        ``cancelling`` is a request the run's worker answers at its next poll; when no worker holds the
        run any more (its task died, its lease lapsed) nobody ever will, and the run, with every ancestor
        that refuses to be deleted under it, waits forever (4999ac17, 2026-11-15). The caller has judged
        the holder gone; this is only the CAS (status must still be ``cancelling``, so a run that settled
        or resumed meanwhile is untouched). The marker is ``_cancel.reason = 'graceful'``: a person's stop,
        never auto-resumed by the shutdown reconciliation (which resumes only ``'immediate'``)."""
        at = datetime.now(UTC)
        applied, _row = await self._write_terminal(
            run_id,
            {"id": str(UUID(run_id)), "status": RunControlStatus.CANCELLING.value},
            "cancelled",
            cancel_reason="graceful",
            status="cancelled",
            completed_at=at,
            metadata_merge={"_cancel": {"reason": "graceful", "settled_without_holder": why, "at": at.isoformat()}},
        )
        return applied

    async def end_unanswered(
        self,
        run_id: str,
        *,
        reason: str,
        node_id: str | None = None,
        deadline_at: str | None = None,
        checkpoint_id: str | None = None,
    ) -> list[str]:
        """End a run that is WAITING ON A PERSON because nobody answered in time.

        Guarded on the two waiting statuses, so it is the same race the resume
        claim runs: a person who answered first has already moved the run to
        ``running`` and this write loses — their answer stands. The run ends
        ``failed`` carrying ``reason`` as its message and the stable cause
        ``nobody_answered``, which every run surface already shows. Called
        workflows parked under it (their question was this run's question) end
        the same way, so ending the asker never strands the asked.

        ``checkpoint_id`` is the question the caller judged: the write matches
        only while the run is still parked on THAT checkpoint. A person who
        answered it, after which the run parked on a NEW question, has a run
        that is waiting again — on something nobody's deadline has run out on.

        Returns the ids of every run it ended, this run first; empty when the
        write was refused (so it reads as a yes/no too).
        """
        from matrx_graph.failure import Cause

        error = {
            "message": reason,
            "cause": Cause.NOBODY_ANSWERED,
            "error_type": Cause.NOBODY_ANSWERED,
            "node_id": node_id,
            "deadline_at": deadline_at,
            "source": "run_store.end_unanswered",
        }
        filters: dict[str, Any] = {"id": str(UUID(run_id)), "status__in": list(WAITING_STATUSES)}
        parked_on = _to_uuid(checkpoint_id)
        if parked_on is not None:
            filters["last_checkpoint_id"] = parked_on
        applied, _row = await self._write_terminal(
            run_id,
            filters,
            "failed",
            status="failed",
            error=self._sanitize_error({k: v for k, v in error.items() if v is not None}),
            completed_at=datetime.now(UTC),
        )
        if not applied:
            return []
        return [str(UUID(run_id)), *await self._end_waiting_descendants(run_id, error=error)]

    async def _end_waiting_descendants(self, run_id: str, *, error: dict[str, Any]) -> list[str]:
        """Called workflows still waiting under an ended run end with it. Never raises: the
        run's own end already landed; a failed walk is loud and the host's sweep ends each
        leftover on its own deadline."""
        model = get_model("WfRun")
        frontier = [str(UUID(run_id))]
        seen: set[str] = set(frontier)
        ended: list[str] = []
        try:
            while frontier:
                rows = await model.filter(
                    parent_run_id__in=frontier,
                    status__in=list(WAITING_STATUSES),
                    deleted_at=None,
                    metadata__json_has_key="subgraph_parent",
                ).values("id")
                children = [str(row["id"]) for row in rows if str(row["id"]) not in seen]
                if not children:
                    return ended
                seen.update(children)
                for child in children:
                    applied, _row = await self._write_terminal(
                        child,
                        {"id": child, "status__in": list(WAITING_STATUSES)},
                        "failed",
                        status="failed",
                        error=self._sanitize_error(
                            {k: v for k, v in {**error, "ended_with_run": run_id}.items() if v is not None}
                        ),
                        completed_at=datetime.now(UTC),
                    )
                    if applied:
                        ended.append(child)
                frontier = children
        except Exception:  # noqa: BLE001 — the run's own end stands
            logger.exception(
                "[wf:%s] ending the run did not reach its waiting called workflows", run_id[:8]
            )
        return ended

    async def mark_cancelled(self, run_id: str, *, steps_executed: int, cancel_reason: str | None = None) -> bool:
        """Guarded: never flips a completed/failed run to canceled. ``cancel_reason`` only travels to the
        run-settled hook (``'immediate'`` = the task was killed under the run, which may resume it)."""
        return (await self._mark_cancelled(run_id, steps_executed=steps_executed, cancel_reason=cancel_reason))[0]

    async def _mark_cancelled(
        self,
        run_id: str,
        *,
        steps_executed: int,
        cancel_reason: str | None = None,
        alongside: Callable[[], Awaitable[Any]] | None = None,
        never_parked: bool = False,
    ) -> tuple[bool, dict[str, Any] | None]:
        return await self._write_terminal(
            run_id,
            {
                "id": str(UUID(run_id)),
                "status__not_in": ["completed", "failed"],
            },
            "cancelled",
            cancel_reason=cancel_reason,
            alongside=alongside,
            never_parked=never_parked,
            status="cancelled",
            steps_executed=steps_executed,
            completed_at=datetime.now(UTC),
        )

    async def control_status(self, run_id: str) -> str | None:
        """The run's status in ONE read — the scheduler's ``control_check``,
        answering its pause and cancel polls together."""
        rows = await get_model("WfRun").filter(id=str(UUID(run_id))).values("status")
        return str(rows[0]["status"]) if rows else None

    async def control_statuses(self, run_ids: list[str]) -> dict[str, str]:
        """Several runs' statuses in ONE read (a called child's control check reads its own
        row and its caller's together — one round trip per step boundary, not two)."""
        given = {str(UUID(r)): r for r in run_ids if r}
        if not given:
            return {}
        rows = await get_model("WfRun").filter(id__in=list(given)).values("id", "status")
        # Keyed by the id exactly as the caller passed it.
        return {given[str(row["id"])]: str(row["status"]) for row in rows}

    async def is_cancelling(self, run_id: str) -> bool:
        """Cheap poll for the scheduler's cancel_check hook."""
        rows = await get_model("WfRun").filter(id=str(UUID(run_id))).values("status")
        return bool(rows and rows[0]["status"] == RunControlStatus.CANCELLING.value)

    async def load_metadata_fields(
        self, run_id: str, *, organization_id: str, **paths: tuple[str, ...]
    ) -> dict[str, Any] | None:
        """Read named JSON paths from a live run without fetching the run payload."""
        if not paths or any(not path for path in paths.values()):
            raise ValueError("Select at least one nonempty run metadata path.")
        fields = [Projection(JsonPath(F("metadata"), *path, as_text=False), alias) for alias, path in paths.items()]
        rows = await get_model("WfRun").filter(
            id=str(UUID(run_id)), organization_id=str(UUID(organization_id)), deleted_at__isnull=True,
        ).values(*fields)
        return rows[0] if rows else None

    async def load(
        self,
        run_id: str,
        *,
        resolve_output: bool = True,
        missing: str = "raise",
        resolve_inputs: bool = True,
        reattach_as: tuple[str | None, str | None] | None = None,
    ) -> dict[str, Any] | None:
        """One run, its ``output`` whole: a step output the row keeps by reference (over the
        ``workflow.run_output.inline_value_max_bytes`` knob) is resolved from the run's value store here, so
        every server reader (a subgraph.call reattaching to a finished child, a plan step, a mandate's answer,
        a chat wake) reads exactly what the run produced.

        ``resolve_output=False`` reads the row only (owner / status / org checks, sweeps): the value store is
        not touched for ``output``, and ``output`` may hold references — never hand it on as an answer; resolve
        it with :meth:`resolve_output` first. A referenced value that is gone raises
        :class:`RunOutputValueMissingError`; only the display read passes ``missing="mark"`` for the honest
        ``{"output_elided": true, "missing": true}`` marker.

        The stored input values are resolved by default. Pass ``resolve_inputs=False`` when the
        caller must check the run's identity before following stored input references.
        ``reattach_as=(actor_id, organization_id)`` also checks ownership and retirement before
        fetching inline values. A found but unavailable run raises ``RunReattachRefused``.
        A gone input NEVER raises from a load: an owner
        check, a cancel, a delete or a sweep of a run whose input is gone must still work (2026-10-28 review:
        an errored run with a missing input 500'd on view / cancel / delete). Only a leg about to EXECUTE the
        run raises, through :func:`execution_input_values`."""
        query = get_model("WfRun").filter(id=str(UUID(run_id)))
        if reattach_as is not None:
            identity = await query.values("created_by", "organization_id", "deleted_at")
            if not identity:
                return None
            owner_filters = _reattach_owner_filters(reattach_as)
            owner = identity[0]
            saved_actor = str(owner["created_by"]) if owner["created_by"] is not None else None
            if str(owner["organization_id"]) != owner_filters["organization_id"] or saved_actor != owner_filters.get("created_by"):
                raise RunReattachRefused(
                    "This retry key belongs to a different caller or organization. Start with a new key."
                )
            if owner["deleted_at"] is not None:
                raise RunReattachRefused("This workflow run was retired. Start with a new key.")
            # Repeat the authorization predicates on the payload read. A change after
            # the projection must never expose the new owner's values or start a new run.
            query = query.filter(**owner_filters)
        rows = await query.values()
        if not rows:
            if reattach_as is not None:
                raise RunReattachRefused("This workflow run changed while retrying. Retry with the same key.")
            return None
        run = _row_to_run_dict(rows[0])
        if resolve_inputs:
            await resolve_input_values(run)
        if resolve_output:
            await self.resolve_output(run, missing=missing)
        return run

    @asynccontextmanager
    async def completed_reattachment(
        self, run_id: str, *, reattach_as: tuple[str | None, str | None]
    ) -> AsyncIterator[dict[str, Any]]:
        """Keep a completed run's owner and retirement state stable while its answer is read."""
        from matrx_orm import transaction
        from matrx_orm.core.config import resolve_database_name
        from matrx_orm.core.transaction import get_active_database_name

        model = get_model("WfRun")
        active_database = get_active_database_name()
        if active_database is not None and active_database != resolve_database_name(model._database):
            raise RunReattachRefused("The saved workflow cannot be read in this transaction.")
        filters = _reattach_owner_filters(reattach_as)
        async with transaction(model._database):
            rows = await (
                model.filter(id=str(UUID(run_id)), status="completed", **filters)
                .select_for_update(mode="SHARE")
                .values("id", "definition_id", "status", "output", "started_at", "completed_at")
            )
            if not rows:
                raise RunReattachRefused(
                    "This retry key belongs to a different caller or organization, or the workflow is no longer completed."
                )
            run = rows[0]
            run["output"] = _coerce_run_json(run["output"])
            yield run

    @asynccontextmanager
    async def resume_reattachment(
        self, run_id: str, *, reattach_as: tuple[str | None, str | None]
    ) -> AsyncIterator[dict[str, Any]]:
        """Read a parked run under its owner lock, then claim it on successful admission."""
        from matrx_orm import transaction
        from matrx_orm.core.transaction import get_active_database_name

        # The scheduler and resumed notification must run after the claim commits.
        if get_active_database_name() is not None:
            raise RunReattachRefused("The saved workflow cannot be resumed inside another transaction.")
        model = get_model("WfRun")
        filters = _reattach_owner_filters(reattach_as)
        parked_statuses = ("errored", "paused")
        async with transaction(model._database):
            rows = await (
                model.filter(id=str(UUID(run_id)), status__in=list(parked_statuses), **filters)
                .select_for_update()
                .values("id", "status", "definition_id", "definition_version_id", "definition_hash", "metadata")
            )
            if not rows:
                if await model.filter(id=str(UUID(run_id)), **filters).values("id"):
                    raise RunResumeClaimLost("The saved workflow is no longer parked.")
                raise RunReattachRefused(
                    "This retry key belongs to a different caller or organization, or the workflow was retired."
                )
            run = rows[0]
            status = run["status"]
            run["metadata"] = _coerce_run_json(run["metadata"]) or {}
            await resolve_input_values(run)
            yield run
            if not await self.transition(
                run_id, from_statuses=(status,), to_status="running", reattach_as=reattach_as,
            ):
                raise RunResumeClaimLost("This workflow run changed before it could resume.")
        await _announce_waiting(run_id, "resumed", "running", None)

    async def resolve_output(self, run: dict[str, Any], *, missing: str = "raise") -> dict[str, Any]:
        """``run`` (a :meth:`load` row) with its ``output`` references resolved in place; returns ``run``."""
        if run.get("output"):
            from matrx_graph.checkpoint.value_store import resolve_run_output

            run["output"] = await resolve_run_output(str(run["id"]), run["output"], missing=missing)
        return run

    async def called_descendants(self, run_id: str) -> list[dict[str, Any]]:
        """Every live-row CALLED workflow (``subgraph.call`` child, marked by ``metadata.subgraph_parent``)
        under ``run_id``, down the ``parent_run_id`` chain, as ``{"id", "status"}`` rows. A fork or re-run
        also carries ``parent_run_id`` but is a run of its own and is never listed."""
        model = get_model("WfRun")
        frontier = [str(UUID(run_id))]
        seen: set[str] = set(frontier)
        found: list[dict[str, Any]] = []
        while frontier:
            rows = await model.filter(
                parent_run_id__in=frontier,
                deleted_at=None,
                metadata__json_has_key="subgraph_parent",
            ).values("id", "status")
            fresh = [r for r in rows if str(r["id"]) not in seen]
            if not fresh:
                break
            seen.update(str(r["id"]) for r in fresh)
            found.extend({"id": str(r["id"]), "status": str(r["status"])} for r in fresh)
            frontier = [str(r["id"]) for r in fresh]
        return found

    async def soft_delete(self, run_id: str) -> bool:
        """Canonically retire a terminal run and its unclaimed queue residue.

        A workflow definition can be soft-deleted while one of its historical
        runs remains visible to recovery/watchdog machinery.  Test fixtures and
        other explicitly disposable workflows must first reach a terminal state,
        then use this boundary so a stale queued job cannot outlive its owner.
        Live work is deliberately refused rather than being silently hidden.
        """
        result = await get_model("WfRun").update_where(
            {
                "id": str(UUID(run_id)),
                "deleted_at__isnull": True,
                "status__in": ["completed", "failed", "cancelled", "errored"],
            },
            returning=RUN_UPDATE_RETURNS,
            deleted_at=datetime.now(UTC),
        )
        if result.rows_affected:
            from matrx_graph.workers.queue import discard_for_run

            await discard_for_run(run_id)
        return result.rows_affected == 1

    async def claim_callback(self, run_id: str) -> str | None:
        """Atomically claim the run's terminal-completion callback.

        A run requests a callback by carrying ``metadata._settings
        .callback_url`` (set at create from the request body or the firing
        trigger). Every API replica hears the same terminal
        ``wf_run_announce`` NOTIFY, so delivery MUST be single-winner: this
        CAS writes ``metadata._callback.state='claimed'`` only when the run
        is terminal, has a callback_url, and no claim exists yet — exactly
        one caller gets the URL back; everyone else gets ``None``.
        """
        # Single-statement jsonb CAS: the WHERE guard (status terminal,
        # callback_url present, no existing claim) is fused with the write
        # in ONE update_where-shaped statement — typed JSON-path predicates
        # keep the guards fused with the update, so N replicas racing this
        # still get exactly one winner
        # (no read-then-write window reopens between guard and claim).
        # metadata->'_callback' IS NULL per the guard, so a top-level
        # JsonbMerge (== jsonb_set replace-at-key) is equivalent to the
        # original jsonb_set — there is nothing under '_callback' to lose.
        claimed_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
        from matrx_orm import ArrayAny, F, Is, JsonPath

        result = await (
            get_model("WfRun")
            .filter(
                ArrayAny(F("status"), list(TERMINAL_STATUSES), cast="text[]"),
                Is(JsonPath(F("metadata"), "_settings", "callback_url"), None, negated=True),
                Is(JsonPath(F("metadata"), "_callback", as_text=False), None),
                id=str(UUID(run_id)),
            )
            .returning("id", "metadata")
            .update(
                metadata=JsonbMerge(
                    "metadata", {"_callback": {"state": "claimed", "claimed_at": claimed_at}}
                )
            )
        )
        if result.rows_affected != 1:
            return None
        metadata = result.updated_rows[0].get("metadata")
        if isinstance(metadata, str):
            metadata = json.loads(metadata)
        if not isinstance(metadata, dict):
            return None
        url = (metadata.get("_settings") or {}).get("callback_url")
        return str(url) if url else None

    async def record_callback_result(
        self,
        run_id: str,
        *,
        state: str,
        attempts: int,
        status_code: int | None = None,
        detail: str | None = None,
    ) -> None:
        """Persist the callback delivery outcome under ``metadata._callback``.

        ``state`` is 'delivered' or 'failed'. Kept as a single-key JSONB
        merge so it never clobbers sibling metadata written mid-flight.
        """
        result = {
            "state": state,
            "attempts": attempts,
            "status_code": status_code,
            "detail": (detail or "")[:500] or None,
            "finished_at": datetime.now(UTC).isoformat(),
        }
        # Atomic single-key jsonb merge under '_callback' — matrx_orm's
        # patch_jsonb_path(..., merge=True) shallow-merges `result`'s keys
        # into whatever already lives at metadata._callback (preserving
        # claim_callback's earlier `claimed_at` instead of clobbering it, the
        # same way JsonbMerge does for a top-level key) so concurrent
        # metadata writers are never clobbered — a read-merge-write via a
        # plain ORM update would race.
        await get_instance("wf_run_manager").patch_jsonb_path(
            str(UUID(run_id)), "metadata", ["_callback"], result, merge=True
        )

    async def list_for_definition(
        self,
        definition_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        flagged: bool | None = None,
        sort_flagged_first: bool = False,
        omit: Sequence[str] = (),
    ) -> list[dict[str, Any]]:
        """One workflow's runs, newest first.

        ``omit`` names columns left out of the read (the row carries ``None``/``{}`` for
        them). A LIST reads only what it shows: pass ``LIST_HEAVY_COLUMNS`` (input, output,
        interrupt_payload, metadata - one workflow held 276 MB of output over 117 runs) and
        open a run by id for the rest.

        ``flagged=True`` keeps only runs that raised review flags
        (``review_flag_count > 0``); ``flagged=False`` only clean runs. The filter runs
        in the query, so an old flagged run is found past the page window.
        ``sort_flagged_first=True`` orders by flag count (most first), then newest.
        """
        filters: dict[str, Any] = {
            "definition_id": str(UUID(definition_id)),
            "deleted_at__isnull": True,
        }
        filters.update(_flagged_filter(flagged))
        ordered = (
            get_model("WfRun")
            .filter(**filters)
            .order_by(*_run_order(sort_flagged_first))
            .limit(limit)
            .offset(offset)
        )
        model_fields = getattr(get_model("WfRun"), "_fields", None)
        if omit and model_fields:
            rows = await ordered.values(*[f for f in model_fields if f not in omit])
        else:
            rows = await ordered.values()
        return [_row_to_run_dict(r) for r in rows]

    async def list_recent(
        self,
        *,
        user_id: str | None = None,
        organization_id: str | None = None,
        status: str | None = None,
        statuses: Sequence[str] | None = None,
        limit: int = 100,
        offset: int = 0,
        include_children: bool = False,
        include_ids: Sequence[str] | None = None,
        omit_output: bool = False,
        filter_organization_id: str | None = None,
        flagged: bool | None = None,
        sort_flagged_first: bool = False,
        parent_run_id: str | None = None,
        record_ids: Sequence[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Caller-scoped recent runs for the Studio Runs dashboard.

        ``record_ids`` lists only the runs ABOUT those records — ``metadata.record_id`` is one of
        them (stamped by the table-event fire, the store fire, the system / mandate start, and
        carried onto every subgraph child) — plus the direct children of a matching run that carry
        no record stamp of their own (runs started before children inherited it). Children are
        listed either way (it implies ``include_children``); the access scope still binds.

        ``parent_run_id`` lists only that run's durable children (it implies
        ``include_children``); an invalid id matches nothing, never every run.

        ``omit_output=True`` leaves the ``output`` column out of the read (the
        row carries ``output: None``). A LIST never renders a run's output, and
        it is the heavy column: 200 of one person's runs held 56 MB of it, so
        ``GET /runs`` hit the query timeout and the runs list never loaded
        (measured 2026-09-29). Open a run by id for its output.

        Filters build up based on which scoping args are supplied. The UI
        passes its authenticated user_id + the current project; admin views
        can pass org-level to see all runs in a tenant.

        ``include_children=False`` (default) hides durable subgraph child
        runs (``parent_run_id`` set) — a 50-item fan-out must not flood the
        top-level list; children are reached through their parent's canvas
        chips or by direct id.

        ``include_ids`` is the host's discoverable-id set (share grants
        resolved through its access kernel), ORed into the owner/org scope
        so shared runs appear in lists; the common filters (children/status/
        soft-delete), ordering, and limit/offset apply to both arms.
        ``None``/empty keeps the exact single-query owner fast path.

        ``flagged=True`` keeps only runs that raised review flags
        (``review_flag_count > 0``), ``False`` only clean runs; it binds every arm and
        runs in the query, so an old flagged run is found past the page window.
        ``sort_flagged_first=True`` orders by flag count (most first), then newest.
        """
        common: dict[str, Any] = {}
        common.update(_flagged_filter(flagged))
        scope: dict[str, Any] = {}
        wanted_records = [str(r).strip() for r in record_ids or () if str(r or "").strip()]
        if record_ids is not None and not wanted_records:
            return []  # asked for runs about no record: nothing, never every run
        if parent_run_id:
            coerced_parent = _to_uuid(parent_run_id)
            if coerced_parent is None:
                return []
            common["parent_run_id"] = coerced_parent
        elif not include_children and not wanted_records:
            common["parent_run_id__isnull"] = True
        for field, raw_value in (
            ("created_by", user_id),
            ("organization_id", organization_id),
        ):
            if raw_value:
                coerced = _to_uuid(raw_value)
                if coerced is None:
                    # Provided-but-invalid UUID matched nothing in the raw SQL
                    # (`col = NULL`); an ORM `IS NULL` filter would leak
                    # ownerless rows instead. Preserve "matches nothing".
                    return []
                scope[field] = coerced
        if statuses:
            # A SET of statuses (the "waiting on you" inbox asks for two at
            # once). Mutually exclusive with ``status`` by construction — a
            # caller that passes both gets the set, which is the superset.
            common["status__in"] = list(statuses)
        elif status:
            common["status"] = status
        common["deleted_at__isnull"] = True
        if filter_organization_id:
            # An on-page filter ON TOP of the access set: it binds every arm,
            # the discoverable-id arm included. Never the selected organization.
            coerced_filter = _to_uuid(filter_organization_id)
            if coerced_filter is None:
                return []
            common["organization_id"] = coerced_filter

        extra_ids = [u for u in (_to_uuid(v) for v in include_ids or ()) if u is not None]

        def scoped(*about: Any) -> Any:
            qb = get_model("WfRun")
            if extra_ids and scope:
                return qb.filter(*about, Q(**scope) | Q(id__in=extra_ids), **common)
            if extra_ids:
                return qb.filter(*about, id__in=extra_ids, **common)
            return qb.filter(*about, **scope, **common)

        if wanted_records:
            # ``metadata ->> 'record_id' = ANY(...)`` — the shape the partial expression index
            # ``run_record_id_idx`` (migration 0122) serves; ``metadata @> {...}`` scanned the whole table.
            about: Any = ArrayAny(JsonPath(F("metadata"), "record_id"), wanted_records)
            # The direct children of a matching run, for children written before they inherited the stamp.
            # An index lookup since 0122, so the second pass is cheap.
            parents = await scoped(about).limit(RECORD_PARENT_SCAN_MAX).values("id")
            parent_ids = [str(p["id"]) for p in parents if p.get("id")]
            if parent_ids:
                about = about | ArrayAny(F("parent_run_id"), parent_ids, cast="uuid[]")
            qb = scoped(about)
        else:
            qb = scoped()
        ordered = qb.order_by(*_run_order(sort_flagged_first)).limit(limit).offset(offset)
        model_fields = getattr(get_model("WfRun"), "_fields", None)
        if omit_output and model_fields:
            rows = await ordered.values(*[f for f in model_fields if f != "output"])
        else:
            rows = await ordered.values()
        return [_row_to_run_dict(r) for r in rows]

    async def apply_result(
        self,
        run_id: str,
        *,
        status: RunStatus,
        steps_executed: int,
        output: dict[str, Any] | None,
        interrupt: dict[str, Any] | None,
        error: str | None,
        last_checkpoint_id: str | None,
        failure: RunFailure | None = None,
        cancel_reason: str | None = None,
        stopped: dict[str, Any] | None = None,
        schedule_wake: bool = True,
        prior_output: dict[str, Any] | None = None,
        never_parked: bool = False,
    ) -> bool:
        """The terminal write; :meth:`apply_result_with_row` without the row."""
        return (await self.apply_result_with_row(
            run_id, status=status, steps_executed=steps_executed, output=output, interrupt=interrupt, error=error,
            last_checkpoint_id=last_checkpoint_id, failure=failure, cancel_reason=cancel_reason, stopped=stopped,
            schedule_wake=schedule_wake, prior_output=prior_output, never_parked=never_parked,
        )).applied  # fmt: skip

    async def apply_result_with_row(
        self,
        run_id: str,
        *,
        status: RunStatus,
        steps_executed: int,
        output: dict[str, Any] | None,
        interrupt: dict[str, Any] | None,
        error: str | None,
        last_checkpoint_id: str | None,
        failure: RunFailure | None = None,
        cancel_reason: str | None = None,
        stopped: dict[str, Any] | None = None,
        schedule_wake: bool = True,
        prior_output: dict[str, Any] | None = None,
        never_parked: bool = False,
    ) -> AppliedResult:
        """The terminal write, which never leaves a run "running" because the write itself failed. Hands back the
        row a terminal write left, so the caller never reads it again (L-SPEED round 6l).

        ``prior_output``: what the row's ``output`` already holds, when the caller KNOWS it (a leg that created the
        row and ran it to its end without a park passes ``{}``): a completion then sizes its output against it
        instead of reading the row first (one round trip fewer per called child, P8-RUNS 2026-11-15).

        ``schedule_wake=False``: a timer park records no wake job of its own — a called child whose
        caller relays the park (and its timer) to the outermost run, which holds the one wake.

        When the write raises (a statement timeout on a huge output, a dropped connection), the run
        is ended FAILED with a small error naming the write that failed and no output payload, then
        the original error is re-raised for the caller to log. 2026-10-05: run 70601b15 finished all
        its steps, its 11 MB final write timed out, every caller only logged it, and the run read
        "running" forever."""
        try:
            return await self._apply_result(
                run_id, status=status, steps_executed=steps_executed, output=output, interrupt=interrupt,
                error=error, last_checkpoint_id=last_checkpoint_id, failure=failure,
                cancel_reason=cancel_reason, stopped=stopped, schedule_wake=schedule_wake,
                prior_output=prior_output, never_parked=never_parked,
            )
        except Exception as exc:
            # A FAILED write that fails is no exception: the row still must not stay "running"
            # (2026-10-27 review: a failing child whose final write raised read "running" forever).
            # The small fallback names the cause the run meant to end with, so it is not lost.
            fallback: dict[str, Any] = {
                "cause": "final_write_failed",
                "message": "The run finished its steps, but saving its final result failed, so it is "
                           "marked failed instead of staying 'running'. Its steps' results are kept.",
                "technical": f"{type(exc).__name__}: {str(exc)[:500]} (intended status: "
                             f"{getattr(status, 'value', status)})",
            }
            intended_cause = getattr(failure, "cause", None)
            if intended_cause:
                fallback["intended_cause"] = str(getattr(intended_cause, "value", intended_cause))
            if await self._already_failed_with_a_cause(run_id):
                # The row already says why it failed (the write landed, then a later step of it
                # raised): never overwrite a real cause with final_write_failed.
                raise
            try:
                await self.mark_failed(run_id, error=fallback, steps_executed=steps_executed)
            except Exception:  # noqa: BLE001 — the reaper is the last backstop; the original error re-raises
                logger.exception("[wf:%s] fallback failed-status write also failed", run_id[:8])
            raise

    async def _already_failed_with_a_cause(self, run_id: str) -> bool:
        """True when the row is already ``failed`` with a recorded ``cause`` (a read error: False)."""
        try:
            rows = await get_model("WfRun").filter(id=str(UUID(run_id))).values("status", "error")
        except Exception:  # noqa: BLE001 — the fallback write still runs when the row cannot be read
            return False
        row = rows[0] if rows else {}
        error = row.get("error")
        return row.get("status") == "failed" and isinstance(error, dict) and bool(error.get("cause"))

    async def _apply_result(
        self,
        run_id: str,
        *,
        status: RunStatus,
        steps_executed: int,
        output: dict[str, Any] | None,
        interrupt: dict[str, Any] | None,
        error: str | None,
        last_checkpoint_id: str | None,
        failure: RunFailure | None = None,
        cancel_reason: str | None = None,
        stopped: dict[str, Any] | None = None,
        schedule_wake: bool = True,
        prior_output: dict[str, Any] | None = None,
        never_parked: bool = False,
    ) -> AppliedResult:
        """Convenience: translate a scheduler RunResult into one workflow.run update.

        Returns False when a TERMINAL write was rejected by the
        immutability guard (the run already ended in a different terminal
        state) — callers should log that loudly, never ignore it.

        On a successful terminal write (completed / failed / canceled /
        errored) any UNCLAIMED queued wf_job for this run is discarded:
        once a run is terminal a queued job can only re-drive dead work, and
        leaving it behind is what produced the 2026-06 zombie-job false alarm.
        A worker's own job is claimed, so it is never touched here — the worker
        deletes/dead-letters it through complete()/fail() itself.

        ``failure`` is the STRUCTURED failure (``RunResult.failure``), and it is
        what lands in the jsonb ``error`` column when present: ``cause`` +
        ``step_id``/``step_label``/``field``/``expected``/``got`` +
        ``technical``. It always carries ``message`` too, so every reader that
        predates the structure keeps working against a strictly richer payload.
        Callers that genuinely only hold a string (a sweeper, a host route)
        still pass ``error`` alone and get a derived cause rather than a raw
        exception line in a JSON coat.

        ``cancel_reason`` distinguishes the two cancel paths ON THE ROW —
        ``'graceful'`` (the scheduler observed the user's ``cancelling`` flag
        between super-steps) vs ``'immediate'`` (the asyncio task was killed
        underneath the run: deploy, shutdown, OOM). It lands in
        ``metadata._cancel`` because the event stream alone cannot be queried
        cheaply by the boot-time reconciliation sweep, and only
        ``'immediate'`` rows are ever eligible for automatic resume — an
        unmarked or graceful cancel is deliberate and stays terminal.
        """

        def error_payload() -> dict[str, Any]:
            """The jsonb ``error`` value — structured whenever we have it.

            The pre-change shape was ``{"message": "<raw python string>"}``:
            a string in a JSON coat, which forced the client to regex English
            back into meaning. When the engine hands us a ``RunFailure`` we
            write its fields; when a caller only has a string we still derive a
            ``cause`` from it here rather than persisting a bare line.
            """
            if failure is not None:
                return failure.to_column()
            text = (error or "").strip() or "unknown"
            # No ``message=`` override: the raw text is TECHNICAL and belongs
            # in the technical field, never as the headline. build_failure
            # generates the human sentence from the derived cause. Nothing is
            # lost — the full raw line is preserved verbatim under
            # ``technical``, which is the field surfaces are required to keep.
            return failure_from_text(text).to_column()

        terminal = status in (
            RunStatus.COMPLETED,
            RunStatus.FAILED,
            RunStatus.CANCELLED,
            RunStatus.ERRORED,
        )

        async def _discard_jobs() -> None:
            from matrx_graph.workers.queue import discard_for_run

            await discard_for_run(run_id)

        async def _discard_jobs_if_terminal(applied: bool) -> bool:
            if applied and terminal:
                await _discard_jobs()
            return applied

        # The unclaimed-job discard of a COMPLETED / FAILED / CANCELLED end runs alongside the settle hooks (only
        # when the write applied, as before): it touches no row they read (L-SPEED round 6l).
        if status is RunStatus.COMPLETED:
            applied, row = await self._mark_completed(
                run_id, output=output or {}, steps_executed=steps_executed, stopped=stopped, alongside=_discard_jobs,
                prior_output=prior_output, never_parked=never_parked,
            )
            return AppliedResult(applied, row)
        elif status is RunStatus.INTERRUPTED:
            await self.mark_interrupted(
                run_id,
                interrupt_payload=interrupt or {},
                last_checkpoint_id=last_checkpoint_id,
                steps_executed=steps_executed,
                output=output,
            )
            # Durable timers (flow.sleep / flow.wait_until): a park whose
            # interrupt carries the sleep marker gets its wake job HERE, in
            # the one funnel every lane runs — a wf_job 'resume' row with
            # visible_at = wake_at. Best-effort by contract: the helper
            # screams on failure and never raises (the park already stands
            # and the run remains manually resumable).
            from matrx_graph.workers.sleep_wake import schedule_sleep_wake

            if schedule_wake:
                await schedule_sleep_wake(run_id, interrupt, last_checkpoint_id=last_checkpoint_id)
            return AppliedResult(True)
        elif status is RunStatus.AWAITING_INPUT:
            await self.mark_awaiting_input(
                run_id,
                interrupt_payload=interrupt or {},
                steps_executed=steps_executed,
            )
            return AppliedResult(True)
        elif status is RunStatus.PAUSED:
            await self.mark_paused(
                run_id,
                last_checkpoint_id=last_checkpoint_id,
                steps_executed=steps_executed,
                output=output,
            )
            return AppliedResult(True)
        elif status is RunStatus.ERRORED:
            await self.mark_errored(
                run_id,
                error=error_payload(),
                last_checkpoint_id=last_checkpoint_id,
                steps_executed=steps_executed,
                output=output,
            )
            await _discard_jobs_if_terminal(True)
            return AppliedResult(True)
        elif status is RunStatus.FAILED:
            applied, row = await self._mark_failed(
                run_id, error=error_payload(), steps_executed=steps_executed, alongside=_discard_jobs,
                never_parked=never_parked,
            )
            return AppliedResult(applied, row)
        elif status is RunStatus.CANCELLED:
            applied, row = await self._mark_cancelled(
                run_id, steps_executed=steps_executed, cancel_reason=cancel_reason, alongside=_discard_jobs,
                never_parked=never_parked,
            )
            if applied and cancel_reason:
                # Ordered AFTER the terminal write on purpose: dying between
                # the two leaves an UNMARKED canceled row, which the
                # reconciliation sweep never resurrects — the safe direction.
                await self.merge_metadata(
                    run_id,
                    {
                        "_cancel": {
                            "reason": cancel_reason,
                            "at": datetime.now(UTC).isoformat(),
                        }
                    },
                )
            return AppliedResult(applied, row)
        else:
            raise ExecutionError(f"apply_result got unsupported status {status!r}")


async def input_values_settings_by_reference(
    run_id: str, metadata: dict[str, Any] | None, *, organization_id: str | None = None
) -> dict[str, Any] | None:
    """``metadata["_settings"]`` with every large ``input_values`` entry stored in the run's value store and
    referenced, or None when nothing is large (or no value store exists). The values are written before this
    returns. Same rule, knob and store as a ``node_started`` event's ``inputs`` (``outcome_input_row`` at the
    ``workflow.event_payload.inline_value_max_bytes`` knob), so a value the run's events already stored is the
    same row, never a second copy. Never raises: a failure keeps the values inline (logged)."""
    settings = (metadata or {}).get("_settings")
    values = settings.get("input_values") if isinstance(settings, dict) else None
    if not isinstance(values, dict) or not values:
        return None
    try:
        from matrx_graph.checkpoint.postgres import _value_store_available
        from matrx_graph.checkpoint.value_store import store_run_values
        from matrx_graph.checkpoint.values import outcome_input_row, run_pure_off_loop
        from matrx_graph.knobs import event_inline_value_max_bytes

        if not _value_store_available():
            return None
        row, stored = await run_pure_off_loop(outcome_input_row, values, await event_inline_value_max_bytes())
        if not stored:
            return None
        await store_run_values(run_id, stored, organization_id=organization_id)
    except Exception:  # noqa: BLE001 — inline is slower, never wrong
        logger.exception("[wf:%s] input values stay INLINE on the run row (value store write failed)", run_id[:8])
        return None
    logger.info("[wf:%s] input values: %d value(s) kept by reference", run_id[:8], len(stored))
    return {**settings, "input_values": row}


async def resolve_input_values(run: dict[str, Any]) -> dict[str, Any]:
    """``run`` (a loaded row) with ``metadata._settings.input_values`` references resolved in place.

    Never raises: a value that is gone leaves the references in place and logs an ERROR, so the run can still
    be opened, checked, cancelled, swept and deleted. A leg about to EXECUTE the run reads its inputs through
    :func:`execution_input_values`, which raises on exactly those left-over references."""
    settings = (run.get("metadata") or {}).get("_settings")
    values = settings.get("input_values") if isinstance(settings, dict) else None
    if not isinstance(values, dict):
        return run
    from matrx_graph.checkpoint.values import referenced_hashes

    if not referenced_hashes(values):
        return run
    from matrx_graph.checkpoint.value_store import _load_all
    from matrx_graph.checkpoint.values import MissingCheckpointValueError, resolve_values

    try:
        resolved = resolve_values(values, await _load_all(str(run["id"]), referenced_hashes(values)))
    except MissingCheckpointValueError:
        logger.error("[wf:%s] the run's stored input values are missing — references left in place",
                     str(run["id"])[:8], exc_info=True)
        return run
    run["metadata"] = {**run["metadata"], "_settings": {**settings, "input_values": resolved}}
    return run


def execution_input_values(run: dict[str, Any] | None) -> dict[str, Any]:
    """The input values a leg about to EXECUTE ``run`` (a :meth:`RunStore.load` row) starts with.

    Raises :class:`RunInputValueMissingError` when a stored value is gone (the load left its reference in
    place), so the run fails naming it — never starts with ``{"__matrx_checkpoint_value__": …}`` where its
    input should be. Every non-executing reader keeps working on the same row."""
    settings = ((run or {}).get("metadata") or {}).get("_settings")
    values = settings.get("input_values") if isinstance(settings, dict) else None
    if not isinstance(values, dict):
        return {}
    from matrx_graph.checkpoint.values import referenced_hashes

    gone = referenced_hashes(values)
    if gone:
        raise RunInputValueMissingError(
            str((run or {}).get("id")),
            f"{len(gone)} referenced value(s) not in the run's value store: "
            + ", ".join(sorted(h[:12] + "…" for h in gone)),
        )
    return dict(values)


async def _output_by_reference(run_id: str, output: dict[str, Any] | None) -> dict[str, Any] | None:
    """What a write of ``workflow.run.output`` stores: every step output over the run-output knob by reference
    (``value_store.output_by_reference``), sized against what the row ALREADY holds — the write merges into it,
    so earlier legs (pause / interrupt / resume) count too. 2026-10-27: run 61b8404f finished all 59 steps and
    ended ``final_write_failed`` on a 21.7 MB row (one step 11 MB)."""
    if not output:
        return output
    from matrx_graph.checkpoint.value_store import output_by_reference, run_output_limit

    if await run_output_limit() <= 0:
        return output
    rows = await get_model("WfRun").filter(id=str(UUID(run_id))).values("output")
    existing = rows[0].get("output") if rows else None
    if isinstance(existing, str):
        try:
            existing = json.loads(existing)
        except json.JSONDecodeError:
            existing = None
    return await output_by_reference(run_id, output, existing=existing if isinstance(existing, dict) else None)


async def _output_by_reference_known(
    run_id: str, output: dict[str, Any] | None, prior_output: dict[str, Any]
) -> dict[str, Any] | None:
    """``_output_by_reference`` when the caller KNOWS what the row holds (``prior_output``: a leg that created the
    row and ran it to its end passes ``{}``) — the same sizing, without reading the row first (P8-RUNS)."""
    if not output:
        return output
    from matrx_graph.checkpoint.value_store import output_by_reference, run_output_limit

    if await run_output_limit() <= 0:
        return output
    return await output_by_reference(run_id, output, existing=prior_output or None)


#: How many runs about a record are scanned for their unstamped direct children (``list_recent(record_ids=)``).
RECORD_PARENT_SCAN_MAX = 500  # protocol-constant: bound on an ancestry walk guarding against cycles, a technical invariant


def _to_uuid(value: str | None) -> str | None:
    """Coerce a string to a normalized UUID string, or None. See
    definition_store._to_uuid."""
    if not value:
        return None
    try:
        return str(UUID(str(value)))
    except (ValueError, AttributeError, TypeError):
        return None


def _require_optional_uuid(value: str | UUID | None, field_name: str) -> str | None:
    if value is None or value == "":
        return None
    try:
        return str(UUID(str(value)))
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValueError(f"RunStore.create: {field_name} must be a valid UUID") from exc


def _coerce_run_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _row_to_run_dict(row: Any) -> dict[str, Any]:
    return {
        "id": str(row["id"]),
        "thread_id": str(row["thread_id"]),
        "parent_run_id": str(row["parent_run_id"]) if row["parent_run_id"] else None,
        "definition_id": str(row["definition_id"]),
        "definition_version_id": str(row["definition_version_id"])
        if row["definition_version_id"]
        else None,
        "definition_hash": row["definition_hash"],
        "status": row["status"],
        "input": _coerce_run_json(row.get("input")),
        "output": _coerce_run_json(row.get("output")),
        "error": _coerce_run_json(row["error"]),
        "interrupt_payload": _coerce_run_json(row.get("interrupt_payload")),
        "steps_executed": row["steps_executed"],
        "last_checkpoint_id": str(row["last_checkpoint_id"]) if row["last_checkpoint_id"] else None,
        "created_by": str(row["created_by"]) if row["created_by"] else None,
        "organization_id": str(row["organization_id"]) if row["organization_id"] else None,
        "deleted_at": row.get("deleted_at"),
        "project_id": str(row["project_id"]) if row["project_id"] else None,
        "task_id": str(row["task_id"]) if row["task_id"] else None,
        "conversation_id": str(row["conversation_id"]) if row["conversation_id"] else None,
        "request_attribution_complete": bool(row.get("request_attribution_complete", False)),
        "agent_id": str(row["agent_id"]) if row["agent_id"] else None,
        "agent_version_id": str(row["agent_version_id"]) if row["agent_version_id"] else None,
        "metadata": _coerce_run_json(row.get("metadata")) or {},
        # Review flags the run raised (workflow.run.review_flag_count) — the runs lists show and
        # filter on it. A store whose table has no such column reports 0.
        "review_flag_count": int(row.get("review_flag_count") or 0),
        "created_at": row["created_at"],
        "started_at": row["started_at"],
        "completed_at": row["completed_at"],
    }
