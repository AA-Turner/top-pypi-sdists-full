"""Vision wait/check helper — check_until_condition.

Smart-gated: calls the vision sidecar's visibility/check endpoint.
When smart is OFF, returns False immediately (condition not met — skip behavior).
"""
import base64
import logging

import aiohttp

from testmu._helpers._http import create_session
from testmu._helpers._screenshot import take_screenshot

from testmu import _config

_log = logging.getLogger("testmu")

_AI_API_HOST_DEFAULT = "https://kaneai-api.lambdatest.com/v16-server"


async def check_until_condition(page, condition: str) -> bool:
    """Decide whether an until-loop's exit condition is satisfied.

    When kane_version == "v3": ``condition`` is a Python expression produced
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

    Legacy path: smart-gated visual visibility/check via the vision sidecar.

    Args:
        page: Playwright page object.
        condition: When kane_version == "v3" — a Python condition expression; legacy — a natural-language
            description of the condition to check.

    Returns:
        True if the condition is satisfied, False otherwise.
    """
    import os

    # Evaluate the generated logical condition locally (parity with
    # the Selenium binding). Gated on kane_version so the legacy path keeps the vision
    # wait/check behaviour below.
    from testmu import _configure
    if _configure.get("kane_version", "v4") == "v3":
        return _evaluate_v3_condition(condition)

    if not _config.smart:
        _log.info("[check_until_condition] smart is OFF — returning False (condition skipped)")
        return False

    vision_api_host = os.getenv("TESTMU_AI_API_HOST", _AI_API_HOST_DEFAULT)

    _log.info("    [check_until_condition] condition=%s", condition[:80])

    screenshot_bytes = await take_screenshot(page)
    screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

    async with create_session() as session:
        async with session.post(
            f"{vision_api_host}/api/v1/visibility/check",
            json={"screenshot_b64": screenshot_b64, "query": condition},
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:
            if response.status == 200:
                result = await response.json()
                # Parity with the m-hps UntilBlock evaluator: missing
                # "visible" defaults to condition-met.
                met = result.get("visible", True)
                _log.info(
                    "    [check_until_condition] condition check: visible=%s, confidence=%s",
                    result.get("visible"), result.get("confidence"),
                )
                return met
            _log.info("    [check_until_condition] API error status=%d → returning False",
                      response.status)
            return False


def _evaluate_v3_condition(condition: str) -> bool:
    """Evaluate a generated until-condition expression locally.

    Mirrors ``testmu_selenium._helpers.wait.check_until_condition``: the eval
    namespace is restricted to the condition runtime classes + get_variable_value
    with no builtins, and an unevaluable expression raises ConditionEvaluationError
    rather than silently returning False.
    """
    from testmu._helpers.condition import (
        Condition,
        ResolvedCondition,
        PossibleCondition,
        ConcatenationOperator,
    )
    from testmu._vars import get_variable_value
    from testmu._errors import ConditionEvaluationError

    # The module-level Condition now defaults is_v3 from kane_version config, so a
    # plain Condition(...) already evaluates with V3 semantics here — no wrapper needed.
    _log.info("    [check_until_condition v3] condition=%s", condition[:80])
    allowed_names = {
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
