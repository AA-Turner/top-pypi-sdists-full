"""A try's GPU readings on the rollout side: taken off each `/generate` reply and each session's `/samples` reply
(`take_reply_trace`, `take_session_trace`), kept by attempt key once the try finishes (`GpuTraces`), and bound to
each logged sample's final key (`GpuBinding`). Why: DESIGN.md beside this file."""

from __future__ import annotations

import threading
from collections import OrderedDict
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from probe.integrations.miles.serving import GPU_FIELD

if TYPE_CHECKING:
    from .rollout import Rollout

#: Readings held across finished tries (~1 KB each: about 256 MB worst case), and tries held.
MAX_READINGS = 262_144
MAX_TRIES = 65_536
#: `extras` keys on a sample part (the server's hardware read, `app/runs/samples/hardware`).
INCOMPLETE_EXTRA, DROPPED_EXTRA, UNSUPPORTED_EXTRA = "gpu_incomplete", "gpu_dropped_readings", "gpu_unsupported"
#: `GpuUnsupported.ENGINE`: the run's engines were not launched by the run, so Probe is not inside them.
ENGINE_UNSUPPORTED = "engine"
ATTEMPT_KEY = "probe_attempt_key"


def take_reply_trace(rollout: Rollout | None, output: Any) -> None:
    """Pop the readings off a `/generate` reply (Miles never sees them) into the running try. A reply without them
    marks that try incomplete."""
    replies = output if isinstance(output, list) else [output]
    for reply in replies:
        meta = reply.get("meta_info") if isinstance(reply, Mapping) else None
        trace = meta.pop(GPU_FIELD, None) if isinstance(meta, dict) else None
        if rollout is not None:
            _add(rollout, trace)


def take_session_trace(rollout: Rollout | None, result: Any) -> None:
    """Pop the session's readings off a collected `SamplesReply` before Miles merges its metadata into the sample
    (v1, `agentic_tool_call.py:191`)."""
    metadata = getattr(result, "session_metadata", None)
    trace = metadata.pop(GPU_FIELD, None) if isinstance(metadata, dict) else None
    if rollout is not None:
        _add(rollout, trace)


def _add(rollout: Rollout, trace: Any) -> None:
    if isinstance(trace, Mapping):
        rollout.gpu.extend(trace)
    else:
        rollout.gpu.is_incomplete = True


class GpuTraces:
    """Finished tries' traces by attempt key until their samples are logged; bounded by readings, oldest first. A key
    it no longer holds (evicted, or never kept) reads as None, which a sample's binding calls incomplete."""

    def __init__(self, max_readings: int = MAX_READINGS, max_tries: int = MAX_TRIES) -> None:
        self._max_readings = max_readings
        self._max_tries = max_tries
        self._traces: OrderedDict[str, dict] = OrderedDict()
        self._readings = 0
        self._lock = threading.Lock()

    def put(self, key: str, trace: dict) -> None:
        """Keep a copy: a straggler reply after the try ended still extends the try's own list, never this one."""
        trace = {**trace, "readings": list(trace["readings"])}
        with self._lock:
            old = self._traces.pop(key, None)
            self._readings -= len(old["readings"]) if old else 0
            self._traces[key] = trace
            self._readings += len(trace["readings"])
            while self._traces and (self._readings > self._max_readings or len(self._traces) > self._max_tries):
                _, found = self._traces.popitem(last=False)
                self._readings -= len(found["readings"])

    def take(self, key: str) -> dict | None:
        """The try's trace, once; None for a try it no longer holds."""
        with self._lock:
            found = self._traces.pop(key, None)
            if found is not None:
                self._readings -= len(found["readings"])
            return found


class GpuBinding:
    """One log call's samples: each part gets its try's readings under its final key, and the extras the Compute tab
    reads. A try that became several samples (v2 leaves) gives each the same readings."""

    def __init__(self, traces: GpuTraces, *, is_engine_unsupported: bool) -> None:
        self._traces = traces
        self._is_engine_unsupported = is_engine_unsupported
        self._taken: dict[str, dict | None] = {}
        self._readings: list[tuple[str, list]] = []

    def bind(self, part: dict, sample: Any) -> None:
        extras: dict[str, Any] = {UNSUPPORTED_EXTRA: ENGINE_UNSUPPORTED} if self._is_engine_unsupported else {}
        metadata = getattr(sample, "metadata", None)
        key = metadata.get(ATTEMPT_KEY) if isinstance(metadata, Mapping) else None
        if isinstance(key, str):
            if key not in self._taken:
                self._taken[key] = self._traces.take(key)
            # A try Probe stamped but holds no trace for (evicted, or its finish never kept): incomplete, never empty.
            trace = self._taken[key] or {"readings": [], "incomplete": True}
            if trace.get("incomplete"):
                extras[INCOMPLETE_EXTRA] = True
            if trace.get("dropped"):
                extras[DROPPED_EXTRA] = int(trace["dropped"])
            if trace.get("readings"):
                self._readings.append((part["key"], trace["readings"]))
        if extras:
            part["extras"] = {**(part.get("extras") or {}), **extras}

    def send(self, writer: Any) -> None:
        """`run.samples.log_hardware(final key, readings)` for each bound part with readings."""
        for key, readings in self._readings:
            writer.log_hardware(key, readings)
