"""Failure routing for exported standalone code.

Exported code wraps each failure_condition-bearing statement in try/except and calls
testmu_appium.route_failure(condition, exc, label) from the except body.
Empty/None/unknown conditions fail closed (re-raise).

"Fail but continue executing" records the swallowed failure into `_test_state`, the
same accumulator `step(on_failure="fail-continue")` writes and `run()` drains. There is
exactly one verdict accumulator per test, and this module keeps none of its own.

That is an intentional divergence from the canonical selenium copy
(`selenium-python/testmu_selenium/_route_failure.py`), which keeps a module-local list
because that binding surfaces the end-of-test verdict its own way.
"""
import logging

from testmu_appium._test_state import mark_step_failed

_log = logging.getLogger(__name__)

# "Fail test immediately" (and empty/None/unknown) is the fall-through raise
# branch, so it needs no named constant of its own. Both vocabularies are
# accepted: the legacy long enum strings recorded by V2/V3 blobs, and the
# canonical short tokens the Appium code generator normalises to (the same
# pair step(on_failure=...) accepts) — the generator emits the short form.
_FAIL_CONTINUE_TOKENS = frozenset(("Fail but continue executing", "fail-continue"))
_WARN_CONTINUE_TOKENS = frozenset(("Warn but continue executing", "warn-continue"))


def route_failure(condition, exc, label):
    """Route a caught exception according to the operation's failure_condition.

    Args:
        condition: The failure_condition string (or enum-like with .value).
                   Accepts the legacy long enum strings and the canonical
                   short tokens ("fail-continue"/"warn-continue").
                   Empty/None/unknown → fail closed (raise).
        exc:       The caught exception instance.
        label:     A human-readable description of the step (used in the error message).

    Returns:
        None when the condition swallows the exception.

    Raises:
        RuntimeError: For "Fail test immediately", empty, None, or any unknown condition.
    """
    cond = condition.value if hasattr(condition, "value") else (condition or "")
    if cond in _WARN_CONTINUE_TOKENS:
        _log.warning("%s: continuing after failure (warn): %s", label, exc)
        return
    if cond in _FAIL_CONTINUE_TOKENS:
        mark_step_failed(label, exc)
        return
    # "Fail test immediately", empty string, None (normalised to ""), or unknown → fail closed
    raise RuntimeError(f"{label}: {exc}")
