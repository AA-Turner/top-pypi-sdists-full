"""check_until_condition() — the until-loop's per-iteration condition check.

The generator emits this inside a while body: the loop keeps running while the
condition is unmet.

The question goes to the v16-server visibility check — the same yes/no checker
the authoring agent judges its own until-loops with — not to the analyzer's
extraction leg. Asked as an extraction with a boolean coercion, the analyzer
answers a value-shaped condition ("the quantity shows 3") with the value it
found ("3") the moment the condition holds, which coerces to False and the loop
never exits; the visibility checker answers visible/not visible with a
confidence for exactly this kind of claim.

There is nothing to evaluate locally, deliberately unlike the selenium sibling:
that binding receives a generated Python expression over recorded `Condition`
objects, while a mobile until-condition is a natural-language statement about
what is on the screen.

A clean "no" from the model is `False` — that is the loop's normal path. Anything
that prevents the question being ANSWERED (smart off, transport failure, a
malformed body) raises instead, rather than returning False and letting the caller's
until-loop burn its whole budget. A verdict the model did not actually give (no
tool call: confidence 0 and not visible) is asked once more before it counts as
"no".
"""
import logging

from testmu_appium import _config
from testmu_appium._errors import TestmuConfigError
from testmu_appium._v4._helpers._http import auth, headers, request_with_retry
from testmu_appium._v4._helpers._perception import capture_perception
from testmu_appium._v4._vars import var

_log = logging.getLogger("testmu_appium")

_ENDPOINT = "/api/v1/visibility/check"

#: How many times one check may be asked before an unanswered verdict counts as
#: "not visible".
_ASK_ATTEMPTS = 2


def _post(url: str, body: dict) -> dict:
    """One visibility call, with its failure modes named."""
    response = request_with_retry(
        "POST", url, headers=headers(), json_data=body, auth=auth(),
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"check_until_condition: {_ENDPOINT} returned {response.status_code}: "
            f"{response.text[:500]}"
        )
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"check_until_condition: {_ENDPOINT} returned a non-JSON body: "
            f"{response.text[:500]}"
        ) from exc
    if not isinstance(data, dict) or "visible" not in data:
        raise RuntimeError(
            f"check_until_condition: {_ENDPOINT} response missing 'visible': {data!r}"
        )
    return data


def _answered(data: dict) -> bool:
    """Whether the model gave a verdict at all; the server reports a missing
    tool call as not visible at confidence 0."""
    return bool(data.get("visible")) or float(data.get("confidence") or 0) > 0


def check_until_condition(driver, condition: str, *, perception=None) -> bool:
    """Return whether the natural-language `condition` currently holds on screen.

    Args:
        driver: Live Appium driver — a fresh perception + screenshot is captured
            unless ``perception`` hands one in.
        condition: The recorded condition. May carry `{{var}}`/`${var}` tokens.

    Returns:
        True when the condition is satisfied, False when it is not.

    Raises:
        TestmuConfigError: TESTMU_SMART is off — there is no local evaluator.
        RuntimeError: the endpoint could not be reached or answered unusably.
        ScreenshotUnavailable: the screen could not be captured.
    """
    if not _config.smart_enabled():
        raise TestmuConfigError(
            "check_until_condition requires TESTMU_SMART=1 (AI-backed check, "
            "no local fallback)"
        )
    resolved = var(condition)
    resolved = resolved if isinstance(resolved, str) else str(resolved)
    if perception is None:
        perception = capture_perception(
            driver, include_screenshot=True, require_screenshot=True
        )
    host = _config.resolved("ai_api_host", _config._resolve_ai_api_host)
    url = f"{host}{_ENDPOINT}"
    body = {"screenshot_b64": perception.screenshot_b64, "query": resolved}
    data: dict = {}
    for _ in range(_ASK_ATTEMPTS):
        data = _post(url, body)
        if _answered(data):
            break
    met = bool(data.get("visible"))
    _log.info(
        "[check_until_condition] condition=%r met=%s confidence=%s",
        resolved[:80], met, data.get("confidence"),
    )
    return met
