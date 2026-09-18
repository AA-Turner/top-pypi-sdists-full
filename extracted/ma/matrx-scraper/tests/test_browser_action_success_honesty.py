"""`success` means THE ACTION HAPPENED — never "the call was delivered".

Live evidence, 2026-09-17 (manage.aimatrx.com/administration/users/limits):
  * a `cloud_browser` click on a tab returned ``"success": true`` while the very
    same payload carried ``error_message: "Page.click: Timeout 10000ms
    exceeded."``. A caller that checks ``success`` — the natural thing — believed
    a click landed that never landed.
  * a `cloud_browser` scroll returned ``"success": true, "scroll_y": 0``: the
    page never moved, and nothing in the payload said so.

Two rules, pinned here against the REAL result models and the REAL action
functions (a fake Playwright page, the real SSRF landing gate):

  1. Structural: no result in this family can carry ``success=True`` next to a
     non-empty ``error_message``/``error_type``. One validator on ``_BaseResult``
     downgrades it, so no future action can re-open the hole by hand.
  2. Effect: an action that demonstrably did nothing says so. ``scroll``
     compares the scroll position before and after and either reports the move,
     or fails with ``error_type="no_effect"``, or — when the container is
     already at the far end — succeeds while NAMING that in its own
     ``no_effect_reason`` field. Never a silent success.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

actions = importlib.import_module("matrx_scraper.ai_browser.actions")
commands = importlib.import_module("matrx_scraper.cloud_browser.worker.commands")
url_guard = importlib.import_module("matrx_scraper.ai_browser.url_guard")

PUBLIC_URL = "https://example.com/page"

# The verbatim message from the live run above.
TIMEOUT_TEXT = "Page.click: Timeout 10000ms exceeded."


class PlaywrightTimeoutError(Exception):
    """Stands in for ``playwright.async_api.TimeoutError``.

    The action layer must not import Playwright (it lives behind the `browser`
    extra), so it classifies by exception NAME. This fake carries the same name
    shape and the same message the live worker produced.
    """


PlaywrightTimeoutError.__name__ = "TimeoutError"


class FakePage:
    """A page with a real, if tiny, scroll model."""

    def __init__(
        self,
        *,
        scroll_y: int = 0,
        scroll_height: int = 2_000,
        inner_height: int = 800,
        scrollable: bool = True,
        click_raises: Exception | None = None,
    ) -> None:
        self.url = PUBLIC_URL
        self.scroll_y = scroll_y
        self.scroll_height = scroll_height
        self.inner_height = inner_height
        self.scrollable = scrollable
        self.click_raises = click_raises

    async def title(self) -> str:
        return "Title"

    async def inner_text(self, selector: str = "body") -> str:
        return "body text"

    async def click(self, selector: str, **kwargs: Any) -> None:
        if self.click_raises is not None:
            raise self.click_raises

    async def wait_for_timeout(self, ms: int) -> None:
        return None

    @property
    def _max(self) -> int:
        return max(0, self.scroll_height - self.inner_height)

    async def evaluate(self, expression: str, arg: Any = None) -> Any:
        # The state probe the action uses before and after the move.
        if "scrollHeight" in expression and "return" in expression:
            return {"pos": self.scroll_y, "max": self._max}
        if "window.scrollTo(0, 0)" in expression:
            if self.scrollable:
                self.scroll_y = 0
            return None
        if "document.body.scrollHeight" in expression:
            if self.scrollable:
                self.scroll_y = self._max
            return None
        if "window.scrollBy" in expression:
            delta = int(expression.split("(0, ")[1].rstrip(")"))
            if self.scrollable:
                self.scroll_y = max(0, min(self._max, self.scroll_y + delta))
            return None
        if "window.scrollY" in expression:
            return self.scroll_y
        return None


class FakeSession:
    def __init__(self, page: FakePage) -> None:
        self.session_id = "sess1"
        self.page = page


class FakeManager:
    def __init__(self, session: FakeSession) -> None:
        self.session = session

    async def get(self, session_id: str) -> FakeSession:
        return self.session


@pytest.fixture(autouse=True)
def _public_landing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The landing gate runs for real; the resolver treats our fake URL as public."""

    async def fake_validate(url: str) -> str:
        return url

    monkeypatch.setattr(url_guard, "validate_public_http_url", fake_validate)


def _mgr(**page_kwargs: Any) -> FakeManager:
    return FakeManager(FakeSession(FakePage(**page_kwargs)))


# ── Rule 1: success and an error can never coexist ──────────────────────────

# Every result model the cloud-browser action family can return. A new action
# whose result model does not inherit the one base fails this census.
_RESULT_MODELS = [
    actions.NavigateResult,
    actions.ClickResult,
    actions.FillResult,
    actions.TypeResult,
    actions.SelectOptionResult,
    actions.ScreenshotResult,
    actions.WaitForResult,
    actions.GetElementResult,
    actions.QuerySelectorsResult,
    actions.EvalJsResult,
    actions.ScrollResult,
    actions.GetHtmlResult,
    actions.GetTextResult,
    commands.ActivatePageResult,
    commands.ClosePageResult,
    commands.HandleDialogResult,
    commands.DownloadResult,
]


@pytest.mark.parametrize("model", _RESULT_MODELS, ids=lambda m: m.__name__)
def test_no_result_can_claim_success_while_carrying_an_error(model: type) -> None:
    result = model(success=True, error_type="timeout", error_message=TIMEOUT_TEXT)

    assert result.success is False, f"{model.__name__} claimed success next to an error"
    assert result.error_message == TIMEOUT_TEXT
    assert result.error_type == "timeout"


def test_an_error_message_alone_is_enough_to_deny_success() -> None:
    """The live payload carried only a message; no error_type was set."""

    result = actions.ClickResult(success=True, error_message=TIMEOUT_TEXT)

    assert result.success is False
    assert result.error_type  # a downgrade is never silent — it names a class


def test_an_ordinary_successful_result_is_untouched() -> None:
    result = actions.ClickResult(success=True, selector="#tab", url=PUBLIC_URL)
    assert result.success is True
    assert result.error_message is None


# ── Rule 1, live: the click that timed out ──────────────────────────────────


@pytest.mark.asyncio
async def test_a_clicked_element_that_times_out_is_never_a_success() -> None:
    mgr = _mgr(click_raises=PlaywrightTimeoutError(TIMEOUT_TEXT))

    result = await actions.click("sess1", "#account-add-ons", mgr=mgr)

    assert result.success is False
    assert TIMEOUT_TEXT in result.error_message
    # A timeout is a timeout — not the catch-all 'browser'. The event ledger
    # and the agent both read this field to decide whether to retry.
    assert result.error_type == "timeout"


@pytest.mark.asyncio
async def test_a_click_that_lands_reports_the_page_it_landed_on() -> None:
    result = await actions.click("sess1", "#tab", mgr=_mgr())

    assert result.success is True
    assert result.error_message is None
    assert result.url == PUBLIC_URL


# ── Rule 2: scroll reports its actual effect ────────────────────────────────


@pytest.mark.asyncio
async def test_a_scroll_that_moves_nothing_on_a_scrollable_page_fails() -> None:
    """The live defect: `success: true, scroll_y: 0` on a page that never moved."""

    mgr = _mgr(scrollable=False)

    result = await actions.scroll("sess1", direction="down", pixels=500, mgr=mgr)

    assert result.success is False
    assert result.error_type == "no_effect"
    assert result.moved is False
    assert result.scroll_y == 0
    assert result.scroll_y_before == 0
    assert result.no_effect_reason == "not_scrollable"
    assert "did not move" in result.error_message


@pytest.mark.asyncio
async def test_a_scroll_already_at_the_bottom_says_so_and_is_not_a_failure() -> None:
    mgr = _mgr(scroll_y=1_200, scroll_height=2_000, inner_height=800)

    result = await actions.scroll("sess1", direction="down", pixels=500, mgr=mgr)

    assert result.success is True  # an honest non-move, explicitly named
    assert result.moved is False
    assert result.at_end is True
    assert result.no_effect_reason == "already_at_end"
    assert result.error_message is None


@pytest.mark.asyncio
async def test_a_scroll_already_at_the_top_says_so_when_asked_to_go_up() -> None:
    result = await actions.scroll("sess1", direction="up", pixels=500, mgr=_mgr(scroll_y=0))

    assert result.success is True
    assert result.moved is False
    assert result.no_effect_reason == "already_at_start"


@pytest.mark.asyncio
async def test_a_scroll_that_moves_reports_both_positions() -> None:
    result = await actions.scroll("sess1", direction="down", pixels=500, mgr=_mgr())

    assert result.success is True
    assert result.moved is True
    assert result.scroll_y_before == 0
    assert result.scroll_y == 500
    assert result.no_effect_reason is None
