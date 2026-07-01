"""Tests for Heal.desktop_locate_full_page() — DESKTOP_LOCATE_FULL_PAGE tier.

POSTs to /v2/locate/desktop with a FULL-PAGE screenshot (screen_width=0,
screen_height=0), then scales the returned image-pixel coordinate to page-CSS-px:
    page_x = raw_x * page_width  / image_width
    page_y = raw_y * page_height / image_height
where page_width/height come from document.documentElement scrollWidth/scrollHeight
and image_width/height come from the PNG IHDR header.

Key contracts:
  - Full-page screenshot (capture_full_page_screenshot), NOT viewport (_take_screenshot)
  - Lean body with screen_width=0, screen_height=0 (full-page locate contract)
  - Miss detection: HTTP 200 with coordinate==[0,0] → HealTierMiss
  - PNG validated BEFORE the POST (corrupt screenshot never burns an API call)
  - Empty intent short-circuit: HealTierMiss immediately, no screenshot, no HTTP call
"""
from __future__ import annotations

import base64
import io
import struct
import zlib
from unittest.mock import MagicMock, patch, call

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
    """Create a minimal valid PNG of given dims (PIL or manual IHDR)."""
    try:
        from PIL import Image
        img = Image.new("RGB", (width, height), color=(100, 100, 100))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except ImportError:
        sig = b"\x89PNG\r\n\x1a\n"
        ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
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
    driver.session_id = "sess-dlf-1"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    # Default page dims: 1200x3000 CSS px (scrollWidth x scrollHeight)
    driver.execute_script.return_value = [1200, 3000]
    return driver


@pytest.fixture()
def action():
    return {
        "operation_type": "scroll_until_element",
        "operation_intent": "find the checkout button",
        "use_query_v2": True,
        "version": "v3",
    }


@pytest.fixture()
def heal(action, mock_driver):
    return Heal(action, mock_driver, username="user", accesskey="key",
                automind_url=AUTOMIND_URL, test_id="t1", commit_id="c1", org_id=1)


# ---------------------------------------------------------------------------
# Coordinate scaling — the core contract
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_scales_image_coords_to_page_css(heal, mock_driver):
    """COORDINATE SCALING PROOF: image 2400x6000 px, page dims 1200x3000 CSS px.
    Scale factor = 1200/2400 = 0.5 for X, 3000/6000 = 0.5 for Y.
    Raw coordinate (1200, 3000) → page coord (600, 1500).
    Reverting the page_x = raw_x * page_width / image_width scaling breaks this.
    """
    image_b64 = _make_png_b64(2400, 6000)
    mock_driver.execute_script.return_value = [1200, 3000]  # page dims

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [1200, 3000]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        result = heal.desktop_locate_full_page()

    # page_x = int(1200 * 1200 / 2400) = 600
    # page_y = int(3000 * 3000 / 6000) = 1500
    assert result == (600, 1500), (
        f"Expected (600, 1500), got {result} (scaling bug in desktop_locate_full_page)"
    )


@respx.mock
def test_desktop_locate_full_page_identity_scale_when_image_equals_page(heal, mock_driver):
    """When image dims == page dims, scale=1.0 → page coord == raw coord."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [600, 1500]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        result = heal.desktop_locate_full_page()

    assert result == (600, 1500)


# ---------------------------------------------------------------------------
# Miss detection: [0,0] coordinate is not-found (NOT 404)
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_zero_coordinate_raises_heal_tier_miss(heal, mock_driver):
    """HTTP 200 with coordinate==[0,0] must raise HealTierMiss."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [0, 0]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss) as exc_info:
            heal.desktop_locate_full_page()

    assert "DESKTOP_LOCATE_FULL_PAGE" in str(exc_info.value)


@respx.mock
def test_desktop_locate_full_page_null_coordinate_raises_heal_tier_miss(heal, mock_driver):
    """HTTP 200 with coordinate==null → HealTierMiss."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": None})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss):
            heal.desktop_locate_full_page()


# ---------------------------------------------------------------------------
# Non-200 after retries → HealTierMiss
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_non_200_raises_heal_tier_miss_after_3(heal, mock_driver):
    """All 3 attempts return non-200 → HealTierMiss; route called exactly 3 times."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(500, json={"error": "server error"})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        with pytest.raises(HealTierMiss) as exc_info:
            heal.desktop_locate_full_page()

    assert "DESKTOP_LOCATE_FULL_PAGE" in str(exc_info.value)
    assert route.call_count == 3, f"Expected 3 POST attempts, got {route.call_count}"


@respx.mock
def test_desktop_locate_full_page_retries_on_non_200_succeeds_on_third(heal, mock_driver):
    """[500, 500, 200] → returns coords; route called 3x."""
    image_b64 = _make_png_b64(2400, 6000)
    mock_driver.execute_script.return_value = [1200, 3000]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        side_effect=[
            httpx.Response(500, json={"error": "transient-1"}),
            httpx.Response(500, json={"error": "transient-2"}),
            httpx.Response(200, json={"coordinate": [600, 1500]}),
        ]
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        result = heal.desktop_locate_full_page()

    # raw (600, 1500), image 2400x6000, page 1200x3000
    # page_x = int(600 * 1200 / 2400) = 300, page_y = int(1500 * 3000 / 6000) = 750
    assert result == (300, 750)
    assert route.call_count == 3, f"Expected 3 POST attempts, got {route.call_count}"


# ---------------------------------------------------------------------------
# Invalid PNG → HealTierMiss (validated BEFORE POST)
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_invalid_png_raises_before_http_call(heal, mock_driver):
    """Garbage screenshot → HealTierMiss raised; HTTP route NOT called.
    Validation must happen before the POST so a corrupt screenshot never burns an API call."""
    mock_driver.execute_script.return_value = [1200, 3000]
    garbage_b64 = base64.b64encode(b"not a png at all").decode()

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [100, 200]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=garbage_b64):
        with pytest.raises(HealTierMiss) as exc_info:
            heal.desktop_locate_full_page()

    assert "DESKTOP_LOCATE_FULL_PAGE" in str(exc_info.value)
    assert not route.called, "HTTP route must NOT be called when screenshot is invalid PNG"


# ---------------------------------------------------------------------------
# Empty intent short-circuit
# ---------------------------------------------------------------------------

def test_desktop_locate_full_page_empty_intent_raises_before_screenshot_and_http(mock_driver):
    """Falsy operation_intent → HealTierMiss immediately; no screenshot, no HTTP call."""
    empty_action = {
        "operation_type": "scroll_until_element",
        "operation_intent": "",   # empty / falsy
        "use_query_v2": True,
        "version": "v3",
    }
    h = Heal(empty_action, mock_driver, username="user", accesskey="key",
             automind_url=AUTOMIND_URL, test_id="t1", commit_id="c1", org_id=1)

    with respx.mock:
        route = respx.post(LOCATE_DESKTOP_URL).mock(
            return_value=httpx.Response(200, json={"coordinate": [100, 200]})
        )
        with patch("testmu_selenium._heal.capture_full_page_screenshot") as mock_fp:
            with pytest.raises(HealTierMiss) as exc_info:
                h.desktop_locate_full_page()

    assert "DESKTOP_LOCATE_FULL_PAGE" in str(exc_info.value)
    assert "empty operation_intent" in str(exc_info.value)
    mock_fp.assert_not_called()
    assert not route.called


# ---------------------------------------------------------------------------
# Lean body: screen_width=0, screen_height=0
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_payload_has_zero_screen_dims(heal, mock_driver):
    """Lean body must carry screen_width=0 and screen_height=0 (full-page contract)."""
    import json as _json
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [600, 1500]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        heal.desktop_locate_full_page()

    body = _json.loads(route.calls.last.request.content)
    assert body["screen_width"] == 0, (
        f"Expected screen_width=0 (full-page locate contract), got {body['screen_width']}"
    )
    assert body["screen_height"] == 0, (
        f"Expected screen_height=0 (full-page locate contract), got {body['screen_height']}"
    )


@respx.mock
def test_desktop_locate_full_page_payload_required_fields(heal, mock_driver):
    """Lean body must carry all required fields."""
    import json as _json
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [600, 1500]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        heal.desktop_locate_full_page()

    body = _json.loads(route.calls.last.request.content)
    required = {"intent", "image", "os", "platform", "screen_width", "screen_height",
                "drop_aware", "request_id", "a11y_flatten"}
    missing = required - set(body.keys())
    assert not missing, f"Payload missing fields: {missing}"
    assert body["os"] == "desktop"
    assert body["platform"] == "web"
    assert body["drop_aware"] is False
    assert body["a11y_flatten"] == []


# ---------------------------------------------------------------------------
# Uses full-page screenshot (not viewport)
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_uses_full_page_not_viewport_screenshot(heal, mock_driver):
    """Must call capture_full_page_screenshot (NOT _take_screenshot/viewport)."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [600, 1500]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64) as m_fp, \
         patch.object(heal, "_take_screenshot") as m_vp:
        heal.desktop_locate_full_page()

    m_fp.assert_called_once()
    m_vp.assert_not_called()


# ---------------------------------------------------------------------------
# Clamp coordinates to page bounds
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_clamps_coordinates_to_page_bounds(heal, mock_driver):
    """Out-of-bounds coordinate clamped to [0, page_dim-1]."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [99999, 99999]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        result = heal.desktop_locate_full_page()

    # With image == page dims: raw=99999,99999 → unscaled then clamped to 1199, 2999
    assert result[0] == 1199, f"Expected x clamped to 1199, got {result[0]}"
    assert result[1] == 2999, f"Expected y clamped to 2999, got {result[1]}"


# ---------------------------------------------------------------------------
# Return type: tuple of ints
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_returns_int_tuple(heal, mock_driver):
    """desktop_locate_full_page() must return a (int, int) tuple."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [600, 1500]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        result = heal.desktop_locate_full_page()

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], int)
    assert isinstance(result[1], int)


# ---------------------------------------------------------------------------
# Uses Basic auth
# ---------------------------------------------------------------------------

@respx.mock
def test_desktop_locate_full_page_sends_basic_auth(heal, mock_driver):
    """LT_USERNAME:LT_ACCESS_KEY encoded as Basic auth header."""
    image_b64 = _make_png_b64(1200, 3000)
    mock_driver.execute_script.return_value = [1200, 3000]

    route = respx.post(LOCATE_DESKTOP_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [600, 1500]})
    )

    with patch("testmu_selenium._heal.capture_full_page_screenshot", return_value=image_b64):
        heal.desktop_locate_full_page()

    expected_auth = "Basic " + base64.b64encode(b"user:key").decode()
    assert route.calls.last.request.headers["Authorization"] == expected_auth
