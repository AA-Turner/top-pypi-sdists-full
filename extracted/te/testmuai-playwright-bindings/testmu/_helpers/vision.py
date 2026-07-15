"""Vision helpers — query, textual query, wait, action, and coordinate lookup.

All five functions are smart-gated: when _config.smart is OFF they return
safe fallbacks immediately without touching any network endpoint.

When smart is ON, they call the analyzer sidecar via aiohttp.

Analyzer base URL is read from TESTMU_AI_API_HOST env var
(default: http://localhost:8000).
"""

import asyncio
import base64
import io
import logging
import os

import aiohttp

try:
    from PIL import Image  # type: ignore
except ImportError:  # pragma: no cover - Pillow is a declared dependency
    Image = None  # type: ignore[assignment]

from testmu import _config
from testmu._helpers._http import create_session
from testmu._helpers._screenshot import take_screenshot
from testmu._helpers._dom_capture import (
    build_flat_dom as _build_flat_dom,
    get_element_snapshot as _get_element_snapshot,
)

_log = logging.getLogger("testmu")

_VISION_API_HOST = os.getenv("TESTMU_AI_API_HOST", "https://kaneai-api.lambdatest.com/v16-server")
_ANALYZER_URL = f"{_VISION_API_HOST}/api/v1/analyzer"
_ANALYZER_TIMEOUT = aiohttp.ClientTimeout(total=120)
_QUERY_TIMEOUT = aiohttp.ClientTimeout(total=60)

_WAIT_MAX_RETRIES = 5
_WAIT_RETRY_INTERVAL = 2  # seconds

_COORD_MAX_RETRIES = 10
_COORD_RETRY_INTERVAL = 1  # seconds


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


async def _post_analyzer(
    session: aiohttp.ClientSession, body: dict, timeout=None
) -> dict:
    """POST to the analyzer endpoint and return parsed JSON."""
    t = timeout or _ANALYZER_TIMEOUT
    async with session.post(_ANALYZER_URL, json=body, timeout=t) as resp:
        if resp.status != 200:
            text = await resp.text()
            raise Exception(f"Analyzer API error {resp.status}: {text}")
        return await resp.json()


async def _derive_if_recorded(page, code_js: str | None, value):
    """Recompute a recorded derivation over a freshly extracted raw value.

    No code_js — or an empty one — means the recording had nothing to derive:
    the raw value IS the operand.
    """
    if not code_js:
        return value
    from testmu._helpers.derive import derive

    return await derive(page, code_js, str(value))


async def _check_wait_condition(
    session: aiohttp.ClientSession, screenshot_b64: str, query: str
) -> dict:
    async with session.post(
        f"{_VISION_API_HOST}/api/v1/wait/check",
        json={"screenshot_b64": screenshot_b64, "query": query},
        timeout=aiohttp.ClientTimeout(total=30),
    ) as resp:
        if resp.status == 200:
            return await resp.json()
        raise Exception(f"Wait API error: {resp.status}")


async def _check_visibility(
    session: aiohttp.ClientSession, screenshot_b64: str, query: str
) -> dict:
    async with session.post(
        f"{_VISION_API_HOST}/api/v1/visibility/check",
        json={"screenshot_b64": screenshot_b64, "query": query},
        timeout=aiohttp.ClientTimeout(total=30),
    ) as resp:
        if resp.status == 200:
            return await resp.json()
        raise Exception(f"Visibility API error: {resp.status}")


async def _wait_for_visibility(page, query: str, opts: dict = None) -> str:
    """Poll visibility API until element is visible; return the last screenshot_b64.

    opts keys (all optional):
        max_retries (int):     defaults to _COORD_MAX_RETRIES
        retry_interval (int):  seconds between attempts, defaults to _COORD_RETRY_INTERVAL
        should_raise (bool):   when False, return the last screenshot_b64 instead of
                               raising on exhaustion. Defaults to True.
    """
    opts = opts or {}
    max_retries = opts.get("max_retries", _COORD_MAX_RETRIES)
    retry_interval = opts.get("retry_interval", _COORD_RETRY_INTERVAL)
    should_raise = opts.get("should_raise", True)

    last_reasoning = None
    last_screenshot_b64 = None
    async with create_session() as session:
        for attempt in range(1, max_retries + 1):
            screenshot_bytes = await take_screenshot(page)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            last_screenshot_b64 = screenshot_b64

            result = await _check_visibility(session, screenshot_b64, query)
            _log.info(
                "    [visibility] attempt %d/%d visible=%s",
                attempt,
                max_retries,
                result.get("visible"),
            )

            if result.get("visible", False):
                return screenshot_b64

            last_reasoning = result.get("reasoning", "unknown")
            if attempt < max_retries:
                await asyncio.sleep(retry_interval)

    if not should_raise:
        _log.info(
            "    [visibility] not visible after %d attempts (should_raise=False); returning last screenshot. reasoning=%s",
            max_retries,
            last_reasoning,
        )
        return last_screenshot_b64

    raise Exception(
        f"Element not visible after {max_retries} attempts. Last reasoning: {last_reasoning}"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _cast_v3_vision_query_result(raw, return_type: str):
    """Cast the vision heal answer to the requested return type.

    bool branches accept JSON booleans and truthy string representations;
    number branches accept int/float and fall back to digit-extraction;
    everything else is coerced to str.

    Args:
        raw: The value read from response["vision_query"].
        return_type: "bool", "number", or any other string (treated as str).

    Returns:
        Typed Python value.
    """
    if return_type == "bool":
        if isinstance(raw, bool):
            return raw
        return str(raw).strip().lower() in ("true", "1", "yes")
    if return_type == "number":
        if isinstance(raw, (int, float)):
            return float(raw)
        s = str(raw).strip()
        try:
            return float(s)
        except ValueError:
            filtered = "".join(c for c in s if c.isdigit() or c == ".")
            return float(filtered) if filtered else 0.0
    return "" if raw is None else str(raw)


def _coerce_textual_value(value, return_type: str):
    """Cast the textual query heal ``value`` to ``return_type``.

    Only the "number" return type is special-cased; every other type passes the
    value through unchanged (str / bool / None / dict preserved). Empty/None inputs
    pass through even for "number" (e.g. a regex-miss returns ""). Direct
    float() is tried first, then a digit-filter fallback for formatted numerics
    like "$1,234.56"; a "-" anywhere flips the sign.

    Args:
        value: Raw value read from the textual_query response's ``value`` field.
        return_type: Expected type hint; "number" is the only special case.

    Returns:
        float for "number" inputs containing digits (0.0 if none); the value
        unchanged (str / bool / None / "") otherwise.
    """
    if return_type != "number":
        return value
    if value is None or value == "":
        return value
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (ValueError, TypeError):
        s = str(value)
        is_negative = "-" in s
        filtered = "".join(c for c in s if c.isdigit() or c == ".")
        if not filtered:
            return 0.0
        result = float(filtered)
        return -result if is_negative else result


async def vision_query(
    page,
    description: str,
    return_type: str,
    expected_value: str | None = None,
    code_js: str | None = None,
):
    """Extract a value from the page using a screenshot + analyzer API.

    Smart-gated: returns None when _config.smart is OFF.

    Args:
        page: Playwright page object.
        description: Natural-language description of what to extract.
        return_type: Expected type hint (e.g. "string").
        expected_value: When 'true' or 'false', signals a boolean
            visibility/state check. The backend analyzer activates its
            boolean-check path and returns 'true'/'false' instead
            of free-form page text. None for value extraction.
        code_js: The recorded derivation, if this extraction had one. Its
            PRESENCE (even as '') tells the backend which extraction contract
            authored this recording, so the raw value it returns is shaped the
            way the derivation expects; the derivation itself is recomputed
            here, in the browser, over that fresh raw value. Absent for
            recordings made before derivations existed.

    Returns:
        Extracted value as a string (derived when code_js is set), or None when
        smart is OFF.
    """
    if not _config.smart:
        return None

    from testmu import _configure

    _log.info("    [vision_query] query=%s", description[:80])

    if _configure.get("kane_version", "v4") == "v3":
        # Heal path: posts to the vision heal endpoint. The current_action
        # carries operation_type="VISION_QUERY" (uppercase) and result_type
        # inside operation_dict; the outer payload carries use_query_v2 alongside
        # version.
        from testmu._vars import var
        description = var(description)
        base_url = _configure.get("automind_url", "")
        if not base_url:
            _log_v3.warning("[vision_query] no heal endpoint configured")
            return None
        screenshot_b64 = await _capture_screenshot_b64(page)
        current_action = {
            "operation_type": "VISION_QUERY",
            "operation_intent": description,
            "instruction_id": "",
            "operation_id": "",
            "use_query_v2": True,
            "version": "v3",
            "selector": [],
            "frame_info": [],
            "sub_instruction_obj": {
                "operation_dict": {
                    "queried_value": description,
                    "result_type": return_type,
                },
            },
        }
        payload = _normalize_v3_payload_types({
            "code_export_id": _configure.get("code_export_id", ""),
            "current_action": current_action,
            "commit_id": _configure.get("commit_id", ""),
            "test_id": _configure.get("test_id", ""),
            "username": _configure.get("username", ""),
            "accesskey": _configure.get("accesskey", ""),
            "org_id": _configure.get("org_id", ""),
            "session_id": _configure.get("session_id", ""),
            "untagged_image_base64": screenshot_b64,
            "use_query_v2": True,
            "version": "v3",
        })
        url = f"{base_url}{V3_HEAL_VISION_PATH}"
        headers = _v3_auth_headers()
        try:
            result = await _post_v3_vision(url, payload, headers)
        except Exception as e:
            _log_v3.warning("[vision_query] '%s': %s", description[:80], e)
            raise RuntimeError(f"vision_query failed: {e}") from e
        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(f"vision_query failed: {result['error']}")
        raw = result.get("vision_query") if isinstance(result, dict) else None
        if raw is None:
            raise RuntimeError(
                f"vision_query response missing 'vision_query' field: {result}"
            )
        extracted = _cast_v3_vision_query_result(raw, return_type)
        _log_v3.info("    [vision_query] result=%s", repr(extracted)[:120])
        return await _derive_if_recorded(page, code_js, extracted)

    # VQ must not throw on invisibility — fall through with the last screenshot
    # so the analyzer still gets a chance to extract.
    screenshot_b64 = await _wait_for_visibility(
        page,
        description,
        opts={"max_retries": 2, "retry_interval": 2, "should_raise": False},
    )

    body: dict = {
        "type": "visual",
        "query": description,
        "screenshot_b64": screenshot_b64,
    }
    if expected_value is not None:
        body["expected_value"] = expected_value
    if code_js is not None:
        body["code_js"] = code_js

    async with create_session() as session:
        result = await _post_analyzer(session, body, timeout=_QUERY_TIMEOUT)

    extracted = result.get("extracted_value", "")
    _log.info("    [vision_query] result=%s", repr(extracted)[:120])
    return await _derive_if_recorded(page, code_js, extracted)



async def textual_query(page, description: str, return_type: str, selected_attribute_name: str = "", expected_value: str | None = None):
    """Extract a value from a DOM element using 2-step DOM + analyzer API.

    Step 1: Build flat accessibility tree, identify target element via LLM.
    Step 2: Snapshot element via CDP, extract value via LLM.

    Smart-gated: returns None when _config.smart is OFF.

    Args:
        page: Playwright page object.
        description: Natural-language description of what to extract.
        return_type: Expected type hint (e.g. "string").
        expected_value: When 'true' or 'false', signals a boolean
            state check (e.g. checkbox.checked, radio.selected,
            aria-expanded). The backend DOM analyzer activates its
            boolean-check path and returns 'true'/'false'
            instead of 'checked'/'on'/element text. Only applied on
            the extract step; identify step is unaffected.
        selected_attribute_name: Optional attribute name hint.

    Returns:
        Extracted value as a string, or None when smart is OFF.
    """
    if not _config.smart:
        return None

    _log.info("    [textual_query] query=%s", description[:80])

    # Heal path: snapshot-based read via the textual query heal endpoint.
    # Returns before any screenshot; the analyzer path below is unchanged.
    from testmu import _configure
    if _configure.get("kane_version", "v4") == "v3":
        return await _textual_query_v3(page, description, return_type, selected_attribute_name)

    cdp = await page.context.new_cdp_session(page)
    try:
        await cdp.send("DOM.enable")

        a11y_resp = await cdp.send("Accessibility.getFullAXTree")
        flat_dom = _build_flat_dom(a11y_resp.get("nodes", []))

        screenshot_bytes = await take_screenshot(page)
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

        async with create_session() as session:
            identify_resp = await _post_analyzer(
                session,
                {
                    "type": "dom",
                    "query": description,
                    "full_dom_list": flat_dom,
                    "screenshot_b64": screenshot_b64,
                },
            )
            dom_index = identify_resp.get("dom_index")
            if dom_index is None:
                raise Exception(
                    f"DOM identify step returned no dom_index: {identify_resp}"
                )
            dom_index = int(dom_index)

            target = next((el for el in flat_dom if el.get("index") == dom_index), None)
            if not target or "backend_dom_node_id" not in target:
                raise Exception(
                    f"Element at dom_index={dom_index} not found or missing backend_dom_node_id"
                )

            snapshot = await _get_element_snapshot(cdp, target["backend_dom_node_id"])

            extract_body: dict = {
                "type": "dom",
                "query": description,
                "element_snapshot": snapshot,
            }
            if expected_value is not None:
                extract_body["expected_value"] = expected_value

            extract_resp = await _post_analyzer(session, extract_body)

        extracted = extract_resp.get("extracted_value", "")
        _log.info("    [textual_query] result=%s", repr(extracted)[:120])
        return extracted

    finally:
        await cdp.detach()


async def vision_wait(page, description: str, timeout_ms: int = 30000):
    """Poll the vision wait API until the described condition is met.

    Smart-gated: falls back to page.wait_for_timeout(timeout_ms) when
    _config.smart is OFF.

    Args:
        page: Playwright page object.
        description: Human-readable description of what to wait for.
        timeout_ms: Original timeout in ms. Used as static sleep when smart is OFF.
    """
    if not _config.smart:
        await page.wait_for_timeout(timeout_ms)
        return

    _log.info("    [vision_wait] query=%s", description[:80])

    async with create_session() as session:
        for attempt in range(1, _WAIT_MAX_RETRIES + 1):
            screenshot_b64 = await _capture_screenshot_versioned_b64(page)

            result = await _check_wait_condition(session, screenshot_b64, description)
            waiting = result.get("waiting", True)
            _log.info(
                "    [vision_wait] attempt %d/%d waiting=%s",
                attempt,
                _WAIT_MAX_RETRIES,
                waiting,
            )

            if not waiting:
                return

            if attempt < _WAIT_MAX_RETRIES:
                await asyncio.sleep(_WAIT_RETRY_INTERVAL)

    _log.info("    [vision_wait] max retries exhausted, continuing")


async def _query_viewport_size(page):
    """Query the live viewport via window.innerWidth/innerHeight.

    page.viewport_size is None when Playwright connects over CDP
    (grid / real-device) since Playwright never set the viewport. Reading
    the page directly works regardless of how the browser was launched or
    connected. Returns a {"width", "height"} dict, or None so the caller
    applies its own default.
    """
    try:
        dims = await page.evaluate(
            "() => ({ width: window.innerWidth, height: window.innerHeight })"
        )
        if dims and dims.get("width") and dims.get("height"):
            return dims
    except Exception:
        pass
    return None


async def vision_action(
    page, description: str, action_type: str, direction: str = "down", amount: int = 300
) -> bool:
    """Get vision coordinates and execute click or scroll at those coordinates.

    Smart-gated: returns None when _config.smart is OFF.

    Args:
        page: Playwright page object.
        description: Human-readable description of the target element.
        action_type: "click" or "scroll".
        direction: Scroll direction ("up", "down", "left", "right"). Only used for scroll.
        amount: Scroll amount in pixels. Only used for scroll.

    Returns:
        True if coordinates found and action executed, False on API miss,
        or None when smart is OFF.
    """
    if not _config.smart:
        return None

    _log.info("    [vision_action] action=%s query=%s", action_type, description[:60])

    screenshot_b64 = await _capture_screenshot_versioned_b64(page)

    viewport = await _query_viewport_size(page)
    width = viewport["width"] if viewport else 1920
    height = viewport["height"] if viewport else 1080

    async with create_session() as session:
        async with session.post(
            f"{_VISION_API_HOST}/api/v1/vision/coordinates",
            json={
                "screenshot_b64": screenshot_b64,
                "action_instruction": description,
                "action_type": action_type,
                "width": width,
                "height": height,
            },
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            if resp.status != 200:
                _log.info("    [vision_action] API error status=%d", resp.status)
                return False
            result = await resp.json()
            if not result.get("found", False):
                _log.info("    [vision_action] element not found")
                return False
            coord_x = result["x"]
            coord_y = result["y"]

    _log.info(
        "    [vision_action] executing %s at (%d, %d)", action_type, coord_x, coord_y
    )

    if action_type == "click":
        await page.mouse.click(coord_x, coord_y)
    elif action_type == "scroll":
        delta_x = 0
        delta_y = 0
        if direction == "down":
            delta_y = amount
        elif direction == "up":
            delta_y = -amount
        elif direction == "right":
            delta_x = amount
        elif direction == "left":
            delta_x = -amount
        await page.mouse.move(coord_x, coord_y)
        await page.mouse.wheel(delta_x, delta_y)

    return True


async def get_vision_coordinates(
    page, description: str, action_type: str = "click", x: int = None, y: int = None
) -> dict:
    """Get coordinates for an element via vision API.

    When smart is ON: always uses vision API. No fallback to (x, y) — if the
    API can't find the element or errors, raises instead of silently using
    stale coordinates that may click the wrong thing.

    When smart is OFF: returns {"x": x, "y": y} immediately.

    Args:
        page: Playwright page object.
        description: Description of the action/element to find.
        action_type: Type of action ("click", "type", etc.).
        x: X coordinate used only when smart is OFF.
        y: Y coordinate used only when smart is OFF.

    Returns:
        dict with 'x' and 'y' keys.
    """
    if not _config.smart:
        return {"x": x, "y": y}

    _log.info("    [get_vision_coordinates] query=%s", description[:60])

    screenshot_b64 = await _wait_for_visibility(page, description)

    viewport = await _query_viewport_size(page)
    width = viewport["width"] if viewport else 1920
    height = viewport["height"] if viewport else 1080

    async with create_session() as session:
        async with session.post(
            f"{_VISION_API_HOST}/api/v1/vision/coordinates",
            json={
                "screenshot_b64": screenshot_b64,
                "action_instruction": description,
                "width": width,
                "height": height,
            },
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Vision API error: {resp.status}")
            result = await resp.json()
            if not result.get("found", False):
                raise Exception(
                    f"Vision API: element not found for query={description!r}"
                )
            coords = {"x": result["x"], "y": result["y"]}
            _log.info(
                "    [get_vision_coordinates] found (%d, %d)", coords["x"], coords["y"]
            )
            # Ship the resolved click point via lambda-element-bounds so the
            # per-step record gets coordinates for the vision-heal path —
            # page.mouse.click(x, y) bypasses the Locator wrapper that
            # normally calls _capture_element_bounds. Width/height ship as
            # 0 — analyzer returns only a click point, not a rect.
            await _ship_vision_coords(coords["x"], coords["y"])
            return coords


async def _ship_vision_coords(x, y):
    """Ship a vision-resolved click point via lambda-element-bounds.

    The vision analyzer only returns a click point (no bbox), so width/height
    ship as 0. The next command capture promotes this onto the step's
    coordinates field — mirrors _heal_patch's _capture_element_bounds for
    the page.mouse.click(x, y) path that bypasses Locator wrapping.
    Best-effort — never blocks the action.
    """
    try:
        from testmu import _config
        if _config.run_target != "cloud":
            return
        from testmu._step import _current_step
        step = _current_step.get()
        if step is None:
            return
        instruction_id = getattr(step, "instruction_id", None)
        from testmu._reporter import reporter
        await reporter().send_element_bounds(
            {"x": x, "y": y, "width": 0, "height": 0},
            instruction_id,
        )
    except Exception as e:
        _log.debug(f"[bounds] vision capture skipped: {e}")
# ===========================================================================
# Vision/coordinate heal client (kane_version == "v3")
# ---------------------------------------------------------------------------
# Self-contained block for the heal cascade. None of the functions
# above are modified; these are additive and only reached when kane_version == "v3".
# The cascade (testmu._heal_cascade) imports get_v3_vision_target,
# get_v3_coordinate_target and _extract_coordinates_from_response from here.
# ===========================================================================

_log_v3 = logging.getLogger("testmu.vision_v3")

V3_HEAL_VISION_PATH = "/v1/heal/vision"
V3_HEAL_COORDINATES_PATH = "/v1/heal/coordinates"
V3_HEAL_TEXTUAL_QUERY_PATH = "/v1/heal/textual_query"

# CSS properties requested for the DOMSnapshot.captureSnapshot computed-styles
# read on the textual_query heal path.
_CSS_PROPERTIES = [
    "color", "background-color", "border-color",
    "font-size", "font-family", "font-weight", "font-style",
    "display", "visibility", "opacity",
]

# Payload fields that must be coerced to str (None -> "") to match the
# server-side schema.
_V3_STR_FIELDS = (
    "code_export_id",
    "commit_id",
    "test_id",
    "username",
    "accesskey",
    "session_id",
)


async def _capture_screenshot_b64(page) -> str:
    """Capture a viewport screenshot as a base64 PNG via the Chrome DevTools
    Protocol, bypassing Playwright's high-level ``page.screenshot()``.

    ``page.screenshot()`` blocks on ``document.fonts.ready`` (and animation-frame
    stability) before capturing, with a 30s default timeout — so a single web
    font that never finishes loading makes it raise a Timeout error.
    ``Page.captureScreenshot`` is the CDP analogue and returns the base64-encoded
    PNG directly.

    Chromium-only — the runtime connects via the Chromium CDP path.
    """
    cdp = await page.context.new_cdp_session(page)
    try:
        result = await cdp.send("Page.captureScreenshot", {"format": "png"})
        return result["data"]  # CDP returns base64-encoded PNG
    finally:
        await cdp.detach()


async def _capture_full_page_screenshot_b64(page) -> str:
    """Capture a FULL-PAGE screenshot as base64 PNG via the Chrome DevTools
    Protocol, bypassing Playwright's high-level ``page.screenshot(full_page=True)``.

    Same motivation as ``_capture_screenshot_b64``: the high-level API blocks on
    ``document.fonts.ready`` (and animation-frame stability) before capturing and
    hangs behind the LambdaTest grid proxy. ``Page.captureScreenshot`` with
    ``captureBeyondViewport`` and a clip sized to the document's ``cssContentSize``
    captures the whole scrollable page in one shot.

    Coordinate consumers normalise by the returned image's own dimensions
    (``raw * page_dim / image_dim``), so the absolute capture scale cancels out.

    Chromium-only — the runtime connects via the Chromium CDP path.
    """
    cdp = await page.context.new_cdp_session(page)
    try:
        metrics = await cdp.send("Page.getLayoutMetrics")
        size = metrics.get("cssContentSize") or metrics.get("contentSize") or {}
        params = {"format": "png", "captureBeyondViewport": True}
        width, height = size.get("width"), size.get("height")
        if width and height:
            params["clip"] = {"x": 0, "y": 0, "width": width, "height": height, "scale": 1}
        result = await cdp.send("Page.captureScreenshot", params)
        return result["data"]  # CDP returns base64-encoded PNG
    finally:
        await cdp.detach()


async def _capture_screenshot_versioned_b64(page) -> str:
    """Capture a viewport screenshot as base64 PNG, gated on ``kane_version``.

    When kane_version=="v3": grab via CDP ``Page.captureScreenshot``
    (``_capture_screenshot_b64``), dodging the ``document.fonts.ready`` timeout
    that ``page.screenshot()`` raises behind the LambdaTest grid proxy.

    Otherwise (default): keep the high-level binding screenshot
    (``take_screenshot``) — behavior unchanged.

    Used by the version-agnostic vision sites (``vision_wait``, ``vision_action``).
    (``textual_query`` has its own heal route via ``_textual_query_v3`` —
    snapshot-based, no screenshot — so it does not use this.)
    """
    from testmu import _configure
    if _configure.get("kane_version", "v4") == "v3":
        return await _capture_screenshot_b64(page)
    screenshot_bytes = await take_screenshot(page)
    return base64.b64encode(screenshot_bytes).decode("utf-8")


async def _textual_query_v3(page, description: str, return_type: str, selected_attribute_name: str = ""):
    """Textual query heal — locate element locally then read attribute, with
    server POST as last-resort fallback.

    Route table:
    1. ``automind_url`` unconfigured → return None (no CDP, no network).
    2. ``selected_attribute_name`` empty or not in ``_LOCAL_READ_ATTRS`` →
       short-circuit to ``_textual_query_v3_server`` (no locate, no scroll, no
       full-page screenshot — preserves today's contract for the common no-attr
       case).
    3. Supported attr → locate via DESKTOP_LOCATE_FULL_PAGE (full-page screenshot
       + server call to /v2/locate/desktop) → scroll into view →
       ``resolve_coordinate_read`` (exact hit, no interactable up-walk) →
       ``_textual_extract_value``. Returns the local result without any server POST.
    4. Any locate/resolve/read failure → fall back to ``_textual_query_v3_server``
       with the **raw** ``description`` (byte-identical to today's server contract).

    V3-only (reached only from the ``kane_version=="v3"`` gate in
    ``textual_query``). The V4 analyzer path (``vision.py``) is never
    touched.

    Args:
        page: Playwright page object.
        description: Natural-language description (raw, before ``var()`` resolution).
        return_type: Coercion hint for the extracted value.
        selected_attribute_name: Attribute to extract locally, or "" for server.

    Returns:
        Extracted value (coerced to return_type), or None when unconfigured.

    Raises:
        RuntimeError: Propagated from ``_textual_query_v3_server`` on transport
            failure or error envelope (same contract as before this change).
    """
    from testmu import _configure
    base_url = _configure.get("automind_url", "")
    if not base_url:
        _log_v3.warning("[textual_query] no heal endpoint configured")
        return None

    # Short-circuit (must-fix §4): empty/unsupported attr → server straight away.
    # No locate, no full-page screenshot, no scrollTo — preserves today's contract.
    if (not selected_attribute_name) or (selected_attribute_name not in _LOCAL_READ_ATTRS):
        return await _textual_query_v3_server(page, description, return_type, selected_attribute_name)

    # Locate-then-read path for supported attributes.
    # ``var(description)`` resolves {{vars}}/${params} for the locate intent only
    # (plaintext, no masking — parity with vision_query). The RAW description
    # is passed to the server fallback to preserve byte-identical server behavior.
    # var() itself is inside the try block so a resolution error degrades to server
    # fallback rather than hard-failing the test step.
    try:
        from testmu._vars import var
        resolved_desc = var(description)

        import testmu._heal_cascade as _hc
        import testmu._helpers._coordinate_resolver_read as _crr
        import testmu._helpers._textual_read as _tr

        coords = await _hc.get_v3_desktop_locate_full_page_target(page, resolved_desc)
        if coords is not None:
            vx, vy = await _scroll_into_view_and_viewport_coords(page, coords)
            target = await _crr.resolve_coordinate_read(page, vx, vy)
            if target is not None:
                # _v3_textual_selector pins the xpath= engine for Playwright.
                loc = page.locator(_v3_textual_selector(target.xpath))
                return await _tr._extract_value(
                    loc, selected_attribute_name, None, return_type
                )
    except Exception as exc:  # noqa: BLE001 — locate failures must never hard-fail
        _log_v3.warning("[textual_query] locate-read failed (%s); server fallback", exc)

    # Server fallback: receives the ORIGINAL raw description (byte-identical to
    # today on every fallback path: locate miss, resolver null, any error).
    return await _textual_query_v3_server(page, description, return_type, selected_attribute_name)


def _normalize_v3_payload_types(payload: dict) -> dict:
    """Coerce outer payload field types to match the server schema.

    Mutates and returns the payload:
      - str fields normalised via str(), None -> "".
      - org_id coerced to int via int(); unparseable -> 0.
    """
    for key in _V3_STR_FIELDS:
        if key in payload:
            v = payload[key]
            payload[key] = "" if v is None else str(v)
    if "org_id" in payload:
        raw = payload["org_id"]
        if raw in (None, ""):
            payload["org_id"] = 0
        else:
            try:
                payload["org_id"] = int(raw)
            except (TypeError, ValueError):
                payload["org_id"] = 0
    return payload


async def _post_v3_vision(url: str, payload: dict, headers: dict) -> dict:
    """HTTP layer separated for testability (patched in tests)."""
    import httpx as _httpx
    async with _httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, json=payload, headers=headers)
        if r.status_code >= 400:
            _log_v3.error("[v3 vision] HTTP %d body=%s", r.status_code, r.text[:1000])
        r.raise_for_status()
        return r.json()


def _build_v3_vision_payload(description: str, screenshot_b64: str, method_name: str = "click") -> dict:
    """Construct the vision heal payload.

    Args:
        description: Human-readable intent of the action being healed.
        screenshot_b64: Base-64 encoded PNG of the current viewport.
        method_name: Method name forwarded as ``operation_type`` (lowercase).
    """
    from testmu import _configure
    current_action = {
        "operation_type": method_name,
        "operation_intent": description,
        "instruction_id": "",
        "operation_id": "",
        "use_query_v2": True,
        "version": "v3",
        "selector": [],
        "frame_info": [],
        "sub_instruction_obj": {
            "operation_dict": {
                "queried_value": description,
            },
        },
    }
    return _normalize_v3_payload_types({
        "code_export_id": _configure.get("code_export_id", ""),
        "current_action": current_action,
        "commit_id": _configure.get("commit_id", ""),
        "test_id": _configure.get("test_id", ""),
        "username": _configure.get("username", ""),
        "accesskey": _configure.get("accesskey", ""),
        "version": "v3",
        "org_id": _configure.get("org_id", ""),
        "session_id": _configure.get("session_id", ""),
        "untagged_image_base64": screenshot_b64,
    })


def _v3_auth_headers() -> dict:
    """Auth headers for the vision heal endpoint (Basic auth: username:accesskey)."""
    from testmu import _configure
    username = _configure.get("username", "")
    accesskey = _configure.get("accesskey", "")
    auth_token = base64.b64encode(
        f"{username}:{accesskey}".encode()
    ).decode()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_token}",
    }


# ===========================================================================
# V3 textual_query additive helpers (appended; never modify above this line)
# ===========================================================================

# Allow-list of attributes that can be read LOCALLY (all entries have a
# corresponding branch in testmu._helpers._textual_read._populate_attribute).
# Attributes NOT in this set (e.g. "location", "custom_attributes_dict", or any
# unknown name) are short-circuited straight to the server so they preserve
# today's contract exactly.
_LOCAL_READ_ATTRS = frozenset({
    # Computed CSS
    "color", "background_color", "font_size", "font_weight",
    "border_radius", "z_index", "opacity", "transform",
    # HTML attributes
    "id", "class", "href", "src",
    "aria_label", "aria-label", "aria_expanded", "aria-expanded",
    "placeholder", "title",
    # Boolean states
    "enabled", "checked", "selected", "displayed", "disabled",
    # Tag name (explicit only; implicit ARIA role needs CDP → server)
    "tag_name",
    # Content
    "text", "value",
    # Element props
    "size", "outerHTML", "attributes",
})


def _v3_textual_selector(xpath: str) -> str:
    """Pin the xpath= Playwright engine for a read-resolver derived selector.

    Read resolver always yields ``//…`` or ``/html[1]/…`` style xpaths. Playwright
    auto-detects ``//`` but not absolute ``/html``, so always prefix. Already-pinned
    selectors (``xpath=``, ``css=``) are returned unchanged.

    This is a lightweight stand-in for ``_action_engine._engine_selector`` that
    avoids the circular import (``_action_engine`` → ``_heal_cascade`` → ``vision``).
    """
    if xpath.startswith(("xpath=", "css=", "text=")):
        return xpath
    if xpath.startswith(("/", "(")):
        return "xpath=" + xpath
    return xpath


async def _scroll_into_view_and_viewport_coords(page, coords) -> tuple:
    """Scroll the target page-space coordinate into the viewport and return viewport coords.

    Mirrors the tier scroll math in ``_heal_cascade._run_desktop_locate_full_page_tier``.
    Duplicated here (~6 lines) to avoid a module-level import of
    ``_heal_cascade`` (which already imports from this module, creating a cycle).

    Args:
        page: Playwright page object.
        coords: ``(page_x, page_y)`` page-space CSS coordinates from the locate call.

    Returns:
        ``(viewport_x, viewport_y)`` clamped to ``[0, viewport_dim - 1]``.
    """
    px, py = int(coords[0]), int(coords[1])
    dims = await page.evaluate(
        "() => ({ w: window.innerWidth, h: window.innerHeight })"
    )
    vw = dims.get("w") or 1920
    vh = dims.get("h") or 1080
    sx_target = max(0, px - vw // 2)
    sy_target = max(0, py - vh // 2)
    await page.evaluate(f"() => window.scrollTo({sx_target}, {sy_target})")
    await asyncio.sleep(0.15)
    scroll = await page.evaluate(
        "() => ({ x: window.scrollX, y: window.scrollY })"
    )
    sx = scroll.get("x") or 0
    sy = scroll.get("y") or 0
    vx = max(0, min(px - sx, vw - 1))
    vy = max(0, min(py - sy, vh - 1))
    return vx, vy


async def _textual_query_v3_server(
    page, description: str, return_type: str, selected_attribute_name: str = ""
):
    """Server-side textual query heal — verbatim relocation of the original
    ``_textual_query_v3`` body (pre-locate-read refactor).

    POSTs raw CDP a11y + DOM snapshots to the textual query heal endpoint.
    The server reads the value server-side from the snapshots; no screenshot
    is taken.

    Called as the last-resort fallback from ``_textual_query_v3`` whenever the
    locate-then-read path is skipped (empty/unsupported attr, unconfigured) or
    fails (locate miss, resolver null, any error). Always receives the **raw**
    ``description`` so its behavior is byte-identical to the pre-refactor contract
    on every path it is reached.

    Returns the extracted value coerced by return_type, or None when the heal
    endpoint is unconfigured. Raises RuntimeError on transport failure or an
    error envelope.
    """
    from testmu import _configure
    base_url = _configure.get("automind_url", "")
    if not base_url:
        _log_v3.warning("[textual_query] no heal endpoint configured")
        return None

    cdp = await page.context.new_cdp_session(page)
    try:
        await cdp.send("Accessibility.enable")
        a11y_snapshot = await cdp.send("Accessibility.getFullAXTree")
        dom_snapshot = await cdp.send("DOMSnapshot.captureSnapshot", {
            "computedStyles": _CSS_PROPERTIES,
            "includeDOMRects": True,
        })
    finally:
        await cdp.detach()

    # selected_attribute_name lives ONLY in operation_dict — the server falls
    # back to it when the outer selected_attribute is empty, so we omit the outer
    # key.
    current_action = {
        "operation_type": "TEXTUAL_QUERY",
        "operation_intent": description,
        "instruction_id": "",
        "operation_id": "",
        "use_query_v2": True,
        "version": "v3",
        "selector": [],
        "frame_info": [],
        "sub_instruction_obj": {
            "operation_dict": {
                "queried_value": description,
                "selected_attribute_name": selected_attribute_name,
            },
        },
    }
    payload = _normalize_v3_payload_types({
        "code_export_id": _configure.get("code_export_id", ""),
        "username": _configure.get("username", ""),
        "accesskey": _configure.get("accesskey", ""),
        "org_id": _configure.get("org_id", ""),
        "test_id": _configure.get("test_id", ""),
        "commit_id": _configure.get("commit_id", ""),
        "current_action": current_action,
        "version": "v3",
        "a11y_snapshot": a11y_snapshot,
        "dom_snapshot": dom_snapshot,
        "is_browser": True,
        "is_mobile": False,
        "device_os": "",
    })
    url = f"{base_url}{V3_HEAL_TEXTUAL_QUERY_PATH}"
    headers = _v3_auth_headers()
    try:
        result = await _post_v3_vision(url, payload, headers)
    except Exception as e:
        _log_v3.warning("[textual_query] '%s': %s", description[:80], e)
        raise RuntimeError(f"textual_query failed: {e}") from e
    if isinstance(result, dict) and result.get("error"):
        raise RuntimeError(f"textual_query failed: {result['error']}")
    value = result.get("value") if isinstance(result, dict) else None
    extracted = _coerce_textual_value(value, return_type)
    _log_v3.info("    [textual_query] result=%s", repr(extracted)[:120])
    return extracted


async def get_v3_vision_target(page, description: str, method_name: str = "click"):
    """Vision query — posts to the vision heal endpoint.

    Returns the raw response dict, or None on config/transport failure. The
    automind_url check fires BEFORE the screenshot call so an unconfigured
    environment doesn't take a screenshot it will throw away.
    """
    try:
        from testmu import _configure
        base_url = _configure.get("automind_url", "")
        if not base_url:
            _log_v3.warning("[v3 vision] no automind_url configured")
            return None
        snapshot_b64 = await _capture_screenshot_b64(page)
        payload = _build_v3_vision_payload(description, snapshot_b64, method_name=method_name)
        url = f"{base_url}{V3_HEAL_VISION_PATH}"
        headers = _v3_auth_headers()
        return await _post_v3_vision(url, payload, headers)
    except Exception as e:
        _log_v3.warning(f"[v3 vision] '{description}': {e}")
        return None


def _build_v3_coordinates_payload(
    description: str,
    screenshot_b64: str,
    viewport_width: int,
    viewport_height: int,
    method_name: str = "click",
) -> dict:
    """Construct the coordinates heal payload."""
    from testmu import _configure
    current_action = {
        "operation_type": method_name,
        "operation_intent": description,
        "instruction_id": "",
        "operation_id": "",
        "use_query_v2": True,
        "version": "v3",
        "selector": [],
        "frame_info": [],
        "sub_instruction_obj": {
            "operation_dict": {
                "queried_value": description,
            },
        },
    }
    return _normalize_v3_payload_types({
        "code_export_id": _configure.get("code_export_id", ""),
        "username": _configure.get("username", ""),
        "accesskey": _configure.get("accesskey", ""),
        "org_id": _configure.get("org_id", ""),
        "test_id": _configure.get("test_id", ""),
        "commit_id": _configure.get("commit_id", ""),
        "session_id": _configure.get("session_id", ""),
        "prev_actions": [],
        "xpath_mapping": {},
        "tagified_image": "",
        "tags_description": {},
        "is_browser": True,
        "is_mobile": False,
        "device_os": "",
        "width": viewport_width,
        "height": viewport_height,
        "page_source": "",
        "untagged_image_base64": screenshot_b64,
        "current_action": current_action,
        "use_query_v2": True,
        "version": "v3",
    })


def _extract_coordinates_from_response(
    response: dict,
    viewport_width: int,
    viewport_height: int,
):
    """Read (x, y) from the coordinates heal endpoint response.

    Two shapes accepted:
      1. response_coordinates: [x, y] — pre-computed pixel coords (preferred).
      2. element_coordinates_ratio: [rx, ry] — ratio × viewport size (fallback).

    Returns None on miss (including error envelopes) so callers can
    distinguish "tier returned but no actionable coords" from "tier hit".
    """
    if not isinstance(response, dict):
        return None
    if response.get("error"):
        return None
    pre = response.get("response_coordinates")
    if isinstance(pre, (list, tuple)) and len(pre) >= 2:
        try:
            return int(pre[0]), int(pre[1])
        except (TypeError, ValueError):
            pass
    ratio = response.get("element_coordinates_ratio")
    if isinstance(ratio, (list, tuple)) and len(ratio) >= 2:
        try:
            return int(float(ratio[0]) * viewport_width), int(float(ratio[1]) * viewport_height)
        except (TypeError, ValueError):
            pass
    return None


def _crop_b64_to_viewport_aspect(screenshot_b64, viewport_width, viewport_height):
    """Crop a base64 PNG to the viewport aspect ratio, removing device chrome /
    beyond-viewport excess. Mirrors the Selenium browser_coordinate crop: a CDP
    screenshot captured at devicePixelRatio may be taller than the CSS viewport
    aspect; cropping to (0,0,screenshot_width, screenshot_width/aspect) makes the
    image geometry the locate service sees match the width/height the binding sends.
    No-op when Pillow is unavailable, dims are falsy, decode fails, or no crop
    is needed."""
    if Image is None or not viewport_width or not viewport_height:
        return screenshot_b64
    try:
        img = Image.open(io.BytesIO(base64.b64decode(screenshot_b64)))
        screenshot_width, screenshot_height = img.size
        aspect_ratio = viewport_width / viewport_height
        expected_height = int(screenshot_width / aspect_ratio)
        if 0 < expected_height < screenshot_height:
            cropped = img.crop((0, 0, screenshot_width, expected_height))
            buf = io.BytesIO()
            cropped.save(buf, format="PNG")
            return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        _log_v3.warning("[v3 coord] screenshot aspect-crop failed: %s", e)
    return screenshot_b64


def _b64_png_size(screenshot_b64):
    """Return (width, height) of a base64 PNG, or None on decode failure. Diagnostic-only."""
    if Image is None:
        return None
    try:
        return Image.open(io.BytesIO(base64.b64decode(screenshot_b64))).size
    except Exception:
        return None


async def get_v3_coordinate_target(page, description: str, method_name: str = "click"):
    """Coordinate heal — posts to the coordinates heal endpoint.

    Returns the raw response dict (caller passes to
    _extract_coordinates_from_response), or None on config/transport failure so
    the cascade can fall through to the next tier.
    """
    try:
        from testmu import _configure
        base_url = _configure.get("automind_url", "")
        if not base_url:
            _log_v3.warning("[v3 coord] no automind_url configured")
            return None
        viewport = await _query_viewport_size(page) or {"width": 1920, "height": 1080}
        raw_b64 = await _capture_screenshot_b64(page)
        snapshot_b64 = _crop_b64_to_viewport_aspect(raw_b64, viewport["width"], viewport["height"])
        payload = _build_v3_coordinates_payload(
            description,
            snapshot_b64,
            viewport["width"],
            viewport["height"],
            method_name=method_name,
        )
        url = f"{base_url}{V3_HEAL_COORDINATES_PATH}"
        headers = _v3_auth_headers()
        result = await _post_v3_vision(url, payload, headers)
        try:
            dpr = await page.evaluate("() => window.devicePixelRatio")
        except Exception:
            dpr = None
        _log_v3.info(
            "    [v3 coord] query=%r innerWH=(%s,%s) dpr=%s rawPNG=%s response=%r",
            description, viewport["width"], viewport["height"], dpr,
            _b64_png_size(raw_b64), result,
        )
        return result
    except Exception as e:
        _log_v3.warning(f"[v3 coord] '{description}': {e}")
        return None
