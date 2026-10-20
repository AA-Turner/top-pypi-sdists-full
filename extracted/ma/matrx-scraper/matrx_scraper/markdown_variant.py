"""The markdown-variant probe: does this page have a clean markdown twin?

Many documentation sites publish the same page as markdown — the cleanest
extraction there is. A scrape that only reads the HTML never notices. This
module is the ONE place that checks, called from ``orchestrator.scrape`` so
every caller (``web`` read, read_page, site_data, the crawler's single-page
reads) inherits it.

Signals, cheapest first, at most :data:`MAX_EXTRA_REQUESTS` extra page-level
requests per page:

1. ``<link rel="alternate" type="text/markdown">`` (or ``application/markdown``)
   in the fetched HTML — the site tells us exactly where it is;
2. a sibling ``<url>.md`` (``<url>/index.md`` for a directory-style path);
3. ``Accept: text/markdown`` content negotiation on the same URL — accepted only
   when the answer is a markdown body that the HTML answer was not.

Site-level: ``/llms.txt`` and ``/llms-full.txt`` are probed once per host per
TTL and reported as ``site_index`` evidence (they describe the site, they are
not this page, so they never replace page text).

A candidate counts only when it is a markdown body (not HTML, not an error
page) AND clearly the same content as the page (word overlap with the page's
own text). Negative answers are cached per host so a site with no markdown is
not re-probed on every page. The probe never raises and never blocks the normal
result: markdown is an ADDITION. Gated by ``knowledge.scraper.prefer_markdown_variant``.
"""

from __future__ import annotations

import asyncio
import re
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlsplit, urlunsplit

#: Cheap by construction: no more than this many extra page-level requests.
#: A host we have never probed gets one more so each style is tried once; after
#: that every style is either remembered as working or as dead for the host, so
#: later pages cost at most MAX_EXTRA_REQUESTS (usually zero or one).
MAX_EXTRA_REQUESTS = 2
MAX_EXTRA_REQUESTS_FIRST_CONTACT = 3


@dataclass(frozen=True)
class ProbeLimits:
    """Protocol bounds of the probe (not behavior an admin turns: the behavior
    switch is the ``prefer_markdown_variant`` knob)."""

    #: The whole probe is abandoned after this long; the HTML result is unaffected.
    timeout: float = 8.0
    #: How long a host's "no markdown here" answer is trusted.
    negative_ttl: float = 6 * 3600.0
    #: How long a host's llms.txt answer (either way) is trusted.
    site_index_ttl: float = 24 * 3600.0


LIMITS = ProbeLimits()
#: Share of the markdown's distinctive words that must appear in the page.
MIN_OVERLAP = 0.5
MIN_OVERLAP_DECLARED = 0.3
MIN_MARKDOWN_CHARS = 80

READER_USER_AGENT = "Mozilla/5.0 (compatible; MatrxReader/1.0)"
MARKDOWN_TYPES = ("text/markdown", "application/markdown", "text/x-markdown")

SIGNAL_LINK = "link_alternate"
SIGNAL_SIBLING = "sibling_md"
SIGNAL_SIBLING_TXT = "sibling_md_txt"
SIGNAL_NEGOTIATION = "accept_negotiation"
SIGNAL_RAW_SOURCE = "raw_source"

#: ``async (url, accept_markdown) -> (status, content_type, body) | None``.
#: The default goes through the package's own ``fetch`` client; tests inject fakes.
Fetcher = Callable[[str, bool], Awaitable["ProbeResponse | None"]]


@dataclass
class ProbeResponse:
    status: int
    content_type: str
    body: str
    final_url: str = ""


@dataclass
class MarkdownVariant:
    markdown: str
    url: str
    signal: str
    note: str


@dataclass
class SiteIndex:
    llms_txt_url: str | None = None
    llms_full_txt_url: str | None = None


@dataclass
class _HostMemory:
    no_sibling_until: float = 0.0
    no_sibling_txt_until: float = 0.0
    no_negotiation_until: float = 0.0
    sibling_works: bool = False
    sibling_txt_works: bool = False
    probed: bool = False
    site_index: SiteIndex | None = None
    site_index_until: float = 0.0


@dataclass
class ProbeOutcome:
    variant: MarkdownVariant | None = None
    site_index: SiteIndex | None = None
    requests_made: int = 0
    tried: list[str] = field(default_factory=list)


_hosts: dict[str, _HostMemory] = {}


def reset_host_cache() -> None:
    """Forget every host answer (tests, and a host that wants a clean slate)."""
    _hosts.clear()


# ── recognizing markdown ────────────────────────────────────────────────────

_HTML_START = re.compile(r"^\s*(<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])", re.I)
_MD_SIGNS = (
    re.compile(r"^#{1,6}\s+\S", re.M),
    re.compile(r"^\s*[-*+]\s+\S", re.M),
    re.compile(r"^```", re.M),
    re.compile(r"\[[^\]\n]+\]\([^)\n]+\)"),
    re.compile(r"^\s*\d+\.\s+\S", re.M),
    re.compile(r"\*\*[^*\n]+\*\*"),
)
_ERROR_WORDS = re.compile(
    r"\b(404|not found|page not found|access denied|forbidden|just a moment|enable javascript)\b",
    re.I,
)


def _looks_like_markdown(body: str) -> bool:
    if not body or _HTML_START.match(body):
        return False
    head = body[:4000]
    if head.count("<div") + head.count("<script") + head.count("<span") > 3:
        return False
    return sum(1 for sign in _MD_SIGNS if sign.search(body[:20000])) >= 2


def _is_markdown_response(resp: ProbeResponse | None) -> bool:
    if resp is None or resp.status != 200:
        return False
    body = resp.body or ""
    if len(body.strip()) < MIN_MARKDOWN_CHARS or _HTML_START.match(body):
        return False
    ctype = (resp.content_type or "").lower()
    if any(t in ctype for t in MARKDOWN_TYPES):
        return True
    if "html" in ctype:
        return False
    # A plain-text answer (raw.githubusercontent serves text/plain) is accepted
    # only when the body is unmistakably markdown and not a short error note.
    if len(body) < 400 and _ERROR_WORDS.search(body):
        return False
    return _looks_like_markdown(body)


_WORD = re.compile(r"[a-z][a-z0-9]{3,}")


def _words(text: str, limit: int = 600) -> list[str]:
    seen: dict[str, None] = {}
    for word in _WORD.findall(text.lower()):
        seen.setdefault(word, None)
        if len(seen) >= limit:
            break
    return list(seen)


def _same_content(markdown: str, page_text: str, *, declared: bool) -> bool:
    """Is this markdown clearly the page's own content? Word overlap, so a soft
    404 that redirects to a home page or a different article fails."""
    if not page_text.strip():
        # Nothing to compare with: only a site-declared twin earns trust.
        return declared
    md_words = _words(markdown)
    if not md_words:
        return False
    page = set(_words(page_text, limit=20000))
    share = sum(1 for w in md_words if w in page) / len(md_words)
    return share >= (MIN_OVERLAP_DECLARED if declared else MIN_OVERLAP)


# ── candidate URLs ──────────────────────────────────────────────────────────


class _AlternateFinder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []
        self.done = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "link":
            a = {k.lower(): (v or "") for k, v in attrs}
            rels = a.get("rel", "").lower().split()
            ctype = a.get("type", "").lower().split(";")[0].strip()
            if "alternate" in rels and ctype in MARKDOWN_TYPES and a.get("href"):
                self.hrefs.append(a["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self.done = True


def find_link_alternate(html: str | None, base_url: str) -> str | None:
    """The markdown twin the page itself declares, or None."""
    if not html:
        return None
    finder = _AlternateFinder()
    try:
        finder.feed(html[:200_000])
    except Exception:  # noqa: BLE001 — malformed head is an ordinary case
        return None
    for href in finder.hrefs:
        resolved = urljoin(base_url, href.strip())
        if urlsplit(resolved).scheme in ("http", "https"):
            return resolved
    return None


def sibling_markdown_url(url: str) -> str | None:
    """``/a/b`` -> ``/a/b.md``; ``/a/b/`` and ``/`` -> ``.../index.md``.
    None for URLs that already point at a file with an extension."""
    parts = urlsplit(url)
    path = parts.path or "/"
    last = path.rsplit("/", 1)[-1]
    if "." in last and not path.endswith("/"):
        return None
    new_path = path + "index.md" if path.endswith("/") else path + ".md"
    return urlunsplit((parts.scheme, parts.netloc, new_path, "", ""))


_REPO_HOSTS = {"github.com": "https://raw.githubusercontent.com"}


def raw_source_url(url: str) -> str | None:
    """A code-hosting repo page's raw markdown: the repo root maps to its
    README, a ``/blob/<ref>/<file>.md`` page to that file. None elsewhere —
    the sibling/negotiation signals do not apply on such hosts."""
    parts = urlsplit(url)
    raw_host = _REPO_HOSTS.get((parts.netloc or "").lower().removeprefix("www."))
    if not raw_host:
        return None
    segs = [x for x in parts.path.split("/") if x]
    if len(segs) == 2:
        return f"{raw_host}/{segs[0]}/{segs[1]}/HEAD/README.md"
    if len(segs) >= 5 and segs[2] == "blob" and segs[-1].lower().endswith((".md", ".markdown")):
        return f"{raw_host}/{segs[0]}/{segs[1]}/{segs[3]}/{'/'.join(segs[4:])}"
    return None


def sibling_markdown_txt_url(url: str) -> str | None:
    """``/a/b`` -> ``/a/b.md.txt`` — the spelling some doc platforms use."""
    md = sibling_markdown_url(url)
    return md + ".txt" if md else None


# ── the default fetch client ────────────────────────────────────────────────


async def _default_fetcher(url: str, accept_markdown: bool) -> ProbeResponse | None:
    # Imported lazily: scraper.py is the package's one fetch client and this
    # module is imported by the orchestrator that already depends on it.
    from matrx_scraper.scraper import RequestType, fetch

    # A plain, machine-reader request: these are asks for a file, not a page
    # view, and browser-navigation headers make some sites answer with a
    # sign-in redirect instead of the file.
    accept = (
        "text/markdown, text/plain;q=0.8, */*;q=0.1"
        if accept_markdown
        else "text/markdown, text/plain;q=0.9, text/html;q=0.5, */*;q=0.1"
    )
    profile = {"name": "reader", "headers": {"User-Agent": READER_USER_AGENT, "Accept": accept}}
    resp = await fetch(url, request_type=RequestType.NORMAL, header_profile=profile)
    if resp.failed:
        return ProbeResponse(resp.status_code or 0, resp.content_type_raw or "", "", url)
    return ProbeResponse(
        resp.status_code,
        resp.content_type_raw or "",
        resp.content or "",
        resp.response_url or url,
    )


# ── the probe ───────────────────────────────────────────────────────────────


async def _probe_site_index(
    host_url: str, memory: _HostMemory, fetcher: Fetcher, now: float
) -> SiteIndex | None:
    if memory.site_index_until > now:
        return memory.site_index
    parts = urlsplit(host_url)
    root = f"{parts.scheme}://{parts.netloc}"
    index = SiteIndex()
    for name, attr in (("llms.txt", "llms_txt_url"), ("llms-full.txt", "llms_full_txt_url")):
        candidate = f"{root}/{name}"
        try:
            resp = await fetcher(candidate, False)
        except Exception:  # noqa: BLE001 — a failed probe is a negative, never an error
            resp = None
        if (
            resp is not None
            and resp.status == 200
            and len((resp.body or "").strip()) >= MIN_MARKDOWN_CHARS
            and not _HTML_START.match(resp.body or "")
            and "html" not in (resp.content_type or "").lower()
        ):
            setattr(index, attr, candidate)
        if name == "llms.txt" and index.llms_txt_url is None:
            break  # no index at all: skip the bigger file, remember the negative
    memory.site_index = index if (index.llms_txt_url or index.llms_full_txt_url) else None
    memory.site_index_until = now + LIMITS.site_index_ttl
    return memory.site_index


async def probe_markdown_variant(
    url: str,
    *,
    html: str | None,
    page_text: str | None,
    fetcher: Fetcher | None = None,
    now: float | None = None,
) -> ProbeOutcome:
    """Look for the page's markdown twin. Never raises."""
    fetcher = fetcher or _default_fetcher
    now = time.monotonic() if now is None else now
    outcome = ProbeOutcome()
    host = (urlsplit(url).netloc or "").lower()
    if not host:
        return outcome
    memory = _hosts.setdefault(host, _HostMemory())
    text = page_text or ""

    budget = MAX_EXTRA_REQUESTS if memory.probed else MAX_EXTRA_REQUESTS_FIRST_CONTACT
    memory.probed = True

    async def attempt(candidate: str, accept: bool, signal: str, declared: bool) -> bool:
        if outcome.requests_made >= budget:
            return False
        outcome.requests_made += 1
        outcome.tried.append(signal)
        try:
            resp = await fetcher(candidate, accept)
        except Exception:  # noqa: BLE001 — a failed probe is a negative
            return False
        if not _is_markdown_response(resp):
            return False
        assert resp is not None
        explicit_type = any(t in (resp.content_type or "").lower() for t in MARKDOWN_TYPES)
        # With no page text to compare (the HTML read failed), only a body the
        # site itself labels markdown is trusted; otherwise it must match the page.
        if not text.strip() and not declared:
            if not explicit_type:
                return False
        elif not _same_content(resp.body, text, declared=declared):
            return False
        outcome.variant = MarkdownVariant(
            markdown=resp.body,
            url=resp.final_url or candidate,
            signal=signal,
            note=_NOTES[signal],
        )
        return True

    declared = find_link_alternate(html, url)
    if declared and declared.split("#")[0] != url.split("#")[0]:
        if await attempt(declared, False, SIGNAL_LINK, True):
            return await _finish(outcome, url, memory, fetcher, now)

    raw = raw_source_url(url)
    if raw:
        if await attempt(raw, False, SIGNAL_RAW_SOURCE, False):
            return await _finish(outcome, url, memory, fetcher, now)
        return await _finish(outcome, url, memory, fetcher, now)

    sibling = sibling_markdown_url(url)
    if sibling and (memory.sibling_works or memory.no_sibling_until <= now):
        if await attempt(sibling, False, SIGNAL_SIBLING, False):
            memory.sibling_works = True
            return await _finish(outcome, url, memory, fetcher, now)
        if SIGNAL_SIBLING in outcome.tried and not memory.sibling_works:
            memory.no_sibling_until = now + LIMITS.negative_ttl

    sibling_txt = sibling_markdown_txt_url(url)
    if sibling_txt and (memory.sibling_txt_works or memory.no_sibling_txt_until <= now):
        if await attempt(sibling_txt, False, SIGNAL_SIBLING_TXT, False):
            memory.sibling_txt_works = True
            return await _finish(outcome, url, memory, fetcher, now)
        if SIGNAL_SIBLING_TXT in outcome.tried and not memory.sibling_txt_works:
            memory.no_sibling_txt_until = now + LIMITS.negative_ttl

    if memory.no_negotiation_until <= now:
        if await attempt(url, True, SIGNAL_NEGOTIATION, False):
            return await _finish(outcome, url, memory, fetcher, now)
        if SIGNAL_NEGOTIATION in outcome.tried:
            memory.no_negotiation_until = now + LIMITS.negative_ttl

    return await _finish(outcome, url, memory, fetcher, now)


_NOTES = {
    SIGNAL_LINK: "The site links its own clean markdown version of this page; it is attached.",
    SIGNAL_SIBLING: "The site serves a clean markdown version of this page; it is attached.",
    SIGNAL_SIBLING_TXT: "The site serves a clean markdown version of this page; it is attached.",
    SIGNAL_RAW_SOURCE: "The page's own markdown source was found and is attached.",
    SIGNAL_NEGOTIATION: (
        "The site answers with a clean markdown version of this page when asked; it is attached."
    ),
}


async def _finish(
    outcome: ProbeOutcome, url: str, memory: _HostMemory, fetcher: Fetcher, now: float
) -> ProbeOutcome:
    try:
        outcome.site_index = await _probe_site_index(url, memory, fetcher, now)
    except Exception:  # noqa: BLE001
        outcome.site_index = None
    return outcome


# ── attaching to a ScrapeResult ─────────────────────────────────────────────

#: Optional host ext: ``async (organization_id) -> bool`` for the
#: ``knowledge.scraper.prefer_markdown_variant`` knob (org-overridable).
PREFER_MARKDOWN_EXT = "prefer_markdown_variant"


async def prefer_markdown_enabled(organization_id: str | None) -> bool:
    from matrx_scraper._ext import get_ext, has_ext

    # KNOB MIRROR: knowledge.scraper.prefer_markdown_variant = true (platform default).
    if not has_ext(PREFER_MARKDOWN_EXT):
        return True
    try:
        value = get_ext(PREFER_MARKDOWN_EXT)(organization_id)
        if hasattr(value, "__await__"):
            value = await value
        return True if value is None else bool(value)
    except Exception:  # noqa: BLE001 — announced via the log, never a failed scrape
        import logging

        logging.getLogger(__name__).warning(
            "the prefer_markdown_variant knob could not be read; using its starting value",
            exc_info=True,
        )
        return True


async def attach_markdown_variant(
    result: Any,
    *,
    organization_id: str | None = None,
    fetcher: Fetcher | None = None,
    enabled: bool | None = None,
) -> None:
    """Probe for ``result.url``'s markdown twin and attach what is found.

    Adds ``markdown``, ``markdown_url``, ``markdown_source``, ``markdown_note``
    and ``site_index``; when the site's markdown is the richer text it also
    becomes ``markdown_renderable``/``text_data``. The HTML-derived fields are
    otherwise untouched. Never raises, bounded by :data:`LIMITS.timeout`.
    """
    rescue = not result.success and not result.raw_html
    if not rescue and not (result.success and result.content_type == "html" and result.raw_html):
        return
    if rescue and result.failure_reason == "domain_blocked":
        return  # WE refused this address; no probe goes there either
    if enabled is None:
        enabled = await prefer_markdown_enabled(organization_id)
    if not enabled:
        return
    page_text = result.main_content_text or result.text_data or result.markdown_renderable or ""
    try:
        outcome = await asyncio.wait_for(
            probe_markdown_variant(
                (result.url if rescue else (result.response_url or result.url)),
                html=result.raw_html,
                page_text=page_text,
                fetcher=fetcher,
            ),
            timeout=LIMITS.timeout,
        )
    except Exception:  # noqa: BLE001 — TimeoutError included; HTML result stands
        return
    if outcome.site_index is not None:
        result.site_index = {
            "llms_txt": outcome.site_index.llms_txt_url,
            "llms_full_txt": outcome.site_index.llms_full_txt_url,
        }
    variant = outcome.variant
    if variant is None:
        return
    result.markdown = variant.markdown
    result.markdown_url = variant.url
    result.markdown_source = variant.signal
    note = variant.note
    # The site's markdown is the cleanest extraction there is: it is used as the
    # page text unless it is clearly SHORTER than the page's own main content
    # (then it is a summary, and the HTML text stays the page text).
    main = result.main_content_text or ""
    if len(variant.markdown) >= 0.5 * len(main):
        result.markdown_renderable = variant.markdown
        result.text_data = variant.markdown
        note += " It is used as the page text."
    if rescue:
        # The HTML read failed but the site's own markdown answered: the page is
        # readable after all. Said plainly, and the failure trail stays as history.
        result.success = True
        result.content_type = "md"
        result.text_data = variant.markdown
        result.markdown_renderable = variant.markdown
        result.content_chars = len(variant.markdown)
        result.next_rung = result.next_rung_reason = result.next_rung_note = None
        result.next_rung_what_to_do = result.next_rung_estimated_seconds = None
        result.stopped_because = None
        result.failure_message = None
        result.failure_reason = None
        note = (
            "The normal page read failed, but the site serves a clean markdown version "
            "of this page, which was read instead."
        )
    result.markdown_note = note
