"""The held stream: a saved run WAITS, in its open stream, for a client-run tool's result.

Contract: common-docs ``systems/architecture/execution-runtime/RESUME-AND-RECOVERY.md`` section 1a.

``ToolExecutor._execute_delegated`` parks the call durably and emits ``tool_delegated`` exactly as before.
When the client said it keeps reading (``client.reads`` names :data:`HOLD_READ`) and the host bound hold
hooks, the dispatch then waits here instead of ending the turn. The ``chat.tool_call`` row is the only
truth: a wake (same process, or the host's NOTIFY from another server task) only shortens the poll.

Who continues the turn is decided by ONE row update, never by a read:

* the waiting turn keeps a short lease on the row (``held_until``), renewed while it waits;
* the result POST first tries its compare-and-set WITH ``held_until > now()``: one row means this turn
  continues; otherwise it runs the plain compare-and-set, which clears ``held_until``, and the client
  resumes as before;
* this turn gives up with ``held_until = NULL WHERE status = 'delegated' AND held_until IS NOT NULL``:
  one row means it parks; zero rows means a result landed, and it continues only when that row still
  carries ``held_until``.

A package with no hooks bound (matrx-local, a bare install) never holds.

A call parked on a PERSON (an ask, a spend approval, an apply-gate card: ``metadata.parked_on``) is held the
same way when its client also names :data:`PERSON_HOLD_READ` (section 1b): the wait then runs in
``ToolExecutor.execute`` after the dispatch, under the ``person`` reason and its own knob.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from matrx_utils import vcprint

#: What a client names in ``client.reads`` to say it keeps reading its stream after ``tool_delegated``.
HOLD_READ = "delegated-hold-v1"
#: The separate opt-in for a call parked on a PERSON (section 1b rule P2): ``HOLD_READ`` alone never holds a
#: question; a client that keeps its stream open while a person answers names this too.
PERSON_HOLD_READ = "delegated-hold-person-v1"
#: Why a call is held: a client-run tool (the client's app runs it) or a person answering a parked ask.
HoldReason = Literal["client_tool", "person"]
#: ``superseded``: the row is still parked but its lease was taken away (a new message in the conversation,
#: section 1b rule P10); the holder parks without a release write.
ReleaseReason = Literal[
    "timeout", "stopped", "shutdown", "control", "answered_elsewhere", "database", "superseded"
]


@dataclass(frozen=True)
class HoldHooks:
    """What the host binds (``configure_delegated_hold``). Every callable is cheap and never raises."""

    hold_ms: Callable[[HoldReason], int]
    """How long one call held for this reason may wait in the stream (that reason's knob); 0 turns it off."""
    poll_ms: Callable[[], int]
    """The fast poll interval (the knob)."""
    may_hold: Callable[[], bool]
    """False while this process is draining for a deploy: no hold starts, open holds give up."""
    lease_ms: Callable[[], int]
    """The lease a waiting turn keeps on its call (the knob), renewed three times per lease. A holder that
    dies stops renewing, so a result POST stops being told "the open stream continues" within one lease."""
    slow_poll_ms: Callable[[], int]
    """The poll interval once the fast window has passed (the knob): by then a person is deciding."""
    fast_window_ms: Callable[[], int]
    """How long the fast poll runs (the knob): it covers the tools that answer in seconds."""
    max_hold_ms: Callable[[HoldReason], int]
    """The most one call held for this reason may ever wait. ``client_tool``: the host derives it from the
    dispatch backstop (a dispatch timeout would overwrite the parked row with an error). ``person``: the wait
    runs outside the dispatch, so its ceiling is the person knob's own range."""


@dataclass(frozen=True)
class HoldOutcome:
    taken: bool
    """True: the result landed while this turn held the call, and this turn continues with ``row``."""
    row: Any = None
    reason: ReleaseReason | None = None
    waited_ms: int = 0


_hooks: HoldHooks | None = None
_wakes: dict[tuple[str, str], asyncio.Event] = {}  # (conversation_id, call_id) -> the waiting turn's event


def configure_delegated_hold(hooks: HoldHooks | None) -> None:
    """Bind the host's hooks; ``None`` unbinds (no run holds)."""
    global _hooks
    _hooks = hooks


def hooks() -> HoldHooks | None:
    return _hooks


@dataclass(frozen=True)
class HoldSettings:
    """One call's wait, read ONCE before the call is claimed: a limit that cannot be read means no hold,
    decided before anything is promised, never an error in the middle of a wait."""

    seconds: float
    poll_seconds: float
    slow_poll_seconds: float
    fast_window_seconds: float
    lease_seconds: float


def settings(*, reason: HoldReason = "client_tool", cap_seconds: float | None = None) -> HoldSettings | None:
    """The wait a call held for ``reason`` gets now; ``None`` when unbound, switched off, draining, or any
    limit is unreadable."""
    if _hooks is None:
        return None
    try:
        if not _hooks.may_hold():
            return None
        seconds = min(_ms(lambda: _hooks.hold_ms(reason)), _ms(lambda: _hooks.max_hold_ms(reason))) / 1000.0
        if cap_seconds:
            seconds = min(seconds, float(cap_seconds))
        found = HoldSettings(
            seconds=seconds,
            poll_seconds=_ms(_hooks.poll_ms) / 1000.0,
            slow_poll_seconds=_ms(_hooks.slow_poll_ms) / 1000.0,
            fast_window_seconds=_ms(_hooks.fast_window_ms) / 1000.0,
            lease_seconds=_ms(_hooks.lease_ms) / 1000.0,
        )
    except Exception as exc:  # noqa: BLE001 - an unreadable limit means no hold, announced
        vcprint(f"[delegated hold] limit unreadable ({exc!r}); this call is not held", color="red")
        return None
    if found.seconds <= 0 or found.lease_seconds <= 0 or found.poll_seconds <= 0 or found.slow_poll_seconds <= 0:
        return None
    # The lease is renewed on the wait's own ticks, so it must outlast three of the slowest: a lease set
    # shorter than that would lapse on every long wait and silently send every result to /resume.
    slowest = max(found.poll_seconds, found.slow_poll_seconds)
    if found.lease_seconds < slowest * 3:
        vcprint(
            f"[delegated hold] lease {found.lease_seconds:.1f}s is shorter than three polls of {slowest:.1f}s; "
            f"using {slowest * 3:.1f}s (raise runtime.delegated_hold_lease_ms or lower the slow poll)",
            color="yellow",
        )
        found = replace(found, lease_seconds=slowest * 3)
    return found


def person_reads_live() -> bool:
    """RESUME-AND-RECOVERY 1b rules P2-P3: only a run somebody reads live, whose answer reports to nobody.

    The client named :data:`PERSON_HOLD_READ` (``delegated-hold-v1`` alone never holds a question); the run is
    saved (``store``), is a person's top-level turn (no ``parent_request_id``: a child agent run reports to its
    parent), not an internal agent (``is_internal_agent``) or machine run (``system_run``), and not a muted helper
    (``client_delegation_disabled``, set with the silent emitter by ``run_agent``). A headless continuation carries
    no hold read at all (``without_hold_read``). Shared by the executor's person hold and a tool that asks a
    person with a countdown (aidream ``action_requests/countdown.py``).
    """
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.processing.blocks.saved_blocks import client_reads
    from matrx_ai.tools.merge import CLIENT_DELEGATION_DISABLED_KEY

    app_ctx = try_get_app_context()
    if app_ctx is None or not client_reads(app_ctx, PERSON_HOLD_READ):
        return False
    metadata = getattr(app_ctx, "metadata", None) or {}
    return (
        bool(getattr(app_ctx, "store", True))
        and not getattr(app_ctx, "system_run", False)
        and not getattr(app_ctx, "is_internal_agent", False)
        and not getattr(app_ctx, "parent_request_id", None)
        and metadata.get(CLIENT_DELEGATION_DISABLED_KEY) is not True
    )


def hold_seconds() -> float:
    """The wait one call gets now: 0 when it would not be held."""
    found = settings()
    return found.seconds if found is not None else 0.0


def _ms(read: Callable[[], int]) -> int:
    return max(0, int(read()))


def wake(conversation_id: str, call_id: str) -> bool:
    """A result for this call landed (anywhere): let a turn waiting in THIS process look now."""
    event = _wakes.get((str(conversation_id or ""), str(call_id or "")))
    if event is None:
        return False
    event.set()
    return True


def waiting_count() -> int:
    return len(_wakes)


def _tool_call_model() -> Any:
    from matrx_ai.db import cxm

    return cxm.tool_call.model


async def _read_row(row_id: str) -> Any:
    from matrx_ai.db import cxm

    rows = await cxm.tool_call.filter_items(id=row_id)
    return rows[0] if rows else None


async def _write(row_id: str, *, conversation_id: str, held_until: datetime | None, renew: bool) -> int:
    """One immediate, committed row update on its own coordinator; the rows it changed.

    ``renew`` extends a lease this turn already holds; otherwise this is the first claim (``held_until``
    set) or the give-up (``held_until`` None, only where a lease is still there).
    """
    from matrx_ai.persistence import standalone_coordinator

    filters: dict[str, Any] = {"id": row_id, "status": "delegated", "resolved_at__isnull": True}
    if renew or held_until is None:
        filters["held_until__isnull"] = False
    async with standalone_coordinator(reason="delegated_hold", conversation_id=conversation_id or None):
        result = await _tool_call_model().filter(**filters).update(held_until=held_until)
    return int(getattr(result, "rows_affected", 0) or 0)


async def claim(row_id: str, *, conversation_id: str, hold: HoldSettings) -> bool:
    """Take the lease on a parked call BEFORE ``tool_delegated`` is emitted. False: the row is not parked."""
    until = datetime.now(UTC) + timedelta(seconds=hold.lease_seconds)
    return await _write(row_id, conversation_id=conversation_id, held_until=until, renew=False) == 1


async def _give_up(row_id: str, *, conversation_id: str, reason: ReleaseReason, started: float) -> HoldOutcome:
    """Release the lease. A result that beat the release under the lease is taken instead.

    Never raises: a release the database refused leaves a lease that lapses by itself, and the call parks.
    """
    waited_ms = int((time.monotonic() - started) * 1000)
    try:
        released = await _write(row_id, conversation_id=conversation_id, held_until=None, renew=False)
        if released == 1:
            return HoldOutcome(taken=False, reason=reason, waited_ms=waited_ms)
        row = await _read_row(row_id)
    except asyncio.CancelledError:
        raise
    except Exception as exc:  # noqa: BLE001 - the call stays parked; its lease lapses within one lease
        await _report(exc, row_id=row_id, step="give_up")
        # ONE MORE LOOK before parking: a result the resolver took under this lease means its caller was
        # told "the open stream continues" — parking on it would strand the turn. Bounded, never raising.
        try:
            row = await asyncio.wait_for(_read_row(row_id), timeout=max(1.0, poll_seconds_for_give_up()))
        except asyncio.CancelledError:
            raise
        except Exception as again:  # noqa: BLE001 - announced; the call parks and its lease lapses
            await _report(again, row_id=row_id, step="give_up_reread")
            return HoldOutcome(taken=False, reason="database", waited_ms=waited_ms)
        if row is not None and _resolved(row) and getattr(row, "held_until", None) is not None:
            return HoldOutcome(taken=True, row=row, waited_ms=waited_ms)
        return HoldOutcome(taken=False, reason="database", waited_ms=waited_ms)
    if row is not None and _resolved(row) and getattr(row, "held_until", None) is not None:
        return HoldOutcome(taken=True, row=row, waited_ms=waited_ms)
    return HoldOutcome(taken=False, reason="answered_elsewhere" if row is not None and _resolved(row) else reason,
                       waited_ms=waited_ms)


def poll_seconds_for_give_up() -> float:
    """The re-read bound after a failed give-up: the slow poll knob (one wait tick), never a literal."""
    if _hooks is None:
        return 0.0
    return _ms(_hooks.slow_poll_ms) / 1000.0 if _safe(_hooks.slow_poll_ms, None) is not None else 0.0


def _resolved(row: Any) -> bool:
    return getattr(row, "resolved_at", None) is not None or str(getattr(row, "status", "")) != "delegated"


async def wait_for_result(
    row_id: str,
    *,
    conversation_id: str,
    call_id: str,
    hold: HoldSettings,
    stop_reason: Callable[[], Awaitable[tuple[ReleaseReason, str] | None]] | None = None,
) -> HoldOutcome:
    """Wait for the client's result on a call this turn already claimed (:func:`claim`).

    ``stop_reason`` is the run's own stop look (Stop, interrupt, a budget), asked every tick: ``None`` keeps
    waiting, else the release reason and its words.

    Returns ``taken`` with the resolved row, or a release with its reason; the lease is released on every
    path that does not take a result, cancellation included (shielded), so a parked call never keeps a
    lease nobody stands behind.
    """
    active = _hooks
    key = (str(conversation_id or ""), str(call_id or ""))
    event = asyncio.Event()
    _wakes[key] = event
    started = time.monotonic()
    deadline = started + hold.seconds
    renew_every = hold.lease_seconds / 3
    next_renew = started + renew_every
    failing_since: float | None = None
    try:
        while True:
            now = time.monotonic()
            reason: ReleaseReason | None = None
            if active is not None and not _safe(active.may_hold, True):
                reason = "shutdown"
            elif now >= deadline:
                reason = "timeout"
            elif stop_reason is not None:
                stop = await _safe_async(stop_reason)
                if stop:
                    reason = stop[0]
            if reason is not None:
                return await _give_up(row_id, conversation_id=key[0], reason=reason, started=started)

            tick = hold.poll_seconds if now - started < hold.fast_window_seconds else hold.slow_poll_seconds
            try:
                await asyncio.wait_for(event.wait(), timeout=max(0.02, min(tick, deadline - now)))
            except TimeoutError:
                pass
            event.clear()

            # A DATABASE BLIP NEVER BECOMES A FAILED TOOL: the client may be running the call right now, so
            # an error here must not escape into the dispatch (which would write the row as an error and
            # tell the model the click failed). The wait keeps going; only a database unreachable for a
            # whole lease gives the call up, and then it parks like any other given-up hold.
            try:
                row = await _read_row(row_id)
                if not _resolved(row) and row is not None and time.monotonic() >= next_renew:
                    next_renew = time.monotonic() + renew_every
                    until = datetime.now(UTC) + timedelta(seconds=hold.lease_seconds)
                    await _write(row_id, conversation_id=key[0], held_until=until, renew=True)
                failing_since = None
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 - announced; the wait continues
                failing_since = failing_since or time.monotonic()
                await _report(exc, row_id=row_id, step="poll")
                if time.monotonic() - failing_since >= hold.lease_seconds:
                    return await _give_up(row_id, conversation_id=key[0], reason="database", started=started)
                continue
            if row is None:
                return HoldOutcome(taken=False, reason="answered_elsewhere",
                                   waited_ms=int((time.monotonic() - started) * 1000))
            if _resolved(row):
                waited_ms = int((time.monotonic() - started) * 1000)
                if getattr(row, "held_until", None) is not None:
                    return HoldOutcome(taken=True, row=row, waited_ms=waited_ms)
                # Resolved after this turn's lease lapsed or was cleared: the client was told to resume.
                return HoldOutcome(taken=False, reason="answered_elsewhere", waited_ms=waited_ms)
            if getattr(row, "held_until", None) is None:
                # THE LEASE WAS TAKEN AWAY (section 1b rule P10): still parked, but whoever cleared it (a new
                # message in the conversation) will continue it. Park at once; there is nothing to release.
                return HoldOutcome(taken=False, reason="superseded",
                                   waited_ms=int((time.monotonic() - started) * 1000))
    except asyncio.CancelledError:
        # Stop, interrupt, shutdown: the row stays parked, and never under a lease nobody stands behind.
        try:
            await asyncio.shield(_write(row_id, conversation_id=key[0], held_until=None, renew=False))
        except Exception as exc:  # noqa: BLE001 - the lease lapses by itself within one lease
            vcprint(f"[delegated hold] lease not released on cancel ({exc!r}); it lapses by itself",
                    color="yellow")
        raise
    finally:
        if _wakes.get(key) is event:
            _wakes.pop(key, None)


async def _report(exc: BaseException, *, row_id: str, step: str) -> None:
    vcprint(f"[delegated hold] database error while waiting ({step}, row {row_id}): {exc!r}", color="red")
    try:
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(exc, kind="delegated_hold_wait_database_error", route="tools/delegated_hold",
                            context={"tool_call_id": row_id, "step": step})
    except Exception:  # noqa: BLE001 - the banner above already said it
        pass


async def answered_meanwhile(conversation_id: str | None, call_ids: list[str]) -> dict[str, dict[str, Any]]:
    """Of these still-pending calls, the ones whose row is already answered, as model-facing tool results.

    Never raises: a read that fails leaves the calls pending, and the turn parks as it would have.
    """
    if not conversation_id or not call_ids:
        return {}
    try:
        from matrx_ai.db import cxm
        from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content

        found: dict[str, dict[str, Any]] = {}
        for call_id in call_ids:
            rows = await cxm.tool_call.filter_items(conversation_id=conversation_id, call_id=call_id)
            row = rows[0] if rows else None
            if row is not None and _resolved(row) and getattr(row, "is_client_delegated", False):
                found[call_id] = _rebuild_tool_result_content([row])[0]
        return found
    except Exception as exc:  # noqa: BLE001 - announced; the calls stay pending
        await _report(exc, row_id=",".join(call_ids), step="answered_meanwhile")
        return {}


def _safe(read: Callable[[], Any], fallback: Any) -> Any:
    try:
        return read()
    except Exception:  # noqa: BLE001 - a hook blip keeps the wait going on its fallback
        return fallback


async def _safe_async(read: Callable[[], Awaitable[Any]]) -> Any:
    try:
        return await read()
    except Exception:  # noqa: BLE001 - a stop look that fails allows the wait (the loop's own look still runs)
        return None
