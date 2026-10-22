from __future__ import annotations

import json
import re
from collections.abc import Iterator
from typing import Any, Literal
from urllib.parse import urljoin, urlparse

from pydantic import BaseModel, Field
from selectolax.parser import HTMLParser, Node

from matrx_scraper.clean_content import looks_like_address, street_addresses_in
from matrx_scraper.events import PageSummary
from matrx_scraper.media_embed import video_embed_provider

CandidateCategory = Literal["media", "fact", "social", "link", "identity"]

_SOCIAL_HOSTS = {
    "instagram.com": "instagram",
    "facebook.com": "facebook",
    "x.com": "x",
    "twitter.com": "x",
    "tiktok.com": "tiktok",
    "youtube.com": "youtube",
    "youtu.be": "youtube",
    "linkedin.com": "linkedin",
    "pinterest.com": "pinterest",
    "pinterest.ca": "pinterest",
}
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE_PATTERN = r"(?<!\w)(?:\+?1[ .-]?)?(?:\([2-9]\d{2}\)|[2-9]\d{2})[ .-]\d{3}[ .-]\d{4}(?!\w)"
_PHONE_RE = re.compile(_PHONE_PATTERN)
_FAX_RE = re.compile(
    rf"\b(?:fax|facsimile)(?:\s*(?:number|no\.?|#))?\s*[:\-]?\s*(?P<number>{_PHONE_PATTERN})",
    re.IGNORECASE,
)
_LOGO_HINTS = ("logo", "brand", "wordmark", "logomark")
_HERO_HINTS = ("hero", "banner", "masthead", "cover")
# A file or alt text that names itself a social-share card is never a logo.
_SHARE_HINTS = ("social-sharing", "social_sharing", "social-share", "social_share", "sharing-banner",
                "share-image", "share_image", "og-image", "og_image", "og-default", "opengraph", "open-graph",
                "twitter-card", "social-card", "social-media-image", "social_media_image")


def is_share_banner_shape(width: int | None, height: int | None) -> bool:
    """True for a social-share banner's shape (about 1.91:1, 1000px or wider): never a logo."""
    return bool(width and height and width >= 1000 and 1.7 <= width / height <= 2.1)


class DiscoveredCandidate(BaseModel):
    category: CandidateCategory
    guessed_kind: str
    url: str | None = None
    value: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)


class SiteIdentity(BaseModel):
    """Observed homepage identity persisted to ``web.site`` seconds into
    initialize (only-fill-nulls; the user's own edits are never overwritten)."""

    description: str | None = None
    favicon_url: str | None = None
    og_image_url: str | None = None
    logo_url: str | None = None


# A logo candidate below this confidence is left out of the identity write —
# the discovery inbox still receives every candidate. Admits schema.org logos
# (0.99) and header/nav or hint-matched logos (0.8+). The og:image / twitter:image
# share banner is never a logo candidate at all (it is its own og_image kind).
_IDENTITY_LOGO_MIN_CONFIDENCE = 0.8


def derive_site_identity(
    candidates: list[DiscoveredCandidate],
    *,
    summary: PageSummary,
) -> SiteIdentity:
    """Pick the best observed identity values from homepage candidates."""

    def best_url(category: str, kind: str, min_confidence: float = 0.0) -> str | None:
        matches = [
            candidate
            for candidate in candidates
            if candidate.category == category
            and candidate.guessed_kind == kind
            and candidate.url
            and candidate.confidence >= min_confidence
        ]
        if not matches:
            return None
        return max(matches, key=lambda candidate: candidate.confidence).url

    description = (summary.meta_description or "").strip() or None
    return SiteIdentity(
        description=description,
        favicon_url=best_url("media", "favicon"),
        og_image_url=best_url("media", "og_image"),
        logo_url=best_url("media", "logo", _IDENTITY_LOGO_MIN_CONFIDENCE),
    )


def _absolute_http_url(raw: str | None, base_url: str) -> str | None:
    if not raw:
        return None
    value = raw.strip()
    if not value:
        return None
    resolved = urljoin(base_url, value)
    parsed = urlparse(resolved)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return resolved


#: Query parameters that NAME a social page (a video ``?v=``, a Facebook ``profile.php?id=``). Everything else on a
#: social link is junk to the account (``view_as=subscriber``, ``utm_*``, ``fbclid``, ``si``, ``hl``…) and is cut
#: before the link is stored, so one account is one address (live defect 2026-10-15: a brand's YouTube carried
#: ``?view_as=subscriber`` into its stored profile).
_SOCIAL_IDENTIFYING_PARAMS = frozenset({"v", "id", "fbid", "story_fbid", "list"})


def clean_social_url(url: str) -> str:
    """``url`` without its fragment and every query parameter that does not name the page."""
    from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

    parts = urlsplit(url)
    keep = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=False) if k.lower() in _SOCIAL_IDENTIFYING_PARAMS]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(keep), ""))


def _social_kind(url: str) -> str | None:
    host = (urlparse(url).hostname or "").lower()
    host = host.removeprefix("www.")
    for domain, kind in _SOCIAL_HOSTS.items():
        if host == domain or host.endswith(f".{domain}"):
            return kind
    return None


def _schema_nodes(value: Any, path: str = "$") -> Iterator[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _schema_nodes(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _schema_nodes(child, f"{path}[{index}]")


def _schema_url(value: Any, base_url: str) -> str | None:
    if isinstance(value, str):
        return _absolute_http_url(value, base_url)
    if isinstance(value, dict):
        for key in ("url", "contentUrl", "@id"):
            resolved = _absolute_http_url(value.get(key), base_url)
            if resolved:
                return resolved
    return None


def _int_attr(node: Node, name: str) -> int | None:
    raw = (node.attributes.get(name) or "").strip().lower().removesuffix("px")
    try:
        return int(float(raw))
    except ValueError:
        return None


def _ancestor_is_header_or_nav(node: Node) -> bool:
    parent = node.parent
    for _ in range(6):
        if parent is None:
            return False
        if parent.tag in {"header", "nav"}:
            return True
        parent = parent.parent
    return False


def _surrounding(text: str, start: int, length: int) -> str:
    return text[max(0, start - 80) : min(len(text), start + length + 80)].strip()


def extract_homepage_candidates(
    html: str,
    *,
    base_url: str,
    summary: PageSummary,
) -> list[DiscoveredCandidate]:
    tree = HTMLParser(html)
    candidates: list[DiscoveredCandidate] = []

    def add(
        category: CandidateCategory,
        guessed_kind: str,
        *,
        url: str | None = None,
        value: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        confidence: float,
    ) -> None:
        payload = value or {}
        if url is None and not any(item not in (None, "", [], {}) for item in payload.values()):
            return
        candidates.append(
            DiscoveredCandidate(
                category=category,
                guessed_kind=guessed_kind,
                url=url,
                value=payload,
                context=context or {},
                confidence=confidence,
            )
        )

    for link in tree.css("link[href]"):
        rel = (link.attributes.get("rel") or "").lower()
        if "icon" not in rel:
            continue
        url = _absolute_http_url(link.attributes.get("href"), base_url)
        add(
            "media",
            "favicon",
            url=url,
            context={"where": "head link", "rel": rel},
            confidence=0.98,
        )
    for path, node in _schema_nodes(summary.schema_org):
        if not isinstance(node, dict):
            continue
        for key, raw in node.items():
            lowered = key.lower()
            schema_path = f"{path}.{key}"
            if lowered == "logo":
                add(
                    "media",
                    "logo",
                    url=_schema_url(raw, base_url),
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.99,
                )
            elif lowered == "sameas":
                values = raw if isinstance(raw, list) else [raw]
                for item in values:
                    url = _schema_url(item, base_url)
                    kind = _social_kind(url) if url else None
                    if url and kind:
                        add(
                            "social",
                            kind,
                            url=clean_social_url(url),
                            context={"where": "schema.org sameAs", "schema_path": schema_path},
                            confidence=0.98,
                        )
            elif lowered in {"telephone", "phone"} and isinstance(raw, str):
                add(
                    "fact",
                    "phone",
                    value={"text": raw.strip()},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.98,
                )
            elif lowered in {"faxnumber", "fax"} and isinstance(raw, str):
                add(
                    "fact",
                    "fax",
                    value={"text": raw.strip()},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.99,
                )
            elif lowered == "email" and isinstance(raw, str):
                add(
                    "fact",
                    "email",
                    value={"text": raw.strip().removeprefix("mailto:")},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.98,
                )
            elif lowered == "address" and isinstance(raw, str | dict) and (
                isinstance(raw, dict) and any(raw.get(k) for k in ("streetAddress", "postalCode", "addressLocality"))
                or isinstance(raw, str) and looks_like_address(raw)
            ):
                add(
                    "fact",
                    "address",
                    value={"address": raw},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.97,
                )

    og_image = _absolute_http_url(str(summary.og_tags.get("og:image") or ""), base_url)
    twitter_image = _absolute_http_url(str(summary.twitter_tags.get("twitter:image") or ""), base_url)
    share_urls = {u for u in (og_image, twitter_image) if u}

    for image in tree.css("img"):
        attrs = image.attributes
        raw_src = attrs.get("src") or attrs.get("data-src")
        url = _absolute_http_url(raw_src, base_url)
        if not url:
            continue
        alt = (attrs.get("alt") or "").strip()
        class_name = attrs.get("class") or ""
        element_id = attrs.get("id") or ""
        hints = " ".join((raw_src or "", alt, class_name, element_id)).lower()
        context = {
            "where": "header/nav image" if _ancestor_is_header_or_nav(image) else "page image",
            "alt": alt,
            "class": class_name,
            "id": element_id,
        }
        width = _int_attr(image, "width")
        height = _int_attr(image, "height")
        # The share image (og:image / twitter:image) and anything shaped or named like one is stored as its
        # own kind, never as a logo candidate.
        is_share = (
            url in share_urls
            or any(hint in hints for hint in _SHARE_HINTS)
            or is_share_banner_shape(width, height)
        )
        in_header = _ancestor_is_header_or_nav(image)
        named_logo = any(hint in hints for hint in ("logo", "wordmark", "logomark"))
        if not is_share and (in_header or named_logo or any(hint in hints for hint in _LOGO_HINTS)):
            # Real logo signals rank: named logo in the header > named logo or header image > "brand" only.
            confidence = 0.9 if (in_header and named_logo) else 0.85 if (in_header or named_logo) else 0.8
            add("media", "logo", url=url, context=context, confidence=confidence)
        if any(hint in hints for hint in _HERO_HINTS) or (
            width is not None and height is not None and width >= 800 and height >= 300
        ):
            add(
                "media",
                "hero_image",
                url=url,
                context={**context, "width": width, "height": height},
                confidence=0.82,
            )

    if og_image:
        add("media", "og_image", url=og_image, context={"where": "og:image"}, confidence=0.99)
    add(
        "media",
        "twitter_image",
        url=twitter_image,
        context={"where": "twitter:image"},
        confidence=0.98,
    )

    for selector in ("video[src]", "video source[src]"):
        for node in tree.css(selector):
            url = _absolute_http_url(node.attributes.get("src"), base_url)
            if url:
                add(
                    "media",
                    "video",
                    url=url,
                    context={
                        "where": selector,
                        "provider": "html_video",
                        "title": node.attributes.get("title") or "",
                    },
                    confidence=0.85,
                )

    for node in tree.css("iframe[src]"):
        url = _absolute_http_url(node.attributes.get("src"), base_url)
        provider = video_embed_provider(url) if url else None
        if url and provider:
            add(
                "media",
                "video",
                url=url,
                context={
                    "where": "iframe[src]",
                    "provider": provider,
                    "title": node.attributes.get("title") or "",
                },
                confidence=0.95,
            )

    for link in summary.links:
        kind = _social_kind(link.target_url)
        if kind:
            add(
                "social",
                kind,
                url=clean_social_url(link.target_url),
                context={"where": "homepage link", "anchor_text": link.anchor_text},
                confidence=0.92,
            )

    body = tree.body
    visible_text = (body.text(deep=True, separator=" ") if body else tree.text()) or ""
    visible_text = re.sub(r"\s+", " ", visible_text).strip()

    fax_matches = list(_FAX_RE.finditer(visible_text))
    for match in fax_matches:
        number = match.group("number")
        add(
            "fact",
            "fax",
            value={"text": number.strip()},
            context={
                "where": "homepage text",
                "surrounding_text": _surrounding(visible_text, match.start(), len(match.group(0))),
            },
            confidence=0.96,
        )

    for regex, kind, confidence in (
        (_EMAIL_RE, "email", 0.9),
        (_PHONE_RE, "phone", 0.82),
        (None, "address", 0.72),
    ):
        matches = street_addresses_in(visible_text) if kind == "address" else list(regex.finditer(visible_text))
        for match in matches:
            if kind == "phone" and any(
                match.start() >= fax.start("number") and match.end() <= fax.end("number")
                for fax in fax_matches
            ):
                continue
            add(
                "fact",
                kind,
                value={"text": match.group(0).strip()},
                context={
                    "where": "homepage text",
                    "surrounding_text": _surrounding(
                        visible_text, match.start(), len(match.group(0))
                    ),
                },
                confidence=confidence,
            )

    add(
        "identity",
        "title",
        value={"text": summary.title},
        context={"where": "title"},
        confidence=0.99,
    )
    add(
        "identity",
        "description",
        value={"text": summary.meta_description},
        context={"where": "meta description"},
        confidence=0.98,
    )
    add(
        "identity",
        "site_name",
        value={"text": summary.og_tags.get("og:site_name")},
        context={"where": "og:site_name"},
        confidence=0.98,
    )

    deduped: dict[tuple[str, str, str, str], DiscoveredCandidate] = {}
    for candidate in candidates:
        key = (
            candidate.category,
            candidate.guessed_kind,
            candidate.url or "",
            json.dumps(candidate.value, sort_keys=True, separators=(",", ":")),
        )
        current = deduped.get(key)
        if current is None or candidate.confidence > current.confidence:
            deduped[key] = candidate
    return list(deduped.values())


__all__ = [
    "CandidateCategory",
    "DiscoveredCandidate",
    "SiteIdentity",
    "derive_site_identity",
    "extract_homepage_candidates",
]
