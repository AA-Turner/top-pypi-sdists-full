"""SEO audit extractor — server-side equivalent of matrx-extend's audit.ts.

This is the canonical "what does a page look like for SEO?" routine in the
package. Both the crawler and any host that wants a one-shot audit (e.g. an
admin endpoint that audits a single URL) call this so the output shape is
identical to what the chrome-extension renders in its side panel.

Input: parsed HTML (string) OR an already-built BeautifulSoup-like document.
Output: the same field set the extension uses, plus a few extras the
crawler benefits from (text_hash, sentence_count).

Two halves, one module:

1. **Evidence** — `audit_html` extracts what the page IS.
2. **Checks** — `PAGE_CHECKS` / `run_page_checks` decide whether that evidence
   is GOOD. This is the ONE implementation of every per-page SEO verdict in
   the platform; every threshold it uses is a named CAPS constant here (or,
   for the SERP length limits, imported from `meta_metrics`, which owns them
   as a byte-identical mirror of the TypeScript implementation). Consumers —
   `web_crawl/analysis.py`, agent tools, admin one-shot audits — call these
   functions; they never re-derive a verdict from raw evidence.

Cross-page work (duplicate titles across a crawl, site rollups) is a
DIFFERENT job and deliberately lives in `web_crawl/analysis.py` — it needs a
whole site, not a page.

🚨 THE MIRROR IS ENFORCED — a counting rule here cannot change alone.
matrx-extend's `src/lib/seo/audit.ts` is the live-DOM second implementation of
`audit_html`: it audits the rendered DOM the user is looking at, this audits
the HTML the server fetched. On an SPA those are different pages, which is why
both exist — but the RULES must agree, and four numeric ones drifted apart
silently before 2026-08-09 with both sides persisting different numbers for the
same page. `tests/__fixtures__/seo-audit-parity.json` is now generated from THIS
function and replayed through the TypeScript. Change a rule below → regenerate
and make the matching TS change in the same unit of work:

    .venv/bin/python packages/matrx-scraper/scripts/generate_seo_audit_parity_fixture.py

`tests/test_seo_audit_parity_fixture.py` fails if you forget.

Standalone — does not import from matrx-connect, matrx-orm, or aidream.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from urllib.parse import parse_qsl, urljoin, urlparse, urlsplit

from pydantic import BaseModel, Field, JsonValue
from selectolax.parser import HTMLParser

from matrx_scraper.audit_metrics import evaluate_indexability
from matrx_scraper.media_embed import video_embed_provider
from matrx_scraper.meta_metrics import (
    DESCRIPTION_SEO_MAX_CHARS,
    DESCRIPTION_SEO_MIN_CHARS,
    TITLE_SEO_MAX_CHARS,
    TITLE_SEO_MIN_CHARS,
    calculate_meta_description_metrics,
    calculate_meta_title_metrics,
)
from matrx_scraper.parser.hashing import compute_text_fingerprint
from matrx_scraper.structured_data import extract_structured_payload


@dataclass
class HeadingItem:
    level: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level, "text": self.text}


@dataclass
class HreflangItem:
    lang: str
    href: str

    def to_dict(self) -> dict[str, Any]:
        return {"lang": self.lang, "href": self.href}


@dataclass
class LinkItem:
    target_url: str
    anchor_text: str
    rel: str | None
    link_type: str  # internal | external | subdomain
    nofollow: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_url": self.target_url,
            "anchor_text": self.anchor_text,
            "rel": self.rel,
            "link_type": self.link_type,
            "nofollow": self.nofollow,
        }


@dataclass
class SeoAuditResult:
    url: str
    title: str
    title_length: int
    meta_description: str | None
    meta_description_length: int
    canonical: str | None
    robots: str | None
    lang: str | None
    hreflang: list[HreflangItem]
    og: dict[str, str]
    twitter: dict[str, str]
    schema_types: list[str]
    schema_org: dict[str, Any]
    headings: list[HeadingItem]
    h1: list[str]
    h2: list[str]
    h1_count: int
    internal_links: int
    external_links: int
    link_count: int
    images_total: int
    images_missing_alt: int
    word_count: int
    sentence_count: int
    flesch_reading_ease: float | None
    # UTF-8 byte length of the SAME visible text `word_count` counts. The
    # numerator of `check_text_html_ratio`; its denominator is the raw HTML
    # byte size, which only the transport knows.
    text_bytes: int = 0
    text_hash: str | None = None
    # Duplicate-detection fingerprint over the same visible text as
    # word_count — see parser/hashing.compute_text_fingerprint (versioned).
    content_fingerprint: dict[str, Any] | None = None
    # Full link graph rows — full URL list with anchor text + rel
    links: list[LinkItem] = field(default_factory=list)
    # Mixed-content audit (http:// resources on https:// pages)
    mixed_content: list[str] = field(default_factory=list)
    # Pagination — {prev, next} from rel="prev"/"next" link tags.
    pagination: dict[str, Any] = field(default_factory=dict)
    # Complete raw + normalized JSON-LD, microdata, RDFa, and microformats.
    structured_data: dict[str, Any] = field(default_factory=dict)
    # Per-image evidence plus the complete DOM-declared resource inventory.
    image_inventory: list[dict[str, Any]] = field(default_factory=list)
    resources: dict[str, Any] = field(default_factory=dict)
    # Page identity signals such as CMS generator, author, dates, and hero.
    page_identity: dict[str, Any] = field(default_factory=dict)
    # Raw `<meta name="viewport">` content — the mobile-rendering contract.
    viewport: str | None = None
    # Raw `<meta http-equiv="refresh">` content ("5; url=https://…").
    meta_refresh: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "title_length": self.title_length,
            "meta_description": self.meta_description,
            "meta_description_length": self.meta_description_length,
            "canonical": self.canonical,
            "robots": self.robots,
            "lang": self.lang,
            "hreflang": [h.to_dict() for h in self.hreflang],
            "og": self.og,
            "twitter": self.twitter,
            "schema_types": self.schema_types,
            "schema_org": self.schema_org,
            "headings": [h.to_dict() for h in self.headings],
            "h1": self.h1,
            "h2": self.h2,
            "h1_count": self.h1_count,
            "internal_links": self.internal_links,
            "external_links": self.external_links,
            "link_count": self.link_count,
            "images_total": self.images_total,
            "images_missing_alt": self.images_missing_alt,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "flesch_reading_ease": self.flesch_reading_ease,
            "text_bytes": self.text_bytes,
            "text_hash": self.text_hash,
            "content_fingerprint": self.content_fingerprint,
            "structured_data": self.structured_data,
            "image_inventory": self.image_inventory,
            "resources": self.resources,
            "page_identity": self.page_identity,
            "viewport": self.viewport,
            "meta_refresh": self.meta_refresh,
        }


def audit_html(html: str, base_url: str) -> SeoAuditResult:
    """Run the full SEO audit on a raw HTML string.

    `base_url` is used to resolve relative hrefs and decide internal vs.
    external links. Pass the response URL (after any redirects) for accuracy.
    """
    if not html:
        return _empty_result(base_url)
    tree = HTMLParser(html)
    return _audit_tree(tree, base_url)


def _empty_result(url: str) -> SeoAuditResult:
    return SeoAuditResult(
        url=url,
        title="",
        title_length=0,
        meta_description=None,
        meta_description_length=0,
        canonical=None,
        robots=None,
        lang=None,
        hreflang=[],
        og={},
        twitter={},
        schema_types=[],
        schema_org={},
        headings=[],
        h1=[],
        h2=[],
        h1_count=0,
        internal_links=0,
        external_links=0,
        link_count=0,
        images_total=0,
        images_missing_alt=0,
        word_count=0,
        sentence_count=0,
        flesch_reading_ease=None,
    )


def _audit_tree(tree: HTMLParser, base_url: str) -> SeoAuditResult:
    body = tree.body

    # Title — both <title> text and <html lang>
    title = ""
    title_node = tree.css_first("title")
    if title_node and title_node.text():
        title = title_node.text(deep=True, separator="").strip()

    html_node = tree.css_first("html")
    lang = html_node.attributes.get("lang") if html_node else None

    # Meta tags
    meta_description: str | None = None
    robots: str | None = None
    og: dict[str, str] = {}
    twitter: dict[str, str] = {}
    viewport: str | None = None
    meta_refresh: str | None = None
    for meta in tree.css("meta"):
        attrs = meta.attributes
        name = (attrs.get("name") or "").lower()
        prop = (attrs.get("property") or "").lower()
        equiv = (attrs.get("http-equiv") or "").lower()
        content = attrs.get("content") or ""
        if not content:
            continue
        if name == "description" and meta_description is None:
            meta_description = content
        elif name == "robots" and robots is None:
            robots = content
        elif name == "viewport" and viewport is None:
            viewport = content
        elif equiv == "refresh" and meta_refresh is None:
            meta_refresh = content
        elif name.startswith("twitter:"):
            twitter[name] = content
        elif prop.startswith("og:"):
            og[prop] = content

    # Canonical
    canonical: str | None = None
    canonical_link = tree.css_first('link[rel="canonical"]')
    if canonical_link:
        canonical = canonical_link.attributes.get("href") or None

    # hreflang variants
    hreflang: list[HreflangItem] = []
    for link in tree.css('link[rel="alternate"]'):
        hl = link.attributes.get("hreflang")
        href = link.attributes.get("href")
        if hl and href:
            hreflang.append(HreflangItem(lang=hl, href=href))

    structured = extract_structured_payload(tree.html, base_url)
    schema_types = structured.schema_types
    schema_org = structured.schema_org

    # Headings
    headings: list[HeadingItem] = []
    h1: list[str] = []
    h2: list[str] = []
    for h in tree.css("h1, h2, h3, h4, h5, h6"):
        try:
            level = int(h.tag[1])
        except (ValueError, IndexError):
            continue
        text = (h.text(deep=True, separator=" ") or "").strip()
        if not text:
            continue
        headings.append(HeadingItem(level=level, text=text))
        if level == 1:
            h1.append(text)
        elif level == 2:
            h2.append(text)
        if len(headings) >= 200:
            break

    # Links — capture target URL, anchor text, rel, type
    base_parsed = urlparse(base_url)
    base_host = base_parsed.netloc.lower()
    base_reg = ".".join(base_host.split(".")[-2:]) if base_host else ""
    is_https = base_parsed.scheme == "https"
    internal = 0
    external = 0
    links: list[LinkItem] = []
    seen_targets: set[str] = set()
    for a in tree.css("a[href]"):
        href = a.attributes.get("href")
        if not href:
            continue
        try:
            u = urljoin(base_url, href)
            host = urlparse(u).netloc.lower()
        except Exception:
            continue
        if not host or not u.startswith(("http://", "https://")):
            continue
        if host == base_host:
            link_type = "internal"
            internal += 1
        elif base_reg and host.endswith("." + base_reg) or host == base_reg:
            link_type = "subdomain"
            external += 1
        else:
            link_type = "external"
            external += 1
        rel = a.attributes.get("rel")
        anchor_raw = (a.text(deep=True, separator=" ") or "").strip()
        if len(anchor_raw) > 500:
            anchor_raw = anchor_raw[:500]
        nofollow = bool(rel and "nofollow" in rel.lower())
        # Dedup by (url, anchor) — most pages have many duplicate nav links;
        # we keep one representative per anchor.
        key = u + "\x00" + anchor_raw.lower()
        if key in seen_targets:
            continue
        seen_targets.add(key)
        links.append(
            LinkItem(
                target_url=u,
                anchor_text=anchor_raw,
                rel=rel,
                link_type=link_type,
                nofollow=nofollow,
            )
        )
        if len(links) >= 2000:
            break

    # Pagination — rel="prev"/"next" link tags
    pagination: dict[str, Any] = {}
    for el in tree.css('link[rel="prev"], link[rel="next"]'):
        rel = (el.attributes.get("rel") or "").lower().strip()
        href = el.attributes.get("href")
        if rel and href:
            pagination[rel] = urljoin(base_url, href)

    # Mixed-content audit — http:// resources loaded on an https:// page
    mixed_content: list[str] = []
    if is_https:
        for sel in (
            "img[src]",
            "script[src]",
            "link[href]",
            "iframe[src]",
            "video[src]",
            "audio[src]",
            "source[src]",
        ):
            for el in tree.css(sel):
                attr = "src" if sel != "link[href]" else "href"
                v = el.attributes.get(attr)
                if v and v.startswith("http://"):
                    mixed_content.append(v)
                    if len(mixed_content) >= 50:
                        break
            if len(mixed_content) >= 50:
                break

    image_inventory, resources = _extract_page_resources(tree, base_url)
    _append_structured_resources(resources, structured.to_dict(), base_url)
    images_total = len(tree.css("img"))
    images_missing_alt = sum(
        1 for img in tree.css("img") if not (img.attributes.get("alt") or "").strip()
    )
    page_identity = _extract_page_identity(
        tree,
        base_url,
        og=og,
        twitter=twitter,
        structured_data=structured.to_dict(),
    )
    featured_url = page_identity.get("featured_image")
    if isinstance(featured_url, str):
        for item in image_inventory:
            if item.get("src") == featured_url or featured_url in item.get("srcset", []):
                item["featured"] = True

    # Word/sentence counts on visible text
    text = ""
    if body:
        text = (body.text(deep=True, separator=" ") or "").strip()
        text = re.sub(r"\s+", " ", text)
    words = text.split() if text else []
    word_count = len(words)
    sentences = re.split(r"[.!?]+\s+", text) if text else []
    sentence_count = len([s for s in sentences if s.strip()]) or (1 if text else 0)
    flesch = _flesch_reading_ease(text, word_count, sentence_count)
    fingerprint = compute_text_fingerprint(text)

    return SeoAuditResult(
        url=base_url,
        title=title,
        title_length=len(title),
        meta_description=meta_description,
        meta_description_length=len(meta_description) if meta_description else 0,
        canonical=canonical,
        robots=robots,
        lang=lang,
        hreflang=hreflang,
        og=og,
        twitter=twitter,
        schema_types=schema_types,
        schema_org=schema_org,
        headings=headings,
        h1=h1,
        h2=h2,
        h1_count=len(h1),
        internal_links=internal,
        external_links=external,
        link_count=internal + external,
        images_total=images_total,
        images_missing_alt=images_missing_alt,
        word_count=word_count,
        sentence_count=sentence_count,
        flesch_reading_ease=flesch,
        text_bytes=len(text.encode("utf-8")),
        text_hash=fingerprint["exact_sha256"] if fingerprint else None,
        content_fingerprint=fingerprint,
        links=links,
        mixed_content=mixed_content,
        pagination=pagination,
        structured_data=structured.to_dict(),
        image_inventory=image_inventory,
        resources=resources,
        page_identity=page_identity,
        viewport=viewport,
        meta_refresh=meta_refresh,
    )


_DOCUMENT_EXTENSIONS = {
    "csv",
    "doc",
    "docx",
    "epub",
    "md",
    "odt",
    "pdf",
    "ppt",
    "pptx",
    "rtf",
    "txt",
    "xls",
    "xlsx",
}
_FONT_EXTENSIONS = {"eot", "otf", "ttf", "woff", "woff2"}
_IMAGE_EXTENSIONS = {
    "apng",
    "avif",
    "bmp",
    "gif",
    "ico",
    "jpeg",
    "jpg",
    "png",
    "svg",
    "webp",
}
_VIDEO_EXTENSIONS = {"m3u8", "m4v", "mov", "mp4", "ogv", "webm"}
_AUDIO_EXTENSIONS = {"aac", "flac", "m4a", "mp3", "oga", "ogg", "wav"}
_RESOURCE_LIMIT = 5000
# Per-page cap on the `image_inventory` items persisted into
# web.snapshot.images.items (counts stay uncapped/true totals).
IMAGE_INVENTORY_LIMIT = 100


def _resolved_url(base_url: str, value: str | None) -> str | None:
    if not value:
        return None
    cleaned = value.strip()
    if not cleaned or cleaned.startswith(("#", "data:", "blob:", "javascript:")):
        return None
    try:
        resolved = urljoin(base_url, cleaned)
    except Exception:
        return None
    return resolved if resolved.startswith(("http://", "https://")) else None


def _srcset_urls(base_url: str, value: str | None) -> list[str]:
    if not value:
        return []
    output: list[str] = []
    for entry in value.split(","):
        candidate = entry.strip().split()[0] if entry.strip() else ""
        resolved = _resolved_url(base_url, candidate)
        if resolved and resolved not in output:
            output.append(resolved)
    return output


def _number_attribute(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\d+", value)
    return int(match.group()) if match else None


_IMAGE_FORMAT_ALIASES = {"jpeg": "jpg", "tiff": "tif"}


def _srcset_widths(value: str | None) -> list[int]:
    """The intrinsic widths an author DECLARES via srcset ``w`` descriptors.

    This is the only intrinsic-size evidence available from HTML alone — real
    decoded dimensions and transfer bytes both need a fetch, which the crawl
    never makes for sub-resources. `check_image_oversized` reads it.
    """
    if not value:
        return []
    widths: set[int] = set()
    for entry in value.split(","):
        tokens = entry.strip().split()
        for token in tokens[1:]:
            if token.endswith("w"):
                parsed = _number_attribute(token)
                if parsed:
                    widths.add(parsed)
    return sorted(widths)


def _image_format(url: str | None) -> str | None:
    """Raster/vector format from a URL path extension, `None` when unknowable.

    A CDN URL that carries no extension (`/cdn-cgi/image/w=800/hero`) genuinely
    does not declare a format — callers must treat `None` as "not captured",
    never as "legacy".
    """
    if not url:
        return None
    tail = urlparse(url).path.lower().rsplit("/", 1)[-1]
    if "." not in tail:
        return None
    suffix = tail.rsplit(".", 1)[-1]
    if suffix not in _IMAGE_EXTENSIONS:
        return None
    return _IMAGE_FORMAT_ALIASES.get(suffix, suffix)


def _picture_source_formats(node: Any, base_url: str) -> list[str]:
    """Formats the enclosing ``<picture>`` offers instead of the ``<img>`` src.

    Without this the CORRECT modern-format pattern —
    ``<picture><source type="image/avif"><img src="hero.jpg"></picture>`` —
    reads as a legacy JPEG, and `check_image_modern_format` would punish the one
    markup shape it exists to reward.
    """
    parent = node.parent
    if parent is None or parent.tag != "picture":
        return []
    formats: set[str] = set()
    for source in parent.css("source"):
        attrs = source.attributes
        mime_type = (attrs.get("type") or "").strip().lower()
        if mime_type.startswith("image/"):
            subtype = mime_type.split("/", 1)[1]
            formats.add(_IMAGE_FORMAT_ALIASES.get(subtype, subtype))
        for candidate in _srcset_urls(base_url, attrs.get("srcset") or attrs.get("data-srcset")):
            resolved = _image_format(candidate)
            if resolved:
                formats.add(resolved)
    return sorted(formats)


def _picture_source_urls(node: Any, base_url: str) -> list[str]:
    parent = node.parent
    if parent is None or parent.tag != "picture":
        return []
    urls: list[str] = []
    for source in parent.css("source"):
        for candidate in _srcset_urls(
            base_url,
            source.attributes.get("srcset") or source.attributes.get("data-srcset"),
        ):
            if candidate not in urls:
                urls.append(candidate)
    return urls


def _resource_kind(tag: str, url: str, rel: str, mime_type: str) -> str:
    path = urlparse(url).path.lower()
    suffix = path.rsplit(".", 1)[-1] if "." in path.rsplit("/", 1)[-1] else ""
    if tag in {"img", "picture"}:
        return "image"
    if tag in {"video"}:
        return "video"
    if tag == "audio":
        return "audio"
    if tag in {"iframe", "embed", "object"}:
        return "embed"
    if tag == "script":
        return "script"
    if "stylesheet" in rel or suffix == "css":
        return "stylesheet"
    if "icon" in rel:
        return "icon"
    if "manifest" in rel:
        return "manifest"
    if suffix in _FONT_EXTENSIONS or mime_type.startswith("font/"):
        return "font"
    if suffix in _IMAGE_EXTENSIONS or mime_type.startswith("image/"):
        return "image"
    if suffix in _VIDEO_EXTENSIONS or mime_type.startswith("video/"):
        return "video"
    if suffix in _AUDIO_EXTENSIONS or mime_type.startswith("audio/"):
        return "audio"
    if suffix in _DOCUMENT_EXTENSIONS:
        return "document"
    if tag == "track":
        return "track"
    if tag == "source":
        if mime_type.startswith("video/"):
            return "video"
        if mime_type.startswith("audio/"):
            return "audio"
        if mime_type.startswith("image/"):
            return "image"
    return "other"


def _extract_page_resources(
    tree: HTMLParser,
    base_url: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    images: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    counts: dict[str, int] = {}
    total_observed = 0

    def add(
        *,
        tag: str,
        url: str | None,
        source_attribute: str,
        rel: str = "",
        mime_type: str = "",
        attributes: dict[str, Any] | None = None,
        kind: str | None = None,
    ) -> None:
        nonlocal total_observed
        if not url:
            return
        resolved = _resolved_url(base_url, url)
        if not resolved:
            return
        resolved_kind = kind or _resource_kind(tag, resolved, rel, mime_type)
        key = (resolved_kind, resolved)
        if key in seen:
            return
        seen.add(key)
        total_observed += 1
        counts[resolved_kind] = counts.get(resolved_kind, 0) + 1
        if len(items) >= _RESOURCE_LIMIT:
            return
        item: dict[str, Any] = {
            "kind": resolved_kind,
            "url": resolved,
            "tag": tag,
            "source_attribute": source_attribute,
        }
        if rel:
            item["rel"] = rel
        if mime_type:
            item["mime_type"] = mime_type
        if attributes:
            item["attributes"] = attributes
        items.append(item)

    for img in tree.css("img"):
        attrs = img.attributes
        src = next(
            (
                _resolved_url(base_url, attrs.get(name))
                for name in (
                    "src",
                    "data-src",
                    "data-lazy-src",
                    "data-original",
                    "nitro-lazy-src",
                )
                if attrs.get(name)
            ),
            None,
        )
        srcset = _srcset_urls(
            base_url,
            attrs.get("srcset") or attrs.get("data-srcset"),
        )
        if not src:
            src = srcset[0] if srcset else None
        image = {
            "src": src,
            "srcset": srcset,
            "srcset_widths": _srcset_widths(attrs.get("srcset") or attrs.get("data-srcset")),
            "picture_formats": _picture_source_formats(img, base_url),
            "picture_sources": _picture_source_urls(img, base_url),
            "sizes": attrs.get("sizes"),
            "alt": attrs.get("alt"),
            "width": _number_attribute(attrs.get("width")),
            "height": _number_attribute(attrs.get("height")),
            "loading": attrs.get("loading"),
            "decoding": attrs.get("decoding"),
            "fetchpriority": attrs.get("fetchpriority"),
            "title": attrs.get("title"),
        }
        if len(images) < IMAGE_INVENTORY_LIMIT:
            images.append(image)
        if src:
            add(
                tag="img",
                url=src,
                source_attribute="src",
                attributes={key: value for key, value in image.items() if key != "src"},
                kind="image",
            )
        for candidate in srcset:
            add(
                tag="img",
                url=candidate,
                source_attribute="srcset",
                kind="image",
            )

    for tag, selector, source_attribute, forced_kind in (
        ("video", "video[src]", "src", "video"),
        ("video", "video[poster]", "poster", "image"),
        ("audio", "audio[src]", "src", "audio"),
        ("input", 'input[type="image"][src]', "src", "image"),
        ("iframe", "iframe[src]", "src", "embed"),
        ("embed", "embed[src]", "src", "embed"),
        ("object", "object[data]", "data", "embed"),
        ("script", "script[src]", "src", "script"),
        ("source", "source[src]", "src", None),
        ("track", "track[src]", "src", "track"),
    ):
        for node in tree.css(selector):
            attrs = node.attributes
            url = attrs.get(source_attribute)
            provider = video_embed_provider(url or "") if tag == "iframe" else None
            add(
                tag=tag,
                url=url,
                source_attribute=source_attribute,
                mime_type=attrs.get("type") or "",
                attributes={"provider": provider} if provider else None,
                kind="video" if provider else forced_kind,
            )

    for source in tree.css("source"):
        attrs = source.attributes
        parent_tag = source.parent.tag if source.parent is not None else ""
        source_kind = (
            "image"
            if parent_tag == "picture"
            else "video"
            if parent_tag == "video"
            else "audio"
            if parent_tag == "audio"
            else None
        )
        for candidate in _srcset_urls(
            base_url,
            attrs.get("srcset") or attrs.get("data-srcset"),
        ):
            add(
                tag="source",
                url=candidate,
                source_attribute="srcset",
                mime_type=attrs.get("type") or "",
                kind=source_kind,
            )

    for image in tree.css("image"):
        attrs = image.attributes
        add(
            tag="image",
            url=attrs.get("href") or attrs.get("xlink:href"),
            source_attribute="href",
            kind="image",
        )

    for link in tree.css("link[href]"):
        attrs = link.attributes
        rel = (attrs.get("rel") or "").lower()
        preload_kind = {
            "audio": "audio",
            "document": "document",
            "fetch": "other",
            "font": "font",
            "image": "image",
            "script": "script",
            "style": "stylesheet",
            "track": "track",
            "video": "video",
        }.get((attrs.get("as") or "").lower())
        add(
            tag="link",
            url=attrs.get("href"),
            source_attribute="href",
            rel=rel,
            mime_type=attrs.get("type") or "",
            kind=preload_kind,
        )

    for meta_node in tree.css("meta[content]"):
        attrs = meta_node.attributes
        name = (attrs.get("name") or attrs.get("property") or attrs.get("itemprop") or "").lower()
        kind = (
            "image"
            if name
            in {
                "image",
                "msapplication-tileimage",
                "og:image",
                "og:image:secure_url",
                "twitter:image",
                "twitter:image:src",
            }
            else "video"
            if name in {"og:video", "og:video:secure_url", "twitter:player"}
            else "audio"
            if name in {"og:audio", "og:audio:secure_url"}
            else None
        )
        if kind:
            add(
                tag="meta",
                url=attrs.get("content"),
                source_attribute=name,
                kind=kind,
            )

    for anchor in tree.css("a[href]"):
        href = anchor.attributes.get("href")
        resolved = _resolved_url(base_url, href)
        if resolved and _resource_kind("a", resolved, "", "") == "document":
            add(tag="a", url=href, source_attribute="href", kind="document")

    css_url_pattern = re.compile(r"url\((['\"]?)(.*?)\1\)", re.IGNORECASE)
    for node in tree.css("[style]"):
        style = node.attributes.get("style") or ""
        for match in css_url_pattern.finditer(style):
            add(
                tag=node.tag,
                url=match.group(2),
                source_attribute="style",
            )
    for style_node in tree.css("style"):
        for match in css_url_pattern.finditer(style_node.text(deep=True) or ""):
            add(
                tag="style",
                url=match.group(2),
                source_attribute="text",
            )

    return images, {
        "count": total_observed,
        "counts": counts,
        "items": items,
        "truncated": total_observed > len(items),
    }


def _append_structured_resources(
    resources: dict[str, Any],
    structured_data: dict[str, Any],
    base_url: str,
) -> None:
    """Add media URLs that exist only in structured data to the inventory."""
    items = resources.get("items")
    counts = resources.get("counts")
    if not isinstance(items, list) or not isinstance(counts, dict):
        return
    seen = {(item.get("kind"), item.get("url")) for item in items if isinstance(item, dict)}
    media_keys = {
        "associatedMedia",
        "contentUrl",
        "embedUrl",
        "image",
        "logo",
        "primaryImageOfPage",
        "thumbnail",
        "thumbnailUrl",
    }

    def add(value: Any, key: str, schema_types: list[str]) -> None:
        if isinstance(value, list):
            for item in value:
                add(item, key, schema_types)
            return
        if isinstance(value, dict):
            candidate = _image_url(value)
            if candidate:
                add(candidate, key, _types_of_schema_node(value) or schema_types)
            return
        if not isinstance(value, str):
            return
        resolved = _resolved_url(base_url, value)
        if not resolved:
            return
        kind = (
            "video"
            if key == "embedUrl" or any("Video" in schema_type for schema_type in schema_types)
            else "audio"
            if any("Audio" in schema_type for schema_type in schema_types)
            else "image"
        )
        dedupe_key = (kind, resolved)
        if dedupe_key in seen:
            return
        seen.add(dedupe_key)
        resources["count"] = int(resources.get("count") or 0) + 1
        counts[kind] = int(counts.get(kind) or 0) + 1
        if len(items) >= _RESOURCE_LIMIT:
            resources["truncated"] = True
            return
        items.append(
            {
                "kind": kind,
                "url": resolved,
                "tag": "structured-data",
                "source_attribute": key,
                "attributes": {"schema_types": schema_types},
            }
        )

    def walk(node: Any, inherited_types: list[str] | None = None) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item, inherited_types)
            return
        if not isinstance(node, dict):
            return
        node_types = _types_of_schema_node(node) or inherited_types or []
        for key, value in node.items():
            if key in media_keys:
                add(value, key, node_types)
            walk(value, node_types)

    for source in ("json_ld", "microdata", "rdfa", "microformats"):
        walk(structured_data.get(source, []))


def _types_of_schema_node(node: dict[str, Any]) -> list[str]:
    value = node.get("@type") or node.get("type")
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _image_url(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        for item in value:
            resolved = _image_url(item)
            if resolved:
                return resolved
    if isinstance(value, dict):
        for key in ("contentUrl", "url", "@id", "image", "thumbnailUrl"):
            resolved = _image_url(value.get(key))
            if resolved:
                return resolved
    return None


def _find_schema_value(node: Any, key: str) -> Any:
    if isinstance(node, dict):
        if key in node:
            return node[key]
        for value in node.values():
            found = _find_schema_value(value, key)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _find_schema_value(item, key)
            if found is not None:
                return found
    return None


def _extract_page_identity(
    tree: HTMLParser,
    base_url: str,
    *,
    og: dict[str, str],
    twitter: dict[str, str],
    structured_data: dict[str, Any],
) -> dict[str, Any]:
    meta: dict[str, str] = {}
    for node in tree.css("meta"):
        attrs = node.attributes
        name = (attrs.get("name") or attrs.get("property") or attrs.get("itemprop") or "").lower()
        content = (attrs.get("content") or "").strip()
        if name and content and name not in meta:
            meta[name] = content

    json_ld = structured_data.get("json_ld", [])
    primary_image = _image_url(_find_schema_value(json_ld, "primaryImageOfPage"))
    schema_image = _image_url(_find_schema_value(json_ld, "image"))
    image_src = None
    for node in tree.css('link[rel="image_src"]'):
        image_src = _resolved_url(base_url, node.attributes.get("href"))
        if image_src:
            break
    featured_image = None
    featured_image_source = None
    for source, candidate in (
        ("schema.primaryImageOfPage", primary_image),
        ("og:image", og.get("og:image")),
        ("twitter:image", twitter.get("twitter:image")),
        ("link:image_src", image_src),
        ("meta:image", meta.get("image")),
        ("schema.image", schema_image),
    ):
        resolved = _resolved_url(base_url, candidate)
        if resolved:
            featured_image = resolved
            featured_image_source = source
            break
    schema_types = structured_data.get("schema_types", [])
    page_types = [
        value
        for value in schema_types
        if isinstance(value, str)
        and value
        not in {
            "BreadcrumbList",
            "ContactPoint",
            "ImageObject",
            "ListItem",
            "Offer",
            "Organization",
            "Person",
            "Place",
            "PostalAddress",
            "SearchAction",
            "WebSite",
        }
    ]
    author = (
        meta.get("author") or meta.get("article:author") or _find_schema_value(json_ld, "author")
    )
    if isinstance(author, dict):
        author = author.get("name") or author.get("@id")
    if isinstance(author, list):
        author = ", ".join(
            str(item.get("name") or item.get("@id") or item)
            if isinstance(item, dict)
            else str(item)
            for item in author
        )
    body_classes = (
        (tree.body.attributes.get("class") or "").split() if tree.body is not None else []
    )
    page_id_match = next(
        (
            match
            for class_name in body_classes
            if (match := re.fullmatch(r"(?:page-id|postid)-(\d+)", class_name))
        ),
        None,
    )
    template = next(
        (
            class_name
            for class_name in body_classes
            if class_name.startswith(
                (
                    "page-template-",
                    "single-",
                    "template-",
                )
            )
        ),
        None,
    )
    links_by_rel: dict[str, list[str]] = {}
    feed_urls: list[str] = []
    for node in tree.css("link[href]"):
        href = _resolved_url(base_url, node.attributes.get("href"))
        if not href:
            continue
        rel_values = (node.attributes.get("rel") or "").lower().split()
        for rel_value in rel_values:
            links_by_rel.setdefault(rel_value, []).append(href)
        if "alternate" in rel_values and (node.attributes.get("type") or "").lower() in {
            "application/atom+xml",
            "application/feed+json",
            "application/rss+xml",
        }:
            feed_urls.append(href)
    html_lower = tree.html.lower()
    platform_signals: list[str] = []
    if "wp-content" in html_lower or "wp-includes" in html_lower:
        platform_signals.append("wordpress-assets")
    if "https://api.w.org/" in html_lower or "api.w.org" in links_by_rel:
        platform_signals.append("wordpress-rest-api")
    if "cdn.shopify.com" in html_lower:
        platform_signals.append("shopify-cdn")
    if any(name.startswith("shopify-") for name in meta):
        platform_signals.append("shopify-meta")
    detected_cms = (
        "wordpress"
        if any(signal.startswith("wordpress-") for signal in platform_signals)
        else "shopify"
        if any(signal.startswith("shopify-") for signal in platform_signals)
        else None
    )
    platform_details = {
        "wordpress_post_id": page_id_match.group(1) if page_id_match else None,
        "template": template,
        "shopify_theme_store_id": meta.get("shopify-theme-store-id"),
        # Never persist a checkout token; presence is enough to identify Shopify.
        "shopify_checkout_token_present": "shopify-checkout-api-token" in meta,
    }
    return {
        "featured_image": featured_image,
        "featured_image_source": featured_image_source,
        "cms": detected_cms,
        "generator": meta.get("generator"),
        "application_name": meta.get("application-name"),
        "site_name": og.get("og:site_name") or meta.get("application-name"),
        "author": author if isinstance(author, str) else None,
        "published_at": (
            meta.get("article:published_time")
            or meta.get("datepublished")
            or _find_schema_value(json_ld, "datePublished")
        ),
        "modified_at": (
            meta.get("article:modified_time")
            or meta.get("datemodified")
            or _find_schema_value(json_ld, "dateModified")
        ),
        "page_types": page_types,
        "theme_color": meta.get("theme-color"),
        "html_lang": (
            tree.css_first("html").attributes.get("lang")
            if tree.css_first("html") is not None
            else None
        ),
        "locale": og.get("og:locale"),
        "content_section": meta.get("article:section"),
        "shortlink": (links_by_rel.get("shortlink") or [None])[0],
        "amp_url": (links_by_rel.get("amphtml") or [None])[0],
        "manifest_url": (links_by_rel.get("manifest") or [None])[0],
        "api_urls": links_by_rel.get("https://api.w.org/", []),
        "feed_urls": feed_urls,
        "body_classes": body_classes[:100],
        "platform_signals": list(dict.fromkeys(platform_signals)),
        "platform_details": {
            key: value for key, value in platform_details.items() if value not in (None, False)
        },
    }


_FLESCH_DB_MIN = -999.99
_FLESCH_DB_MAX = 999.99


def _flesch_reading_ease(text: str, word_count: int, sentence_count: int) -> float | None:
    """Cheap Flesch reading-ease — same approximation as the extension."""
    if word_count == 0 or sentence_count == 0 or not text:
        return None
    syllables = _count_syllables(text)
    score = (
        206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllables / max(1, word_count))
    )
    score = round(score * 100) / 100
    return max(_FLESCH_DB_MIN, min(_FLESCH_DB_MAX, score))


_VOWEL_RUN = re.compile(r"[aeiouy]+")


def _count_syllables(text: str) -> int:
    count = 0
    for w in text.lower().split():
        cleaned = re.sub(r"[^a-z]", "", w)
        if not cleaned:
            continue
        runs = _VOWEL_RUN.findall(cleaned)
        count += max(1, len(runs))
    return count


# ===========================================================================
# PER-PAGE CHECKS — the ONE implementation of every per-page SEO verdict.
#
# A check turns evidence into a verdict. It NEVER parses HTML (the evidence is
# already extracted) and never touches a database, so the same function serves
# a live one-shot audit, the crawl-time pipeline, and the persisted-snapshot
# sweep in `web_crawl/analysis.py`.
#
# Every decision boundary below is a named constant declared exactly once. The
# SERP length limits are NOT redeclared here — `meta_metrics` owns them as a
# byte-identical mirror of the frontend TypeScript, and a second copy is the
# drift this consolidation exists to kill.
#
# 🚨 THIS SECTION IS MIRRORED IN TYPESCRIPT — CHANGE ONE → CHANGE BOTH IN THE
# SAME UNIT OF WORK. matrx-frontend `features/marketing/seo/audit/checks.ts` is
# the byte-identical browser twin of `PageEvidence`, `CheckOutcome`, every
# `check_*`, and `PAGE_CHECKS`, so a UI can render a verdict without a round
# trip and without re-inventing the rules in a component. Statuses, scores,
# issue counts, evidence payloads AND the reasoning strings must agree — a
# reasoning string is a user-facing expert sentence, so a difference means the
# same page gets two different explanations depending on who computed it.
# Change a rule below, then regenerate the frontend's fixture:
#
#     .venv/bin/python packages/matrx-scraper/scripts/generate_page_checks_parity_fixture.py
#
# matrx-frontend `features/marketing/seo/audit/checks.parity.test.ts` fails if
# you forget.
# ===========================================================================

# Thin content, in words of audited visible text. Screaming Frog's "low
# content" default is 200 words; we warn below 300 and fail below 100.
CONTENT_OK_WORDS = 300
CONTENT_WARN_WORDS = 200
CONTENT_FAIL_WORDS = 100

# `url_design_quality` — the deduction formula from its live catalogue row.
URL_DESIGN_MAX_LENGTH = 115
URL_DESIGN_MAX_PARAMS = 2
URL_DESIGN_LONG_PENALTY = 15
URL_DESIGN_MANY_PARAMS_PENALTY = 15
URL_DESIGN_UPPERCASE_PENALTY = 10
URL_DESIGN_UNDERSCORE_PENALTY = 10
URL_DESIGN_NON_ASCII_PENALTY = 10
URL_DESIGN_SESSION_PARAM_PENALTY = 25
URL_DESIGN_SESSION_PARAM_NAMES = frozenset(
    {"aspsessionid", "jsessionid", "phpsessid", "session", "sessionid", "sid"}
)

# Missing image alt escalates from warn to fail at either bound.
IMAGE_ALT_FAIL_RATIO = 0.5
IMAGE_ALT_FAIL_COUNT = 10

# --- Images & media --------------------------------------------------------
# Every one of these bands maps to a rule in the `web.analysis_item` row's
# `score_contract`; the row is the spec, these constants are its only home.

# Raster formats worth converting, and the modern targets to convert them to.
IMAGE_MODERN_RASTER_FORMATS = frozenset({"avif", "webp"})
IMAGE_LEGACY_RASTER_FORMATS = frozenset({"bmp", "gif", "jpg", "png", "tif"})

# Share of images that must declare width/height before the page is clean.
IMAGE_DIMENSION_ATTR_PASS_COVERAGE = 0.9
IMAGE_DIMENSION_ATTR_FAIL_COVERAGE = 0.5

# Share of convertible raster bytes... of convertible raster IMAGES — see
# `check_image_modern_format` for why this is count-weighted, not byte-weighted.
IMAGE_MODERN_FORMAT_PASS_COVERAGE = 0.9
IMAGE_MODERN_FORMAT_FAIL_COVERAGE = 0.5

# Fold geometry is NOT captured, so DOM order stands in for it: the first N
# <img> elements are treated as likely above-the-fold.
IMAGE_ABOVE_FOLD_DOM_COUNT = 3
IMAGE_BELOW_FOLD_EAGER_FAIL_RATIO = 0.5

# Oversizing, in declared-intrinsic-width / declared-display-width. A 2x ratio
# is CORRECT (retina), so the bands start above the DPR headroom.
IMAGE_OVERSIZE_MINOR_RATIO = 2.0
IMAGE_OVERSIZE_MAJOR_RATIO = 4.0
IMAGE_OVERSIZE_SEVERE_RATIO = 8.0
IMAGE_OVERSIZE_WARN_BYTES = 300 * 1024
IMAGE_OVERSIZE_FAIL_BYTES = 1024 * 1024

# Broken images: the row's own band — 3+ is a page that looks abandoned.
BROKEN_IMAGE_FAIL_COUNT = 3

# Redirects: hops BEYOND the first are the waste. >2 entries in the chain
# means the crawler followed more than one hop to land.
REDIRECT_CHAIN_MAX_HOPS = 2

# Weight ceiling for the HTML DOCUMENT — the only transfer size the crawl
# measures. Subresource bytes (images, scripts, fonts) are NOT fetched, so
# there is no total-page-weight number here and the catalogue row says so.
LARGE_PAGE_BYTES = 5_000_000

# TTFB bands, straight from the `ttfb_server_response` row's score_contract and
# from Google's server-response-time audit: at or under 800 ms is good, over
# 1800 ms is poor. These grade TRUE time-to-first-byte (`PageEvidence.ttfb_ms`),
# never total response time — a fast server behind a slow download must not be
# scored as slow, and the reverse is worse.
TTFB_GOOD_MS = 800
TTFB_POOR_MS = 1800

# --- Mobile rendering, language, social ------------------------------------
# Every band below maps to a rule in the matching `web.analysis_item` row's
# `score_contract`; the row is the spec, these constants are its only home.

# Viewport zoom lockout. A `maximum-scale` at or below this pins the page at
# its initial scale — the same WCAG 1.4.4 failure `user-scalable=no` causes.
VIEWPORT_ZOOM_LOCK_MAX_SCALE = 1.0
# Values of `user-scalable` that disable pinch-zoom.
VIEWPORT_ZOOM_DISABLED_VALUES = frozenset({"no", "0", "false"})

# Formats the social-share crawlers actually render. Anything else (svg, bmp,
# ico, tiff) is fetched and then dropped, so the share renders imageless.
OG_IMAGE_SUPPORTED_EXTENSIONS = frozenset({"jpg", "jpeg", "png", "gif", "webp"})

# The Open Graph tags a rich share preview requires, per the catalogue row.
SOCIAL_REQUIRED_OG_TAGS = ("og:title", "og:description", "og:image", "og:url", "og:type")
# Deductions from the tag-coverage score — the catalogue row's formula, verbatim.
SOCIAL_OG_URL_CONFLICT_PENALTY = 20
SOCIAL_NO_TWITTER_CARD_PENALTY = 10
# Score bands the coverage formula maps to a status. Only a complete card
# passes: every deduction is a share that renders worse than it could.
SOCIAL_META_PASS_SCORE = 100
SOCIAL_META_WARN_SCORE = 60

# A meta refresh at or below this delay is an outright HTTP-redirect
# substitute; above it the page is an interstitial the user actually sees.
META_REFRESH_INSTANT_MAX_SECONDS = 0

# --- Security --------------------------------------------------------------
# The bands below are the `security` catalogue rows' `score_contract`, verbatim.

# Response headers persisted as security evidence. An ALLOWLIST, never the whole
# header set: a snapshot must not carry `set-cookie` or any credential echo, and
# a check needs only these. `security_response_headers()` is the one filter, and
# `web.snapshot.extracted.response_headers` is the one place they land.
SECURITY_RESPONSE_HEADERS: frozenset[str] = frozenset(
    {
        "strict-transport-security",
        "content-security-policy",
        "content-security-policy-report-only",
        "x-content-type-options",
        "x-frame-options",
        "referrer-policy",
        "permissions-policy",
        "cross-origin-opener-policy",
        "cross-origin-resource-policy",
    }
)

# HTTP-variant probe verdicts for `https_enforcement`. A permanent redirect is
# the only answer that consolidates the duplicate; a temporary one leaves both
# URLs indexable and tells crawlers the HTTP address is still real.
HTTP_VARIANT_PERMANENT_REDIRECTS = frozenset({301, 308})

# --- Outline, depth, and error-page detection ------------------------------
# Every band below is a rule in the matching `web.analysis_item` row's
# `score_contract`; the row is the spec, these constants are its only home.

# `heading_hierarchy` — a "skip" is a jump of more than one level between two
# consecutive headings (h2 → h4). More than this many skips, or more than this
# share of headings with no text, is the fail band.
HEADING_SKIP_FAIL_COUNT = 3
HEADING_EMPTY_FAIL_RATIO = 0.3

# `text_html_ratio` — extracted visible-text bytes / raw HTML bytes.
TEXT_HTML_RATIO_FAIL = 0.03
TEXT_HTML_RATIO_WARN = 0.10

# `content_depth` — per-TYPE word expectations, the analytics counterpart to
# `thin_content`'s absolute floor. Only evaluated when the page declares a type
# (schema.org @type or og:type); an unknown type is `n_a`, never a second
# thin-content verdict.
CONTENT_DEPTH_ARTICLE_MIN_WORDS = 500
CONTENT_DEPTH_ARTICLE_TARGET_WORDS = 900
CONTENT_DEPTH_COMMERCE_MIN_WORDS = 100
#: schema.org @type values (lowercased) that carry a long-form expectation.
CONTENT_DEPTH_ARTICLE_SCHEMA_TYPES = frozenset(
    {
        "article",
        "advertisercontentarticle",
        "blogposting",
        "liveblogposting",
        "newsarticle",
        "report",
        "scholarlyarticle",
        "socialmediaposting",
        "techarticle",
    }
)
#: Commerce/listing types — a short page is normal, an EMPTY one is not.
CONTENT_DEPTH_COMMERCE_SCHEMA_TYPES = frozenset(
    {
        "collectionpage",
        "individualproduct",
        "itemlist",
        "offercatalog",
        "product",
        "productgroup",
        "productmodel",
    }
)
#: Types with no content expectation at all — exempt, per the catalogue row.
CONTENT_DEPTH_UTILITY_SCHEMA_TYPES = frozenset(
    {
        "aboutpage",
        "checkoutpage",
        "contactpage",
        "profilepage",
        "searchresultspage",
    }
)

# `soft_404_detection` — a 200 that serves error content. Both word bounds are
# read together with the not-found phrasing below.
SOFT_404_PHRASE_MAX_WORDS = 50
SOFT_404_EMPTY_MAX_WORDS = 30
#: Not-found phrasing in a TITLE. Deliberately narrow — an article titled
#: "What to do when a page is missing" must not be called a soft 404.
SOFT_404_TITLE_PATTERN = re.compile(
    r"\b(404|page not found|not found|no longer (?:exists|available)|"
    r"page (?:does not|doesn'?t) exist|page unavailable|error 404)\b",
    re.IGNORECASE,
)

# `temporary_redirect_usage` — statuses that should have been 301/308.
TEMPORARY_REDIRECT_STATUSES = frozenset({302, 307})

# How many offending URLs a check attaches as evidence.
CHECK_EVIDENCE_SAMPLE_LIMIT = 5


def security_response_headers(headers: Mapping[str, str] | None) -> dict[str, str]:
    """Lower-cased security headers worth persisting, and nothing else.

    Returns ``{}`` for "no headers to keep" — which is indistinguishable from
    "the fetch captured nothing". Callers that persist evidence therefore store
    ``None``/absent when they never had headers at all, so the checks can tell
    a site with no security headers apart from a snapshot that never saw any.
    """
    if not headers:
        return {}
    kept: dict[str, str] = {}
    for name, value in headers.items():
        key = str(name).strip().lower()
        if key in SECURITY_RESPONSE_HEADERS and value is not None:
            kept[key] = str(value).strip()
    return kept


@dataclass(frozen=True)
class LabPerformance:
    """One PageSpeed Insights observation, reduced to what the checks score.

    Built ONLY by `lab_performance_from_lighthouse` from a persisted
    `seo.page_performance.lighthouse` payload — there is no second reader of
    that shape (a persisted shape has ONE deserializer; see the root
    `CLAUDE.md`). Every field is `None` when PageSpeed did not report it, and
    every check must answer `n_a` for a `None`.
    """

    strategy: str
    observed_at: datetime | None = None
    lcp_ms: float | None = None
    tbt_ms: float | None = None
    cls: float | None = None
    #: Estimated total savings across the delivery fix-list, milliseconds.
    delivery_savings_ms: float | None = None
    #: Per-audit `{name: savings_ms}` — the offender list behind that total.
    delivery_audits: dict[str, float] = field(default_factory=dict)
    #: Total transferred bytes of cacheable static assets. `None` = PageSpeed
    #: reported no request table, which is different from "no static assets".
    cache_static_bytes: float | None = None
    #: `[{"url", "cache_lifetime_ms", "total_bytes"}]` for assets PageSpeed
    #: flagged as under-cached. Empty with a non-None `cache_static_bytes`
    #: means every static asset is cached well.
    cache_short_ttl_resources: list[dict[str, Any]] = field(default_factory=list)


def _lab_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def _lab_metric(metrics: dict[str, Any], name: str) -> float | None:
    entry = metrics.get(name)
    return _lab_number(entry.get("numeric_value")) if isinstance(entry, dict) else None


def lab_performance_from_lighthouse(
    payload: dict[str, Any] | None,
    *,
    strategy: str,
    observed_at: datetime | None = None,
) -> LabPerformance:
    """The ONE deserializer for a persisted `seo.page_performance.lighthouse`.

    Tolerant by construction: a payload written before the delivery projection
    existed (`matrx_seo.providers.pagespeed::_delivery_facts`, added 2026-08-09)
    simply yields `None` for the delivery/cache fields, so those checks answer
    `n_a` on old rows instead of scoring a fabricated zero.
    """
    body = payload if isinstance(payload, dict) else {}
    metrics = body.get("metrics") if isinstance(body.get("metrics"), dict) else {}
    delivery = body.get("delivery") if isinstance(body.get("delivery"), dict) else {}
    cache = delivery.get("cache") if isinstance(delivery.get("cache"), dict) else {}
    audits = delivery.get("audits") if isinstance(delivery.get("audits"), dict) else {}

    delivery_audits: dict[str, float] = {}
    for name, entry in audits.items():
        savings = _lab_number(entry.get("savings_ms")) if isinstance(entry, dict) else None
        if savings is not None:
            delivery_audits[str(name)] = savings
    short_ttl = cache.get("short_ttl_resources")
    return LabPerformance(
        strategy=strategy,
        observed_at=observed_at,
        lcp_ms=_lab_metric(metrics, "lcp_ms"),
        tbt_ms=_lab_metric(metrics, "tbt_ms"),
        cls=_lab_metric(metrics, "cls"),
        delivery_savings_ms=(
            _lab_number(delivery.get("total_savings_ms")) if delivery_audits else None
        ),
        delivery_audits=delivery_audits,
        cache_static_bytes=(
            _lab_number(cache.get("static_bytes")) if cache.get("measured") else None
        ),
        cache_short_ttl_resources=[r for r in short_ttl if isinstance(r, dict)]
        if isinstance(short_ttl, list)
        else [],
    )


@dataclass
class PageEvidence:
    """Everything a per-page check needs, from ANY source.

    Built from a live `SeoAuditResult` (`evidence_from_audit`) or from a
    persisted snapshot row (`web_crawl/analysis.py::PageFacts`, which extends
    this). A `None` field means "not captured" — every check must answer
    ``n_a`` for it, NEVER a silent pass.
    """

    url: str
    title: str | None = None
    title_metrics: dict[str, Any] = field(default_factory=dict)
    description: str | None = None
    description_metrics: dict[str, Any] = field(default_factory=dict)
    meta_robots: str | None = None
    canonical_url: str | None = None
    canonical_matches: bool | None = None
    noindex: bool | None = None
    nofollow: bool | None = None
    h1_count: int | None = None
    # Every heading in document order as [{"level": 1-6, "text": str}] —
    # `web.snapshot.headings.all`. `None` = never captured (the outline checks
    # answer n_a); `[]` = captured, and the page genuinely has no headings.
    headings: list[dict[str, Any]] | None = None
    word_count: int | None = None
    # UTF-8 bytes of the visible text `word_count` counts. Paired with
    # `response_bytes` by `check_text_html_ratio`; `None` on snapshots captured
    # before the field existed.
    text_bytes: int | None = None
    # schema.org @type values declared by the page. `None` = never captured;
    # `[]` = captured, page declares none.
    schema_types: list[str] | None = None
    image_count: int | None = None
    images_missing_alt: int | None = None
    # Per-<img> inventory in DOM order — `web.snapshot.images.items`, capped at
    # IMAGE_INVENTORY_LIMIT while `image_count` stays the true total. Empty with
    # a non-zero `image_count` means the snapshot predates the inventory, which
    # every image check must answer `n_a` for.
    image_items: list[dict[str, Any]] = field(default_factory=list)
    http_status: int | None = None
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)
    mixed_content: list[str] = field(default_factory=list)
    # Security-relevant response headers, lower-cased (`security_response_headers`).
    # `None` = the capture never recorded headers; `{}` = it did and the server
    # sent none of them. The site-wide header checks live in
    # `web_crawl/analysis.py` (they sample many pages); this field is what they
    # sample, and it is carried here so ONE struct describes a captured page.
    response_headers: dict[str, str] | None = None
    # Result of probing this URL's http:// variant — {"status": int,
    # "location": str | None}. `None` = never probed (the catalogue row's own
    # declared capture gap), which `check_https_enforcement` answers `n_a` for.
    http_variant_probe: dict[str, Any] | None = None
    # Transfer size of the HTML DOCUMENT only — subresources are never fetched,
    # so this is NOT total page weight (see `check_page_weight`).
    response_bytes: int | None = None
    # Total elapsed time of the fetch: server think time PLUS the body
    # download. Recorded for the record; NOT what the TTFB check grades.
    response_time_ms: int | None = None
    # TRUE time to first byte, in ms, measured by the transport (curl's
    # STARTTRANSFER_TIME_T / httpx streamed headers), redirect hops included.
    # `None` = never measured — snapshots captured before 2026-08-09, and
    # anything fetched through the browser transport. `check_ttfb_server_response`
    # answers `n_a` for those; it must NEVER fall back to `response_time_ms`,
    # which measures a different thing.
    ttfb_ms: int | None = None
    # {"prev": url, "next": url} from rel=prev/next link tags. Empty = the page
    # declares no pagination, which is NOT a defect (see check_pagination_markup).
    pagination: dict[str, Any] = field(default_factory=dict)
    # hreflang annotations as [{"lang": ..., "href": ...}] — exactly the shape
    # `HreflangItem.to_dict` / `HreflangEntry` persist into snapshot head_tags.
    hreflang: list[dict[str, Any]] = field(default_factory=list)
    # The COMPLETE structured-data payload — `structured_data.py::
    # StructuredDataExtraction.to_dict()`: parsed JSON-LD, the ORIGINAL script
    # strings (malformed ones included), their parse errors, normalized blocks,
    # microdata, RDFa, microformats. Empty dict = never captured (n_a), which is
    # a different fact from "captured, and the page has no markup".
    structured_data: dict[str, Any] = field(default_factory=dict)
    # True once an HTML <head> was actually parsed for this page. A URL the
    # crawler attempted but never snapshotted (a 404, a timeout, a redirect
    # loop) has NO head evidence, and `lang`/`og`/`twitter` being empty there
    # says nothing about the page — so every head check answers n_a instead of
    # reporting a tag as missing on markup nobody ever read.
    head_captured: bool = False
    # `<html lang>` verbatim; empty when the page declares none.
    lang: str | None = None
    # Raw social tag bags, keys exactly as authored ("og:title", "twitter:card").
    og: dict[str, str] = field(default_factory=dict)
    twitter: dict[str, str] = field(default_factory=dict)
    # {"viewport": str | None, "refresh": str | None} — the two head metas that
    # are neither SEO text nor transport. `None` = the snapshot predates this
    # capture, so its checks answer n_a instead of inventing a missing-tag fail.
    head_meta: dict[str, Any] | None = None
    # Lab performance from the ONE PageSpeed store, `seo.page_performance`
    # (written by matrx-seo, read by `web_crawl/analysis.py::_load_lab_performance`).
    # `None` = PageSpeed has never run for this page, which every Core Web
    # Vitals check answers `n_a` + `COLLECT_PAGESPEED` for — NEVER a pass. A
    # crawl cannot produce these numbers: they need a real browser render.
    lab_performance: LabPerformance | None = None


@dataclass(frozen=True)
class Remediation:
    """The ONE-CLICK FIX for a check the platform could not run yet.

    🚨 A check that answers ``n_a`` because EVIDENCE IS MISSING must attach one
    of these. It may NEVER tell the user to run something in prose — the reader
    is a non-technical subject-matter expert for whom "run the link check
    command" is a dead end (NO DEAD ENDS doctrine:
    ``common-docs/policies/no-dead-ends.md``). The sentence carries the
    meaning; this binding carries the action.

    ``command`` names a crawler command the platform ALREADY performs, and
    every value must appear in ``REMEDIATION_COMMANDS``. Nothing here may name
    an action that does not already exist — a binding the UI cannot dispatch is
    the same dead end wearing a button.

    Consumed by matrx-frontend's ``crawler/remediation.ts``, which maps
    ``command`` to the existing `direct-client` call for the matching
    `/crawler/sites/{site_id}/…` endpoint.
    """

    #: Existing crawler command key (see ``REMEDIATION_COMMANDS``).
    command: str
    #: "site" (one command covers the whole site) | "page" (this page only).
    scope: str
    #: The button's verb, in the user's language.
    label: str
    #: What will happen, stated BEFORE it happens (the assists intentional-action law).
    explainer: str


#: Every command a remediation may name → the crawler endpoint that performs it.
#: The endpoint column is documentation for humans; the FE owns the dispatch.
REMEDIATION_COMMANDS: dict[str, str] = {
    "links_check": "POST /crawler/sites/{site_id}/links/check",
    "page_fetch": "POST /crawler/sites/{site_id}/pages/fetch",
    "site_recrawl": "POST /crawler/sites/{site_id}/rescrape",
    "sitemaps_sync": "POST /crawler/sites/{site_id}/sitemaps/sync",
    "pagespeed_collect": "POST /seo/pages/{page_id}/pagespeed/sync",
    "gsc_sync": "POST /crawler/sites/{site_id}/gsc/sync",
}

SYNC_GSC = Remediation(
    command="gsc_sync",
    scope="site",
    label="Pull this site's Google data",
    explainer=(
        "We ask Google Search Console for the clicks, impressions and average "
        "positions it recorded for this site, and store them so the search "
        "checks can read real numbers instead of guessing. It reads only; "
        "nothing on your website or in Google changes."
    ),
)

CHECK_SITE_LINKS = Remediation(
    command="links_check",
    scope="site",
    label="Check this site's links",
    explainer=(
        "We follow every link on the site once and record which ones are broken "
        "or bounce through a redirect. It runs across the whole site, so it only "
        "needs doing once after each crawl."
    ),
)

RECAPTURE_PAGE = Remediation(
    command="page_fetch",
    scope="page",
    label="Capture this page again",
    explainer=(
        "We fetch a fresh copy of this one page right now and measure it. It "
        "takes a few seconds and changes nothing on your website."
    ),
)

COLLECT_PAGESPEED = Remediation(
    command="pagespeed_collect",
    scope="page",
    label="Measure this page's speed",
    explainer=(
        "We load this one page in a real phone-sized browser and time it — how "
        "fast the main content appears, how long it stays unresponsive, and how "
        "much the layout jumps. It takes under a minute and changes nothing on "
        "your website."
    ),
)

RECRAWL_SITE = Remediation(
    command="site_recrawl",
    scope="site",
    label="Crawl this site again",
    explainer=(
        "We walk the whole site from the homepage, re-reading every page and "
        "the links between them. This is the slow one — it can take a while on "
        "a large site — but it is what rebuilds the site-wide picture."
    ),
)

SYNC_SITEMAPS = Remediation(
    command="sitemaps_sync",
    scope="site",
    label="Read this site's sitemap",
    explainer=(
        "We find and read the sitemap files your website publishes — the list "
        "of pages it asks search engines to index — and compare them with the "
        "pages we actually found. It takes seconds and changes nothing on your "
        "website."
    ),
)


@dataclass
class CheckOutcome:
    """A verdict. `score` is 1-100 for pass/warn/fail and None otherwise —
    the shape `web.analysis_result`'s status/score constraint requires."""

    status: str  # pass | warn | fail | n_a
    score: int | None
    reasoning: str
    issue_count: int = 0
    evidence: dict[str, Any] | None = None
    #: Set whenever the verdict is blocked on evidence the platform can go get.
    remediation: Remediation | None = None


def clamp_score(value: int) -> int:
    return max(1, min(100, value))


def sample_urls(urls: list[str]) -> list[str]:
    return urls[:CHECK_EVIDENCE_SAMPLE_LIMIT]


def registrable_host(url: str) -> str:
    host = urlsplit(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def evidence_from_audit(
    audit: SeoAuditResult,
    *,
    http_status: int | None = None,
    redirect_chain: list[dict[str, Any]] | None = None,
    final_url: str | None = None,
    response_bytes: int | None = None,
    response_time_ms: int | None = None,
    ttfb_ms: int | None = None,
) -> PageEvidence:
    """Turn a live `audit_html` result into checkable evidence.

    Transport facts (status, redirects, weight, latency) are not in the HTML,
    so the caller supplies them. Length metrics and the indexability verdict
    are computed by their canonical owners (`meta_metrics`, `audit_metrics`) —
    never re-derived here.
    """
    title = audit.title.strip() if audit.title and audit.title.strip() else None
    description = (
        audit.meta_description.strip()
        if audit.meta_description and audit.meta_description.strip()
        else None
    )
    indexability = evaluate_indexability(
        http_status,
        audit.robots,
        audit.canonical,
        redirect_chain or [],
        final_url or audit.url,
    )
    return PageEvidence(
        url=audit.url,
        title=title,
        title_metrics=calculate_meta_title_metrics(title) if title else {},
        description=description,
        description_metrics=(
            calculate_meta_description_metrics(description) if description else {}
        ),
        meta_robots=audit.robots,
        canonical_url=audit.canonical,
        canonical_matches=indexability["canonical_matches"],
        noindex=indexability["noindex"],
        nofollow=indexability["nofollow"],
        h1_count=audit.h1_count,
        headings=[h.to_dict() for h in audit.headings],
        word_count=audit.word_count,
        text_bytes=audit.text_bytes,
        schema_types=list(audit.schema_types),
        image_count=audit.images_total,
        images_missing_alt=audit.images_missing_alt,
        image_items=list(audit.image_inventory),
        http_status=http_status,
        redirect_chain=list(redirect_chain or []),
        mixed_content=list(audit.mixed_content),
        response_bytes=response_bytes,
        response_time_ms=response_time_ms,
        ttfb_ms=ttfb_ms,
        pagination=dict(audit.pagination or {}),
        head_captured=True,
        lang=audit.lang.strip() if audit.lang and audit.lang.strip() else None,
        og=dict(audit.og or {}),
        twitter=dict(audit.twitter or {}),
        head_meta={"viewport": audit.viewport, "refresh": audit.meta_refresh},
        hreflang=[item.to_dict() for item in audit.hreflang],
        structured_data=dict(audit.structured_data or {}),
    )


# --- Title -----------------------------------------------------------------


def check_url_design_quality(ev: PageEvidence) -> CheckOutcome:
    """Grade only URL facts named by the live catalogue deduction formula."""
    parts = urlsplit(ev.url)
    params = parse_qsl(parts.query, keep_blank_values=True)
    designed_part = f"{parts.path}?{parts.query}" if parts.query else parts.path
    normalized_param_names = {re.sub(r"[^a-z0-9]", "", name.lower()) for name, _value in params}
    problems: list[str] = []
    penalty = 0
    if len(ev.url) > URL_DESIGN_MAX_LENGTH:
        penalty += URL_DESIGN_LONG_PENALTY
        problems.append(f"longer than {URL_DESIGN_MAX_LENGTH} characters")
    if len(params) > URL_DESIGN_MAX_PARAMS:
        penalty += URL_DESIGN_MANY_PARAMS_PENALTY
        problems.append(f"has {len(params)} query parameters")
    if any(character.isupper() for character in designed_part):
        penalty += URL_DESIGN_UPPERCASE_PENALTY
        problems.append("contains uppercase letters")
    if "_" in designed_part:
        penalty += URL_DESIGN_UNDERSCORE_PENALTY
        problems.append("contains underscores")
    if any(ord(character) > 127 for character in ev.url):
        penalty += URL_DESIGN_NON_ASCII_PENALTY
        problems.append("contains non-ASCII characters")
    session_params = sorted(normalized_param_names & URL_DESIGN_SESSION_PARAM_NAMES)
    if session_params:
        penalty += URL_DESIGN_SESSION_PARAM_PENALTY
        problems.append(f"contains a session identifier ({', '.join(session_params)})")

    score = max(1, 100 - penalty)
    evidence = {
        "url_length": len(ev.url),
        "parameter_count": len(params),
        "has_uppercase": any(character.isupper() for character in designed_part),
        "has_underscores": "_" in designed_part,
        "has_non_ascii": any(ord(character) > 127 for character in ev.url),
        "session_params": session_params,
    }
    if not problems:
        return CheckOutcome(
            "pass",
            100,
            "This URL is short, readable, and free of tracking-state clutter.",
            evidence=evidence,
        )
    return CheckOutcome(
        "warn",
        score,
        f"This URL {'; '.join(problems)} — simpler, stable URLs are easier for people "
        "and search engines to understand.",
        issue_count=len(problems),
        evidence=evidence,
    )


def check_title_presence(ev: PageEvidence) -> CheckOutcome:
    if ev.title:
        return CheckOutcome("pass", 100, f'Title present: "{ev.title[:120]}".')
    return CheckOutcome(
        "fail",
        5,
        "This page has no <title> tag (or it is empty) — search engines will "
        "synthesize one, and the SERP headline is out of your control.",
        issue_count=1,
    )


def check_title_length(ev: PageEvidence) -> CheckOutcome:
    metrics = ev.title_metrics
    if not ev.title:
        return CheckOutcome(
            "n_a", None, "This page has no title yet, so there is nothing to measure."
        )
    if not metrics:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't measured this page's title yet.",
            remediation=RECAPTURE_PAGE,
        )
    issues = [str(i) for i in metrics.get("issues") or []]
    chars = metrics.get("character_count")
    pixels = metrics.get("pixel_width")
    detail = f"{chars} chars, {pixels}px" if chars is not None else "measured at capture"
    if metrics.get("ok") or metrics.get("title_ok"):
        return CheckOutcome("pass", 100, f"Title length is within limits ({detail}).")
    flags_bad = sum(
        1
        for ok in (
            metrics.get("seo_length_ok"),
            metrics.get("desktop_ok"),
            metrics.get("mobile_ok"),
        )
        if ok is False
    )
    score = 60 if flags_bad <= 1 else 35
    reason = (
        f"Title length problem ({detail}): " + "; ".join(issues)
        if issues
        else (
            f"Title is outside the recommended window ({detail}; aim for "
            f"{TITLE_SEO_MIN_CHARS}-{TITLE_SEO_MAX_CHARS} chars) and may truncate in SERPs."
        )
    )
    return CheckOutcome("warn", score, reason, issue_count=max(1, len(issues)))


# --- Meta description ------------------------------------------------------


def check_meta_description_presence(ev: PageEvidence) -> CheckOutcome:
    if ev.description:
        return CheckOutcome("pass", 100, "Meta description present.")
    return CheckOutcome(
        "fail",
        25,
        "No meta description — Google will scrape arbitrary body text for the "
        "snippet, and CTR suffers.",
        issue_count=1,
    )


def check_meta_description_length(ev: PageEvidence) -> CheckOutcome:
    metrics = ev.description_metrics
    if not ev.description:
        return CheckOutcome(
            "n_a",
            None,
            "This page has no meta description yet, so there is nothing to measure.",
        )
    if not metrics:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't measured this page's meta description yet.",
            remediation=RECAPTURE_PAGE,
        )
    issues = [str(i) for i in metrics.get("issues") or []]
    chars = metrics.get("character_count")
    pixels = metrics.get("pixel_width")
    detail = f"{chars} chars, {pixels}px" if chars is not None else "measured at capture"
    if metrics.get("ok") or metrics.get("description_ok"):
        return CheckOutcome("pass", 100, f"Meta description length is within limits ({detail}).")
    flags_bad = sum(
        1
        for ok in (
            metrics.get("seo_length_ok"),
            metrics.get("desktop_ok"),
            metrics.get("mobile_ok"),
        )
        if ok is False
    )
    score = 60 if flags_bad <= 1 else 40
    reason = (
        f"Meta description length problem ({detail}): " + "; ".join(issues)
        if issues
        else (
            f"Meta description is outside the recommended window ({detail}; aim for "
            f"{DESCRIPTION_SEO_MIN_CHARS}-{DESCRIPTION_SEO_MAX_CHARS} chars)."
        )
    )
    return CheckOutcome("warn", score, reason, issue_count=max(1, len(issues)))


# --- Structure -------------------------------------------------------------


def check_h1_presence(ev: PageEvidence) -> CheckOutcome:
    if ev.h1_count is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded this page's headings yet.",
            remediation=RECAPTURE_PAGE,
        )
    if ev.h1_count == 1:
        return CheckOutcome("pass", 100, "Exactly one H1.")
    if ev.h1_count == 0:
        return CheckOutcome(
            "fail",
            20,
            "No H1 on the page — the primary on-page topic signal is missing.",
            issue_count=1,
        )
    return CheckOutcome(
        "warn",
        50,
        f"{ev.h1_count} H1 tags — multiple H1s dilute the primary topic signal; keep one.",
        issue_count=ev.h1_count - 1,
    )


def check_heading_hierarchy(ev: PageEvidence) -> CheckOutcome:
    """The document outline: skipped levels and empty headings.

    A "skip" is a jump of more than one level between two CONSECUTIVE headings
    (h2 → h4). The first heading is never a skip — a page whose outline starts
    at h2 has a missing H1, which is `check_h1_presence`'s verdict, not this
    one's; counting it twice would double-charge the same defect.
    """
    headings = ev.headings
    if headings is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded this page's headings yet.",
            remediation=RECAPTURE_PAGE,
        )

    levels: list[int] = []
    empty = 0
    for item in headings:
        level = item.get("level")
        if not isinstance(level, int) or not 1 <= level <= 6:
            continue
        levels.append(level)
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            empty += 1

    if not levels:
        words = ev.word_count
        if words is None:
            return CheckOutcome(
                "n_a",
                None,
                "This page has no headings, and we haven't counted its words yet — "
                "we can't tell whether that's a problem.",
                remediation=RECAPTURE_PAGE,
            )
        if words > CONTENT_OK_WORDS:
            return CheckOutcome(
                "warn",
                55,
                f"{words} words of text and not a single heading — readers and search "
                "engines both navigate by headings, and this page gives them none.",
                issue_count=1,
            )
        return CheckOutcome(
            "pass", 100, "No headings, but too little content on the page to need them."
        )

    skips = [
        (previous, current)
        for previous, current in zip(levels, levels[1:], strict=False)
        if current > previous + 1
    ]
    empty_ratio = empty / len(levels)
    detail = (
        f"{len(skips)} skipped heading level(s)" if skips else f"{empty} heading(s) with no text"
    )
    evidence = {
        "heading_levels": levels[:CHECK_EVIDENCE_SAMPLE_LIMIT],
        "skipped_levels": [f"h{a}->h{b}" for a, b in skips][:CHECK_EVIDENCE_SAMPLE_LIMIT],
        "empty_headings": empty,
        "heading_count": len(levels),
    }
    if len(skips) > HEADING_SKIP_FAIL_COUNT or empty_ratio > HEADING_EMPTY_FAIL_RATIO:
        # The row's severity_map puts a 45 in the "low" band — a real defect to
        # fix, not a page-breaking one, so it warns rather than fails.
        return CheckOutcome(
            "warn",
            45,
            f"The heading outline is broken ({detail} across {len(levels)} headings) — "
            "the page reads as a pile of styled text rather than a structured document.",
            issue_count=len(skips) + empty,
            evidence=evidence,
        )
    if skips or empty:
        return CheckOutcome(
            "warn",
            70,
            f"The heading outline has gaps ({detail}) — headings should step down one "
            "level at a time and always carry text.",
            issue_count=len(skips) + empty,
            evidence=evidence,
        )
    return CheckOutcome("pass", 100, f"Clean heading outline across {len(levels)} headings.")


def check_thin_content(ev: PageEvidence) -> CheckOutcome:
    words = ev.word_count
    if words is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't counted the words on this page yet.",
            remediation=RECAPTURE_PAGE,
        )
    if words >= CONTENT_OK_WORDS:
        return CheckOutcome("pass", 100, f"{words} words of visible text.")
    if words >= CONTENT_WARN_WORDS:
        return CheckOutcome(
            "warn",
            60,
            f"Only {words} words of visible text (below {CONTENT_OK_WORDS}) — "
            "thin pages struggle to rank for anything competitive.",
            issue_count=1,
        )
    if words >= CONTENT_FAIL_WORDS:
        return CheckOutcome(
            "warn",
            40,
            f"Only {words} words of visible text — this is thin content by any "
            f"industry bar (Screaming Frog flags under {CONTENT_WARN_WORDS}).",
            issue_count=1,
        )
    return CheckOutcome(
        "fail",
        15,
        f"Only {words} words of visible text — effectively an empty page to a search engine.",
        issue_count=1,
    )


def declared_page_type(ev: PageEvidence) -> str | None:
    """The page's own claim about what kind of page it is.

    Read from schema.org ``@type`` first, then ``og:type`` — both are the
    PAGE's declaration, never our guess. Returns "article" | "commerce" |
    "utility", or ``None`` when the page declares nothing we recognize (which
    is a genuine "we don't know", not a default).
    """
    declared: list[str] = []
    if ev.schema_types is not None:
        declared.extend(t.lower().strip() for t in ev.schema_types if isinstance(t, str))
    if ev.og is not None:
        og_type = ev.og.get("og:type")
        if isinstance(og_type, str) and og_type.strip():
            declared.append(og_type.lower().strip())
    if any(t in CONTENT_DEPTH_ARTICLE_SCHEMA_TYPES for t in declared):
        return "article"
    if any(t in CONTENT_DEPTH_COMMERCE_SCHEMA_TYPES for t in declared):
        return "commerce"
    if any(t in CONTENT_DEPTH_UTILITY_SCHEMA_TYPES for t in declared):
        return "utility"
    return None


def check_content_depth(ev: PageEvidence) -> CheckOutcome:
    """Content volume measured against the page's OWN declared type.

    Deliberately NOT a second thin-content verdict. `check_thin_content` asks
    an absolute question ("is there enough here for any query at all?") with a
    fixed floor. This asks a relative one ("is there enough here for THIS kind
    of page?") — a 400-word article is a shallow article and a perfectly normal
    product page. When the page declares no type there is no expectation to
    measure against, so this answers `n_a` rather than restating the floor.
    """
    words = ev.word_count
    if words is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't counted the words on this page yet.",
            remediation=RECAPTURE_PAGE,
        )
    if ev.schema_types is None and ev.og is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded what kind of page this is, so there's no "
            "expectation to measure its length against.",
            remediation=RECAPTURE_PAGE,
        )
    page_type = declared_page_type(ev)
    if page_type is None:
        return CheckOutcome(
            "n_a",
            None,
            "This page doesn't say what kind of page it is (no schema.org type, no "
            "og:type), so there is no per-type length expectation to hold it to. "
            "Its raw length is covered by the thin-content check.",
        )
    evidence = {"page_type": page_type, "word_count": words}
    if page_type == "utility":
        return CheckOutcome(
            "pass",
            100,
            f"This is a {page_type} page — length is not what makes it good.",
            evidence=evidence,
        )
    if page_type == "article":
        if words < CONTENT_DEPTH_ARTICLE_MIN_WORDS:
            return CheckOutcome(
                "warn",
                55,
                f"This page presents itself as an article but runs only {words} words "
                f"(articles that compete usually clear {CONTENT_DEPTH_ARTICLE_MIN_WORDS}).",
                issue_count=1,
                evidence=evidence,
            )
        if words < CONTENT_DEPTH_ARTICLE_TARGET_WORDS:
            # A PASS carrying an 80: worth knowing on a competitive topic, not a
            # defect — the row's severity_map calls this band "info".
            return CheckOutcome(
                "pass",
                80,
                f"{words} words — a solid article, still short of the "
                f"{CONTENT_DEPTH_ARTICLE_TARGET_WORDS} words the best-performing pages "
                "on a competitive topic tend to carry.",
                issue_count=1,
                evidence=evidence,
            )
        return CheckOutcome(
            "pass", 100, f"{words} words — full depth for an article.", evidence=evidence
        )
    if words < CONTENT_DEPTH_COMMERCE_MIN_WORDS:
        return CheckOutcome(
            "warn",
            60,
            f"Only {words} words of unique copy on a product/listing page — there is "
            "nothing here for a search engine to match a buyer's question against.",
            issue_count=1,
            evidence=evidence,
        )
    return CheckOutcome(
        "pass",
        100,
        f"{words} words — enough unique copy for a product/listing page.",
        evidence=evidence,
    )


def check_text_html_ratio(ev: PageEvidence) -> CheckOutcome:
    """Visible-text bytes as a share of the HTML the server sent."""
    text_bytes = ev.text_bytes
    html_bytes = ev.response_bytes
    if text_bytes is None or not html_bytes:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't measured this page's text against its page size yet.",
            remediation=RECAPTURE_PAGE,
        )
    ratio = text_bytes / html_bytes
    evidence = {
        "text_bytes": text_bytes,
        "html_bytes": html_bytes,
        "ratio": round(ratio, 4),
    }
    percent = f"{ratio * 100:.1f}%"
    if ratio < TEXT_HTML_RATIO_FAIL:
        return CheckOutcome(
            "warn",
            50,
            f"Only {percent} of this page is readable text ({text_bytes:,} of "
            f"{html_bytes:,} bytes) — either the markup is enormously bloated or the "
            "real content only appears after JavaScript runs.",
            issue_count=1,
            evidence=evidence,
        )
    if ratio < TEXT_HTML_RATIO_WARN:
        # A PASS carrying a 75 — the row's own logic is "advisory signal; only
        # extreme values matter", and its severity_map calls this band "info".
        return CheckOutcome(
            "pass",
            75,
            f"{percent} of the page is readable text — low, though not unusual for a "
            "component-heavy template.",
            issue_count=1,
            evidence=evidence,
        )
    return CheckOutcome("pass", 100, f"{percent} of the page is readable text.", evidence=evidence)


def check_image_alt_presence(ev: PageEvidence) -> CheckOutcome:
    count = ev.image_count
    missing = ev.images_missing_alt
    if count is None or missing is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't listed this page's images yet.",
            remediation=RECAPTURE_PAGE,
        )
    if count == 0:
        return CheckOutcome("n_a", None, "No images on this page.")
    if missing == 0:
        return CheckOutcome("pass", 100, f"All {count} images carry alt text.")
    ratio = missing / count
    score = clamp_score(round(95 * (1 - ratio)))
    status = (
        "fail" if (ratio >= IMAGE_ALT_FAIL_RATIO or missing >= IMAGE_ALT_FAIL_COUNT) else "warn"
    )
    return CheckOutcome(
        status,
        score,
        f"{missing} of {count} images have no alt text — invisible to image "
        "search and screen readers.",
        issue_count=missing,
    )


# --- Images & media --------------------------------------------------------
#
# All five read the per-<img> inventory in `web.snapshot.images.items`. The live
# crawl enriches that same inventory with bounded status, byte, response-format,
# and decoded-dimension evidence before persistence. Old snapshots and capture
# failures remain explicit `n_a`, never an unverified pass.


def _inventory_or_reason(ev: PageEvidence) -> tuple[list[dict[str, Any]], CheckOutcome | None]:
    """The usable per-image inventory, or the `n_a` that explains its absence."""
    if ev.image_count == 0:
        return [], CheckOutcome("n_a", None, "No images on this page.")
    items = [item for item in ev.image_items if isinstance(item, dict)]
    if not items:
        return [], CheckOutcome(
            "n_a",
            None,
            "We haven't listed this page's images yet.",
            remediation=RECAPTURE_PAGE,
        )
    return items, None


def _inventory_note(ev: PageEvidence, items: list[dict[str, Any]]) -> str:
    """Names the inventory cap when the page carried more images than we kept."""
    total = ev.image_count
    if isinstance(total, int) and total > len(items):
        return f" (measured over the first {len(items)} of {total} images)"
    return ""


def check_image_dimension_attrs(ev: PageEvidence) -> CheckOutcome:
    """Width/height on every <img> — the main image-driven CLS prevention.

    A CSS `aspect-ratio` reserves space just as well but is invisible to an
    HTML-only audit, so a page styled that way scores low here. That is the
    documented limit of the evidence, not a hidden assumption.
    """
    items, unavailable = _inventory_or_reason(ev)
    if unavailable:
        return unavailable
    missing = [
        item.get("src") or "(no src)"
        for item in items
        if item.get("width") is None or item.get("height") is None
    ]
    total = len(items)
    covered = total - len(missing)
    coverage = covered / total
    score = clamp_score(round(100 * coverage))
    note = _inventory_note(ev, items)
    if coverage >= IMAGE_DIMENSION_ATTR_PASS_COVERAGE:
        return CheckOutcome(
            "pass",
            score,
            f"{covered} of {total} images declare width and height{note}.",
            issue_count=len(missing),
            evidence={"missing_dimensions": sample_urls(missing)} if missing else None,
        )
    status = "fail" if coverage < IMAGE_DIMENSION_ATTR_FAIL_COVERAGE else "warn"
    return CheckOutcome(
        status,
        score,
        f"{len(missing)} of {total} images declare no width/height{note} — the browser "
        "cannot reserve space for them, so the page jumps as they load (layout shift).",
        issue_count=len(missing),
        evidence={"missing_dimensions": sample_urls(missing)},
    )


def check_image_lazy_loading(ev: PageEvidence) -> CheckOutcome:
    """Lazy below the fold, eager above it — and never lazy on the hero.

    Viewport geometry is not captured, so "above the fold" is approximated by
    DOM order (the first `IMAGE_ABOVE_FOLD_DOM_COUNT` images) plus the page's
    own featured/OG image, which IS captured and is the usual LCP element.
    """
    items, unavailable = _inventory_or_reason(ev)
    if unavailable:
        return unavailable

    def is_lazy(item: dict[str, Any]) -> bool:
        return str(item.get("loading") or "").strip().lower() == "lazy"

    above_fold_indexes = {
        index
        for index, item in enumerate(items)
        if index < IMAGE_ABOVE_FOLD_DOM_COUNT or item.get("featured") is True
    }
    above_fold = [item for index, item in enumerate(items) if index in above_fold_indexes]
    below_fold = [item for index, item in enumerate(items) if index not in above_fold_indexes]
    note = _inventory_note(ev, items)

    hero_lazy = [item.get("src") or "(no src)" for item in above_fold if is_lazy(item)]
    if hero_lazy:
        return CheckOutcome(
            "fail",
            30,
            f"{len(hero_lazy)} image(s) at the top of the page are lazy-loaded — "
            "lazy-loading the hero/LCP image delays the largest paint the browser "
            "measures and is a known Core Web Vitals killer.",
            issue_count=len(hero_lazy),
            evidence={"lazy_above_fold": sample_urls(hero_lazy)},
        )

    eager_below = [item.get("src") or "(no src)" for item in below_fold if not is_lazy(item)]
    if not eager_below:
        return CheckOutcome(
            "pass",
            100,
            f"Lazy-loading policy is correct in both directions across {len(items)} images{note}.",
        )
    ratio = len(eager_below) / len(below_fold)
    score = 60 if ratio > IMAGE_BELOW_FOLD_EAGER_FAIL_RATIO else 80
    return CheckOutcome(
        "warn",
        score,
        f"{len(eager_below)} of {len(below_fold)} images below the fold load eagerly{note} — "
        "the browser downloads them before the visitor can possibly see them.",
        issue_count=len(eager_below),
        evidence={"eager_below_fold": sample_urls(eager_below)},
    )


def check_image_modern_format(ev: PageEvidence) -> CheckOutcome:
    """Share of raster images served as WebP/AVIF instead of JPEG/PNG/GIF.

    Uses captured transfer bytes and response content type, including the
    preferred `<picture>` source rather than its legacy `<img>` fallback.
    """
    items, unavailable = _inventory_or_reason(ev)
    if unavailable:
        return unavailable

    measured = [
        item
        for item in items
        if isinstance(item.get("bytes"), int)
        and item["bytes"] >= 0
        and item.get("capture_status") in {"complete", "http_error", "too_large"}
    ]
    if not measured:
        return CheckOutcome(
            "n_a",
            None,
            "Image transfer sizes have not been captured, so the promised byte-weighted "
            "modern-format share cannot be calculated.",
            remediation=RECAPTURE_PAGE,
        )

    modern_bytes = 0
    legacy_bytes = 0
    legacy: list[str] = []
    for item in measured:
        byte_count = item["bytes"]
        offered = {str(fmt).lower() for fmt in (item.get("picture_formats") or [])}
        actual = str(item.get("actual_format") or "").lower()
        candidates = [item.get("final_url"), item.get("src"), *(item.get("srcset") or [])]
        formats = {actual, *(fmt for fmt in (_image_format(url) for url in candidates) if fmt)}
        if actual in IMAGE_MODERN_RASTER_FORMATS or (
            not actual and offered & IMAGE_MODERN_RASTER_FORMATS
        ):
            modern_bytes += byte_count
        elif formats & IMAGE_LEGACY_RASTER_FORMATS:
            legacy_bytes += byte_count
            legacy.append(item.get("src") or "(no src)")

    classified = modern_bytes + legacy_bytes
    note = _inventory_note(ev, items)
    if classified == 0:
        return CheckOutcome(
            "n_a",
            None,
            f"None of the {len(measured)} measured images had a classifiable raster format.",
        )
    coverage = modern_bytes / classified
    score = clamp_score(round(100 * coverage))
    if coverage >= IMAGE_MODERN_FORMAT_PASS_COVERAGE:
        return CheckOutcome(
            "pass",
            score,
            f"{modern_bytes} of {classified} measured raster bytes are WebP/AVIF{note}.",
            issue_count=len(legacy),
        )
    status = "fail" if coverage < IMAGE_MODERN_FORMAT_FAIL_COVERAGE else "warn"
    return CheckOutcome(
        status,
        score,
        f"{legacy_bytes} of {classified} measured raster bytes are JPEG/PNG/GIF{note} — "
        "WebP or AVIF typically cuts those downloads by a quarter to a half.",
        issue_count=len(legacy),
        evidence={"legacy_format_images": sample_urls(legacy)},
    )


def check_image_oversized(ev: PageEvidence) -> CheckOutcome:
    """Images delivered far larger than the box they are drawn into.

    Scores captured transfer-byte bands and decoded natural width against the
    declared display width. Missing capture remains `n_a`.
    """
    items, unavailable = _inventory_or_reason(ev)
    if unavailable:
        return unavailable

    measured: list[tuple[str, float, int, int, int]] = []
    for item in items:
        display = item.get("width")
        intrinsic = item.get("natural_width")
        byte_count = item.get("bytes")
        if (
            not isinstance(display, int)
            or display <= 0
            or not isinstance(intrinsic, int)
            or intrinsic <= 0
            or not isinstance(byte_count, int)
            or byte_count < 0
        ):
            continue
        measured.append(
            (item.get("src") or "(no src)", intrinsic / display, intrinsic, display, byte_count)
        )

    if not measured:
        return CheckOutcome(
            "n_a",
            None,
            "No image has all three measurements needed here: display width, decoded "
            "natural width, and transfer bytes.",
            remediation=RECAPTURE_PAGE,
        )

    measured.sort(key=lambda row: row[1], reverse=True)
    worst_src, worst_ratio, worst_intrinsic, worst_display, _worst_bytes = measured[0]
    offenders = [
        f"{src} ({intrinsic}px for a {display}px slot; {byte_count} bytes)"
        for src, ratio, intrinsic, display, byte_count in measured
        if ratio > IMAGE_OVERSIZE_MINOR_RATIO or byte_count > IMAGE_OVERSIZE_WARN_BYTES
    ]
    worst_bytes = max(row[4] for row in measured)
    estimated_waste_bytes = sum(
        round(byte_count * (1 - min(1.0, (display / intrinsic) ** 2)))
        for _src, _ratio, intrinsic, display, byte_count in measured
    )
    if worst_ratio <= IMAGE_OVERSIZE_MINOR_RATIO and worst_bytes <= IMAGE_OVERSIZE_WARN_BYTES:
        return CheckOutcome(
            "pass",
            100,
            f"All {len(measured)} measurable images are sized for their slot "
            f"(worst case {worst_ratio:.1f}x and {worst_bytes} bytes).",
        )
    detail = (
        f"the worst is {worst_intrinsic}px wide for a {worst_display}px slot "
        f"({worst_ratio:.1f}x): {worst_src}"
    )
    if worst_ratio > IMAGE_OVERSIZE_SEVERE_RATIO or worst_bytes > IMAGE_OVERSIZE_FAIL_BYTES:
        status, score = "fail", 25
    elif worst_ratio > IMAGE_OVERSIZE_MAJOR_RATIO or worst_bytes > IMAGE_OVERSIZE_WARN_BYTES:
        status, score = "warn", 50
    else:
        status, score = "warn", 80
    return CheckOutcome(
        status,
        score,
        f"{len(offenders)} image(s) are delivered far larger than they are displayed — "
        f"{detail}. Estimated avoidable transfer is {estimated_waste_bytes} bytes.",
        issue_count=len(offenders),
        evidence={
            "oversized_images": sample_urls(offenders),
            "estimated_waste_bytes": estimated_waste_bytes,
            "largest_image_bytes": worst_bytes,
        },
    )


def check_broken_images(ev: PageEvidence) -> CheckOutcome:
    """<img> sources that return 4xx/5xx.

    Uses the bounded image evidence captured before snapshot persistence. A
    network failure or old snapshot without statuses remains `n_a`.
    """
    items, unavailable = _inventory_or_reason(ev)
    if unavailable:
        return unavailable
    statuses = [
        (item.get("src") or "(no src)", item["http_status"], item.get("content_type"))
        for item in items
        if isinstance(item.get("http_status"), int)
    ]
    if not statuses:
        return CheckOutcome(
            "n_a",
            None,
            f"None of this page's {len(items)} images have been status-checked — the "
            "crawl fetches pages, not their images, so whether they load is unverified.",
        )
    broken = [
        src
        for src, status, content_type in statuses
        if status == 0
        or status >= 400
        or (isinstance(content_type, str) and not content_type.lower().startswith("image/"))
    ]
    if not broken and len(statuses) < len(items):
        return CheckOutcome(
            "n_a",
            None,
            f"Only {len(statuses)} of {len(items)} inventoried images returned a status; "
            "the unchecked remainder prevents a reliable all-clear.",
            remediation=RECAPTURE_PAGE,
        )
    if not broken:
        return CheckOutcome(
            "pass",
            100,
            f"All {len(statuses)} status-checked images load.",
        )
    score = 25 if len(broken) >= BROKEN_IMAGE_FAIL_COUNT else 50
    return CheckOutcome(
        "fail",
        score,
        f"{len(broken)} image(s) on this page do not load — visitors see a broken "
        "icon where a picture should be.",
        issue_count=len(broken),
        evidence={"broken_images": sample_urls(broken)},
    )


# --- Indexability ----------------------------------------------------------


def check_meta_robots_conflicts(ev: PageEvidence) -> CheckOutcome:
    robots = (ev.meta_robots or "").lower()
    tokens = {t.strip() for t in robots.split(",") if t.strip()}
    if ev.noindex is None and not robots:
        return CheckOutcome("pass", 100, "No robots directives — indexable by default.")
    if "index" in tokens and "noindex" in tokens:
        return CheckOutcome(
            "fail",
            20,
            f'Conflicting robots directives ("{ev.meta_robots}") — index and '
            "noindex together leave the outcome to the crawler's mood.",
            issue_count=1,
        )
    if ev.noindex:
        return CheckOutcome(
            "fail",
            10,
            "Page is noindexed — it can never rank. If that is intentional, "
            "suppress this finding; if not, this silently removes the page from Google.",
            issue_count=1,
            evidence={"meta_robots": ev.meta_robots},
        )
    if ev.nofollow:
        return CheckOutcome(
            "warn",
            55,
            "Page is nofollowed — its internal links pass no signals onward.",
            issue_count=1,
            evidence={"meta_robots": ev.meta_robots},
        )
    return CheckOutcome(
        "pass",
        100,
        f'Robots directives are clean ("{ev.meta_robots}").'
        if robots
        else "Robots directives are clean.",
    )


def check_canonical_presence(ev: PageEvidence) -> CheckOutcome:
    canonical = ev.canonical_url
    if not canonical:
        return CheckOutcome(
            "warn",
            50,
            "No rel=canonical — parameter/scheme/host variants of this URL can "
            "compete with it in the index.",
            issue_count=1,
        )
    if not canonical.startswith(("http://", "https://")):
        return CheckOutcome(
            "warn",
            45,
            f'rel=canonical is not an absolute URL ("{canonical[:120]}") — '
            "relative canonicals are error-prone and best made absolute.",
            issue_count=1,
        )
    return CheckOutcome("pass", 100, f"rel=canonical present: {canonical[:160]}")


def check_canonical_conflicts(ev: PageEvidence) -> CheckOutcome:
    canonical = ev.canonical_url
    if not canonical or not canonical.startswith(("http://", "https://")):
        return CheckOutcome(
            "n_a",
            None,
            "This page has no full canonical link, so there is nothing to check.",
        )
    if ev.canonical_matches is True:
        return CheckOutcome("pass", 100, "Canonical is self-referential — no conflict.")
    if ev.canonical_matches is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't checked where this page's canonical link points yet.",
            remediation=RECAPTURE_PAGE,
        )
    if registrable_host(canonical) != registrable_host(ev.url):
        return CheckOutcome(
            "fail",
            25,
            f"Canonical points at a DIFFERENT site ({canonical[:160]}) — this page "
            "donates all its equity off-domain. Verify that is deliberate.",
            issue_count=1,
            evidence={"canonical_url": canonical},
        )
    if ev.noindex:
        return CheckOutcome(
            "fail",
            20,
            "Page is noindexed AND canonicalized to another URL — two conflicting "
            "de-indexing signals; Google ignores canonicals on noindexed pages.",
            issue_count=1,
            evidence={"canonical_url": canonical},
        )
    return CheckOutcome(
        "warn",
        55,
        f"Page is canonicalized to another URL ({canonical[:160]}) — fine when "
        "this is a deliberate duplicate, a leak when it is not.",
        issue_count=1,
        evidence={"canonical_url": canonical},
    )


# --- Transport (was ONLY in the aidream IssueDetector) ---------------------
#
# Status and redirects are split into FOUR checks, not two, because the
# `web.analysis_item` catalogue models them as four separate items
# (`broken_page_4xx`, `server_error_5xx`, `redirect_chain`, `redirect_loop`)
# with different weights and severity bands — a 5xx is a 3.0-weight outage, a
# 4xx is a dead end, and a loop is categorically worse than a long chain. One
# combined check could only ever be recorded under one of those keys, so the
# other verdicts would be computed and thrown away.


def _chain_urls(ev: PageEvidence) -> list[str]:
    return [
        hop["url"] for hop in (ev.redirect_chain or []) if isinstance(hop, dict) and hop.get("url")
    ]


def check_broken_page_4xx(ev: PageEvidence) -> CheckOutcome:
    status = ev.http_status
    if status is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded what this page's server answered yet.",
            remediation=RECAPTURE_PAGE,
        )
    if 400 <= status < 500:
        return CheckOutcome(
            "fail",
            10,
            f"The page returns HTTP {status} — it is a dead end; every link "
            "pointing here is wasted.",
            issue_count=1,
            evidence={"http_status": status},
        )
    return CheckOutcome("pass", 100, f"HTTP {status} — not a client error.")


def check_server_error_5xx(ev: PageEvidence) -> CheckOutcome:
    status = ev.http_status
    if status is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded what this page's server answered yet.",
            remediation=RECAPTURE_PAGE,
        )
    # 0 is the crawler's "no response at all" (timeout / connection refused),
    # which the catalogue item scores together with 5xx.
    if status == 0:
        return CheckOutcome(
            "fail",
            5,
            "The server never responded (timeout or connection failure) — the page "
            "is unreachable for users and crawlers alike.",
            issue_count=1,
            evidence={"http_status": status},
        )
    if 500 <= status < 600:
        return CheckOutcome(
            "fail",
            5,
            f"The server returned HTTP {status} — the page is broken for users and "
            "will be dropped from the index if it persists.",
            issue_count=1,
            evidence={"http_status": status},
        )
    return CheckOutcome("pass", 100, f"HTTP {status} — not a server error.")


def check_redirect_chain(ev: PageEvidence) -> CheckOutcome:
    chain = ev.redirect_chain or []
    status = ev.http_status
    if status is not None and 300 <= status < 400:
        return CheckOutcome(
            "warn",
            60,
            f"The URL answers with HTTP {status} rather than serving content "
            "directly — link to the destination instead.",
            issue_count=1,
            evidence={"http_status": status},
        )
    if not chain:
        return CheckOutcome("pass", 100, "No redirects — the URL serves content directly.")
    if len(chain) > REDIRECT_CHAIN_MAX_HOPS:
        return CheckOutcome(
            "warn",
            45,
            f"{len(chain) - 1} redirect hops before this page resolves (limit is "
            f"{REDIRECT_CHAIN_MAX_HOPS - 1}) — every hop wastes crawl budget and "
            "leaks link equity.",
            issue_count=len(chain) - 1,
            evidence={"redirect_chain": sample_urls(_chain_urls(ev))},
        )
    return CheckOutcome("pass", 100, f"Redirect chain is short ({max(0, len(chain) - 1)} hop(s)).")


def check_redirect_loop(ev: PageEvidence) -> CheckOutcome:
    urls_in_chain = _chain_urls(ev)
    if not urls_in_chain:
        return CheckOutcome("pass", 100, "No redirect chain to loop.")
    if len(urls_in_chain) != len(set(urls_in_chain)):
        return CheckOutcome(
            "fail",
            1,
            "The redirect chain visits the same URL twice — a redirect LOOP; "
            "neither users nor crawlers ever arrive.",
            issue_count=1,
            evidence={"redirect_chain": sample_urls(urls_in_chain)},
        )
    return CheckOutcome("pass", 100, "Every hop in the redirect chain is a distinct URL.")


def check_temporary_redirect_usage(ev: PageEvidence) -> CheckOutcome:
    """302/307 where a 301/308 was meant.

    A temporary redirect tells search engines to keep the OLD address and pass
    nothing to the new one. Almost every 302 on a real site is permanent in
    practice, which quietly strands the destination.

    ⚠️ SINGLE-SESSION TIER ONLY. The catalogue row scores a 302 that survives
    three or more crawl sessions harder (40) than one seen once (65), because
    persistence is what proves it is not genuinely temporary. This sweep reads
    only the LATEST accepted snapshot per page, so the multi-session tier is
    NOT evaluated here and this check never claims it — see
    ``FOUND_DEFECTS.md`` (multi-session persistence for analysis checks).
    Meta-refresh redirects belong to ``check_meta_refresh``, not here.
    """
    chain = ev.redirect_chain or []
    status = ev.http_status
    hop_statuses = [hop.get("status") for hop in chain if isinstance(hop, dict)]
    known = [s for s in hop_statuses if isinstance(s, int)]
    temporary = sorted({s for s in known if s in TEMPORARY_REDIRECT_STATUSES})
    if isinstance(status, int) and status in TEMPORARY_REDIRECT_STATUSES:
        temporary = sorted({*temporary, status})

    if temporary:
        codes = "/".join(str(code) for code in temporary)
        return CheckOutcome(
            "warn",
            65,
            f"This URL redirects with a temporary {codes} — search engines keep the "
            "old address and pass none of its earned authority to the destination. "
            "A move you do not plan to undo should be a 301.",
            issue_count=len(temporary),
            evidence={
                "temporary_statuses": temporary,
                "redirect_chain": sample_urls(_chain_urls(ev)),
            },
        )
    if known:
        redirects = [code for code in known if 300 <= code < 400]
        if isinstance(status, int) and 300 <= status < 400:
            redirects.append(status)
        return CheckOutcome(
            "pass",
            100,
            "Every redirect on the way to this page is permanent (301/308)."
            if redirects
            else "No redirect — the URL serves content directly.",
        )
    if chain or status is not None:
        # A chain was recorded but its hop statuses were not — older captures
        # stored URLs only. Nothing to judge; say so rather than passing.
        if chain:
            return CheckOutcome(
                "n_a",
                None,
                "We recorded this page's redirects but not the kind of redirect they "
                "were, so we can't tell temporary from permanent.",
                remediation=RECAPTURE_PAGE,
            )
        return CheckOutcome("pass", 100, "No redirect — the URL serves content directly.")
    return CheckOutcome(
        "n_a",
        None,
        "We haven't fetched this URL yet, so we don't know whether it redirects.",
        remediation=RECAPTURE_PAGE,
    )


def check_soft_404_detection(ev: PageEvidence) -> CheckOutcome:
    """A 200 that is really an error page.

    A "soft 404" answers OK and then shows the visitor nothing — so search
    engines index an empty page, and the site's real 404s never get counted.

    ⚠️ Two of the catalogue row's signals need evidence this per-page check
    cannot see: a hash match against the SITE's own 404 template (that is a
    site-wide comparison) and a redirect to a generic error page. Only the
    page-local signals — not-found phrasing and a near-empty body — are scored
    here; the template-hash tier is filed in ``FOUND_DEFECTS.md``.
    """
    status = ev.http_status
    if status is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't fetched this URL yet, so we don't know what it answers with.",
            remediation=RECAPTURE_PAGE,
        )
    if status != 200:
        return CheckOutcome(
            "pass",
            100,
            f"This URL answers with HTTP {status} — whatever it is, it is not "
            "pretending to be a working page.",
        )
    words = ev.word_count
    if words is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't counted the words on this page yet.",
            remediation=RECAPTURE_PAGE,
        )
    phrasing = bool(ev.title and SOFT_404_TITLE_PATTERN.search(ev.title))
    nearly_empty = words < SOFT_404_PHRASE_MAX_WORDS
    evidence = {"word_count": words, "title": ev.title, "http_status": status}

    if phrasing and nearly_empty:
        return CheckOutcome(
            "fail",
            15,
            f'This page answers HTTP 200 while its title says "{ev.title}" and it '
            f"carries only {words} words — it is an error page in disguise. Search "
            "engines index it as a real page and visitors hit a dead end.",
            issue_count=1,
            evidence=evidence,
        )
    if words < SOFT_404_EMPTY_MAX_WORDS:
        return CheckOutcome(
            "warn",
            40,
            f"This page answers HTTP 200 with only {words} words — there is nothing "
            "here, which is what a broken or removed page usually looks like.",
            issue_count=1,
            evidence=evidence,
        )
    if phrasing:
        return CheckOutcome(
            "warn",
            70,
            f"This page answers HTTP 200 but its title reads like an error page "
            f'("{ev.title}"). If the page is genuinely gone it should answer 404 or 410.',
            issue_count=1,
            evidence=evidence,
        )
    if nearly_empty:
        return CheckOutcome(
            "warn",
            70,
            f"This page answers HTTP 200 with only {words} words — thin enough that a "
            "search engine may treat it as an error page rather than content.",
            issue_count=1,
            evidence=evidence,
        )
    return CheckOutcome("pass", 100, "This page answers HTTP 200 and serves real content.")


def check_pagination_markup(ev: PageEvidence) -> CheckOutcome:
    """`rel=next`/`rel=prev` sanity — captured, never audited, before 2026-08-09.

    Google stopped using these as an indexing signal in 2019, but they remain a
    discovery hint for crawlers and a correctness signal for the site: a page
    that points `rel=next`/`rel=prev` at ITSELF is a paginator bug that traps a
    crawler on one page of the series.
    """
    pagination = ev.pagination or {}
    if not pagination:
        return CheckOutcome(
            "n_a",
            None,
            "This page is not part of a next/previous page series, so there is nothing to check.",
        )
    self_refs = [
        rel
        for rel in ("prev", "next")
        if pagination.get(rel) and str(pagination[rel]).rstrip("/") == ev.url.rstrip("/")
    ]
    if self_refs:
        return CheckOutcome(
            "fail",
            25,
            f"rel={'/'.join(self_refs)} points at this page itself — the pagination "
            "series is a dead end; crawlers cannot reach the rest of it.",
            issue_count=len(self_refs),
            evidence={"pagination": dict(pagination)},
        )
    declared = ", ".join(f"rel={rel}" for rel in ("prev", "next") if pagination.get(rel))
    return CheckOutcome(
        "pass",
        100,
        f"Pagination markup is coherent ({declared}).",
        evidence={"pagination": dict(pagination)},
    )


def check_mixed_content(ev: PageEvidence) -> CheckOutcome:
    resources = ev.mixed_content or []
    if not resources:
        return CheckOutcome("pass", 100, "No insecure http:// resources on this page.")
    n = len(resources)
    return CheckOutcome(
        "warn",
        clamp_score(70 - 5 * n),
        f"{n} resource(s) load over plain http:// on an https:// page — browsers "
        "block or warn on mixed content, and the padlock disappears.",
        issue_count=n,
        evidence={"mixed_content": sample_urls(resources)},
    )


def check_https_enforcement(ev: PageEvidence) -> CheckOutcome:
    """Served over HTTPS, and no HTTP duplicate left reachable.

    Two independent facts, and the catalogue row scores both. The FIRST is free
    — the URL's own scheme — and is the whole reason this check is per-page: a
    single http:// page on an otherwise-HTTPS site is the failure. The SECOND
    needs a probe of the URL's http:// variant, supplied as
    `http_variant_probe` — the site probe samples real page paths for exactly
    this (`site_probe.page_http_variant_probe`), and falls back to the site's
    http:// ORIGIN result for a page outside the sample. A check is pure: it
    NEVER fetches. With neither, the last three bands are unknowable and this
    answers `n_a` rather than passing on evidence nobody collected.
    """
    scheme = urlsplit(ev.url).scheme.lower()
    if scheme not in ("http", "https"):
        return CheckOutcome("n_a", None, f"Not an http(s) URL ({ev.url[:120]}).")
    if scheme == "http":
        return CheckOutcome(
            "fail",
            5,
            "This page is served over plain HTTP — browsers mark it 'Not secure', "
            "the content can be read and rewritten in transit, and Google has "
            "treated HTTPS as a ranking signal since 2014.",
            issue_count=1,
            evidence={"scheme": "http", "url": ev.url},
        )

    probe = ev.http_variant_probe
    status = probe.get("status") if isinstance(probe, dict) else None
    if not isinstance(status, int):
        return CheckOutcome(
            "n_a",
            None,
            "This page is served securely. We haven't checked whether an insecure "
            "copy of it is also reachable — this page wasn't in the sample we probed.",
            evidence={"scheme": "https"},
        )

    location = probe.get("location") if isinstance(probe, dict) else None
    target_scheme = urlsplit(str(location)).scheme.lower() if location else ""
    if 200 <= status < 300:
        return CheckOutcome(
            "fail",
            30,
            f"The http:// variant of this URL answers HTTP {status} instead of "
            "redirecting — the page is live at two addresses, splitting its "
            "signals and leaving an insecure copy indexable.",
            issue_count=1,
            evidence={"http_variant": probe},
        )
    if 300 <= status < 400:
        if target_scheme and target_scheme != "https":
            return CheckOutcome(
                "fail",
                30,
                f"The http:// variant redirects (HTTP {status}) but lands on "
                f"{target_scheme}:// — the insecure address is never left behind.",
                issue_count=1,
                evidence={"http_variant": probe},
            )
        if status in HTTP_VARIANT_PERMANENT_REDIRECTS:
            return CheckOutcome(
                "pass",
                100,
                f"Served over HTTPS, and the http:// variant redirects permanently "
                f"(HTTP {status}).",
                evidence={"http_variant": probe},
            )
        return CheckOutcome(
            "warn",
            70,
            f"The http:// variant redirects with HTTP {status} rather than a "
            "permanent 301/308 — a temporary redirect tells crawlers the insecure "
            "URL is still the real one and passes signals grudgingly.",
            issue_count=1,
            evidence={"http_variant": probe},
        )
    # 4xx / 5xx / 0 on the http:// variant: there is no insecure duplicate to
    # consolidate. Not the textbook redirect, but nothing is reachable over HTTP.
    return CheckOutcome(
        "pass",
        100,
        f"Served over HTTPS, and the http:// variant is not reachable (HTTP {status}).",
        evidence={"http_variant": probe},
    )


def check_page_weight(ev: PageEvidence) -> CheckOutcome:
    """HTML DOCUMENT weight — not total page weight.

    The crawl downloads the document and reads every subresource URL out of the
    markup, but it never fetches those subresources, so their transfer sizes do
    not exist anywhere in the evidence. This check therefore grades the one
    number that IS measured, and the catalogue row states the same scope. The
    day subresource sizes are captured, both move together.
    """
    size = ev.response_bytes
    if size is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded how big this page is yet.",
            remediation=RECAPTURE_PAGE,
        )
    if size <= LARGE_PAGE_BYTES:
        return CheckOutcome("pass", 100, f"HTML document is {size:,} bytes.")
    return CheckOutcome(
        "warn",
        40,
        f"The HTML document alone is {size:,} bytes (over {LARGE_PAGE_BYTES:,}) — "
        "slow on mobile connections and expensive to crawl.",
        issue_count=1,
        evidence={"bytes": size},
    )


def check_ttfb_server_response(ev: PageEvidence) -> CheckOutcome:
    """True time to first byte, graded on the row's 800 / 1800 ms bands.

    Reads `ttfb_ms` ONLY. `response_time_ms` is total elapsed — it also covers
    the body download, so a big page on a fast server looks slow through it.
    A snapshot captured before TTFB was measured (or by the browser transport,
    which cannot report it) has no `ttfb_ms` and answers `n_a`: an unknown
    server speed is never scored, in either direction.
    """
    ttfb = ev.ttfb_ms
    if ttfb is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't measured this page's server response time yet.",
            remediation=RECAPTURE_PAGE,
        )
    # Floor division, not round(), in all three bands: Python rounds halves to
    # even and JavaScript rounds them up, so a `round()` here would hand the
    # TypeScript mirror a different score on exact midpoints and break parity
    # for no reason. Floor over non-negative ints means the same thing in both.
    if ttfb <= TTFB_GOOD_MS:
        # 100 at instant, easing to 90 at the good/needs-work boundary.
        return CheckOutcome(
            "pass",
            clamp_score(100 - (10 * ttfb) // TTFB_GOOD_MS),
            f"The server sent the first byte in {ttfb} ms — comfortably inside "
            f"the {TTFB_GOOD_MS} ms bar for a good server response.",
            evidence={"ttfb_ms": ttfb},
        )
    if ttfb <= TTFB_POOR_MS:
        # 89 down to 50 across the needs-improvement band.
        span = TTFB_POOR_MS - TTFB_GOOD_MS
        return CheckOutcome(
            "warn",
            clamp_score(89 - (39 * (ttfb - TTFB_GOOD_MS)) // span),
            f"The server took {ttfb} ms to send the first byte (over "
            f"{TTFB_GOOD_MS} ms) — every other speed metric starts late, and "
            "visitors feel the delay before anything appears.",
            issue_count=1,
            evidence={"ttfb_ms": ttfb},
        )
    return CheckOutcome(
        "fail",
        clamp_score(49 - (ttfb - TTFB_POOR_MS) // 100),
        f"The server took {ttfb} ms to send the first byte (over "
        f"{TTFB_POOR_MS} ms) — slow server response suppresses both rankings "
        "and conversions.",
        issue_count=1,
        evidence={"ttfb_ms": ttfb},
    )


# --- Mobile rendering ------------------------------------------------------


def _parse_viewport(content: str) -> dict[str, str]:
    """`width=device-width, initial-scale=1` → {"width": "device-width", …}."""
    parsed: dict[str, str] = {}
    for part in content.split(","):
        key, _, value = part.partition("=")
        key = key.strip().lower()
        if key:
            parsed[key] = value.strip().lower()
    return parsed


def check_viewport_meta(ev: PageEvidence) -> CheckOutcome:
    """The single tag that decides whether a phone renders the page at all.

    Without it every mobile browser lays the page out at ~980 CSS px and then
    shrinks it, so the site is a pinch-and-pan desktop page on a phone —
    which is what Google's mobile-first index actually sees.
    """
    if ev.head_meta is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded this page's mobile viewport tag yet.",
            remediation=RECAPTURE_PAGE,
        )
    raw = ev.head_meta.get("viewport")
    content = raw.strip() if isinstance(raw, str) else ""
    if not content:
        return CheckOutcome(
            "fail",
            20,
            "This page has no viewport tag, so phones render it as a shrunken "
            "desktop page. Google indexes the mobile version — this is the single "
            "biggest mobile-rendering defect a page can have.",
            issue_count=1,
        )
    directives = _parse_viewport(content)
    width = directives.get("width", "")
    if width != "device-width":
        return CheckOutcome(
            "fail",
            40,
            (
                f'The viewport is fixed at "{width}" instead of the device width — '
                "the page cannot adapt to the screen it is on."
                if width
                else "The viewport tag never sets a width, so phones fall back to a "
                "desktop-width layout."
            ),
            issue_count=1,
            evidence={"viewport": content},
        )
    lockouts: list[str] = []
    if directives.get("user-scalable", "") in VIEWPORT_ZOOM_DISABLED_VALUES:
        lockouts.append("user-scalable=no")
    try:
        max_scale = float(directives["maximum-scale"])
    except (KeyError, ValueError):
        max_scale = None
    if max_scale is not None and max_scale <= VIEWPORT_ZOOM_LOCK_MAX_SCALE:
        lockouts.append(f"maximum-scale={directives['maximum-scale']}")
    if lockouts:
        return CheckOutcome(
            "warn",
            60,
            f"The viewport is responsive but blocks zoom ({', '.join(lockouts)}) — "
            "anyone who needs to enlarge the text cannot, which fails accessibility "
            "guidelines and drives real visitors away.",
            issue_count=len(lockouts),
            evidence={"viewport": content},
        )
    return CheckOutcome("pass", 100, f'Responsive viewport declared ("{content}").')


# --- Language --------------------------------------------------------------

# Well-formed BCP-47: language[-script][-region][-variant…][-extension…][-private].
# Structural only — this says the tag is SHAPED right, never that the content
# is in that language (nothing in a crawl snapshot detects content language).
_BCP47_RE = re.compile(
    r"^[A-Za-z]{2,3}(?:-[A-Za-z]{3}){0,3}"
    r"(?:-[A-Za-z]{4})?"
    r"(?:-(?:[A-Za-z]{2}|[0-9]{3}))?"
    r"(?:-(?:[0-9A-Za-z]{5,8}|[0-9][0-9A-Za-z]{3}))*"
    r"(?:-[0-9A-WY-Za-wy-z](?:-[0-9A-Za-z]{2,8})+)*"
    r"(?:-x(?:-[0-9A-Za-z]{1,8})+)?$"
)


def check_html_lang_validity(ev: PageEvidence) -> CheckOutcome:
    if not ev.head_captured:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't read this page's markup yet, so its language tag is unknown.",
            remediation=RECAPTURE_PAGE,
        )
    lang = (ev.lang or "").strip()
    if not lang:
        return CheckOutcome(
            "warn",
            55,
            "The <html> tag declares no language. Screen readers pick the wrong "
            "voice, browsers offer the wrong translation, and search engines have "
            "to guess which country's results this page belongs in.",
            issue_count=1,
        )
    if not _BCP47_RE.match(lang) or lang.lower().startswith("x-"):
        return CheckOutcome(
            "fail",
            45,
            f'The declared language "{lang[:60]}" is not a valid language code — '
            "it is ignored exactly as if it were missing. Use a standard code "
            'such as "en" or "en-US".',
            issue_count=1,
            evidence={"lang": lang},
        )
    return CheckOutcome(
        "pass",
        100,
        f'Language declared as "{lang}", a valid code. (Whether the writing is '
        "actually in that language is not measured from a crawl.)",
    )


# --- Social cards ----------------------------------------------------------


def _url_extension(url: str) -> str:
    return urlsplit(url).path.rsplit(".", 1)[-1].lower() if "." in urlsplit(url).path else ""


def _same_target(a: str, b: str) -> bool:
    """URL equality for canonical-vs-og:url — scheme/host case and the
    trailing slash are noise, everything else is a real difference."""
    left, right = urlsplit(a), urlsplit(b)
    return (
        left.scheme.lower() == right.scheme.lower()
        and left.netloc.lower() == right.netloc.lower()
        and (left.path or "/").rstrip("/") == (right.path or "/").rstrip("/")
        and left.query == right.query
    )


def check_og_image_validity(ev: PageEvidence) -> CheckOutcome:
    """The picture that appears when the page is shared.

    A crawl can prove the tag exists and points somewhere a share crawler can
    fetch; it cannot prove the pixels are big enough, because that needs the
    image itself. The reasoning says which half was measured.
    """
    if not ev.head_captured:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't read this page's markup yet, so its share tags are unknown.",
            remediation=RECAPTURE_PAGE,
        )
    raw = ev.og.get("og:image")
    image = raw.strip() if isinstance(raw, str) else ""
    if not image:
        return CheckOutcome(
            "fail",
            45,
            "No share image (og:image) — links to this page post as a bare grey "
            "rectangle everywhere, which collapses how often anyone clicks them.",
            issue_count=1,
        )
    if not image.startswith(("http://", "https://")):
        return CheckOutcome(
            "fail",
            45,
            f'The share image is not a full web address ("{image[:120]}"). Facebook, '
            "LinkedIn and X do not resolve relative paths, so no image is shown.",
            issue_count=1,
            evidence={"og_image": image},
        )
    extension = _url_extension(image)
    if extension and extension not in OG_IMAGE_SUPPORTED_EXTENSIONS:
        return CheckOutcome(
            "warn",
            55,
            f"The share image is a .{extension} file, which the social networks do "
            f"not render. Use one of: {', '.join(sorted(OG_IMAGE_SUPPORTED_EXTENSIONS))}.",
            issue_count=1,
            evidence={"og_image": image},
        )
    return CheckOutcome(
        "pass",
        100,
        f"Share image declared as a full web address ({image[:160]}). Its pixel "
        "size is not measured here — that needs the image file itself.",
        evidence={"og_image": image},
    )


def check_social_meta_completeness(ev: PageEvidence) -> CheckOutcome:
    if not ev.head_captured:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't read this page's markup yet, so its share tags are unknown.",
            remediation=RECAPTURE_PAGE,
        )
    missing = [
        tag
        for tag in SOCIAL_REQUIRED_OG_TAGS
        if not (isinstance(ev.og.get(tag), str) and ev.og[tag].strip())
    ]
    present = len(SOCIAL_REQUIRED_OG_TAGS) - len(missing)
    twitter_card = ev.twitter.get("twitter:card")
    has_twitter_card = isinstance(twitter_card, str) and bool(twitter_card.strip())

    og_url = (ev.og.get("og:url") or "").strip()
    canonical = (ev.canonical_url or "").strip()
    conflicts = bool(
        og_url
        and canonical
        and og_url.startswith(("http://", "https://"))
        and canonical.startswith(("http://", "https://"))
        and not _same_target(og_url, canonical)
    )

    score = round(100 * present / len(SOCIAL_REQUIRED_OG_TAGS))
    if conflicts:
        score -= SOCIAL_OG_URL_CONFLICT_PENALTY
    if not has_twitter_card:
        score -= SOCIAL_NO_TWITTER_CARD_PENALTY
    score = clamp_score(score)

    problems: list[str] = []
    if missing:
        problems.append(f"missing {', '.join(missing)}")
    if not has_twitter_card:
        problems.append("no twitter:card, so X falls back to a small preview")
    if conflicts:
        problems.append(
            f"og:url ({og_url[:100]}) disagrees with the canonical URL "
            f"({canonical[:100]}), so shares may credit the wrong page"
        )
    evidence: dict[str, Any] = {
        "missing_og_tags": missing,
        "twitter_card": twitter_card if has_twitter_card else None,
        "og_url": og_url or None,
        "canonical_url": canonical or None,
    }
    if not problems:
        return CheckOutcome(
            "pass",
            score,
            "Share preview is complete: all five Open Graph tags plus a Twitter "
            f'card ("{twitter_card}"), and og:url agrees with the canonical URL.',
            evidence=evidence,
        )
    status = (
        "pass"
        if score >= SOCIAL_META_PASS_SCORE
        else "warn"
        if score >= SOCIAL_META_WARN_SCORE
        else "fail"
    )
    return CheckOutcome(
        status,
        score,
        "Shares of this page will not render a full preview — " + "; ".join(problems) + ".",
        issue_count=len(missing) + (0 if has_twitter_card else 1) + (1 if conflicts else 0),
        evidence=evidence,
    )


# --- Redirects declared in the markup --------------------------------------


def check_meta_refresh_redirect(ev: PageEvidence) -> CheckOutcome:
    """A `<meta http-equiv="refresh">` standing in for an HTTP redirect.

    Only the markup half is measured: a crawl snapshot records the tag, not
    the client-side `location =` assignments that do the same thing in
    JavaScript, and the reasoning never implies otherwise.
    """
    if ev.head_meta is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded this page's refresh tag yet.",
            remediation=RECAPTURE_PAGE,
        )
    raw = ev.head_meta.get("refresh")
    content = raw.strip() if isinstance(raw, str) else ""
    if not content:
        return CheckOutcome(
            "pass", 100, "This page does not redirect itself through a meta refresh tag."
        )
    delay_part, _, target_part = content.partition(";")
    target = target_part.split("=", 1)[1].strip().strip("'\"") if "=" in target_part else ""
    try:
        delay = float(delay_part.strip())
    except ValueError:
        delay = 0.0
    if not target:
        return CheckOutcome(
            "pass",
            100,
            f"The page reloads itself every {delay_part.strip() or '0'} seconds but "
            "does not send visitors elsewhere, so it is not standing in for a redirect.",
            evidence={"meta_refresh": content},
        )
    if delay <= META_REFRESH_INSTANT_MAX_SECONDS:
        return CheckOutcome(
            "fail",
            35,
            f"This page instantly bounces visitors to {target[:120]} using a meta "
            "refresh tag instead of a real server redirect. Search engines treat "
            "that as a weaker, slower signal and some ignore it, so the destination "
            "inherits little of this page's standing.",
            issue_count=1,
            evidence={"meta_refresh": content, "target": target},
        )
    return CheckOutcome(
        "warn",
        50,
        f"This page shows for {delay_part.strip()} seconds and then sends visitors "
        f"to {target[:120]} via a meta refresh tag. Interstitials like this waste "
        "the visit and are a weaker signal than a server redirect.",
        issue_count=1,
        evidence={"meta_refresh": content, "target": target},
    )


# --- Structured data -------------------------------------------------------
#
# The capture is RICHER than the checks here: `web.snapshot.structured_data`
# keeps every parsed JSON-LD document, every ORIGINAL script string (malformed
# ones included) and the parse error each one produced, plus normalized blocks,
# microdata, RDFa and microformats. Nothing below re-parses anything — a
# second JSON-LD parser would be a second source of truth for the same page.


#: Properties Google requires for a rich result of this type. A type missing
#: from this table is markup we do not claim rich-result eligibility for; its
#: presence is still recorded (schema_types) and judged by the coverage item.
RICH_RESULT_REQUIRED_PROPERTIES: dict[str, tuple[str, ...]] = {
    "Article": ("headline",),
    "NewsArticle": ("headline",),
    "BlogPosting": ("headline",),
    "BreadcrumbList": ("itemListElement",),
    "Course": ("name", "description", "provider"),
    "Event": ("name", "startDate", "location"),
    "FAQPage": ("mainEntity",),
    "HowTo": ("name", "step"),
    "JobPosting": ("title", "datePosted", "hiringOrganization", "jobLocation"),
    "LocalBusiness": ("name", "address"),
    "Organization": ("name",),
    "Product": ("name", "offers"),
    "QAPage": ("mainEntity",),
    "Recipe": ("name", "image"),
    "Review": ("itemReviewed", "reviewRating", "author"),
    "SoftwareApplication": ("name", "offers"),
    "VideoObject": ("name", "thumbnailUrl", "uploadDate"),
}

#: Properties Google recommends — absent, the markup is still valid but the
#: rich result renders with less (a warn, never a fail).
RICH_RESULT_RECOMMENDED_PROPERTIES: dict[str, tuple[str, ...]] = {
    "Article": ("image", "author", "datePublished", "dateModified", "publisher"),
    "NewsArticle": ("image", "author", "datePublished", "dateModified", "publisher"),
    "BlogPosting": ("image", "author", "datePublished", "dateModified"),
    "Course": ("url", "image"),
    "Event": ("description", "endDate", "image", "offers", "performer"),
    "HowTo": ("image", "totalTime", "supply", "tool"),
    "JobPosting": ("description", "baseSalary", "employmentType", "validThrough"),
    "LocalBusiness": ("telephone", "openingHours", "geo", "url", "image", "priceRange"),
    "Organization": ("url", "logo", "sameAs", "contactPoint"),
    "Product": ("image", "description", "brand", "aggregateRating", "sku"),
    "Recipe": (
        "author",
        "datePublished",
        "description",
        "recipeIngredient",
        "recipeInstructions",
        "cookTime",
    ),
    "Review": ("datePublished",),
    "SoftwareApplication": ("aggregateRating", "applicationCategory", "operatingSystem"),
    "VideoObject": ("description", "duration", "contentUrl", "embedUrl"),
}

#: Spellings schema.org accepts for the SAME fact. A page that declares
#: `openingHoursSpecification` has stated its opening hours; calling that
#: "missing" is the check being wrong, not the page.
SCHEMA_PROPERTY_ALIASES: dict[str, tuple[str, ...]] = {
    "address": ("address", "location"),
    "author": ("author", "creator"),
    "image": ("image", "thumbnailUrl", "photo"),
    "openingHours": ("openingHours", "openingHoursSpecification"),
    "offers": ("offers", "aggregateRating", "review"),
    "step": ("step", "steps"),
    "telephone": ("telephone", "phone"),
}

#: schema.org LocalBusiness subtypes common enough to be worth naming. A page
#: that declares `Restaurant` HAS declared a local business.
LOCAL_BUSINESS_SUBTYPES: frozenset[str] = frozenset(
    {
        "AutomotiveBusiness",
        "ChildCare",
        "Dentist",
        "DryCleaningOrLaundry",
        "EmergencyService",
        "EmploymentAgency",
        "EntertainmentBusiness",
        "FinancialService",
        "FoodEstablishment",
        "GovernmentOffice",
        "HealthAndBeautyBusiness",
        "HomeAndConstructionBusiness",
        "InsuranceAgency",
        "LegalService",
        "Library",
        "LodgingBusiness",
        "MedicalBusiness",
        "ProfessionalService",
        "RadioStation",
        "RealEstateAgent",
        "Restaurant",
        "SelfStorage",
        "ShoppingCenter",
        "SportsActivityLocation",
        "Store",
        "TelevisionStation",
        "TouristInformationCenter",
        "TravelAgency",
    }
)

#: Types that declare "this site belongs to this business/organization".
BUSINESS_ENTITY_TYPES: frozenset[str] = frozenset(
    {"Organization", "Corporation", "NGO", "LocalBusiness", *LOCAL_BUSINESS_SUBTYPES}
)

#: NAP — Name, Address, Phone. The three properties a business entity exists to
#: state; every local-search surface keys on them.
BUSINESS_CORE_PROPERTIES: tuple[str, ...] = ("name", "address", "telephone")

#: Present, the entity competes in local search; absent, it is merely correct.
BUSINESS_ENHANCED_PROPERTIES: tuple[str, ...] = ("geo", "openingHours", "sameAs")

#: How many core NAP properties may be missing before the markup is a defect
#: rather than an omission (`local_business_markup` score contract).
BUSINESS_MISSING_CORE_FAIL_COUNT = 2

#: How many offending values a structured-data check attaches as evidence.
STRUCTURED_DATA_EVIDENCE_LIMIT = 5

#: How much of a malformed JSON-LD script is quoted back to the user. Enough to
#: recognize WHICH script broke; never the whole document.
MALFORMED_SCRIPT_SNIPPET_CHARS = 200


def structured_data_blocks(structured_data: dict[str, Any]) -> list[dict[str, Any]]:
    """The normalized entity blocks the capture already produced.

    Each is ``{"source": "json-ld"|"microdata"|…, "types": [...], "data": {...}}``
    exactly as `structured_data.StructuredDataBlock.to_dict` wrote it.
    """
    blocks = structured_data.get("blocks")
    if not isinstance(blocks, list):
        return []
    return [block for block in blocks if isinstance(block, dict)]


def _block_types(block: dict[str, Any]) -> list[str]:
    types = block.get("types")
    if not isinstance(types, list):
        return []
    # Microdata carries full schema.org URLs; the capture already trims those,
    # but RDFa vocabularies can still arrive prefixed.
    return [str(t).rstrip("/").rsplit("/", 1)[-1] for t in types if t]


def _property_value(node: dict[str, Any], prop: str) -> Any:
    """The declared value for `prop`, honouring the accepted alias spellings."""
    for name in SCHEMA_PROPERTY_ALIASES.get(prop, (prop,)):
        value = node.get(name)
        if value not in (None, "", [], {}):
            return value
    return None


def _missing_properties(node: dict[str, Any], props: tuple[str, ...]) -> list[str]:
    return [prop for prop in props if _property_value(node, prop) is None]


def rich_result_type_of(types: list[str]) -> str | None:
    """Which rich-result contract a block is claiming, if any."""
    for declared in types:
        if declared in RICH_RESULT_REQUIRED_PROPERTIES:
            return declared
    for declared in types:
        if declared in LOCAL_BUSINESS_SUBTYPES:
            return "LocalBusiness"
    return None


#: Sub-properties worth flattening a schema.org object down to, in the order a
#: human writes them. Anything else falls back to a stable JSON rendering, so a
#: value is never "missing" just because we did not recognize its shape.
SCHEMA_VALUE_SUBPROPERTIES: tuple[str, ...] = (
    "name",
    "streetAddress",
    "addressLocality",
    "addressRegion",
    "postalCode",
    "addressCountry",
    "latitude",
    "longitude",
    "telephone",
)


def flatten_schema_value(value: Any) -> str | None:
    """A comparable string for a schema.org value of ANY shape.

    Used to decide whether two pages state the SAME business fact, so the
    result is normalized (whitespace collapsed, lowercased) and lists are
    order-insensitive — `sameAs` in a different order is not a NAP conflict.
    """
    if value is None or value == "" or value == [] or value == {}:
        return None
    if isinstance(value, str):
        return " ".join(value.split()).lower() or None
    if isinstance(value, list):
        parts = [part for part in (flatten_schema_value(item) for item in value) if part]
        return ", ".join(sorted(parts)) or None
    if isinstance(value, dict):
        parts = [
            part
            for part in (flatten_schema_value(value.get(key)) for key in SCHEMA_VALUE_SUBPROPERTIES)
            if part
        ]
        if parts:
            return " ".join(parts)
        return json.dumps(value, sort_keys=True, default=str).lower()
    return str(value).strip().lower() or None


def business_entities_in(structured_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Every Organization / LocalBusiness declaration in ONE page's capture.

    Returned normalized so the site-level check can compare declarations from
    different pages directly: `{"types": [...], "name": ..., "address": ...}`
    with a `None` for each property the entity does not state.
    """
    entities: list[dict[str, Any]] = []
    for block in structured_data_blocks(structured_data):
        data = block.get("data")
        if not isinstance(data, dict):
            continue
        types = [name for name in _block_types(block) if name in BUSINESS_ENTITY_TYPES]
        if not types:
            continue
        entity: dict[str, Any] = {"types": types}
        for prop in (*BUSINESS_CORE_PROPERTIES, *BUSINESS_ENHANCED_PROPERTIES):
            entity[prop] = flatten_schema_value(_property_value(data, prop))
        entities.append(entity)
    return entities


def check_structured_data_validity(ev: PageEvidence) -> CheckOutcome:
    """Parse errors and rich-result completeness, from the stored capture.

    Order is the catalogue row's, top-down: a parse error voids the whole
    script, so it outranks any missing property.
    """
    payload = ev.structured_data or {}
    if not payload:
        return CheckOutcome(
            "n_a",
            None,
            "This page has no stored structured-data capture yet.",
            remediation=RECAPTURE_PAGE,
        )

    errors = [e for e in (payload.get("parse_errors") or []) if isinstance(e, dict)]
    if errors:
        raw_scripts = [s for s in (payload.get("json_ld_raw") or []) if isinstance(s, str)]
        broken: list[dict[str, Any]] = []
        for error in errors[:STRUCTURED_DATA_EVIDENCE_LIMIT]:
            index = error.get("index")
            snippet = (
                raw_scripts[index][:MALFORMED_SCRIPT_SNIPPET_CHARS]
                if isinstance(index, int) and 0 <= index < len(raw_scripts)
                else None
            )
            broken.append(
                {
                    "source": error.get("source"),
                    "message": error.get("message"),
                    **({"script": snippet} if snippet else {}),
                }
            )
        return CheckOutcome(
            "fail",
            30,
            f"{len(errors)} structured-data script(s) on this page could not be "
            "read at all — a search engine discards a block it cannot parse, so "
            "every rich result this page markup was written for is void.",
            issue_count=len(errors),
            evidence={"parse_errors": broken},
        )

    blocks = structured_data_blocks(payload)
    if not blocks:
        return CheckOutcome(
            "n_a",
            None,
            "This page carries no structured data, so there is nothing to "
            "validate (whether it SHOULD have some is the coverage check's job).",
        )

    missing_required: list[dict[str, Any]] = []
    missing_recommended: list[dict[str, Any]] = []
    validated: list[str] = []
    for block in blocks:
        data = block.get("data")
        if not isinstance(data, dict):
            continue
        rich_type = rich_result_type_of(_block_types(block))
        if rich_type is None:
            continue
        validated.append(rich_type)
        required = _missing_properties(data, RICH_RESULT_REQUIRED_PROPERTIES[rich_type])
        if required:
            missing_required.append({"type": rich_type, "missing": required})
            continue
        recommended = _missing_properties(
            data, RICH_RESULT_RECOMMENDED_PROPERTIES.get(rich_type, ())
        )
        if recommended:
            missing_recommended.append({"type": rich_type, "missing": recommended})

    if missing_required:
        named = ", ".join(
            f"{item['type']} (no {', '.join(item['missing'])})" for item in missing_required
        )
        return CheckOutcome(
            "fail",
            50,
            f"Structured data on this page is missing properties Google REQUIRES "
            f"for the rich result it describes: {named}. The markup parses, but "
            "it cannot produce the enhanced search listing it was written for.",
            issue_count=len(missing_required),
            evidence={"missing_required": missing_required[:STRUCTURED_DATA_EVIDENCE_LIMIT]},
        )
    if missing_recommended:
        named = ", ".join(
            f"{item['type']} (no {', '.join(item['missing'])})"
            for item in missing_recommended[:STRUCTURED_DATA_EVIDENCE_LIMIT]
        )
        return CheckOutcome(
            "warn",
            75,
            f"Structured data is valid, but recommended properties are absent: "
            f"{named}. The rich result will show, with less in it.",
            issue_count=len(missing_recommended),
            evidence={"missing_recommended": missing_recommended[:STRUCTURED_DATA_EVIDENCE_LIMIT]},
        )
    if not validated:
        return CheckOutcome(
            "pass",
            100,
            f"{len(blocks)} structured-data block(s) parse cleanly. None of them "
            "claims a rich-result type with published property requirements.",
        )
    return CheckOutcome(
        "pass",
        100,
        f"Structured data parses cleanly and every rich-result type in use "
        f"({', '.join(sorted(set(validated)))}) declares its required and "
        "recommended properties.",
    )


# --- International ---------------------------------------------------------

#: `x-default` is the reserved hreflang value for the fallback page — it is not
#: a language tag, so `_BCP47_RE` (the ONE language-tag shape in this module,
#: shared with `check_html_lang_validity`) must never see it.
HREFLANG_DEFAULT_VALUE = "x-default"

#: Below this share of return-linking targets, a broken hreflang cluster is a
#: failure rather than a gap (`hreflang_reciprocity` is a formula item, so this
#: is the only band it needs).
HREFLANG_RECIPROCITY_FAIL_SCORE = 50


def is_valid_hreflang_value(value: str) -> bool:
    """A legal `hreflang` attribute value: a BCP-47 tag, or `x-default`."""
    tag = (value or "").strip()
    if not tag:
        return False
    if tag.lower() == HREFLANG_DEFAULT_VALUE:
        return True
    return bool(_BCP47_RE.match(tag)) and not tag.lower().startswith("x-")


def normalized_url_key(url: str) -> str:
    """Comparison key for "is this the same page?" across annotations.

    Scheme and fragment are dropped and the host is lowercased with `www.`
    folded away, because an hreflang cluster that disagrees with itself only on
    those is not the defect this check exists to report.
    """
    parts = urlsplit((url or "").strip())
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/") or "/"
    return f"{host}{path}" + (f"?{parts.query}" if parts.query else "")


def hreflang_entries(ev: PageEvidence) -> list[tuple[str, str]]:
    """(lang, href) pairs as captured, both non-empty strings."""
    entries: list[tuple[str, str]] = []
    for item in ev.hreflang or []:
        if not isinstance(item, dict):
            continue
        lang = item.get("lang")
        href = item.get("href")
        if isinstance(lang, str) and isinstance(href, str) and lang.strip() and href.strip():
            entries.append((lang.strip(), href.strip()))
    return entries


def check_hreflang_validity(ev: PageEvidence) -> CheckOutcome:
    """Codes, absolute URLs, self-reference, canonical agreement, x-default.

    Rule order is the catalogue row's and is deliberate: an invalid code breaks
    the whole cluster for every page in it, so it is reported ahead of the
    self-reference and canonical problems that break only this page's half.
    """
    entries = hreflang_entries(ev)
    if not entries:
        return CheckOutcome(
            "n_a",
            None,
            "This page declares no hreflang annotations, so there is no "
            "language cluster to validate.",
        )

    bad_codes = [lang for lang, _ in entries if not is_valid_hreflang_value(lang)]
    relative = [href for _, href in entries if not href.lower().startswith(("http://", "https://"))]
    if bad_codes or relative:
        problems = []
        if bad_codes:
            problems.append(
                f"{len(bad_codes)} annotation(s) use a language code that is not "
                f"a valid language(-script)(-region) tag: {', '.join(bad_codes[:5])}"
            )
        if relative:
            problems.append(
                f"{len(relative)} annotation(s) point at a relative URL — hreflang "
                "must always be absolute"
            )
        return CheckOutcome(
            "fail",
            30,
            "; ".join(problems)
            + ". Search engines drop an entire hreflang cluster that contains an "
            "annotation they cannot resolve.",
            issue_count=len(bad_codes) + len(relative),
            evidence={
                "invalid_codes": bad_codes[:STRUCTURED_DATA_EVIDENCE_LIMIT],
                "relative_urls": sample_urls(relative),
            },
        )

    self_key = normalized_url_key(ev.url)
    self_entry = next(
        ((lang, href) for lang, href in entries if normalized_url_key(href) == self_key), None
    )
    if self_entry is None:
        return CheckOutcome(
            "fail",
            45,
            f"This page's hreflang set names {len(entries)} language version(s) but "
            "never names ITSELF. A cluster without a self-reference is invalid, and "
            "search engines ignore the whole set.",
            issue_count=1,
            evidence={"declared": sample_urls([href for _, href in entries])},
        )

    canonical = ev.canonical_url
    if canonical and canonical.startswith(("http://", "https://")):
        if normalized_url_key(canonical) != normalized_url_key(self_entry[1]):
            return CheckOutcome(
                "fail",
                40,
                f"The hreflang self-reference ({self_entry[1][:120]}) and the "
                f"rel=canonical ({canonical[:120]}) name DIFFERENT URLs — the page "
                "is annotating a URL it also says is not the canonical one, and "
                "the two signals cancel out.",
                issue_count=1,
                evidence={"self_href": self_entry[1], "canonical_url": canonical},
            )

    if not any(lang.lower() == HREFLANG_DEFAULT_VALUE for lang, _ in entries):
        return CheckOutcome(
            "warn",
            80,
            f"The hreflang set is valid ({len(entries)} version(s), self-reference "
            "present) but declares no x-default — visitors whose language matches "
            "none of the declared versions get no designated fallback page.",
            issue_count=1,
        )
    return CheckOutcome(
        "pass",
        100,
        f"Valid hreflang set: {len(entries)} version(s), all codes and URLs well "
        "formed, self-reference present, x-default declared.",
    )


# --- Lab performance (PageSpeed Insights) ----------------------------------
#
# 🚨 These checks are PURE, like every other one here: they read
# `ev.lab_performance` and nothing else. PageSpeed is a paid, rate-limited,
# minute-long remote render — fetching it from inside a check would put a
# network call in the middle of a per-page sweep over thousands of pages.
# Collection is a separate step (`POST /seo/pages/{id}/pagespeed/sync` →
# matrx-seo → `seo.page_performance`); this half only scores what landed.
#
# Every band below is the `web.analysis_item` row's own published formula. The
# row is the contract; these constants are that contract, named.

# cwv_lcp — Google's Core Web Vitals thresholds, in milliseconds.
LCP_GOOD_MS = 2_500
LCP_POOR_MS = 4_000
#: Milliseconds of LCP above `LCP_POOR_MS` that cost one point.
LCP_POOR_MS_PER_POINT = 200

# cwv_inp_tbt — Total Blocking Time, the lab proxy for INP.
TBT_GOOD_MS = 200
TBT_POOR_MS = 600
TBT_POOR_MS_PER_POINT = 50

# cwv_cls — unitless layout-shift score.
CLS_GOOD = 0.1
CLS_POOR = 0.25
#: CLS above `CLS_POOR` is multiplied by this before being deducted.
CLS_POOR_PENALTY_PER_UNIT = 100

# The band a "good" measurement is scored within (90-100), and the middle band
# (50-89) that "needs improvement" maps onto. Shared by all three CWV checks —
# the catalogue rows publish the identical shape.
CWV_GOOD_BAND = (90, 100)
CWV_MID_BAND = (50, 89)
CWV_POOR_CEILING = 49

# asset_delivery — estimated savings, in milliseconds.
DELIVERY_SAVINGS_GOOD_MS = 250
DELIVERY_SAVINGS_POOR_MS = 1_500
DELIVERY_POOR_MS_PER_POINT = 100
DELIVERY_POOR_FLOOR = 10

# caching_policy — a static asset is "well cached" at or above this lifetime.
CACHE_WELL_CACHED_MIN_MS = 30 * 24 * 60 * 60 * 1_000
#: Below this many static bytes, caching is not a meaningful lever and the
#: catalogue row's formula scores a flat 100 ("negligible static bytes").
CACHE_NEGLIGIBLE_STATIC_BYTES = 10_000

#: A measurement older than this is stale evidence, not today's truth: answer
#: `n_a` with the one-click re-measure rather than scoring a year-old render.
LAB_PERFORMANCE_MAX_AGE_DAYS = 90

#: Status bands shared by the performance checks, applied to the final score.
PERFORMANCE_PASS_SCORE = 90
PERFORMANCE_WARN_SCORE = 50


def _linear_band(value: float, low: float, high: float, band: tuple[int, int]) -> int:
    """Map `value` in [low, high] onto `band`, where LOWER value scores HIGHER."""
    span = high - low
    top, bottom = band[1], band[0]
    if span <= 0:
        return top
    fraction = min(max((value - low) / span, 0.0), 1.0)
    return clamp_score(round(top - fraction * (top - bottom)))


def _performance_status(score: int) -> str:
    if score >= PERFORMANCE_PASS_SCORE:
        return "pass"
    return "warn" if score >= PERFORMANCE_WARN_SCORE else "fail"


def _lab(ev: PageEvidence) -> tuple[LabPerformance | None, CheckOutcome | None]:
    """The shared "is there a usable measurement?" gate.

    Returns `(lab, None)` when a check may score, or `(None, outcome)` with the
    `n_a` verdict + its one-click fix when it may not.
    """
    lab = ev.lab_performance
    if lab is None:
        return None, CheckOutcome(
            "n_a",
            None,
            "We haven't measured this page's real-world loading speed yet. It "
            "needs a browser to load the page and time it, which a crawl cannot do.",
            remediation=COLLECT_PAGESPEED,
        )
    if lab.observed_at is not None:
        age_days = (datetime.now(lab.observed_at.tzinfo) - lab.observed_at).days
        if age_days > LAB_PERFORMANCE_MAX_AGE_DAYS:
            return None, CheckOutcome(
                "n_a",
                None,
                f"The last speed measurement of this page is {age_days} days old — "
                "too old to describe the page as it is today.",
                remediation=COLLECT_PAGESPEED,
            )
    return lab, None


def _measured_on(lab: LabPerformance) -> str:
    where = "on a phone" if lab.strategy == "mobile" else f"on {lab.strategy}"
    when = f" on {lab.observed_at.date().isoformat()}" if lab.observed_at else ""
    return f"{where}{when}"


def check_cwv_lcp(ev: PageEvidence) -> CheckOutcome:
    lab, blocked = _lab(ev)
    if blocked is not None:
        return blocked
    assert lab is not None
    if lab.lcp_ms is None:
        return CheckOutcome(
            "n_a",
            None,
            "The speed measurement for this page did not report when its main "
            "content finished drawing.",
            remediation=COLLECT_PAGESPEED,
        )
    lcp = lab.lcp_ms
    seconds = f"{lcp / 1000:.1f}s"
    if lcp <= LCP_GOOD_MS:
        score = _linear_band(lcp, 0, LCP_GOOD_MS, CWV_GOOD_BAND)
    elif lcp <= LCP_POOR_MS:
        score = _linear_band(lcp, LCP_GOOD_MS, LCP_POOR_MS, CWV_MID_BAND)
    else:
        score = clamp_score(round(CWV_POOR_CEILING - (lcp - LCP_POOR_MS) / LCP_POOR_MS_PER_POINT))
    evidence = {"lcp_ms": lcp, "strategy": lab.strategy}
    if score >= PERFORMANCE_PASS_SCORE:
        return CheckOutcome(
            "pass",
            score,
            f"The main content of this page appears in {seconds} "
            f"({_measured_on(lab)}) — inside Google's 2.5 second target.",
            evidence=evidence,
        )
    return CheckOutcome(
        _performance_status(score),
        score,
        f"The main content of this page takes {seconds} to appear "
        f"({_measured_on(lab)}). Google's target is 2.5 seconds and it treats "
        "anything over 4 as poor; visitors leave before a slow page finishes, "
        "so this costs both rankings and the visits you already earned.",
        issue_count=1,
        evidence=evidence,
    )


def check_cwv_inp_tbt(ev: PageEvidence) -> CheckOutcome:
    lab, blocked = _lab(ev)
    if blocked is not None:
        return blocked
    assert lab is not None
    if lab.tbt_ms is None:
        return CheckOutcome(
            "n_a",
            None,
            "The speed measurement for this page did not report how long it "
            "stayed unresponsive while loading.",
            remediation=COLLECT_PAGESPEED,
        )
    tbt = lab.tbt_ms
    if tbt <= TBT_GOOD_MS:
        score = _linear_band(tbt, 0, TBT_GOOD_MS, CWV_GOOD_BAND)
    elif tbt <= TBT_POOR_MS:
        score = _linear_band(tbt, TBT_GOOD_MS, TBT_POOR_MS, CWV_MID_BAND)
    else:
        score = clamp_score(round(CWV_POOR_CEILING - (tbt - TBT_POOR_MS) / TBT_POOR_MS_PER_POINT))
    evidence = {"tbt_ms": tbt, "strategy": lab.strategy}
    if score >= PERFORMANCE_PASS_SCORE:
        return CheckOutcome(
            "pass",
            score,
            f"While loading, this page ignores taps and clicks for only "
            f"{round(tbt)}ms ({_measured_on(lab)}) — comfortably responsive.",
            evidence=evidence,
        )
    return CheckOutcome(
        _performance_status(score),
        score,
        f"While loading, this page is busy running scripts for {round(tbt)}ms "
        f"({_measured_on(lab)}) and cannot react to taps or clicks during that "
        "time. Visitors read that as broken and tap again, and Google measures "
        "it directly as a ranking signal. The usual cause is too much JavaScript "
        "running before the page is usable.",
        issue_count=1,
        evidence=evidence,
    )


def check_cwv_cls(ev: PageEvidence) -> CheckOutcome:
    lab, blocked = _lab(ev)
    if blocked is not None:
        return blocked
    assert lab is not None
    if lab.cls is None:
        return CheckOutcome(
            "n_a",
            None,
            "The speed measurement for this page did not report how much its "
            "layout moved while loading.",
            remediation=COLLECT_PAGESPEED,
        )
    cls = lab.cls
    if cls <= CLS_GOOD:
        score = _linear_band(cls, 0, CLS_GOOD, CWV_GOOD_BAND)
    elif cls <= CLS_POOR:
        score = _linear_band(cls, CLS_GOOD, CLS_POOR, CWV_MID_BAND)
    else:
        score = clamp_score(round(CWV_POOR_CEILING - (cls - CLS_POOR) * CLS_POOR_PENALTY_PER_UNIT))
    evidence = {"cls": cls, "strategy": lab.strategy}
    if score >= PERFORMANCE_PASS_SCORE:
        return CheckOutcome(
            "pass",
            score,
            f"This page holds still as it loads (layout shift {cls:.3f}, "
            f"{_measured_on(lab)}) — under Google's 0.1 limit.",
            evidence=evidence,
        )
    return CheckOutcome(
        _performance_status(score),
        score,
        f"Content on this page jumps around while it loads (layout shift "
        f"{cls:.3f}, {_measured_on(lab)}; Google's limit is 0.1). That is the "
        "effect where someone goes to tap one thing and hits another because an "
        "image or advert pushed the page down. It is usually fixed by giving "
        "images and embeds a declared width and height.",
        issue_count=1,
        evidence=evidence,
    )


def check_asset_delivery(ev: PageEvidence) -> CheckOutcome:
    lab, blocked = _lab(ev)
    if blocked is not None:
        return blocked
    assert lab is not None
    if lab.delivery_savings_ms is None:
        return CheckOutcome(
            "n_a",
            None,
            "The stored speed measurement for this page predates the delivery "
            "breakdown, so there is nothing to add up yet.",
            remediation=COLLECT_PAGESPEED,
        )
    savings = lab.delivery_savings_ms
    if savings <= DELIVERY_SAVINGS_GOOD_MS:
        score = _linear_band(savings, 0, DELIVERY_SAVINGS_GOOD_MS, CWV_GOOD_BAND)
    elif savings <= DELIVERY_SAVINGS_POOR_MS:
        score = _linear_band(
            savings, DELIVERY_SAVINGS_GOOD_MS, DELIVERY_SAVINGS_POOR_MS, CWV_MID_BAND
        )
    else:
        score = max(
            DELIVERY_POOR_FLOOR,
            clamp_score(
                round(
                    CWV_POOR_CEILING
                    - (savings - DELIVERY_SAVINGS_POOR_MS) / DELIVERY_POOR_MS_PER_POINT
                )
            ),
        )
    offenders = sorted(
        ((name, ms) for name, ms in lab.delivery_audits.items() if ms > 0),
        key=lambda pair: pair[1],
        reverse=True,
    )
    evidence = {
        "total_savings_ms": savings,
        "audits": dict(offenders[:CHECK_EVIDENCE_SAMPLE_LIMIT]),
        "strategy": lab.strategy,
    }
    if score >= PERFORMANCE_PASS_SCORE:
        return CheckOutcome(
            "pass",
            score,
            f"How this page's files are delivered costs it about {round(savings)}ms "
            f"({_measured_on(lab)}) — nothing worth chasing.",
            evidence=evidence,
        )
    names = ", ".join(_DELIVERY_AUDIT_LABELS.get(name, name) for name, _ in offenders[:4])
    return CheckOutcome(
        _performance_status(score),
        score,
        f"About {round(savings) / 1000:.1f}s of this page's load is spent on how "
        f"its files are delivered rather than on the page itself "
        f"({_measured_on(lab)}). The measured causes: {names}. These are the "
        "standard build-and-hosting fixes — nothing about your content has to change.",
        issue_count=len(offenders),
        evidence=evidence,
    )


#: Lighthouse audit id → the same defect stated for a non-technical reader.
_DELIVERY_AUDIT_LABELS: dict[str, str] = {
    "render-blocking-insight": "files that block the page from drawing",
    "document-latency-insight": "a slow or uncompressed first response",
    "image-delivery-insight": "images sent larger than they are shown",
    "legacy-javascript-insight": "code shipped twice for old browsers",
    "duplicated-javascript-insight": "the same code included more than once",
    "font-display-insight": "fonts that hide text while they load",
    "unminified-css": "styling files sent uncompacted",
    "unminified-javascript": "code files sent uncompacted",
    "unused-css-rules": "styling rules this page never uses",
    "unused-javascript": "code this page never runs",
}


def check_caching_policy(ev: PageEvidence) -> CheckOutcome:
    lab, blocked = _lab(ev)
    if blocked is not None:
        return blocked
    assert lab is not None
    if lab.cache_static_bytes is None:
        return CheckOutcome(
            "n_a",
            None,
            "The stored speed measurement for this page predates the caching "
            "breakdown, so its cache lifetimes are unknown.",
            remediation=COLLECT_PAGESPEED,
        )
    static_bytes = lab.cache_static_bytes
    if static_bytes < CACHE_NEGLIGIBLE_STATIC_BYTES:
        return CheckOutcome(
            "pass",
            100,
            "This page loads almost no images, styling or code files of its own, "
            "so how long they are cached makes no practical difference.",
            evidence={"static_bytes": static_bytes},
        )
    short_ttl = [
        resource
        for resource in lab.cache_short_ttl_resources
        if _lab_number(resource.get("cache_lifetime_ms")) is not None
        and float(resource["cache_lifetime_ms"]) < CACHE_WELL_CACHED_MIN_MS
    ]
    poorly_cached_bytes = min(
        static_bytes,
        sum(float(_lab_number(r.get("total_bytes")) or 0.0) for r in short_ttl),
    )
    well_cached_bytes = max(0.0, static_bytes - poorly_cached_bytes)
    score = clamp_score(round(100 * well_cached_bytes / static_bytes))
    evidence = {
        "static_bytes": static_bytes,
        "well_cached_bytes": well_cached_bytes,
        "short_ttl_urls": sample_urls([str(r.get("url") or "") for r in short_ttl]),
        "strategy": lab.strategy,
    }
    if score >= PERFORMANCE_PASS_SCORE:
        return CheckOutcome(
            "pass",
            score,
            "Visitors' browsers keep this page's images, styling and code for a "
            "month or more, so returning visits reuse them instead of "
            "re-downloading them.",
            evidence=evidence,
        )
    share = round(100 * poorly_cached_bytes / static_bytes)
    return CheckOutcome(
        _performance_status(score),
        score,
        f"{share}% of this page's images, styling and code are told to expire in "
        f"under a month ({len(short_ttl)} files, {_measured_on(lab)}), so people "
        "who come back download them all over again — a slower repeat visit for "
        "no benefit. It is a one-line hosting setting, not a content change.",
        issue_count=len(short_ttl),
        evidence=evidence,
    )


# The canonical registry. A per-page SEO check exists HERE or it does not
# exist — no consumer may re-derive one of these verdicts from raw evidence.
PAGE_CHECKS: dict[str, Callable[[PageEvidence], CheckOutcome]] = {
    "url_design_quality": check_url_design_quality,
    "title_presence": check_title_presence,
    "title_length": check_title_length,
    "meta_description_presence": check_meta_description_presence,
    "meta_description_length": check_meta_description_length,
    "h1_presence": check_h1_presence,
    "heading_hierarchy": check_heading_hierarchy,
    "thin_content": check_thin_content,
    "content_depth": check_content_depth,
    "text_html_ratio": check_text_html_ratio,
    "image_alt_presence": check_image_alt_presence,
    "image_dimension_attrs": check_image_dimension_attrs,
    "image_lazy_loading": check_image_lazy_loading,
    "image_modern_format": check_image_modern_format,
    "image_oversized": check_image_oversized,
    "broken_images": check_broken_images,
    "viewport_meta": check_viewport_meta,
    "html_lang_validity": check_html_lang_validity,
    "og_image_validity": check_og_image_validity,
    "social_meta_completeness": check_social_meta_completeness,
    "meta_robots_conflicts": check_meta_robots_conflicts,
    "canonical_presence": check_canonical_presence,
    "canonical_conflicts": check_canonical_conflicts,
    "meta_refresh_redirect": check_meta_refresh_redirect,
    "broken_page_4xx": check_broken_page_4xx,
    "server_error_5xx": check_server_error_5xx,
    "redirect_chain": check_redirect_chain,
    "redirect_loop": check_redirect_loop,
    "temporary_redirect_usage": check_temporary_redirect_usage,
    "soft_404_detection": check_soft_404_detection,
    "pagination_markup": check_pagination_markup,
    "mixed_content": check_mixed_content,
    "https_enforcement": check_https_enforcement,
    "page_weight": check_page_weight,
    "ttfb_server_response": check_ttfb_server_response,
    "structured_data_validity": check_structured_data_validity,
    "hreflang_validity": check_hreflang_validity,
    "cwv_lcp": check_cwv_lcp,
    "cwv_inp_tbt": check_cwv_inp_tbt,
    "cwv_cls": check_cwv_cls,
    "asset_delivery": check_asset_delivery,
    "caching_policy": check_caching_policy,
}


def run_page_checks(ev: PageEvidence) -> dict[str, CheckOutcome]:
    """Every per-page check, keyed by check name."""
    return {key: check(ev) for key, check in PAGE_CHECKS.items()}


# ===========================================================================
# THE WIRE LAYER — verdicts as typed, BOUNDED payloads.
#
# `CheckOutcome` is the in-process shape. Anything that leaves the process —
# an HTTP response the dashboard renders, a tool result an LLM reads — uses
# the Pydantic models below so the field set is concrete (no `dict[str, Any]`
# crossing an API boundary) and the size is bounded by construction.
#
# NOTHING here decides anything. Every verdict comes from `run_page_checks`;
# these builders only project it.
# ===========================================================================

# Bounds for a projected verdict. Reasoning sentences are authored (~1-2
# lines) and evidence lists are already sampled to CHECK_EVIDENCE_SAMPLE_LIMIT,
# so these are backstops against a pathological URL, not routine truncation.
CHECK_REASONING_MAX_CHARS = 600
CHECK_EVIDENCE_VALUE_MAX_CHARS = 300

# How much of a page's raw evidence a model-facing summary carries.
AUDIT_SUMMARY_LIST_LIMIT = 10
AUDIT_SUMMARY_TEXT_MAX_CHARS = 300

CheckStatus = Literal["pass", "warn", "fail", "n_a"]


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _bounded_evidence(evidence: dict[str, Any] | None) -> dict[str, JsonValue] | None:
    """Evidence, with every string and list bounded. Never raises."""
    if not evidence:
        return None
    out: dict[str, JsonValue] = {}
    for key, value in evidence.items():
        if isinstance(value, str):
            out[str(key)] = _clip(value, CHECK_EVIDENCE_VALUE_MAX_CHARS)
        elif isinstance(value, int | float | bool) or value is None:
            out[str(key)] = value
        elif isinstance(value, list):
            out[str(key)] = [
                _clip(str(item), CHECK_EVIDENCE_VALUE_MAX_CHARS)
                for item in value[:CHECK_EVIDENCE_SAMPLE_LIMIT]
            ]
        elif isinstance(value, dict):
            out[str(key)] = {
                str(k): _clip(str(v), CHECK_EVIDENCE_VALUE_MAX_CHARS)
                for k, v in list(value.items())[:AUDIT_SUMMARY_LIST_LIMIT]
            }
        else:
            out[str(key)] = _clip(str(value), CHECK_EVIDENCE_VALUE_MAX_CHARS)
    return out


class PageCheckResult(BaseModel):
    """One verdict on the wire. `reasoning` is the sentence a non-technical
    owner reads — it is the product, not a debug string."""

    key: str
    status: CheckStatus
    score: int | None = None
    reasoning: str
    issue_count: int = 0
    evidence: dict[str, JsonValue] | None = None

    @classmethod
    def from_outcome(cls, key: str, outcome: CheckOutcome) -> PageCheckResult:
        return cls(
            key=key,
            status=outcome.status,  # type: ignore[arg-type]
            score=outcome.score,
            reasoning=_clip(outcome.reasoning, CHECK_REASONING_MAX_CHARS),
            issue_count=outcome.issue_count,
            evidence=_bounded_evidence(outcome.evidence),
        )


class PageCheckTally(BaseModel):
    total: int
    failed: int
    warned: int
    passed: int
    not_applicable: int
    issue_count: int


class PageCheckReport(BaseModel):
    """Every verdict, for a surface that renders all of them (the preview card)."""

    tally: PageCheckTally
    checks: list[PageCheckResult]


class PageCheckDigest(BaseModel):
    """Model-facing projection: the problems in full, the rest as names.

    An LLM needs the failing verdicts and WHY; eighteen verbose "this is fine"
    objects are re-sent to the provider on every loop iteration and buy nothing.
    """

    tally: PageCheckTally
    problems: list[PageCheckResult]
    passed_checks: list[str]
    not_applicable_checks: list[str]


_STATUS_ORDER = {"fail": 0, "warn": 1, "pass": 2, "n_a": 3}


def _tally(results: list[PageCheckResult]) -> PageCheckTally:
    by_status = {status: 0 for status in _STATUS_ORDER}
    for result in results:
        by_status[result.status] += 1
    return PageCheckTally(
        total=len(results),
        failed=by_status["fail"],
        warned=by_status["warn"],
        passed=by_status["pass"],
        not_applicable=by_status["n_a"],
        issue_count=sum(r.issue_count for r in results),
    )


def _results(ev: PageEvidence) -> list[PageCheckResult]:
    return [
        PageCheckResult.from_outcome(key, outcome) for key, outcome in run_page_checks(ev).items()
    ]


def build_page_check_report(ev: PageEvidence) -> PageCheckReport:
    """Every verdict for this page, worst first."""
    results = sorted(_results(ev), key=lambda r: (_STATUS_ORDER[r.status], r.key))
    return PageCheckReport(tally=_tally(results), checks=results)


def build_page_check_digest(ev: PageEvidence) -> PageCheckDigest:
    """The problems in full; passes and n_a as bare names. Bounded by design."""
    results = _results(ev)
    problems = sorted(
        (r for r in results if r.status in ("fail", "warn")),
        key=lambda r: (_STATUS_ORDER[r.status], r.key),
    )
    return PageCheckDigest(
        tally=_tally(results),
        problems=problems,
        passed_checks=sorted(r.key for r in results if r.status == "pass"),
        not_applicable_checks=sorted(r.key for r in results if r.status == "n_a"),
    )


class PageAuditSummary(BaseModel):
    """The page's evidence, bounded — what a model needs to reason about it.

    `SeoAuditResult.to_dict()` carries the full structured-data blob, the whole
    resource inventory, and every link row; that is right for persistence and
    wrong for a tool result that re-enters the prompt on every iteration.
    """

    url: str
    title: str | None = None
    title_length: int = 0
    meta_description: str | None = None
    meta_description_length: int = 0
    canonical: str | None = None
    robots: str | None = None
    lang: str | None = None
    h1: list[str] = Field(default_factory=list)
    h2: list[str] = Field(default_factory=list)
    h1_count: int = 0
    schema_types: list[str] = Field(default_factory=list)
    og: dict[str, str] = Field(default_factory=dict)
    word_count: int = 0
    sentence_count: int = 0
    flesch_reading_ease: float | None = None
    link_count: int = 0
    internal_links: int = 0
    external_links: int = 0
    images_total: int = 0
    images_missing_alt: int = 0
    mixed_content: list[str] = Field(default_factory=list)
    pagination: dict[str, str] = Field(default_factory=dict)


def summarize_audit(audit: SeoAuditResult) -> PageAuditSummary:
    """Bounded projection of a full audit. Lists capped, strings clipped."""
    limit = AUDIT_SUMMARY_LIST_LIMIT
    chars = AUDIT_SUMMARY_TEXT_MAX_CHARS
    return PageAuditSummary(
        url=audit.url,
        title=_clip(audit.title, chars) if audit.title else None,
        title_length=audit.title_length,
        meta_description=_clip(audit.meta_description, chars) if audit.meta_description else None,
        meta_description_length=audit.meta_description_length,
        canonical=_clip(audit.canonical, chars) if audit.canonical else None,
        robots=_clip(audit.robots, chars) if audit.robots else None,
        lang=audit.lang,
        h1=[_clip(h, chars) for h in audit.h1[:limit]],
        h2=[_clip(h, chars) for h in audit.h2[:limit]],
        h1_count=audit.h1_count,
        schema_types=[_clip(s, chars) for s in audit.schema_types[:limit]],
        og={str(k): _clip(str(v), chars) for k, v in list(audit.og.items())[:limit]},
        word_count=audit.word_count,
        sentence_count=audit.sentence_count,
        flesch_reading_ease=audit.flesch_reading_ease,
        link_count=audit.link_count,
        internal_links=audit.internal_links,
        external_links=audit.external_links,
        images_total=audit.images_total,
        images_missing_alt=audit.images_missing_alt,
        mixed_content=[_clip(u, chars) for u in audit.mixed_content[:CHECK_EVIDENCE_SAMPLE_LIMIT]],
        pagination={
            str(k): _clip(str(v), chars) for k, v in list((audit.pagination or {}).items())[:limit]
        },
    )


__all__ = [
    "CACHE_WELL_CACHED_MIN_MS",
    "CLS_GOOD",
    "CLS_POOR",
    "COLLECT_PAGESPEED",
    "DELIVERY_SAVINGS_GOOD_MS",
    "DELIVERY_SAVINGS_POOR_MS",
    "LAB_PERFORMANCE_MAX_AGE_DAYS",
    "LCP_GOOD_MS",
    "LCP_POOR_MS",
    "TBT_GOOD_MS",
    "TBT_POOR_MS",
    "LabPerformance",
    "check_asset_delivery",
    "check_caching_policy",
    "check_cwv_cls",
    "check_cwv_inp_tbt",
    "check_cwv_lcp",
    "lab_performance_from_lighthouse",
    "BUSINESS_CORE_PROPERTIES",
    "BUSINESS_ENHANCED_PROPERTIES",
    "BUSINESS_ENTITY_TYPES",
    "BUSINESS_MISSING_CORE_FAIL_COUNT",
    "HREFLANG_RECIPROCITY_FAIL_SCORE",
    "RICH_RESULT_RECOMMENDED_PROPERTIES",
    "RICH_RESULT_REQUIRED_PROPERTIES",
    "STRUCTURED_DATA_EVIDENCE_LIMIT",
    "SECURITY_RESPONSE_HEADERS",
    "HTTP_VARIANT_PERMANENT_REDIRECTS",
    "BROKEN_IMAGE_FAIL_COUNT",
    "CONTENT_DEPTH_ARTICLE_MIN_WORDS",
    "CONTENT_DEPTH_ARTICLE_SCHEMA_TYPES",
    "CONTENT_DEPTH_ARTICLE_TARGET_WORDS",
    "CONTENT_DEPTH_COMMERCE_MIN_WORDS",
    "CONTENT_DEPTH_COMMERCE_SCHEMA_TYPES",
    "CONTENT_DEPTH_UTILITY_SCHEMA_TYPES",
    "CONTENT_FAIL_WORDS",
    "CONTENT_OK_WORDS",
    "CONTENT_WARN_WORDS",
    "HEADING_EMPTY_FAIL_RATIO",
    "HEADING_SKIP_FAIL_COUNT",
    "IMAGE_ABOVE_FOLD_DOM_COUNT",
    "IMAGE_ALT_FAIL_COUNT",
    "IMAGE_ALT_FAIL_RATIO",
    "IMAGE_BELOW_FOLD_EAGER_FAIL_RATIO",
    "IMAGE_DIMENSION_ATTR_FAIL_COVERAGE",
    "IMAGE_DIMENSION_ATTR_PASS_COVERAGE",
    "IMAGE_LEGACY_RASTER_FORMATS",
    "IMAGE_MODERN_FORMAT_FAIL_COVERAGE",
    "IMAGE_MODERN_FORMAT_PASS_COVERAGE",
    "IMAGE_MODERN_RASTER_FORMATS",
    "IMAGE_OVERSIZE_MAJOR_RATIO",
    "IMAGE_OVERSIZE_MINOR_RATIO",
    "IMAGE_OVERSIZE_SEVERE_RATIO",
    "IMAGE_OVERSIZE_WARN_BYTES",
    "IMAGE_OVERSIZE_FAIL_BYTES",
    "LARGE_PAGE_BYTES",
    "META_REFRESH_INSTANT_MAX_SECONDS",
    "OG_IMAGE_SUPPORTED_EXTENSIONS",
    "PAGE_CHECKS",
    "REDIRECT_CHAIN_MAX_HOPS",
    "SOCIAL_META_PASS_SCORE",
    "SOCIAL_META_WARN_SCORE",
    "SOCIAL_NO_TWITTER_CARD_PENALTY",
    "SOCIAL_OG_URL_CONFLICT_PENALTY",
    "SOCIAL_REQUIRED_OG_TAGS",
    "SOFT_404_EMPTY_MAX_WORDS",
    "SOFT_404_PHRASE_MAX_WORDS",
    "SOFT_404_TITLE_PATTERN",
    "SYNC_SITEMAPS",
    "TEMPORARY_REDIRECT_STATUSES",
    "TEXT_HTML_RATIO_FAIL",
    "TEXT_HTML_RATIO_WARN",
    "TTFB_GOOD_MS",
    "TTFB_POOR_MS",
    "VIEWPORT_ZOOM_DISABLED_VALUES",
    "VIEWPORT_ZOOM_LOCK_MAX_SCALE",
    "CheckOutcome",
    "CheckStatus",
    "HeadingItem",
    "HreflangItem",
    "LinkItem",
    "PageAuditSummary",
    "PageCheckDigest",
    "PageCheckReport",
    "PageCheckResult",
    "PageCheckTally",
    "PageEvidence",
    "SeoAuditResult",
    "audit_html",
    "build_page_check_digest",
    "build_page_check_report",
    "check_canonical_conflicts",
    "check_canonical_presence",
    "check_broken_images",
    "check_broken_page_4xx",
    "check_content_depth",
    "check_h1_presence",
    "check_heading_hierarchy",
    "check_hreflang_validity",
    "check_html_lang_validity",
    "check_image_alt_presence",
    "check_image_dimension_attrs",
    "check_image_lazy_loading",
    "check_image_modern_format",
    "check_image_oversized",
    "check_meta_description_length",
    "check_meta_description_presence",
    "check_meta_refresh_redirect",
    "check_meta_robots_conflicts",
    "check_https_enforcement",
    "check_mixed_content",
    "check_og_image_validity",
    "check_page_weight",
    "check_pagination_markup",
    "check_redirect_chain",
    "check_redirect_loop",
    "check_server_error_5xx",
    "check_soft_404_detection",
    "check_structured_data_validity",
    "check_social_meta_completeness",
    "check_temporary_redirect_usage",
    "check_text_html_ratio",
    "check_thin_content",
    "check_title_length",
    "check_title_presence",
    "check_ttfb_server_response",
    "check_viewport_meta",
    "business_entities_in",
    "clamp_score",
    "declared_page_type",
    "flatten_schema_value",
    "hreflang_entries",
    "is_valid_hreflang_value",
    "normalized_url_key",
    "rich_result_type_of",
    "structured_data_blocks",
    "evidence_from_audit",
    "registrable_host",
    "run_page_checks",
    "sample_urls",
    "security_response_headers",
    "summarize_audit",
]
