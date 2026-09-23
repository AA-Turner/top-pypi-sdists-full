"""Pure async functions implementing AI-callable browser operations.

Every function:
  * Takes plain Python args (or a Pydantic model where the shape is wide).
  * Returns a Pydantic result model — JSON-serialisable, MCP-friendly.
  * Raises only `ValueError` on bad input. Operational failures (timeouts,
    selector-not-found) are surfaced via `success=False` + `error_message`
    fields on the result, never as exceptions, so an AI loop can recover.
  * Touches Playwright via the session manager only. No host imports.

These power three call sites without modification:
  * matrx-ai's `browser_*` tool implementations (forthcoming refactor)
  * matrx-scraper's MCP server
  * direct Python callers (`from matrx_scraper.ai_browser import navigate`)
"""

from __future__ import annotations

import asyncio
import base64
import logging
from typing import Any

from pydantic import BaseModel, Field, model_validator

from matrx_scraper.ai_browser.session import (
    BrowserSession,
    BrowserSessionManager,
    get_browser_session_manager,
)
from matrx_scraper.ai_browser.humanize import HumanInput
from matrx_scraper.ai_browser.readiness import (
    PROBE_TIMEOUT_MS as READINESS_PROBE_TIMEOUT_MS,
)
from matrx_scraper.ai_browser.readiness import element_readiness
from matrx_scraper.ai_browser.url_guard import (
    UnsafeUrlError,
    guard_landing,
    guard_proxy,
    guard_target,
)

logger = logging.getLogger(__name__)


# ── Output caps — declared ONCE, here; every slice in the package names one ──
#
# A reader that cuts its payload and says nothing hands a model a fragment it
# reasons over confidently. Every cap below is paired with the `_cap_text`
# helper, which appends an inline `[truncated: …]` marker AND fills the
# `truncated` / `total_chars` fields on `_CappedResult`.
#
# The HTTP router, the remote client, and the AI-tool specs import these — a
# second literal anywhere is a defect, not a default.

TEXT_PREVIEW_CAP = 20_000  # body-text preview on navigate / click / type_text
ELEMENT_TEXT_CAP = 5_000  # get_element text_content
ELEMENT_HTML_CAP = 50_000  # get_element inner_html / outer_html (each)
ROW_TEXT_CAP = 1_000  # query_selectors per-row text
ROW_COUNT_CAP = 50  # query_selectors elements per selector
GET_HTML_CAP = 500_000  # get_html page source
GET_TEXT_CAP = 50_000  # get_text visible text
ECHO_CAP = 200  # caller's OWN input echoed back (fill value, typed text)
LABEL_CAP = 80  # caller's OWN input echoed into a human-readable label


def _failure_type(exc: Exception) -> str:
    """Name the failure class of a Playwright exception.

    A timeout is the single most common operational failure and the only one an
    agent should consider retrying — calling it the catch-all 'browser' hid it
    from the caller AND from the action-event ledger. Classified by exception
    NAME because Playwright lives behind the `browser` extra and must not be
    imported here.
    """
    return "timeout" if type(exc).__name__ == "TimeoutError" else "browser"


#: How long the courtesy body-text preview may take. A PREVIEW IS NOT THE
#: ACTION, and it must never be able to cost more than the action it describes.
#: Measured on production 2026-09-21: the signed-in `/staff` page made
#: `inner_text("body")` cost 25 s or more, and because every navigate / click /
#: type_text ran it unconditionally, every one of those commands blew the
#: worker's 55 s command ceiling — on a five-character `type_text`. The SAME
#: navigate on the SAME page in the SAME run took 7.1 s with `extract_text` off
#: and 31.2 s with it on. That is the real shape of the reported "type_text
#: drops about 1 in 5": nothing to do with typing, and it looked random only
#: because a heavy page sometimes finished under the client's deadline.
TEXT_PREVIEW_TIMEOUT_SECONDS = 5.0

#: What the caller is told when the preview did not finish. It goes in
#: `text_preview` because that is the field the agent reads, and a preview that
#: quietly turned into `None` would be a screen that lies about an action that
#: actually succeeded.
PREVIEW_UNAVAILABLE = (
    "[page text preview unavailable: this page took longer than "
    f"{TEXT_PREVIEW_TIMEOUT_SECONDS:.0f}s to read, so it was skipped. The action itself "
    "succeeded. Use get_text or get_element with a narrower selector to read this page.]"
)


async def _body_preview(page: Any) -> tuple[str, int, bool]:
    """The capped body-text preview, BOUNDED and honest when it cannot be had.

    The one place the three preview-carrying actions (navigate, click,
    type_text) read page text, so the bound is written once and cannot be
    forgotten by the fourth one.
    """
    try:
        async with asyncio.timeout(TEXT_PREVIEW_TIMEOUT_SECONDS):
            text = await page.inner_text("body")
    except (TimeoutError, asyncio.CancelledError):
        logger.warning("body-text preview exceeded %ss; skipped", TEXT_PREVIEW_TIMEOUT_SECONDS)
        return PREVIEW_UNAVAILABLE, 0, False
    return _cap_text(text, TEXT_PREVIEW_CAP)


def _cap_text(text: str, limit: int) -> tuple[str, int, bool]:
    """Cap `text` at `limit` characters, visibly.

    Returns `(content, total_chars, truncated)`. When the cap fires the content
    carries an inline marker so the model reading it cannot mistake a fragment
    for the whole thing. There is no offset/range parameter on these readers —
    the marker deliberately promises no paging that does not exist.
    """
    total = len(text)
    if total <= limit:
        return text, total, False
    marker = f"\n\n[truncated: showing {limit:,} of {total:,} characters]"
    return text[:limit] + marker, total, True


# ── Result models ──────────────────────────────────────────────────────────


class _BaseResult(BaseModel):
    """`success` states ONE thing: the action actually happened.

    🚨 It may never be True beside an error. On 2026-09-17 a click that raised
    ``Page.click: Timeout 10000ms exceeded.`` reached a caller as
    ``success: true`` with that message sitting in the same payload, and the
    caller — reasonably — believed the click landed. The validator below makes
    that shape unconstructible for EVERY result in this family, here and in
    ``cloud_browser/worker/commands.py``, which imports these models rather
    than re-declaring them. Guard: ``tests/test_browser_action_success_honesty.py``.

    The downgrade is never silent (it logs and always names an error class):
    a result that trips it is a defect in its author, not a runtime condition.
    """

    success: bool
    session_id: str | None = None
    error_message: str | None = None
    # 'blocked' is the SSRF gate firing (see ai_browser/url_guard.py) and is
    # kept distinct from 'validation' so it greps out on its own. 'no_effect'
    # is an action that completed without doing anything (see `scroll`).
    error_type: str | None = (
        None  # 'not_found' | 'timeout' | 'navigation' | 'browser' | 'validation' | 'blocked' | 'no_effect'
    )

    @model_validator(mode="after")
    def _success_never_survives_an_error(self) -> _BaseResult:
        if self.success and (self.error_message or self.error_type):
            logger.warning(
                "browser_action_success_downgraded model=%s error_type=%s",
                type(self).__name__,
                self.error_type or "browser",
            )
            self.success = False
            if not self.error_type:
                self.error_type = "browser"
        return self


class _CappedResult(_BaseResult):
    """A reader that slices its payload declares what it cut.

    `truncated` is True when ANY capped field in this result was cut.
    `total_chars` is the PRE-truncation size, in characters, of the capped
    content — summed when a result caps more than one field. An untruncated
    result is still self-describing: `truncated=False` and `total_chars` =
    the real size.

    The flags are the machine signal; the inline `[truncated: …]` marker
    appended to the content itself is what the MODEL reads (a sibling boolean
    is easy to miss mid-payload).
    """

    truncated: bool = False
    total_chars: int = 0


class NavigateResult(_CappedResult):
    url: str | None = None
    title: str | None = None
    http_status: int | None = None
    text_preview: str | None = None


class ClickResult(_CappedResult):
    selector: str | None = None
    url: str | None = None
    title: str | None = None
    text_preview: str | None = None


class FillResult(_BaseResult):
    selector: str | None = None
    value: str | None = None


class TypeResult(_CappedResult):
    selector: str | None = None
    typed: str | None = None
    url: str | None = None
    text_preview: str | None = None


class SelectOptionResult(_BaseResult):
    selector: str | None = None
    selected_values: list[str] | None = None


class ScreenshotResult(_BaseResult):
    url: str | None = None
    media_type: str = "image/png"
    width: int | None = None
    height: int | None = None
    bytes_size: int | None = None
    image_base64: str | None = None


class WaitForResult(_BaseResult):
    waited_for: str | None = None
    url: str | None = None


class GetElementResult(_CappedResult):
    selector: str | None = None
    #: THE shared readiness verdict (``ai_browser/readiness.py``): True only for
    #: an element the input actions will actually accept. It is deliberately NOT
    #: "matched the DOM" — a ``visibility:hidden`` field reported found=True here
    #: while ``type_text`` timed out on the very same selector.
    found: bool = False
    #: The selector matched something. ``present=True, found=False`` is the
    #: honest answer for a field the page has not revealed yet, and needs a
    #: different remedy from a wrong selector.
    present: bool = False
    #: One word from ``readiness.READINESS_REASONS``.
    readiness: str = "absent"
    text: str | None = None
    inner_html: str | None = None
    outer_html: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)
    bounding_box: dict[str, float] | None = None


class QuerySelectorsResult(_CappedResult):
    results: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    # Total matches per selector BEFORE the row cap — `len(results[sel])` alone
    # cannot tell a 50-match page from a 5,000-match one.
    match_counts: dict[str, int] = Field(default_factory=dict)


class EvalJsResult(_BaseResult):
    value: Any = None


class ScrollResult(_BaseResult):
    """A scroll reports the position it started from, not just where it ended.

    `scroll_y: 0` on its own cannot tell "the page is at the top because it just
    went there" from "nothing moved at all" — the 2026-09-17 defect.
    """

    direction: str | None = None
    pixels: int | None = None
    scroll_y: int | None = None
    scroll_y_before: int | None = None
    #: Did the scroll position actually change?
    moved: bool = False
    #: Is the container at the far end in the requested direction?
    at_end: bool = False
    #: Named, dedicated field for a move that did not happen:
    #: 'already_at_end' | 'already_at_start' (honest, non-failing) or
    #: 'not_scrollable' (a failure — the region does not scroll here).
    no_effect_reason: str | None = None


class GetHtmlResult(_CappedResult):
    url: str | None = None
    html: str | None = None


class GetTextResult(_CappedResult):
    url: str | None = None
    text: str | None = None


# ── Helpers ────────────────────────────────────────────────────────────────


#: One probe, run before AND after a scroll, so the action can say whether it
#: actually moved anything instead of reporting the end position alone.
#: Returns ``{pos, max}`` for the window, or for `selector`'s element, or null
#: when the selector matches nothing.
_SCROLL_STATE_JS = (
    "(sel) => {"
    " const el = sel ? document.querySelector(sel) : null;"
    " if (sel && !el) return null;"
    " const pos = sel ? el.scrollTop : (window.scrollY || 0);"
    " const height = sel ? el.scrollHeight : (document.documentElement.scrollHeight || 0);"
    " const view = sel ? el.clientHeight : (window.innerHeight || 0);"
    " return {pos: pos, max: Math.max(0, height - view)};"
    "}"
)


def _scroll_pos(state: Any) -> int:
    return int((state or {}).get("pos") or 0)


def _scroll_max(state: Any) -> int:
    return int((state or {}).get("max") or 0)


async def _resolve_session(
    session_id: str,
    *,
    mgr: BrowserSessionManager | None = None,
) -> tuple[BrowserSession | None, str | None]:
    manager = mgr or get_browser_session_manager()
    session = await manager.get(session_id)
    if session is None:
        return None, f"Browser session '{session_id}' not found or expired."
    return session, None


# ── Actions ────────────────────────────────────────────────────────────────


async def navigate(
    url: str,
    *,
    session_id: str | None = None,
    wait_until: str = "load",
    timeout_ms: int = 30_000,
    extract_text: bool = False,
    user_agent: str | None = None,
    viewport: dict[str, int] | None = None,
    proxy: str | None = None,
    mgr: BrowserSessionManager | None = None,
) -> NavigateResult:
    if not url:
        return NavigateResult(
            success=False, error_type="validation", error_message="url is required"
        )
    if wait_until not in ("load", "domcontentloaded", "networkidle"):
        wait_until = "load"
    # SSRF gate, part 1 — before a session exists, so a blocked target cannot
    # even mint one. `target` is the CORRECTED url: navigate what was
    # validated, never the raw input.
    try:
        target = await guard_target(url)
        await guard_proxy(proxy)
    except UnsafeUrlError as exc:
        return NavigateResult(success=False, error_type="blocked", error_message=str(exc))
    manager = mgr or get_browser_session_manager()
    if session_id:
        session, err = await _resolve_session(session_id, mgr=manager)
        if err:
            return NavigateResult(
                success=False, error_type="not_found", error_message=err, session_id=session_id
            )
    else:
        try:
            session = await manager.create(user_agent=user_agent, viewport=viewport, proxy=proxy)
        except ImportError as exc:
            return NavigateResult(success=False, error_type="browser", error_message=str(exc))

    try:
        resp = await session.page.goto(target, wait_until=wait_until, timeout=timeout_ms)
        # SSRF gate, part 2 — the browser follows redirects, so the page we
        # actually rendered may be an internal host reached via a public 302
        # (or a DNS rebind between validation and navigation). Re-validate the
        # landing address and withhold everything read from it.
        blocked = await guard_landing(session.page)
        if blocked:
            error_type, message = blocked
            return NavigateResult(
                success=False,
                session_id=session.session_id,
                error_type=error_type,
                error_message=message,
            )
        result = NavigateResult(
            success=True,
            session_id=session.session_id,
            url=session.page.url,
            title=await session.page.title(),
            http_status=resp.status if resp else None,
        )
        if extract_text:
            result.text_preview, result.total_chars, result.truncated = await _body_preview(
                session.page
            )
        return result
    except Exception as exc:
        return NavigateResult(
            success=False,
            session_id=session.session_id,
            error_type="navigation",
            error_message=f"Navigation failed: {exc}",
        )


async def click(
    session_id: str,
    selector: str,
    *,
    wait_after_ms: int = 0,
    timeout_ms: int = 10_000,
    human: bool = False,
    mgr: BrowserSessionManager | None = None,
) -> ClickResult:
    if not selector:
        return ClickResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="selector is required",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return ClickResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    refusal = await _refuse_unusable_target(
        session.page, selector, timeout_ms=timeout_ms, act="clicked"
    )
    if refusal is not None:
        error_type, message = refusal
        return ClickResult(
            success=False,
            session_id=session_id,
            selector=selector,
            error_type=error_type,
            error_message=message,
        )
    try:
        # ``human`` shapes the pointer events like a person's (humanize.py);
        # when the target has no box to aim at, the plain click is the fallback.
        if not (human and await HumanInput(session.page).click(selector, timeout_ms=timeout_ms)):
            await session.page.click(selector, timeout=timeout_ms)
        if wait_after_ms > 0:
            await session.page.wait_for_timeout(wait_after_ms)
        # A click is a navigation the pre-gate never saw — a link to an
        # internal host is the cheapest way around a navigate-only gate.
        blocked = await guard_landing(session.page)
        if blocked:
            error_type, message = blocked
            return ClickResult(
                success=False,
                session_id=session_id,
                selector=selector,
                error_type=error_type,
                error_message=message,
            )
        preview, total_chars, truncated = await _body_preview(session.page)
        return ClickResult(
            success=True,
            session_id=session_id,
            selector=selector,
            url=session.page.url,
            title=await session.page.title(),
            text_preview=preview,
            total_chars=total_chars,
            truncated=truncated,
        )
    except Exception as exc:
        return ClickResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"Click failed: {exc}",
        )


async def fill(
    session_id: str,
    selector: str,
    value: str,
    *,
    timeout_ms: int = 10_000,
    human: bool = False,
    mgr: BrowserSessionManager | None = None,
) -> FillResult:
    if not selector:
        return FillResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="selector is required",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return FillResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    refusal = await _refuse_unusable_target(
        session.page, selector, timeout_ms=timeout_ms, act="filled in"
    )
    if refusal is not None:
        error_type, message = refusal
        return FillResult(
            success=False,
            session_id=session_id,
            selector=selector,
            error_type=error_type,
            error_message=message,
        )
    try:
        # A person cannot set a field's value in one event; ``human`` clears
        # and retypes it keystroke by keystroke. Fields no keyboard can drive
        # (date/colour pickers, zero-size inputs) keep Playwright's fill.
        typed = human and await _human_fill(session.page, selector, value, timeout_ms)
        if not typed:
            await session.page.fill(selector, value, timeout=timeout_ms)
        return FillResult(
            success=True, session_id=session_id, selector=selector, value=value[:ECHO_CAP]
        )
    except Exception as exc:
        return FillResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"Fill failed: {exc}",
        )


async def _human_fill(page: Any, selector: str, value: str, timeout_ms: int) -> bool:
    """Human-shaped ``fill``: only for fields a keyboard can drive."""
    kind = await page.locator(selector).first.evaluate(
        "el => (el.tagName === 'INPUT' ? (el.type || 'text') : el.tagName.toLowerCase())"
    )
    if kind in {"date", "time", "datetime-local", "month", "week", "color", "range", "file", "select"}:
        return False
    return await HumanInput(page).type_text(selector, value, clear_first=True, timeout_ms=timeout_ms)


#: One fixed sentence per readiness verdict: what is wrong with the element and
#: what to do about it. Never a page body or a raw Playwright message.
#: ``{act}`` is the acting verb of whichever action asked — the sentence belongs
#: to the readiness verdict, not to one action.
_UNUSABLE_TARGET_MESSAGE = {
    "absent": "Nothing on this page matches {selector}.",
    "not_visible": (
        "{selector} exists on this page but is hidden, so it cannot be {act}. "
        "Reveal it first (open the section, choose the option that shows it) and "
        "try again."
    ),
    "zero_size": (
        "{selector} exists on this page but has no size, so it cannot be {act}. "
        "It is probably a collapsed or placeholder element."
    ),
    "probe_failed": "{selector} could not be examined on this page.",
}


async def _refuse_unusable_target(
    page: Any, selector: str, *, timeout_ms: int, act: str
) -> tuple[str, str] | None:
    """THE ONE pre-gate every element-aimed action runs.

    Returns ``(error_type, message)`` when the element is not something a person
    could act on, else ``None``. Two things it buys, both observed failing in
    production on 2026-09-21:

    * **Agreement.** ``get_element`` and every action share one verdict, so a
      field an agent was told it had can never be a field the action refuses.
      ``type_text`` and ``get_element`` were brought onto it first; ``click``,
      ``fill`` and ``select_option`` were the rest of the same class.
    * **An honest, fast answer.** Without it, a hidden target burns the caller's
      whole timeout inside Playwright and comes back with a raw locator message
      that names nothing the agent can act on. A hidden Cancel button used to
      cost eight seconds and say "Timeout 8000ms exceeded"; it now costs under a
      second and says the button is hidden and how to reveal it.

    Playwright still runs its own, stricter actionability checks afterwards —
    this gate never replaces them, it only refuses first and says why.

    🚨 It refuses ONLY what it positively determined is unusable. When the probe
    itself could not run (``probe_failed``), the action proceeds and Playwright
    answers: refusing because we could not look is a guess dressed as a fact,
    and it would turn working actions into errors on any page the probe cannot
    read.
    """
    verdict = await element_readiness(page, selector, timeout_ms=timeout_ms)
    if verdict.usable or verdict.reason == "probe_failed":
        return None
    return (
        "not_found" if verdict.reason == "absent" else "timeout",
        _UNUSABLE_TARGET_MESSAGE[verdict.reason].format(selector=selector, act=act),
    )


async def type_text(
    session_id: str,
    selector: str,
    text: str,
    *,
    clear_first: bool = False,
    press_enter: bool = False,
    timeout_ms: int = 10_000,
    human: bool = False,
    mgr: BrowserSessionManager | None = None,
) -> TypeResult:
    if not selector:
        return TypeResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="selector is required",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return TypeResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    # THE ONE readiness definition, applied BEFORE any typing — the same
    # verdict ``get_element`` reports, so a field an agent was told it had
    # cannot silently be a field this refuses. It also turns the commonest
    # failure from "sat on the page for the whole timeout, then a generic
    # error" into a fast sentence naming what is wrong with the element.
    refusal = await _refuse_unusable_target(
        session.page, selector, timeout_ms=timeout_ms, act="typed into"
    )
    if refusal is not None:
        error_type, message = refusal
        return TypeResult(
            success=False,
            session_id=session_id,
            selector=selector,
            error_type=error_type,
            error_message=message,
        )
    try:
        hi = HumanInput(session.page) if human else None
        typed = False
        if hi is not None:
            typed = await hi.type_text(
                selector, text, clear_first=clear_first, timeout_ms=timeout_ms
            )
        if not typed:
            if clear_first:
                await session.page.fill(selector, text, timeout=timeout_ms)
            else:
                await session.page.type(selector, text, timeout=timeout_ms)
        if press_enter:
            if hi is not None:
                await hi.press_enter()
            else:
                await session.page.keyboard.press("Enter")
            await session.page.wait_for_load_state("load", timeout=15_000)
        # Enter submits a form, which navigates — same unseen-navigation hole
        # as click.
        blocked = await guard_landing(session.page)
        if blocked:
            error_type, message = blocked
            return TypeResult(
                success=False,
                session_id=session_id,
                selector=selector,
                error_type=error_type,
                error_message=message,
            )
        preview, total_chars, truncated = await _body_preview(session.page)
        return TypeResult(
            success=True,
            session_id=session_id,
            selector=selector,
            typed=text[:ECHO_CAP],
            url=session.page.url,
            text_preview=preview,
            total_chars=total_chars,
            truncated=truncated,
        )
    except Exception as exc:
        return TypeResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"Type failed: {exc}",
        )


async def select_option(
    session_id: str,
    selector: str,
    *,
    value: str | None = None,
    label: str | None = None,
    timeout_ms: int = 10_000,
    mgr: BrowserSessionManager | None = None,
) -> SelectOptionResult:
    if not selector:
        return SelectOptionResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="selector is required",
        )
    if not value and not label:
        return SelectOptionResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="provide value or label",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return SelectOptionResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    refusal = await _refuse_unusable_target(
        session.page, selector, timeout_ms=timeout_ms, act="chosen from"
    )
    if refusal is not None:
        error_type, message = refusal
        return SelectOptionResult(
            success=False,
            session_id=session_id,
            selector=selector,
            error_type=error_type,
            error_message=message,
        )
    try:
        if value:
            selected = await session.page.select_option(selector, value=value, timeout=timeout_ms)
        else:
            selected = await session.page.select_option(selector, label=label, timeout=timeout_ms)
        return SelectOptionResult(
            success=True,
            session_id=session_id,
            selector=selector,
            selected_values=list(selected) if selected else [],
        )
    except Exception as exc:
        return SelectOptionResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"Select failed: {exc}",
        )


async def screenshot(
    session_id: str,
    *,
    selector: str | None = None,
    full_page: bool = False,
    width: int | None = None,
    height: int | None = None,
    return_base64: bool = True,
    mgr: BrowserSessionManager | None = None,
) -> ScreenshotResult:
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return ScreenshotResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return ScreenshotResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    try:
        if width and height:
            await session.page.set_viewport_size({"width": width, "height": height})
        if selector:
            element = await session.page.query_selector(selector)
            if element is None:
                return ScreenshotResult(
                    success=False,
                    session_id=session_id,
                    error_type="browser",
                    error_message=f"selector not found: {selector}",
                )
            png = await element.screenshot(type="png")
        else:
            png = await session.page.screenshot(type="png", full_page=full_page)
        result = ScreenshotResult(
            success=True,
            session_id=session_id,
            url=session.page.url,
            width=width,
            height=height,
            bytes_size=len(png),
        )
        if return_base64:
            result.image_base64 = base64.b64encode(png).decode("ascii")
        return result
    except Exception as exc:
        return ScreenshotResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"Screenshot failed: {exc}",
        )


async def wait_for(
    session_id: str,
    *,
    selector: str | None = None,
    text: str | None = None,
    state: str = "visible",
    timeout_ms: int = 10_000,
    mgr: BrowserSessionManager | None = None,
) -> WaitForResult:
    if not selector and not text:
        return WaitForResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="provide selector or text",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return WaitForResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    # `wait_for(text=...)` is a content oracle — success vs timeout reveals what
    # the page says — so it is gated like any other read.
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return WaitForResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    try:
        if selector:
            valid = {"visible", "attached", "detached", "hidden"}
            await session.page.wait_for_selector(
                selector, state=state if state in valid else "visible", timeout=timeout_ms
            )
            waited = f"selector '{selector}' ({state})"
        else:
            await session.page.wait_for_function(
                f"document.body.innerText.includes({repr(text)})",
                timeout=timeout_ms,
            )
            waited = f"text '{text[:LABEL_CAP]}'"
        return WaitForResult(
            success=True, session_id=session_id, waited_for=waited, url=session.page.url
        )
    except Exception as exc:
        return WaitForResult(
            success=False,
            session_id=session_id,
            error_type="timeout",
            error_message=f"Wait timed out: {exc}",
        )


async def get_element(
    session_id: str,
    selector: str,
    *,
    include_html: bool = False,
    mgr: BrowserSessionManager | None = None,
) -> GetElementResult:
    if not selector:
        return GetElementResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="selector is required",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return GetElementResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return GetElementResult(
            success=False,
            session_id=session_id,
            selector=selector,
            error_type=error_type,
            error_message=message,
        )
    try:
        # THE ONE readiness definition (readiness.py) — the same one the input
        # actions apply, so "found" here and "typeable" there cannot disagree.
        verdict = await element_readiness(
            session.page, selector, timeout_ms=READINESS_PROBE_TIMEOUT_MS
        )
        element = await session.page.query_selector(selector) if verdict.present else None
        if element is None:
            return GetElementResult(
                success=True,
                session_id=session_id,
                selector=selector,
                found=False,
                present=verdict.present,
                readiness=verdict.reason,
            )
        # Pull a flat attribute map via evaluate.
        attrs_raw = await element.evaluate(
            "el => Object.fromEntries([...el.attributes].map(a => [a.name, a.value]))"
        )
        text = await element.text_content() or ""
        capped_text, text_total, text_cut = _cap_text(text, ELEMENT_TEXT_CAP)
        result = GetElementResult(
            success=True,
            session_id=session_id,
            selector=selector,
            found=verdict.usable,
            present=verdict.present,
            readiness=verdict.reason,
            text=capped_text,
            attributes={str(k): str(v) for k, v in (attrs_raw or {}).items()},
            total_chars=text_total,
            truncated=text_cut,
        )
        if include_html:
            inner, inner_total, inner_cut = _cap_text(await element.inner_html(), ELEMENT_HTML_CAP)
            outer, outer_total, outer_cut = _cap_text(
                await element.evaluate("el => el.outerHTML"), ELEMENT_HTML_CAP
            )
            result.inner_html = inner
            result.outer_html = outer
            # Multi-field result: total_chars sums every capped field, truncated
            # is True if ANY of them was cut.
            result.total_chars += inner_total + outer_total
            result.truncated = result.truncated or inner_cut or outer_cut
        # The box comes from the readiness verdict, which offers one only for
        # something a pointer can actually be aimed at. A box on an unusable
        # element is the exact lie this class of defect was made of.
        result.bounding_box = verdict.box
        return result
    except Exception as exc:
        return GetElementResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"get_element failed: {exc}",
        )


async def query_selectors(
    session_id: str,
    selectors: list[str],
    *,
    attributes: list[str] | None = None,
    limit_per_selector: int = ROW_COUNT_CAP,
    mgr: BrowserSessionManager | None = None,
) -> QuerySelectorsResult:
    """Bulk extraction — pull text + attribute values for many selectors in one round-trip."""
    if not selectors:
        return QuerySelectorsResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="selectors is required",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return QuerySelectorsResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return QuerySelectorsResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    attrs = attributes or ["href", "src", "alt", "title", "id", "class"]
    out: dict[str, list[dict[str, Any]]] = {}
    match_counts: dict[str, int] = {}
    total_chars = 0
    truncated = False
    try:
        for sel in selectors:
            elements = await session.page.query_selector_all(sel)
            match_counts[sel] = len(elements)
            rows: list[dict[str, Any]] = []
            for el in elements[:limit_per_selector]:
                row: dict[str, Any] = {}
                try:
                    capped, row_total, row_cut = _cap_text(
                        (await el.text_content()) or "", ROW_TEXT_CAP
                    )
                    row["text"] = capped
                    total_chars += row_total
                    truncated = truncated or row_cut
                except Exception:
                    row["text"] = None
                for attr in attrs:
                    try:
                        row[attr] = await el.get_attribute(attr)
                    except Exception:
                        row[attr] = None
                rows.append(row)
            if len(elements) > limit_per_selector:
                # The row cap is the other silent cut here — say so where the
                # model is reading the rows, in the same shape as the rows.
                truncated = True
                notice: dict[str, Any] = {
                    "text": f"[truncated: showing {limit_per_selector:,} of {len(elements):,} matching elements for this selector]"
                }
                for attr in attrs:
                    notice[attr] = None
                rows.append(notice)
            out[sel] = rows
        return QuerySelectorsResult(
            success=True,
            session_id=session_id,
            results=out,
            match_counts=match_counts,
            total_chars=total_chars,
            truncated=truncated,
        )
    except Exception as exc:
        return QuerySelectorsResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"query failed: {exc}",
        )


async def eval_js(
    session_id: str,
    expression: str,
    *,
    allow_eval_js: bool = False,
    mgr: BrowserSessionManager | None = None,
) -> EvalJsResult:
    """Evaluate a JS expression in the page context.

    OFF by default. Hosts must opt in by passing allow_eval_js=True. The
    expression must return a JSON-serialisable value. Useful when an AI
    loop needs to read window state or compute something from DOM.
    """
    if not allow_eval_js:
        return EvalJsResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="eval_js disabled — pass allow_eval_js=True to enable",
        )
    if not expression:
        return EvalJsResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="expression is required",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return EvalJsResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return EvalJsResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    try:
        value = await session.page.evaluate(expression)
        return EvalJsResult(success=True, session_id=session_id, value=value)
    except Exception as exc:
        return EvalJsResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"eval_js failed: {exc}",
        )


async def scroll(
    session_id: str,
    *,
    direction: str = "down",
    pixels: int = 500,
    selector: str | None = None,
    human: bool = False,
    mgr: BrowserSessionManager | None = None,
) -> ScrollResult:
    if direction not in ("up", "down", "top", "bottom"):
        return ScrollResult(
            success=False,
            session_id=session_id,
            error_type="validation",
            error_message="direction must be up/down/top/bottom",
        )
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return ScrollResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return ScrollResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    try:
        before = await session.page.evaluate(_SCROLL_STATE_JS, selector)
        if before is None:
            return ScrollResult(
                success=False,
                session_id=session_id,
                direction=direction,
                pixels=pixels,
                error_type="not_found",
                error_message=f"No element matches the scroll selector: {selector}",
            )
        if human and direction in ("up", "down"):
            # Wheel notches over the region, the way a hand scrolls; top/bottom
            # jumps stay programmatic (a person would press Home/End anyway).
            await HumanInput(session.page).scroll_by(
                -pixels if direction == "up" else pixels, over_selector=selector
            )
        elif selector:
            await session.page.evaluate(
                "([sel, dir, px]) => {"
                " const el = document.querySelector(sel);"
                " if (!el) return null;"
                " if (dir === 'top') el.scrollTop = 0;"
                " else if (dir === 'bottom') el.scrollTop = el.scrollHeight;"
                " else el.scrollTop += dir === 'up' ? -px : px;"
                " return el.scrollTop;"
                "}",
                [selector, direction, pixels],
            )
        else:
            if direction == "top":
                await session.page.evaluate("window.scrollTo(0, 0)")
            elif direction == "bottom":
                await session.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            else:
                delta = -pixels if direction == "up" else pixels
                await session.page.evaluate(f"window.scrollBy(0, {delta})")
        after = await session.page.evaluate(_SCROLL_STATE_JS, selector)
    except Exception as exc:
        return ScrollResult(
            success=False,
            session_id=session_id,
            direction=direction,
            pixels=pixels,
            error_type=_failure_type(exc),
            error_message=f"Scroll failed: {exc}",
        )

    start = _scroll_pos(before)
    end = _scroll_pos(after)
    moved = end != start
    forward = direction in ("down", "bottom")
    at_end = (start >= _scroll_max(before) - 1) if forward else (start <= 0)
    common = {
        "session_id": session_id,
        "direction": direction,
        "pixels": pixels,
        "scroll_y": end,
        "scroll_y_before": start,
        "moved": moved,
        "at_end": at_end if not moved else (end >= _scroll_max(after) - 1 if forward else end <= 0),
    }
    if moved:
        return ScrollResult(success=True, **common)
    if at_end:
        # An honest non-move: the caller asked to go further in a direction that
        # has no further. It is a fine outcome — but it is SAID, in its own
        # field, never left as a bare success.
        return ScrollResult(
            success=True,
            no_effect_reason="already_at_end" if forward else "already_at_start",
            **common,
        )
    where = f"the element matching {selector}" if selector else "the page"
    return ScrollResult(
        success=False,
        error_type="no_effect",
        error_message=(
            f"Scroll had no effect: {where} did not move (still at {end}) and is not at the "
            "end. The scrollable region is probably an inner element — pass `selector` for "
            "the container that actually scrolls."
        ),
        no_effect_reason="not_scrollable",
        **common,
    )


async def get_html(
    session_id: str,
    *,
    cap: int = GET_HTML_CAP,
    mgr: BrowserSessionManager | None = None,
) -> GetHtmlResult:
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return GetHtmlResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return GetHtmlResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    try:
        html, total_chars, truncated = _cap_text(await session.page.content(), cap)
        return GetHtmlResult(
            success=True,
            session_id=session_id,
            url=session.page.url,
            html=html,
            total_chars=total_chars,
            truncated=truncated,
        )
    except Exception as exc:
        return GetHtmlResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"get_html failed: {exc}",
        )


async def get_text(
    session_id: str,
    *,
    selector: str = "body",
    cap: int = GET_TEXT_CAP,
    mgr: BrowserSessionManager | None = None,
) -> GetTextResult:
    session, err = await _resolve_session(session_id, mgr=mgr)
    if err:
        return GetTextResult(
            success=False, session_id=session_id, error_type="not_found", error_message=err
        )
    blocked = await guard_landing(session.page)
    if blocked:
        error_type, message = blocked
        return GetTextResult(
            success=False, session_id=session_id, error_type=error_type, error_message=message
        )
    try:
        text, total_chars, truncated = _cap_text(await session.page.inner_text(selector), cap)
        return GetTextResult(
            success=True,
            session_id=session_id,
            url=session.page.url,
            text=text,
            total_chars=total_chars,
            truncated=truncated,
        )
    except Exception as exc:
        return GetTextResult(
            success=False,
            session_id=session_id,
            error_type=_failure_type(exc),
            error_message=f"get_text failed: {exc}",
        )


async def close(
    session_id: str,
    *,
    mgr: BrowserSessionManager | None = None,
) -> dict[str, Any]:
    manager = mgr or get_browser_session_manager()
    closed = await manager.close(session_id)
    return {"success": True, "session_id": session_id, "closed": closed}
