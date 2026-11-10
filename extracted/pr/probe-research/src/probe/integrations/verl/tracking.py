"""`trainer.logger=['console','probe']`: verl's `Tracking` (`utils/tracking.py:39-224`) has no plugin door, only an
assert against `supported_backend` and an if-chain. `add_probe_backend` adds `probe` to that list and wraps `__init__`
and `finish` on the class, in this process only; `setup_worker` does it in every Ray worker (Ray's
`worker_process_setup_hook`). Line refs are `verl-project/verl@b17218ba58a6`. Why: DESIGN.md."""

from __future__ import annotations

import functools
import importlib
import logging
import os
import sys
from collections.abc import Mapping
from typing import Any

from .runs import NEXT_SETUP_HOOK_ENV

logger = logging.getLogger(__name__)

#: The backend name in `trainer.logger`.
BACKEND = "probe"
#: Marks the `Tracking` class Probe already taught.
TAUGHT_MARK = "__probe_verl_taught__"


class ProbeLogger:
    """The `probe` entry in `Tracking.logger`: verl calls `log(data=, step=)` on every backend (`tracking.py:192-195`);
    `finish` is called by the wrapped `Tracking.finish`."""

    def __init__(self, session: Any) -> None:
        self._session = session

    def log(self, data: Mapping[str, Any], step: Any) -> None:
        session = self._session
        session.guard.call("metrics", session.log_metrics, data, step)
        session.guard.call("the trainer hooks", session.check_hooks, data)

    def finish(self, exit_code: int = 0) -> None:
        session = self._session
        session.guard.call("the run's end", session.finish, "completed" if not exit_code else "failed")


def add_probe_backend() -> None:
    """Teach `verl.utils.tracking.Tracking` the `probe` backend, once per process, and let the fully async rollouter
    record its validation (`watch_rollouter`). Raises ImportError without verl."""
    import verl.utils.tracking as tracking

    tracker_class = tracking.Tracking
    if getattr(tracker_class, TAUGHT_MARK, False):
        return
    if isinstance(getattr(tracking, "ValidationGenerationsLogger", None), type):
        watch_rollouter(tracking.ValidationGenerationsLogger)
    if BACKEND not in tracker_class.supported_backend:
        tracker_class.supported_backend.append(BACKEND)
    original_init, original_finish = tracker_class.__init__, tracker_class.finish

    @functools.wraps(original_init)
    def __init__(self: Any, project_name: Any, experiment_name: Any, default_backend: Any = "console",
                 config: Any = None, *args: Any, **kwargs: Any) -> None:
        original_init(self, project_name, experiment_name, default_backend, config, *args, **kwargs)
        backends = [default_backend] if isinstance(default_backend, str) else list(default_backend or ())
        if BACKEND in backends:
            probe_logger = _start_logger(project_name, experiment_name, config)
            if probe_logger is not None:
                self.logger[BACKEND] = probe_logger

    @functools.wraps(original_finish)
    def finish(self: Any, exit_code: int = 0, *args: Any, **kwargs: Any) -> None:
        was_finished = getattr(self, "_finished", False)
        try:
            original_finish(self, exit_code, *args, **kwargs)
        finally:
            probe_logger = getattr(self, "logger", {}).get(BACKEND)
            if not was_finished and isinstance(probe_logger, ProbeLogger):
                probe_logger.finish(exit_code)

    tracker_class.__init__, tracker_class.finish = __init__, finish
    setattr(tracker_class, TAUGHT_MARK, True)


def watch_rollouter(logger_class: type) -> None:
    """The fully async rollouter builds no `Tracking` but builds a `ValidationGenerationsLogger` in its `__init__`
    (`fully_async_rollouter.py:369`), in its own process: the moment its session can start. The builder is the
    caller's `self`; any other builder (a trainer) starts nothing. Fails open."""
    original = logger_class.__init__

    @functools.wraps(original)
    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
        original(self, *args, **kwargs)
        try:
            from .verl import start_rollouter_session

            session = start_rollouter_session(sys._getframe(1).f_locals.get("self"))
        except Exception as exc:  # noqa: BLE001 -- fail open: the rollouter validates unrecorded
            logger.warning("Probe could not record the verl rollouter's validation; verl continues: %s", exc)
            return
        if session is not None:
            logger.info("Probe records this verl rollouter's validation samples (producer %s).",
                        session.samples.producer)

    logger_class.__init__ = __init__


def register(**init_kwargs: Any) -> None:
    """Make `trainer.logger=[..., 'probe']` work in this process (the launcher does it in every Ray worker).
    ``init_kwargs`` go to `probe.init` when this process opens its own run (`project=`, `client=`)."""
    from .verl import set_init_kwargs

    set_init_kwargs(init_kwargs)
    add_probe_backend()


def setup_worker() -> None:
    """Ray's `worker_process_setup_hook`: teach `Tracking` before verl's code runs in this worker, then run the
    job's own hook if it had one. Never raises for Probe's own failure: a Probe problem must not stop a worker."""
    try:
        add_probe_backend()
    except Exception as exc:  # noqa: BLE001 -- fail open: the worker runs without the probe backend
        logger.warning("Probe could not add its verl tracker backend in this Ray worker; verl continues: %s", exc)
    try:
        from .live import watch_agent_loop_import

        watch_agent_loop_import()  # an agent loop worker's loops are live samples (rl-next W37)
    except Exception as exc:  # noqa: BLE001 -- fail open: the loops run unrecorded
        logger.warning("Probe could not watch verl's agent loops in this Ray worker; verl continues: %s", exc)
    if next_hook := os.environ.get(NEXT_SETUP_HOOK_ENV):
        module, _, name = next_hook.rpartition(".")
        getattr(importlib.import_module(module), name)()


def _start_logger(project_name: Any, experiment_name: Any, config: Any) -> ProbeLogger | None:
    """The process's session (started by the first `probe` Tracking) wrapping the trainer classes imported here.
    Fails open with one warning; a missing project still stops the run (a setup mistake, before GPU hours)."""
    from probe.sdk.settings.settings import Mode, resolve_mode

    from .. import _rl_owner
    from .verl import start_session

    if resolve_mode(None) is Mode.DISABLED:
        return None  # PROBE_MODE=disabled: no run, no wraps, verl untouched
    guard = _rl_owner.HookGuard("verl")
    session = guard.call("the run", start_session, project_name, experiment_name, config)
    if session is None:
        return None
    session.guard.call("the trainer", session.wraps.install)
    return ProbeLogger(session)
