"""The ordinary public routes of a page — tried before a read is marked failed.

Reddit answers the main site with a bot check or an empty page far more often than its own plain public
routes do (research_web, 2026-11-17: 6 of 6 Reddit reads failed). Before a Reddit page is judged failed,
the same page is asked for on ``old.reddit.com`` and in its ``.json`` form: both are public URLs fetched
the ordinary way. Nothing here solves or evades a challenge; a route that is also walled is simply the
next attempt, and when every route fails the caller records the failure of the ORIGINAL url.

ONE seam: every page reader passes its own fetch function to :func:`fetch_with_public_routes`
(``features.read_page`` x2, ``features.mcp_tool_helpers``), so every caller benefits.
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urlsplit, urlunsplit

_REDDIT_HOSTS = frozenset({"reddit.com", "www.reddit.com", "np.reddit.com", "new.reddit.com", "m.reddit.com"})


def alternate_public_urls(url: str) -> list[str]:
    """The other public routes of this page, in the order to try them; ``[]`` when it has none."""
    parts = urlsplit((url or "").strip())
    if (parts.hostname or "").lower() not in _REDDIT_HOSTS or parts.scheme not in ("http", "https"):
        return []
    path = parts.path or "/"
    if path.endswith(".json") or path.strip("/") == "":
        return []
    old = urlunsplit(("https", "old.reddit.com", path, parts.query, ""))
    json_query = "&".join(q for q in (parts.query, "raw_json=1") if q)
    json_form = urlunsplit(("https", "www.reddit.com", path.rstrip("/") + ".json", json_query, ""))
    return [old, json_form]


def _plain(text: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", text or "").split())


def _unusable(response: Any) -> bool:
    """True when the answer is not a read: a failed fetch, no body, an HTTP error, or a wall."""
    from matrx_scraper.read_judge import judge_read

    body = getattr(response, "content", "") or getattr(response, "content_bytes", None)
    if getattr(response, "failed", False) or not body:
        return True
    status = int(getattr(response, "status_code", 0) or 0) or None
    content = getattr(response, "content", "") or ""
    is_html = "html" in str(getattr(getattr(response, "content_type", ""), "value", getattr(response, "content_type", ""))).lower()
    verdict = judge_read(
        status=status,
        text=_plain(content) if is_html else content,
        html=content if is_html else None,
        title=getattr(response, "title", None),
        headers=getattr(response, "response_headers", None),
    )
    return bool(verdict.failed)


#: Markup only a real Reddit thread/listing page carries (old.reddit, new reddit). A login page, a
#: "Welcome to Reddit" landing page and the proof-of-work interstitial all answer HTTP 200 with none of it,
#: and the read judge does not call them failed (measured from this Mac, 2026-11-17).
_THREAD_MARKUP = ("id=\"siteTable\"", "class=\"commentarea\"", "<shreddit-post", "<shreddit-comment")


def _hollow_reddit_page(response: Any) -> bool:
    """True when an HTML answer from a Reddit route carries none of a thread's markup (a login or check page)."""
    body = getattr(response, "content", "") or ""
    is_html = "html" in str(getattr(getattr(response, "content_type", ""), "value", getattr(response, "content_type", ""))).lower()
    return bool(is_html and not any(marker in body for marker in _THREAD_MARKUP))


def reddit_json_to_text(raw: str) -> str | None:
    """A Reddit ``.json`` thread as readable text (post, then comments in order); ``None`` when it is not one."""
    try:
        data = json.loads(raw)
    except (TypeError, ValueError):
        return None
    if not isinstance(data, list) or not data:
        return None
    lines: list[str] = []

    def walk(children: list[Any], depth: int) -> None:
        for child in children:
            d = (child or {}).get("data") or {}
            kind = (child or {}).get("kind")
            if kind == "t3":
                lines.append(f"# {d.get('title', '')}\n\n{d.get('selftext', '')}".strip())
            elif kind == "t1":
                lines.append(f"{'  ' * depth}- u/{d.get('author', '?')}: {d.get('body', '')}".rstrip())
                replies = d.get("replies")
                if isinstance(replies, dict):
                    walk(((replies.get("data") or {}).get("children")) or [], depth + 1)

    for listing in data:
        walk(((listing or {}).get("data") or {}).get("children") or [], 0)
    text = "\n\n".join(lines).strip()
    return text or None


def _as_text_response(response: Any, text: str) -> Any:
    """The ``.json`` answer carried as the readable text it holds (a copy; the fetched object is untouched)."""
    from matrx_scraper.scraper import ContentType

    out = copy.copy(response)
    out.content = text
    out.content_type = ContentType.MARKDOWN
    out.content_type_raw = "text/markdown"
    return out


async def fetch_with_public_routes(url: str, fetch: Callable[[str], Awaitable[Any]]) -> Any:
    """``await fetch(url)``; when that is not a read and the page has other public routes, try each in turn.

    Returns the first usable answer, else the ORIGINAL url's answer (so the caller's failure names it).
    """
    first = await fetch(url)
    alternates = alternate_public_urls(url)
    if not alternates or not (_unusable(first) or _hollow_reddit_page(first)):
        return first
    for alt in alternates:
        try:
            got = await fetch(alt)
        except Exception:  # noqa: BLE001 - an alternate that errors is just a route that did not open
            continue
        if alt.endswith(".json") or ".json?" in alt:
            text = reddit_json_to_text(getattr(got, "content", "") or "")
            if text:
                return _as_text_response(got, text)
            continue
        if not _unusable(got) and not _hollow_reddit_page(got):
            return got
    return first
