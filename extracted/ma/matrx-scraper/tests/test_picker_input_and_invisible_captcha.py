"""Feedback 07db1a1e, proven in a REAL Chromium (no mocks of the browser).

1. Humanized typing of an ISO date into a native ``<input type=date>`` produced a
   five-digit year. Keystrokes overflow the segmented picker; the value must be
   set as ISO instead.
2. An invisible / badge-only reCAPTCHA iframe made a successful signup report
   ``anti_bot_challenge_detected``. Only a visible challenge may count.
"""

from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest

pytest.importorskip("playwright.async_api")
from playwright.async_api import async_playwright  # noqa: E402

actions = importlib.import_module("matrx_scraper.ai_browser.actions")

PAGE = "<input id='dob' type='date'><input id='txt' type='text'>"


async def _page():
    pw = await async_playwright().start()
    try:
        browser = await pw.chromium.launch(headless=True)
    except Exception as exc:  # pragma: no cover - environment without chromium
        await pw.stop()
        pytest.skip(f"chromium unavailable: {exc}")
    return pw, browser, await browser.new_page()


def test_normalize_picker_value_us_to_iso():
    n = actions.normalize_picker_value
    assert n("date", "10/13/1990") == "1990-10-13"
    assert n("date", "1/2/2000") == "2000-01-02"
    assert n("date", "1990-10-13") == "1990-10-13"
    assert n("text", "10/13/1990") == "10/13/1990"


@pytest.mark.asyncio
@pytest.mark.parametrize("raw,human", [("1990-10-13", True), ("10/13/1990", True), ("1990-10-13", False)])
async def test_type_text_into_date_input_gives_four_digit_year(monkeypatch, raw, human):
    pw, browser, page = await _page()
    try:
        await page.set_content(PAGE)
        session = SimpleNamespace(page=page)

        async def _get(_sid):
            return session

        async def _no_block(_page):
            return None

        monkeypatch.setattr(actions, "guard_landing", _no_block)
        mgr = SimpleNamespace(get=_get)
        result = await actions.type_text("s", "#dob", raw, human=human, mgr=mgr)
        assert result.success, result
        assert await page.input_value("#dob") == "1990-10-13"
    finally:
        await browser.close()
        await pw.stop()


@pytest.mark.asyncio
async def test_settle_captcha_selector_ignores_invisible_badge_but_sees_visible_challenge():
    cl = importlib.import_module("aidream.services.cloud_browser.credential_login")
    sel = cl._SETTLE_CAPTCHA
    pw, browser, page = await _page()
    try:
        # Invisible reCAPTCHA as real pages ship it: badge iframe (size=invisible),
        # a hidden challenge iframe, and a v3 submit button carrying a sitekey.
        await page.set_content(
            "<div class='grecaptcha-badge'><iframe width=256 height=60 "
            "src='about:blank#https://www.google.com/recaptcha/api2/anchor?size=invisible'></iframe></div>"
            "<div style='visibility:hidden;position:absolute'><iframe width=400 height=580 "
            "src='about:blank#https://www.google.com/recaptcha/api2/bframe'></iframe></div>"
            "<button class='g-recaptcha' data-sitekey='k' data-size='invisible'>Sign up</button>"
            "<div data-sitekey='k' data-size='invisible' class='g-recaptcha'></div>"
        )
        assert len(await page.query_selector_all(sel)) == 0

        # A VISIBLE checkbox/challenge still counts.
        await page.set_content(
            "<iframe width=304 height=78 "
            "src='about:blank#https://www.google.com/recaptcha/api2/anchor?size=normal'></iframe>"
        )
        assert len(await page.query_selector_all(sel)) == 1
        await page.set_content("<div class='h-captcha' data-sitekey='k' style='width:300px;height:80px'>x</div>")
        assert len(await page.query_selector_all(sel)) >= 1
    finally:
        await browser.close()
        await pw.stop()
