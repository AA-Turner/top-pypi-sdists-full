"""Pure RSS / Atom parsing — no HTTP, no DB. A fetched feed document in, typed entries out.

One parser for every feed the platform reads (news intake, the media catalog's blog and podcast
adapters). Port of newsjack's ``parseFeed`` / ``feedItemDict`` / ``cleanText``
(``detector_sources.go``), with two of its defects fixed:

- **RSS ``pubDate`` was never read.** Their decoder lower-cased element names, then looked up
  ``pubDate``, so every RSS 2.0 item lost its date. Element names match case-insensitively here.
- **The Google News publisher was lost.** Google News RSS links are ``news.google.com`` redirects;
  the real publisher is ``<source url="…">``. It is kept as ``source_url`` so the caller never
  mistakes the redirect for the article's identity.

It also reads what a podcast feed carries (the iTunes and Podcasting 2.0 namespaces): per entry
the enclosure, ``itunes:duration``, ``itunes:image`` and ``podcast:transcript``; per feed the
description, image, author, language, ``lastBuildDate`` and the RFC 5005 next-page
``atom:link rel="next"``.

A feed is a document from an arbitrary third party, so entity declarations are refused outright
(no billion-laughs, no external entities) and the parse never touches the network.
"""

from __future__ import annotations

import html
import re
from datetime import UTC, date, datetime, time, timedelta
from email.utils import parsedate_to_datetime
from typing import Literal
from xml.etree import ElementTree

from pydantic import BaseModel, ConfigDict, Field

from matrx_scraper.utils.proxy import redact_url_secrets

__all__ = [
    "FeedEntry",
    "FeedParseError",
    "ParsedFeed",
    "clean_text",
    "duration_seconds",
    "normalize_feed_date",
    "parse_feed",
]

_SCRIPT_STYLE = re.compile(r"(?is)<script[^>]*>.*?</script>|<style[^>]*>.*?</style>")
_TAGS = re.compile(r"(?s)<[^>]+>")
_SPACE = re.compile(r"\s+")
_RELATIVE = re.compile(r"(?i)^\s*(\d+)\s+(minute|minutes|hour|hours|day|days|week|weeks|month|months)\s+ago\s*$")
_DATE_ONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ENTITY_DECL = re.compile(rb"<!ENTITY", re.IGNORECASE)
# hh:mm:ss, mm:ss, or bare seconds — all three appear in <itunes:duration> in the wild.
_CLOCK = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})$")

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ATOM_NS = "http://www.w3.org/2005/Atom"
#: Podcasting 2.0; older feeds declare the namespace by its GitHub address.
PODCAST_NS = frozenset({
    "https://podcastindex.org/namespace/1.0",
    "https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md",
})

Precision = Literal["time", "date", "none"]


class FeedParseError(ValueError):
    """The document is not a readable RSS or Atom feed."""


class FeedEntry(BaseModel):
    """One item of a feed, as the feed published it."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    kind: Literal["feed_entry"] = Field(default="feed_entry", alias="__kind")
    id: str
    title: str
    url: str = ""
    excerpt: str = ""
    author: str | None = None
    container: str = ""
    published_at: str | None = None
    published_precision: Precision = "none"
    raw_published: str | None = None
    guid: str | None = None
    #: Google News (and other aggregators): the publisher named in ``<source>``.
    source_name: str | None = None
    source_url: str | None = None
    feed_title: str = ""
    feed_url: str = ""
    #: 1-based position among the entries kept, in document order (a front-page rank).
    feed_position: int
    # ── podcast fields (absent on an ordinary feed) ──
    enclosure_url: str | None = None
    enclosure_type: str | None = None
    enclosure_length: int | None = None
    #: ``<itunes:duration>`` as written, and in seconds when it is readable.
    itunes_duration: str | None = None
    duration_seconds: int | None = None
    #: ``<itunes:image href>`` of the entry.
    image_url: str | None = None
    #: The first ``<podcast:transcript>``.
    transcript_url: str | None = None
    transcript_type: str | None = None


class ParsedFeed(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    kind: Literal["parsed_feed"] = Field(default="parsed_feed", alias="__kind")
    title: str
    feed_url: str
    #: ``rss`` (RSS 2.0, which has a ``<channel>``), ``atom`` or ``rdf`` (RSS 1.0).
    format: Literal["rss", "atom", "rdf"] = "rss"
    description: str = ""
    #: The site the feed belongs to (RSS ``<link>``, Atom ``rel="alternate"``).
    link: str | None = None
    #: ``<itunes:image href>``, else RSS ``<image><url>``, else Atom ``<logo>``/``<icon>``.
    image_url: str | None = None
    author: str | None = None
    language: str | None = None
    #: ``<lastBuildDate>`` (Atom: the feed's ``<updated>``), normalized, and as written.
    last_build_date: str | None = None
    raw_last_build_date: str | None = None
    #: RFC 5005: the next page of a paged feed (``atom:link rel="next"``).
    next_url: str | None = None
    entries: list[FeedEntry] = Field(default_factory=list)


def clean_text(value: str | None) -> str:
    """Unescape, strip scripts/styles/tags, collapse whitespace."""
    text = html.unescape(value or "")
    text = _SCRIPT_STYLE.sub(" ", text)
    text = _TAGS.sub(" ", text)
    return _SPACE.sub(" ", text).strip()


def _iso_z(moment: datetime) -> str:
    text = moment.astimezone(UTC).replace(tzinfo=None).isoformat()
    if "." in text:
        head, _, frac = text.partition(".")
        frac = frac.rstrip("0")
        text = f"{head}.{frac}" if frac else head
    return f"{text}Z"


def normalize_feed_date(value: str | None, *, now: datetime | None = None) -> tuple[str | None, Precision]:
    """A feed's date as RFC 3339 UTC plus its precision. Unreadable → ``(None, "none")``.

    ``N hours ago`` resolves only when ``now`` is given (this module has no clock of its own).
    """
    raw = (value or "").strip()
    if not raw:
        return None, "none"
    if _DATE_ONLY.match(raw):
        try:
            date.fromisoformat(raw)
        except ValueError:
            return None, "none"
        return raw, "date"
    relative = _RELATIVE.match(raw)
    if relative:
        if now is None:
            return None, "none"
        n, unit = int(relative.group(1)), relative.group(2).lower()
        hours = {"minute": 1 / 60, "hour": 1, "day": 24, "week": 168, "month": 720}[unit.rstrip("s")]
        return _iso_z(now - timedelta(hours=n * hours)), "time"
    parsed: datetime | None
    try:
        parsed = datetime.fromisoformat(raw[:-1] + "+00:00" if raw.endswith("Z") else raw)
    except ValueError:
        try:
            parsed = parsedate_to_datetime(raw)
        except (TypeError, ValueError, IndexError):
            parsed = None
    if parsed is None:
        return None, "none"
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    if parsed.time() == time.min and "T" not in raw and ":" not in raw:
        return parsed.date().isoformat(), "date"
    return _iso_z(parsed), "time"


def duration_seconds(raw: str | None) -> int | None:
    """``<itunes:duration>`` is hh:mm:ss, mm:ss or bare seconds. All three occur."""
    text = (raw or "").strip()
    if not text:
        return None
    match = _CLOCK.match(text)
    if match:
        hours, minutes, seconds = match.groups()
        return int(hours or 0) * 3600 + int(minutes) * 60 + int(seconds)
    try:
        return int(float(text))
    except ValueError:
        return None


def _as_int(value: str | None) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _ns(tag: object) -> str:
    text = str(tag)
    return text[1:].split("}", 1)[0] if text.startswith("{") else ""


def _local(tag: object) -> str:
    text = str(tag)
    return (text.rsplit("}", 1)[-1] if "}" in text else text.rsplit(":", 1)[-1]).lower()


def _text(element: ElementTree.Element) -> str:
    return "".join(element.itertext()).strip()


def _link(element: ElementTree.Element) -> str:
    href = (element.get("href") or "").strip()
    return href or _text(element)


def _entry(
    element: ElementTree.Element, feed_title: str, feed_url: str, position: int, now: datetime | None
) -> FeedEntry | None:
    fields: dict[str, str] = {}
    link = ""
    alt_link = ""
    source_url = None
    podcast: dict[str, object] = {}
    for child in element:
        name = _local(child.tag)
        ns = _ns(child.tag)
        if name == "enclosure" and child.get("url") and "enclosure_url" not in podcast:
            podcast["enclosure_url"] = child.get("url", "").strip()
            podcast["enclosure_type"] = (child.get("type") or "").strip() or None
            podcast["enclosure_length"] = _as_int(child.get("length"))
            continue
        if ns == ITUNES_NS and name == "image":
            podcast.setdefault("image_url", (child.get("href") or "").strip() or None)
            continue
        if ns == ITUNES_NS and name == "duration":
            podcast.setdefault("itunes_duration", _text(child) or None)
            continue
        if ns in PODCAST_NS and name == "transcript":
            if child.get("url") and "transcript_url" not in podcast:
                podcast["transcript_url"] = child.get("url", "").strip()
                podcast["transcript_type"] = (child.get("type") or "").strip() or None
            continue
        if name == "link":
            rel = (child.get("rel") or "alternate").lower()
            value = _link(child)
            if rel == "alternate" and value and not alt_link:
                alt_link = value
            elif value and not link:
                link = value
            continue
        if name == "source" and child.get("url"):
            source_url = child.get("url", "").strip() or None
        if name in ("author", "contributor") and len(child):
            value = " ".join(_text(c) for c in child if _local(c.tag) == "name")
        else:
            value = _text(child)
        if value:
            fields[name] = f"{fields[name]} {value}" if name in fields else value
    title = clean_text(fields.get("title"))
    excerpt = clean_text(fields.get("description") or fields.get("summary") or fields.get("encoded")
                         or fields.get("content"))
    if not title and not excerpt and not podcast.get("enclosure_url"):
        return None
    if not title:
        title = excerpt[:120]
    guid = (fields.get("guid") or fields.get("id") or "").strip() or None
    url = (alt_link or link or (guid if guid and guid.startswith(("http://", "https://")) else "")).strip()
    raw_date = (fields.get("pubdate") or fields.get("published") or fields.get("date") or fields.get("updated")
                or fields.get("issued") or "").strip()
    published_at, precision = normalize_feed_date(raw_date, now=now)
    source_name = clean_text(fields.get("source")) or None
    author = clean_text(fields.get("author") or fields.get("creator")) or None
    return FeedEntry(
        id=guid or url or f"{feed_url}#{position}",
        title=title,
        url=url,
        excerpt=excerpt,
        author=author,
        container=source_name or feed_title,
        published_at=published_at,
        published_precision=precision,
        raw_published=raw_date or None,
        guid=guid,
        source_name=source_name,
        source_url=source_url,
        feed_title=feed_title,
        feed_url=feed_url,
        feed_position=position,
        duration_seconds=duration_seconds(podcast.get("itunes_duration")),  # type: ignore[arg-type]
        **podcast,  # type: ignore[arg-type]
    )


def _channel_meta(container: ElementTree.Element, now: datetime | None) -> dict[str, object]:
    """The feed-level fields, read from the channel's (or Atom feed's) direct children only."""
    first: dict[tuple[str, str], ElementTree.Element] = {}
    next_url = link = None
    for child in container:
        name, ns = _local(child.tag), _ns(child.tag)
        if name == "link":
            rel = (child.get("rel") or "").lower()
            href = (child.get("href") or "").strip()
            if rel == "next" and href and next_url is None:
                next_url = href
            elif not rel or rel == "alternate":
                value = href or _text(child)
                if value and link is None:
                    link = value
            continue
        first.setdefault((ns, name), child)

    def text(*keys: tuple[str, str]) -> str | None:
        for key in keys:
            node = first.get(key)
            if node is not None and (value := _text(node)):
                return value
        return None

    atom = _ns(container.tag) or ATOM_NS
    image = first.get((ITUNES_NS, "image"))
    image_url = (image.get("href") or "").strip() or None if image is not None else None
    if image_url is None and (rss_image := first.get(("", "image"))) is not None:
        image_url = next((_text(c) for c in rss_image if _local(c.tag) == "url" and _text(c)), None)
    image_url = image_url or text((atom, "logo"), (atom, "icon"))
    author = text((ITUNES_NS, "author"))
    if author is None and (atom_author := first.get((atom, "author"))) is not None:
        author = " ".join(_text(c) for c in atom_author if _local(c.tag) == "name") or _text(atom_author) or None
    raw_built = text(("", "lastbuilddate"), (atom, "updated"))
    built, _ = normalize_feed_date(raw_built, now=now)
    language = text(("", "language")) or container.get("{http://www.w3.org/XML/1998/namespace}lang")
    description = text(("", "description"), (atom, "subtitle"), (ITUNES_NS, "summary"), (ITUNES_NS, "subtitle"))
    return {
        "description": clean_text(description),
        "link": link,
        "image_url": image_url,
        "author": clean_text(author) or None,
        "language": (language or "").strip() or None,
        "last_build_date": built,
        "raw_last_build_date": raw_built,
        "next_url": next_url,
    }


def parse_feed(
    document: str | bytes, feed_url: str, *, limit: int | None = None, now: datetime | None = None
) -> ParsedFeed:
    """Parse an RSS 2.0, RSS 1.0 (RDF) or Atom document. Raises :class:`FeedParseError`."""
    raw = document.encode() if isinstance(document, str) else document
    if _ENTITY_DECL.search(raw):
        raise FeedParseError(
            f"feed {redact_url_secrets(feed_url)!r} declares XML entities; refusing to parse it"
        )
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError as exc:
        raise FeedParseError(
            f"feed {redact_url_secrets(feed_url)!r} is not well-formed XML: "
            f"{redact_url_secrets(exc)}"
        ) from None
    root_name = _local(root.tag)
    if root_name not in {"rss", "feed", "rdf"}:
        raise FeedParseError(
            f"feed {redact_url_secrets(feed_url)!r} is not RSS or Atom "
            f"(root element <{root_name}>)"
        )

    items = [element for element in root.iter() if _local(element.tag) in {"item", "entry"}]
    feed_title = ""
    containers = [root, *(child for child in root if _local(child.tag) == "channel")]
    for container in containers:
        for child in container:
            if _local(child.tag) == "title" and (text := clean_text(_text(child))):
                feed_title = text
                break
        if feed_title:
            break
    feed_title = feed_title or feed_url
    channel = next((c for c in root if _local(c.tag) == "channel"), None)
    meta = _channel_meta(channel if channel is not None else root, now)
    feed_format = {"rss": "rss", "feed": "atom", "rdf": "rdf"}[root_name]
    if feed_format == "rss" and channel is None:
        feed_format = "rdf"

    entries: list[FeedEntry] = []
    for element in items:
        entry = _entry(element, feed_title, feed_url, len(entries) + 1, now)
        if entry is None:
            continue
        entries.append(entry)
        if limit is not None and limit > 0 and len(entries) >= limit:
            break
    return ParsedFeed(title=feed_title, feed_url=feed_url, format=feed_format, entries=entries, **meta)
