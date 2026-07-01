"""Tests for scroll_until_element() — V3 vision-agent SCROLL_UNTIL_ELEMENT verb.

Mirrors the record-time Step-1 locate flow:
  full-page screenshot -> POST /v2/locate/desktop -> scale image-space coord to
  page-space -> window.scrollTo(centered).

Network + screenshot are mocked; tests never hit real automind.
"""
from __future__ import annotations

import base64
import io
import json
from unittest.mock import MagicMock, patch

import httpx
import pytest
import respx
from selenium.common.exceptions import NoSuchElementException

AUTOMIND_URL = "https://kaneai-api.lambdatest.com"
LOCATE_URL = f"{AUTOMIND_URL}/v2/locate/desktop"

MODULE = "testmu_selenium._action_scroll_until_element"


def _make_png_b64(width: int, height: int) -> str:
    from PIL import Image
    img = Image.new("RGB", (width, height), color=(128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "sess-sue-1"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    return driver


# ---------------------------------------------------------------------------
# Export / callable
# ---------------------------------------------------------------------------

def test_scroll_until_element_is_exported_and_callable():
    import testmu_selenium
    assert hasattr(testmu_selenium, "scroll_until_element")
    assert callable(testmu_selenium.scroll_until_element)


# ---------------------------------------------------------------------------
# Success: scaled + centered scrollTo
# ---------------------------------------------------------------------------

@respx.mock
def test_scroll_until_element_scrolls_to_scaled_centered_coords(mock_driver, monkeypatch):
    # page 1920x4000, viewport 1920x1080, image 960x2000 -> scale 2.0
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "key")
    monkeypatch.delenv("AUTOMIND_URL", raising=False)

    page_w, page_h, vp_w, vp_h = 1920, 4000, 1920, 1080
    fake_png = _make_png_b64(960, 2000)

    # execute_script: 1st call returns dims list, 2nd call is the scrollTo
    mock_driver.execute_script.side_effect = [[page_w, page_h, vp_w, vp_h], None]

    route = respx.post(LOCATE_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [300, 1000]})
    )

    with patch(f"{MODULE}.capture_full_page_screenshot", return_value=fake_png):
        from testmu_selenium import scroll_until_element
        scroll_until_element(mock_driver, description="verify code button")

    assert route.called
    # page_x = 300 * (1920/960) = 600 ; page_y = 1000 * (4000/2000) = 2000
    # scrollTo x = max(0, 600 - 1920//2) = max(0, -360) = 0  (clamp)
    # scrollTo y = max(0, 2000 - 1080//2) = 2000 - 540 = 1460
    scroll_call = mock_driver.execute_script.call_args_list[-1]
    assert "scrollTo" in scroll_call.args[0]
    assert scroll_call.args[1] == 0
    assert scroll_call.args[2] == 1460


# ---------------------------------------------------------------------------
# Request shape: endpoint, intent, basic auth
# ---------------------------------------------------------------------------

@respx.mock
def test_scroll_until_element_posts_locate_desktop_with_intent_and_auth(mock_driver, monkeypatch):
    monkeypatch.setenv("LT_USERNAME", "alice")
    monkeypatch.setenv("LT_ACCESS_KEY", "secret")
    monkeypatch.delenv("AUTOMIND_URL", raising=False)

    mock_driver.execute_script.side_effect = [[1920, 4000, 1920, 1080], None]
    fake_png = _make_png_b64(960, 2000)

    route = respx.post(LOCATE_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [300, 1000]})
    )

    with patch(f"{MODULE}.capture_full_page_screenshot", return_value=fake_png):
        from testmu_selenium import scroll_until_element
        scroll_until_element(mock_driver, description="verify code button")

    req = route.calls.last.request
    assert str(req.url) == LOCATE_URL
    body = json.loads(req.content)
    assert body["intent"] == "verify code button"
    assert body["image"] == fake_png
    assert body["os"] == "desktop"
    assert body["platform"] == "web"
    assert body["drop_aware"] is False

    expected_auth = "Basic " + base64.b64encode(b"alice:secret").decode()
    assert req.headers["Authorization"] == expected_auth


# ---------------------------------------------------------------------------
# Not found: [0,0] -> raise
# ---------------------------------------------------------------------------

@respx.mock
def test_scroll_until_element_zero_coordinate_raises(mock_driver, monkeypatch):
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "key")
    monkeypatch.delenv("AUTOMIND_URL", raising=False)

    mock_driver.execute_script.side_effect = [[1920, 4000, 1920, 1080], None]
    fake_png = _make_png_b64(960, 2000)

    respx.post(LOCATE_URL).mock(
        return_value=httpx.Response(200, json={"coordinate": [0, 0]})
    )

    with patch(f"{MODULE}.capture_full_page_screenshot", return_value=fake_png):
        from testmu_selenium import scroll_until_element
        with pytest.raises(NoSuchElementException):
            scroll_until_element(mock_driver, description="missing thing")

    # must not have scrolled
    scroll_calls = [c for c in mock_driver.execute_script.call_args_list
                    if c.args and isinstance(c.args[0], str) and "scrollTo" in c.args[0]]
    assert scroll_calls == []


@respx.mock
def test_scroll_until_element_missing_coordinate_raises(mock_driver, monkeypatch):
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "key")
    monkeypatch.delenv("AUTOMIND_URL", raising=False)

    mock_driver.execute_script.side_effect = [[1920, 4000, 1920, 1080], None]
    fake_png = _make_png_b64(960, 2000)

    respx.post(LOCATE_URL).mock(
        return_value=httpx.Response(200, json={"confidence": 0.0})
    )

    with patch(f"{MODULE}.capture_full_page_screenshot", return_value=fake_png):
        from testmu_selenium import scroll_until_element
        with pytest.raises(NoSuchElementException):
            scroll_until_element(mock_driver, description="missing thing")


@respx.mock
def test_scroll_until_element_non_200_raises(mock_driver, monkeypatch):
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "key")
    monkeypatch.delenv("AUTOMIND_URL", raising=False)

    mock_driver.execute_script.side_effect = [[1920, 4000, 1920, 1080], None]
    fake_png = _make_png_b64(960, 2000)

    respx.post(LOCATE_URL).mock(
        return_value=httpx.Response(500, json={"error": "boom"})
    )

    with patch(f"{MODULE}.capture_full_page_screenshot", return_value=fake_png):
        from testmu_selenium import scroll_until_element
        with pytest.raises(NoSuchElementException):
            scroll_until_element(mock_driver, description="thing")


# ---------------------------------------------------------------------------
# URL resolution — must honor AUTEUR_AUTOMIND (parity with _config resolver)
# ---------------------------------------------------------------------------


def test_resolve_automind_url_honors_auteur_automind(monkeypatch):
    """scroll_until's _resolve_automind_url() returns the binding config value.

    Inject the expected value directly into _config._config (auto-restored by
    monkeypatch).  The env resolution chain (AUTEUR_AUTOMIND > AUTOMIND_URL > prod)
    is tested in test_config_url_resolution.py; here we verify that
    _resolve_automind_url() delegates to _config.get("automind_url").
    """
    import importlib
    import testmu_selenium._config as _config_mod

    # Simulate config resolved with AUTEUR_AUTOMIND winning — inject directly.
    monkeypatch.setitem(_config_mod._config, "automind_url", "https://auteur-automind.example.com")
    module = importlib.import_module(MODULE)
    assert module._resolve_automind_url() == "https://auteur-automind.example.com"
