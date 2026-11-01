"""How the process is ending (sys.exit wrapper, excepthook, note_exit): the exit record, the exit and
SIGTERM-flush hooks, and closing the runs still bound at exit."""

from __future__ import annotations

import atexit
import os
import sys
import threading
from typing import TYPE_CHECKING

from .. import errors

if TYPE_CHECKING:

    from ..run.run import Run


# -- exit hooks ----------------------------------------------------------------
# How the process ends decides how the run ends, and Python announces it in
# three places, none of which sees the others:
#
#   * an uncaught exception reaches ``sys.excepthook`` (never a SystemExit);
#   * ``sys.exit(code)`` raises a SystemExit no hook ever sees -- Hydra and
#     Lightning both end a failed or interrupted job this way, from INSIDE their
#     own ``except`` blocks, so the traceback is swallowed and the exit is all
#     that is left;
#   * atexit runs after both and is the only place a run can still be closed.
#
# So the first two RECORD and atexit ACTS. The sys.exit wrapper is W&B's
# (`wandb/sdk/lib/exit_hooks.py`): replace ``sys.exit``, remember the code, call
# the previous one. Code-less exits a library raises itself (Lightning's
# SIGTERMException) reach none of them; the integration says so through
# :func:`note_exit`.
#
# KNOWN LIMITS, shared with W&B: an exit that never calls the wrapper is not
# seen -- ``raise SystemExit(2)``, the ``exit()`` builtin, a ``from sys import
# exit`` taken before ``probe.init()``, and above all ``sys.exit(main())`` with
# ``probe.init()`` inside ``main()``, where ``sys.exit`` is looked up before
# ``main()`` runs. With no launcher such a run closes ``completed``. Under
# ``probe exec`` it is right: with nothing recorded the child leaves the close to
# the launcher, which has the real exit code (``EXEC_FINALIZES_ENV``). A
# ``sys.exit(2)`` the script catches and survives still records ``failed``.
#
#: The chain lives on ``sys``, not in this module, like ``sys._probe_reads_state``
#: in inputs.py: ``importlib.reload(fluent)`` re-runs this file in the SAME module
#: dict while ``sys.exit`` is still the wrapper whose globals ARE that dict. With
#: the chain in module globals, a reload reset "the previous sys.exit" to None
#: (every exit raised TypeError) and a re-install captured the wrapper as its own
#: predecessor (RecursionError). Keys: ``exit`` and ``excepthook`` -- what was
#: installed before us -- and ``pid``, the process whose exit is the bound run's.
#: A forked child inherits all of it together with the parent's binding, so
#: without the pid a child's exit closed the PARENT's run with its own verdict.
_HOOKS_ATTR = "_probe_exit_hooks"
_exit_status = "completed"
#: Whether a hook saw how the process is ending (sys.exit, the excepthook,
#: note_exit). When none did, the status at exit is a guess -- see
#: :func:`_finish_at_exit`.
_exit_recorded = False
#: The exception that ended the process, held for :func:`_finish_at_exit` to
#: report. This hook is the only place in the client where a dying run's
#: traceback is in scope; until it was kept, the sole evidence a crash left
#: behind was ``_exit_status``, which says THAT the run broke and never why.
_exit_exception: BaseException | None = None
#: The non-zero code the process is exiting with, and what reported it
#: (``sys.exit`` or ``excepthook``). Written as the run's ``exit`` process span,
#: which is where the crash email reads an exit code from (`_EXIT_SQL`).
_exit_code: int | None = None
_exit_via: str | None = None


def _reset_exit_record() -> None:
    """Forget how the previous run's process was ending: status, exception, code (`_bind_new`
    calls it under `_default_lock` for each run it binds)."""
    global _exit_status, _exit_exception, _exit_code, _exit_via, _exit_recorded
    _exit_status = "completed"
    _exit_recorded = False
    _exit_exception = None
    _exit_code = None
    _exit_via = None


_EXIT_STATUSES = ("completed", "failed", "canceled")


def _hooks() -> dict | None:
    state = getattr(sys, _HOOKS_ATTR, None)
    return state if isinstance(state, dict) else None


def _in_hooks_process() -> bool:
    state = _hooks()
    return state is not None and state.get("pid") == os.getpid()


def _record_exit(
    status: str,
    *,
    exc: BaseException | None = None,
    code: int | None = None,
    via: str | None = None,
) -> None:
    """Remember how the process is ending, for :func:`_finish_at_exit`.

    Last word wins: a Lightning Ctrl-C reports through :func:`note_exit` and
    then through its own ``sys.exit(1)``, and both say ``canceled``."""
    global _exit_status, _exit_exception, _exit_code, _exit_via, _exit_recorded
    _exit_recorded = True
    _exit_status = status
    # Only a failure is diagnosed. Ctrl-C is a decision, not a defect, and a
    # process that chose to exit 0 has declared the exception handled.
    _exit_exception = exc if status == "failed" else None
    _exit_code = code or None
    _exit_via = via if code else None


def note_exit(status: str, exc: BaseException | None = None) -> None:
    """Tell the close at exit how this process is ending. For integrations.

    Some endings reach no process hook at all. Lightning turns SIGTERM into
    ``SIGTERMException``, a code-less SystemExit: the process exits 0, the
    excepthook never runs, and the run would close ``completed``. A trainer's
    ``on_exception`` sees it, so the integration calls this from there:
    KeyboardInterrupt -> ``"canceled"``; ``SIGTERMException`` or anything else
    -> ``"failed"``, passing the exception so it is reported as the run's
    diagnostic. The run is closed with this status when the process exits.

    Not a signal handler itself. The SIGTERM handler `init` installs
    (:mod:`probe.sdk.run.launch.preempt`) runs AFTER a framework's own -- Lightning's
    composes with it -- and a close on the way out of a SIGTERM is
    ``failed`` whatever is noted here.
    """
    if status not in _EXIT_STATUSES:
        raise errors.ValidationError(
            f"note_exit status must be one of {', '.join(_EXIT_STATUSES)}, not {status!r}"
        )
    if not _in_hooks_process():
        # No probe.init() in this process -- or a forked child, whose ending
        # is not the parent's run's.
        return
    _record_exit(status, exc=exc)
    binding = _binding(required=False)
    if binding is not None:
        # Also on the run itself: inside `with probe.init()`, the block closes
        # the run before any exit hook runs, and a code-less SystemExit
        # (Lightning's SIGTERMException) alone reads as success there.
        binding.run._noted_exit = (status, exc)


def _forget_noted_exit(run: "Run") -> None:
    """Take back a :func:`note_exit` the process outlived. For integrations.

    A sweep loop caught the error one trainer noted, and a new trainer is now
    starting on the same run (the script's, or a launcher's): that ending was
    not the process's, and it must not close the run ``failed`` at exit. The
    process-wide record is cleared only while it is still the one ``note_exit``
    made -- anything recorded since (a ``sys.exit`` wrapper) stands."""
    global _exit_status, _exit_exception, _exit_code, _exit_via, _exit_recorded
    noted = getattr(run, "_noted_exit", None)
    if noted is None:
        return
    run._noted_exit = None
    if not _in_hooks_process():
        return
    status, exc = noted
    if (
        _exit_recorded
        and _exit_status == status
        and _exit_code is None
        and _exit_exception is (exc if status == "failed" else None)
    ):
        _exit_status = "completed"
        _exit_recorded = False
        _exit_exception = None
        _exit_via = None


def _exit(code: object = None) -> None:
    """``sys.exit``, recording the code first, then the previous one -- which
    raises the SystemExit, so whatever was installed before still decides."""
    try:
        _note_system_exit(code)
    except Exception:  # noqa: BLE001 -- nothing may stand between a script and its exit
        pass
    try:
        _close_ending_ray_trial(code)
    except Exception:  # noqa: BLE001 -- as above
        pass
    previous = (_hooks() or {}).get("exit")
    if previous is None or previous is _exit:
        raise SystemExit(code)
    previous(code)


def _note_system_exit(code: object) -> None:
    if threading.current_thread() is not threading.main_thread():
        # sys.exit in a worker thread ends that thread, not the process: the
        # script goes on, and so does the run.
        return
    if not _in_hooks_process():
        return
    if "ipykernel" in sys.modules:
        # A notebook: IPython catches the SystemExit and the kernel carries on,
        # so the cell stopping says nothing about how the run ends. The same
        # heuristic outputs.py uses to keep fd capture out of notebooks.
        return
    from ..run.closing.status import _status_for_system_exit

    in_flight = sys.exc_info()[1]
    # Lightning's Ctrl-C (`except KeyboardInterrupt: ... sys.exit(1)`) is
    # canceled: the person stopped it, the 1 is the framework's. The code is
    # what the OS will report -- `sys.exit(-1)` exits 255, never "a signal".
    status, exit_code = _status_for_system_exit(code, in_flight)
    _record_exit(
        status,
        # Hydra: `except Exception as e: ... sys.exit(1)` -- the traceback it
        # swallowed is the in-flight exception, and it is the crash report.
        exc=in_flight if isinstance(in_flight, Exception) else None,
        code=exit_code,
        via="sys.exit",
    )


def _excepthook(exc_type, exc, tb) -> None:
    if _in_hooks_process():
        # KeyboardInterrupt is a real lifecycle outcome in this vocabulary, and
        # it is the common way a training run ends early. Calling it 'failed'
        # would lose the distinction between "I stopped it" and "it broke" --
        # and Ctrl-C is a decision, not a defect: diagnosing it would file a
        # report on every interactive session anyone ever interrupts.
        if issubclass(exc_type, KeyboardInterrupt):
            _record_exit("canceled")
        else:
            # An uncaught exception exits 1.
            _record_exit("failed", exc=exc, code=1, via="excepthook")
    previous = (_hooks() or {}).get("excepthook")
    if previous is None or previous is _excepthook:
        previous = sys.__excepthook__
    previous(exc_type, exc, tb)


def _close_bound_at_exit(binding: _Binding) -> None:
    run = binding.run
    if getattr(run, "_closed_status", None) is not None or _finish_called(run):
        # The script closed it -- `run.finish(...)`, `with probe.init()`
        # ending, `run.execute()` -- and that verdict stands. Closing again
        # overwrote it: a `with` block that completed, then `sys.exit(2)` from
        # a gate check after it, turned a finished run `failed` and mailed a
        # crash notice. So no exit code and no crash report on it.
        # Still finish() it -- idempotent: the first close's answer, or a wait
        # for one still running, or the rest of the close a bare `set_status`
        # left (the crumb, lineage, the drain; review of #2016) -- and let go
        # of it: closing the client init() built is what makes the last export
        # pass, hands leftovers to the background uploader and seals the
        # outbox producer.
        try:
            finish(_exit_status)
        except Exception:  # noqa: BLE001 -- its verdict is already out
            _release_quietly(binding)
        return
    if not _exit_recorded and _launcher_finalizes(run):
        # No hook saw how this process ends, so `completed` would be a guess,
        # and it used to land first: `sys.exit(main())` looks sys.exit up
        # before main() calls probe.init(), and the launcher's own verdict,
        # from the real exit code, then deferred to it. Deliver the data and
        # leave the close to the launcher.
        run._sends_terminal_status = False
    # BEFORE finish(), never after: finish() flips the run terminal and owns
    # the delivery barrier, so a span written behind it races a closed run.
    # Both swallow unconditionally -- neither can stop the run being closed.
    if _exit_code:
        _write_exit_span(run, _exit_code, _exit_via, _exit_status)
    if _exit_exception is not None:
        from .. import diagnostics

        diagnostics.report_exception(run, _exit_exception)
    try:
        finish(_exit_status)
    except Exception as exc:
        # Never raise from here -- it would only obscure whatever is ending the
        # process -- but never be silent either: a bare `pass` here is how one
        # busy-server 503 at exit left runs `running` until the reaper called
        # them `crashed`, with nothing on screen to say why.
        _warn_not_closed_at_exit(run, exc)


def _finish_unbound_at_exit() -> None:
    """Close what ``reinit="create_new"`` opened and nothing closed since."""
    with _default_lock:
        # This process's own: a forked child inherits the parent's list, and
        # its exit must not close the parent's runs.
        pending = [b for b in _unbound if not b.closed and b.owner[0] == os.getpid()]
        _unbound.clear()
    for binding in pending:
        was_open = _is_open(binding)
        try:
            # Idempotent, like the bound run's: a run a bare `set_status`
            # closed (`run.execute()`) keeps its verdict and gets the rest.
            binding.run.finish(_exit_status)
        except Exception as exc:  # noqa: BLE001 -- interpreter teardown, as above
            if was_open:
                _warn_not_closed_at_exit(binding.run, exc)
        finally:
            _release_quietly(binding)


def _install_sigterm_flush() -> None:
    """The run is open: put the SIGTERM flush in front of SIGTERM
    (:mod:`probe.sdk.run.launch.preempt`; main thread only, never raises)."""
    from ..run.launch import preempt

    preempt.install()


def _uninstall_sigterm_flush_if_idle() -> None:
    """No run of this process is open any more: give SIGTERM back what it had
    -- unless a handler installed after ours now holds it."""
    try:
        if _has_open_run():
            return
        from ..run.launch import preempt

        preempt.uninstall()
    except Exception:  # noqa: BLE001 -- a close never fails over this
        pass


def _install_exit_hooks() -> None:
    """Install once per interpreter, under the lock.

    Unsynchronised, two threads calling :func:`init` concurrently — which this
    module explicitly supports — can both pass the check; the second then
    captures ``sys.excepthook`` AFTER the first replaced it, so the
    "previous" hook becomes :func:`_excepthook` itself and any later uncaught
    exception recurses until the stack blows. ``sys.exit`` is chained the same
    way, and for the same reason captured only once -- keyed on ``sys``, so a
    reloaded module does not capture its own wrapper either."""
    with _default_lock:
        state = _hooks()
        if state is None:
            state = {"exit": sys.exit, "excepthook": sys.excepthook}
            setattr(sys, _HOOKS_ATTR, state)
            sys.excepthook = _excepthook
            sys.exit = _exit
            atexit.register(_finish_at_exit)
        # A forked child that opens a run of its own adopts the hooks it
        # inherited (re-wrapping would chain them to themselves); from then on
        # its exit is ITS run's, and the parent's pid no longer matches.
        state["pid"] = os.getpid()
from probe.sdk.fluent.at_exit import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _finish_at_exit,
    _launcher_finalizes,
    _warn_not_closed_at_exit,
    _write_exit_span,
)
from probe.sdk.fluent.bindings import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _Binding,
    _default_lock,
    _finish_called,
    _has_open_run,
    _is_open,
    _release_quietly,
    _unbound,
)
from probe.sdk.fluent.fluent import finish  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.ray import _close_ending_ray_trial  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.reinit import _binding  # noqa: E402 -- pieces need each other; the front door loads this one first
