"""Sanitization helpers — the privacy boundary the worker enforces by construction.

Every value the worker returns to the Browser Manager on an audit-facing field
(``ActionEventFacts``, ``PageRecord``, ``HumanEpisodeSummary``, ``WorkerError``,
worker events) passes through here. PLAN.md §Audit: "coarse ownership, not a
keylogger transcript." A query string carries login codes and OTP challenges, so
it is stripped everywhere; a label is capped so a page cannot smuggle content
through a title.

There is exactly ONE place that turns a URL into a safe URL and ONE place that
caps a label. A second implementation is a drift defect under the one-deserializer
law.
"""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

# The label cap is the module constant from actions.py — never re-literalled.
from matrx_scraper.ai_browser.actions import LABEL_CAP


def safe_url(url: str | None) -> str | None:
    """Return ``scheme://host/path`` with the query string and fragment REMOVED.

    Login URLs carry one-time codes in the query string, so the query is dropped
    unconditionally. ``None`` in, ``None`` out. A non-network URL (``about:blank``,
    ``data:``) is returned scheme-only so it cannot leak an inline document body.
    """
    if not url:
        return None
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    if not parts.scheme:
        return None
    if parts.scheme in ("about", "data", "blob", "chrome", "file"):
        # Nothing safe to reveal beyond the scheme itself.
        return f"{parts.scheme}:blank" if parts.scheme == "about" else f"{parts.scheme}:"
    # netloc keeps host[:port] but NEVER userinfo (credentials in the URL).
    host = parts.hostname or ""
    netloc = host if parts.port is None else f"{host}:{parts.port}"
    return urlunsplit((parts.scheme, netloc, parts.path or "", "", ""))


def origin_of(url: str | None) -> str | None:
    """Return ``scheme://host[:port]`` only — no path, no query. Used for
    ``origins_visited`` on the human-episode summary, which may carry origins but
    never paths."""
    if not url:
        return None
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    if not parts.scheme or not parts.hostname:
        return None
    netloc = parts.hostname if parts.port is None else f"{parts.hostname}:{parts.port}"
    return f"{parts.scheme}://{netloc}"


def host_of(url: str | None) -> str | None:
    if not url:
        return None
    try:
        return urlsplit(url).hostname or None
    except ValueError:
        return None


def cap_label(text: str | None) -> str | None:
    """Cap a human-readable label at ``LABEL_CAP`` characters, visibly truncated."""
    if text is None:
        return None
    if len(text) <= LABEL_CAP:
        return text
    return text[: LABEL_CAP - 1] + "…"


def sanitize_selector_shape(selector: str | None) -> str | None:
    """A selector describes WHERE an action landed, but a page can embed a secret
    in an attribute-value selector (``[value="123456"]``). We keep the tag/id/class
    shape and cap it; we never return an attribute-value selector verbatim beyond
    the cap. The cap is the real defence — a value long enough to be a secret is
    cut."""
    if selector is None:
        return None
    return cap_label(selector)
