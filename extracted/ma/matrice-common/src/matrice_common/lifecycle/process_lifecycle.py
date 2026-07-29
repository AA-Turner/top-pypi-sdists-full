"""Single shutdown registration point.

Replaces ad-hoc ``atexit.register`` + per-module ``signal.signal`` calls with
one ordered registry. Callbacks run once on whichever of:
    * ``atexit`` (interpreter shutdown)
    * ``SIGTERM`` (orchestrator stop)
    * ``SIGINT`` (Ctrl+C)
fires first. After running, the previous signal handler is invoked so the
default termination path still happens — we don't swallow signals.

Lower ``weight`` runs first. Use higher weights (e.g. 100) for "release
GPU last" hooks that depend on workers having stopped.
"""

from __future__ import annotations

import atexit
import logging
import signal
import threading
from typing import Callable, List, Tuple

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_callbacks: List[Tuple[int, int, Callable[[], None], str]] = []
_seq = 0
_already_ran = False
_signal_handlers_installed = False
_prev_handlers: dict = {}


def register_shutdown(
    callback: Callable[[], None],
    *,
    weight: int = 0,
    name: str = "",
) -> None:
    """Register ``callback`` to run on process shutdown.

    Args:
        callback: Zero-arg callable. Exceptions are caught and logged.
        weight: Lower runs first; ties broken by registration order.
        name: Optional label used in logs; defaults to ``callback.__qualname__``.
    """
    global _seq
    label = name or getattr(callback, "__qualname__", repr(callback))
    with _lock:
        _seq += 1
        _callbacks.append((weight, _seq, callback, label))
        _install_signal_handlers_locked()
        # atexit is idempotent for the same callable; safe to call repeatedly.
    atexit.register(_run_once)


def run_shutdown_now() -> None:
    """Run all registered callbacks immediately and clear the registry.

    Idempotent: subsequent calls are no-ops. Useful in tests and for callers
    that want to drive shutdown explicitly without waiting for atexit.
    """
    _run_once()


def _run_once() -> None:
    global _already_ran
    with _lock:
        if _already_ran:
            return
        _already_ran = True
        ordered = sorted(_callbacks, key=lambda item: (item[0], item[1]))
        _callbacks.clear()
    for _weight, _seq_, cb, label in ordered:
        try:
            cb()
        except Exception:  # noqa: BLE001 - shutdown must continue
            logger.exception("shutdown callback %s failed", label)


def _install_signal_handlers_locked() -> None:
    global _signal_handlers_installed
    if _signal_handlers_installed:
        return
    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            prev = signal.getsignal(sig)
            _prev_handlers[sig] = prev
            signal.signal(sig, _make_signal_handler(sig))
        except (OSError, ValueError):
            # Not in main thread, or signal not supported on this platform.
            # atexit still covers the normal-exit case.
            pass
    _signal_handlers_installed = True


def _make_signal_handler(sig: int):
    def _chain_or_terminate(signum, frame):
        """Run after cleanup: delegate to a prior handler or fall back to default."""
        prev = _prev_handlers.get(sig)
        if callable(prev):
            try:
                prev(signum, frame)
                return
            except Exception:  # noqa: BLE001
                logger.exception("previous signal handler for %s failed", sig)
        # Default behaviour: re-raise so the process actually terminates.
        try:
            signal.signal(sig, signal.SIG_DFL)
        except (OSError, ValueError):
            return
        try:
            signal.raise_signal(sig)
        except AttributeError:  # py3.7
            import os

            os.kill(os.getpid(), sig)

    def handler(signum, frame):
        # Always run cleanup first, then chain/terminate. Neither step is placed
        # inside a ``finally`` so that any exception from cleanup is not silently
        # discarded by a ``return`` (see Sonar python:S1143).
        try:
            _run_once()
        finally:
            _chain_or_terminate(signum, frame)

    return handler


# --- test helper -------------------------------------------------------------


def _reset_for_tests() -> None:
    """Wipe state so tests can register fresh callbacks. Not for production use."""
    global _already_ran, _signal_handlers_installed, _seq
    with _lock:
        _callbacks.clear()
        _already_ran = False
        _signal_handlers_installed = False
        _seq = 0
        for sig, prev in list(_prev_handlers.items()):
            try:
                signal.signal(sig, prev if callable(prev) else signal.SIG_DFL)
            except (OSError, ValueError):
                pass
        _prev_handlers.clear()
