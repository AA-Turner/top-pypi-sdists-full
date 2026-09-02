"""HTTP client mirror of `matrx_scraper.ai_browser.actions`.

For hosts that don't run Playwright themselves (e.g. ai-dream-server,
matrx-ai when used in a no-Chromium runtime), this client posts each call
to a remote scraper-service that does. The wire shape matches the local
actions exactly, so callers can swap implementations behind the same
result-model API.

Usage::

    from matrx_scraper.ai_browser import RemoteBrowserClient

    client = RemoteBrowserClient(
        base_url="https://scraper.app.matrxserver.com",
        auth_token=os.environ["MATRX_SCRAPER_TOKEN"],
    )
    nav = await client.navigate("https://example.com")
    print(nav.session_id, nav.title)
    await client.close(nav.session_id)

The client is safe to share across requests — it lazily owns an
``httpx.AsyncClient`` and closes it on ``aclose()``.

Configuration via env vars (read by ``RemoteBrowserClient.from_env()``):

  * ``MATRX_SCRAPER_URL``   — base URL, e.g. ``https://scraper.app.matrxserver.com``
  * ``MATRX_SCRAPER_TOKEN`` — the approved-server shared secret (matches the
    scraper's ``ADMIN_API_TOKEN``); the scraper admits it as one-of-our-servers.
    A real user-login token also works. (NOT a plain "admin token" — the scraper
    only honors this value via the approved-server handshake in
    ``matrx_scraper/server/service_auth.py``.)
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from matrx_scraper.ai_browser.actions import (
    GET_HTML_CAP,
    GET_TEXT_CAP,
    ROW_COUNT_CAP,
    ClickResult,
    EvalJsResult,
    FillResult,
    GetElementResult,
    GetHtmlResult,
    GetTextResult,
    NavigateResult,
    QuerySelectorsResult,
    ScreenshotResult,
    ScrollResult,
    SelectOptionResult,
    TypeResult,
    WaitForResult,
)

logger = logging.getLogger(__name__)


_DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0, read=60.0)


class BrowserClientError(RuntimeError):
    """Raised when the remote browser endpoint returns an unparseable response or HTTP error."""


class RemoteBrowserClient:
    """Async client over the scraper-service `/api/scraper/browser/*` surface."""

    def __init__(
        self,
        base_url: str,
        *,
        auth_token: str | None = None,
        acting_user_id: str | None = None,
        timeout: httpx.Timeout | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required (e.g. https://scraper.app.matrxserver.com)")
        self._base_url = base_url.rstrip("/")
        self._auth_token = auth_token
        # When we authenticate as an approved server (the MATRX_SCRAPER_TOKEN
        # shared secret) rather than forwarding a person's login, this names the
        # user to attribute the work to — the scraper acts as THIS user. Optional:
        # ephemeral browser sessions that own no rows can omit it.
        self._acting_user_id = acting_user_id
        self._timeout = timeout or _DEFAULT_TIMEOUT
        self._client = client
        self._owns_client = client is None

    @classmethod
    def from_env(
        cls,
        *,
        base_url_override: str | None = None,
        acting_user_id: str | None = None,
    ) -> RemoteBrowserClient | None:
        """Build a client from MATRX_SCRAPER_URL + MATRX_SCRAPER_TOKEN.

        Pass ``acting_user_id`` (the current user) so scrapes are attributed back
        to them via the X-Matrx-User-Id header. Returns None if no base URL is
        configured — callers can use this to feature-flag remote vs in-process
        browser execution.
        """
        base_url = base_url_override or os.environ.get("MATRX_SCRAPER_URL", "").strip()
        if not base_url:
            return None
        token = os.environ.get("MATRX_SCRAPER_TOKEN", "").strip() or None
        return cls(base_url=base_url, auth_token=token, acting_user_id=acting_user_id)

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    async def aclose(self) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> RemoteBrowserClient:
        await self._ensure_client()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    def _headers(self) -> dict[str, str]:
        h: dict[str, str] = {"Accept": "application/json"}
        if self._auth_token:
            h["Authorization"] = f"Bearer {self._auth_token}"
        if self._acting_user_id:
            h["X-Matrx-User-Id"] = self._acting_user_id
        return h

    async def _post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        client = await self._ensure_client()
        url = f"{self._base_url}/api/scraper{path}"
        try:
            resp = await client.post(url, json=json, headers=self._headers())
        except httpx.HTTPError as exc:
            raise BrowserClientError(f"transport error calling {url}: {exc}") from exc
        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:500]
            raise BrowserClientError(f"{url} returned {resp.status_code}: {detail}")
        try:
            return resp.json()
        except Exception as exc:
            raise BrowserClientError(f"non-JSON response from {url}: {exc}") from exc

    async def _delete(self, path: str) -> dict[str, Any]:
        client = await self._ensure_client()
        url = f"{self._base_url}/api/scraper{path}"
        try:
            resp = await client.delete(url, headers=self._headers())
        except httpx.HTTPError as exc:
            raise BrowserClientError(f"transport error calling {url}: {exc}") from exc
        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:500]
            raise BrowserClientError(f"{url} returned {resp.status_code}: {detail}")
        try:
            return resp.json()
        except Exception as exc:
            raise BrowserClientError(f"non-JSON response from {url}: {exc}") from exc

    # ── Actions ────────────────────────────────────────────────────────────

    async def navigate(
        self,
        url: str,
        *,
        session_id: str | None = None,
        wait_until: str = "load",
        timeout_ms: int = 30_000,
        extract_text: bool = False,
        user_agent: str | None = None,
        viewport: dict[str, int] | None = None,
        proxy: str | None = None,
    ) -> NavigateResult:
        body: dict[str, Any] = {
            "url": url,
            "wait_until": wait_until,
            "timeout_ms": timeout_ms,
            "extract_text": extract_text,
        }
        if session_id:
            body["session_id"] = session_id
        if user_agent:
            body["user_agent"] = user_agent
        if viewport:
            body["viewport"] = viewport
        if proxy:
            body["proxy"] = proxy
        return NavigateResult(**await self._post("/browser/navigate", body))

    async def click(
        self,
        session_id: str,
        selector: str,
        *,
        wait_after_ms: int = 0,
        timeout_ms: int = 10_000,
    ) -> ClickResult:
        return ClickResult(
            **await self._post(
                "/browser/click",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "wait_after_ms": wait_after_ms,
                    "timeout_ms": timeout_ms,
                },
            )
        )

    async def fill(
        self,
        session_id: str,
        selector: str,
        value: str,
        *,
        timeout_ms: int = 10_000,
    ) -> FillResult:
        return FillResult(
            **await self._post(
                "/browser/fill",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "value": value,
                    "timeout_ms": timeout_ms,
                },
            )
        )

    async def type_text(
        self,
        session_id: str,
        selector: str,
        text: str,
        *,
        clear_first: bool = False,
        press_enter: bool = False,
        timeout_ms: int = 10_000,
    ) -> TypeResult:
        return TypeResult(
            **await self._post(
                "/browser/type",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "text": text,
                    "clear_first": clear_first,
                    "press_enter": press_enter,
                    "timeout_ms": timeout_ms,
                },
            )
        )

    async def select_option(
        self,
        session_id: str,
        selector: str,
        *,
        value: str | None = None,
        label: str | None = None,
        timeout_ms: int = 10_000,
    ) -> SelectOptionResult:
        return SelectOptionResult(
            **await self._post(
                "/browser/select_option",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "value": value,
                    "label": label,
                    "timeout_ms": timeout_ms,
                },
            )
        )

    async def screenshot(
        self,
        session_id: str,
        *,
        selector: str | None = None,
        full_page: bool = False,
        width: int | None = None,
        height: int | None = None,
        return_base64: bool = True,
    ) -> ScreenshotResult:
        return ScreenshotResult(
            **await self._post(
                "/browser/screenshot",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "full_page": full_page,
                    "width": width,
                    "height": height,
                    "return_base64": return_base64,
                },
            )
        )

    async def wait_for(
        self,
        session_id: str,
        *,
        selector: str | None = None,
        text: str | None = None,
        state: str = "visible",
        timeout_ms: int = 10_000,
    ) -> WaitForResult:
        return WaitForResult(
            **await self._post(
                "/browser/wait_for",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "text": text,
                    "state": state,
                    "timeout_ms": timeout_ms,
                },
            )
        )

    async def get_element(
        self,
        session_id: str,
        selector: str,
        *,
        include_html: bool = False,
    ) -> GetElementResult:
        return GetElementResult(
            **await self._post(
                "/browser/get_element",
                {
                    "session_id": session_id,
                    "selector": selector,
                    "include_html": include_html,
                },
            )
        )

    async def query_selectors(
        self,
        session_id: str,
        selectors: list[str],
        *,
        attributes: list[str] | None = None,
        limit_per_selector: int = ROW_COUNT_CAP,
    ) -> QuerySelectorsResult:
        return QuerySelectorsResult(
            **await self._post(
                "/browser/query_selectors",
                {
                    "session_id": session_id,
                    "selectors": selectors,
                    "attributes": attributes,
                    "limit_per_selector": limit_per_selector,
                },
            )
        )

    async def eval_js(
        self,
        session_id: str,
        expression: str,
        *,
        allow_eval_js: bool = False,
    ) -> EvalJsResult:
        return EvalJsResult(
            **await self._post(
                "/browser/eval_js",
                {
                    "session_id": session_id,
                    "expression": expression,
                    "allow_eval_js": allow_eval_js,
                },
            )
        )

    async def scroll(
        self,
        session_id: str,
        *,
        direction: str = "down",
        pixels: int = 500,
        selector: str | None = None,
    ) -> ScrollResult:
        return ScrollResult(
            **await self._post(
                "/browser/scroll",
                {
                    "session_id": session_id,
                    "direction": direction,
                    "pixels": pixels,
                    "selector": selector,
                },
            )
        )

    async def get_html(
        self,
        session_id: str,
        *,
        cap: int = GET_HTML_CAP,
    ) -> GetHtmlResult:
        return GetHtmlResult(
            **await self._post(
                "/browser/get_html",
                {"session_id": session_id, "cap": cap},
            )
        )

    async def get_text(
        self,
        session_id: str,
        *,
        selector: str = "body",
        cap: int = GET_TEXT_CAP,
    ) -> GetTextResult:
        return GetTextResult(
            **await self._post(
                "/browser/get_text",
                {"session_id": session_id, "selector": selector, "cap": cap},
            )
        )

    async def close(self, session_id: str) -> dict[str, Any]:
        return await self._delete(f"/browser/sessions/{session_id}")

    async def list_sessions(self) -> dict[str, Any]:
        client = await self._ensure_client()
        url = f"{self._base_url}/api/scraper/browser/sessions"
        try:
            resp = await client.get(url, headers=self._headers())
        except httpx.HTTPError as exc:
            raise BrowserClientError(f"transport error calling {url}: {exc}") from exc
        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:500]
            raise BrowserClientError(f"{url} returned {resp.status_code}: {detail}")
        return resp.json()


__all__ = ["RemoteBrowserClient", "BrowserClientError"]
