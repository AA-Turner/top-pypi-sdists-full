"""SSRF gate for the stateful browser-session surface.

A browser session is an arbitrary-URL, JS-executing fetch from INSIDE the
scraper network, so the same two gates the one-shot `/browser-fetch` endpoint
uses apply here — but at the ACTION layer, not the HTTP router, because four
consumers drive these functions (the HTTP router, matrx-scraper's MCP server,
matrx-ai's `browser_*` tools, and direct Python callers) and a router-only
gate protects exactly one of them.

Two independent layers, each sufficient alone, each loud when it fires:

  1. `guard_target` — the PRE-gate. Nothing navigates to a URL that doesn't
     resolve to a publicly-routable address, and the CORRECTED url it returns
     is what gets navigated. "Validate one thing, fetch another" is how these
     gates get walked around.

  2. `guard_landing` — the POST-gate. The browser follows redirects, and a
     click or an Enter keypress can move the page anywhere the pre-gate never
     saw, so the address the session actually LANDED on is re-validated before
     any content leaves. On a miss the page is parked at about:blank, so a
     later get_html/get_text/screenshot has nothing to read even if it somehow
     skipped its own check.

Rejections never echo the resolver's reason to the caller: it names the
resolved address, which turns any authenticated caller into an
internal-network resolution oracle. The reason IS logged server-side —
a gate that fires silently teaches nobody it fired.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlparse

from matrx_scraper.utils.url import validate_public_http_url

logger = logging.getLogger(__name__)

BLOCKED_TARGET_MESSAGE = "url must be a publicly routable http(s) address"
BLOCKED_LANDING_MESSAGE = "navigation ended on a non-public address; content withheld"
NO_PAGE_MESSAGE = "no page loaded in this session — navigate first"

# Schemes a session can sit on that are not a fetch of anything: a fresh page,
# a parked page, or an in-memory document. Nothing to withhold, nothing to read.
_NON_FETCH_SCHEMES = ("about:", "chrome:", "data:", "blob:", "file:")
_BLANK = "about:blank"


class UnsafeUrlError(ValueError):
    """A requested URL is not publicly routable. Carries no resolver detail."""


async def guard_target(url: str) -> str:
    """Pre-gate. Returns the corrected url to navigate, or raises UnsafeUrlError."""
    try:
        return await validate_public_http_url(url)
    except Exception as exc:
        logger.warning("browser session BLOCKED target %r: %s", url, exc)
        raise UnsafeUrlError(BLOCKED_TARGET_MESSAGE) from exc


async def guard_proxy(proxy: str | None) -> None:
    """Pre-gate for a caller-supplied proxy — same reach, same class of abuse.

    A proxy is an address the browser is told to connect to, so an internal one
    is the identical primitive with an extra hop.
    """
    if not proxy:
        return
    try:
        await validate_public_http_url(proxy)
    except Exception as exc:
        logger.warning("browser session BLOCKED proxy %r: %s", proxy, exc)
        raise UnsafeUrlError("proxy must be a publicly routable http(s) address") from exc


async def guard_landing(page: Any) -> tuple[str, str] | None:
    """Post-gate. None when the current page is safe to read.

    Otherwise returns `(error_type, message)` and — for a genuine non-public
    landing — parks the page at about:blank so the bytes are unreachable to
    every later action on this session.
    """
    current = getattr(page, "url", "") or ""
    if not current or current.startswith(_NON_FETCH_SCHEMES):
        return ("validation", NO_PAGE_MESSAGE)
    try:
        await validate_public_http_url(current)
    except Exception as exc:
        logger.warning(
            "browser session landed on a NON-PUBLIC address, parking and withholding: %s",
            exc,
        )
        try:
            await page.goto(_BLANK)
        except Exception:
            logger.warning(
                "could not park the session at about:blank after a non-public landing",
                exc_info=True,
            )
        return ("blocked", BLOCKED_LANDING_MESSAGE)
    return None


# --- Layer 3: egress ----------------------------------------------------------
#
# `guard_target` and `guard_landing` both key on the page's ADDRESS, so neither
# can see a request made FROM a page that is legitimately public. That gap is
# real and was filed as its own finding: on `https://example.com/`,
#   eval_js("fetch('http://169.254.169.254/latest/meta-data/').then(r=>r.text())")
# passes every address check and returns internal content — and a public page's
# OWN scripts can do the same and render the result into the DOM, where
# `get_text` returns it. `allow_eval_js` is a caller-supplied request field, so
# it is an opt-in, not a gate.
#
# The only thing that closes it is intercepting the requests themselves, which
# is what this does: ONE context-level route that applies the SAME
# `validate_public_http_url` to every request the page makes — document,
# subresource, XHR, fetch, websocket handshake — regardless of what issued it.
#
# Cost is bounded by a per-context host memo: one DNS resolution per unique
# (scheme, host, port) for the life of the context, not one per request. A page
# pulling 80 subresources off 3 hosts pays for 3 lookups.
#
# SCOPE — deliberately NOT the crawler's browser pool. This is installed on the
# ai_browser session contexts (where a caller runs arbitrary JS) and on the
# /preview screenshot context (which renders an arbitrary user URL). The crawl
# pool executes no caller-supplied JS, and putting a Python callback in front of
# every subresource of every page of every crawl is a real cost on the hottest
# path we have. If a crawl-side egress leak is ever demonstrated, install it
# there deliberately and measure — do not widen this by reflex.

BLOCKED_EGRESS_REASON = "blockedbyclient"

_ALLOWED_EGRESS_SCHEMES = ("http", "https")


async def install_egress_guard(context: Any) -> None:
    """Abort every request this context makes to a non-public address.

    The third layer, and the only one that sees requests a PUBLIC page issues.
    Fails CLOSED: a request whose verdict cannot be established is aborted, not
    allowed. That is cheap here — a blocked subresource degrades a page, where
    letting one through is the leak this exists to stop.
    """

    verdicts: dict[str, bool] = {}

    async def _is_public(url: str) -> bool:
        parsed = urlparse(url)
        host = parsed.hostname
        if not host:
            return False
        key = f"{parsed.scheme}://{host}:{parsed.port or ''}"
        cached = verdicts.get(key)
        if cached is not None:
            return cached
        try:
            await validate_public_http_url(url)
            allowed = True
        except Exception as exc:
            allowed = False
            # Logged ONCE per host per context (the memo makes it so), with the
            # resolver's reason — this side is ours, and a gate that fires
            # silently teaches nobody it fired.
            logger.warning("browser egress BLOCKED to %s: %s", key, exc)
        verdicts[key] = allowed
        return allowed

    async def _route(route: Any) -> None:
        try:
            request = route.request
            url = getattr(request, "url", "") or ""
            scheme = urlparse(url).scheme
            # Non-network schemes (data:, blob:, about:) fetch nothing off the
            # network and cannot reach an internal host.
            if scheme and scheme not in _ALLOWED_EGRESS_SCHEMES:
                await route.continue_()
                return
            if await _is_public(url):
                await route.continue_()
            else:
                await route.abort(BLOCKED_EGRESS_REASON)
        except Exception:
            # Our own bug must not hang the page on an un-answered route, and
            # must not become an accidental allow. Abort + scream.
            logger.exception("browser egress guard failed; aborting the request")
            try:
                await route.abort(BLOCKED_EGRESS_REASON)
            except Exception:
                logger.debug("could not abort a request after an egress-guard failure")

    await context.route("**/*", _route)


__all__ = [
    "BLOCKED_EGRESS_REASON",
    "BLOCKED_LANDING_MESSAGE",
    "BLOCKED_TARGET_MESSAGE",
    "NO_PAGE_MESSAGE",
    "UnsafeUrlError",
    "guard_landing",
    "guard_proxy",
    "guard_target",
    "install_egress_guard",
]
