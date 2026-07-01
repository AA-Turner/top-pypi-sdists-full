"""capture_full_page_screenshot must settle the DOM before any capture work.

The full-page capture settles, measures, snapshots scroll, captures, then restores
scroll. If the DOM hasn't settled, the dimensions/scroll snapshot are stale and the
post-capture scroll restore mislands, corrupting the follow-up read. A 1s settle wait
*before* the dimension/snapshot/capture work — and another before the restore — keeps
the layout stable. This guards that ordering: settle -> snapshot -> capture -> settle
-> restore.
"""
from unittest.mock import MagicMock, patch

import testmu_selenium._helpers._screenshot as screenshot_mod
from testmu_selenium._helpers._screenshot import capture_full_page_screenshot


def test_full_page_capture_settle_waits_bracket_capture_and_restore():
    events: list[str] = []
    metrics = {"width": 1000, "height": 2000}

    def _execute_script(script, *args):
        if "scrollHeight" in script:        # full-page metrics query
            return metrics
        if "scrollX" in script:             # scroll snapshot
            events.append("snapshot")
            return [10, 20]
        if "scrollTo" in script:            # scroll restore
            events.append("restore")
            return None
        return None

    driver = MagicMock(name="driver")
    driver.execute_script.side_effect = _execute_script

    def _cdp(_driver, cmd, _params):
        events.append(f"capture:{cmd}")
        return {"data": "FAKE_B64"}

    def _sleep(secs):
        events.append(f"sleep:{secs}")

    with patch.object(screenshot_mod, "execute_cdp_command", side_effect=_cdp), \
         patch.object(screenshot_mod.time, "sleep", side_effect=_sleep):
        out = capture_full_page_screenshot(driver)

    assert out == "FAKE_B64"
    # Settle fires FIRST (before the scroll snapshot/capture), then a second settle before
    # restore. Ordered: wait -> snapshot -> capture -> wait -> restore.
    assert events == [
        "sleep:1",
        "snapshot",
        "capture:Page.captureScreenshot",
        "sleep:1",
        "restore",
    ]
