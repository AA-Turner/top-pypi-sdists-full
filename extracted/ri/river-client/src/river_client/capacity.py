"""Session capacity observations and quiet terminal progress hints."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import sys
import threading
import time
from typing import Literal, cast

from river_client._proto import pb2

CapacityState = Literal[
    "ready", "scaling_up", "preparing", "waiting", "at_limit", "unavailable"
]
Workload = Literal["training", "inference"]
_FRESH_SECONDS = 30.0
_HINT_DELAY_SECONDS = 5.0
_HINT_INTERVAL_SECONDS = 30.0
_STATES = {"ready", "scaling_up", "preparing", "waiting", "at_limit", "unavailable"}


@dataclass(frozen=True)
class CapacityStatus:
    """Latest capacity observation for one workload in a session's training run.

    ``capacity_wait`` is evidence of workload capacity pressure, not a diagnosis
    of an individual request's latency. ``unavailable`` is not a ready signal.
    """

    training_run_id: str
    workload: Workload
    state: CapacityState
    capacity_wait: bool
    observed_at: datetime | None


class _CapacityMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self._statuses: dict[tuple[str, str], tuple[CapacityStatus, float]] = {}
        self._candidates: dict[tuple[str, str], tuple[tuple[str, bool], float]] = {}
        self._announced: dict[tuple[str, str], tuple[str, bool]] = {}
        self._last_hint_at: dict[tuple[str, str], float] = {}
        self._next_sequence = 0
        self._accepted_sequence = -1

    def begin_heartbeat(self) -> int:
        """Order concurrent heartbeat attempts independently of observation age."""
        with self._lock:
            sequence = self._next_sequence
            self._next_sequence += 1
            return sequence

    def snapshot(self) -> tuple[CapacityStatus, ...]:
        """Expire observations even when heartbeats stop arriving."""
        now = time.monotonic()
        with self._lock:
            return tuple(
                status
                if now <= expires
                else replace(status, state="unavailable", capacity_wait=False)
                for status, expires in self._statuses.values()
            )

    def update(
        self, observations: Iterable[pb2.CapacityStatus], *, hints: bool, sequence: int
    ) -> None:
        now = time.monotonic()
        wall_now = time.time()
        statuses = {}
        for observation in observations:
            if observation.workload not in ("training", "inference"):
                continue
            observed = None
            age = float("inf")
            if observation.HasField("observed_at"):
                seconds = (
                    observation.observed_at.seconds
                    + observation.observed_at.nanos / 1e9
                )
                age = wall_now - seconds
                if -5 <= age <= _FRESH_SECONDS:
                    observed = datetime.fromtimestamp(seconds, timezone.utc)
            state = observation.state if observation.state in _STATES else "unavailable"
            if observed is None:
                state = "unavailable"
            status = CapacityStatus(
                training_run_id=observation.training_run_id,
                workload=cast(Workload, observation.workload),
                state=cast(CapacityState, state),
                capacity_wait=observation.capacity_wait and state != "unavailable",
                observed_at=observed,
            )
            statuses[(status.training_run_id, status.workload)] = (
                status,
                now + max(0, _FRESH_SECONDS - max(0, age)),
            )
        with self._lock:
            if sequence <= self._accepted_sequence:
                return
            self._accepted_sequence = sequence
            self._last_hint_at = {
                key: printed_at
                for key, printed_at in self._last_hint_at.items()
                if now - printed_at < _HINT_INTERVAL_SECONDS
            }
            for key in statuses:
                previous = self._statuses.get(key)
                if previous is not None and now > previous[1]:
                    self._candidates.pop(key, None)
                    self._announced.pop(key, None)
            self._statuses = dict(sorted(statuses.items()))
            for key in self._candidates.keys() - statuses.keys():
                del self._candidates[key]
            for key in self._announced.keys() - statuses.keys():
                del self._announced[key]
            for key, (status, expires) in self._statuses.items():
                if not hints or status.state == "unavailable" or now > expires:
                    self._candidates.pop(key, None)
                    self._announced.pop(key, None)
                    continue
                semantic = (
                    status.state,
                    status.capacity_wait
                    if status.state in ("at_limit", "ready")
                    else False,
                )
                candidate = self._candidates.get(key)
                if candidate is None or candidate[0] != semantic:
                    self._candidates[key] = (semantic, now)
                    continue
                announced = self._announced.get(key)
                if now - candidate[1] < _HINT_DELAY_SECONDS:
                    continue
                if announced == semantic or key in self._last_hint_at:
                    continue
                message = _hint(status, recovering=announced is not None)
                if message is not None:
                    try:
                        print(
                            f"[river] {status.training_run_id} · {status.workload.capitalize()}: {message}",
                            file=sys.stderr,
                            flush=True,
                        )
                    except (OSError, ValueError):
                        # A closed output stream must not break session liveness.
                        continue
                    self._announced[key] = semantic
                    self._last_hint_at[key] = now


def _hint(status: CapacityStatus, *, recovering: bool) -> str | None:
    if status.state == "scaling_up":
        return "Additional workers are preparing to handle requests."
    if status.state == "preparing":
        return "Allocated workers are preparing to process requests."
    if status.state == "waiting":
        return "Waiting for worker capacity to become available."
    if status.state == "at_limit" and status.capacity_wait:
        return "Requests are waiting for capacity; the current allocation is at its scaling limit."
    if status.state == "at_limit" and recovering:
        return "No capacity wait is currently reported; the allocation remains at its scaling limit."
    if status.state == "ready" and not status.capacity_wait and recovering:
        return "Worker capacity is ready."
    return None
