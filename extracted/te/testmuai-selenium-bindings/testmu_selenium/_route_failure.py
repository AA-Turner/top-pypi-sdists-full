"""Failure routing for exported standalone code.

`route_failure` mirrors the V3 runtime failure-routing helper: exported V3 selenium code
wraps each failure_condition-bearing statement in try/except and calls
testmu_selenium.route_failure(condition, exc, label) from the except body.
Empty/None/unknown conditions fail closed (re-raise).

Pending-failure accumulator: "Fail but continue executing"
records the swallowed failure into a module-level list. _session.run()
resets this list at the start of every test and, after the test body
returns cleanly, marks the LT session FAILED and raises if the list is
non-empty. Without this surfacing, every "Fail but continue" step exits
silently and the test is reported as PASSED despite failures (regression repro).
The V3 runtime helper still swallows (its comment: "V3 test-status
pending"); export-side parity is the chosen scope of this change.
"""
import logging

_log = logging.getLogger(__name__)

# "Fail test immediately" (and empty/None/unknown) is the fall-through raise
# branch, so it needs no named constant of its own.
_FAIL_CONTINUE = "Fail but continue executing"
_WARN_CONTINUE = "Warn but continue executing"


# Module-level accumulator. Populated by the FAIL_CONTINUE branch and drained
# by _session.run() via _reset_pending_failures() at start + _has_pending_failures()
# / _pending_failures_summary() after fn(driver) returns. Underscore-prefixed
# names stay private — callers go through _session.run().
_pending_failures: list[str] = []


def _reset_pending_failures() -> None:
    """Clear the pending-failure list. Called by _session.run() at start."""
    _pending_failures.clear()


def _has_pending_failures() -> bool:
    return bool(_pending_failures)


def _pending_failures_summary() -> str:
    """Human-readable summary used in the end-of-run RuntimeError + LT remark."""
    return "; ".join(_pending_failures)


def route_failure(condition, exc, label):
    """Route a caught exception according to the operation's failure_condition.

    Args:
        condition: The failure_condition string (or enum-like with .value).
                   Empty/None/unknown → fail closed (raise).
        exc:       The caught exception instance.
        label:     A human-readable description of the step (used in the error message).

    Returns:
        None when the condition swallows the exception.

    Raises:
        RuntimeError: For "Fail test immediately", empty, None, or any unknown condition.
    """
    cond = condition.value if hasattr(condition, "value") else (condition or "")
    if cond == _WARN_CONTINUE:
        _log.warning("%s: continuing after failure (warn): %s", label, exc)
        return
    if cond == _FAIL_CONTINUE:
        _log.error("%s: continuing after failure: %s", label, exc)
        _pending_failures.append(f"{label}: {exc}")
        return
    # "Fail test immediately", empty string, None (normalised to ""), or unknown → fail closed
    raise RuntimeError(f"{label}: {exc}")
