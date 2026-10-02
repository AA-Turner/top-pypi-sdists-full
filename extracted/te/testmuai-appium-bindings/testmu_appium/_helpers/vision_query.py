"""vision_query() — read a value off a screenshot of the current screen.

Posts a fresh screenshot to the analyzer's ``visual`` leg on the v16-server host
resolved by ``_config._resolve_ai_api_host()`` — the same endpoint and request
shape the web bindings use for this verb. The query is visual (colour, layout,
presence) rather than text-shaped; ``textual_query`` covers the text-shaped read.
"""
import logging

from testmu_appium import _config
from testmu_appium._errors import TestmuConfigError
from testmu_appium._helpers._analyzer_result import is_not_visible
from testmu_appium._helpers._http import auth, headers, request_with_retry
from testmu_appium._helpers._perception import capture_perception
from testmu_appium._helpers._return_type import coerce
from testmu_appium._vars import set_var, var

_log = logging.getLogger("testmu_appium")

_ENDPOINT = "/api/v1/analyzer"


def _resolve_query(query: str) -> str:
    resolved = var(query)
    return resolved if isinstance(resolved, str) else str(resolved)


def vision_query(
    driver,
    *,
    query: str,
    description: str = "",
    output_variable: str = "",
    return_type: str | None = None,
    expected_value=None,
    perception=None,
):
    """Extract a value from a fresh screenshot of the current screen.

    Request: ``POST {ai_api_host}/api/v1/analyzer`` with
    ``{"type": "visual", "query": <resolved query>, "screenshot_b64": ...}``.

    Args:
        driver: Live Appium driver — a fresh perception (incl. screenshot) is
            captured from it.
        query: Natural-language description of what to read from the screen.
            May carry ``{{var}}``/``${var}`` tokens, resolved before the request.
        description: Human-readable label for this read, carried into every
            log line for the call. DEFAULTS TO THE RESOLVED QUERY when empty,
            so every read is identifiable in the log.
        output_variable: When non-empty, the extracted value is written via
            ``set_var(output_variable, value)``.

    Returns:
        The extracted value as a string.

    Raises:
        TestmuConfigError: smart is off — this is an AI-backed read
            with no local fallback.
        ScreenshotUnavailable: The screen could not be captured. This verb reads a
            value off the PIXELS; answering from the flat entry list alone is a
            different question, not a degraded version of this one.
        RuntimeError: The endpoint responded non-200, the response body has no
            usable ``extracted_value``, or the visual analyzer abstained.
    """
    if not _config.smart_enabled():
        raise TestmuConfigError(
            "vision_query requires TESTMU_SMART=1 (AI-backed read, no local fallback)"
        )

    resolved_query = _resolve_query(query)
    # This verb requires the screenshot capture that heal's perception is allowed to
    # lose: a visual read with no pixels is a different question, not a degraded one.
    # A caller mid-loop may have ALREADY captured the screen for another use — the
    # scroll_until condition check reuses the very perception it reads movement from,
    # so the tree is not read twice per gesture. Only capture when none was handed in.
    if perception is None:
        perception = capture_perception(
            driver, include_screenshot=True, require_screenshot=True
        )
    step_description = description or resolved_query
    _log.info(
        "[vision_query] %s | query=%r entries=%d",
        step_description, resolved_query, len(perception.entries),
    )

    host = _config.resolved("ai_api_host", _config._resolve_ai_api_host)
    url = f"{host}{_ENDPOINT}"
    # The visual leg reads the pixels; a flat entry list is not part of its
    # request shape, so the capture's entries stay local to this call.
    body = {
        "type": "visual",
        "query": resolved_query,
        "screenshot_b64": perception.screenshot_b64,
    }
    if return_type is not None:
        body["return_type"] = return_type
    if expected_value is not None:
        body["expected_value"] = expected_value
    response = request_with_retry(
        "POST", url, headers=headers(), json_data=body, auth=auth(),
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"vision_query: {_ENDPOINT} returned {response.status_code}: {response.text[:500]}"
        )
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"vision_query: {_ENDPOINT} returned a non-JSON body: {response.text[:500]}"
        ) from exc
    if not isinstance(data, dict) or "extracted_value" not in data:
        raise RuntimeError(
            f"vision_query: {_ENDPOINT} response missing 'extracted_value': {data!r}"
        )

    raw = data["extracted_value"]
    if is_not_visible(raw):
        raise RuntimeError(
            "vision_query: analyzer could not extract the requested value "
            "from the current screenshot"
        )
    extracted = coerce(raw, return_type)
    _log.info("[vision_query] %s | result=%r", step_description, str(extracted)[:120])
    if output_variable:
        set_var(output_variable, extracted)
    return extracted
