"""Tests for testmu_selenium._helpers.scroll — all mode × target combinations."""
from __future__ import annotations

from unittest.mock import MagicMock, call, patch

import pytest

from testmu_selenium._helpers.scroll import scroll


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _driver(exec_return=None):
    driver = MagicMock()
    driver.execute_script.return_value = exec_return
    return driver


# ---------------------------------------------------------------------------
# mode='pixels' — window
# ---------------------------------------------------------------------------

class TestScrollPixelsWindow:
    def test_down_positive_scroll_by(self):
        driver = _driver()
        scroll(driver, direction='down', amount=200, mode='pixels')
        driver.execute_script.assert_any_call("window.scrollBy(0, 200)")

    def test_up_negative_scroll_by(self):
        driver = _driver()
        scroll(driver, direction='up', amount=100, mode='pixels')
        driver.execute_script.assert_any_call("window.scrollBy(0, -100)")

    def test_right_horizontal_positive(self):
        driver = _driver()
        scroll(driver, direction='right', amount=50, mode='pixels')
        driver.execute_script.assert_any_call("window.scrollBy(50, 0)")

    def test_left_horizontal_negative(self):
        driver = _driver()
        scroll(driver, direction='left', amount=50, mode='pixels')
        driver.execute_script.assert_any_call("window.scrollBy(-50, 0)")


# ---------------------------------------------------------------------------
# mode='pixels' — element
# ---------------------------------------------------------------------------

class TestScrollPixelsElement:
    def test_element_passed_as_js_argument_vertical(self):
        driver = _driver()
        el = MagicMock()
        scroll(driver, direction='down', amount=300, mode='pixels', element=el)
        driver.execute_script.assert_any_call(
            "arguments[0].scrollBy(0, arguments[1])", el, 300
        )

    def test_element_up_negative_delta(self):
        driver = _driver()
        el = MagicMock()
        scroll(driver, direction='up', amount=100, mode='pixels', element=el)
        driver.execute_script.assert_any_call(
            "arguments[0].scrollBy(0, arguments[1])", el, -100
        )

    def test_element_horizontal_right(self):
        driver = _driver()
        el = MagicMock()
        scroll(driver, direction='right', amount=80, mode='pixels', element=el)
        driver.execute_script.assert_any_call(
            "arguments[0].scrollBy(arguments[1], 0)", el, 80
        )


# ---------------------------------------------------------------------------
# mode='percentage' — window
# ---------------------------------------------------------------------------

class TestScrollPercentageWindow:
    def test_reads_inner_height_then_scrolls(self):
        driver = MagicMock()
        # First execute_script call returns window.innerHeight
        driver.execute_script.side_effect = [500, None]
        scroll(driver, direction='down', amount=50, mode='percentage')

        calls = driver.execute_script.call_args_list
        # First call reads height
        assert "innerHeight" in calls[0][0][0]
        # Second call scrolls: 500 * 50 / 100 = 250
        assert calls[1] == call("window.scrollBy(0, 250)")

    def test_up_direction_negative_delta(self):
        driver = MagicMock()
        driver.execute_script.side_effect = [400, None]
        scroll(driver, direction='up', amount=25, mode='percentage')

        calls = driver.execute_script.call_args_list
        # 400 * 25 / 100 * -1 = -100
        assert calls[1] == call("window.scrollBy(0, -100)")


# ---------------------------------------------------------------------------
# mode='times' — window
# ---------------------------------------------------------------------------

class TestScrollTimesWindow:
    def test_loops_n_times(self):
        driver = MagicMock()
        # First call returns innerHeight, subsequent calls are scrollBy (return None)
        driver.execute_script.side_effect = [600] + [None] * 3
        scroll(driver, direction='down', amount=3, mode='times')

        # Expect: 1 innerHeight read + 3 scrollBy calls
        assert driver.execute_script.call_count == 4
        scroll_calls = [
            c for c in driver.execute_script.call_args_list
            if "scrollBy" in str(c)
        ]
        assert len(scroll_calls) == 3

    def test_up_loops_with_negative_delta(self):
        driver = MagicMock()
        driver.execute_script.side_effect = [800] + [None] * 2
        scroll(driver, direction='up', amount=2, mode='times')

        scroll_calls = [
            c for c in driver.execute_script.call_args_list
            if "scrollBy" in str(c)
        ]
        assert len(scroll_calls) == 2
        # Each scrollBy uses negative value
        for c in scroll_calls:
            assert c == call("window.scrollBy(0, -800)")


# ---------------------------------------------------------------------------
# mode='times' — element
# ---------------------------------------------------------------------------

class TestScrollTimesElement:
    def test_element_down_uses_scroll_by_per_iteration(self):
        driver = _driver(exec_return=500)  # clientHeight read returns 500
        el = MagicMock()
        scroll(driver, direction='down', amount=3, mode='times', element=el)

        scroll_by_calls = [
            c for c in driver.execute_script.call_args_list
            if c == call("arguments[0].scrollBy(0, arguments[1])", el, 500)
        ]
        assert len(scroll_by_calls) == 3

    def test_element_does_not_dispatch_wheel_event(self):
        driver = _driver(exec_return=500)
        el = MagicMock()
        scroll(driver, direction='down', amount=3, mode='times', element=el)

        assert not any(
            "WheelEvent" in str(c) for c in driver.execute_script.call_args_list
        )

    def test_element_up_negative_delta(self):
        driver = _driver(exec_return=400)
        el = MagicMock()
        scroll(driver, direction='up', amount=2, mode='times', element=el)

        scroll_by_calls = [
            c for c in driver.execute_script.call_args_list
            if c == call("arguments[0].scrollBy(0, arguments[1])", el, -400)
        ]
        assert len(scroll_by_calls) == 2

    def test_element_horizontal_right_uses_client_width(self):
        driver = _driver(exec_return=300)  # clientWidth read returns 300
        el = MagicMock()
        scroll(driver, direction='right', amount=2, mode='times', element=el)

        scroll_by_calls = [
            c for c in driver.execute_script.call_args_list
            if c == call("arguments[0].scrollBy(arguments[1], 0)", el, 300)
        ]
        assert len(scroll_by_calls) == 2


# ---------------------------------------------------------------------------
# mode='none'
# ---------------------------------------------------------------------------

class TestScrollNone:
    def test_top_calls_scroll_to_zero(self):
        driver = _driver()
        scroll(driver, direction='top', mode='none')
        driver.execute_script.assert_any_call("window.scrollTo(0, 0)")

    def test_bottom_calls_scroll_to_scroll_height(self):
        driver = _driver()
        scroll(driver, direction='bottom', mode='none')
        driver.execute_script.assert_any_call(
            "window.scrollTo(0, document.documentElement.scrollHeight)"
        )

    def test_element_top_sets_scroll_top_zero(self):
        driver = _driver()
        el = MagicMock()
        scroll(driver, direction='top', mode='none', element=el)
        driver.execute_script.assert_any_call(
            "arguments[0].scrollTop = 0", el
        )

    def test_element_bottom_sets_scroll_top_scroll_height(self):
        driver = _driver()
        el = MagicMock()
        scroll(driver, direction='bottom', mode='none', element=el)
        driver.execute_script.assert_any_call(
            "arguments[0].scrollTop = arguments[0].scrollHeight", el
        )


# ---------------------------------------------------------------------------
# Settle sleep parity
# ---------------------------------------------------------------------------

class TestScrollSettleSleep:
    def test_time_sleep_called_once_after_scroll(self):
        driver = _driver()
        with patch("testmu_selenium._helpers.scroll.time.sleep") as mock_sleep:
            scroll(driver, direction='down', amount=100, mode='pixels')
        mock_sleep.assert_called_once_with(1)

    def test_sleep_called_for_none_mode_too(self):
        driver = _driver()
        with patch("testmu_selenium._helpers.scroll.time.sleep") as mock_sleep:
            scroll(driver, direction='top', mode='none')
        mock_sleep.assert_called_once_with(1)
