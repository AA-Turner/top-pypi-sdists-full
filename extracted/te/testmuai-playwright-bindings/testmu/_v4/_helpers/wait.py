"""Vision wait/check helper — check_until_condition.

Smart-gated: calls the vision sidecar's visibility/check endpoint.
When smart is OFF, returns False immediately (condition not met — skip behavior).
"""
import base64
import logging

import aiohttp

from testmu._v4._helpers._http import create_session
from testmu._v4._helpers._screenshot import take_screenshot

from testmu import _config

_log = logging.getLogger("testmu")

_AI_API_HOST_DEFAULT = "https://kaneai-api.lambdatest.com/v16-server"


async def check_until_condition(page, condition: str) -> bool:
    """Decide whether an until-loop's exit condition is satisfied.

    Smart-gated visual check: the vision sidecar's visibility/check endpoint
    decides whether ``condition`` (a natural-language description) holds. With
    smart OFF it returns False (condition skipped).

    Args:
        page: Playwright page object.
        condition: natural-language description of the condition to check.

    Returns:
        True if the condition is satisfied, False otherwise.
    """
    import os


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


