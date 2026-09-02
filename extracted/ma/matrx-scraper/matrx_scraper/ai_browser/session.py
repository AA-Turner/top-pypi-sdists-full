"""Browser session manager — process-wide registry of live Playwright pages.

A `BrowserSession` is a (Playwright, Browser, Context, Page) quadruple keyed by
an opaque session_id. The AI loop calls `navigate(...)` once to mint the id,
then passes it to subsequent calls. Sessions are evicted automatically after
SESSION_TTL_SECONDS of inactivity.

This is the canonical session manager for the matrx ecosystem. Both matrx-ai's
`browser_*` tool surface and matrx-scraper's `ai_browser.actions` build on top
of this — no duplication, no host-only Playwright pool somewhere upstairs.
"""

from __future__ import annotations

import asyncio
import atexit
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import supervised_task

logger = logging.getLogger(__name__)

SESSION_TTL_SECONDS = 300  # 5 minutes idle before auto-close
EVICTION_INTERVAL_SECONDS = 60


@dataclass
class BrowserSession:
    session_id: str
    pw: Any  # AsyncPlaywright instance (kept opaque to avoid hard import here)
    browser: Any  # Browser
    context: Any  # BrowserContext
    page: Any  # Page
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)

    async def close(self) -> None:
        for closer, label in (
            (self.page, "page"),
            (self.context, "context"),
            (self.browser, "browser"),
        ):
            try:
                await closer.close()
            except Exception:
                logger.debug("error closing %s for session %s", label, self.session_id)
        try:
            await self.pw.stop()
        except Exception:
            logger.debug("error stopping playwright for session %s", self.session_id)


class BrowserSessionManager:
    """Process-wide registry of live browser sessions with TTL eviction."""

    def __init__(self, ttl_seconds: int = SESSION_TTL_SECONDS) -> None:
        self._sessions: dict[str, BrowserSession] = {}
        self._lock = asyncio.Lock()
        self._eviction_task: asyncio.Task[None] | None = None
        self._ttl = ttl_seconds

    def _ensure_eviction_task(self) -> None:
        if self._eviction_task is None or self._eviction_task.done():
            try:
                loop = asyncio.get_running_loop()
                self._eviction_task = loop.create_task(
                    self._eviction_loop(), name="matrx-scraper-browser-eviction"
                )
            except RuntimeError:
                pass

    async def _eviction_loop(self) -> None:
        while True:
            try:
                await asyncio.sleep(EVICTION_INTERVAL_SECONDS)
                await self.evict_stale()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.info("session eviction loop error: %s", exc)

    async def create(
        self,
        *,
        user_agent: str | None = None,
        viewport: dict[str, int] | None = None,
        proxy: str | None = None,
        headless: bool = True,
    ) -> BrowserSession:
        try:
            from playwright.async_api import async_playwright
        except ImportError as exc:
            raise ImportError(
                "playwright is required for AI browser sessions: "
                "pip install playwright && playwright install chromium"
            ) from exc

        # A caller-supplied proxy is an address the browser is told to connect
        # to — the same SSRF primitive as a target url, one hop removed. Gated
        # here so every caller of create() inherits it, not only the actions.
        from matrx_scraper.ai_browser.url_guard import guard_proxy, install_egress_guard

        await guard_proxy(proxy)

        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=headless)
        context_kwargs: dict[str, Any] = {}
        if user_agent:
            context_kwargs["user_agent"] = user_agent
        if viewport:
            context_kwargs["viewport"] = viewport
        if proxy:
            context_kwargs["proxy"] = {"server": proxy}
        context = await browser.new_context(**context_kwargs)
        # Installed on the CONTEXT before any page exists, so it covers every
        # request this session ever makes — including the ones a legitimately
        # public page issues from its own JS, which the address gates cannot see.
        await install_egress_guard(context)
        page = await context.new_page()
        session_id = uuid.uuid4().hex[:12]
        session = BrowserSession(
            session_id=session_id,
            pw=pw,
            browser=browser,
            context=context,
            page=page,
        )
        async with self._lock:
            self._sessions[session_id] = session
        self._ensure_eviction_task()
        return session

    async def get(self, session_id: str) -> BrowserSession | None:
        async with self._lock:
            session = self._sessions.get(session_id)
            if session is not None:
                session.last_used = time.time()
        return session

    async def close(self, session_id: str) -> bool:
        async with self._lock:
            session = self._sessions.pop(session_id, None)
        if session is None:
            return False
        await session.close()
        return True

    async def close_all(self) -> None:
        async with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        if self._eviction_task and not self._eviction_task.done():
            self._eviction_task.cancel()
            try:
                await self._eviction_task
            except asyncio.CancelledError:
                pass
        for session in sessions:
            await session.close()

    async def evict_stale(self) -> None:
        cutoff = time.time() - self._ttl
        async with self._lock:
            stale_ids = [sid for sid, s in self._sessions.items() if s.last_used < cutoff]
            stale = [self._sessions.pop(sid) for sid in stale_ids]
        for session in stale:
            await session.close()

    @property
    def active_count(self) -> int:
        return len(self._sessions)

    @property
    def session_ids(self) -> list[str]:
        return list(self._sessions.keys())


# Process-level singleton.
_manager: BrowserSessionManager | None = None


def get_browser_session_manager() -> BrowserSessionManager:
    global _manager
    if _manager is None:
        _manager = BrowserSessionManager()
    return _manager


def _shutdown() -> None:
    global _manager
    if _manager is None or _manager.active_count == 0:
        return
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            supervised_task(
                _manager.close_all(),
                kind="browser_session_shutdown_failed",
                name="browser-session-shutdown",
            )
        else:
            loop.run_until_complete(_manager.close_all())
    except Exception as exc:
        logger.info("browser session shutdown error: %s", exc)


atexit.register(_shutdown)
