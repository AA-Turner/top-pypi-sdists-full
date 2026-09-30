"""No test in this suite may ever open a VISIBLE browser window (2026-09-28).

A full-suite run on Arman's Mac opened "Google Chrome for Testing" windows over
and over on top of his work. `conftest._no_visible_browser_ever` forces every
Playwright launch headless, session-wide, and `_fail_on_headed_request` fails
any test whose code asked for a headed browser. These pin both halves. The real
launch runs the headless shell only.
"""

from __future__ import annotations

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")


def test_the_launch_wrapper_forces_headless_and_records_the_request() -> None:
    import conftest

    seen: dict = {}

    def original(self, *args, **kwargs):  # the real BrowserType.launch stands here
        seen.update(kwargs)
        return "browser"

    wrapped = conftest._force_headless("BrowserType.launch", original)
    conftest._HEADED_REQUESTS.clear()
    assert wrapped(None, headless=False, args=["--headless=new", "--lang=en-US"]) == "browser"
    assert seen["headless"] is True
    assert seen["args"] == ["--lang=en-US"]
    assert conftest._HEADED_REQUESTS == ["BrowserType.launch"]
    conftest._HEADED_REQUESTS.clear()


def test_the_guard_is_installed_on_every_playwright_launch_door() -> None:
    from playwright.async_api import BrowserType as AsyncBrowserType
    from playwright.sync_api import BrowserType as SyncBrowserType

    for cls in (AsyncBrowserType, SyncBrowserType):
        for name in ("launch", "launch_persistent_context"):
            assert getattr(getattr(cls, name), "_matrx_headless_guard", False), (
                f"{cls.__module__}.{name} is not wrapped — a test could open a visible window"
            )


@pytest.mark.headed_request_expected
@pytest.mark.asyncio
async def test_a_real_headed_request_launches_headless() -> None:
    import conftest
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.launch(headless=False)
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"no chromium browser binary: {exc}")
        try:
            page = await browser.new_page()
            agent = await page.evaluate("navigator.userAgent")
        finally:
            await browser.close()
    assert "HeadlessChrome" in agent, agent
    assert conftest._HEADED_REQUESTS, "the headed request must be recorded"
