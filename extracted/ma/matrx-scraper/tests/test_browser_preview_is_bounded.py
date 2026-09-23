"""A preview is a courtesy. It may never cost more than the action it describes.

THE PRODUCTION FAILURE, 2026-09-21. The reported symptom was "`type_text` drops
about 1 in 5" on the signed-in `/staff` composer. It had nothing to do with
typing. Every `navigate`/`click`/`type_text` ended with an unconditional
`page.inner_text("body")` to build `text_preview`, and on that page that single
call cost 25 s or more — enough to blow the worker's 55 s command ceiling on a
five-character `type_text`. The A/B that proved it, same page, same run, one
variable: `navigate` with `extract_text=False` took **7.1 s and succeeded**;
with `extract_text=True` it took **31.2 s and failed**. It looked random only
because a heavy page sometimes finished under the client's deadline.

These guards drive the REAL actions against REAL Chromium. Only
`page.inner_text` is slowed — that is the external cost being bounded, and
everything the action itself does (readiness, humanised typing, the SSRF landing
gate) runs for real.
"""

from __future__ import annotations

import asyncio
import importlib
import time

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from playwright.async_api import async_playwright  # noqa: E402

actions = importlib.import_module("matrx_scraper.ai_browser.actions")

PAGE = """
<html><body>
  <h1>Harbor Dental — front desk</h1>
  <label>Message <textarea id="composer"></textarea></label>
  <button id="send" type="button">Send</button>
</body></html>
"""

#: Far longer than the bound, and far longer than the action itself.
SLOW_READ_SECONDS = 30


class _Session:
    def __init__(self, page) -> None:  # noqa: ANN001
        self.page = page
        self.session_id = "front-desk"


class _Registry:
    def __init__(self, session: _Session) -> None:
        self._session = session

    async def get(self, session_id: str) -> _Session:
        return self._session


async def _allow_landing(page):  # noqa: ANN001
    return None


@pytest.fixture
async def slow_page(monkeypatch):
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.launch()
        except Exception as exc:  # pragma: no cover - environment probe
            pytest.skip(f"no chromium browser binary: {exc}")
        page = await browser.new_page()
        await page.set_content(PAGE)
        monkeypatch.setattr(actions, "guard_landing", _allow_landing)

        async def _glacial_inner_text(selector: str, **_kwargs):  # noqa: ANN202
            await asyncio.sleep(SLOW_READ_SECONDS)
            return "never arrives"

        monkeypatch.setattr(page, "inner_text", _glacial_inner_text)
        yield page
        await browser.close()


@pytest.mark.asyncio
async def test_a_page_that_is_slow_to_read_cannot_eat_the_command_budget(slow_page) -> None:
    registry = _Registry(_Session(slow_page))

    started = time.monotonic()
    result = await actions.type_text(
        "front-desk", "#composer", "hello", timeout_ms=5_000, human=True, mgr=registry
    )
    elapsed = time.monotonic() - started

    assert elapsed < actions.TEXT_PREVIEW_TIMEOUT_SECONDS + 10, (
        f"type_text took {elapsed:.1f}s on a page whose body text takes "
        f"{SLOW_READ_SECONDS}s to read; the preview is not bounded"
    )
    assert result.success is True, (
        "the TYPING succeeded; a preview that could not be read must never fail the action: "
        f"{result.error_message}"
    )


@pytest.mark.asyncio
async def test_the_skipped_preview_says_so_and_says_what_to_do(slow_page) -> None:
    """Nothing fails silently. A preview that quietly became empty would be a
    result that lies about a page with plenty of text on it."""
    registry = _Registry(_Session(slow_page))

    result = await actions.type_text(
        "front-desk", "#composer", "hello", timeout_ms=5_000, mgr=registry
    )

    preview = result.text_preview or ""
    assert "unavailable" in preview, f"the preview was silently empty: {preview!r}"
    assert "The action itself\nsucceeded." in preview or "action itself succeeded" in preview
    assert "get_text" in preview, "an announcement without a remedy is half a message"


@pytest.mark.asyncio
async def test_click_and_navigate_are_bounded_by_the_same_one_place(slow_page) -> None:
    """The bound lives in ONE helper, so the fourth preview-carrying action
    cannot be written without it. Census: click and navigate too."""
    registry = _Registry(_Session(slow_page))

    started = time.monotonic()
    clicked = await actions.click("front-desk", "#send", timeout_ms=5_000, mgr=registry)
    elapsed = time.monotonic() - started

    assert clicked.success is True, clicked.error_message
    assert elapsed < actions.TEXT_PREVIEW_TIMEOUT_SECONDS + 10
    assert "unavailable" in (clicked.text_preview or "")

    source = importlib.import_module("pathlib").Path(actions.__file__).read_text(encoding="utf-8")
    assert source.count('await page.inner_text("body")') == 1, (
        "the ONE bounded body read lives in _body_preview and there is exactly one of it"
    )
    assert 'session.page.inner_text("body")' not in source, (
        "an action reading body text directly off its session page bypasses the bound "
        "and re-opens the whole class"
    )


# ── The OTHER unbounded cost on the same page ───────────────────────────────
#
# Bounding the preview was not enough. `get_element` never reads body text and
# it STILL ran 55.4 s on the signed-in production `/staff` page and was killed
# by the worker's command ceiling (run a7890d21, 2026-09-21), while asking for a
# ONE-SECOND probe. The reason: `element_readiness` gave each step its own
# `timeout_ms`, and `bounding_box()` takes no timeout argument at all, so it
# fell back to Playwright's 30-second page default — and the presence check on
# the timeout path inherited the same default on top of it.


@pytest.mark.asyncio
async def test_a_readiness_probe_never_costs_more_than_the_timeout_it_was_given(
    slow_page, monkeypatch
) -> None:
    readiness = importlib.import_module("matrx_scraper.ai_browser.readiness")

    original_locator = slow_page.locator

    def _glacial_locator(selector: str, **kwargs):  # noqa: ANN202
        handle = original_locator(selector, **kwargs)

        class _Glacial:
            first = None

            async def wait_for(self, **_kw):
                return None

            async def scroll_into_view_if_needed(self, **_kw):
                return None

            async def bounding_box(self):
                # No timeout argument exists on this call; before the fix it
                # inherited Playwright's 30 s page default.
                await asyncio.sleep(SLOW_READ_SECONDS)
                return {"x": 0, "y": 0, "width": 10, "height": 10}

        glacial = _Glacial()
        glacial.first = glacial
        return glacial

    monkeypatch.setattr(slow_page, "locator", _glacial_locator)

    started = time.monotonic()
    verdict = await readiness.element_readiness(slow_page, "#composer", timeout_ms=1_000)
    elapsed = time.monotonic() - started

    assert elapsed < 6.0, (
        f"a 1-second readiness probe took {elapsed:.1f}s; on production this is what "
        "made a get_element blow the worker's 55 s command ceiling"
    )
    assert verdict.usable is False
    assert verdict.reason in readiness.READINESS_REASONS


@pytest.mark.asyncio
async def test_the_wait_leaves_room_to_measure_what_it_waited_for(slow_page, monkeypatch) -> None:
    """The edge a whole-budget wait creates, and why the wait gets a share.

    The probe is bounded end to end. If the visibility wait were handed the
    WHOLE budget, an element that appears late — but inside it — would still be
    reported unusable, because nothing would be left to scroll it into view and
    read its box. The probe would fail precisely the case it exists to catch.

    The fake below behaves the way Playwright does: `wait_for` returns when the
    element appears, bounded by the timeout it was given.
    """
    readiness = importlib.import_module("matrx_scraper.ai_browser.readiness")
    budget_ms = 2_000
    appears_after = 1.8  # inside the budget, but only just

    def _late_locator(selector: str, **kwargs):  # noqa: ANN202
        class _Late:
            first = None

            async def wait_for(self, *, timeout: int, **_kw):
                await asyncio.sleep(min(appears_after, timeout / 1000))
                if appears_after > timeout / 1000:
                    raise TimeoutError("not visible in time")

            async def scroll_into_view_if_needed(self, **_kw):
                return None

            async def bounding_box(self):
                await asyncio.sleep(0.4)
                return {"x": 0, "y": 0, "width": 200, "height": 30}

        late = _Late()
        late.first = late
        return late

    monkeypatch.setattr(slow_page, "locator", _late_locator)

    verdict = await readiness.element_readiness(slow_page, "#composer", timeout_ms=budget_ms)

    assert verdict.usable is True, (
        "an element that appeared inside the budget came back unusable because the "
        f"wait had spent everything there was to measure it with (reason={verdict.reason})"
    )
    assert verdict.box is not None
