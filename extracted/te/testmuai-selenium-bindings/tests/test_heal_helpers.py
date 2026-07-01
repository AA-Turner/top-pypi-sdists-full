"""Smoke tests for Heal helper modules (Phase A Task 11).

Covers:
- ``_helpers/_screenshot.py`` — public screenshot fns + private ``execute_cdp_command``.
- ``_helpers/_tagify.py``     — ``MOBILE_TAGIFY_SCRIPT`` constant.
- ``_helpers/_frame.py``      — ``switch_to_frame_by_xpath`` + ``ShadowContext``.

Phase A keeps these as thin import/wiring smoke tests; deeper behavioural coverage
lands in later phases when wired into the public action surface.
"""
from __future__ import annotations

from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Module import smoke
# ---------------------------------------------------------------------------

def test_screenshot_module_imports():
    from testmu_selenium._helpers import _screenshot

    assert hasattr(_screenshot, "get_browser_screenshot_as_base64")
    assert hasattr(_screenshot, "make_tagged_screenshot")
    assert hasattr(_screenshot, "capture_full_page_screenshot")
    assert hasattr(_screenshot, "_take_screenshot")
    # Private CDP helper required by capture_full_page_screenshot
    assert hasattr(_screenshot, "execute_cdp_command")


def test_capture_full_page_screenshot_no_viewport_resize_restores_scroll():
    """Full-page capture must NOT resize the viewport via setDeviceMetricsOverride —
    forcing the viewport to the full scrollHeight collapses scrollY to 0 (scroll-to-top)
    and balloons vh/%-relative layout, corrupting the locate screenshot. It captures via
    captureBeyondViewport + an explicit clip and restores the scroll position."""
    from unittest.mock import patch
    from testmu_selenium._helpers import _screenshot

    def fake_execute_script(script, *args):
        if "scrollWidth" in script:
            return {"width": 1920, "height": 8000}
        if "window.scrollX" in script:
            return [120, 340]
        return None

    driver = MagicMock()
    driver.execute_script.side_effect = fake_execute_script

    cdp_calls = []

    def fake_cdp(drv, cmd, params=None):
        cdp_calls.append((cmd, params or {}))
        return {"data": "ZmFrZQ=="} if cmd == "Page.captureScreenshot" else None

    with patch.object(_screenshot, "execute_cdp_command", side_effect=fake_cdp):
        data = _screenshot.capture_full_page_screenshot(driver)

    assert data == "ZmFrZQ=="

    cmds = [c for c, _ in cdp_calls]
    assert "Page.captureScreenshot" in cmds
    # The viewport-resize that caused the scroll-to-top must be gone.
    assert "Emulation.setDeviceMetricsOverride" not in cmds
    assert "Emulation.clearDeviceMetricsOverride" not in cmds

    shot = next(p for c, p in cdp_calls if c == "Page.captureScreenshot")
    assert shot.get("captureBeyondViewport") is True
    assert shot["clip"]["width"] == 1920 and shot["clip"]["height"] == 8000
    assert "scale" in shot["clip"]

    # Scroll position snapshotted and restored (no net scroll side-effect).
    scroll_restore = [
        c for c in driver.execute_script.call_args_list if "scrollTo" in c.args[0]
    ]
    assert scroll_restore, "scroll position was not restored after capture"
    assert scroll_restore[-1].args[1:] == (120, 340)


def test_tagify_module_imports():
    from testmu_selenium._helpers._tagify import MOBILE_TAGIFY_SCRIPT

    # Standalone fallback is None; inside the host runtime it may be a non-empty str.
    assert MOBILE_TAGIFY_SCRIPT is None or isinstance(MOBILE_TAGIFY_SCRIPT, str)


def test_frame_module_imports():
    from testmu_selenium._helpers import _frame

    assert hasattr(_frame, "switch_to_frame_by_xpath")
    assert hasattr(_frame, "ShadowContext")


# ---------------------------------------------------------------------------
# get_browser_screenshot_as_base64
# ---------------------------------------------------------------------------

def test_get_browser_screenshot_falls_back_to_selenium_on_non_ios():
    from testmu_selenium._helpers._screenshot import get_browser_screenshot_as_base64

    mock_driver = MagicMock()
    # Explicitly set non-iOS so the iOS branch doesn't run accidentally.
    mock_driver.capabilities = {"platformName": "chrome"}
    mock_driver.get_screenshot_as_base64.return_value = "FAKE_BASE64"

    result = get_browser_screenshot_as_base64(mock_driver)

    assert result == "FAKE_BASE64"
    mock_driver.get_screenshot_as_base64.assert_called_once()


def test_get_browser_screenshot_uses_ios_viewport_path_when_available():
    from testmu_selenium._helpers._screenshot import get_browser_screenshot_as_base64

    mock_driver = MagicMock()
    mock_driver.capabilities = {"platformName": "iOS"}
    mock_driver.execute_script.return_value = "IOS_BASE64"

    result = get_browser_screenshot_as_base64(mock_driver)

    assert result == "IOS_BASE64"
    mock_driver.execute_script.assert_called_once_with("mobile: viewportScreenshot")
    # The selenium fallback should NOT be invoked when iOS path returned a value.
    mock_driver.get_screenshot_as_base64.assert_not_called()


# ---------------------------------------------------------------------------
# _take_screenshot — CDP guard / fallback
# ---------------------------------------------------------------------------

def test_take_screenshot_falls_back_when_selenium_test_agent_absent():
    """In bindings runtime ``selenium_test_agent`` is unavailable; _take_screenshot
    must transparently fall through to the Selenium screenshot path."""
    from testmu_selenium._helpers._screenshot import _take_screenshot

    mock_driver = MagicMock()
    mock_driver.capabilities = {"platformName": "chrome"}
    mock_driver.get_screenshot_as_base64.return_value = "FALLBACK_B64"

    result = _take_screenshot(mock_driver)

    assert result == "FALLBACK_B64"


# ---------------------------------------------------------------------------
# switch_to_frame_by_xpath — boundary handling
# ---------------------------------------------------------------------------

def test_switch_to_frame_by_xpath_no_op_on_empty_string():
    """Empty/None frame info is a no-op and returns ``None`` (no shadow ctx)."""
    from testmu_selenium._helpers._frame import switch_to_frame_by_xpath

    mock_driver = MagicMock()

    # Empty string short-circuits before json.loads — should not call driver at all.
    assert switch_to_frame_by_xpath(mock_driver, "") is None
    mock_driver.find_element.assert_not_called()
    mock_driver.switch_to.frame.assert_not_called()


def test_switch_to_frame_by_xpath_handles_invalid_json_gracefully():
    """Invalid frame_info should be caught and return None (verbatim port behaviour)."""
    from testmu_selenium._helpers._frame import switch_to_frame_by_xpath

    mock_driver = MagicMock()
    # "not-json" will trip json.loads — outer try/except returns None.
    assert switch_to_frame_by_xpath(mock_driver, "not-json") is None


def test_switch_to_frame_by_xpath_iframe_branch_calls_switch():
    """A single-iframe frame_info should resolve via XPATH and call driver.switch_to.frame."""
    from testmu_selenium._helpers._frame import switch_to_frame_by_xpath

    mock_driver = MagicMock()
    iframe_el = MagicMock(name="iframe_el")
    mock_driver.find_element.return_value = iframe_el

    frame_info = '[{"iframe": "//iframe[@id=\\"f1\\"]"}]'
    result = switch_to_frame_by_xpath(mock_driver, frame_info)

    assert result is None  # iframe branch resets shadow_ctx → returns None
    mock_driver.switch_to.frame.assert_called_once_with(iframe_el)
