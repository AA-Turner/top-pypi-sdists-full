"""Stateful browser session HTTP API.

Exposes the `matrx_scraper.ai_browser.actions` surface over HTTP so any host
(matrx-ai, MCP servers, dashboards, mobile apps) can drive a real Playwright
session without bundling Chromium themselves. The scraper-service container
is the single source of truth for browser execution — there is no second
Chromium install anywhere in the ecosystem.

Lifecycle is identical to the in-process `BrowserSessionManager`:
  POST /sessions               → create a session, returns session_id
  POST /sessions/{id}/...      → operate on the session
  DELETE /sessions/{id}        → close
  GET /sessions                → list (admin/debug)

Sessions auto-evict after SESSION_TTL_SECONDS of idle (5 min) so abandoned
clients can't leak Chromium memory.

Auth is enforced one layer up — this router is mounted under
`Depends(require_authenticated)` in matrx_scraper.server.app.

The SSRF gate is NOT here — it lives in `ai_browser/url_guard.py` and is
applied inside `ai_browser/actions.py`, so the MCP server, matrx-ai's
`browser_*` tools, and direct Python callers are covered by the same two
gates rather than only HTTP traffic. A blocked action comes back as a normal
`success=False` result with `error_type="blocked"`.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from matrx_scraper.ai_browser import (
    BrowserSessionManager,
    actions as _actions,
    get_browser_session_manager,
)
from matrx_scraper.ai_browser.actions import GET_HTML_CAP, GET_TEXT_CAP, ROW_COUNT_CAP
from matrx_scraper.ai_browser.url_guard import UnsafeUrlError

router = APIRouter()


# ── Request models ─────────────────────────────────────────────────────────


class _SessionRef(BaseModel):
    session_id: str = Field(..., description="Session id returned by /sessions or navigate")


class CreateSessionRequest(BaseModel):
    user_agent: str | None = None
    viewport: dict[str, int] | None = None
    proxy: str | None = None
    headless: bool = True


class NavigateRequest(BaseModel):
    url: str
    session_id: str | None = Field(
        default=None, description="Reuse existing session; create new if omitted"
    )
    wait_until: str = "load"
    timeout_ms: int = 30_000
    extract_text: bool = False
    user_agent: str | None = None
    viewport: dict[str, int] | None = None
    proxy: str | None = None


class ClickRequest(_SessionRef):
    selector: str
    wait_after_ms: int = 0
    timeout_ms: int = 10_000


class FillRequest(_SessionRef):
    selector: str
    value: str
    timeout_ms: int = 10_000


class TypeRequest(_SessionRef):
    selector: str
    text: str
    clear_first: bool = False
    press_enter: bool = False
    timeout_ms: int = 10_000


class SelectOptionRequest(_SessionRef):
    selector: str
    value: str | None = None
    label: str | None = None
    timeout_ms: int = 10_000


class ScreenshotRequest(_SessionRef):
    selector: str | None = None
    full_page: bool = False
    width: int | None = None
    height: int | None = None
    return_base64: bool = True


class WaitForRequest(_SessionRef):
    selector: str | None = None
    text: str | None = None
    state: str = "visible"
    timeout_ms: int = 10_000


class GetElementRequest(_SessionRef):
    selector: str
    include_html: bool = False


class QuerySelectorsRequest(_SessionRef):
    selectors: list[str]
    attributes: list[str] | None = None
    limit_per_selector: int = ROW_COUNT_CAP


class EvalJsRequest(_SessionRef):
    expression: str
    allow_eval_js: bool = False


class ScrollRequest(_SessionRef):
    direction: str = "down"
    pixels: int = 500
    selector: str | None = None


class GetHtmlRequest(_SessionRef):
    cap: int = GET_HTML_CAP


class GetTextRequest(_SessionRef):
    selector: str = "body"
    cap: int = GET_TEXT_CAP


# ── Helpers ────────────────────────────────────────────────────────────────


def _mgr() -> BrowserSessionManager:
    return get_browser_session_manager()


# ── Session lifecycle ──────────────────────────────────────────────────────


@router.post("/browser/sessions", summary="Create a new browser session")
async def create_session(body: CreateSessionRequest) -> dict[str, Any]:
    try:
        session = await _mgr().create(
            user_agent=body.user_agent,
            viewport=body.viewport,
            proxy=body.proxy,
            headless=body.headless,
        )
    except UnsafeUrlError as exc:
        # The gate's own message carries no resolver detail — safe to echo.
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        )
    except ImportError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Playwright not available on scraper-service: {exc}",
        )
    return {
        "success": True,
        "session_id": session.session_id,
        "created_at": session.created_at,
    }


@router.delete("/browser/sessions/{session_id}", summary="Close a browser session")
async def close_session(session_id: str) -> dict[str, Any]:
    closed = await _mgr().close(session_id)
    return {"success": True, "session_id": session_id, "closed": closed}


@router.get("/browser/sessions", summary="List active browser sessions")
async def list_sessions() -> dict[str, Any]:
    mgr = _mgr()
    return {"active_count": mgr.active_count, "session_ids": mgr.session_ids}


# ── Actions ────────────────────────────────────────────────────────────────


@router.post(
    "/browser/navigate", summary="Navigate a session to a URL (creates a session if none provided)"
)
async def navigate(body: NavigateRequest) -> dict[str, Any]:
    result = await _actions.navigate(
        url=body.url,
        session_id=body.session_id,
        wait_until=body.wait_until,
        timeout_ms=body.timeout_ms,
        extract_text=body.extract_text,
        user_agent=body.user_agent,
        viewport=body.viewport,
        proxy=body.proxy,
    )
    return result.model_dump()


@router.post("/browser/click", summary="Click a CSS selector")
async def click(body: ClickRequest) -> dict[str, Any]:
    result = await _actions.click(
        session_id=body.session_id,
        selector=body.selector,
        wait_after_ms=body.wait_after_ms,
        timeout_ms=body.timeout_ms,
    )
    return result.model_dump()


@router.post("/browser/fill", summary="Set the value of an input/textarea")
async def fill(body: FillRequest) -> dict[str, Any]:
    result = await _actions.fill(
        session_id=body.session_id,
        selector=body.selector,
        value=body.value,
        timeout_ms=body.timeout_ms,
    )
    return result.model_dump()


@router.post("/browser/type", summary="Type text into a focused element")
async def type_text(body: TypeRequest) -> dict[str, Any]:
    result = await _actions.type_text(
        session_id=body.session_id,
        selector=body.selector,
        text=body.text,
        clear_first=body.clear_first,
        press_enter=body.press_enter,
        timeout_ms=body.timeout_ms,
    )
    return result.model_dump()


@router.post("/browser/select_option", summary="Select an option in a <select>")
async def select_option(body: SelectOptionRequest) -> dict[str, Any]:
    result = await _actions.select_option(
        session_id=body.session_id,
        selector=body.selector,
        value=body.value,
        label=body.label,
        timeout_ms=body.timeout_ms,
    )
    return result.model_dump()


@router.post("/browser/screenshot", summary="Capture a PNG screenshot")
async def screenshot(body: ScreenshotRequest) -> dict[str, Any]:
    result = await _actions.screenshot(
        session_id=body.session_id,
        selector=body.selector,
        full_page=body.full_page,
        width=body.width,
        height=body.height,
        return_base64=body.return_base64,
    )
    return result.model_dump()


@router.post("/browser/wait_for", summary="Wait for a selector or visible text")
async def wait_for(body: WaitForRequest) -> dict[str, Any]:
    result = await _actions.wait_for(
        session_id=body.session_id,
        selector=body.selector,
        text=body.text,
        state=body.state,
        timeout_ms=body.timeout_ms,
    )
    return result.model_dump()


@router.post("/browser/get_element", summary="Inspect a DOM element")
async def get_element(body: GetElementRequest) -> dict[str, Any]:
    result = await _actions.get_element(
        session_id=body.session_id,
        selector=body.selector,
        include_html=body.include_html,
    )
    return result.model_dump()


@router.post("/browser/query_selectors", summary="Bulk pull text/attrs across many selectors")
async def query_selectors(body: QuerySelectorsRequest) -> dict[str, Any]:
    result = await _actions.query_selectors(
        session_id=body.session_id,
        selectors=body.selectors,
        attributes=body.attributes,
        limit_per_selector=body.limit_per_selector,
    )
    return result.model_dump()


@router.post("/browser/eval_js", summary="Evaluate a JS expression (opt-in)")
async def eval_js(body: EvalJsRequest) -> dict[str, Any]:
    result = await _actions.eval_js(
        session_id=body.session_id,
        expression=body.expression,
        allow_eval_js=body.allow_eval_js,
    )
    return result.model_dump()


@router.post("/browser/scroll", summary="Scroll the page or a container")
async def scroll(body: ScrollRequest) -> dict[str, Any]:
    result = await _actions.scroll(
        session_id=body.session_id,
        direction=body.direction,
        pixels=body.pixels,
        selector=body.selector,
    )
    return result.model_dump()


@router.post("/browser/get_html", summary="Get the page HTML (post-JS, post-recipe)")
async def get_html(body: GetHtmlRequest) -> dict[str, Any]:
    result = await _actions.get_html(
        session_id=body.session_id,
        cap=body.cap,
    )
    return result.model_dump()


@router.post("/browser/get_text", summary="Get the visible text of an element (default body)")
async def get_text(body: GetTextRequest) -> dict[str, Any]:
    result = await _actions.get_text(
        session_id=body.session_id,
        selector=body.selector,
        cap=body.cap,
    )
    return result.model_dump()
