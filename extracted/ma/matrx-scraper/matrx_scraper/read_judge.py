"""judge_read — the ONE honest answer to "did this page read fail?".

A read is marked FAILED only on a strong signal (owner-approved design, 2026-10-16):

* a bot wall / challenge / captcha page (the challenge census in ``scraper.py`` — one classifier,
  never a second copy of its phrases);
* the target answered HTTP status >= 400;
* nothing came back at all (empty body), or the fetch itself failed;
* a JavaScript app shell: almost no text plus app-shell markers;
* a sign-in wall: a short page whose title or text asks the reader to log in;
* a soft 404: a page that SAYS it does not exist (title or opening words: "Page not found", "404",
  "This page doesn't exist", an Instagram / LinkedIn not-found shell) while answering HTTP 200.

**A short page alone is NOT a failure.** Real 404-style stubs, paywall teasers, a one-line answer,
an Instagram caption — retrying those with a paid reader wastes the person's points (scrape history
2026-10-16: ~8% of reads "fail", mostly as thin pages that were not failures at all).
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from matrx_scraper.app_shell import SHELL_HTML_MARKERS, SHELL_TEXT_MARKERS
from matrx_scraper.scraper import (
    CHALLENGE_FAILURE_REASONS,
    SHORT_PAGE_CHARS,
    challenge_text_reason,
    detect_challenge_reasons,
)

#: Closed vocabulary (a caller may branch on these).
CHALLENGE = "challenge"
HTTP_ERROR = "http_error"
EMPTY = "empty"
JS_SHELL = "js_shell"
SIGN_IN_WALL = "sign_in_wall"
NOT_FOUND = "not_found"
FETCH_ERROR = "fetch_error"

#: Words a person or an agent reads for each reason (no vendor, no jargon).
REASON_WORDS = {
    CHALLENGE: "the site showed a bot check instead of the page",
    HTTP_ERROR: "the site refused the request",
    EMPTY: "the page came back empty",
    JS_SHELL: "the page needs a full browser to show its content",
    SIGN_IN_WALL: "the page asks the reader to sign in",
    NOT_FOUND: "the site says this page does not exist",
    FETCH_ERROR: "the page could not be reached",
}

#: At or under this many characters of text, app-shell markers mean an unrendered app.
#: The content-sanity gate's own boundary between "thin" and "nothing" (``content_sanity``).
JS_SHELL_TEXT_CHARS = 200

#: The app-shell markers are app_shell's (one list, shared with the SEO audit's ``is_js_shell``).
_SHELL_TEXT_MARKERS = SHELL_TEXT_MARKERS
#: HTTP statuses that mean the page does not exist (anywhere): a different reader cannot find it either.
MISSING_EVERYWHERE = frozenset({404, 410})
#: Unrendered shells and wait screens whose whole text is one of these (short pages only).
_SHELL_ONLY_MARKERS = ("watch unknown video",)
_WAIT_SCREEN_MARKERS = ("we are optimizing your request", "please wait while we process your request")
#: A soft 404 is judged only on a page this short: a long article ABOUT "page not found" errors is an article.
SOFT_404_MAX_CHARS = 5000
#: How far into the text a not-found phrase must appear to count (the page's opening words).
_SOFT_404_LEAD_CHARS = 300
_SOFT_404_PHRASES = (
    "page not found",
    "page can't be found",
    "page cannot be found",
    "page could not be found",
    "page isn't available",
    "page is not available",
    "page doesn't exist",
    "page does not exist",
    "page no longer exists",
    "this content isn't available",
    "this content is not available",
    "requested page could not be found",
    "requested url was not found",
    "we couldn't find that page",
    "we can't find the page",
    "404 not found",
    "404 error",
    "error 404",
    "http 404",
    "http error 404",
)
#: A title that IS the error ("404", "Not Found", "Error 404 ...") rather than merely containing a phrase.
_SOFT_404_TITLE_LEAD = re.compile(
    r"^(oops[!,.]?\s*)?((error\s*)?(404|410)|(page\s*)?not found)(?![a-z0-9])(?!\s+(ways|tips|things|reasons|best|facts|tricks|ideas))"
)
_SIGN_IN_HEADINGS = ("# sign in", "# log in", "# login")
_SHELL_HTML_MARKERS = SHELL_HTML_MARKERS
_SIGN_IN_TITLES = ("log in", "login", "sign in", "sign-in", "signin", "log in or sign up")
_SIGN_IN_MARKERS = (
    "log in to continue",
    "login to continue",
    "sign in to continue",
    "please log in",
    "please sign in",
    "you must be logged in",
    "you need to log in",
    "you need to sign in",
    "log in or sign up",
    "sign up to see",
    "log in to see",
    "sign in to view",
    "sign in to see",
    "join now to see",
    "log in to view",
    "join to view",
    "sign in to your account",
    "forgot password?",
)


@dataclass(frozen=True)
class ReadVerdict:
    failed: bool
    #: One of the reason constants above; ``None`` when the read is fine.
    reason: str | None = None
    #: Plain words (``REASON_WORDS``) plus the specific signal, safe to show anyone.
    detail: str = ""
    #: Characters of text the read produced (informational; never the reason by itself).
    text_chars: int = 0
    #: ``False`` for a page that is missing everywhere (HTTP 404 / 410): still failed, but no other
    #: reader can open it, so it carries no coverage and no paid retry is ever offered.
    coverable: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(reason: str, signal: str, chars: int, *, coverable: bool = True) -> ReadVerdict:
    words = REASON_WORDS[reason]
    return ReadVerdict(failed=True, reason=reason, detail=f"{words} ({signal})" if signal else words, text_chars=chars,
                       coverable=coverable)


def _soft_404(lowered_title: str, lowered_body: str, chars: int) -> str | None:
    """The signal that a short page says it does not exist, or ``None``."""
    if chars > SOFT_404_MAX_CHARS:
        return None
    title = lowered_title.replace("\u2019", "'")
    lead = lowered_body[:_SOFT_404_LEAD_CHARS].replace("\u2019", "'")
    if title:
        if _SOFT_404_TITLE_LEAD.match(title):
            return f"title {title[:60]}"
        found = next((p for p in _SOFT_404_PHRASES if p in title), None)
        if found:
            return f"title says {found}"
    found = next((p for p in _SOFT_404_PHRASES if p in lead), None)
    return f"page says {found}" if found else None


def judge_read(
    *,
    status: int | None = None,
    text: str | None = None,
    html: str | None = None,
    title: str | None = None,
    fetch_failure: str | None = None,
) -> ReadVerdict:
    """Judge ONE read. ``text`` = the extracted text; ``html`` (optional) = the raw page;
    ``fetch_failure`` = the fetcher's own failure reason when it gave up (``FailureReason`` value)."""
    body = " ".join((text or "").split())
    chars = len(body)
    lowered = body.lower()
    lowered_title = (title or "").strip().lower()

    # 1. A bot wall outranks everything (it is served with ANY status, often 403/429/503).
    if fetch_failure and fetch_failure in {r.value for r in CHALLENGE_FAILURE_REASONS}:
        return _fail(CHALLENGE, "", chars)  # the fetcher's code names the site's firewall: words only
    if html:
        found = detect_challenge_reasons(html=html, title=title)
        if found:
            return _fail(CHALLENGE, next(iter(found[0].values())), chars)
    wall = challenge_text_reason(title=title, text=body)
    if wall:
        return _fail(CHALLENGE, wall.removeprefix("the page title is ").removeprefix("the page is "), chars)

    # 2. The target refused.
    if status is not None and int(status) >= 400:
        return _fail(HTTP_ERROR, f"HTTP {int(status)}", chars, coverable=int(status) not in MISSING_EVERYWHERE)

    # 3. Nothing came back.
    if fetch_failure and not body:
        return _fail(FETCH_ERROR, "", chars)
    if not body:
        return _fail(EMPTY, "no text", 0)

    # 3b. A soft 404: the page says it does not exist, whatever the status said.
    missing = _soft_404(lowered_title, lowered, chars)
    if missing:
        return _fail(NOT_FOUND, missing, chars)

    # 4. An unrendered JavaScript app: almost no text AND an app-shell marker.
    if chars <= JS_SHELL_TEXT_CHARS:
        marker = next((m for m in _SHELL_TEXT_MARKERS if m in lowered), None)
        if marker is None and html:
            raw = html.lower()
            marker = next((m for m in _SHELL_HTML_MARKERS if m in raw), None)
        if marker:
            return _fail(JS_SHELL, marker, chars)

    # 4b. A wait screen or an unrendered player shell: short, and nothing else on it.
    if chars <= JS_SHELL_TEXT_CHARS:
        marker = next((m for m in _SHELL_ONLY_MARKERS if m in lowered), None)
        if marker:
            return _fail(JS_SHELL, marker, chars)
        marker = next((m for m in _WAIT_SCREEN_MARKERS if m in lowered), None)
        if marker:
            return _fail(CHALLENGE, marker, chars)

    # 5. A sign-in wall: a SHORT page that asks the reader to log in.
    if chars <= SHORT_PAGE_CHARS:
        if lowered_title and (lowered_title in _SIGN_IN_TITLES
                              or any(lowered_title.startswith(t + " ") for t in ("log in", "sign in"))
                              or lowered_title.startswith(("log in •", "login •", "sign in •"))):
            return _fail(SIGN_IN_WALL, f"title {title!s}", chars)
        marker = next((m for m in _SIGN_IN_MARKERS if m in lowered), None)
        if marker is None and lowered.startswith(_SIGN_IN_HEADINGS):
            marker = "sign-in heading"
        if marker:
            return _fail(SIGN_IN_WALL, marker, chars)

    return ReadVerdict(failed=False, text_chars=chars)


__all__ = [
    "CHALLENGE",
    "EMPTY",
    "FETCH_ERROR",
    "HTTP_ERROR",
    "JS_SHELL",
    "MISSING_EVERYWHERE",
    "NOT_FOUND",
    "REASON_WORDS",
    "ReadVerdict",
    "SIGN_IN_WALL",
    "judge_read",
]
