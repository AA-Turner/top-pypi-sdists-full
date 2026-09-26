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

__all__ = ["canonical_url", "url_host", "host_folder"]

_SLUG = re.compile(r"[^a-z0-9]+")


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
