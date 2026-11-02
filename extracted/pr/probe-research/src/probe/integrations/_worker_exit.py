"""Closing a run on the way out of a multiprocessing worker (framework-free).

Shared by the trainer integrations (``lightning``, ``huggingface``): a forked
worker (``ddp_fork``, accelerate's ``notebook_launcher``, a ``Process`` per
trial) exits through ``os._exit``, which runs no exit hook, so a run it opened
is closed from multiprocessing's own worker-exit finalizers instead. Nothing
here imports a framework.
"""

from __future__ import annotations

import logging
import math
import os
import signal
import threading
from typing import Any

log = logging.getLogger(__name__)

#: The close a worker makes on its way out is bounded, and what does not go out
#: in time stays queued, terminal status behind it. torch's ProcessContext.join
#: SIGTERMs the surviving workers the moment one fails and SIGKILLs them 30 s
#: later, so the close has to fit inside that grace: a larger
#: ``PROBE_FINISH_TIMEOUT_SEC`` is capped to this in a worker (a smaller one
#: stands).
WORKER_CLOSE_SECONDS = 20.0

#: The longest the worker's close holds back a SIGTERM or SIGINT. Past it the
#: signal goes to the handler it was meant for, close finished or not: held
#: without a limit, a close that hung could not be stopped short of SIGKILL.
WORKER_HOLD_SECONDS = 25.0


def run_held(fn: Any, signums: tuple[int, ...], seconds: float) -> None:
    """``fn()`` with ``signums`` held (:class:`_signals_held`), for a worker's
    close. torch's launcher forwards the SIGINT it got to its workers as it
    shuts down, and one that lands while the hold is being set up ran torch's
    handler, which raises: the close was skipped and the run stayed
    ``running``. So a hold that could not be set up is tried again; after
    three signals in a row, ``fn()`` runs without one. A hold
    :func:`hold_until_the_close` started ends after ``fn()``."""
    try:
        for _attempt in range(3):
            hold = _signals_held(signums, seconds)
            try:
                hold.__enter__()
            except BaseException:  # noqa: BLE001 -- that signal was the ending; the close still runs
                continue
            try:
                fn()
            finally:
                hold.__exit__(None, None, None)
            return
        fn()
    finally:
        end_hold_until_the_close()


#: (pid, hold) of the hold :func:`hold_until_the_close` started; :func:`run_held` ends it.
_until_close: tuple[int, Any] | None = None


def hold_until_the_close(signums: tuple[int, ...]) -> None:
    """Hold ``signums`` from a worker's first SIGINT / SIGTERM until its close (`run_held`).

    torch's launcher forwards the signal it got to its workers as it shuts down, 1-2 ms after
    the first. One landing in multiprocessing's exit before the close's own hold was up skipped
    the close: the run stayed ``running``. Call it from the worker's signal handler, before
    handing the signal on. Bounded by `WORKER_HOLD_SECONDS`, should no close come."""
    global _until_close
    if _until_close is not None and _until_close[0] == os.getpid():
        if not _until_close[1]._expired:
            return
        end_hold_until_the_close()  # ran out with no close (the worker went on): start afresh
    hold = _signals_held(signums, WORKER_HOLD_SECONDS)
    hold.__enter__()  # a signal landing meanwhile runs the handler it finds, as before
    _until_close = (os.getpid(), hold)


def end_hold_until_the_close() -> None:
    """Deliver what :func:`hold_until_the_close` held to the handlers it held them from: after
    the close, or when a later ``train()`` begins (the worker went on; a note chained over a
    spent hold would hand it its signal, which it drops). Main thread only."""
    global _until_close
    if threading.current_thread() is not threading.main_thread():
        return
    held, _until_close = _until_close, None
    if held is not None and held[0] == os.getpid():
        held[1].__exit__(None, None, None)


def _forget_the_hold_in_a_child() -> None:
    """A child forked under a hold (this one, or a close's over it) inherits its handlers but
    not its timer, so it would hold for good: put back what each hold took over."""
    global _until_close
    _until_close = None
    for signum in (signal.SIGINT, signal.SIGTERM):
        for _depth in range(4):
            try:
                handler = signal.getsignal(signum)
                if getattr(handler, "__func__", None) is not _signals_held._hold:
                    break
                fallback = signal.default_int_handler if signum == signal.SIGINT else signal.SIG_DFL
                signal.signal(signum, handler.__self__._previous.get(signum, fallback))
            except Exception:  # noqa: BLE001 -- a child's start must never fail here
                break


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_forget_the_hold_in_a_child)


def cap_finish_timeout(seconds: float) -> None:
    """Cap ``PROBE_FINISH_TIMEOUT_SEC`` at ``seconds`` (a smaller one stands)."""
    raw = os.environ.get("PROBE_FINISH_TIMEOUT_SEC", "")
    try:
        requested = float(raw)
    except ValueError:
        requested = math.inf
    if not requested <= seconds:  # also NaN
        os.environ["PROBE_FINISH_TIMEOUT_SEC"] = str(seconds)


def capped_finish_timeout(seconds: float) -> float:
    """What :func:`cap_finish_timeout` would leave in ``PROBE_FINISH_TIMEOUT_SEC``,
    as a value, for a close that must not change the environment the rest of
    the process reads (one made while the process goes on)."""
    try:
        requested = float(os.environ.get("PROBE_FINISH_TIMEOUT_SEC", ""))
    except ValueError:
        return seconds
    return requested if requested <= seconds else seconds  # also NaN


class _signals_held:
    """Hold these signals while the worker's close runs, then deliver them.

    SIGTERM: when one rank fails, torch SIGTERMs the others, and Lightning's
    SIGTERM handler runs a `dist.broadcast` -- to a rank that is already gone
    -- so gloo raised "Connection closed by peer" from inside the close and the
    run stayed `running`. SIGINT: a parent killed by SIGTERM sends its workers
    their death signal (SIGINT), whose KeyboardInterrupt cut the close short
    and dropped a queued write (the outbox counts an interrupted append as a
    drop).

    Each is re-delivered afterwards to the handler that was there before; after
    ``seconds`` it is delivered at once, close finished or not (a timer thread
    wakes the main thread with it). A signal whose handler was not set from
    Python (``getsignal`` is None) is not held: that handler could never be
    put back."""

    def __init__(self, signums: tuple[int, ...], seconds: float) -> None:
        self._signums = signums
        self._seconds = seconds
        self._previous: dict[int, Any] = {}
        self._caught: list[int] = []
        self._expired = False
        self._timer: threading.Timer | None = None

    def __enter__(self) -> _signals_held:
        if threading.current_thread() is not threading.main_thread():
            return self  # only the main thread may set a handler: nothing to hold
        try:
            for signum in self._signums:
                try:
                    current = signal.getsignal(signum)
                except (ValueError, OSError):
                    continue
                if current is None:
                    continue
                # Recorded first: if a signal's handler interrupts us between
                # these two lines, the restore below must know what to put back.
                self._previous[signum] = current
                try:
                    signal.signal(signum, self._hold)
                except (ValueError, OSError):
                    del self._previous[signum]
            if self._previous:
                self._timer = threading.Timer(
                    self._seconds, self._expire, args=(threading.main_thread().ident,)
                )
                self._timer.daemon = True
                self._timer.start()
        except BaseException:
            # A signal already on its way ran the handler it found (torch's
            # raises) before every hold was up: put back what was taken over,
            # then let the caller see it (run_held tries again).
            if self._timer is not None:
                self._timer.cancel()
            for signum, previous in list(self._previous.items()):
                try:
                    signal.signal(signum, previous)
                except Exception:  # noqa: BLE001
                    pass
            self._previous.clear()
            raise
        return self

    def _hold(self, signum: int, _frame: Any) -> None:
        if self._expired:
            self._deliver(signum)
        elif signum not in self._caught:
            self._caught.append(signum)

    def _expire(self, main_thread: int) -> None:
        self._expired = True
        for signum in list(self._caught):
            try:
                # To the main thread, so a blocking call there is interrupted
                # and the Python-level handler runs.
                signal.pthread_kill(main_thread, signum)
            except Exception:  # noqa: BLE001
                pass

    def _deliver(self, signum: int) -> None:
        previous = self._previous.pop(signum, None)
        if signum in self._caught:
            self._caught.remove(signum)
        if previous is None:
            return
        signal.signal(signum, previous)
        signal.raise_signal(signum)

    def __exit__(self, *exc_info: Any) -> None:
        if self._timer is not None:
            self._timer.cancel()
        # Every handler back first, then every held signal, each to its own:
        # one handler raising must not leave another signal held forever.
        for signum, previous in list(self._previous.items()):
            try:
                signal.signal(signum, previous)
            except Exception:  # noqa: BLE001
                log.debug("probe: restoring a signal handler failed", exc_info=True)
        self._previous.clear()
        caught, self._caught = self._caught, []
        interrupt: BaseException | None = None
        for signum in caught:
            try:
                signal.raise_signal(signum)
            except Exception:  # noqa: BLE001 -- the previous handler's own failure
                log.debug("probe: re-delivering a held signal failed", exc_info=True)
            except BaseException as exc:  # KeyboardInterrupt: the handler's job
                interrupt = interrupt or exc
        if interrupt is not None:
            raise interrupt
