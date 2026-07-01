"""Tests for Heal.desktop_locate() — DESKTOP_LOCATE tier.

POSTs to /v2/locate/desktop with a VIEWPORT screenshot, then scales the
returned image-pixel coordinate to viewport-CSS-px using PNG IHDR dims.

Key contract:
  css_x = raw_x * viewport_width  / image_width
  css_y = raw_y * viewport_height / image_height

Miss detection: HTTP 200 with coordinate==[0,0] is a not-found (NOT 404).
Treats coordinate missing/null/[0,0]/len<2 as HealTierMiss. Also raises
HealTierMiss on non-200 (after up to 3 retry attempts with fresh screenshots).
"""
from __future__ import annotations

import base64
import io
import logging
import struct
from unittest.mock import MagicMock, patch

import httpx
import pytest
import respx

from testmu_selenium._heal import Heal
from testmu_selenium._errors import HealTierMiss

AUTOMIND_URL = "https://kaneai-api.lambdatest.com"
LOCATE_DESKTOP_URL = f"{AUTOMIND_URL}/v2/locate/desktop"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_png_b64(width: int, height: int) -> str:
    """Create a real PNG of given dims (via PIL or manual IHDR header)."""
    try:
        from PIL import Image
        img = Image.new("RGB", (width, height), color=(100, 100, 100))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except ImportError:
        # Minimal valid PNG: 8-byte signature + IHDR chunk + IDAT + IEND
        sig = b"\x89PNG\r\n\x1a\n"
        ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        import zlib
        ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF
        ihdr = struct.pack(">I", 13) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)
        idat_data = zlib.compress(b"\x00" + b"\x00" * (width * 3))
        idat_crc = zlib.crc32(b"IDAT" + idat_data) & 0xFFFFFFFF
        idat = struct.pack(">I", len(idat_data)) + b"IDAT" + idat_data + struct.pack(">I", idat_crc)
        iend_crc = zlib.crc32(b"IEND") & 0xFFFFFFFF
        iend = struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)
        return base64.b64encode(sig + ihdr + idat + iend).decode("utf-8")


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "sess-dl-1"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    # Default: execute_script returns viewport [1280, 720]
    driver.execute_script.return_value = [1280, 720]
    return driver


@pytest.fixture()
def action():
    return {
        "operation_type": "click",
        "operation_intent": "click the submit button",
        "use_query_v2": True,
        "version": "v3",
    }


@pytest.fixture()
def heal(action, mock_driver):
    return Heal(action, mock_driver, username="user", accesskey="key", test_id="t1",
                commit_id="c1", org_id=1)


# ---------------------------------------------------------------------------
# Coordinate scaling — the core contract
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_scales_image_coords_to_viewport_css(heal, mock_driver):
    """COORDINATE SCALING PROOF: image is 2560×1440 (HiDPI), viewport is 1280×720.
    Scale factor = 1280/2560 = 0.5 for X, 720/1440 = 0.5 for Y.
    Raw coordinate (1000, 800) → css (500, 400).
    Reverting the css_x = raw_x * vw / iw scaling in desktop_locate() breaks this.
    """
    # Image: 2560×1440 (e.g. HiDPI screen, devicePixelRatio=2)
    # Viewport: 1280×720
    image_b64 = _make_png_b64(2560, 1440)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [1000, 800]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        css_x, css_y = heal.desktop_locate()

    assert route.called
    # css_x = 1000 * (1280 / 2560) = 500
    # css_y = 800 * (720 / 1440) = 400
    assert css_x == 500, f"Expected css_x=500, got {css_x} (scaling bug in desktop_locate)"
    assert css_y == 400, f"Expected css_y=400, got {css_y} (scaling bug in desktop_locate)"


@respx.mock
def test_desktop_locate_identity_scale_when_image_equals_viewport(heal, mock_driver):
    """When image dims == viewport dims, scale=1.0 → css coord == raw coord."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [640, 360]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        css_x, css_y = heal.desktop_locate()

    assert css_x == 640
    assert css_y == 360


# ---------------------------------------------------------------------------
# Miss detection: [0,0] coordinate is not-found (NOT 404)
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_zero_coordinate_raises_heal_tier_miss(heal, mock_driver):
    """HTTP 200 with coordinate==[0,0] must raise HealTierMiss, not return coords.
    Reverting the [0,0] check in desktop_locate() turns this RED."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [0, 0]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss) as exc_info:
            heal.desktop_locate()

    assert "DESKTOP_LOCATE" in str(exc_info.value)


@respx.mock
def test_desktop_locate_missing_coordinate_raises_heal_tier_miss(heal, mock_driver):
    """HTTP 200 with no 'coordinate' field → HealTierMiss."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"confidence": 0.0})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss):
            heal.desktop_locate()


@respx.mock
def test_desktop_locate_null_coordinate_raises_heal_tier_miss(heal, mock_driver):
    """HTTP 200 with coordinate==null → HealTierMiss."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": None})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss):
            heal.desktop_locate()


@respx.mock
def test_desktop_locate_non_200_raises_heal_tier_miss(heal, mock_driver):
    """Non-200 response → HealTierMiss (never returns coords)."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(404, json={"error": "not found"})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss):
            heal.desktop_locate()


@respx.mock
def test_desktop_locate_500_raises_heal_tier_miss(heal, mock_driver):
    """5xx → HealTierMiss."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(500, json={"error": "internal"})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss):
            heal.desktop_locate()


# ---------------------------------------------------------------------------
# Request shape: endpoint, payload fields, Basic auth
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_posts_to_correct_endpoint(heal, mock_driver):
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate()

    assert route.called
    assert str(route.calls.last.request.url) == LOCATE_DESKTOP_URL


@respx.mock
def test_desktop_locate_payload_required_fields(heal, mock_driver):
    """Lean body must carry all required fields per the locked design contract."""
    import json
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate()

    body = json.loads(route.calls.last.request.content)
    required = {"intent", "image", "os", "platform", "screen_width", "screen_height",
                "drop_aware", "request_id", "a11y_flatten"}
    missing = required - set(body.keys())
    assert not missing, f"Payload missing fields: {missing}"
    assert body["os"] == "desktop"
    assert body["platform"] == "web"
    assert body["drop_aware"] is False
    assert body["a11y_flatten"] == []
    assert isinstance(body["request_id"], str) and len(body["request_id"]) == 16


@respx.mock
def test_desktop_locate_uses_viewport_screenshot_not_full_page(heal, mock_driver):
    """Must use _take_screenshot (viewport), NOT capture_full_page_screenshot.
    Verifies the VIEWPORT vs full-page distinction from the design contract."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64) as m_vp, \
         patch("testmu_selenium._heal.capture_full_page_screenshot") as m_fp:
        heal.desktop_locate()

    m_vp.assert_called_once()
    m_fp.assert_not_called()


@respx.mock
def test_desktop_locate_sends_lt_basic_auth(heal, mock_driver, monkeypatch):
    """LT_USERNAME:LT_ACCESS_KEY encoded as Basic auth header."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    # heal fixture was created with username="user", accesskey="key"
    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate()

    expected_auth = "Basic " + base64.b64encode(b"user:key").decode()
    assert route.calls.last.request.headers["Authorization"] == expected_auth


@respx.mock
def test_desktop_locate_uses_viewport_dims_in_payload(heal, mock_driver):
    """screen_width and screen_height in the payload match window.innerWidth/innerHeight."""
    import json
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1366, 768]  # non-default dims

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate()

    body = json.loads(route.calls.last.request.content)
    assert body["screen_width"] == 1366
    assert body["screen_height"] == 768


@respx.mock
def test_desktop_locate_uses_intent_from_current_action(heal, mock_driver):
    """intent in the payload must come from current_action.operation_intent."""
    import json
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate()

    body = json.loads(route.calls.last.request.content)
    assert body["intent"] == "click the submit button"  # from action fixture


# ---------------------------------------------------------------------------
# drop_aware keyword — drag-target locates flip the payload flag (spec §10.1)
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_drop_aware_defaults_false(heal, mock_driver):
    """No kwarg → payload drop_aware is False (pre-§10 behaviour unchanged)."""
    import json
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate()

    body = json.loads(route.calls.last.request.content)
    assert body["drop_aware"] is False


@respx.mock
def test_desktop_locate_drop_aware_true_threads_into_payload(heal, mock_driver):
    """drop_aware=True (drag TARGET endpoint) → payload drop_aware is True."""
    import json
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        heal.desktop_locate(drop_aware=True)

    body = json.loads(route.calls.last.request.content)
    assert body["drop_aware"] is True


# ---------------------------------------------------------------------------
# Return type: tuple of ints
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_returns_int_tuple(heal, mock_driver):
    """desktop_locate() must return a (int, int) tuple, not floats."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [640, 360]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        result = heal.desktop_locate()

    assert isinstance(result, tuple)
    assert len(result) == 2
    css_x, css_y = result
    assert isinstance(css_x, int)
    assert isinstance(css_y, int)


# ---------------------------------------------------------------------------
# FIX 1 — Retry on non-200: fresh screenshot per attempt
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_retries_on_non_200_succeeds_on_third(heal, mock_driver):
    """FIX 1(a): [500, 500, 200] → returns coords; route called 3x; _take_screenshot 3x.
    The deleted browser_coordinate tier retried up to 3 attempts on ANY non-200
    taking a fresh screenshot each time. Reverting the retry loop breaks this.
    """
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        side_effect=[
            httpx.Response(500, json={"error": "transient-1"}),
            httpx.Response(500, json={"error": "transient-2"}),
            httpx.Response(200, json={"coordinate": [100, 200]}),
        ]
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64) as mock_ss:
        css_x, css_y = heal.desktop_locate()

    assert (css_x, css_y) == (100, 200)
    assert route.call_count == 3, f"Expected 3 POST attempts, got {route.call_count}"
    assert mock_ss.call_count == 3, (
        f"Expected _take_screenshot called 3x (fresh per attempt), got {mock_ss.call_count}"
    )


@respx.mock
def test_desktop_locate_all_non_200_raises_heal_tier_miss_after_3(heal, mock_driver):
    """FIX 1(b): all 500s → HealTierMiss; route called exactly 3 times.
    Reverting the loop so it only tries once breaks this (call_count == 1 not 3).
    """
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(500, json={"error": "boom"})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss) as exc_info:
            heal.desktop_locate()

    assert "DESKTOP_LOCATE" in str(exc_info.value)
    assert route.call_count == 3, f"Expected 3 POST attempts, got {route.call_count}"


# ---------------------------------------------------------------------------
# FIX 2 — Validate PNG BEFORE the POST
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_invalid_png_raises_before_http_call(heal, mock_driver):
    """FIX 2: garbage screenshot → HealTierMiss raised; HTTP route NOT called.
    Moving the decode+IHDR validation after the POST (the pre-fix order) breaks
    this: the garbage image would fire the API call before failing on the response.
    """
    mock_driver.execute_script.return_value = [1280, 720]
    garbage_b64 = base64.b64encode(b"not a png at all").decode()

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch.object(heal, "_take_screenshot", return_value=garbage_b64):
        with pytest.raises(HealTierMiss) as exc_info:
            heal.desktop_locate()

    assert "DESKTOP_LOCATE" in str(exc_info.value)
    assert not route.called, "HTTP route must NOT be called when screenshot is invalid PNG"


# ---------------------------------------------------------------------------
# FIX 4 — Mobile warning
# ---------------------------------------------------------------------------

def test_desktop_locate_mobile_platform_logs_warning(mock_driver, caplog):
    """FIX 4: android platformName → warning logged; tier still proceeds normally."""
    mock_driver.capabilities = {"platformName": "android", "browserName": "chrome"}
    mock_driver.execute_script.return_value = [1280, 720]
    image_b64 = _make_png_b64(1280, 720)

    mobile_action = {
        "operation_type": "click",
        "operation_intent": "click submit button",
        "use_query_v2": True,
        "version": "v3",
    }
    mobile_heal = Heal(mobile_action, mock_driver, username="user", accesskey="key",
                       test_id="t1", commit_id="c1", org_id=1)

    with respx.mock:
        respx.post(LOCATE_DESKTOP_URL).mock(
            return_value=httpx.Response(200, json={"coordinate": [100, 200]})
        )
        with patch.object(mobile_heal, "_take_screenshot", return_value=image_b64):
            with caplog.at_level(logging.WARNING, logger="testmu_selenium._heal"):
                css_x, css_y = mobile_heal.desktop_locate()

    # warning must mention device chrome / desktop assumption
    warning_msgs = [r.message for r in caplog.records if r.levelno >= logging.WARNING]
    assert any("DESKTOP_LOCATE" in m and "desktop web" in m for m in warning_msgs), (
        f"Expected mobile warning in caplog; got: {warning_msgs}"
    )
    # tier must still return coordinates (not block)
    assert (css_x, css_y) == (100, 200)


# ---------------------------------------------------------------------------
# FIX 5 — Aspect-ratio sanity warning
# ---------------------------------------------------------------------------

def test_desktop_locate_aspect_ratio_mismatch_logs_warning(heal, mock_driver, caplog):
    """FIX 5: image 1280x900 vs viewport 1280x720 → AR mismatch warning logged.
    img_ar = 1280/900 ≈ 1.422; vp_ar = 1280/720 ≈ 1.778
    deviation = |1.422 - 1.778| / 1.778 ≈ 0.200 > 0.02 → warn.
    """
    image_b64 = _make_png_b64(1280, 900)
    mock_driver.execute_script.return_value = [1280, 720]

    with respx.mock:
        respx.post(LOCATE_DESKTOP_URL).mock(
            return_value=httpx.Response(200, json={"coordinate": [100, 200]})
        )
        with patch.object(heal, "_take_screenshot", return_value=image_b64):
            with caplog.at_level(logging.WARNING, logger="testmu_selenium._heal"):
                heal.desktop_locate()

    warning_msgs = [r.message for r in caplog.records if r.levelno >= logging.WARNING]
    assert any("aspect ratio" in m.lower() for m in warning_msgs), (
        f"Expected AR warning for 1280x900 image vs 1280x720 viewport; got: {warning_msgs}"
    )


def test_desktop_locate_matching_aspect_ratio_no_warning(heal, mock_driver, caplog):
    """FIX 5: image 1280x720 vs viewport 1280x720 → no aspect-ratio warning."""
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    with respx.mock:
        respx.post(LOCATE_DESKTOP_URL).mock(
            return_value=httpx.Response(200, json={"coordinate": [100, 200]})
        )
        with patch.object(heal, "_take_screenshot", return_value=image_b64):
            with caplog.at_level(logging.WARNING, logger="testmu_selenium._heal"):
                heal.desktop_locate()

    warning_msgs = [r.message for r in caplog.records if r.levelno >= logging.WARNING]
    assert not any("aspect ratio" in m.lower() for m in warning_msgs), (
        f"Unexpected AR warning for matching dims; got: {warning_msgs}"
    )


# ---------------------------------------------------------------------------
# FIX 6 — Empty-intent short-circuit
# ---------------------------------------------------------------------------

def test_desktop_locate_empty_intent_raises_before_screenshot_and_http(mock_driver):
    """FIX 6: falsy operation_intent → HealTierMiss immediately; no screenshot, no HTTP call."""
    empty_action = {
        "operation_type": "click",
        "operation_intent": "",   # empty / falsy
        "use_query_v2": True,
        "version": "v3",
    }
    h = Heal(empty_action, mock_driver, username="user", accesskey="key",
             test_id="t1", commit_id="c1", org_id=1)

    with respx.mock:
        route = respx.post(LOCATE_DESKTOP_URL).mock(
            return_value=httpx.Response(200, json={"coordinate": [100, 200]})
        )
        with patch.object(h, "_take_screenshot") as mock_ss:
            with pytest.raises(HealTierMiss) as exc_info:
                h.desktop_locate()

    assert "DESKTOP_LOCATE" in str(exc_info.value)
    assert "empty operation_intent" in str(exc_info.value)
    mock_ss.assert_not_called()
    assert not route.called


# ---------------------------------------------------------------------------
# FIX 7 — Clamp scaled coordinates to viewport bounds
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_clamps_coordinates_to_viewport(heal, mock_driver):
    """FIX 7: coordinate [99999, 99999] with 1280x720 image+viewport → clamped to (1279, 719).
    Without clamping, css_x = 99999 (out-of-viewport), which crashes ActionChains.moveToElement.
    """
    image_b64 = _make_png_b64(1280, 720)
    mock_driver.execute_script.return_value = [1280, 720]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [99999, 99999]})
    )

    with patch.object(heal, "_take_screenshot", return_value=image_b64):
        css_x, css_y = heal.desktop_locate()

    assert css_x == 1279, f"Expected css_x clamped to 1279, got {css_x}"
    assert css_y == 719, f"Expected css_y clamped to 719, got {css_y}"
