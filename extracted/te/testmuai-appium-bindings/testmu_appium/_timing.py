"""Opt-in, per-action timing capture for host runtimes.

The binding does not log these measurements by itself.  A host that needs
diagnostics installs :func:`capture_action_timings` around generated code and
receives plain dictionaries when binding actions finish.  With no capture
context, the helpers below are intentionally close to no-ops.
"""

from __future__ import annotations

import time
from collections import defaultdict
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator


_captured: ContextVar[list[dict] | None] = ContextVar(
    "testmu_appium_captured_action_timings", default=None
)
_active: ContextVar[dict | None] = ContextVar(
    "testmu_appium_active_action_timing", default=None
)


@contextmanager
def capture_action_timings() -> Iterator[list[dict]]:
    """Collect binding action timings executed within this context.

    The returned list is populated as actions complete, including actions that
    raise.  Context-local storage keeps concurrent sessions isolated and avoids
    a process-global callback that one runner could accidentally leave behind.
    """
    timings: list[dict] = []
    token = _captured.set(timings)
    try:
        yield timings
    finally:
        _captured.reset(token)


@contextmanager
def action_timing(
    action_type: str,
    *,
    target_mode: str,
    surface: str = "native",
    grounded_by: str = "",
) -> Iterator[dict | None]:
    """Start one binding-owned action measurement when capture is enabled."""
    sink = _captured.get()
    if sink is None:
        yield None
        return

    trace = {
        "action_type": action_type or "action",
        "target_mode": target_mode,
        "surface": surface,
        "grounded_by": grounded_by or "unspecified",
        "route": "",
        "outcome": "success",
        "phases_ms": defaultdict(float),
        "action_phases_ms": defaultdict(float),
        "counts": defaultdict(int),
    }
    started_ns = time.perf_counter_ns()
    token = _active.set(trace)
    try:
        yield trace
    except BaseException as exc:
        trace["outcome"] = "error"
        trace["error_type"] = type(exc).__name__
        raise
    finally:
        trace["total_ms"] = round((time.perf_counter_ns() - started_ns) / 1_000_000, 2)
        trace["phases_ms"] = {
            name: round(value, 2)
            for name, value in trace["phases_ms"].items()
            if value >= 0
        }
        trace["action_phases_ms"] = {
            name: round(value, 2)
            for name, value in trace["action_phases_ms"].items()
            if value >= 0
        }
        trace["counts"] = dict(trace["counts"])
        sink.append(trace)
        _active.reset(token)


@contextmanager
def phase(name: str) -> Iterator[None]:
    """Accumulate one non-exclusive phase on the active action trace."""
    trace = _active.get()
    if trace is None:
        yield
        return
    started_ns = time.perf_counter_ns()
    try:
        yield
    finally:
        trace["phases_ms"][name] += (
            time.perf_counter_ns() - started_ns
        ) / 1_000_000


@contextmanager
def action_phase(name: str) -> Iterator[None]:
    """Break down the aggregate ``device_action`` phase into verb commands."""
    trace = _active.get()
    if trace is None:
        yield
        return
    started_ns = time.perf_counter_ns()
    try:
        yield
    finally:
        trace["action_phases_ms"][name] += (
            time.perf_counter_ns() - started_ns
        ) / 1_000_000


def count(name: str, amount: int = 1) -> None:
    """Increment a diagnostic counter on the active trace, if any."""
    trace = _active.get()
    if trace is not None:
        trace["counts"][name] += amount


def set_route(route: str) -> None:
    """Record which execution path ultimately acted on the target."""
    trace = _active.get()
    if trace is not None:
        trace["route"] = route


def set_detail(name: str, value: str) -> None:
    """Attach a non-sensitive categorical detail to the active trace."""
    trace = _active.get()
    if trace is not None:
        trace[name] = value
