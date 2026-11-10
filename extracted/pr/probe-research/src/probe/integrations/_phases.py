"""A trainer's own step timers as phase spans (`run.samples.record_phases`): each timed block keeps its real start and
end until the metrics row that reports it (`<prefix><name>`) gives it a step. Shared by the verl and SkyRL adapters."""

from __future__ import annotations

import socket
import threading
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

#: Phases held between two metrics rows; past it new ones are not kept (a process that never logs).
MAX_PENDING_PHASES = 10_000
#: Who the phases belong to (`sdk/run/samples/phases.py` `Phase.role`).
ROLE = "trainer"


class PhaseClock:
    """Timed blocks since the last metrics row. ``prefix`` is how a row names a block's time (verl `timing_s/`,
    SkyRL `timing/`); ``source`` goes on each phase's attributes. Thread-safe."""

    def __init__(self, *, prefix: str, source: str) -> None:
        self._prefix = prefix
        self._source = source
        self._pending: list[dict] = []
        self._lock = threading.Lock()
        self._node = socket.gethostname()

    def record(self, name: Any, started: float, ended: float) -> None:
        with self._lock:
            if len(self._pending) >= MAX_PENDING_PHASES:
                return
            self._pending.append({"name": str(name), "started_at": _to_iso(started), "ended_at": _to_iso(ended),
                                  "role": ROLE, "node": self._node, "attributes": {"source": self._source}})

    def take_reported(self, metrics: Mapping[str, Any]) -> list[dict]:
        """The phases since the last metrics row that this row reports as `<prefix><name>` (or under their own
        name), in start order; every held phase is forgotten here. A timer the trainer never reports (a per-request
        one) is no phase."""
        with self._lock:
            phases, self._pending = self._pending, []
        reported = [phase for phase in phases
                    if self._prefix + phase["name"] in metrics or phase["name"] in metrics]
        return sorted(reported, key=lambda phase: phase["started_at"])


def _to_iso(at: float) -> str:
    return datetime.fromtimestamp(at, tz=timezone.utc).isoformat()
