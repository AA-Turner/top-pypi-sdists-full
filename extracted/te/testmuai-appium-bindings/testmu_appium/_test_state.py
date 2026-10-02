"""Cross-step verdict state for one test run.

A `fail-continue` step swallows its exception and records it here instead. `run()`
reads the accumulated failures for the final pass/fail call and raises at session end
so CI sees a non-zero exit.

`warn-continue` deliberately does NOT touch this state — a warning is not a verdict.
"""
import logging

_log = logging.getLogger("testmu_appium")

_pending_failures: list[str] = []


def reset_test_state() -> None:
    """Clear accumulated failures. Called by run() at session start so a prior test
    in the same process cannot contaminate this one."""
    _pending_failures.clear()


def mark_step_failed(description: str, error: BaseException) -> None:
    """Record a swallowed fail-continue failure."""
    _log.error("step %r failed (on_failure=fail-continue): %s", description, error)
    _pending_failures.append(f"{description}: {error}")


def has_pending_failures() -> bool:
    return bool(_pending_failures)


def pending_failures_summary() -> str:
    """Human-readable summary used in the end-of-run RuntimeError + LT remark."""
    return "; ".join(_pending_failures)
