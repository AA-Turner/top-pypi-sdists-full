"""Failure routing for generated standalone code.

``route_failure`` implements soft-failure (warn/fail-but-continue/fail) semantics:
generated Playwright test code wraps each failure_condition-bearing statement in
try/except and calls testmu.route_failure(condition, exc, label) from the
except body. Empty/None/unknown conditions fail closed (re-raise).
"""
import logging

_log = logging.getLogger("testmu")

# "Fail test immediately" (and empty/None/unknown) is the fall-through raise
# branch, so it needs no named constant of its own.
_FAIL_CONTINUE = "Fail but continue executing"
_WARN_CONTINUE = "Warn but continue executing"


def route_failure(condition, exc, label):
    """Route a caught exception according to the operation's failure_condition.

    Args:
        condition: The failure_condition string (or enum-like with .value).
                   Empty/None/unknown -> fail closed (raise).
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
        return
    # "Fail test immediately", empty string, None (normalised to ""), or unknown -> fail closed
    raise RuntimeError(f"{label}: {exc}")
