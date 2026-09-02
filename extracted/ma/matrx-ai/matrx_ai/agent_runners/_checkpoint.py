"""RunCheckpointer — the resumable-run primitive for agent_runners.

A multi-stage agent pipeline (podcast, research, ...) that spends real money
must never throw away completed work when it fails late. This primitive gives
any runner durable, memoized, resumable stages backed by the
``agent_run`` / ``agent_run_stage`` tables (the ``arm`` bundle).

The contract is one method::

    ckpt = await RunCheckpointer.start(kind="podcast", user_id=uid, request=req_dict)
    # ... or, to resume a failed run, replaying only the MISSING stages:
    ckpt = await RunCheckpointer.resume(run_id=rid, user_id=uid)

    payload = await ckpt.stage("create_script", lambda: _do_script())  # dict in/out
    await ckpt.finish(result_dict)        # or ckpt.fail(exc) on the way out

``stage(key, fn)`` semantics
----------------------------
* If a ``completed`` checkpoint already exists for ``key`` → return the stored
  output dict and DO NO WORK (the resume money-saver — paid media already
  rendered are never re-paid).
* Otherwise run ``fn()``, commit the result as a checkpoint row, and return it.
  A payload with ``success=False`` is committed as ``status='failed'`` so it is
  re-run on the next resume (a failed paid asset has no URL — we must retry).

Durability vs. robustness
-------------------------
Checkpoint writes are SYNCHRONOUS per stage (a podcast gen is minutes long — we
want each stage durably landed before the next starts; a crash then loses at
most the one in-flight stage). But checkpointing is an *optimization for
resume*, not the canonical artifact persistence (the episode row is written by
the host router). So:

* If the run row can't even be created (registry not configured, DB down) we
  fall back to a :class:`NullCheckpointer` — the pipeline runs EXACTLY as before
  (no resume, but no regression). This is also what keeps the package runnable
  standalone in tests with no DB.
* A per-stage commit failure is logged LOUDLY and never aborts generation — that
  one stage just won't be resumable; the generation itself still completes.

Both fallbacks log loudly (never silently) so a broken checkpoint sink is
visible rather than mysterious.

Universal failure capture
-------------------------
A complex multi-stage pipeline has many parts that can fail *softly* — a
single image agent errors, the pipeline keeps going, and the run still
"succeeds" with a missing asset. Those soft failures used to be invisible
(streamed to the client, then gone). Now EVERY stage failure that flows
through ``stage()`` — whether the stage returns ``success=False`` OR raises —
is also captured into the platform's central, human-reviewable error queue
(``system_error`` via ``matrx_connect``'s injected ``capture_error`` seam),
tagged ``kind='agent_run_stage_failed'`` and keyed to the run id + stage key.
So "find and resolve every single error" becomes one query, regardless of how
many parts of how many runs failed. Capture is best-effort and never-raising:
it can never break the generation it is observing, and is a silent no-op when
no host capture sink is configured (standalone / tests).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from matrx_utils import vcprint

#: USD precision for every cost written to the run/stage ledger.
_USD = Decimal("0.000001")

#: Reserved key stamped on a payload RETURNED FROM A CHECKPOINT (a replay) and on
#: no other payload. It is the only way a caller can tell "this stage just ran and
#: I owe its cost" from "a previous attempt ran and paid for this" — and telling
#: those apart is what decides whether the run's spend gets settled at all.
#:
#: Added to the returned COPY only; the committed payload never carries it.
REPLAYED_KEY = "__matrx_replayed"

# A stage function returns a JSON-serializable dict payload. Convention: the
# dict carries a ``success`` bool (defaults True if absent); everything else is
# runner-defined (e.g. {"output": "<url>"} or {"stage_result": {...}, "data": {...}}).
StagePayload = dict[str, Any]
StageFn = Callable[[], Awaitable[StagePayload]]


def fingerprint_request(kind: str, user_id: str | None, request: dict[str, Any]) -> str:
    """Stable hash of a normalized request — for idempotent-resume bookkeeping."""
    blob = json.dumps(
        {"kind": kind, "user_id": user_id or "", "request": request},
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class DurableRunUnavailable(RuntimeError):
    """The durable run record could not be created and the caller requires one.

    Raised by ``RunCheckpointer.start(require_durable=True)`` BEFORE any paid
    work begins, so an expensive multi-minute pipeline never starts in a state
    where its output cannot be saved, listed, or resumed.

    Carries ``error_info`` so the streaming error handler emits a NAMED
    ``fatal_error`` the UI can explain, instead of the generic
    "failed unexpectedly. Please try again or adjust your settings." — which is
    actively misleading here: retrying and changing settings both do nothing.
    """

    def __init__(self, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(message)
        from matrx_ai.providers.errors import RetryableError

        self.error_info = RetryableError(
            error_type="durable_run_unavailable",
            message=message,
            is_retryable=False,
            user_message=(
                "We couldn't start this run because our database isn't accepting "
                "writes right now — so the run could not have been saved or "
                "recovered later. Nothing was started and nothing was charged. "
                "This is on our side; please try again shortly."
            ),
            details={"cause": type(cause).__name__ if cause is not None else None},
        )


class NullCheckpointer:
    """No-op checkpointer — runs every stage, persists nothing.

    Used as the fallback when DB-backed checkpointing is unavailable (standalone
    package use, registry not configured, run-row creation failed). The pipeline
    behaves exactly as it did before checkpointing existed.
    """

    run_id: str = ""
    is_durable: bool = False
    kind: str = ""
    user_id: str | None = None

    async def stage(self, stage_key: str, fn: StageFn) -> StagePayload:
        # No durable run, but still funnel soft/hard failures into the central
        # error queue so a DB-down (NullCheckpointer) run isn't a blind spot.
        try:
            payload = await fn()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            await _capture_stage_failure("", self.kind, self.user_id, stage_key, exc=exc)
            raise
        if not bool(payload.get("success", True)):
            await _capture_stage_failure(
                "", self.kind, self.user_id, stage_key, error=payload.get("error")
            )
        return payload

    async def finish(self, result: dict[str, Any], *, total_cost: float | None = None) -> None:
        return None

    async def fail(
        self, error: dict[str, Any] | str, *, total_cost: float | None = None
    ) -> None:
        return None

    async def touch(self) -> None:
        return None


class RunCheckpointer:
    """DB-backed resumable run over the ``agent_run`` / ``agent_run_stage`` tables."""

    is_durable: bool = True

    def __init__(
        self,
        run_id: str,
        completed: dict[str, StagePayload],
        *,
        kind: str = "",
        user_id: str | None = None,
    ) -> None:
        self.run_id = run_id
        self.kind = kind
        self.user_id = user_id
        # stage_key -> stored output payload, for stages already completed.
        self._completed: dict[str, StagePayload] = completed
        # Host-spine settle for this run pass (see _open_spine_tracking). None when
        # the host injected no tracker (standalone) or the open declined/failed.
        self._spine_settle: Any = None

    async def _open_spine_tracking(self) -> None:
        """Record this run pass on the host's runtime spine (the injected
        ``agent_run_tracker`` seam — one `global_execution` per pass, per-stage AI
        calls nesting under it). Best-effort and never-raising: unconfigured hosts
        and tracker failures leave the run exactly as it was."""
        try:
            from matrx_ai._ext import get_agent_run_tracker

            tracker = get_agent_run_tracker()
            if tracker is None:
                return
            self._spine_settle = await tracker(
                run_id=self.run_id, kind=self.kind, user_id=self.user_id
            )
        except Exception as exc:  # noqa: BLE001 — tracking must never break a run
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: spine tracking open failed "
                f"(run unaffected): {exc}",
                color="yellow",
            )
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, "_open_spine_tracking", exc
            )

    async def _settle_spine(self, status: str, error: str | None = None) -> None:
        """Settle the spine execution for this pass. Best-effort, never-raising;
        an unsettled pass is swept by the host's lease + reaper backstop."""
        settle, self._spine_settle = self._spine_settle, None
        if settle is None:
            return
        try:
            await settle(status, error)
        except Exception as exc:  # noqa: BLE001 — the reaper is the backstop
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: spine settle failed "
                f"({status}) — reaper will sweep: {exc}",
                color="yellow",
            )
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, "_settle_spine", exc,
                context={"status": status, "error": error},
            )

    # -- construction ------------------------------------------------------

    @classmethod
    async def start(
        cls,
        *,
        kind: str,
        user_id: str | None,
        request: dict[str, Any],
        fingerprint: str | None = None,
        require_durable: bool = False,
    ) -> RunCheckpointer | NullCheckpointer:
        """Begin a fresh run.

        ``require_durable=True`` makes an un-creatable run row FATAL — the caller
        gets :class:`DurableRunUnavailable` and never starts. Pass it from any
        pipeline whose value depends on being findable and resumable later.
        Otherwise this falls back to :class:`NullCheckpointer` and generation
        runs un-resumable but without regression (standalone use, tests).
        """
        try:
            arm = _arm()
            run = await arm.runs.create_item(
                kind=kind,
                created_by=user_id or None,
                status="processing",
                request=request,
                input_fingerprint=fingerprint or fingerprint_request(kind, user_id, request),
            )
            run_id = str(run.id)
            vcprint(f"[RunCheckpointer] started run {run_id} (kind={kind})", color="cyan")
            ckpt = cls(run_id=run_id, completed={}, kind=kind, user_id=user_id)
            await ckpt._open_spine_tracking()
            return ckpt
        except Exception as exc:
            # A silent degrade here is what made runs UNFINDABLE for four days in
            # 2026-08: with no run row the pipeline emitted run_id="", the client
            # stored no backend_run_id, the runs list (which reads agent_run) was
            # empty, and there was no checkpoint to resume from — while the run
            # itself burned minutes of paid provider calls. Loud, always.
            vcprint(
                f"[RunCheckpointer] COULD NOT START A DURABLE RUN (kind={kind}): {exc!r}\n"
                f"  Without it this run cannot be listed, reopened, or resumed, and\n"
                f"  every stage checkpoint is lost. This is a DB/infrastructure fault.",
                color="red",
            )
            await _capture_stage_failure("", kind, user_id, "_start_durable_run", exc=exc)
            if require_durable:
                raise DurableRunUnavailable(
                    f"Cannot start a {kind} run: the durable run record could not be "
                    f"created, so the run could not be saved, resumed, or found again. "
                    f"Nothing was charged. Underlying error: {exc}",
                    cause=exc,
                ) from exc
            return NullCheckpointer()

    @classmethod
    async def resume(
        cls,
        *,
        run_id: str,
        user_id: str | None,
    ) -> RunCheckpointer:
        """Resume an existing run, preloading its completed-stage outputs so
        ``stage()`` skips them. Raises if the run doesn't exist or isn't owned by
        ``user_id`` (None bypasses the ownership check for system callers)."""
        arm = _arm()
        run = await arm.runs.load_by_id(run_id)
        if run is None:
            raise ValueError(f"agent_run {run_id} not found")
        if user_id is not None and str(getattr(run, "created_by", "") or "") not in (
            "",
            str(user_id),
        ):
            raise PermissionError(f"agent_run {run_id} is not owned by {user_id}")

        stages = await arm.stages.filter_items(run_id=run_id)
        completed = {
            s.stage_key: (s.output or {})
            for s in stages
            if str(getattr(s, "status", "")) == "completed"
        }
        # Re-open the run for another pass; clear the prior error.
        await arm.runs.update_item(run_id, status="processing", error=None)
        vcprint(
            f"[RunCheckpointer] resumed run {run_id} — {len(completed)} stage(s) "
            f"already completed, replaying the rest",
            color="cyan",
        )
        ckpt = cls(
            run_id=run_id,
            completed=completed,
            kind=str(getattr(run, "kind", "") or ""),
            user_id=(str(run.user_id) if getattr(run, "user_id", None) else None),
        )
        # A resume pass is its OWN spine execution (the failed pass's execution is
        # already terminal — terminal-once CAS); find_by_link shows every pass.
        await ckpt._open_spine_tracking()
        return ckpt

    @classmethod
    async def load_request(cls, run_id: str) -> dict[str, Any] | None:
        """The original request dict stored on the run row (for a router that
        resumes from a run_id alone)."""
        arm = _arm()
        run = await arm.runs.load_by_id(run_id)
        if run is None:
            return None
        return dict(getattr(run, "request", {}) or {})

    # -- the one method runners call --------------------------------------

    async def stage(self, stage_key: str, fn: StageFn) -> StagePayload:
        cached = self._completed.get(stage_key)
        if cached is not None:
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: stage '{stage_key}' "
                f"already complete — reusing checkpoint (no work)",
                color="green",
            )
            # Marked as a REPLAY so the caller settles only what this attempt
            # actually paid for. A copy — the stored payload stays untouched.
            return {**cached, REPLAYED_KEY: True}

        try:
            payload = await fn()
        except asyncio.CancelledError:
            # A cancel is not a captured failure here — the request-level cancel
            # path owns that. Mark the stage failed (resumable) and propagate.
            await self._commit_stage(
                stage_key, {"success": False, "error": {"message": "cancelled"}}, False
            )
            raise
        except Exception as exc:
            # Hard failure (a stage raised). Capture to the central queue AND
            # commit a failed checkpoint so it re-runs on resume, then re-raise.
            await _capture_stage_failure(self.run_id, self.kind, self.user_id, stage_key, exc=exc)
            await self._commit_stage(
                stage_key,
                {"success": False, "error": {"message": f"{type(exc).__name__}: {exc}"}},
                False,
            )
            raise

        success = bool(payload.get("success", True))
        await self._commit_stage(stage_key, payload, success)
        if success:
            self._completed[stage_key] = payload
        else:
            # Soft failure (the "random parts keep failing" case): the stage
            # returned success=False and the pipeline carries on. Still capture
            # it centrally so no failure is ever invisible.
            await _capture_stage_failure(
                self.run_id, self.kind, self.user_id, stage_key, error=payload.get("error")
            )
        return payload

    # -- terminal transitions ---------------------------------------------

    async def finish(self, result: dict[str, Any], *, total_cost: float | None = None) -> None:
        persisted = True
        try:
            arm = _arm()
            await arm.runs.update_item(
                self.run_id,
                status="completed",
                result=result,
                **(await self._cost_update(total_cost)),
            )
        except Exception as exc:
            persisted = False
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: failed to mark completed: {exc}",
                color="red",
            )
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, "_finish_run", exc
            )
        if persisted:
            await self._settle_spine("completed")
        else:
            await self._settle_spine("failed", "agent_run terminal persistence failed")

    async def fail(
        self, error: dict[str, Any] | str, *, total_cost: float | None = None
    ) -> None:
        err = error if isinstance(error, dict) else {"message": str(error)}
        try:
            arm = _arm()
            await arm.runs.update_item(
                self.run_id,
                status="failed",
                error=err,
                **(await self._cost_update(total_cost)),
            )
        except Exception as exc:
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: failed to mark failed: {exc}",
                color="red",
            )
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, "_fail_run", exc
            )
        await self._settle_spine("failed", str(err.get("message") or err))

    async def _cost_update(self, total_cost: float | None) -> dict[str, Any]:
        """The `total_cost` field of a terminal update — the pass's settle-safe
        spend ADDED to whatever the row already carries.

        Additive, not absolute: a resumed pass settles only the stages IT paid
        for (the caller passes the unsettled delta), so the row accumulates the
        run's true lifetime cost across every pass instead of the last pass
        overwriting the first. Folded into the terminal write itself so status
        and cost can never half-land.

        A run that spent real money and reports $0.00 is a BILLING defect, not a
        display bug — so a caller that can compute its spend must always pass it,
        and a failure to read the current total is loud, never silent.
        """
        if not total_cost:
            return {}
        current = Decimal("0")
        try:
            run = await _arm().runs.load_by_id(self.run_id)
            current = Decimal(str(getattr(run, "total_cost", 0) or 0))
        except Exception as exc:  # noqa: BLE001 — settle the delta rather than lose the spend
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: could not read the current "
                f"total_cost — settling this pass's ${total_cost} on its own, so an "
                f"earlier pass's spend may be under-reported: {exc}",
                color="red",
            )
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, "_read_total_cost", exc,
                context={"unsettled_cost": total_cost},
            )
        # Quantized to the platform's USD precision — the delta arrives as a
        # float, and summing raw floats onto a money column persists artifacts.
        return {"total_cost": (current + Decimal(str(total_cost))).quantize(_USD)}

    # -- internals --------------------------------------------------------

    async def _commit_stage(self, stage_key: str, payload: StagePayload, success: bool) -> None:
        """Upsert a checkpoint row. Best-effort: a failure here is logged loudly
        and never aborts generation — that one stage just won't be resumable."""
        status = "completed" if success else "failed"
        now = datetime.now(UTC)
        error = None if success else (payload.get("error") or {"message": "stage failed"})
        if error is not None and not isinstance(error, dict):
            error = {"message": str(error)}
        # The stage's own spend, lifted out of the payload's usage block onto the
        # dedicated column. The payload already carried it, but only as JSON — so
        # "what did stage X cost" was unqueryable and the run-level total had no
        # per-stage evidence to be reconciled against.
        cost = _payload_cost(payload)
        arm = _arm()
        try:
            existing = await arm.stages.filter_items(run_id=self.run_id, stage_key=stage_key)
            if existing:
                await arm.stages.update_item(
                    existing[0].id,
                    status=status,
                    output=payload,
                    error=error,
                    cost=cost,
                    finished_at=now,
                )
            else:
                await arm.stages.create_item(
                    run_id=self.run_id,
                    stage_key=stage_key,
                    status=status,
                    output=payload,
                    error=error,
                    cost=cost,
                    finished_at=now,
                )
        except Exception as exc:
            vcprint(
                f"[RunCheckpointer] run {self.run_id}: could not checkpoint stage "
                f"'{stage_key}' (status={status}) — it won't be resumable: {exc}",
                color="red",
            )
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, stage_key, exc,
                context={"status": status, "cost": str(cost)},
            )

        # Per-stage spine note: if the host's tracker settle carries a `.note`
        # channel (duck-typed — older/standalone hosts simply don't), record the
        # stage transition as a durable execution event so a reconnecting client
        # following the host's canonical event stream sees real stage progress,
        # not just created/started/terminal. Best-effort, never blocks a run.
        note = getattr(self._spine_settle, "note", None)
        if note is not None:
            try:
                await note("stage", {"stage_key": stage_key, "status": status})
            except Exception:  # noqa: BLE001 — progress detail, never a run failure
                pass

        # Liveness heartbeat: bump the run's DB-visible clock on every stage
        # commit so the studio manage view can distinguish "alive" from
        # "stalled" without holding the stream open (the in-memory TICK never
        # reaches the DB). Best-effort — never blocks or fails generation.
        await self.touch()

    async def touch(self) -> None:
        """Bump ``last_heartbeat_at`` on the run row — the DB-visible pulse.

        Stage commits call this, but they are NOT enough on their own: a single
        video/audio render runs for many minutes with zero commits, and every
        client that isn't holding the live stream (page reload, phone unlock,
        the manage list, background polls) judges liveness from this column
        with a ~3-minute threshold. The pipeline's ticker therefore also calls
        this periodically during long stages — otherwise a perfectly healthy
        run reads as "stalled"/"interrupted" (the 2026-08-10 fake-interruption
        banner). Best-effort — never blocks or fails generation.
        """
        try:
            await _arm().runs.update_item(
                self.run_id, last_heartbeat_at=datetime.now(UTC)
            )
        except Exception as exc:
            await _capture_checkpoint_write_failure(
                self.run_id, self.kind, self.user_id, "_heartbeat", exc
            )


def _payload_cost(payload: StagePayload) -> Decimal | None:
    """What ONE stage cost, read from its checkpoint payload — the single
    definition of that, shared by the live commit path, the reconciliation
    sweep, and the backfill so all three can never disagree.

    ``None`` (never a faked zero) when the stage tracked no usage at all.
    """
    return stage_cost(payload)


def stage_cost(payload: dict[str, Any] | None) -> Decimal | None:
    """Public twin of :func:`_payload_cost` — the cost recorded on a stage
    checkpoint payload (``usage.cost_usd``), or ``None`` when it tracked none."""
    usage = (payload or {}).get("usage")
    if not isinstance(usage, dict):
        return None
    raw = usage.get("cost_usd")
    if raw is None:
        return None
    try:
        return Decimal(str(raw))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _arm() -> Any:
    """Lazy import so this module is import-safe before the host has configured
    the matrx-ai DB registry (validation / standalone import paths)."""
    from matrx_ai.db.arm_managers import arm

    return arm


class _StageFailure(Exception):
    """Synthetic carrier for a soft (``success=False``) stage failure, so the
    central capture sink gets a real exception object + a clean one-line text
    even when the stage didn't raise."""


async def _capture_checkpoint_write_failure(
    run_id: str,
    kind: str,
    user_id: str | None,
    operation: str,
    exc: BaseException,
    *,
    context: dict[str, Any] | None = None,
) -> None:
    """Capture a checkpoint-ledger persistence failure without masking the run."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        exc,
        kind="agent_run_persistence_failed",
        user_id=user_id,
        route=f"agent_run/{kind or 'unknown'}",
        error_type=type(exc).__name__,
        error_text=f"{operation}: {exc}",
        payload={"run_id": run_id, "run_kind": kind, "operation": operation},
        context=context or {},
    )


async def _capture_stage_failure(
    run_id: str,
    kind: str,
    user_id: str | None,
    stage_key: str,
    *,
    exc: BaseException | None = None,
    error: Any = None,
) -> None:
    """Route ONE stage failure into the platform's central error queue
    (``system_error`` via the injected ``capture_error`` seam).

    Best-effort and never-raising by contract — a capture failure can never
    break the generation it observes, and is a silent no-op when the host has
    configured no capture sink (standalone matrx-ai, tests). This is the single
    funnel that makes "every stage failure of every run is findable" true.
    """
    # Build a clean one-line description from whatever we were handed.
    if error is None and exc is not None:
        detail = f"{type(exc).__name__}: {exc}"
    elif isinstance(error, dict):
        detail = str(error.get("message") or error.get("error") or error)
    else:
        detail = str(error) if error is not None else "stage failed"

    captured = exc if exc is not None else _StageFailure(detail)

    try:
        from matrx_connect.streaming.error_capture import capture_error

        # Enrich with the live request context when we're inside one.
        request_id: str | None = None
        conversation_id: str | None = None
        ctx_user_id: str | None = None
        try:
            from matrx_connect import try_get_app_context

            ctx = try_get_app_context()
            if ctx is not None:
                request_id = getattr(ctx, "request_id", None)
                conversation_id = getattr(ctx, "conversation_id", None)
                ctx_user_id = getattr(ctx, "user_id", None)
        except Exception:
            pass

        await capture_error(
            captured,
            kind="agent_run_stage_failed",
            request_id=request_id,
            user_id=user_id or ctx_user_id,
            conversation_id=conversation_id,
            route=f"agent_run/{kind or 'unknown'}",
            error_type=(type(exc).__name__ if exc is not None else "stage_failed"),
            error_text=f"[{kind or 'run'}:{stage_key}] {detail}",
            payload={"run_id": run_id, "run_kind": kind, "stage_key": stage_key},
            context={
                "run_id": run_id,
                "run_kind": kind,
                "stage_key": stage_key,
                "stage_error": error,
                "resume_hint": (
                    f"POST /api/podcast/resume/{run_id}" if kind == "podcast" and run_id else None
                ),
            },
        )
    except Exception as cap_exc:  # capture must never escalate
        vcprint(
            f"[RunCheckpointer] run {run_id}: failed to capture stage "
            f"'{stage_key}' error to system_error: {cap_exc}",
            color="red",
        )


__all__ = [
    "DurableRunUnavailable",
    "RunCheckpointer",
    "NullCheckpointer",
    "StagePayload",
    "StageFn",
    "fingerprint_request",
    "stage_cost",
    "REPLAYED_KEY",
]
