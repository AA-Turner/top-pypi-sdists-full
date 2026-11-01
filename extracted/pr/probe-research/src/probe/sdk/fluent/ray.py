"""A Ray Tune trial thread's sys.exit: restart the outbox worker and close the trial's run."""

from __future__ import annotations

import atexit
import os
import sys
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from ..run.run import Run


# -- Ray Tune: the trial's thread ends, then Ray kills the process -------------
# A Ray Tune function trainable runs on Ray's `RunnerThread` in the trial's
# actor, and Tune ends it there: when it stops the trial -- a scheduler's early
# stop (ASHA, median stopping), or after the function returned, which Ray
# reports as one last result -- the `tune.report()` the thread waits in calls
# ``sys.exit(0)`` (`_TrainSession._report_training_result`). The actor's
# `stop()` does not wait for the thread; Tune removes the trial's placement
# group, and the raylet SIGTERMs the actor's process group and SIGKILLs it
# 200 ms later (hard-coded, Ray 2.58 `NodeManager::DisconnectClient`). Ray's
# SIGTERM handler ends the main thread, so the atexit close started only after
# Ray's own shutdown (15-80 ms in, measured): over a real network it was killed
# mid-request, and the run stayed `running` with its lease held -- the output
# helper, in the same group, died too, so nothing reported it gone.
#
# So a ``sys.exit`` on that thread closes the run the thread opened, THERE, with
# no budget: ``flush_timeout=0`` sends nothing, it queues the verdict (the lease
# release) behind the run's data and hands the queue to the detached outbox
# worker -- milliseconds of local work. That worker is started again at exit,
# past Ray's kill of the actor's children (`_arm_ray_trial_exit`). The
# verdict is the exit code's, as for any ``sys.exit``: Ray's stop is 0, so
# `completed` -- Tune records the trial TERMINATED, as one that ran every
# iteration; `canceled` means a person's Ctrl-C. A `tune.Trainable` class needs
# none of this: Tune runs its `cleanup()` and waits for it, so `probe.finish()`
# there closes the run in full.


def _ray_trial_thread() -> bool:
    """Whether this thread runs a Ray Tune function trainable: Ray's
    ``RunnerThread``, which a ``SystemExit`` ends (it never reaches the process).
    By the thread's class, never through Ray's session: the actor's `stop()`
    clears that session (``shutdown_session()``) as it releases the thread, so
    by the time the thread's ``sys.exit(0)`` runs it is already gone. Never
    imports Ray: a process that has not loaded it has no trial."""
    util = sys.modules.get("ray.air._internal.util")
    runner = getattr(util, "RunnerThread", None)
    return isinstance(runner, type) and isinstance(threading.current_thread(), runner)


def _close_ending_ray_trial(code: object) -> None:
    """A ``sys.exit`` is ending the Ray Tune trial function on this thread:
    close the run this thread opened now, queue-only (see above). Not on the
    main thread, where the process's own exit hooks close it."""
    global _ray_closes
    if threading.current_thread() is threading.main_thread():
        return
    if not _in_hooks_process() or not _ray_trial_thread():
        return
    binding = _binding(required=False)
    if binding is None or binding.owner[:2] != (os.getpid(), threading.get_ident()):
        return
    from ..run.closing.status import _status_for_system_exit

    status, _ = _status_for_system_exit(code, sys.exc_info()[1])
    with _ray_closing:
        _ray_closes += 1
    try:
        finish(status, flush_timeout=0)
    except Exception as exc:  # noqa: BLE001 -- the trial ends either way; say so
        _warn_not_closed_at_exit(binding.run, exc)
    finally:
        with _ray_closing:
            _ray_closes -= 1
            _ray_closing.notify_all()


#: Ray-trial closes running now (`_close_ending_ray_trial`), which the exit
#: kick waits out; and the outboxes it kicks at exit.
_ray_closing = threading.Condition()
_ray_closes = 0
_ray_exit_kicks: set[str] = set()
#: The longest the exit kick waits for a trial close still running. Ray's
#: SIGKILL ends the wait far sooner; outside a teardown nothing is running.
_RAY_EXIT_KICK_WAIT_S = 5.0
#: The longest the exit kick waits for the outbox worker Ray's shutdown just
#: SIGKILLed to let go of its lease (`outbox_worker.spawn_past_a_kill`): a few
#: ms normally, and Ray's group SIGKILL at 200 ms ends a teardown's wait
#: anyway. Only a live worker's lease -- a sibling trial's -- waits it out.
_RAY_KILLED_WORKER_WAIT_S = 0.5


def _arm_ray_trial_exit(run: "Run") -> None:
    """A run opened on a Ray trial's thread: start the outbox worker again at
    interpreter exit. Ray's core worker, shutting down on the SIGTERM,
    SIGKILLs the actor's direct children (``kill_child_processes_on_worker_exit``,
    on by default) -- the detached outbox worker this process started among
    them, however far it had got with the queue and the queued close. atexit
    runs after that sweep and before the group's SIGKILL: a worker started
    there is past the sweep, and in a session of its own the group's SIGKILL
    misses it. Armed at the open, not at the close: that close may still be
    running when the main thread reaches atexit, and a handler registered then
    never runs -- so the kick waits for it instead. Never raises."""
    try:
        client = run._client
        if not _ray_trial_thread() or not getattr(client, "_default_transport", False):
            return
        journal_dir = str(client.journal.dir)
    except Exception:  # noqa: BLE001 -- a run's open never fails over this
        return
    with _ray_closing:
        if journal_dir in _ray_exit_kicks:
            return
        _ray_exit_kicks.add(journal_dir)

    def kick() -> None:
        try:
            with _ray_closing:
                _ray_closing.wait_for(lambda: _ray_closes == 0, timeout=_RAY_EXIT_KICK_WAIT_S)
            from ..delivery import outbox as outbox_worker

            # Past the worker Ray just killed, whose lease outlives the kill
            # by the time the kernel takes to tear it down.
            outbox_worker.spawn_past_a_kill(journal_dir, wait=_RAY_KILLED_WORKER_WAIT_S)
        except Exception:  # noqa: BLE001 -- best effort, like every kick
            pass

    atexit.register(kick)
from probe.sdk.fluent.at_exit import _warn_not_closed_at_exit  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.exit import _in_hooks_process  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.fluent import finish  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.reinit import _binding  # noqa: E402 -- pieces need each other; the front door loads this one first
