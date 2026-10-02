"""check_until_condition() — the until-loop's per-iteration condition check.

The generator emits this inside a while body: the loop keeps running while the
condition is unmet.

There is nothing to evaluate locally, deliberately unlike the selenium sibling: that
binding receives a generated Python expression over recorded `Condition` objects,
while a mobile until-condition is a natural-language statement about what is on the
screen. So the check goes through the vision_query endpoint path with
`return_type="boolean"`.

`expected_value="true"` puts the analyzer on its boolean-check branch, which
answers the condition with `"true"`/`"false"`. Without it the analyzer answers
the EXTRACTION question instead — for "the Select a Venue section is visible" it
returns `"Select a Venue"`, which reads as unmet.

A clean "no" from the model is `False` — that is the loop's normal path. Anything
that prevents the question being ANSWERED (smart off, transport failure, a
malformed body) raises instead, rather than returning False and letting the caller's
until-loop burn its whole budget.

The truthy vocabulary lives in `_return_type` and is applied by
`coerce(..., "boolean")`; this module keeps no copy of its own.
"""
import logging

from testmu_appium._helpers.vision_query import vision_query

_log = logging.getLogger("testmu_appium")


def check_until_condition(driver, condition: str, *, perception=None) -> bool:
    """Return whether the natural-language `condition` currently holds on screen.

    Args:
        driver: Live Appium driver — a fresh perception + screenshot is captured.
        condition: The recorded condition. May carry `{{var}}`/`${var}` tokens.

    Returns:
        True when the condition is satisfied, False when it is not.

    Raises:
        TestmuConfigError: TESTMU_SMART is off — there is no local evaluator.
        RuntimeError: the endpoint could not be reached or answered unusably.
    """
    met = vision_query(
        driver,
        query=condition,
        return_type="boolean",
        expected_value="true",
        description="until-condition check",
        perception=perception,
    )
    _log.info("[check_until_condition] condition=%r met=%s", str(condition)[:80], met)
    return met
