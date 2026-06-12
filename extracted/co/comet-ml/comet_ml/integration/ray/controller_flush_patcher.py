# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
"""Flush controller-side Comet experiments before Ray tears the controller down.

On Ray Train V2 the ``CometTrainLoggerCallback`` hooks run inside the **Train
controller process**, which Ray hard-kills once the run finishes — without
running Python ``atexit``/``Experiment._on_end``. Anything the controller logged
that the background streamer has not yet delivered is then lost. Metrics are
re-sent every report so they survive, but **asynchronous artifact/checkpoint
uploads** logged from ``after_report`` can be cut off mid-flight and land as
empty (0-byte) artifact versions.

Ray Train V2 gives a ``UserCallback`` no run-completion hook, and the controller
runs as a Ray actor whose class is reconstructed from a serialized definition —
so patching the module-level ``TrainController`` class at import time has no
effect on the class the actor actually dispatches on. Instead we patch at
**runtime, from inside a controller-side hook** (``after_report``): the running
controller instance is on the call stack, so we locate it and wrap *its* class's
``_shutdown`` (which runs on the normal completion path, before the kill) to
flush the registered experiments first. This makes no assumption about Ray's
serialization, and **fails safe** — if the controller can't be located (e.g. Ray
changed its internals) it does nothing, leaving behaviour as it was before this
patcher. Regression is caught by the test suite, not by user-facing warnings.
"""
import functools
import inspect
import logging
import weakref
from typing import Any

LOGGER = logging.getLogger(__name__)

# Experiments to flush at controller shutdown. WeakSet: the owning callback holds
# the strong reference, so ended/collected experiments drop out on their own.
_experiments: "weakref.WeakSet[Any]" = weakref.WeakSet()

# Once we have wrapped a controller's ``_shutdown`` in this process we stop
# walking the stack on every report.
_installed = False


def _looks_like_controller(obj: Any) -> bool:
    """Duck-type the Ray Train V2 controller.

    We deliberately avoid ``isinstance`` against an imported ``TrainController``:
    the actor's class is a deserialized copy, so the identity check can fail.
    These two methods are the ones we depend on (``_shutdown`` is what we wrap,
    ``_poll_workers`` distinguishes the controller from the worker group / report
    handler that also appear on the stack).
    """
    return (
        obj is not None and hasattr(obj, "_shutdown") and hasattr(obj, "_poll_workers")
    )


def _flush_experiments() -> None:
    for experiment in list(_experiments):
        try:
            experiment.flush()
        except Exception:
            # Non-actionable for the user; tests cover the mechanism.
            LOGGER.debug(
                "Comet: failed to flush experiment before Ray controller shutdown",
                exc_info=True,
            )


def _wrap_controller_shutdown(controller_cls: type) -> None:
    # ``_shutdown`` is a private Ray method we attach a marker attribute to and
    # replace on the class; mypy can't know either, hence the targeted ignores.
    original = controller_cls._shutdown  # type: ignore[attr-defined]
    if getattr(original, "_comet_flush_wrapped", False):
        return

    if inspect.iscoroutinefunction(original):

        @functools.wraps(original)
        async def _shutdown(
            self: Any, *args: Any, _original: Any = original, **kwargs: Any
        ) -> Any:
            _flush_experiments()
            return await _original(self, *args, **kwargs)

    else:  # defensive: tolerate a future synchronous _shutdown

        @functools.wraps(original)
        def _shutdown(
            self: Any, *args: Any, _original: Any = original, **kwargs: Any
        ) -> Any:
            _flush_experiments()
            return _original(self, *args, **kwargs)

    _shutdown._comet_flush_wrapped = True  # type: ignore[attr-defined]
    controller_cls._shutdown = _shutdown  # type: ignore[attr-defined]


def ensure_drain(experiment: Any) -> bool:
    """Register ``experiment`` to be flushed at controller shutdown, wrapping the
    live controller's ``_shutdown`` the first time it is found.

    Must be called from within a controller-side callback hook (e.g.
    ``after_report``) so the running controller instance is on the call stack.
    Returns ``True`` if the controller-shutdown drain is active.
    """
    if experiment is not None:
        _experiments.add(experiment)

    global _installed
    if _installed:
        return True

    try:
        stack = inspect.stack()
        try:
            for frame_info in stack:
                candidate = frame_info.frame.f_locals.get("self")
                if _looks_like_controller(candidate):
                    _wrap_controller_shutdown(type(candidate))
                    _installed = True
                    LOGGER.debug(
                        "Comet: installed controller-shutdown flush on %s",
                        type(candidate).__name__,
                    )
                    return True
        finally:
            # Drop references to frames promptly (inspect docs warn about cycles).
            del stack
    except Exception:
        # Non-actionable for the user; tests cover the mechanism.
        LOGGER.debug(
            "Comet: error while installing the Ray controller-shutdown flush",
            exc_info=True,
        )
        return False

    # Could not find the controller on the stack — Ray internals likely changed.
    # Stay silent for users (no action they can take); the regression test is the
    # signal that this needs updating.
    LOGGER.debug(
        "Comet: could not locate the Ray Train controller on the call stack; "
        "controller-shutdown flush not installed"
    )
    return False
