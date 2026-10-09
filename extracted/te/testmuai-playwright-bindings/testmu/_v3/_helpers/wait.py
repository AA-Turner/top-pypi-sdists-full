"""Until-condition helper — check_until_condition.

Evaluates the generated condition expression locally (no vision call).
"""
import logging

_log = logging.getLogger("testmu")

_AI_API_HOST_DEFAULT = "https://kaneai-api.lambdatest.com/v16-server"


async def check_until_condition(page, condition: str) -> bool:
    """Decide whether an until-loop's exit condition is satisfied.

    ``condition`` is a Python expression produced
    by code generation — e.g. ``Condition(...).evaluate({}, get_variable_value)[0]``.
    Evaluate it locally against the runtime variable store and the bundled
    condition runtime classes, mirroring the Selenium binding
    (``testmu_selenium._helpers.wait.check_until_condition``). The generated test must
    NOT call the visual wait/check API: the condition is logical — over variables
    set by in-loop steps — not a natural-language vision query. Routing it to the
    vision endpoint returns errors and always returns False, so the loop never
    exits. A condition that cannot be evaluated (natural language, syntax error,
    unknown name) raises ConditionEvaluationError rather than returning False, so
    a never-evaluable condition fails loudly instead of silently exhausting the
    retry budget.

    Args:
        page: Playwright page object.
        condition: a Python condition expression.

    Returns:
        True if the condition is satisfied, False otherwise.
    """
    # Evaluate the generated logical condition locally (parity with
    # the Selenium binding).
    return _evaluate_v3_condition(condition)


def _evaluate_v3_condition(condition: str) -> bool:
    """Evaluate a generated until-condition expression locally.

    Mirrors ``testmu_selenium._helpers.wait.check_until_condition``: the eval
    namespace is restricted to the condition runtime classes + get_variable_value
    with no builtins, and an unevaluable expression raises ConditionEvaluationError
    rather than silently returning False.
    """
    from testmu._v3._helpers.condition import (
        Condition,
        ResolvedCondition,
        PossibleCondition,
        ConcatenationOperator,
    )
    # Assertion lives in _assertion_v3_eval (not condition.py); imported lazily
    # here to avoid a circular import at module load.
    from testmu._v3._helpers._assertion_v3_eval import Assertion
    from testmu._v3._vars import get_variable_value
    from testmu._errors import ConditionEvaluationError

    # Condition defaults to V3 semantics in this package, so a plain
    # Condition(...) already evaluates with them here — no wrapper needed.
    _log.info("    [check_until_condition v3] condition=%s", condition[:80])
    # Union of every condition-family name the producer/cgf can bake into a
    # while/until condition string (parity with the selenium binding's
    # allowed_names). Missing a bakeable name makes the eval NameError on every
    # loop. `Mathmatic` is intentionally absent: playwright has no Mathmatic
    # class — cgf emits math as `testmu.evaluate_math(...)` into a variable, so
    # the condition string references `{{var}}`, never a bare `Mathmatic(...)`.
    allowed_names = {
        "Assertion": Assertion,
        "Condition": Condition,
        "ResolvedCondition": ResolvedCondition,
        "PossibleCondition": PossibleCondition,
        "ConcatenationOperator": ConcatenationOperator,
        "get_variable_value": get_variable_value,
    }
    try:
        met = bool(eval(condition, {"__builtins__": {}}, allowed_names))
    except Exception as exc:
        _log.warning(
            "    [check_until_condition v3] could not evaluate condition %r: %s",
            condition[:120], exc,
        )
        raise ConditionEvaluationError(condition, exc) from exc
    _log.info("    [check_until_condition v3] met=%s", met)
    return met
