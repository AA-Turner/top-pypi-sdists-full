"""The compute timeline from Miles' dashboard collector (`--use-miles-dashboard`, RL plan §3.3c T5), read in
the driver from the collector's append-only streams under `{dump_details}/dashboard/`
(`dashboard/store.py:63-200`): phase intervals become `phase` spans, SGLang engine series metrics with an
`engine` dimension, and the engine topology the run's config `miles_topology`."""

from __future__ import annotations

import bisect
import json
import logging
import threading
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: Streams read, each a flat `<stream>.jsonl` or hourly `<stream>/<YYYYMMDD_HH>.jsonl` files.
STREAMS = ("metrics", "phases", "engine_series", "topology")
#: An open interval's end (`PhaseEvent.OPEN_T1`): its closing event comes later.
OPEN_T1 = -1.0
#: A metric name ending here marks a rollout step in the collector's metrics stream.
STEP_KEY = "rollout/step"
#: Engine metrics are sent under this prefix.
ENGINE_PREFIX = "sglang/"


class StreamCursor:
    """Byte offsets into each stream file: complete lines only, never a producer's half-written one."""

    def __init__(self, folder: Path) -> None:
        self._folder = folder
        self._offsets: dict[Path, int] = {}

    def read_new(self, stream: str) -> list[dict]:
        records = []
        for path in [self._folder / f"{stream}.jsonl", *sorted((self._folder / stream).glob("*.jsonl"))]:
            if not path.is_file():
                continue
            offset = self._offsets.get(path, 0)
            if path.stat().st_size < offset:
                offset = 0  # rewritten
            with path.open("rb") as handle:
                handle.seek(offset)
                raw = handle.read()
            end = raw.rfind(b"\n")
            if end < 0:
                continue
            self._offsets[path] = offset + end + 1
            for line in raw[: end + 1].splitlines():
                try:
                    records.append(json.loads(line))
                except ValueError:
                    continue
        return records


class StepClock:
    """When each rollout step was logged. A phase belongs to the first step logged at or after it ended:
    the collector records no step on an interval (`PhaseEvent`, `dashboard/store.py:105-130`)."""

    def __init__(self) -> None:
        self._times: list[float] = []
        self._steps: list[int] = []

    def observe(self, record: dict) -> None:
        at, metrics = record.get("ts"), record.get("metrics") or {}
        for name, value in metrics.items():
            if name.endswith(STEP_KEY) and isinstance(value, (int, float)) and isinstance(at, (int, float)):
                index = bisect.bisect_right(self._times, at)
                self._times.insert(index, float(at))
                self._steps.insert(index, int(value))

    def find_step(self, ended_at: float) -> int | None:
        index = bisect.bisect_left(self._times, ended_at)
        return self._steps[index] if index < len(self._steps) else None

    @property
    def last_step(self) -> int | None:
        return max(self._steps) if self._steps else None


class ComputeTimeline:
    """Reads the collector's streams every ``interval`` seconds on a daemon thread and sends what is new.
    Never raises into Miles; `close()` sends the rest, a phase past the last logged step at that step."""

    def __init__(self, run: Any, dashboard_dir: Path, *, interval: float = 15.0) -> None:
        self._run = run
        self._cursor = StreamCursor(Path(dashboard_dir))
        self._clock = StepClock()
        self._pending: list[dict] = []
        self._topology: Any = None
        self._interval = max(1.0, interval)
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._run_loop, name="probe-miles-compute", daemon=True)

    def start(self) -> ComputeTimeline:
        self._thread.start()
        return self

    def close(self, timeout: float = 5.0) -> None:
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join(timeout)
        self.sync_once(is_final=True)

    def sync_once(self, *, is_final: bool = False) -> None:
        with self._lock:
            try:
                for record in self._cursor.read_new("metrics"):
                    self._clock.observe(record)
                self._pending += [p for p in self._cursor.read_new("phases") if _is_closed(p)]
                self._send_phases(is_final)
                self._send_engine_series(self._cursor.read_new("engine_series"))
                self._send_topology(self._cursor.read_new("topology"))
            except Exception:  # noqa: BLE001 -- the timeline is never worth a training step
                logger.warning("Probe could not read Miles' compute timeline; training continues", exc_info=True)

    def _run_loop(self) -> None:
        while not self._stop.wait(self._interval):
            self.sync_once()

    def _send_phases(self, is_final: bool) -> None:
        by_step: dict[int, list[dict]] = defaultdict(list)
        waiting = []
        for phase in self._pending:
            step = self._clock.find_step(float(phase.get("t1", 0)))
            if step is None and is_final:
                step = self._clock.last_step
            if step is None:
                waiting.append(phase)
            else:
                by_step[step].append(phase)
        self._pending = waiting
        for step, phases in sorted(by_step.items()):
            ordered = sorted(phases, key=lambda p: (p.get("t0", 0), str(p.get("role")), p.get("rank", -1), str(p.get("name"))))
            self._run.samples.record_phases(step, [_to_phase(p) for p in ordered])

    def _send_engine_series(self, samples: list[dict]) -> None:
        grouped: dict[tuple[float, str], dict[str, float]] = defaultdict(dict)
        for sample in samples:
            at, addr, metric, value = sample.get("ts"), sample.get("addr"), sample.get("metric"), sample.get("value")
            if isinstance(at, (int, float)) and addr and metric and isinstance(value, (int, float)):
                grouped[(float(at), str(addr))][ENGINE_PREFIX + str(metric)] = float(value)
        for (at, addr), metrics in grouped.items():
            self._run.log_hw(metrics, wall_clock=_to_iso(at), engine=addr)

    def _send_topology(self, snapshots: list[dict]) -> None:
        if not snapshots:
            return
        latest = snapshots[-1].get("engines")
        if latest is not None and latest != self._topology:
            self._topology = latest
            self._run.update_config({"miles_topology": {"engines": latest, "at": _to_iso(snapshots[-1].get("ts"))}})


def _is_closed(record: dict) -> bool:
    """A finished interval: an open one (`t1 = -1`) is superseded by its closing event."""
    t0, t1 = record.get("t0"), record.get("t1")
    return isinstance(t0, (int, float)) and isinstance(t1, (int, float)) and t1 != OPEN_T1 and t1 >= t0


def _to_phase(record: dict) -> dict:
    rank = record.get("rank")
    return {
        "name": str(record.get("name") or "phase"),
        "started_at": _to_iso(record.get("t0")),
        "ended_at": _to_iso(record.get("t1")),
        "role": record.get("role") or None,
        "rank": rank if isinstance(rank, int) and rank >= 0 else None,
        "node": record.get("node") or None,
        "gpus": [int(gpu) for gpu in record.get("gpus") or [] if isinstance(gpu, int)],
    }


def _to_iso(at: Any) -> str | None:
    return datetime.fromtimestamp(float(at), tz=timezone.utc).isoformat() if isinstance(at, (int, float)) else None


def start_compute_timeline(run: Any, args: Any) -> ComputeTimeline | None:
    """The timeline reader, when this run has a dashboard collector (`--use-miles-dashboard` with
    `--dump-details`); None otherwise."""
    dump = getattr(args, "dump_details", None)
    if not dump or not getattr(args, "use_miles_dashboard", False):
        return None
    interval = getattr(args, "probe_dashboard_interval_sec", None) or 15.0
    return ComputeTimeline(run, Path(str(dump)) / "dashboard", interval=float(interval)).start()
