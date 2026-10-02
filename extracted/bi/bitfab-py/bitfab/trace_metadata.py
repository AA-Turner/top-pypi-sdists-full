from __future__ import annotations

import os
import threading
from dataclasses import dataclass, field
from typing import Any

from bitfab.warn_once import warn

RETAINED_COMPLETED_TRACES = 128

_lock = threading.Lock()


@dataclass
class _TraceMetadataRecord:
    caller: dict[str, Any] = field(default_factory=dict)
    derived: dict[str, Any] = field(default_factory=dict)
    warned_keys: set[str] = field(default_factory=set)


_active_records: dict[str, _TraceMetadataRecord] = {}
_completed_records: dict[str, _TraceMetadataRecord] = {}


def _reset_lock_after_fork() -> None:
    global _lock
    _lock = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_lock_after_fork)


def _find_record(trace_id: str) -> _TraceMetadataRecord | None:
    record = _active_records.get(trace_id)
    return record if record is not None else _completed_records.get(trace_id)


def record_caller_trace_metadata(trace_id: str, metadata: dict[str, Any]) -> None:
    if not isinstance(trace_id, str) or not trace_id:
        return
    if not isinstance(metadata, dict) or not metadata:
        return
    with _lock:
        record = _find_record(trace_id)
        if record is None:
            record = _TraceMetadataRecord()
            _active_records[trace_id] = record
        record.caller.update(metadata)


def caller_trace_metadata(trace_id: str) -> dict[str, Any] | None:
    with _lock:
        record = _find_record(trace_id)
        if record is None or not record.caller:
            return None
        return dict(record.caller)


def retire_trace_metadata(trace_id: str) -> None:
    with _lock:
        record = _active_records.pop(trace_id, None)
        if record is None:
            return
        _completed_records[trace_id] = record
        while len(_completed_records) > RETAINED_COMPLETED_TRACES:
            del _completed_records[next(iter(_completed_records))]


def merge_caller_metadata_into_trace_payload(
    payload: dict[str, Any],
) -> dict[str, Any]:
    external_trace = payload.get("externalTrace")
    if not isinstance(external_trace, dict):
        return payload
    trace_id = payload.get("id") or external_trace.get("id")
    if not isinstance(trace_id, str) or not trace_id:
        return payload
    exported = external_trace.get("metadata")
    with _lock:
        record = _find_record(trace_id)
        if record is None or not record.caller:
            return payload
        if isinstance(exported, dict):
            record.derived.update(exported)
        resolved = {**record.derived, **record.caller}
        shadowed = sorted(
            key
            for key, value in record.derived.items()
            if key in record.caller
            and record.caller[key] != value
            and key not in record.warned_keys
        )
        record.warned_keys.update(shadowed)
    if shadowed:
        warn(
            f"trace metadata key(s) {', '.join(shadowed)} on trace {trace_id} "
            "were set both by the caller and by an integration's own trace "
            "export; the caller's value is the one kept on the trace."
        )
    return {**payload, "externalTrace": {**external_trace, "metadata": resolved}}


def _reset_trace_metadata() -> None:
    with _lock:
        _active_records.clear()
        _completed_records.clear()
