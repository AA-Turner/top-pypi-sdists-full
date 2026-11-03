"""close, at interpreter exit or preemption, the runs the script never closed, writing the exit span."""

from __future__ import annotations
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:

    from ..run.run import Run


def _write_exit_span(
    run: "Run",
    code: int,
    via: str | None,
    status: str,
    *,
    extra: dict | None = None,
    direct: bool = False,
) -> None:
    """The exit code, as a ``process`` span named ``exit``. Never raises.

    The crash email reads a run's exit code from its latest process span
    (`_EXIT_SQL`); without this an in-process run that ended with
    ``sys.exit(2)`` and no traceback could only say it "was marked failed".
    Non-blocking, like the diagnostic: it must never hold the close. The id is
    derived, so writing it twice addresses one row; the epoch keeps a reopened
    run's exit apart from the first attempt's, and a non-zero rank writes its
    own rather than overwriting rank 0's. ``direct``: sent now, never queued
    (a SIGTERMed run's close on a throwaway disk, whose queue is stuck behind
    data that will not arrive); a queued copy that lands too is the same row."""
    try:
        from ..run.metrics.values import _now

        rank = _nonzero_global_rank()
        key = f"exit:{run.write_epoch}" + (f":rank{rank}" if rank is not None else "")
        attributes: dict[str, Any] = {**(extra or {}), "exit_code": code, "via": via}
        if rank is not None:
            attributes["rank"] = rank
        now = _now()
        run.span(
            "process",
            name="exit",
            external_key=key,
            parent_span_id=None,
            status=status,
            started_at=now,
            ended_at=now,
            attributes=attributes,
            strict=direct,
            blocking=False,
        )
    except Exception:  # noqa: BLE001 -- evidence never gates a close
        pass


def _finish_at_exit() -> None:
    """Close a run the script never closed.

    Without this, a script that simply ends leaves its run ``running`` until the
    server's reaper marks it ``crashed`` — the wrong answer for one that
    succeeded. atexit still runs after an unhandled exception (the traceback
    prints first), so guessing ``completed`` for every exit would be a lie;
    :func:`_excepthook` and the ``sys.exit`` wrapper are what tell them apart."""
    if not _in_hooks_process():
        # A forked child inherits this registration AND the parent's binding;
        # its exit must not close the parent's run.
        return
    binding = _binding(required=False)
    if binding is not None and binding.owner[0] == os.getpid():
        # A forked child that opened its own run with create_new is still
        # BOUND to the parent's run it inherited; its exit must not close it.
        _close_bound_at_exit(binding)
    _finish_unbound_at_exit()


def _warn_not_closed_at_exit(run: "Run", exc: BaseException) -> None:
    """One line on stderr through the SDK's non-raising warning channel."""
    from ...foundation.safe_warn import safe_warn
    from ..delivery.outbox.waiter import DeliveryIncomplete

    if isinstance(exc, DeliveryIncomplete):
        # The run was closed (queued); what is missing is said, the exit code left alone (R8).
        safe_warn.warn(f"probe: {exc}", stacklevel=2)
        return

    try:
        detail = f"{type(exc).__name__}: {exc}"
    except Exception:  # noqa: BLE001 -- a hostile __str__ must not stop the report
        detail = safe_warn.describe(exc)
    try:
        label = run.slug or run.id
    except Exception:  # noqa: BLE001
        label = "?"
    safe_warn.warn(
        f"probe: run {label} was not closed at exit ({detail[:300]}); it will be reaped "
        "as crashed -- see `probe outbox status`",
        stacklevel=2,
    )


def _launcher_finalizes(run: "Run") -> bool:
    """A `probe exec` launcher runs this process and will close THIS run from
    its real exit code (`Run.execute(finalize=True)` names the run it closes;
    another run this process attached to has no such launcher)."""
    from ..run.launch.execute import EXEC_FINALIZES_ENV

    return (os.environ.get(EXEC_FINALIZES_ENV) or "").strip() == run.id


def _close_for_preemption() -> None:
    """A SIGTERM is ending this process (:mod:`probe.sdk.run.launch.preempt`, on its
    worker thread): close what :func:`_finish_at_exit` would close, ``failed``.
    `Run.finish` adds the preemption's facts and holds each close to the
    budget."""
    if not _in_hooks_process():
        return
    # Recorded, so a finalizing launcher's child still speaks (the launcher
    # never learns the SIGTERM), and no exit span from here: `Run.finish`
    # writes the preemption's own.
    _record_exit("failed")
    _finish_at_exit()
from probe.sdk.fluent.attach import _nonzero_global_rank  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.exit import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _close_bound_at_exit,
    _finish_unbound_at_exit,
    _in_hooks_process,
    _record_exit,
)
from probe.sdk.fluent.reinit import _binding  # noqa: E402 -- pieces need each other; the front door loads this one first
