"""A worker's close survives a signal that lands while its hold is set up.

torch's launcher forwards the SIGINT it got to its workers as it shuts down,
and torch's worker handler raises. One that landed while
`_signals_held.__enter__` was installing the hold skipped the close, and the
run stayed `running` (seen in #2070's forked-worker Ctrl-C test, under load).
The interruption is placed deterministically here: at the moment the hold
for SIGINT is installed, the handler found there runs and raises.
"""

from __future__ import annotations

import signal

import pytest

from probe.integrations import _worker_exit


@pytest.fixture
def handlers():
    before = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    yield before
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
