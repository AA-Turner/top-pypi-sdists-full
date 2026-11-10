"""Per-sample lifecycle events and in-flight attempts in the rollout process (RL plan §3.3c).

- `EventRecorder` sits in Miles' trajectory seam (`utils/lifecycle.py:13`, duck-typed like the dashboard's
  `TrajectorySink`, `dashboard/hooks.py:153-239`), keeps each sample's events until its hook call takes them,
  and passes every call on to the sink that was there (the dashboard's, when it is on).
- `record_sandbox_reports` turns `report_sandbox` reports (`dashboard/hooks.py:385-420`) into attempt starts
  and heartbeats: the in-flight row of the sandbox's attempt.
"""

from __future__ import annotations

import logging
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from probe.integrations.miles.samples.mapping import build_events

logger = logging.getLogger(__name__)

#: Samples whose events are held at once; the oldest go first (a sample the hook never logs).
MAX_HELD_SAMPLES = 50_000
#: Events kept per sample (`Sample.events` holds 256).
MAX_EVENTS_PER_SAMPLE = 256


class EventRecorder:
    """Miles' trajectory sink, recording by `Sample.index` and passing calls on to `inner`."""

    def __init__(self, inner: Any = None) -> None:
        self.inner = inner
        self._held: OrderedDict[int, list[dict]] = OrderedDict()
        self._lock = threading.Lock()

    # -- the seam's calls (`dashboard/hooks.py:163-197`) ---------------------------------------
    def attempt_start(self, sample) -> None:
        self._save_event("attempt_start", sample)
        self._call_inner("attempt_start", sample)

    def gen_start(self, sample) -> None:
        self._save_event("gen_start", sample)
        self._call_inner("gen_start", sample)

    def attempt_end(self, result) -> None:
        samples = result if isinstance(result, list) else [result]
        for sample in samples:
            value = (getattr(sample, "metadata", None) or {}).get("lifecycle")
            for segment in value if isinstance(value, list) else [value] if value else []:
                gap_end = segment.get("req_ts") or segment.get("t0")
                if segment.get("prev_t1") is not None and gap_end is not None:
                    self._save_event("tool_start", sample, ts=segment["prev_t1"], turn=segment.get("turn"))
                    self._save_event("tool_end", sample, ts=gap_end, turn=segment.get("turn"))
                if segment.get("t0") is not None:
                    self._save_event("gen_start", sample, ts=segment["t0"], turn=segment.get("turn"))
                self._save_event("gen_end", sample, ts=segment.get("t1"), turn=segment.get("turn"))
        if samples:
            status = getattr(samples[-1], "status", None)
            self._save_event("attempt_end", samples[-1], detail=str(getattr(status, "value", status) or ""))
        self._call_inner("attempt_end", result)

    def gen_span(self, sample, t0: float, t1: float, turn: int, detail: str = "") -> None:
        self._save_event("gen_start", sample, ts=t0, turn=turn)
        self._save_event("gen_end", sample, ts=t1, turn=turn, detail=detail)
        self._call_inner("gen_span", sample, t0, t1, turn, detail)

    def tool_span(self, sample, t0: float, t1: float, turn: int, detail: str = "") -> None:
        self._save_event("tool_start", sample, ts=t0, turn=turn, detail=detail)
        self._save_event("tool_end", sample, ts=t1, turn=turn, detail=detail)
        self._call_inner("tool_span", sample, t0, t1, turn, detail)

    def flush(self) -> None:
        self._call_inner("flush")

    # -- the hook's side -----------------------------------------------------------------------
    def take_events(self, sample_index: Any) -> list[dict]:
        """This sample's events as `SampleEvent`s, forgotten here."""
        if not isinstance(sample_index, int):
            return []
        with self._lock:
            raw = self._held.pop(sample_index, [])
        return build_events(raw)

    def _save_event(self, kind: str, sample, *, ts: float | None = None, turn: Any = None, detail: str = "") -> None:
        try:
            index = getattr(sample, "index", None)
            if not isinstance(index, int):
                return
            spans = getattr(sample, "all_weight_version_spans", None) or []
            event = {"kind": kind, "ts": time.time() if ts is None else ts, "turn": turn, "detail": detail,
                     "weight_version": getattr(spans[-1], "version", None) if spans else None}
            with self._lock:
                events = self._held.setdefault(index, [])
                if len(events) < MAX_EVENTS_PER_SAMPLE:
                    events.append(event)
                while len(self._held) > MAX_HELD_SAMPLES:
                    self._held.popitem(last=False)
        except Exception:  # noqa: BLE001 -- an event is never worth a rollout
            pass

    def _call_inner(self, name: str, *args: Any) -> None:
        call = getattr(self.inner, name, None)
        if callable(call):
            call(*args)


def install_event_recorder() -> EventRecorder | None:
    """Put an `EventRecorder` in this process's trajectory seam (upstream only: the fork has no seam).
    Kept in front of the dashboard's sink, which it calls on. None when the seam is absent."""
    try:
        from miles.utils.lifecycle import TrajectoryLifecycle
    except ImportError:
        return None
    seam = TrajectoryLifecycle()
    if isinstance(seam.sink, EventRecorder):
        return seam.sink
    seam.sink = EventRecorder(seam.sink)
    return seam.sink


def get_event_recorder() -> EventRecorder | None:
    """The recorder in this process's seam, if one is installed."""
    try:
        from miles.utils.lifecycle import TrajectoryLifecycle
    except ImportError:
        return None
    sink = TrajectoryLifecycle().sink
    return sink if isinstance(sink, EventRecorder) else None


class SandboxReports:
    """`report_sandbox` reports as attempt parts, keyed by the report's `sandbox_key`: name it after the
    attempt (a Harbor trial's `external_key`) and the finished sample merges into the same row."""

    def __init__(self, get_samples: Callable[[], Any]) -> None:
        self._get_samples = get_samples
        self._started: set[str] = set()
        self._lock = threading.Lock()

    def record(self, reports: list) -> None:
        samples = self._get_samples()
        if samples is None:
            return
        running = _get_running_try()
        for report in reports:
            key = str(getattr(report, "sandbox_key", "") or "")
            if not key:
                continue
            fields = _read_report_fields(report)
            if running is not None:
                # Made inside a live try (rl-next W36): its sandbox's news is that try's progress, never a second row.
                fields.pop("error_reason", None)
                fields.pop("error_message", None)
                samples.heartbeat(running.key, **fields)
                continue
            with self._lock:
                is_new = key not in self._started
                self._started.add(key)
            if is_new:
                task = str(getattr(report, "task", None) or key)[:512]
                samples.attempt_start(key, task_key=task, **fields)
            elif "error_reason" in fields or getattr(report, "status", None) == "finished":
                # An error or the end is news: sent now, never held behind the 30 s beat window.
                beat = {"key": key, "role": "attempt", "heartbeat_at": datetime.now(timezone.utc).isoformat(), **fields}
                samples.log([beat], role="attempt")
            else:
                samples.heartbeat(key, **fields)


def _get_running_try():
    """The live try this call runs in (`../live/`), if any."""
    from probe.integrations.miles.live import CURRENT

    return CURRENT.get()


def _read_report_fields(report) -> dict:
    """A `SandboxReport`'s facts (`dashboard/sandbox_health.py:22-33`) as attempt-part fields."""
    fields: dict[str, Any] = {}
    at = getattr(report, "ts", None)
    if isinstance(at, (int, float)):
        fields["last_command_at"] = datetime.fromtimestamp(at, tz=timezone.utc).isoformat()
    if sandbox := getattr(report, "sandbox_id", None):
        fields["sandbox_id"] = str(sandbox)[:256]
    if provider := getattr(report, "provider", None):
        fields["environment_type"] = str(provider)[:256]
    status = str(getattr(report, "status", "") or "")
    if status == "error":
        fields["error_reason"] = "sandbox"
        fields["error_message"] = str(getattr(report, "error", None) or "sandbox error")[:1024]
    if status:
        fields["extras"] = {"sandbox_status": status}
    return fields
