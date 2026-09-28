"""Small URL helpers — pulled out of the host so the package can offer
"accept any URL the user typed and normalise it" semantics standalone.
"""

from __future__ import annotations


def accept_url_input(value: str) -> str:
    """Accept what a person typed as a web address (INPUT ACCEPTANCE, never an identity).

    Accepts anything the user can plausibly type and returns an https:// URL.
    Examples:
      "abc.com"            -> "https://abc.com"
      "www.example.com"    -> "https://www.example.com"
      "http://example.com" -> "http://example.com"
      "https://x.com/page" -> "https://x.com/page"

    Raises ValueError on empty input or unsupported schemes (anything other
    than http(s) — we don't crawl ftp://, mailto:, etc.).
    """
    raw = (value or "").strip()
    if not raw:
        raise ValueError("base_url cannot be empty")
    if raw.startswith(("http://", "https://")):
        return raw
    if "://" in raw:
        raise ValueError(f"unsupported URL scheme: {raw!r}")
    return f"https://{raw.lstrip('/')}"


# NOTE: `accept_url_input` is the INPUT-ACCEPTANCE layer ("accept anything the
# user typed → a valid https URL"), NOT a canonicalizer: it was named
# `normalize_url` until 2026-09-27, a second function of that name beside the
# stored-identity one, and renamed so no caller can mistake it for an identity
# (NEWS-ENGINE-SPEC §2 URL-identity census, Lane F). The ONE canonical stored identity for the crawl system is
# `matrx_scraper.utils.url.normalize_url` (feeds `url_hash`, used by every
# ingestion source). A former `canonicalize_url_identity` here was a SECOND,
# unused identity function — deleted 2026-07-29 (dead competing identity; the
# Identity Contract forbids a second canonicalizer). Do not reintroduce one here.
__all__ = ["accept_url_input"]
