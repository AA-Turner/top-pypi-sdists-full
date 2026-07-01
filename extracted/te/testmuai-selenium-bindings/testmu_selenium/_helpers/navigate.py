"""testmu_selenium.navigate — settle in-flight prior navigation, then driver.get(url).

Cross-browser via Selenium primitives only (no CDP).

The race this addresses: when a prior action (e.g. ENTER on a search box,
click on a submit button) triggers a navigation, the browser may still be
committing/loading that navigation when the next driver.get fires. Chrome's
renderer aborts the new navigation request (net::ERR_ABORTED) while the
prior commit is in flight; the page ends up on the prior nav's destination
even though driver.get returns success.

Fix: poll briefly for navigation activity (URL changed since last call OR
readyState != 'complete'). If detected, wait for readyState to reach
'complete' before issuing the new driver.get.

URL-change-only polling misses the case where URL has already changed
but the page is still loading sub-resources (which is what causes the abort).
ReadyState polling catches both cases and is cheap on the happy path.
"""
from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

_DETECT_WINDOW_S = 0.5
_SETTLE_TIMEOUT_S = 10
_POLL_INTERVAL_S = 0.05

_HYPEREX_WAIT_S = 5
_IS_HYPEREX_JS = (
    'document.dispatchEvent(new CustomEvent("set-storage-values", '
    '{ detail: { event: "is_hyperex", is_hyperex: true } }));'
)

_hyperex_primed = False


def _reset_hyperex() -> None:
    """Reset the once-per-session is_hyperex guard (called from run())."""
    global _hyperex_primed
    _hyperex_primed = False


def _prime_hyperex(driver) -> None:
    """Prime the dom-watcher extension on the first cloud-chrome navigation.

    Dispatches the is_hyperex CustomEvent so the extension skips its
    browserTabSync POST to the (absent) local agent on cloud. Mirrors V2's
    setup_hyperex_env, gated by run_target=="cloud" (V2's not IS_WEBSOCKET_AVAILABLE).
    Best-effort: never breaks navigation.
    """
    global _hyperex_primed
    if _hyperex_primed:
        return
    from testmu_selenium import _config
    if _config.run_target != "cloud":
        return
    try:
        browser = (driver.capabilities or {}).get("browserName", "").lower()
    except Exception:  # noqa: BLE001
        browser = ""
    if browser not in ("chrome", "chromium"):
        return
    try:
        WebDriverWait(driver, _HYPEREX_WAIT_S).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        driver.execute_script(_IS_HYPEREX_JS)
        _hyperex_primed = True
    except Exception:  # noqa: BLE001 — recorder priming must never break the test
        pass


def navigate(driver, url: str) -> None:
    """Navigate ``driver`` to ``url`` after settling any in-flight prior navigation.

    Args:
        driver: Selenium WebDriver instance.
        url: Target URL.
    """
    initial_url = ""
    try:
        initial_url = driver.current_url
    except WebDriverException:
        pass

    nav_in_progress = False
    deadline = time.monotonic() + _DETECT_WINDOW_S
    while time.monotonic() < deadline:
        try:
            ready_state = driver.execute_script("return document.readyState")
            current_url = driver.current_url
            if ready_state != "complete" or (initial_url and current_url != initial_url):
                nav_in_progress = True
                break
        except WebDriverException:
            pass
        time.sleep(_POLL_INTERVAL_S)

    if nav_in_progress:
        try:
            WebDriverWait(driver, _SETTLE_TIMEOUT_S).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except (TimeoutException, WebDriverException):
            pass

    driver.get(url)
    _prime_hyperex(driver)


__all__ = ["navigate"]
