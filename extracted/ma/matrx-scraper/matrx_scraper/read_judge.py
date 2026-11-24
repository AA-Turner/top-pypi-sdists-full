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
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import urlsplit

from selectolax.lexbor import LexborHTMLParser

from matrx_scraper.challenge_census import challenge_evidence

from matrx_scraper.app_shell import SHELL_HTML_MARKERS, SHELL_TEXT_MARKERS
from matrx_scraper.scraper import (
    CHALLENGE_FAILURE_REASONS,
    SHORT_PAGE_CHARS,
    challenge_text_reason,
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
_SHELL_HTML_MARKERS = SHELL_HTML_MARKERS
_SIGN_IN_TITLES = ("log in", "login", "sign in", "sign-in", "signin", "log in or sign up")
#: Knob feature of the judge's structural thresholds (``platform.feature_knob``; the host installs the reader
#: with :func:`set_read_judge_knobs_source`). Locked (nobody overrides): a read's honesty is a platform guarantee.
READ_JUDGE_KNOB_FEATURE = "scraper.read_judge"


@dataclass(frozen=True)
class JudgeKnobs:
    """The structural judge's thresholds. Agent-set starting values (blind approval), set by the research_web
    fix-round-3 lane on 2026-11-17 from 23 real and real-derived responses (``tests/fixtures/read_judge``):
    every login page measured kept 0-1 content blocks once its login widget and chrome were removed, every real
    page with a login form 3 or more; the share of text outside the widget did NOT separate them (GitHub's login
    page measured 75%, so share only widens the unsure band). Review due 2027-01-15."""

    #: A page with a password field and at most this many content blocks outside the login widget and chrome,
    #: and no main/article region holding content, IS a login page.
    login_max_blocks: int = 2
    #: A password page the judge cannot settle (a few blocks inside a main region, or under this percent of its
    #: text outside the widget and chrome with no main region) is read and marked "possibly a sign-in page".
    unsure_content_share_pct: int = 60
    #: A content block (paragraph, list item, quote, cell) holds at least this many words.
    paragraph_min_words: int = 8
    #: A page whose only challenge evidence is a generic phrase or widget, with at most this many content
    #: blocks, IS the interstitial.
    interstitial_max_blocks: int = 1


READ_JUDGE_KNOB_KEYS = tuple(JudgeKnobs.__dataclass_fields__)
_KNOBS_SOURCE: Callable[[], dict[str, int]] | None = None


def set_read_judge_knobs_source(source: Callable[[], dict[str, int]] | None) -> None:
    """Install the host's SYNC reader of the ``scraper.read_judge`` knobs (``None`` = standalone defaults)."""
    global _KNOBS_SOURCE
    _KNOBS_SOURCE = source


def judge_knobs() -> JudgeKnobs:
    """The live thresholds. A reader failure is announced in red and the package defaults hold for this read."""
    if _KNOBS_SOURCE is None:
        return JudgeKnobs()
    from matrx_utils.knob_fallback import knob_or_declared_default_sync

    def read() -> JudgeKnobs:
        got = _KNOBS_SOURCE() or {}
        return JudgeKnobs(**{k: max(0, int(got[k])) for k in READ_JUDGE_KNOB_KEYS if got.get(k) is not None})

    try:
        return knob_or_declared_default_sync(
            lambda: read(), feature=READ_JUDGE_KNOB_FEATURE, declared_default=JudgeKnobs(),
            consequence="the package defaults hold until the rows are seeded")
    except Exception as exc:  # noqa: BLE001 — one failure shape, said out loud
        print(f"[read_judge] {READ_JUDGE_KNOB_FEATURE} knobs could not be read ({type(exc).__name__}: {exc}); "
              "using the package defaults. Fix the knob rows or the host reader.", file=sys.stderr)
        return JudgeKnobs()


#: A path segment that names a sign-in page (exact segment, never a substring of a slug).
_LOGIN_SEGMENTS = frozenset({"login", "log-in", "log_in", "signin", "sign-in", "sign_in", "logon"})
_CHROME = ("header, nav, footer, aside, dialog, [role=banner], [role=navigation], [role=contentinfo], "
           "[role=dialog], [aria-modal=true]")
_BLOCKS = "p, li, blockquote, pre, dd, td"
_REGIONS = "main, article, [role=main]"


@dataclass(frozen=True)
class PageAnatomy:
    """What a page IS, measured from its HTML: how much of its visible text is its own content."""

    visible_chars: int
    #: Text outside the login widget(s) and the page chrome.
    content_chars: int
    #: Content blocks (paragraphs, list items, quotes, cells) of at least ``paragraph_min_words`` words.
    content_blocks: int
    has_password_field: bool
    #: A main/article region that still holds a content block once the login widget and chrome are gone.
    has_content_region: bool

    @property
    def content_share_pct(self) -> int:
        return round(100 * self.content_chars / self.visible_chars) if self.visible_chars else 0


def _text_chars(node: Any) -> int:
    return len(" ".join((node.text(separator=" ") or "").split())) if node is not None else 0


def _login_widget(field: Any) -> Any:
    """The smallest ancestor of a password field that is its form or holds its submit button; a page-wrapping
    form (one that holds the page's main/article) is never the widget."""
    node = field.parent
    while node is not None and node.tag not in ("body", "html"):
        if node.tag == "form" or node.css_first("button, input[type=submit], input[type=image]"):
            return field.parent if node.css_first(_REGIONS) else node
        node = node.parent
    return field


def page_anatomy(html: str | None, knobs: JudgeKnobs | None = None) -> PageAnatomy | None:
    """Measure ``html``; ``None`` when there is nothing to parse."""
    if not html:
        return None
    knobs = knobs or judge_knobs()
    try:
        tree = LexborHTMLParser(html)
    except Exception:  # noqa: BLE001 — an unparseable page has no anatomy; the judge then says it is unsure
        return None
    for node in tree.css("script, style, noscript, template, svg"):
        node.decompose()
    body = tree.body
    if body is None:
        return None
    visible = _text_chars(body)
    fields = [i for i in body.css("input") if (i.attributes.get("type") or "").strip().lower() == "password"]
    for widget in {id(w): w for w in (_login_widget(f) for f in fields)}.values():
        widget.decompose()
    for node in body.css(_CHROME):
        node.decompose()

    def _blocks(root: Any) -> int:
        return sum(1 for b in root.css(_BLOCKS) if len((b.text(separator=" ") or "").split()) >= knobs.paragraph_min_words)

    return PageAnatomy(
        visible_chars=visible,
        content_chars=_text_chars(body),
        content_blocks=_blocks(body),
        has_password_field=bool(fields),
        has_content_region=any(_blocks(r) for r in body.css(_REGIONS)),
    )


def is_login_path(url: str | None) -> bool:
    """True when the URL's path has a sign-in segment (``/login``, ``/users/sign_in``, ``/m/signin``)."""
    path = urlsplit(url or "").path.lower()
    return any(seg in _LOGIN_SEGMENTS for seg in path.split("/"))


def _same_page(a: str | None, b: str | None) -> bool:
    pa, pb = urlsplit(a or ""), urlsplit(b or "")
    return (pa.netloc.lower(), pa.path.rstrip("/")) == (pb.netloc.lower(), pb.path.rstrip("/"))


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
    #: A read the judge could not settle: kept, but every consumer shows these words beside it
    #: ("possibly an interstitial (...)", "possibly a sign-in page (...)"). Empty when the judge is sure.
    unsure: str = ""

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
    headers: dict[str, str] | None = None,
    final_url: str | None = None,
    requested_url: str | None = None,
) -> ReadVerdict:
    """Judge ONE read. ``text`` = the extracted text; ``html`` (optional) = the raw page;
    ``fetch_failure`` = the fetcher's own failure reason when it gave up (``FailureReason`` value);
    ``headers`` = the response headers (a Cloudflare ``cf-mitigated`` header names a challenge whatever the body);
    ``final_url`` / ``requested_url`` = where the fetch landed and what was asked (a redirect onto a sign-in path).

    Login pages and interstitials are judged on what the page IS (:func:`page_anatomy`), never on length plus a
    keyword: a sure answer fails or passes; an unsure one is read with ``unsure`` words every consumer shows."""
    body = " ".join((text or "").split())
    chars = len(body)
    lowered = body.lower()
    lowered_title = (title or "").strip().lower()

    # 1. A bot wall outranks everything (it is served with ANY status, often 403/429/503).
    if fetch_failure and fetch_failure in {r.value for r in CHALLENGE_FAILURE_REASONS}:
        return _fail(CHALLENGE, "", chars)  # the fetcher's code names the site's firewall: words only
    lowered_headers = {str(k).lower(): str(v).lower() for k, v in (headers or {}).items()}
    if "cf-mitigated" in lowered_headers:
        return _fail(CHALLENGE, "Cloudflare mitigated the request", chars)  # the header IS the wall, body or not
    if lowered_headers.get("x-amzn-waf-action") in ("captcha", "challenge"):
        return _fail(CHALLENGE, "AWS WAF answered with a challenge", chars)
    knobs = judge_knobs()
    anatomy = page_anatomy(html, knobs) if html else None
    unsure = ""
    if html:
        strong, generic = challenge_evidence(html=html, title=title)
    else:
        # The census's own rule for text: a wall title counts on a short page only (an article may be titled so).
        title_wall = challenge_text_reason(title=title, text="") if chars <= SHORT_PAGE_CHARS else None
        phrase_wall = challenge_text_reason(title=None, text=body)
        strong, generic = (title_wall, None) if title_wall else (None, phrase_wall)
    if strong:
        return _fail(CHALLENGE, strong.removeprefix("the page title is "), chars)
    if generic:
        # A challenge phrase or a generic captcha widget: the page's structure decides.
        signal = generic.removeprefix("the page is a bot or access wall ")
        if anatomy is None:
            # No HTML: its sentences stand in for its blocks (a wall is its one message; an article goes on).
            sentences = sum(1 for x in re.split(r"(?<=[.!?])\s+", body) if len(x.split()) >= knobs.paragraph_min_words)
            if sentences <= knobs.interstitial_max_blocks:
                return _fail(CHALLENGE, signal, chars)
            unsure = f"possibly an interstitial ({signal}; no HTML to check its structure, {sentences} sentences)"
        elif anatomy.content_blocks <= knobs.interstitial_max_blocks:
            return _fail(CHALLENGE, signal, chars)
        elif not anatomy.has_content_region:
            unsure = f"possibly an interstitial ({signal}; {anatomy.content_blocks} content blocks, no main region)"

    # 2. The target refused.
    if status is not None and int(status) >= 400:
        return _fail(HTTP_ERROR, f"HTTP {int(status)}", chars, coverable=int(status) not in MISSING_EVERYWHERE)

    # 3. Nothing came back.
    if fetch_failure and not body:
        return _fail(FETCH_ERROR, "", chars)
    if not body:
        if html and re.search(r"<script\b", html, re.I):
            return _fail(JS_SHELL, "script-only shell: no text, only scripts", 0)
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

    # 4c. A login page any site can serve, judged on what it IS: a redirect onto a sign-in path, or a password
    # form that leaves the page little content of its own.
    if final_url and is_login_path(final_url) and requested_url and not _same_page(final_url, requested_url):
        return _fail(SIGN_IN_WALL, "the site redirected to its sign-in page", chars)
    if anatomy is not None and anatomy.has_password_field:
        share, blocks = anatomy.content_share_pct, anatomy.content_blocks
        if final_url and is_login_path(final_url):
            return _fail(SIGN_IN_WALL, "a password form on a sign-in address", chars)
        if blocks <= knobs.login_max_blocks and not anatomy.has_content_region:
            return _fail(SIGN_IN_WALL, f"the page is a login form with {blocks} content blocks beside it", chars)
        if not unsure and (blocks <= knobs.login_max_blocks
                           or (share < knobs.unsure_content_share_pct and not anatomy.has_content_region)):
            unsure = f"possibly a sign-in page (a password form; {blocks} content blocks, {share}% of the text is content)"
    elif anatomy is None and final_url and is_login_path(final_url) and not unsure:
        unsure = "possibly a sign-in page (it landed on a sign-in address)"

    # 5. A short page with no password form and no vendor markup is READ. A sign-in title is the one doubt worth
    # saying aloud; a phrase ("Forgot password?", "sign in to your account") in the text never fails a page.
    if (not unsure and chars <= SHORT_PAGE_CHARS and lowered_title
            and (lowered_title in _SIGN_IN_TITLES or any(lowered_title.startswith(t + " ") for t in ("log in", "sign in"))
                 or lowered_title.startswith(("log in •", "login •", "sign in •")))):
        unsure = f"possibly a sign-in page / interstitial (its title is {title!s}; no password form, {chars} characters of text)"

    return ReadVerdict(failed=False, text_chars=chars, unsure=unsure)


__all__ = [
    "CHALLENGE",
    "EMPTY",
    "FETCH_ERROR",
    "HTTP_ERROR",
    "JS_SHELL",
    "JudgeKnobs",
    "PageAnatomy",
    "READ_JUDGE_KNOB_FEATURE",
    "READ_JUDGE_KNOB_KEYS",
    "MISSING_EVERYWHERE",
    "NOT_FOUND",
    "REASON_WORDS",
    "ReadVerdict",
    "SIGN_IN_WALL",
    "is_login_path",
    "judge_knobs",
    "judge_read",
    "page_anatomy",
    "set_read_judge_knobs_source",
]
