"""A worker's close survives a signal that lands while its hold is set up.

torch's launcher forwards the SIGINT it got to its workers as it shuts down,
and torch's worker handler raises. One that landed while
`_signals_held.__enter__` was installing the hold skipped the close, and the
run stayed `running` (seen in #2070's forked-worker Ctrl-C test, under load).
The interruption is placed deterministically here: at the moment the hold
for SIGINT is installed, the handler found there runs and raises.
"""

from __future__ import annotations

import os
import signal
import time
import warnings

import pytest

from probe.integrations import _worker_exit


@pytest.fixture
def handlers(monkeypatch):
    before = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    monkeypatch.setattr(_worker_exit, "_until_close", None)
    yield before
    _worker_exit.end_hold_until_the_close()
    for signum, handler in before.items():
        signal.signal(signum, handler)


def _interrupt_hold_setup(monkeypatch, times: int) -> list[int]:
    """The next ``times`` installs of a hold for SIGINT raise, as torch's
    handler does when its signal is processed at that instant."""
    real = signal.signal
    raised: list[int] = []

    def install(signum, handler):
        if (
            signum == signal.SIGINT
            and getattr(handler, "__func__", None) is _worker_exit._signals_held._hold
            and len(raised) < times
        ):
            raised.append(signum)
            raise RuntimeError("Process got signal: 2")  # torch's SignalException
        return real(signum, handler)

    monkeypatch.setattr(signal, "signal", install)
    return raised


def test_a_signal_during_the_hold_setup_still_closes_once_and_restores_handlers(
    monkeypatch, handlers
):
    raised = _interrupt_hold_setup(monkeypatch, times=1)
    ran = []
    _worker_exit.run_held(lambda: ran.append(True), (signal.SIGTERM, signal.SIGINT), 5.0)
    assert raised == [signal.SIGINT] and ran == [True]
    # No hold left behind from the interrupted attempt: each handler is the
    # one it was before, so a later signal still reaches it.
    assert {s: signal.getsignal(s) for s in handlers} == handlers


def test_signals_that_keep_coming_leave_a_close_without_the_hold(monkeypatch, handlers):
    raised = _interrupt_hold_setup(monkeypatch, times=10)
    ran = []
    _worker_exit.run_held(lambda: ran.append(True), (signal.SIGTERM, signal.SIGINT), 5.0)
    assert len(raised) == 3 and ran == [True]
    assert {s: signal.getsignal(s) for s in handlers} == handlers


def test_the_interrupted_hold_puts_back_what_it_took_over(monkeypatch, handlers):
    """The plain `with` (as the old close used it) still raises, but no longer
    leaves SIGTERM on a dead hold that would swallow every later SIGTERM."""
    _interrupt_hold_setup(monkeypatch, times=1)
    with (
        pytest.raises(RuntimeError),
        _worker_exit._signals_held((signal.SIGTERM, signal.SIGINT), 5.0),
    ):
        pass
    assert signal.getsignal(signal.SIGTERM) is handlers[signal.SIGTERM]


# -- from the worker's first signal (`hold_until_the_close`) -------------------


def test_a_signal_before_the_close_waits_for_it_then_reaches_its_handler(handlers):
    """The worker's first signal starts the hold; the launcher's forwarded one, landing
    before the close's own hold is up (in multiprocessing's exit), waits for the close and
    then reaches the handler it was meant for, once."""
    seen: list = []
    signal.signal(signal.SIGINT, lambda signum, _frame: seen.append(signum))
    mine = signal.getsignal(signal.SIGINT)
    _worker_exit.hold_until_the_close((signal.SIGTERM, signal.SIGINT))
    signal.raise_signal(signal.SIGINT)
    assert seen == []
    _worker_exit.run_held(lambda: seen.append("close"), (signal.SIGTERM, signal.SIGINT), 5.0)
    assert seen == ["close", signal.SIGINT]
    assert signal.getsignal(signal.SIGINT) is mine
    assert signal.getsignal(signal.SIGTERM) is handlers[signal.SIGTERM]
    assert _worker_exit._until_close is None


def test_with_no_close_the_hold_lets_go_at_its_limit(monkeypatch, handlers):
    monkeypatch.setattr(_worker_exit, "WORKER_HOLD_SECONDS", 0.2)
    seen: list = []
    signal.signal(signal.SIGINT, lambda signum, _frame: seen.append(signum))
    _worker_exit.hold_until_the_close((signal.SIGINT,))
    signal.raise_signal(signal.SIGINT)
    assert seen == []
    give_up = time.monotonic() + 30
    while not seen and time.monotonic() < give_up:
        time.sleep(0.01)  # the timer re-delivers it to this (main) thread
    assert seen == [signal.SIGINT]
    # The worker went on (a later train() in the same process): its next first signal
    # holds again rather than finding the spent hold.
    _worker_exit.hold_until_the_close((signal.SIGINT,))
    signal.raise_signal(signal.SIGINT)
    assert seen == [signal.SIGINT]
    _worker_exit.run_held(lambda: None, (signal.SIGINT,), 5.0)
    assert seen == [signal.SIGINT, signal.SIGINT]


@pytest.mark.skipif(not hasattr(os, "fork"), reason="fork")
def test_a_process_forked_under_the_hold_gets_the_handlers_back(handlers):
    """A child inherits the hold's handlers but not its timer: it would hold for good."""
    def mine(_signum, _frame):
        pass

    signal.signal(signal.SIGINT, mine)
    _worker_exit.hold_until_the_close((signal.SIGINT,))
    read_end, write_end = os.pipe()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)  # forking with the hold's timer thread up
        pid = os.fork()
    if pid == 0:
        ok = signal.getsignal(signal.SIGINT) is mine and _worker_exit._until_close is None
        os.write(write_end, b"1" if ok else b"0")
        os._exit(0)
    os.close(write_end)
    assert os.read(read_end, 1) == b"1"
    os.close(read_end)
    os.waitpid(pid, 0)
    assert signal.getsignal(signal.SIGINT) is not mine  # still held here, in the worker
