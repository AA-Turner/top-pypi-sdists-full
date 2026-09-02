"""
Deterministic page-audit evaluators — social share card, heading structure,
and indexability verdict. The CANONICAL Python implementation.

EXACT mirror of the TypeScript implementation in matrx-frontend
`features/marketing/seo/audit/` (social.ts / headings.ts / indexability.ts / stored.ts)
— evaluation logic, thresholds, URL normalization, AND issue strings are
byte-identical, so an audit computed by the scraper at crawl time and one
computed in the browser are always the same. Change ANY value here → make the
same change there in the same unit of work and regenerate the parity fixtures
(`features/marketing/seo/audit/audit.parity.test.ts`).

Persisted contract: ``web.snapshot.audit_metrics`` (v1), stamped by
``CanonicalBodyPersister`` on every capture via ``build_stored_audit_metrics``.
"""

import re
from datetime import datetime, UTC
from urllib.parse import urlsplit

SOCIAL_TITLE_MAX_CHARS = 70
SOCIAL_DESCRIPTION_MAX_CHARS = 200
KNOWN_TWITTER_CARDS = ("summary", "summary_large_image", "app", "player")
HEADING_MAX_CHARS = 70


def _clean(value) -> str | None:
    """Trim a raw tag value; empty/whitespace/non-string → None."""
    if not isinstance(value, str):
        return None
    trimmed = value.strip()
    return trimmed if trimmed else None


# ---------------------------------------------------------------------------
# Social share card
# ---------------------------------------------------------------------------


def _resolve(og_value: str | None, twitter_value: str | None) -> tuple[str | None, str | None]:
    if og_value:
        return og_value, "og"
    if twitter_value:
        return twitter_value, "twitter"
    return None, None


def evaluate_social_card(og_tags: dict, twitter_tags: dict) -> dict:
    """
    Evaluate Open Graph + Twitter card metadata. Inputs are the RAW tag
    records (keys like "og:title", "twitter:card") exactly as persisted in
    ``head_tags.og`` / ``head_tags.twitter``.
    """
    og_title = _clean(og_tags.get("og:title"))
    og_description = _clean(og_tags.get("og:description"))
    og_image = _clean(og_tags.get("og:image"))
    og_site_name = _clean(og_tags.get("og:site_name"))
    og_url = _clean(og_tags.get("og:url"))
    og_type = _clean(og_tags.get("og:type"))
    twitter_card = _clean(twitter_tags.get("twitter:card"))
    twitter_title = _clean(twitter_tags.get("twitter:title"))
    twitter_description = _clean(twitter_tags.get("twitter:description"))
    twitter_image = _clean(twitter_tags.get("twitter:image"))

    title, title_source = _resolve(og_title, twitter_title)
    description, description_source = _resolve(og_description, twitter_description)
    image, image_source = _resolve(og_image, twitter_image)
    title_length = len(title) if title else 0
    description_length = len(description) if description else 0

    issues: list[dict] = []
    if not title:
        issues.append(
            {
                "severity": "error",
                "message": "No social title — add og:title (or twitter:title) so shares don't render as a bare link",
            }
        )
    if not image:
        issues.append(
            {
                "severity": "error",
                "message": "No share image — add og:image (or twitter:image); image posts get dramatically higher engagement",
            }
        )
    if not description:
        issues.append(
            {
                "severity": "warning",
                "message": "No social description — add og:description (or twitter:description)",
            }
        )
    if not twitter_card:
        issues.append(
            {
                "severity": "warning",
                "message": "No twitter:card tag — X falls back to a small summary card",
            }
        )
    elif twitter_card not in KNOWN_TWITTER_CARDS:
        issues.append(
            {
                "severity": "warning",
                "message": f'Unknown twitter:card value "{twitter_card}" — expected summary, summary_large_image, app, or player',
            }
        )
    if title_length > SOCIAL_TITLE_MAX_CHARS:
        issues.append(
            {
                "severity": "warning",
                "message": f"Social title is long ({title_length} chars) — platforms truncate around {SOCIAL_TITLE_MAX_CHARS}",
            }
        )
    if description_length > SOCIAL_DESCRIPTION_MAX_CHARS:
        issues.append(
            {
                "severity": "warning",
                "message": f"Social description is long ({description_length} chars) — platforms truncate around {SOCIAL_DESCRIPTION_MAX_CHARS}",
            }
        )
    if not og_url:
        issues.append(
            {
                "severity": "warning",
                "message": "No og:url — platforms may mis-attribute the canonical link",
            }
        )
    if not og_type:
        issues.append(
            {
                "severity": "warning",
                "message": 'No og:type — defaults to "website" on most platforms',
            }
        )
    if image and image.startswith("http://"):
        issues.append(
            {
                "severity": "warning",
                "message": "Share image is not HTTPS — many platforms refuse mixed-content images",
            }
        )

    return {
        "ok": all(issue["severity"] != "error" for issue in issues),
        "title": title,
        "title_source": title_source,
        "title_length": title_length,
        "description": description,
        "description_source": description_source,
        "description_length": description_length,
        "image": image,
        "image_source": image_source,
        "site_name": og_site_name,
        "url": og_url,
        "og_type": og_type,
        "card_type": twitter_card,
        "has_image": bool(image),
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Heading structure
# ---------------------------------------------------------------------------


def evaluate_heading_structure(headings: list[dict]) -> dict:
    """Evaluate a document-ordered outline of ``{"text", "level"}`` entries."""
    entries = [
        {
            "text": entry.get("text") if isinstance(entry.get("text"), str) else "",
            "level": entry.get("level"),
        }
        for entry in headings
        if isinstance(entry, dict)
        and isinstance(entry.get("level"), int)
        and 1 <= entry.get("level") <= 6
    ]
    total = len(entries)
    h1_count = sum(1 for entry in entries if entry["level"] == 1)
    first_level = entries[0]["level"] if entries else None
    empty_count = sum(1 for entry in entries if not entry["text"].strip())
    long_count = sum(1 for entry in entries if len(entry["text"].strip()) > HEADING_MAX_CHARS)
    skipped_levels = 0
    for i in range(1, len(entries)):
        if entries[i]["level"] > entries[i - 1]["level"] + 1:
            skipped_levels += 1

    issues: list[dict] = []
    if total == 0:
        issues.append(
            {
                "severity": "error",
                "message": "No headings at all — the page has no structural outline",
            }
        )
    elif h1_count == 0:
        issues.append(
            {
                "severity": "error",
                "message": "No H1 heading — every page needs exactly one H1",
            }
        )
    if h1_count > 1:
        issues.append(
            {
                "severity": "warning",
                "message": f"{h1_count} H1 headings — expected exactly 1",
            }
        )
    if first_level is not None and first_level != 1:
        issues.append(
            {
                "severity": "warning",
                "message": f"First heading is an H{first_level} — pages should open with the H1",
            }
        )
    if skipped_levels > 0:
        issues.append(
            {
                "severity": "warning",
                "message": f"{skipped_levels} skipped heading level(s) (e.g. an H2 followed by an H4)",
            }
        )
    if empty_count > 0:
        issues.append(
            {
                "severity": "warning",
                "message": f"{empty_count} empty heading(s) — remove or fill them",
            }
        )
    if long_count > 0:
        issues.append(
            {
                "severity": "warning",
                "message": f"{long_count} heading(s) longer than {HEADING_MAX_CHARS} characters",
            }
        )

    return {
        "ok": all(issue["severity"] != "error" for issue in issues),
        "total": total,
        "h1_count": h1_count,
        "first_level": first_level,
        "skipped_levels": skipped_levels,
        "empty_count": empty_count,
        "long_count": long_count,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# URL quality
# ---------------------------------------------------------------------------

URL_MAX_CHARS = 100
URL_MAX_DEPTH = 4


def evaluate_url_quality(url: str) -> dict:
    """
    Deterministic checks on the URL string itself. Warnings only — a URL
    never blocks indexing by shape alone — so ``ok`` means "no issues" for
    this section. Mirror of TS `evaluateUrlQuality`.
    """
    trimmed = url.strip()
    length = len(trimmed)

    parts = urlsplit(trimmed)
    if parts.scheme and parts.hostname:
        path = parts.path
        query = f"?{parts.query}" if parts.query else ""
        fragment = f"#{parts.fragment}" if parts.fragment else ""
    else:
        path = trimmed
        query = ""
        fragment = ""

    segments = [segment for segment in path.split("/") if segment]
    depth = len(segments)
    has_uppercase = bool(re.search(r"[A-Z]", path))
    has_underscore = "_" in path
    has_query = len(query) > 1
    has_fragment = len(fragment) > 1
    has_encoded_chars = bool(re.search(r"%[0-9A-Fa-f]{2}", path))
    has_double_slash = "//" in path

    issues: list[dict] = []
    if length > URL_MAX_CHARS:
        issues.append(
            {
                "severity": "warning",
                "message": f"URL is long ({length} chars) — keep URLs under {URL_MAX_CHARS} characters",
            }
        )
    if depth > URL_MAX_DEPTH:
        issues.append(
            {
                "severity": "warning",
                "message": f"URL is {depth} levels deep — content buried past {URL_MAX_DEPTH} levels reads as less important",
            }
        )
    if has_uppercase:
        issues.append(
            {
                "severity": "warning",
                "message": "URL path contains uppercase letters — mixed case creates duplicate-URL risk",
            }
        )
    if has_underscore:
        issues.append(
            {
                "severity": "warning",
                "message": "URL path contains underscores — Google treats hyphens as word separators, underscores as joiners",
            }
        )
    if has_query:
        issues.append(
            {
                "severity": "warning",
                "message": "URL carries query parameters — parameterized URLs fragment crawl equity and analytics",
            }
        )
    if has_fragment:
        issues.append(
            {
                "severity": "warning",
                "message": "URL carries a #fragment — fragments are ignored by crawlers",
            }
        )
    if has_encoded_chars:
        issues.append(
            {
                "severity": "warning",
                "message": "URL path contains percent-encoded characters — prefer plain lowercase ASCII slugs",
            }
        )
    if has_double_slash:
        issues.append(
            {
                "severity": "warning",
                "message": "URL path contains a double slash — usually a link-building bug",
            }
        )

    return {
        "ok": len(issues) == 0,
        "length": length,
        "depth": depth,
        "has_uppercase": has_uppercase,
        "has_underscore": has_underscore,
        "has_query": has_query,
        "has_fragment": has_fragment,
        "has_encoded_chars": has_encoded_chars,
        "has_double_slash": has_double_slash,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Indexability
# ---------------------------------------------------------------------------


def _normalize_url_for_comparison(url: str) -> str:
    """Mirror of TS `normalizeUrlForComparison`."""
    trimmed = url.strip()
    parts = urlsplit(trimmed)
    if not parts.scheme or not parts.hostname:
        return trimmed
    scheme = parts.scheme.lower()
    host = parts.hostname.lower()
    port = ""
    if parts.port is not None and not (
        (scheme == "https" and parts.port == 443) or (scheme == "http" and parts.port == 80)
    ):
        port = f":{parts.port}"
    path = parts.path
    if path.endswith("/"):
        path = path[:-1]
    query = f"?{parts.query}" if parts.query else ""
    return f"{scheme}://{host}{port}{path}{query}"


def _robots_tokens(meta_robots: str | None) -> list[str]:
    if not meta_robots:
        return []
    return [token.strip() for token in meta_robots.lower().split(",") if token.strip()]


def evaluate_indexability(
    http_status: int | None,
    meta_robots: str | None,
    canonical_url: str | None,
    redirect_chain: list[dict],
    final_url: str | None,
) -> dict:
    tokens = _robots_tokens(meta_robots)
    noindex = "noindex" in tokens or "none" in tokens
    nofollow = "nofollow" in tokens or "none" in tokens
    redirect_hops = max(0, len(redirect_chain) - 1)
    if canonical_url and final_url:
        canonical_matches = _normalize_url_for_comparison(
            canonical_url
        ) == _normalize_url_for_comparison(final_url)
    else:
        canonical_matches = None

    issues: list[dict] = []
    if http_status is not None and http_status >= 400:
        issues.append(
            {
                "severity": "error",
                "message": f"Page returns HTTP {http_status}",
            }
        )
    if noindex:
        issues.append(
            {
                "severity": "error",
                "message": "Meta robots contains noindex — Google is told not to index this page",
            }
        )
    if nofollow:
        issues.append(
            {
                "severity": "warning",
                "message": "Meta robots contains nofollow — links on this page pass no equity",
            }
        )
    if canonical_matches is False:
        issues.append(
            {
                "severity": "warning",
                "message": f"Canonical points elsewhere ({canonical_url}) — Google may index that URL instead",
            }
        )
    if redirect_hops > 0:
        issues.append(
            {
                "severity": "warning",
                "message": f"URL redirects through {redirect_hops} hop(s) before resolving",
            }
        )
    if http_status is None:
        issues.append(
            {
                "severity": "warning",
                "message": "HTTP status was not captured",
            }
        )

    has_error = any(issue["severity"] == "error" for issue in issues)
    verdict = "blocked" if has_error else ("check" if issues else "indexable")

    return {
        "ok": verdict == "indexable",
        "verdict": verdict,
        "http_status": http_status,
        "noindex": noindex,
        "nofollow": nofollow,
        "canonical_url": canonical_url,
        "canonical_matches": canonical_matches,
        "redirect_hops": redirect_hops,
        "final_url": final_url,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Persisted payload (contract v1)
# ---------------------------------------------------------------------------


def build_stored_audit_metrics(
    *,
    og_tags: dict,
    twitter_tags: dict,
    headings: list[dict],
    http_status: int | None,
    meta_robots: str | None,
    canonical_url: str | None,
    redirect_chain: list[dict],
    final_url: str | None,
    url: str | None = None,
    source: str = "scraper",
) -> dict:
    """The canonical ``web.snapshot.audit_metrics`` payload (contract v1).

    ``url`` is the canonical page URL; the url section is warnings-only and
    deliberately excluded from ``overall_ok``.
    """
    social = evaluate_social_card(og_tags or {}, twitter_tags or {})
    heading_metrics = evaluate_heading_structure(headings or [])
    indexability = evaluate_indexability(
        http_status, meta_robots, canonical_url, redirect_chain or [], final_url
    )
    payload = {
        "v": 1,
        "source": source,
        "computed_at": datetime.now(UTC).isoformat(),
        "social": social,
        "headings": heading_metrics,
        "indexability": indexability,
        "overall_ok": social["ok"] and heading_metrics["ok"] and indexability["ok"],
    }
    if url:
        payload["url"] = evaluate_url_quality(url)
    return payload
