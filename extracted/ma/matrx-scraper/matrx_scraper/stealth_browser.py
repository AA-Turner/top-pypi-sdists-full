"""The stealth BROWSER step: Scrapling's StealthyFetcher behind ``knowledge.scraper.browser_engine``.

``browser_engine`` is ``current`` (our Playwright pool; default again since 2026-10-21) or ``stealth``
(patchright with ~90 anti-detection flags, run HEADFUL, plus Scrapling's Cloudflare
Turnstile / interstitial solver; BSD-3). One path, chosen by the knob, at the single
place the orchestrator performs a browser round-trip. Only the fetcher is used - never
Scrapling's crawler, adaptive relocation or MCP server.

Honest limit: a stealthy browser fixes fingerprint-based blocks. It does NOT fix an
IP-reputation block - from datacenter addresses every tool scores near zero on the
hard sites, so residential exits stay essential (``proxy`` / the egress adapter).

Headful on a server needs a display. On Linux with no ``DISPLAY`` we start our OWN
Xvfb (own PID, stopped at exit) when the binary exists; with neither, the fetch runs
headless and says so once - never silently.
"""

from __future__ import annotations

import atexit
import contextlib
import contextvars
import logging
import os
import shutil
import subprocess
import sys
import threading
from typing import Any

from matrx_scraper.utils.proxy import playwright_proxy

logger = logging.getLogger(__name__)

ENGINE_CURRENT = "current"
ENGINE_STEALTH = "stealth"
_ENGINES = (ENGINE_CURRENT, ENGINE_STEALTH)
#: `current` again (2026-10-21): the hosted A/B showed stealth reads more hard pages (33 vs 26 of 41) but p90 is 2.8x
#: slower, so it runs as a RETRY after a failed read (`knowledge.scraper.stealth_retry`), not as the default engine.
#: A host with no knob reader stays on `current`; the live registry row is "current" too.
DEFAULT_ENGINE = ENGINE_CURRENT

_xvfb_lock = threading.Lock()
_xvfb: subprocess.Popen[bytes] | None = None
_announced_headless = False


def browser_engine() -> str:
    """``knowledge.scraper.browser_engine`` - ``current`` (default) or ``stealth``."""
    from matrx_scraper.parser.knobs import parser_knob

    # KNOB MIRROR: knowledge.scraper.browser_engine = "current"
    value = str(parser_knob("browser_engine", DEFAULT_ENGINE) or DEFAULT_ENGINE).strip().lower()
    if value not in _ENGINES:
        logger.warning("browser_engine %r is not one of %s; using %r", value, _ENGINES, DEFAULT_ENGINE)
        return DEFAULT_ENGINE
    return value


def stealth_available() -> bool:
    try:
        import scrapling.fetchers  # noqa: F401
    except ImportError:
        return False
    return True


def use_stealth() -> bool:
    """True when the knob says stealth AND Scrapling is installed. A knob set to
    stealth on a host without the ``[stealth]`` extra announces itself, then falls
    back to the current engine rather than failing the scrape."""
    if browser_engine() != ENGINE_STEALTH:
        return False
    if stealth_available():
        return True
    logger.warning("browser_engine=stealth but scrapling is not installed (extra [stealth]); using current")
    return False


def _ensure_display() -> bool:
    """True when a PRIVATE virtual display exists for a headful browser, starting Xvfb if needed.

    Headful runs only on Linux, inside our own Xvfb (the scraper host/container). On a person's
    desktop (macOS, Windows, or a Linux desktop session) a headful browser opens a real window that
    steals focus, so those hosts always run headless (2026-10-18: "Chrome for Testing" windows kept
    opening on a developer's Mac and stopped their work)."""
    global _xvfb
    if sys.platform != "linux":
        return False
    if _xvfb is not None and _xvfb.poll() is None:
        return True
    binary = shutil.which("Xvfb")
    if not binary:
        return False
    with _xvfb_lock:
        if _xvfb is not None and _xvfb.poll() is None:
            return True
        read_fd, write_fd = os.pipe()
        proc = subprocess.Popen(  # noqa: S603 - fixed argv, our own binary
            [binary, "-displayfd", str(write_fd), "-screen", "0", "1920x1080x24", "-nolisten", "tcp"],
            pass_fds=(write_fd,),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.close(write_fd)
        with os.fdopen(read_fd) as reader:
            number = reader.readline().strip()
        if not number.isdigit() or proc.poll() is not None:
            proc.terminate()
            return False
        _xvfb = proc
        os.environ["DISPLAY"] = f":{number}"
        atexit.register(_stop_xvfb)
        return True


def _stop_xvfb() -> None:
    if _xvfb is not None and _xvfb.poll() is None:
        _xvfb.terminate()


async def stealth_fetch(
    url: str,
    *,
    proxy: str | None = None,
    timeout_ms: int = 45_000,
    user_agent: str | None = None,
) -> tuple[str, str, int, dict[str, str], str]:
    """Same return shape as ``PlaywrightBrowserPool.fetch``:
    ``(content, response_url, status_code, headers, title)``."""
    global _announced_headless
    from scrapling.fetchers import StealthyFetcher

    from matrx_scraper.ai_browser.url_guard import install_egress_guard
    from matrx_scraper.browser_pool import _solve_challenges_allowed
    from matrx_utils.outbound_guard import resolve_public_address

    # Refuse non-public destinations before a browser is even launched; the context
    # guard below covers every redirect hop and subresource.
    await resolve_public_address(url, allow_http=True)

    guard_installed = False

    async def _guard(page: Any) -> None:
        nonlocal guard_installed
        await install_egress_guard(page.context)
        guard_installed = True

    headful = _ensure_display()
    if not headful and not _announced_headless:
        _announced_headless = True
        logger.warning("stealth browser: no display and no Xvfb; running headless (weaker against bot checks)")

    kwargs: dict[str, Any] = {
        "headless": not headful,
        "timeout": timeout_ms,
        "solve_cloudflare": _solve_challenges_allowed(),
        "page_setup": _guard,
        "network_idle": False,
        "retries": 1,
    }
    if proxy:
        kwargs["proxy"] = playwright_proxy(proxy)
    if user_agent:
        kwargs["useragent"] = user_agent

    page = await StealthyFetcher.async_fetch(url, **kwargs)
    if not guard_installed:
        raise RuntimeError("stealth browser egress guard did not install; refusing the result")

    body = page.body
    content = body.decode(page.encoding or "utf-8", errors="replace") if isinstance(body, (bytes, bytearray)) else str(body)
    title_nodes = page.css("title::text")
    title = str(title_nodes[0]).strip() if title_nodes else ""
    headers = {str(k): str(v) for k, v in dict(getattr(page, "headers", {}) or {}).items()}
    return content, str(page.url), int(page.status), headers, title


#: KNOB MIRROR: knowledge.scraper.stealth_retry = false  (born OFF until the deployed A/B proves it; Arman 2026-10-21)
STEALTH_RETRY_DEFAULT = False
#: KNOB MIRROR: knowledge.scraper.stealth_retry_min_seconds = 20
STEALTH_RETRY_MIN_SECONDS_DEFAULT = 20


def stealth_retry_enabled() -> bool:
    """``knowledge.scraper.stealth_retry`` AND Scrapling installed (without it: no retry, nothing announced per page)."""
    from matrx_scraper.parser.knobs import parser_knob

    value = parser_knob("stealth_retry", STEALTH_RETRY_DEFAULT)
    if isinstance(value, str):
        value = value.strip().lower() not in ("false", "0", "off", "no", "")
    return bool(value) and stealth_available()


def stealth_retry_min_seconds() -> float:
    from matrx_scraper.parser.knobs import parser_knob

    try:
        return float(parser_knob("stealth_retry_min_seconds", STEALTH_RETRY_MIN_SECONDS_DEFAULT))
    except (TypeError, ValueError):
        return float(STEALTH_RETRY_MIN_SECONDS_DEFAULT)


#: KNOB MIRROR: knowledge.scraper.chat_read_budget_seconds = 15
CHAT_READ_BUDGET_SECONDS_DEFAULT = 15

#: The time budget of the read in progress, as a ``time.monotonic()`` deadline. A chat / agent read sets it
#: (``chat_read_budget``); ``scrape()`` falls back to it when its caller passed no ``deadline``.
_read_deadline: contextvars.ContextVar[float | None] = contextvars.ContextVar("matrx_scraper_read_deadline", default=None)


def current_read_deadline() -> float | None:
    return _read_deadline.get()


@contextlib.contextmanager
def chat_read_budget():
    """Mark every ``scrape()`` inside as a chat-origin read with a short budget
    (``knowledge.scraper.chat_read_budget_seconds``), so the optional stealth retry is skipped
    unless that budget leaves ``stealth_retry_min_seconds``. Screen runs and jobs do not use it."""
    import time

    from matrx_scraper.parser.knobs import parser_knob

    try:
        seconds = float(parser_knob("chat_read_budget_seconds", CHAT_READ_BUDGET_SECONDS_DEFAULT))
    except (TypeError, ValueError):
        seconds = float(CHAT_READ_BUDGET_SECONDS_DEFAULT)
    token = _read_deadline.set(time.monotonic() + seconds)
    try:
        yield
    finally:
        _read_deadline.reset(token)
