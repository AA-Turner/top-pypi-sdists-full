"""This Miles process's handle on the run: the driver's own run, or the run a worker joins as a `rank`
producer (`PROBE_RUN_ID` from the launcher's runtime env, or the fork's `args.probe_run_id`), with one
`run.samples` view per producer name. One attach per process; a failure warns once and records nothing."""

from __future__ import annotations

import logging
import os
import re
import threading
from typing import Any

logger = logging.getLogger(__name__)

#: The rollout executor's producer name: one per run (`RolloutExecutor`, `ray/rollout/rollout_executor.py`).
ROLLOUT = "rollout"
_UNSAFE = re.compile(r"[^A-Za-z0-9_.:\-]+")


def get_trainer_name(dp_rank: int, model_id: str | None = None) -> str:
    """`trainer-<dp>`, or `trainer-<model>-<dp>` in a multi-policy run (`trainer_model_id`)."""
    model = _UNSAFE.sub("_", model_id)[:64] if model_id else ""
    return f"trainer-{model}-{dp_rank}" if model else f"trainer-{dp_rank}"


class ProcessRun:
    """The run this process writes into, opened at most once. `get_samples(name)` is that run's samples
    written as `name`; None when Probe is off here or could not join (warned once)."""

    def __init__(self) -> None:
        self._handle: Any = None
        self._has_failed = False
        self._lock = threading.Lock()

    def get_handle(self, args: Any = None, *, producer: str = ROLLOUT) -> Any:
        if self._handle is not None or self._has_failed:
            return self._handle
        if os.environ.get("PROBE_MILES", "").strip().lower() == "off":
            return None
        with self._lock:
            if self._handle is None and not self._has_failed:
                try:
                    self._handle = _open_handle(args, producer)
                except Exception as exc:  # noqa: BLE001 -- fail open: Miles runs on without Probe
                    self._has_failed = True
                    logger.warning("Probe could not join the run from this Miles process; Miles continues: %s", exc)
        return self._handle

    def find_samples(self, producer: str) -> Any:
        """``get_samples`` only when the run is already open here: never opens it (a caller on an event loop)."""
        handle = self._handle
        return None if handle is None else handle.samples.as_producer(producer)

    def get_samples(self, producer: str, args: Any = None) -> Any:
        handle = self.get_handle(args, producer=producer)
        if handle is None:
            return None
        return handle.samples.as_producer(producer)

    def reset(self) -> None:
        """Forget the handle (tests; a process that closed its run)."""
        with self._lock:
            self._handle, self._has_failed = None, False


def _open_handle(args: Any, producer: str) -> Any:
    """The driver's bound run when this is the driver; else attach as a producer."""
    from probe.sdk.fluent.fluent import active_run

    found = active_run()
    if found is not None:
        return found
    from probe.sdk.run.samples import attach_producer

    run_id = os.environ.get("PROBE_RUN_ID", "").strip() or _get_text(getattr(args, "probe_run_id", None))
    return attach_producer(producer, run_id=run_id or None)


def _get_text(value: Any) -> str | None:
    return str(value) if value else None


#: The one handle of this process.
PROCESS = ProcessRun()
