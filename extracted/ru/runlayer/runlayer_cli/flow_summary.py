"""Pure client-flow summary rendering helpers."""

from __future__ import annotations

import time
from collections.abc import Sequence
from typing import Any, Literal, Protocol

from runlayer_cli.flow_contract import MAX_STEPS_PER_FLOW


class FlowSummaryTrace(Protocol):
    @property
    def operation(self) -> str: ...

    @property
    def session_id(self) -> str | None: ...

    @property
    def error_type(self) -> str | None: ...

    @property
    def error_category(self) -> str | None: ...

    @property
    def error_http_status(self) -> int | None: ...

    @property
    def server_id(self) -> str | None: ...

    @property
    def startup_ms(self) -> float | None: ...


class StepSummaryRecord(Protocol):
    @property
    def id(self) -> int: ...

    @property
    def parent_id(self) -> int | None: ...

    @property
    def name(self) -> str: ...

    @property
    def kind(self) -> str: ...

    @property
    def blocking(self) -> bool: ...

    @property
    def start_offset_ms(self) -> float: ...

    @property
    def duration_ms(self) -> float: ...

    @property
    def status(self) -> str: ...

    @property
    def payload_bytes(self) -> int | None: ...


def merge_intervals_ms(intervals: Sequence[tuple[float, float]]) -> float:
    """Union length of ``(start, end)`` intervals (overlaps counted once)."""
    intervals = sorted(intervals)
    total = 0.0
    cur_start: float | None = None
    cur_end = 0.0
    for start, end in intervals:
        if cur_start is None:
            cur_start, cur_end = start, end
            continue
        if start <= cur_end:
            cur_end = max(cur_end, end)
        else:
            total += cur_end - cur_start
            cur_start, cur_end = start, end
    if cur_start is not None:
        total += cur_end - cur_start
    return total


def merged_blocked_ms(steps: Sequence[StepSummaryRecord]) -> float:
    """Wall-clock time during which >=1 blocking step was in flight (union)."""
    return merge_intervals_ms(
        [
            (s.start_offset_ms, s.start_offset_ms + s.duration_ms)
            for s in steps
            if s.blocking
        ]
    )


def build_summary(
    trace: FlowSummaryTrace,
    *,
    status: Literal["ok", "error"],
    steps: Sequence[StepSummaryRecord],
    wall_ms: float,
) -> dict[str, Any]:
    ordered = sorted(steps, key=lambda s: s.start_offset_ms)
    return {
        "operation": trace.operation,
        "session_id": trace.session_id,
        "status": status,
        "error_type": trace.error_type,
        # New optional fields are omitted (not null) when unset: keeps spool
        # entries lean and old backends' extra="ignore" parsing unchanged.
        # server_id: the UUID this process is running (``runlayer run`` only).
        # error_category / error_http_status: sanitized failure classification
        # (flow_contract.CLIENT_FLOW_ERROR_CATEGORIES + integer status) — never
        # free-text exception messages.
        **({"server_id": trace.server_id} if trace.server_id is not None else {}),
        **(
            {"error_category": trace.error_category}
            if trace.error_category is not None
            else {}
        ),
        **(
            {"error_http_status": trace.error_http_status}
            if trace.error_http_status is not None
            else {}
        ),
        "duration_ms": round(wall_ms, 3),
        "blocked_ms": round(merged_blocked_ms(ordered), 3),
        # Omitted (not null) when no entry path stamped the request: keeps
        # spool entries lean and old backends' extra="ignore" parsing unchanged.
        **(
            {"startup_ms": round(trace.startup_ms, 3)}
            if trace.startup_ms is not None
            else {}
        ),
        # Epoch seconds, used only client-side for spool staleness pruning;
        # never interpreted by the backend (durations are relative, so clock
        # skew is irrelevant to the metrics).
        "ts": int(time.time()),
        "steps": [
            {
                "id": s.id,
                "parent": s.parent_id,
                "name": s.name,
                "kind": s.kind,
                "status": s.status,
                "start_offset_ms": round(s.start_offset_ms, 3),
                "duration_ms": round(s.duration_ms, 3),
                # Omitted (not null) when unknown: keeps spool entries lean
                # and old backends' extra="ignore" parsing unchanged.
                **(
                    {"payload_bytes": s.payload_bytes}
                    if s.payload_bytes is not None
                    else {}
                ),
            }
            for s in ordered[:MAX_STEPS_PER_FLOW]
        ],
        "steps_truncated": len(ordered) > MAX_STEPS_PER_FLOW,
    }
