from __future__ import annotations

from typing import Any

from aigie.telemetry._safe import _metric_add, _metric_record, safe_span

__all__ = [
    "judge_tracer",
    "judge_logger",
    "evaluations_counter",
    "issues_counter",
    "fixes_counter",
    "timeouts_counter",
    "latency_histogram",
    "concurrent_gauge",
    "pending_fixes_gauge",
    "safe_span",
    "_metric_add",
    "_metric_record",
]

_METER_NAME = "kytte.judge"


def _meter() -> Any:
    from aigie.telemetry import get_meter
    return get_meter(_METER_NAME)


def judge_tracer() -> Any:
    from aigie.telemetry import get_tracer
    return get_tracer("kytte.judge")


def judge_logger() -> Any:
    from aigie.telemetry import get_logger
    return get_logger("kytte.judge")


def evaluations_counter() -> Any:
    return _meter().create_counter(
        "kytte.judge.evaluations",
        description="Total judge evaluations completed",
        unit="1",
    )


def issues_counter() -> Any:
    return _meter().create_counter(
        "kytte.judge.issues_detected",
        description="Issues detected by judges",
        unit="1",
    )


def fixes_counter() -> Any:
    return _meter().create_counter(
        "kytte.judge.fixes_applied",
        description="Fix attempts by AutoFixApplicator",
        unit="1",
    )


def timeouts_counter() -> Any:
    return _meter().create_counter(
        "kytte.judge.timeouts",
        description="Judge evaluation hard timeouts",
        unit="1",
    )


def latency_histogram() -> Any:
    return _meter().create_histogram(
        "kytte.judge.latency_ms",
        description="Judge evaluation wall-clock time",
        unit="ms",
    )


def concurrent_gauge() -> Any:
    return _meter().create_up_down_counter(
        "kytte.judge.concurrent_evals",
        description="Active concurrent judge evaluations",
        unit="1",
    )


def pending_fixes_gauge() -> Any:
    return _meter().create_up_down_counter(
        "kytte.judge.pending_fixes",
        description="Pending fixes queued but not yet consumed",
        unit="1",
    )


