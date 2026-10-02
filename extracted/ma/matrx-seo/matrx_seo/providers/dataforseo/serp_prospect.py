"""DataForSEO Google organic SERP → prospecting observations.

The SECOND prospecting method (outreach WP2): who already ranks for the
campaign's queries — keyword lists, guest-post footprints, resource pages,
listicles, and last-24-hours news — is who is worth writing to.

**Why this is not the rank-tracking path.** ``seo.serp_snapshot`` requires a
``keyword_id`` into the UNIVERSAL keyword plane, and a prospecting query is an
operator string (``dentist intitle:resources "write for us"``), not a keyword.
This normalizer therefore produces :class:`SerpProspectObservation` — evidence
aggregated by registrable domain — and never touches keyword identity.

**The tag is the contract.** Each submitted task carries a provider-echoed
``tag`` (``encode_prospect_tag``) naming the variant, the seed keyword, and the
domain to exclude (our own site). The tag is what lets the normalizer read the
response without any side-channel — a resumed run normalizes identically
because the mapping rides inside the provider payload itself. A task WITHOUT
the marker refuses loudly: ordinary DataForSEO SERP rank tracking has no
canonical normalizer yet, and silently treating a rank check as prospecting
would be worse than the current explicit NotImplementedError.

This module is a pure normalizer: dict in, contracts out. No DB, no network.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

from ...contracts import (
    SerpProspectDomainItem,
    SerpProspectMentionItem,
    SerpProspectObservation,
)

SERP_ORGANIC_OPERATION = "serp.google.organic.advanced"

#: The provider echoes ``tag`` verbatim (≤255 chars). ``|`` never appears in a
#: variant name, and seed keywords / domains have ``|`` stripped on encode.
_TAG_PREFIX = "matrx_prospect"

#: Result item types worth prospecting from. Everything else on an advanced
#: SERP (ads, related searches, people-also-ask) is either paid placement or
#: not a site at all.
PROSPECT_RESULT_TYPES = frozenset({"organic", "featured_snippet", "news_search"})


def encode_prospect_tag(*, variant: str, seed_keyword: str, exclude_domain: str) -> str:
    parts = [
        _TAG_PREFIX,
        variant.replace("|", " ").strip(),
        seed_keyword.replace("|", " ").strip(),
        exclude_domain.replace("|", " ").strip().lower(),
    ]
    tag = "|".join(parts)
    if len(tag) > 255:
        raise ValueError(f"prospect tag exceeds the provider's 255-char limit: {tag!r}")
    return tag


def decode_prospect_tag(tag: object) -> tuple[str, str, str] | None:
    """``(variant, seed_keyword, exclude_domain)`` or ``None`` if not ours."""
    if not isinstance(tag, str) or not tag.startswith(_TAG_PREFIX + "|"):
        return None
    parts = tag.split("|")
    if len(parts) != 4:
        raise ValueError(f"malformed prospect tag: {tag!r}")
    return parts[1], parts[2], parts[3]


def is_prospect_payload(raw: dict[str, Any] | list[Any]) -> bool:
    """True when every task in the payload carries the prospect tag."""
    if not isinstance(raw, dict):
        return False
    tasks = raw.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return False
    for task in tasks:
        if not isinstance(task, dict):
            return False
        data = task.get("data")
        tag = data.get("tag") if isinstance(data, dict) else None
        if decode_prospect_tag(tag) is None:
            return False
    return True


def normalize_serp_prospect_payload(
    *,
    raw: dict[str, Any],
    site_id: str,
    fetched_at: datetime,
) -> list[SerpProspectObservation]:
    """Turn one (multi-task) SERP payload into ONE prospect observation.

    Aggregates across every task by registrable domain. Raises on a payload
    without the documented envelope — a silently-empty prospect list would read
    as "nobody ranks for your topics", a lie the user cannot see through.
    """
    if not site_id.strip():
        raise ValueError("site_id must be nonblank")
    tasks = raw.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("DataForSEO SERP payload tasks must be a non-empty list")

    by_domain: dict[str, dict[str, Any]] = {}
    queries: list[str] = []
    excluded: set[str] = set()
    failed_tasks: list[dict[str, Any]] = []
    empty_queries: list[str] = []

    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("DataForSEO SERP tasks must contain objects")
        data = task.get("data")
        tag_parts = decode_prospect_tag(data.get("tag") if isinstance(data, dict) else None)
        if tag_parts is None:
            raise NotImplementedError(
                "DataForSEO organic SERP has no canonical rank-tracking "
                "normalizer; only prospect-tagged tasks (serp_prospecting.py) "
                "normalize. Use Brave or SerpAPI for rank collection."
            )
        variant, seed_keyword, exclude_domain = tag_parts
        if exclude_domain:
            excluded.add(exclude_domain)
        query = str(data.get("keyword") or "").strip() if isinstance(data, dict) else ""
        if not query:
            raise ValueError("prospect SERP task carries no keyword")
        queries.append(query)

        status_code = task.get("status_code")
        if status_code == 40102:
            # "No Search Results." — the search RAN and nobody ranks for this
            # query (common for hot-off-press: a niche topic in a 24h window).
            # A correct empty answer, recorded as such, never a failure.
            empty_queries.append(query)
            continue
        if status_code != 20000:
            failed_tasks.append(
                {
                    "query": query,
                    "status_code": status_code,
                    "status_message": task.get("status_message"),
                }
            )
            continue
        results = task.get("result")
        if not isinstance(results, list):
            raise ValueError("DataForSEO SERP task.result must be a list")
        for result in results:
            if not isinstance(result, dict):
                raise ValueError("DataForSEO SERP task.result must contain objects")
            items = result.get("items") or []
            if not isinstance(items, list):
                raise ValueError("DataForSEO SERP result.items must be a list")
            for item in items:
                if not isinstance(item, dict):
                    continue
                if str(item.get("type") or "") not in PROSPECT_RESULT_TYPES:
                    continue
                url = str(item.get("url") or "").strip()
                domain = str(item.get("domain") or "").strip().lower()
                if not domain and url:
                    domain = (urlparse(url).netloc or "").lower()
                domain = domain.split("@")[-1].split(":")[0].removeprefix("www.").rstrip(".")
                if not url or not domain or "." not in domain:
                    continue
                if domain in excluded:
                    continue
                mention = SerpProspectMentionItem(
                    query=query,
                    variant=variant,
                    seed_keyword=seed_keyword or None,
                    url=url,
                    title=_optional_str(item.get("title")),
                    snippet=_optional_str(item.get("description")),
                    rank=_optional_int(item.get("rank_absolute")),
                    result_type=str(item.get("type") or "organic"),
                    extras={
                        key: item[key]
                        for key in ("rank_group", "breadcrumb", "timestamp")
                        if item.get(key) is not None
                    },
                )
                bucket = by_domain.setdefault(
                    domain,
                    {"display": domain, "mentions": [], "queries": set(), "variants": set()},
                )
                bucket["mentions"].append(mention)
                bucket["queries"].add(query)
                bucket["variants"].add(variant)

    if failed_tasks and not by_domain and not empty_queries:
        raise ValueError(f"every prospect SERP task failed; first: {failed_tasks[0]!r}")

    domains = [
        SerpProspectDomainItem(
            normalized_domain=domain,
            display_domain=bucket["display"],
            mention_count=len(bucket["queries"]),
            best_rank=min(
                (m.rank for m in bucket["mentions"] if m.rank is not None),
                default=None,
            ),
            variants=sorted(bucket["variants"]),
            mentions=bucket["mentions"],
        )
        for domain, bucket in by_domain.items()
    ]
    # Most-mentioned first, then best rank — a stable, explainable default
    # order before authority enrichment lands.
    domains.sort(
        key=lambda d: (-d.mention_count, d.best_rank if d.best_rank is not None else 10_000)
    )

    observed_at = fetched_at if fetched_at.tzinfo else fetched_at.replace(tzinfo=UTC)
    return [
        SerpProspectObservation(
            site_id=site_id,
            queries=sorted(set(queries)),
            excluded_domains=sorted(excluded),
            observed_at=observed_at.astimezone(UTC),
            domains=domains,
            extras={
                **({"failed_tasks": failed_tasks} if failed_tasks else {}),
                **({"empty_queries": empty_queries} if empty_queries else {}),
            },
        )
    ]


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


__all__ = [
    "PROSPECT_RESULT_TYPES",
    "SERP_ORGANIC_OPERATION",
    "decode_prospect_tag",
    "encode_prospect_tag",
    "is_prospect_payload",
    "normalize_serp_prospect_payload",
]
