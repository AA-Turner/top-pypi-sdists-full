"""The one URL canonicalizer for a captured web page's identity.

Every producer that lands a web page as a Source (the scraper routes, the extension, the capture
ladder, the crawler) addresses it by ``canonical_url`` — the identity the landing door dedupes on,
``(organization_id, canonical_identity, content_hash)``. It lives in this package, not in a host,
because the hosted scraper service computes it too and may not import the host
(``scripts/check_package_boundaries.py``).

Deliberately conservative — the fragment and a trailing slash only. Stripping query parameters
would merge two genuinely different pages on every site that addresses content with them.
(Moved here from ``aidream.services.capture_ladder.landing.canonical_url``, SOURCE-CONVERGENCE
§2.3; that name now re-exports this one.)
"""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

__all__ = ["canonical_url", "url_host", "host_folder", "story_url_key"]

_SLUG = re.compile(r"[^a-z0-9]+")

#: Query parameters that track the CLICK, not the article: leaving them in files the same story
#: three times from three shares. One list for the whole platform — the union of the three article
#: keys it replaced (coverage, the blog adapter, the corpus key; NEWS-ENGINE-SPEC §2 census).
_TRACKING_PREFIXES = ("utm_", "ref_")
_TRACKING_NAMES = frozenset(
    {
        "fbclid",
        "gclid",
        "msclkid",
        "yclid",
        "igshid",
        "mc_cid",
        "mc_eid",
        "ref",
        "s_kwcid",
        "spm",
        "source",
    }
)
_DEFAULT_PORTS = (80, 443)


def _is_tracking(pair: str) -> bool:
    name, _, value = pair.partition("=")
    name = name.lower()
    return (
        name.startswith(_TRACKING_PREFIXES)
        or name in _TRACKING_NAMES
        # A numeric ``s`` is a share code (``?s=20``); ``?s=term`` is a site search and is kept.
        or (name == "s" and value[:1].isdigit())
    )


def canonical_url(url: str) -> str:
    """The URL, minus the fragment and a trailing slash on a path."""
    cleaned = (url or "").strip()
    cleaned = cleaned.split("#", 1)[0]
    if cleaned.endswith("/") and cleaned.count("/") > 3:
        cleaned = cleaned[:-1]
    return cleaned


def url_host(url: str) -> str:
    """The lower-cased host of ``url`` ('' when there is none)."""
    return (url or "").strip().lower().split("//")[-1].split("/")[0].split("?")[0]


def host_folder(url: str) -> str:
    """A file-tree-safe folder name for a URL's host ('page' when there is none)."""
    return _SLUG.sub("-", url_host(url))[:60].strip("-") or "page"


def story_url_key(url: str) -> str:
    """One spelling of an ARTICLE's address, so two feeds or two shares never file it twice.

    Unlike :func:`canonical_url` (a captured page's identity, which keeps every query parameter),
    this is the tracking-stripped key a news sighting, a coverage mention and a same-story cluster
    agree on: https, lower-cased host without ``www.``, a non-default port kept, no fragment, no
    trailing slash, tracking parameters dropped and the rest sorted. Raises ``ValueError`` for a
    blank or hostless URL. (Moved here from ``matrx_seo.coverage.normalize_url``, NEWS-ENGINE-SPEC
    §4.1; the blog adapter's and the corpus's article keys delegate here too.)
    """
    text = (url or "").strip()
    if not text:
        raise ValueError("a story URL cannot be blank")
    if "://" not in text:
        text = f"https://{text}"
    parts = urlsplit(text)
    host = (parts.hostname or "").lower().removeprefix("www.")
    if not host:
        raise ValueError(f"story URL has no host: {url!r}")
    port = parts.port  # raises ValueError for a malformed port
    netloc = host if port is None or port in _DEFAULT_PORTS else f"{host}:{port}"
    path = parts.path.rstrip("/") or "/"
    kept = [pair for pair in parts.query.split("&") if pair and not _is_tracking(pair)]
    return urlunsplit(("https", netloc, path, "&".join(sorted(kept)), ""))
