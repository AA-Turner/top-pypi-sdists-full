"""Browser-engine detection: the one place that decides a page's engine.

The REQUESTED browser (``smart_browser_name``, set on grid runs) wins over
the local engine identity, because cloud runs go through a relay that
reports Chromium for every engine. Helpers do not call this to branch: they
use the page's perception backend (``testmu._vN._helpers._perception``).
"""
from __future__ import annotations

import os
from contextvars import ContextVar
from typing import Literal

Engine = Literal["chromium", "firefox", "webkit"]

_FIREFOX_NAMES = frozenset({"pw-firefox", "firefox"})
_WEBKIT_NAMES = frozenset({"pw-webkit", "webkit", "safari"})
_CHROMIUM_NAMES = frozenset({
    "chrome", "chromium", "googlechrome", "microsoftedge", "edge", "msedge",
    "pw-chromium", "island",
})


def _engine_for_name(name: str) -> str | None:
    """The one name table: "chromium" / "firefox" / "webkit", or None when
    the name is not a browser this table knows."""
    name = (name or "").strip().lower()
    if name in _FIREFOX_NAMES:
        return "firefox"
    if name in _WEBKIT_NAMES:
        return "webkit"
    if name in _CHROMIUM_NAMES:
        return "chromium"
    return None


def requested_engine() -> str | None:
    """The engine the run ASKED for (``smart_browser_name``, set on grid runs):
    an engine name, ``"unknown"`` for a name outside the table, None if unset."""
    requested = (os.getenv("smart_browser_name") or "").strip()
    if not requested:
        return None
    return _engine_for_name(requested) or "unknown"


def local_engine(page) -> str | None:
    """The engine Playwright reports for ``page`` (None if it can't say).
    Behind the grid relay this is Chromium for every engine."""
    try:
        return _engine_for_name(str(page.context.browser.browser_type.name or ""))
    except Exception:  # noqa: BLE001 — persistent contexts have no .browser
        return None


def page_engine(page) -> Engine:
    """THE engine of ``page`` — the only place that decides it.

    The requested browser wins over the local identity, because cloud runs go
    through a relay that reports Chromium for every engine. Unknown -> chromium.
    """
    requested = requested_engine()
    if requested in ("chromium", "firefox", "webkit"):
        return requested  # type: ignore[return-value]
    return local_engine(page) or "chromium"  # type: ignore[return-value]


engine_of = page_engine


def supports_cdp(page) -> bool:
    """True when this page can speak CDP (Chromium family only)."""
    return page_engine(page) == "chromium"


# The engine of the session running in this context, set by a host runtime
# that drives several sessions in one process (at session start). Request
# headers (``session_engine``) prefer it over the process-wide
# TESTMUAI_BROWSER_ENGINE env, so concurrent sessions never share one engine.
# None = not set.
_BROWSER_ENGINE: ContextVar[str | None] = ContextVar("testmu_browser_engine", default=None)


def set_browser_engine(engine: str | None):
    """Set this context's session engine ("chromium" / "firefox" / "webkit",
    or None to unset). Returns the ContextVar token."""
    return _BROWSER_ENGINE.set(engine or None)


def get_browser_engine() -> str | None:
    """This context's session engine, or None when no host set one."""
    return _BROWSER_ENGINE.get()


def session_engine() -> str:
    """The run's engine without a page in hand (controller request headers,
    messages): the host's per-context engine, else the requested grid browser,
    else ``TESTMUAI_BROWSER_ENGINE``; "chromium" when none says otherwise."""
    for candidate in (get_browser_engine(), requested_engine(), os.getenv("TESTMUAI_BROWSER_ENGINE", "")):
        engine = _engine_for_name(candidate or "")
        if engine:
            return engine
    return "chromium"
