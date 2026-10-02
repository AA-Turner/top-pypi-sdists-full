from __future__ import annotations

import contextlib
import logging
import signal
import sys
import threading
from collections.abc import Callable, Iterator
from typing import Any, Literal, NamedTuple, TypedDict

logger = logging.getLogger(__name__)

ReplayInterruptSignal = Literal["SIGINT", "SIGTERM"]

_SIGNAL_NAMES: dict[int, ReplayInterruptSignal] = {
    signal.SIGINT: "SIGINT",
    signal.SIGTERM: "SIGTERM",
}


class ReplayInterrupt(TypedDict):
    experiment_id: str
    experiment_url: str
    signal: ReplayInterruptSignal
    marked_interrupted: bool


Interrupt = Callable[[ReplayInterruptSignal | None], None]
Interrupted = Callable[[], bool]


class ReplayInterruptHandlers(NamedTuple):
    interrupted: Interrupted
    remove: Callable[[], None]


def describe_replay_interrupt(experiment_id: str, marked_interrupted: bool) -> str:
    if marked_interrupted:
        return f"[replay] Experiment {experiment_id} interrupted."
    return (
        f"[replay] Experiment {experiment_id} stopped, but Bitfab could not mark it "
        "interrupted. It will be marked interrupted within 15 minutes. A resume in "
        "the next two minutes may be refused as still running."
    )


def _send_interrupt(experiment_id: str, send_interrupt: Callable[[], bool]) -> bool:
    try:
        return send_interrupt()
    except Exception:
        logger.debug(
            "Bitfab: could not mark replay experiment %s interrupted",
            experiment_id,
            exc_info=True,
        )
        return False


def _interrupter(
    experiment_id: str,
    experiment_url: str,
    send_interrupt: Callable[[], bool],
    on_interrupt: Callable[[ReplayInterrupt], None] | None,
) -> tuple[Interrupt, Interrupted]:
    sent = False

    def interrupt(signal_name: ReplayInterruptSignal | None) -> None:
        nonlocal sent
        if sent:
            return
        sent = True
        marked_interrupted = _send_interrupt(experiment_id, send_interrupt)
        if signal_name is None:
            return
        if on_interrupt is None:
            print(
                describe_replay_interrupt(experiment_id, marked_interrupted),
                file=sys.stderr,
            )
            return
        try:
            on_interrupt(
                ReplayInterrupt(
                    experiment_id=experiment_id,
                    experiment_url=experiment_url,
                    signal=signal_name,
                    marked_interrupted=marked_interrupted,
                )
            )
        except Exception:
            logger.error("Bitfab: replay on_interrupt callback raised", exc_info=True)

    def interrupted() -> bool:
        return sent

    return interrupt, interrupted


def _chain_to_previous_handler(
    interrupt: Interrupt, previous: Any
) -> Callable[[int, Any], None]:
    def handle(signum: int, frame: Any) -> None:
        interrupt(_SIGNAL_NAMES[signum])
        if callable(previous):
            previous(signum, frame)
            return
        signal.signal(signum, signal.SIG_DFL)
        signal.raise_signal(signum)

    return handle


def _install_handlers(interrupt: Interrupt) -> Callable[[], None]:
    if threading.current_thread() is not threading.main_thread():
        return lambda: None
    installed: dict[int, Any] = {}
    for signum in _SIGNAL_NAMES:
        previous = signal.getsignal(signum)
        if previous in (None, signal.SIG_IGN, signal.default_int_handler):
            continue
        try:
            signal.signal(signum, _chain_to_previous_handler(interrupt, previous))
        except (ValueError, OSError):
            continue
        installed[signum] = previous

    def restore() -> None:
        for signum, previous in installed.items():
            signal.signal(signum, previous)

    return restore


@contextlib.contextmanager
def interrupt_replay_on_early_exit(
    experiment_id: str,
    experiment_url: str,
    send_interrupt: Callable[[], bool],
    on_interrupt: Callable[[ReplayInterrupt], None] | None,
) -> Iterator[ReplayInterruptHandlers]:
    interrupt, interrupted = _interrupter(
        experiment_id, experiment_url, send_interrupt, on_interrupt
    )
    restore_handlers = _install_handlers(interrupt)
    watching_signals = True

    def remove() -> None:
        nonlocal watching_signals
        watching_signals = False
        restore_handlers()

    try:
        yield ReplayInterruptHandlers(interrupted=interrupted, remove=remove)
    except KeyboardInterrupt:
        if watching_signals:
            interrupt("SIGINT")
        raise
    except BaseException:
        interrupt(None)
        raise
    finally:
        remove()
