"""A second init() waits for, replaces or keeps the previous run (W&B reinit modes), closing a replaced run within its bound."""

from __future__ import annotations
import threading
import time
from typing import TYPE_CHECKING

from .. import errors

if TYPE_CHECKING:
    from collections.abc import Callable

    from ..run.run import Run

#: W&B's ``reinit`` values. ``default`` is ``finish_previous`` here (D16): W&B's
#: script default, ``return_previous``, leaves the first run open with nothing
#: bound to it, and an open run nobody closes is reaped ``crashed``.
_REINIT_MODES = ("default", "return_previous", "finish_previous", "create_new")
#: Longest a reinit waits on the previous run's writes before its close is
#: queued behind them: the caller is waiting for its NEW run.
_REINIT_FLUSH_CAP_S = 10.0
#: Held by a reinit from the moment it starts closing the old run until the new
#: one is bound. Another thread that finds no open run meanwhile waits on it
#: instead of raising "no active run" into a training loop that did nothing
#: wrong (`_reinit_in_progress` keeps that wait off the ordinary miss path) --
#: until `_reinit_wait_until`, `_REINIT_FLUSH_CAP_S` after the old run was let
#: go: opening the new run has no bound of its own (~122 s against an API that
#: is down), and that thread is someone's training loop (review of #2016).
_reinit_lock = threading.RLock()
_reinit_in_progress = False
_reinit_wait_until: "float | None" = None
#: Whether `log()` already said it is dropping rows while a reinit runs long.
_warned_reinit_drop = False
#: Writes dropped that way, and the run that replaced the closed one once it
#: is bound: they are counted on it (`probe_finish.dropped_writes` at its
#: close), since they were meant for it. Both under `_default_lock`.
_reinit_dropped = 0
_reinit_new_run: "Run | None" = None


class _ReinitStillOpening(errors.RosError):
    """No run to write to: another thread's :func:`init` is still opening the
    run that replaces the one it closed, past the wait `_binding` allows."""


def _binding(*, required: bool = True) -> "_Binding | None":
    found = _open_binding()
    if found is None and _reinit_in_progress:
        until = _reinit_wait_until
        wait = _REINIT_FLUSH_CAP_S if until is None else max(0.0, until - time.monotonic())
        if _reinit_lock.acquire(timeout=wait):
            try:
                found = _open_binding()
            finally:
                _reinit_lock.release()
        elif required:
            raise _ReinitStillOpening(
                "no active run: probe.init() on another thread closed the previous run "
                f"and is still opening the next one after {_REINIT_FLUSH_CAP_S:g}s"
            )
    if found is None and required:
        raise errors.RosError(
            "no active run — call probe.init() first, or use the explicit API: "
            "probe.Client().run(experiment=...)."
        )
    return found


def _drop_during_reinit(what: str) -> None:
    """A write found no run because a reinit is still opening one: drop it,
    count it on the run that opens (`_count_reinit_drop`), and say so once,
    instead of raising into a training loop."""
    global _warned_reinit_drop
    _count_reinit_drop()
    if _warned_reinit_drop:
        return
    _warned_reinit_drop = True
    from ...foundation.safe_warn import safe_warn

    safe_warn.warn(
        f"probe.{what}: dropped -- probe.init() on another thread closed the previous "
        f"run and is still opening the next one after {_REINIT_FLUSH_CAP_S:g}s; writes "
        "until it opens are dropped and counted on it as dropped_writes (said once)",
        stacklevel=3,
    )


def _count_reinit_drop() -> None:
    global _reinit_dropped
    with _default_lock:
        if _reinit_new_run is not None:
            # Bound after this write gave up waiting: count it there directly.
            _mark_dropped(_reinit_new_run, 1)
        else:
            _reinit_dropped += 1


def _replace_previous(reinit_mode: str, given: dict, open_new: "Callable[[], Run]") -> "Run":
    """:func:`init`'s reinit decision, then ``open_new()`` for the new run.
    ``given`` is every argument the caller passed, named when a returned run
    ignores them."""
    global _reinit_in_progress, _reinit_wait_until, _warned_reinit_drop
    global _reinit_dropped, _reinit_new_run
    previous = _previous_in_scope()
    if previous is not None and (reinit_mode == "return_previous" or previous.attached):
        ignored = sorted(k for k, v in given.items() if v is not None)
        if ignored:
            why = (
                "it joined PROBE_RUN_ID, whose launcher owns the run"
                if previous.attached
                else 'reinit="return_previous"'
            )
            from ...foundation.safe_warn import safe_warn

            safe_warn.warn(
                f"probe.init() returned the run already open in this scope "
                f"({previous.run.slug or previous.run.id}) because {why}, and ignored "
                f"{', '.join(ignored)}. Call probe.finish() first to open a new run.",
                stacklevel=3,
            )
        return previous.run
    if previous is not None and reinit_mode == "finish_previous":
        with _reinit_lock:
            _reinit_in_progress = True
            _reinit_wait_until = None
            _warned_reinit_drop = False
            with _default_lock:
                _reinit_dropped, _reinit_new_run = 0, None
            try:
                # BEFORE the new run exists: its output sweep and read capture
                # skip while another run on this host is still open over the
                # same folder.
                _close_binding(previous, closed_by="reinit")
                # Other threads now find no run; they wait this long for the
                # new one (`_binding`), then `log()` drops instead of waiting.
                _reinit_wait_until = time.monotonic() + _REINIT_FLUSH_CAP_S
                run = open_new()
                with _default_lock:
                    # What was dropped meanwhile was meant for this run.
                    _mark_dropped(run, _reinit_dropped)
                    _reinit_dropped, _reinit_new_run = 0, run
                return run
            finally:
                _reinit_in_progress = False
                _reinit_wait_until = None
    return open_new()


def _reinit_bound(run: "Run") -> float:
    """A reinit's close deadline: ``PROBE_FINISH_TIMEOUT_SEC`` (600 s unset),
    never more than `_REINIT_FLUSH_CAP_S`. The caller waits for a new run."""
    return min(run._resolve_finish_timeout(None), _REINIT_FLUSH_CAP_S)


def _retire(binding: _Binding) -> None:
    """Let go of a run closed through its handle. Never raises.

    After a ``finish()`` this is a release. After a bare ``set_status`` --
    ``run.execute()`` closes its run that way -- ``finish()`` (idempotent)
    first does the rest of the close, bounded like a reinit: crumb, lineage,
    the drain, never a second verdict. A close still RUNNING (another thread's
    ``finish()``) is left alone: releasing closed the client it was sending
    through, and waiting could hold this caller for its whole deadline. Its
    own caller lets go of it, or the next look here does."""
    from ..run.closing.closing import _FINISHING

    run = binding.run
    if getattr(run, "_finish_result", None) is _FINISHING:
        return
    started = time.monotonic()
    bound = _REINIT_FLUSH_CAP_S
    try:
        bound = _reinit_bound(run)
        run.finish(flush_timeout=bound)
    except Exception:  # noqa: BLE001 -- the run already has its verdict
        pass
    # Its client too, within the same bound (see `_close_binding`).
    _release_quietly(binding, timeout=max(0.0, bound - (time.monotonic() - started)))


def _reinit_mode(reinit: object) -> str:
    """W&B's ``reinit`` values; the booleans are W&B's (deprecated) spelling."""
    if reinit is True:
        return "finish_previous"
    if reinit is False:
        return "return_previous"
    if reinit is None or reinit == "default":
        return "finish_previous"  # D16
    if reinit not in _REINIT_MODES:
        raise errors.ValidationError(
            f"reinit must be one of {', '.join(_REINIT_MODES)} (or True/False), not {reinit!r}"
        )
    return str(reinit)


def _close_binding(binding: _Binding, *, closed_by: str) -> None:
    """Close a run because something else replaces it. Never raises.

    ``completed``, with ``probe_finish.closed_by`` in its summary so the run
    says why it ended. The close is BOUNDED -- at most
    ``min(PROBE_FINISH_TIMEOUT_SEC, 10)`` seconds (`_reinit_bound`), letting go
    of its client included -- and whatever is left is queued with the close
    behind it for the detached worker, because the caller is waiting for a new
    run, not for this one's backlog. One line says what happened: printed when
    the close landed, a warning when it is queued or failed. Ctrl-C (or a
    SystemExit) during it queues ``canceled`` behind the data instead of
    leaving the run for the reaper to call ``crashed`` -- unless the terminal
    write was already on its way, which the server may have applied: then that
    same status is queued again (`Run._close`). The interrupt then propagates.

    The marker is merged over the summary this handle last saw, because a
    summary write REPLACES the whole field on the server -- as a metadata
    write does. ``summary`` is where the close's own accounting
    (``probe_finish``) already lives, and the SDK writes a summary only when
    it closes a run, so what this handle saw is what the server has unless a
    caller queued a summary write of their own."""
    from ...foundation.safe_warn import safe_warn

    run = binding.run
    if getattr(run, "disabled", False):
        # PROBE_MODE=disabled recorded nothing, so there is nothing to close
        # or say: its handle finishes and lets go.
        try:
            run.finish("completed")
        except Exception:  # noqa: BLE001 -- the new run must still open
            pass
        _release_quietly(binding)
        return
    label = run.slug or run.id
    bound = _REINIT_FLUSH_CAP_S
    started = time.monotonic()
    try:
        existing = run.data.get("summary_metrics") or run.data.get("summary") or {}
        if not isinstance(existing, dict):
            existing = {}
        accounting = existing.get("probe_finish")
        summary = {
            **existing,
            "probe_finish": {**(accounting if isinstance(accounting, dict) else {}), "closed_by": closed_by},
        }
        bound = _reinit_bound(run)
        # Not the caller's choice to close it, so an interrupt is not a
        # `completed` it asked for. `Run._close` queues it on an interrupt in
        # either window, the finalizers or the drain and terminal write.
        run._status_on_interrupt = "canceled"
        # Never strict: a reinit never raises, and a strict close refuses
        # rather than queueing the verdict behind what it could not deliver.
        result = run.finish("completed", summary=summary, flush_timeout=bound, strict=False)
    except Exception as exc:  # noqa: BLE001 -- the new run must still open
        try:
            run.stop_heartbeat()
        except Exception:  # noqa: BLE001
            pass
        safe_warn.warn(
            f"probe: run {label} did not close cleanly when probe.init() replaced it "
            f"({safe_warn.describe(exc)}); see `probe outbox status`",
            stacklevel=3,
        )
    else:
        if isinstance(result, dict) and (result.get("close_rejected") or result.get("close_unrecorded")):
            safe_warn.warn(
                f"probe: run {label} did not close cleanly when probe.init() replaced it "
                "(the close was rejected or could not be recorded); see `probe outbox status`",
                stacklevel=3,
            )
        elif isinstance(result, dict) and result.get("offline"):
            pass  # an offline close always queues; its own line says where
        elif isinstance(result, dict) and result.get("finish_queued"):
            safe_warn.warn(
                f"probe: closed run {label} because probe.init() opened another; "
                f"{result.get('remaining', 0)} write(s) could not be delivered in "
                f"{bound:g}s and are queued, with the close behind them",
                stacklevel=3,
            )
        else:
            print(
                f"probe: closed run {label} (completed) because probe.init() opened "
                'another; pass reinit="create_new" to keep both open',
                flush=True,
            )
    finally:
        # Closing the client joins its exporter, which a hung API holds
        # mid-request: within what is left of the bound, not 5 s past it.
        _release_quietly(binding, timeout=max(0.0, bound - (time.monotonic() - started)))
from probe.sdk.fluent.bindings import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _Binding,
    _default_lock,
    _mark_dropped,
    _open_binding,
    _previous_in_scope,
    _release_quietly,
)
