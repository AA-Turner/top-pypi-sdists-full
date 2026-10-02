"""verify_assertion() — evaluate a recorded AssertionAction.assertion_tree.

The tree is the shape the code generator records:

    {"claim": "the total is right",
     "composite_operator": "and",
     "sub_checks": [{"description", "extracted_value", "expected_value",
                     "operator", "transforms", "json_path"}, ...]}

Evaluation routes through the same local core `assertion()` uses, so both entry
points agree on operator semantics including the mobile `json_*` family. There is
no network call: unlike the web siblings' visual path, a native mobile session has
no screenshot-assertion endpoint to fall back to, so an assertion is exactly as
good as the values recorded into its sub_checks.

`return_result=True` returns the verdict instead of raising — for the generated
shapes that feed an assertion result into a variable or a branch rather than
letting it fail the step.
"""
import logging

from testmu_appium._helpers.assertion import _failure_summary, _resolve_sub_checks
from testmu_appium._evaluation._mobile_operators import evaluate_sub_checks

_log = logging.getLogger("testmu_appium")


def verify_assertion(
    driver,
    *,
    tree: dict,
    description: str = "",
    return_result: bool = False,
) -> dict:
    """Evaluate a recorded assertion tree.

    Args:
        driver: Accepted for verb-interface parity; unused — evaluation is local.
        tree: AssertionAction.assertion_tree.
        description: Step description (logging only).
        return_result: Return the verdict instead of raising when it failed.

    Returns:
        `{"status", "composite_operator", "sub_results"}`.

    Raises:
        ValueError: the tree is missing or carries no sub_checks — an assertion
            with nothing to check would otherwise pass vacuously.
        AssertionError: the assertion failed and `return_result` is False.
    """
    if not isinstance(tree, dict):
        raise ValueError(f"verify_assertion requires an assertion_tree dict, got {tree!r}")

    sub_checks = tree.get("sub_checks")
    if not sub_checks:
        raise ValueError(
            "assertion_tree carries no sub_checks; an assertion with nothing to "
            "check would pass vacuously"
        )

    claim = tree.get("claim", "") or ""
    composite_operator = tree.get("composite_operator", "and") or "and"

    result = evaluate_sub_checks(claim, composite_operator, _resolve_sub_checks(sub_checks))
    _log.info(
        "[verify_assertion] claim=%r composite_operator=%s status=%s",
        claim, composite_operator, result["status"],
    )

    if result["status"] == "failed" and not return_result:
        raise AssertionError(_failure_summary(claim, result))
    return result
