"""Tests for testmu_selenium.navigate — settle prior nav, then driver.get."""
from __future__ import annotations

import time
from unittest.mock import MagicMock

import pytest
from selenium.common.exceptions import TimeoutException, WebDriverException

import testmu_selenium
from testmu_selenium._helpers import navigate as navigate_module


def _make_driver(ready_states, current_urls=None):
    """Build a mock driver where execute_script("return document.readyState") and
    current_url return successive values from the provided sequences. Last value
    is repeated when the sequence runs out (mirrors a stable terminal state).
    """
    driver = MagicMock()
    rs_iter = iter(ready_states)
    last_rs = ready_states[-1]
    def _exec_script(script, *args):
        nonlocal last_rs
        if "readyState" in script:
            try:
                last_rs = next(rs_iter)
            except StopIteration:
                pass
            return last_rs
        return None
    driver.execute_script.side_effect = _exec_script

    if current_urls is None:
        driver.current_url = "https://example.com/initial"
    else:
        url_iter = iter(current_urls)
        last_url = current_urls[-1]
        def _current_url(self=driver):
            nonlocal last_url
            try:
                last_url = next(url_iter)
            except StopIteration:
                pass
            return last_url
        type(driver).current_url = property(lambda self: _current_url())
    return driver


class TestNavigateHappyPath:
    def test_no_prior_nav_in_progress_calls_driver_get_immediately(self):
        # readyState is 'complete' on first poll, URL stable → no settle wait
        driver = _make_driver(ready_states=["complete"], current_urls=["https://x.com"])
        target = "https://ipinfo.io"
        start = time.monotonic()
        testmu_selenium.navigate(driver, target)
        elapsed = time.monotonic() - start

        driver.get.assert_called_once_with(target)
        # Detection window is ~500ms but loop breaks immediately when stable.
        # Allow generous bound for CI flakiness; happy path should be sub-second.
        assert elapsed < 1.0


class TestNavigateDetectsInProgress:
    def test_ready_state_loading_triggers_settle_wait(self):
        # First poll sees 'loading' → nav_in_progress = True → wait for 'complete'
        # WebDriverWait calls execute_script repeatedly until the lambda returns truthy.
        driver = _make_driver(
            ready_states=["loading", "loading", "complete"],
            current_urls=["https://x.com"],
        )
        target = "https://ipinfo.io"
        testmu_selenium.navigate(driver, target)

        # driver.get is called after the settle wait satisfies
        driver.get.assert_called_once_with(target)
        # execute_script is called multiple times (detect + settle wait polls)
        assert driver.execute_script.call_count >= 2

    def test_url_change_triggers_settle_wait(self):
        # First poll: readyState == 'complete', but URL has changed since baseline
        # → nav_in_progress = True → wait for readyState 'complete' (already true,
        # so wait satisfies immediately on first re-check)
        urls = [
            "https://google.com",         # baseline
            "https://google.com/search",  # changed → nav detected
            "https://google.com/search",
        ]
        driver = _make_driver(
            ready_states=["complete"],  # always complete
            current_urls=urls,
        )
        testmu_selenium.navigate(driver, "https://ipinfo.io")
        driver.get.assert_called_once_with("https://ipinfo.io")


class TestNavigateRobustness:
    def test_webdriver_exception_during_detection_does_not_crash(self):
        # execute_script raises WebDriverException — loop should swallow + continue
        driver = MagicMock()
        # First call raises, second returns 'complete' to allow poll to find a stable state
        driver.execute_script.side_effect = [
            WebDriverException("transient"),
            "complete",
            "complete",
            "complete",
            "complete",
            "complete",
            "complete",
            "complete",
            "complete",
            "complete",
        ]
        driver.current_url = "https://x.com"
        testmu_selenium.navigate(driver, "https://ipinfo.io")
        driver.get.assert_called_once_with("https://ipinfo.io")

    def test_settle_timeout_does_not_crash_falls_through_to_get(self, monkeypatch):
        # Force settle wait to timeout — driver.get must still be called
        driver = _make_driver(
            ready_states=["loading"],  # never goes complete during wait
            current_urls=["https://x.com"],
        )
        # Shrink the settle timeout so the test runs fast
        monkeypatch.setattr(navigate_module, "_SETTLE_TIMEOUT_S", 0.2)
        testmu_selenium.navigate(driver, "https://ipinfo.io")
        driver.get.assert_called_once_with("https://ipinfo.io")

    def test_initial_current_url_failure_still_proceeds(self):
        # current_url access raises before detection loop — navigate should still
        # run detection (with empty initial_url, URL-change check disabled) and
        # eventually call driver.get.
        driver = MagicMock()
        type(driver).current_url = property(
            lambda self: (_ for _ in ()).throw(WebDriverException("no current"))
        )
        driver.execute_script.return_value = "complete"
        testmu_selenium.navigate(driver, "https://ipinfo.io")
        driver.get.assert_called_once_with("https://ipinfo.io")


class TestNavigatePublicAPI:
    def test_navigate_is_public_module_attr(self):
        assert callable(testmu_selenium.navigate)

    def test_navigate_in_dunder_all(self):
        assert "navigate" in testmu_selenium.__all__


class TestHyperexPriming:
    @pytest.fixture(autouse=True)
    def _reset_prime(self):
        navigate_module._reset_hyperex()
        yield
        navigate_module._reset_hyperex()

    def _chrome_driver(self):
        d = MagicMock()
        d.execute_script.return_value = "complete"
        d.current_url = "https://x.com"
        d.capabilities = {"browserName": "chrome"}
        return d

    def _is_hyperex_dispatched(self, driver):
        return any(
            "set-storage-values" in (c.args[0] if c.args else "")
            for c in driver.execute_script.call_args_list
        )

    def test_primes_on_first_navigate_cloud_chrome(self, monkeypatch):
        monkeypatch.setattr("testmu_selenium._config.run_target", "cloud")
        d = self._chrome_driver()
        testmu_selenium.navigate(d, "https://ipinfo.io")
        assert self._is_hyperex_dispatched(d)

    def test_not_primed_when_local(self, monkeypatch):
        monkeypatch.setattr("testmu_selenium._config.run_target", "local")
        d = self._chrome_driver()
        testmu_selenium.navigate(d, "https://ipinfo.io")
        assert not self._is_hyperex_dispatched(d)

    def test_not_primed_twice(self, monkeypatch):
        monkeypatch.setattr("testmu_selenium._config.run_target", "cloud")
        d = self._chrome_driver()
        testmu_selenium.navigate(d, "https://a.com")
        first = sum(
            1 for c in d.execute_script.call_args_list
            if "set-storage-values" in (c.args[0] if c.args else "")
        )
        testmu_selenium.navigate(d, "https://b.com")
        total = sum(
            1 for c in d.execute_script.call_args_list
            if "set-storage-values" in (c.args[0] if c.args else "")
        )
        assert first == 1 and total == 1

    def test_not_primed_non_chrome(self, monkeypatch):
        monkeypatch.setattr("testmu_selenium._config.run_target", "cloud")
        d = self._chrome_driver()
        d.capabilities = {"browserName": "firefox"}
        testmu_selenium.navigate(d, "https://ipinfo.io")
        assert not self._is_hyperex_dispatched(d)
