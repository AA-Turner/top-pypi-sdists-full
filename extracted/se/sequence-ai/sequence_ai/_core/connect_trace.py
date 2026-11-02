"""
A robot's connect as it went, stage by stage: how long each stage took and where one that never served its first act
stopped, reported once - when that act is answered, or when the connect gives up - beside the act reports (Reporter,
`connects` of POST /v1/latency), for the platform to say a deployment's connect times and failures by stage
(`seq policy status`).


In one sentence: a connect with no worker (DirectConnection._connect, a first one or a reconnect) begins a trace → the
platform's connect answered (`gateway`, and the gateway's own `auth` and `place` when it says them), after any wait for
a worker starting (`cold_start`) or for a seat (`queue`) → the connection to the worker opened (`tcp`, `tls`), and the
stream for a policy that takes one (`stream`) → its first act answered (`first_act`): reported "ok"; a connect that
stopped is reported "failed" with the stage it stopped in and what it was told, cut as an act report's error is.

The report carries timings, counts, the stage and an error's code and cut words - never a secret, a key, a worker's
address or an observation. Thread-safe: its stages are written by the act's thread and the connection's opening thread.
"""
from __future__ import annotations

import threading
import time
import uuid
from typing import Any, Callable, Dict, Optional


STAGES = ("gateway", "auth", "place", "queue", "cold_start", "tcp", "tls", "stream", "first_act")


def _ms(seconds: float) -> float:
    return round(max(0.0, seconds) * 1000.0, 1)


class ConnectTrace:
    """One connect, from its first POST /v1/act/connect to its first act answered or its end. `report` is handed the
    report once (Reporter.record, wrapped by the caller); `reconnect`: a connect after the robot's worker went."""

    def __init__(self, report: Callable[[Dict[str, Any]], None], *, reconnect: bool = False,
                 clock: Callable[[], float] = time.monotonic, wall: Callable[[], float] = time.time) -> None:
        self._report = report
        self._clock = clock
        self._lock = threading.Lock()
        self.connect_id = uuid.uuid4().hex
        self.began = clock()
        self.at = wall()
        self.reconnect = reconnect
        self.attempts = 0
        self.stage = "gateway"
        self.stages: Dict[str, float] = {}
        self._waiting: Optional[float] = None
        self._waited_for = "cold_start"
        self.done = False

    def attempt(self) -> float:
        """A POST /v1/act/connect going out: its start."""
        with self._lock:
            self.attempts += 1
            self.stage = "gateway"
            return self._clock()

    def wait(self, *, queued: bool) -> None:
        """Its connect was answered warming (a worker starting) or queued (in line for a seat): still connecting, the
        wait counted from the first such answer."""
        with self._lock:
            if self._waiting is None:
                self._waiting = self._clock()
            self._waited_for = "queue" if queued else "cold_start"
            self.stage = self._waited_for

    def connected(self, sent_at: float, timing: Any = None) -> None:
        """The connect sent at `sent_at` answered with a worker: its round trip, the gateway's own parts of it when its
        answer says them (`timing`: auth_ms, place_ms), and the wait before it."""
        with self._lock:
            now = self._clock()
            self.stages["gateway"] = _ms(now - sent_at)
            if isinstance(timing, dict):
                for stage in ("auth", "place"):
                    said = timing.get(f"{stage}_ms")
                    if isinstance(said, (int, float)) and not isinstance(said, bool) and said >= 0:
                        self.stages[stage] = round(float(said), 1)
            if self._waiting is not None:
                self.stages[self._waited_for] = _ms(sent_at - self._waiting)
            self.stage = "tcp"

    def opened(self, *, tcp_ms: Optional[float], tls_ms: Optional[float]) -> None:
        """The connection to the worker opened - its TCP connect and TLS handshake, None for one already open."""
        with self._lock:
            for stage, ms in (("tcp", tcp_ms), ("tls", tls_ms)):
                if ms is not None and stage not in self.stages:
                    self.stages[stage] = round(float(ms), 1)
            if self.stage in ("tcp", "tls"):
                self.stage = "stream"

    def streamed(self, ms: float) -> None:
        """The stream to the worker opened, for a policy that takes one."""
        with self._lock:
            self.stages.setdefault("stream", round(float(ms), 1))
            self.stage = "first_act"

    def served(self, first_act_ms: float) -> None:
        """Its first act answered: the connect done, reported "ok"."""
        with self._lock:
            if self.done:
                return
            self.stages["first_act"] = round(max(0.0, float(first_act_ms)), 1)
            self.stage = "first_act"
            out = self._out("ok", None, None)
        self._send(out)

    def failed(self, error: Optional[Dict[str, Optional[str]]], *, stage: Optional[str] = None) -> None:
        """The connect stopped - refused, given up on, or its worker not reached - in `stage`, or the stage under way:
        reported "failed" with what it was told (reporting.error_of)."""
        with self._lock:
            if self.done:
                return
            out = self._out("failed", stage if stage in STAGES else self.stage, error)
        self._send(out)

    def dropped(self) -> None:
        """Ended with nothing to say - its robot stopped it (interrupt) or closed: never reported."""
        with self._lock:
            self.done = True

    def _out(self, outcome: str, stage: Optional[str], error: Optional[Dict[str, Optional[str]]]) -> Dict[str, Any]:
        """The report, under _lock; the trace done from here."""
        self.done = True
        out: Dict[str, Any] = {
            "connect_id": self.connect_id, "outcome": outcome, "reconnect": self.reconnect,
            "attempts": self.attempts, "at": self.at, "total_ms": _ms(self._clock() - self.began),
            "stages": {s: self.stages[s] for s in STAGES if s in self.stages}}
        if stage is not None:
            out["stage"] = stage
        if error:
            out["error"] = {k: v for k, v in error.items() if v}
        return out

    def _send(self, out: Dict[str, Any]) -> None:
        try:
            self._report(out)
        except Exception:
            pass
