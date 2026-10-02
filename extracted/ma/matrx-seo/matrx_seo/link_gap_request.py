"""Shared request shaping for both DataForSEO intersection endpoints.

`domain_intersection` and `page_intersection` take the SAME request shape and
differ only in what a "target" is (a domain vs a page URL) and in what the
per-competitor metric fields are called. Everything else — the numbered target
map, the provider-side limits, the spam filter, the ordering — is one contract,
so it lives here once rather than being written twice and drifting.

🚨 **Never ship the provider's default ordering.** A real probe on 2026-08-14
returned `livelycity.com`, `usindex.app`, `intently.co`, `z1biz.com` as the top
gap domains — link-farm shaped, every one. The default order is effectively
random with respect to value, so an unordered, unfiltered run hands a
non-technical user a page of spam and tells them these are their best
opportunities. Order by rank and filter by spam score, always.
"""

from __future__ import annotations

from typing import Any

#: DataForSEO accepts at most 20 entries in the numbered `targets` map.
MAX_INTERSECTION_TARGETS = 20
#: ...and at most 10 in `exclude_targets`.
MAX_EXCLUDE_TARGETS = 10

#: Per-competitor field names differ between the two endpoints. Ordering and
#: filtering are expressed against the NUMBERED prefix of these names, so the
#: caller must pass the pair that matches the endpoint it is calling.
DOMAIN_RANK_FIELD = "rank"
DOMAIN_SPAM_FIELD = "backlinks_spam_score"
PAGE_RANK_FIELD = "domain_from_rank"
PAGE_SPAM_FIELD = "backlink_spam_score"


def numbered_targets(values: list[str]) -> dict[str, str]:
    """Build the numbered target map, preserving order and rejecting overflow.

    The numbered KEY is the only thing in the entire response that identifies
    which competitor a row belongs to, so this map is evidence, not formatting.
    """
    if not values:
        raise ValueError("an intersection needs at least one target")
    if len(values) != len(set(values)):
        raise ValueError("intersection targets must be unique")
    if len(values) > MAX_INTERSECTION_TARGETS:
        raise ValueError(
            f"DataForSEO accepts at most {MAX_INTERSECTION_TARGETS} intersection "
            f"targets; received {len(values)}"
        )
    return {str(index): value for index, value in enumerate(values, start=1)}


def spam_score_filter(target_count: int, max_spam_score: int, *, field: str) -> list[Any]:
    """Keep a referring domain if ANY competitor's link from it is clean enough.

    `or` rather than `and` on purpose: a domain that links to four competitors
    cleanly and to a fifth through a junk page is still a real opportunity, and
    an `and` would silently discard it.
    """
    if target_count < 1:
        raise ValueError("spam filter needs at least one target")
    clauses: list[Any] = []
    for index in range(1, target_count + 1):
        if clauses:
            clauses.append("or")
        clauses.append([f"{index}.{field}", "<=", max_spam_score])
    return clauses


def rank_order_by(field: str) -> list[str]:
    """Order by the first competitor's rank, descending — never the default."""
    return [f"1.{field},desc"]


__all__ = [
    "DOMAIN_RANK_FIELD",
    "DOMAIN_SPAM_FIELD",
    "MAX_EXCLUDE_TARGETS",
    "MAX_INTERSECTION_TARGETS",
    "PAGE_RANK_FIELD",
    "PAGE_SPAM_FIELD",
    "numbered_targets",
    "rank_order_by",
    "spam_score_filter",
]
