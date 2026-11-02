"""run each part of an update on its own thread with a deadline, ending cleanly on Ctrl-C or SIGTERM."""

from __future__ import annotations
import contextlib
import contextvars
import os
import signal
import threading
import time
from collections.abc import Callable
from concurrent.futures import Future
from concurrent.futures import TimeoutError as FuturesTimeout
from contextlib import contextmanager
from dataclasses import dataclass
from probe.shared.harness.harnesses.claude_code import binary as claude_cli


#: Each component's own deadline (plan A3): a coding agent's plugin step, pi's
#: package. Past it the component is failed and left running on its thread;
#: the CLI's step and the other components finish and report.
COMPONENT_DEADLINE_S = 10 * 60
#: Overrides COMPONENT_DEADLINE_S, in seconds (tests).
COMPONENT_DEADLINE_ENV = "PROBE_UPDATE_COMPONENT_DEADLINE_S"


def component_deadline() -> float:
    try:
        value = float(os.environ.get(COMPONENT_DEADLINE_ENV, ""))
    except ValueError:
        return COMPONENT_DEADLINE_S
    return value if value > 0 else COMPONENT_DEADLINE_S


class ComponentOverdue(Exception):
    """A component that did not finish within its deadline (`component_deadline`)."""


def _deadline_words(seconds: float) -> str:
    return f"{seconds / 60:.0f} min" if seconds >= 120 else f"{seconds:g} s"


@dataclass
class _Component:
    """One part of an update on its thread (`_start`): its Future, and the
    processes it started (`claude_cli.Processes`), stopped at its deadline."""

    future: Future
    processes: claude_cli.Processes


def _start(name: str, body: Callable[[], object]) -> _Component:
    """`body` on a thread of its own, in a copy of this context, every agent
    CLI it starts tracked (`claude_cli.tracking`). A thread that cannot start
    runs it here instead."""
    future: Future = Future()
    processes = claude_cli.Processes()
    context = contextvars.copy_context()

    def tracked() -> object:
        with claude_cli.tracking(processes):
            return body()

    def run() -> None:
        try:
            future.set_result(context.run(tracked))
        except BaseException as exc:  # noqa: BLE001 - handed to the waiter, for its component
            future.set_exception(exc)

    try:
        threading.Thread(target=run, name=f"probe-update-{name}", daemon=True).start()
    except RuntimeError:
        run()
    return _Component(future, processes)


def _outcome_by(component: _Component, deadline: float, what: str) -> object:
    """The component's result, or what it raised (an exception value, never
    raised here), or `ComponentOverdue` at `deadline` (time.monotonic()): then
    every process it started is killed with its process group, and it starts
    no more (its thread winds down on its own). An interrupt of THIS thread
    while it waits still rises."""
    future = component.future
    try:
        failure = future.exception(timeout=max(0.0, deadline - time.monotonic()))
    except FuturesTimeout:
        stopped = component.processes.stop()
        return ComponentOverdue(
            f"{what} did not finish within {_deadline_words(component_deadline())}"
            + (f" and was stopped ({stopped} process{'' if stopped == 1 else 'es'})" if stopped else "")
            + "; the next update tries again"
        )
    return failure if failure is not None else future.result()


#: Signals that end an update wherever it is (the service's SIGTERM to the
#: update's process group, a closed terminal's SIGHUP).
_ENDING_SIGNALS = tuple(
    number for number in (getattr(signal, "SIGTERM", None), getattr(signal, "SIGHUP", None)) if number is not None
)


def _exit_on_signal(number: int, _frame) -> None:
    """End the update (SystemExit 128+N) -- the next ending signal ignored
    meanwhile, so a second SIGTERM cannot cut its way out short of stopping
    every step's processes (`_stopped_with_the_update`)."""
    for each in _ENDING_SIGNALS:
        with contextlib.suppress(OSError, ValueError):
            if signal.getsignal(each) is _exit_on_signal:  # only ours: the wait puts them back
                signal.signal(each, signal.SIG_IGN)
    raise SystemExit(128 + number)


@contextmanager
def _stopped_with_the_update(components: "list[_Component]"):
    """The wait for `components`: whatever ends it early -- Ctrl-C's
    KeyboardInterrupt, the service's SIGTERM (`events._stop`'s SystemExit),
    any exception -- first stops every process they started (each runs in a
    session of its own, out of reach of a signal to this process's group),
    then rises. SIGTERM and SIGHUP that nothing here handles (a terminal
    `probe update`: their default kills at once, leaving those processes
    behind) get a handler for the wait that raises SystemExit(128+N)."""
    installed: dict = {}
    if threading.current_thread() is threading.main_thread():
        for number in _ENDING_SIGNALS:
            with contextlib.suppress(OSError, ValueError):
                if signal.getsignal(number) in (signal.SIG_DFL, None):
                    installed[number] = signal.signal(number, _exit_on_signal)
    try:
        yield
    except BaseException:
        for component in components:
            component.processes.stop()
        raise
    finally:
        for number, handler in installed.items():
            with contextlib.suppress(OSError, ValueError):
                signal.signal(number, signal.SIG_DFL if handler is None else handler)


def _stopped_detail(what: str, exc: BaseException) -> str:
    """What a component that raised says, naming the component."""
    if isinstance(exc, ComponentOverdue):
        return str(exc)
    return f"{what} stopped: {type(exc).__name__}: {exc}"
