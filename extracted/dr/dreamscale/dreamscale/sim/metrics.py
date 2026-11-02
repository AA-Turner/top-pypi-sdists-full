"""Live metrics for the LIBERO simulator command."""

from __future__ import annotations

import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Any, TextIO

from dreamscale.sim.timing import (
    LIBERO_ACTION_DT_S,
    LIBERO_ACTION_HZ,
    REALTIME_DEADLINE_TOLERANCE_MS,
    RealtimeTick,
)


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = round((percentile / 100.0) * (len(ordered) - 1))
    return ordered[min(len(ordered) - 1, max(0, index))]


def _series(values: list[float]) -> dict[str, float | None]:
    return {
        "last": values[-1] if values else None,
        "p50": _percentile(values, 50.0),
        "p95": _percentile(values, 95.0),
        "max": max(values) if values else None,
    }


def _duration_ms(start_ns: int | None, end_ns: int | None) -> float | None:
    if start_ns is None or end_ns is None or end_ns < start_ns:
        return None
    return (end_ns - start_ns) / 1_000_000.0


def _int_attr(obj: Any, name: str) -> int | None:
    value = getattr(obj, name, None)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _payload_bytes(observation: Any) -> int:
    frame = getattr(observation, "frame", None)
    aggregate = getattr(frame, "aggregate_payload_bytes", None)
    if isinstance(aggregate, int):
        return aggregate
    camera_payloads = getattr(observation, "camera_payloads", None)
    if isinstance(camera_payloads, dict):
        return sum(len(payload) for payload in camera_payloads.values())
    return 0


@dataclass
class SimMetrics:
    max_steps: int
    action_hz: int = LIBERO_ACTION_HZ
    action_dt_s: float = LIBERO_ACTION_DT_S
    real_time_enabled: bool = True
    started_ns: int = field(default_factory=time.monotonic_ns)
    finished_ns: int | None = None
    steps: int = 0
    policy_calls: int = 0
    observations_sent: int = 0
    chunks_received: int = 0
    action_buffer_remaining: int = 0
    action_buffer_capacity: int = 0
    in_flight_observation_id: int | None = None
    in_flight_since_ns: int | None = None
    in_flight_elapsed_ms: float | None = None
    wait_ms_max: float = 0.0
    last_observation_id: int | None = None
    last_chunk_id: int | None = None
    last_chunk_size: int = 0
    last_payload_bytes: int = 0
    done: bool = False
    rtt_ms: list[float] = field(default_factory=list)
    server_queue_ms: list[float] = field(default_factory=list)
    server_inference_ms: list[float] = field(default_factory=list)
    server_total_ms: list[float] = field(default_factory=list)
    deadline_lateness_ms: list[float] = field(default_factory=list)
    deadline_miss_count: int = 0
    action_underrun_count: int = 0

    def start_episode(self, now_ns: int) -> None:
        self.started_ns = int(now_ns)
        self.finished_ns = None

    def note_realtime_tick(self, tick: RealtimeTick) -> None:
        self.deadline_lateness_ms.append(tick.lateness_ms)
        if tick.lateness_ms > REALTIME_DEADLINE_TOLERANCE_MS:
            self.deadline_miss_count += 1

    def note_action_underrun(self) -> None:
        self.action_underrun_count += 1

    def note_observation_sent(self, *, observation_id: int, observation: Any,
                              now_ns: int) -> None:
        self.observations_sent += 1
        self.in_flight_observation_id = observation_id
        self.in_flight_since_ns = now_ns
        self.in_flight_elapsed_ms = 0.0
        self.last_observation_id = observation_id
        self.last_payload_bytes = _payload_bytes(observation)

    def note_in_flight(self, now_ns: int) -> None:
        if self.in_flight_since_ns is None:
            return
        elapsed_ms = (now_ns - self.in_flight_since_ns) / 1_000_000.0
        self.in_flight_elapsed_ms = max(0.0, elapsed_ms)
        self.wait_ms_max = max(self.wait_ms_max, self.in_flight_elapsed_ms)

    def note_chunk_received(self, *, chunk: Any, rtt_ms: float, now_ns: int,
                            actions_added: int) -> None:
        self.note_in_flight(now_ns)
        self.rtt_ms.append(rtt_ms)
        self.chunks_received += 1
        self.policy_calls = self.chunks_received
        self.in_flight_observation_id = None
        self.in_flight_since_ns = None
        self.in_flight_elapsed_ms = None
        self.last_chunk_id = _int_attr(chunk, "chunk_id")
        self.last_observation_id = _int_attr(chunk, "generated_from_observation_id")
        self.last_chunk_size = len(getattr(chunk, "actions", ()) or ())
        self.note_buffer(actions_added, capacity=max(actions_added, self.action_buffer_capacity))
        self._note_server_timings(chunk)

    def _note_server_timings(self, chunk: Any) -> None:
        server_receive = _int_attr(chunk, "server_receive_time_ns")
        inference_start = _int_attr(chunk, "inference_start_time_ns")
        inference_end = _int_attr(chunk, "inference_end_time_ns")
        server_send = _int_attr(chunk, "server_send_time_ns")
        queue_ms = _duration_ms(server_receive, inference_start)
        inference_ms = _duration_ms(inference_start, inference_end)
        total_ms = _duration_ms(server_receive, server_send)
        if queue_ms is not None:
            self.server_queue_ms.append(queue_ms)
        if inference_ms is not None:
            self.server_inference_ms.append(inference_ms)
        if total_ms is not None:
            self.server_total_ms.append(total_ms)

    def note_buffer(self, remaining: int, *, capacity: int | None = None) -> None:
        self.action_buffer_remaining = max(0, int(remaining))
        if capacity is not None:
            self.action_buffer_capacity = max(0, int(capacity))

    def note_step(self, *, steps: int, buffer_remaining: int) -> None:
        self.steps = steps
        self.note_buffer(buffer_remaining)

    def finish(self, *, steps: int, policy_calls: int, done: bool,
               now_ns: int | None = None) -> None:
        self.steps = steps
        self.policy_calls = policy_calls
        self.done = done
        self.finished_ns = time.monotonic_ns() if now_ns is None else int(now_ns)

    def snapshot(self, now_ns: int | None = None) -> dict[str, Any]:
        now = (
            self.finished_ns
            if now_ns is None and self.finished_ns is not None
            else time.monotonic_ns() if now_ns is None else now_ns
        )
        if self.in_flight_since_ns is not None:
            self.note_in_flight(now)
        elapsed_s = max(0.0, (now - self.started_ns) / 1_000_000_000.0)
        sim_time_s = self.steps * self.action_dt_s
        return {
            "steps": self.steps,
            "max_steps": self.max_steps,
            "policy_calls": self.policy_calls,
            "observations_sent": self.observations_sent,
            "chunks_received": self.chunks_received,
            "elapsed_s": elapsed_s,
            "steps_per_s": self.steps / elapsed_s if elapsed_s > 0 else 0.0,
            "realtime": {
                "enabled": self.real_time_enabled,
                "action_hz": self.action_hz,
                "action_dt_ms": self.action_dt_s * 1000.0,
                "sim_time_s": sim_time_s,
                "wall_time_s": elapsed_s,
                "real_time_factor": sim_time_s / elapsed_s if elapsed_s > 0 else 0.0,
                "deadline_miss_count": self.deadline_miss_count,
                "deadline_lateness_ms": _series(self.deadline_lateness_ms),
                "action_underrun_count": self.action_underrun_count,
            },
            "rtt_ms": _series(self.rtt_ms),
            "server_queue_ms": _series(self.server_queue_ms),
            "server_inference_ms": _series(self.server_inference_ms),
            "server_total_ms": _series(self.server_total_ms),
            "action_buffer": {
                "remaining": self.action_buffer_remaining,
                "capacity": self.action_buffer_capacity,
                "health": self.buffer_health,
            },
            "in_flight": {
                "observation_id": self.in_flight_observation_id,
                "elapsed_ms": self.in_flight_elapsed_ms,
            } if self.in_flight_observation_id is not None else None,
            "last": {
                "observation_id": self.last_observation_id,
                "chunk_id": self.last_chunk_id,
                "chunk_size": self.last_chunk_size,
                "payload_bytes": self.last_payload_bytes,
            },
            "wait_ms_max": self.wait_ms_max,
            "done": self.done,
        }

    @property
    def buffer_health(self) -> str:
        if self.in_flight_observation_id is not None:
            return "waiting"
        if self.action_buffer_capacity <= 0 or self.action_buffer_remaining <= 0:
            return "empty"
        if self.action_buffer_remaining <= max(1, self.action_buffer_capacity // 4):
            return "low"
        return "ok"


def _fmt_ms(value: float | None) -> str:
    return "--" if value is None else f"{value:6.1f}"


def _fmt_int(value: int | None) -> str:
    return "--" if value is None else str(value)


def _fmt_kb(value: int) -> str:
    if value <= 0:
        return "--"
    return f"{value / 1024.0:.1f} KB"


def format_sim_metrics(snapshot: dict[str, Any]) -> str:
    rtt = snapshot["rtt_ms"]
    queue = snapshot["server_queue_ms"]
    inference = snapshot["server_inference_ms"]
    server_total = snapshot["server_total_ms"]
    buffer = snapshot["action_buffer"]
    realtime = snapshot["realtime"]
    in_flight = snapshot["in_flight"]
    last = snapshot["last"]
    current_wait = in_flight["elapsed_ms"] if in_flight is not None else None
    return "\n".join((
        "Dreamscale sim metrics",
        (
            f"step {snapshot['steps']:>4}/{snapshot['max_steps']:<4} | "
            f"policy calls {snapshot['policy_calls']:<3} | "
            f"chunks {snapshot['chunks_received']:<3} | "
            f"rate {snapshot['steps_per_s']:>5.1f} step/s"
        ),
        (
            "rtt_ms send->chunk "
            f"last {_fmt_ms(rtt['last'])} | p50 {_fmt_ms(rtt['p50'])} | "
            f"p95 {_fmt_ms(rtt['p95'])} | max {_fmt_ms(rtt['max'])}"
        ),
        (
            "worker_ms          "
            f"queue {_fmt_ms(queue['last'])} | infer {_fmt_ms(inference['last'])} | "
            f"server {_fmt_ms(server_total['last'])}"
        ),
        (
            f"action buffer      {buffer['remaining']:>2}/{buffer['capacity']:<2} "
            f"{buffer['health']:<7} | wait {_fmt_ms(current_wait)} | "
            f"max wait {_fmt_ms(snapshot['wait_ms_max'])}"
        ),
        (
            "realtime          "
            f"sim {realtime['sim_time_s']:>4.1f}s | wall {realtime['wall_time_s']:>4.1f}s | "
            f"factor {realtime['real_time_factor']:>4.2f}x | "
            f"late {realtime['deadline_miss_count']} | "
            f"underrun {realtime['action_underrun_count']}"
        ),
        (
            f"last chunk         id {_fmt_int(last['chunk_id'])} <- "
            f"obs {_fmt_int(last['observation_id'])} | size {last['chunk_size']:<2} | "
            f"payload {_fmt_kb(last['payload_bytes'])}"
        ),
    ))


class SimMetricsTui:
    def __init__(self, *, enabled: bool = True, stream: TextIO | None = None,
                 min_interval_s: float = 0.1) -> None:
        self._stream = stream or sys.stdout
        self._enabled = enabled and self._stream.isatty()
        self._min_interval_s = min_interval_s
        self._last_render_s = 0.0
        self._line_count = 0
        self._lock = threading.Lock()
        self._cursor_hidden = False

    @property
    def enabled(self) -> bool:
        return self._enabled

    def render(self, metrics: SimMetrics, *, force: bool = False) -> None:
        if not self._enabled:
            return
        now_s = time.monotonic()
        if not force and now_s - self._last_render_s < self._min_interval_s:
            return
        panel = format_sim_metrics(metrics.snapshot()).splitlines()
        with self._lock:
            if not self._cursor_hidden:
                self._stream.write("\x1b[?25l")
                self._cursor_hidden = True
            if self._line_count:
                self._stream.write(f"\x1b[{self._line_count}F")
            for line in panel:
                self._stream.write(f"\x1b[2K{line}\n")
            for _ in range(max(0, self._line_count - len(panel))):
                self._stream.write("\x1b[2K\n")
            self._line_count = len(panel)
            self._last_render_s = now_s
            self._stream.flush()

    def close(self) -> None:
        if not self._enabled:
            return
        with self._lock:
            if self._cursor_hidden:
                self._stream.write("\x1b[?25h")
                self._stream.flush()
                self._cursor_hidden = False
