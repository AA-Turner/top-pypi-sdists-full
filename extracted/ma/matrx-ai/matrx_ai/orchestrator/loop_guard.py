from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from matrx_ai.orchestrator.tracking import ToolCallUsage


@dataclass(frozen=True)
class LoopHealth:
    verdict: Literal["healthy", "stuck"]
    reason: str
    total_calls: int
    window_size: int
    failures_in_window: int
    successes_in_window: int


DEFAULT_MIN_CALLS_BEFORE_CHECK = 8
DEFAULT_WINDOW_SIZE = 20
DEFAULT_FAILURE_THRESHOLD = 8
DEFAULT_RECOVERY_WINDOW = 3


def evaluate_loop_health(
    history: list[ToolCallUsage],
    *,
    min_calls_before_check: int = DEFAULT_MIN_CALLS_BEFORE_CHECK,
    window_size: int = DEFAULT_WINDOW_SIZE,
    failure_threshold: int = DEFAULT_FAILURE_THRESHOLD,
    recovery_window: int = DEFAULT_RECOVERY_WINDOW,
) -> LoopHealth:
    """Decide whether the agent loop is making progress.

    Operates on per-tool-call success flags (one entry per call, not per
    iteration), so a single iteration that fired five parallel tool calls
    contributes five data points. Pure and side-effect-free — safe to call
    every iteration.

    Verdict policy:
      - Fewer than ``min_calls_before_check`` total calls so far → healthy
        (not enough data to judge).
      - If the most recent ``recovery_window`` calls are all successes →
        healthy (the model just recovered from a bad streak).
      - Otherwise, count failures in the most recent ``window_size`` calls.
        If failures ≥ ``failure_threshold`` → stuck.
      - Otherwise → healthy.
    """
    flat: list[bool] = [
        bool(detail.get("success", True))
        for usage in history
        for detail in usage.tool_calls_details
    ]

    total = len(flat)
    if total < min_calls_before_check:
        return LoopHealth(
            verdict="healthy",
            reason=f"only {total} tool calls so far (min {min_calls_before_check} before evaluation)",
            total_calls=total,
            window_size=0,
            failures_in_window=0,
            successes_in_window=0,
        )

    window = flat[-window_size:]
    failures = sum(1 for ok in window if not ok)
    successes = len(window) - failures

    if recovery_window > 0 and total >= recovery_window:
        recent = flat[-recovery_window:]
        if all(recent):
            return LoopHealth(
                verdict="healthy",
                reason=f"last {recovery_window} tool calls all succeeded — recovered",
                total_calls=total,
                window_size=len(window),
                failures_in_window=failures,
                successes_in_window=successes,
            )

    if failures >= failure_threshold:
        return LoopHealth(
            verdict="stuck",
            reason=(
                f"{failures}/{len(window)} tool calls failed in the last {len(window)} "
                f"(threshold ≥ {failure_threshold}) and recent runs did not recover"
            ),
            total_calls=total,
            window_size=len(window),
            failures_in_window=failures,
            successes_in_window=successes,
        )

    return LoopHealth(
        verdict="healthy",
        reason=f"{failures}/{len(window)} failures in window — under threshold",
        total_calls=total,
        window_size=len(window),
        failures_in_window=failures,
        successes_in_window=successes,
    )
