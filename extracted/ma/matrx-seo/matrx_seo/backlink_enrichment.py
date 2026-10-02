"""Stable backlink identities and zero-token enrichment primitives.

Provider observations remain immutable history.  This module projects them
onto ``seo.backlink`` (one source-page -> target-page relationship) and
``seo.referring_domain_profile`` (one known referring domain per managed
site), then supplies the deterministic first rung and durable item-state
writers consumed by aidream's crawl/AI orchestrator.

The package deliberately owns no scraper or AI dependency.  A standalone
consumer can persist and score provider evidence; a host chooses how to fill
``source_capture`` and ``ai_assessment``.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, Literal
from uuid import uuid4

from matrx_orm.core.expressions import Coalesce, Excluded, F, Greatest, JsonbConcat, Least, Now
from matrx_orm.operations.conflict_writes import bulk_upsert_increment
from matrx_utils.quality_engine import QualityVector, compute_composite_quality, to_visible_score
from pydantic import BaseModel, ConfigDict, Field

from .contracts import BacklinkItem
from .db import models_seo as m
from .db.models_host import WebPage
from .rank_matching import canonicalize_domain, canonicalize_rank_url

ASSESSMENT_VERSION = "backlink-provider-v1"
MAX_ENRICHMENT_ATTEMPTS = 4
ITEM_LEASE_MINUTES = 15


class ScoreComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int = Field(ge=0, le=100)
    evidence: list[str] = Field(default_factory=list)


class DeterministicBacklinkAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = ASSESSMENT_VERSION
    page_type_guess: str
    control_likelihood: Literal["direct", "likely", "possible", "unlikely", "unknown"]
    control_reason: str
    recommended_action: str
    action_reason: str
    priority: Literal["high", "medium", "low"]
    quality_components: dict[str, ScoreComponent]
    quality_vector: dict[str, int]
    overall_score: int = Field(ge=0, le=100)
    risks: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    provider_only: bool = True


class EnrichmentQueueSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int = 0
    pending: int = 0
    in_progress: int = 0
    completed: int = 0
    failed: int = 0
    dead_letter: int = 0


def backlink_identity_key(site_id: str, source_url: str, target_url: str) -> str:
    """Stable canonical source-page -> target-page relationship identity.

    Providers commonly return the same physical placement under URL aliases
    (http/https, www/non-www, a trailing slash, reordered query parameters, or
    a fragment).  Those are presentation variants, not distinct backlinks.
    Path case and semantic query parameters remain significant because they can
    identify genuinely different resources.
    """

    canonical_source = canonicalize_rank_url(source_url) or source_url.strip()
    canonical_target = canonicalize_rank_url(target_url) or target_url.strip()
    raw = f"{site_id.strip()}\n{canonical_source}\n{canonical_target}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _merge_duplicate_backlink_items(items: Sequence[BacklinkItem]) -> BacklinkItem:
    """Collapse provider aliases without throwing away their strongest facts."""

    if not items:
        raise ValueError("cannot merge an empty backlink item group")
    epoch = datetime.min.replace(tzinfo=UTC)
    latest = max(items, key=lambda item: item.last_seen_at or epoch)
    extras: dict[str, Any] = {}
    for item in sorted(items, key=lambda value: value.last_seen_at or epoch):
        extras.update(_extras(item))
    extras["provider_url_variants"] = sorted(
        {f"{item.source_url.strip()} -> {item.target_url.strip()}" for item in items}
    )

    def earliest(values: Sequence[datetime | None]) -> datetime | None:
        present = [value for value in values if value is not None]
        return min(present) if present else None

    def latest_value(values: Sequence[datetime | None]) -> datetime | None:
        present = [value for value in values if value is not None]
        return max(present) if present else None

    def strongest(values: Sequence[Decimal | None]) -> Decimal | None:
        present = [value for value in values if value is not None]
        return max(present) if present else None

    return latest.model_copy(
        update={
            "source_domain": latest.source_domain or canonicalize_domain(latest.source_url),
            "anchor_text": latest.anchor_text
            or next((item.anchor_text for item in items if item.anchor_text), None),
            "link_type": latest.link_type
            or next((item.link_type for item in items if item.link_type), None),
            "is_dofollow": (
                latest.is_dofollow
                if latest.is_dofollow is not None
                else next(
                    (item.is_dofollow for item in items if item.is_dofollow is not None),
                    None,
                )
            ),
            "first_seen_at": earliest([item.first_seen_at for item in items]),
            "last_seen_at": latest_value([item.last_seen_at for item in items]),
            "lost_at": latest_value([item.lost_at for item in items]),
            "source_rank": strongest([item.source_rank for item in items]),
            "domain_rank": strongest([item.domain_rank for item in items]),
            "spam_score": strongest([item.spam_score for item in items]),
            "extras": extras,
        }
    )


async def resolve_backlink_target_page_ids(
    site_id: str,
    items: Sequence[BacklinkItem],
) -> dict[str, str]:
    """Resolve each provider target URL to its canonical ``web.page`` identity."""

    if not items:
        return {}
    page_rows = await WebPage.filter(site_id=site_id).values("id", "url")
    page_by_url: dict[str, tuple[tuple[int, str, str], str]] = {}
    for row in page_rows:
        raw_url = str(row["url"])
        canonical_url = canonicalize_rank_url(raw_url)
        if not canonical_url:
            continue
        lowered_url = raw_url.lower()
        preference = (
            0
            if lowered_url.startswith("https://") and not lowered_url.startswith("https://www.")
            else 1
            if lowered_url.startswith("https://")
            else 2
            if not lowered_url.startswith("http://www.")
            else 3,
            raw_url,
            str(row["id"]),
        )
        prior = page_by_url.get(canonical_url)
        if prior is None or preference < prior[0]:
            page_by_url[canonical_url] = (preference, str(row["id"]))

    resolved: dict[str, str] = {}
    for item in items:
        page = page_by_url.get(canonicalize_rank_url(item.target_url))
        if page:
            resolved[backlink_identity_key(site_id, item.source_url, item.target_url)] = page[1]
    return resolved


def _extras(item: BacklinkItem) -> dict[str, Any]:
    return item.extras if isinstance(item.extras, dict) else {}


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float | Decimal):
        return float(value)
    return None


def _rank_score(value: Any, *, neutral: int = 45) -> int:
    number = _number(value)
    if number is None:
        return neutral
    # DataForSEO rank values may be supplied on either a 0-100 or 0-1000
    # scale.  Preserve the former; normalize the latter.
    return round(max(0.0, min(100.0, number / 10.0 if number > 100 else number)))


def _page_type(item: BacklinkItem) -> str:
    extras = _extras(item)
    platforms = extras.get("domain_from_platform_type")
    platform_text = (
        " ".join(str(value) for value in platforms) if isinstance(platforms, list) else ""
    )
    haystack = " ".join(
        (
            item.source_url,
            str(extras.get("page_from_title") or ""),
            platform_text,
        )
    ).lower()
    rules = (
        ("directory", r"\b(directory|listing|citations?|yellowpages|clutch|yelp)\b"),
        ("press_release", r"\b(press[- ]release|newswire|prnews)\b"),
        ("forum", r"\b(forum|community|thread|reddit|quora)\b"),
        ("profile", r"\b(profile|author|member|bio)\b"),
        ("resource", r"\b(resources?|useful[- ]links?|partners?)\b"),
        ("news", r"\b(news|journal|magazine|story)\b"),
        ("blog_or_article", r"\b(blog|article|post|guide|how[- ]to)\b"),
        ("social", r"\b(facebook|linkedin|instagram|youtube|x\.com|twitter)\b"),
    )
    for label, pattern in rules:
        if re.search(pattern, haystack):
            return label
    return "unknown"


def deterministic_assessment(item: BacklinkItem) -> DeterministicBacklinkAssessment:
    """Score only facts already present in provider evidence.

    This is intentionally explicit about its ceiling: it does not claim page
    relevance or editorial quality until the source page has been captured.
    """

    extras = _extras(item)
    attributes = {
        str(value).lower() for value in (extras.get("attributes") or []) if isinstance(value, str)
    }
    placement = str(extras.get("semantic_location") or "").lower()
    page_type = _page_type(item)
    domain_strength = _rank_score(item.domain_rank)
    page_strength = _rank_score(item.source_rank)
    spam = _number(item.spam_score)
    source_quality = round(
        max(0, min(100, (domain_strength * 0.65) + (page_strength * 0.35) - ((spam or 0) * 0.4)))
    )

    context_present = bool(
        item.anchor_text or extras.get("text_pre") or extras.get("text_post") or extras.get("alt")
    )
    alignment = 58 if context_present else 35
    if placement in {"article", "main", "section"}:
        alignment += 12
    if placement in {"footer", "aside", "header"}:
        alignment -= 10
    alignment = max(0, min(100, alignment))

    faithfulness = 55 if context_present else 35
    coverage = 70 if placement in {"article", "main", "section"} else 50
    if item.is_dofollow is True:
        coverage += 10
    if "sponsored" in attributes or "ugc" in attributes:
        coverage -= 10
    coverage = max(0, min(100, coverage))

    capture_quality = 20  # provider snippets are evidence, not a page capture
    utility_value = 55
    risks: list[str] = []
    opportunities: list[str] = []

    broken = (
        extras.get("is_broken") is True or (_number(extras.get("url_to_status_code")) or 0) >= 400
    )
    generic_anchor = (item.anchor_text or "").strip().lower() in {
        "",
        "click here",
        "here",
        "website",
        "learn more",
        "read more",
    }
    if broken:
        action = "fix_or_redirect_target"
        action_reason = (
            "The provider reports a broken destination; recover the existing link "
            "before pursuing a new one."
        )
        priority: Literal["high", "medium", "low"] = "high"
        utility_value = 90
        risks.append("broken_target")
    elif item.state == "lost":
        action = "reclaim_lost_link"
        action_reason = (
            "The link is no longer live; confirm the source change and request "
            "restoration when warranted."
        )
        priority = "high"
        utility_value = 85
        opportunities.append("link_reclamation")
    elif page_type in {"directory", "profile"}:
        action = "claim_or_improve_listing"
        action_reason = (
            "The source pattern looks like a listing or profile that may be "
            "directly claimable or editable."
        )
        priority = "medium"
        utility_value = 80
        opportunities.append("listing_enrichment")
    elif generic_anchor:
        action = "improve_anchor_or_context"
        action_reason = (
            "The stored anchor is missing or generic; a contextual edit could make "
            "the link clearer and more useful."
        )
        priority = "medium"
        utility_value = 72
        opportunities.append("anchor_improvement")
    elif (spam or 0) >= 30:
        action = "review_link_risk"
        action_reason = (
            "The provider spam score crosses the review threshold; inspect the "
            "captured page before any removal or disavow decision."
        )
        priority = "medium"
        utility_value = 70
        risks.append("provider_spam_signal")
    else:
        action = "protect_and_monitor"
        action_reason = (
            "No provider-only defect is evident; capture the source page to validate "
            "relevance, placement, and editorial value."
        )
        priority = "low"
        opportunities.append("source_page_validation")

    control: Literal["direct", "likely", "possible", "unlikely", "unknown"]
    if page_type in {"directory", "profile", "social"}:
        control = "possible"
        control_reason = (
            "This page type often exposes a claim, account, or listing-edit path, "
            "but ownership is not yet proven."
        )
    elif page_type == "press_release":
        control = "possible"
        control_reason = (
            "Press-release placements are sometimes commissioned and correctable "
            "through the publisher."
        )
    else:
        control = "unknown"
        control_reason = (
            "Provider metadata does not establish who controls the referring page; "
            "crawl and human evidence are required."
        )

    vector = QualityVector.from_visible(
        source_quality=source_quality,
        capture_quality=capture_quality,
        faithfulness=faithfulness,
        alignment=alignment,
        coverage=coverage,
        utility_value=utility_value,
    )
    visible = vector.visible()
    overall = to_visible_score(compute_composite_quality(vector, "default"))
    components = {
        "source_quality": ScoreComponent(
            score=source_quality,
            evidence=[
                f"provider domain rank={item.domain_rank}",
                f"provider page rank={item.source_rank}",
                f"provider spam score={item.spam_score}",
            ],
        ),
        "capture_quality": ScoreComponent(
            score=capture_quality,
            evidence=["source page has not been captured yet"],
        ),
        "faithfulness": ScoreComponent(
            score=faithfulness,
            evidence=[
                "provider supplied surrounding context"
                if context_present
                else "no contextual excerpt stored"
            ],
        ),
        "alignment": ScoreComponent(
            score=alignment,
            evidence=[f"provider placement={placement or 'unknown'}"],
        ),
        "coverage": ScoreComponent(
            score=coverage,
            evidence=[f"dofollow={item.is_dofollow}", f"attributes={sorted(attributes)}"],
        ),
        "utility_value": ScoreComponent(score=utility_value, evidence=[action_reason]),
    }
    return DeterministicBacklinkAssessment(
        page_type_guess=page_type,
        control_likelihood=control,
        control_reason=control_reason,
        recommended_action=action,
        action_reason=action_reason,
        priority=priority,
        quality_components=components,
        quality_vector=visible,
        overall_score=overall,
        risks=risks,
        opportunities=opportunities,
    )


async def upsert_current_backlinks(
    *,
    organization_id: str,
    created_by: str,
    site_id: str,
    page_id: str | None,
    provider: str,
    snapshot_id: str,
    items: list[BacklinkItem],
) -> dict[str, str]:
    """Upsert directory + stable link rows and return ``identity_key -> id``."""

    if not items:
        return {}
    now = datetime.now(UTC)
    by_domain: dict[str, list[BacklinkItem]] = defaultdict(list)
    for item in items:
        domain = canonicalize_domain(item.source_domain or item.source_url)
        if domain:
            by_domain[domain].append(item)

    profile_rows: list[dict[str, Any]] = []
    for domain, domain_items in by_domain.items():
        profile_rows.append(
            {
                "id": str(uuid4()),
                "organization_id": organization_id,
                "created_by": created_by,
                "site_id": site_id,
                "normalized_domain": domain,
                "display_domain": domain,
                "first_seen_at": min(
                    (item.first_seen_at for item in domain_items if item.first_seen_at),
                    default=None,
                ),
                "last_seen_at": max(
                    (item.last_seen_at for item in domain_items if item.last_seen_at),
                    default=now,
                ),
                "current_backlinks": len(domain_items),
                "current_referring_pages": len({item.source_url for item in domain_items}),
                "provider_metrics": {
                    "provider": provider,
                    "domain_rank": max(
                        (
                            value
                            for item in domain_items
                            if (value := _number(item.domain_rank)) is not None
                        ),
                        default=None,
                    ),
                    "spam_score": max(
                        (
                            value
                            for item in domain_items
                            if (value := _number(item.spam_score)) is not None
                        ),
                        default=None,
                    ),
                    "snapshot_id": snapshot_id,
                },
                "created_at": now,
                "updated_at": now,
            }
        )
    profile_table = m.ReferringDomainProfile._meta.qualified_table_name
    profile_result = await bulk_upsert_increment(
        m.ReferringDomainProfile,
        profile_rows,
        on_conflict=["site_id", "normalized_domain"],
        set_fields={
            "display_domain": Excluded("display_domain"),
            "first_seen_at": Least(F(f"{profile_table}.first_seen_at"), Excluded("first_seen_at")),
            "last_seen_at": Greatest(F(f"{profile_table}.last_seen_at"), Excluded("last_seen_at")),
            "current_backlinks": Excluded("current_backlinks"),
            "current_referring_pages": Excluded("current_referring_pages"),
            "provider_metrics": JsonbConcat(
                F(f"{profile_table}.provider_metrics"), Excluded("provider_metrics")
            ),
            "updated_at": Now(),
        },
        returning=True,
    )
    profiles = {str(row["normalized_domain"]): str(row["id"]) for row in profile_result}

    # A provider can report duplicate physical placements with the same stable
    # source/target relationship.  Pre-merge so one ON CONFLICT statement never
    # tries to update the same row twice.
    items_by_key: dict[str, list[BacklinkItem]] = defaultdict(list)
    for item in items:
        key = backlink_identity_key(site_id, item.source_url, item.target_url)
        items_by_key[key].append(item)
    latest_by_key = {
        key: _merge_duplicate_backlink_items(group) for key, group in items_by_key.items()
    }

    target_page_ids = (
        {}
        if page_id is not None
        else await resolve_backlink_target_page_ids(site_id, list(latest_by_key.values()))
    )

    link_rows: list[dict[str, Any]] = []
    for key, item in latest_by_key.items():
        domain = canonicalize_domain(item.source_domain or item.source_url)
        assessment = deterministic_assessment(item).model_dump(mode="json")
        link_rows.append(
            {
                "id": str(uuid4()),
                "organization_id": organization_id,
                "created_by": created_by,
                "site_id": site_id,
                "page_id": page_id or target_page_ids.get(key),
                "referring_domain_profile_id": profiles.get(domain),
                "identity_key": key,
                "source_url": item.source_url,
                "source_domain": item.source_domain or domain,
                "target_url": item.target_url,
                "anchor_text": item.anchor_text,
                "link_type": item.link_type,
                "is_dofollow": item.is_dofollow,
                "first_seen_at": item.first_seen_at,
                "last_seen_at": item.last_seen_at,
                "lost_at": item.lost_at,
                "state": item.state,
                "source_rank": item.source_rank,
                "domain_rank": item.domain_rank,
                "spam_score": item.spam_score,
                "provider_evidence": {
                    "provider": provider,
                    "snapshot_id": snapshot_id,
                    "extras": item.extras,
                },
                "deterministic_assessment": assessment,
                "resolved_assessment": assessment,
                "assessment_version": ASSESSMENT_VERSION,
                "created_at": now,
                "updated_at": now,
            }
        )
    link_table = m.Backlink._meta.qualified_table_name
    link_result = await bulk_upsert_increment(
        m.Backlink,
        link_rows,
        on_conflict=["site_id", "identity_key"],
        set_fields={
            "page_id": Coalesce(Excluded("page_id"), F(f"{link_table}.page_id")),
            "referring_domain_profile_id": Coalesce(
                Excluded("referring_domain_profile_id"),
                F(f"{link_table}.referring_domain_profile_id"),
            ),
            "source_url": Excluded("source_url"),
            "source_domain": Excluded("source_domain"),
            "target_url": Excluded("target_url"),
            "anchor_text": Excluded("anchor_text"),
            "link_type": Excluded("link_type"),
            "is_dofollow": Excluded("is_dofollow"),
            "first_seen_at": Least(F(f"{link_table}.first_seen_at"), Excluded("first_seen_at")),
            "last_seen_at": Greatest(F(f"{link_table}.last_seen_at"), Excluded("last_seen_at")),
            "lost_at": Excluded("lost_at"),
            "state": Excluded("state"),
            "source_rank": Excluded("source_rank"),
            "domain_rank": Excluded("domain_rank"),
            "spam_score": Excluded("spam_score"),
            "provider_evidence": Excluded("provider_evidence"),
            "deterministic_assessment": Excluded("deterministic_assessment"),
            # AI/human/resolved evidence survives provider refreshes. The host
            # recomputes the resolved view when it completes the next analysis.
            "assessment_version": Excluded("assessment_version"),
            "updated_at": Now(),
        },
        returning=True,
    )
    return {str(row["identity_key"]): str(row["id"]) for row in link_result}


async def list_enrichment_candidates(
    site_id: str,
    *,
    limit: int,
    force: bool = False,
    backlink_ids: Sequence[str] | None = None,
) -> list[Any]:
    await reclaim_expired_enrichment_claims(site_id)
    now = datetime.now(UTC)
    statuses = ["pending", "failed", "completed"]
    if backlink_ids:
        requested_ids = list(dict.fromkeys(str(value) for value in backlink_ids))[:limit]
        targeted_statuses = [*statuses, "dead_letter"] if force else ["pending", "failed"]
        rows = await m.Backlink.filter(
            site_id=site_id,
            id__in=requested_ids,
            enrichment_status__in=targeted_statuses,
        ).all(use_cache=False)
        by_id = {str(row.id): row for row in rows}
        return [by_id[backlink_id] for backlink_id in requested_ids if backlink_id in by_id]
    if force:
        return await (
            m.Backlink.filter(site_id=site_id, enrichment_status__in=statuses)
            .order_by("-source_rank", "-domain_rank", "created_at", "id")
            .limit(limit)
            .all(use_cache=False)
        )

    # Keep NULL-new and timestamp-due work in separate queries. PostgreSQL puts
    # NULL last for ascending order, so one bounded mixed query could otherwise
    # fill with future completed rows and starve brand-new links indefinitely.
    fresh = await (
        m.Backlink.filter(
            site_id=site_id,
            enrichment_status__in=["pending", "failed"],
            next_enrichment_at__isnull=True,
        )
        .order_by("-source_rank", "-domain_rank", "created_at", "id")
        .limit(limit)
        .all(use_cache=False)
    )
    if len(fresh) >= limit:
        return fresh
    due = await (
        m.Backlink.filter(
            site_id=site_id,
            enrichment_status__in=statuses,
            next_enrichment_at__lte=now,
        )
        .order_by("next_enrichment_at", "-source_rank", "-domain_rank", "created_at", "id")
        .limit(limit - len(fresh))
        .all(use_cache=False)
    )
    return [*fresh, *due]


async def reclaim_expired_enrichment_claims(site_id: str, *, limit: int = 100) -> int:
    """Return abandoned capture/analysis leases to the durable queue.

    A process can disappear after a claim but before its failure handler. The
    lease is the recovery boundary: due work is made immediately eligible
    again, while an item that exhausted the attempt ceiling settles visibly as
    dead-letter instead of looping forever.
    """

    now = datetime.now(UTC)
    rows = await (
        m.Backlink.filter(
            site_id=site_id,
            enrichment_status__in=["capturing", "analyzing"],
            claim_expires_at__lte=now,
        )
        .order_by("claim_expires_at")
        .limit(limit)
        .all(use_cache=False)
    )
    for row in rows:
        dead = int(row.enrichment_attempt_count or 0) >= MAX_ENRICHMENT_ATTEMPTS
        await m.Backlink.update_where(
            {
                "id": str(row.id),
                "enrichment_status__in": ["capturing", "analyzing"],
                "claim_expires_at__lte": now,
            },
            enrichment_status="dead_letter" if dead else "failed",
            next_enrichment_at=None if dead else now,
            last_error={
                "stage": "lease_recovery",
                "message": "worker lease expired before enrichment settled",
            },
            claimed_by=None,
            claimed_at=None,
            claim_expires_at=None,
            updated_at=now,
        )
    return len(rows)


async def claim_enrichment_item(
    backlink_id: str,
    worker_id: str,
    *,
    force: bool = False,
) -> bool:
    now = datetime.now(UTC)
    statuses = ["pending", "failed", "completed"]
    if force:
        statuses.append("dead_letter")
    result = await m.Backlink.update_where(
        {"id": backlink_id, "enrichment_status__in": statuses},
        enrichment_status="capturing",
        enrichment_attempt_count=F("enrichment_attempt_count") + 1,
        claimed_by=worker_id,
        claimed_at=now,
        claim_expires_at=now + timedelta(minutes=ITEM_LEASE_MINUTES),
        last_error=None,
        updated_at=now,
    )
    return result.rows_affected == 1


async def mark_enrichment_analyzing(
    backlink_id: str,
    *,
    source_capture: dict[str, Any],
    deterministic: dict[str, Any],
) -> None:
    now = datetime.now(UTC)
    result = await m.Backlink.update_where(
        {"id": backlink_id, "enrichment_status": "capturing"},
        enrichment_status="analyzing",
        source_capture=source_capture,
        deterministic_assessment=deterministic,
        captured_at=now,
        claim_expires_at=now + timedelta(minutes=ITEM_LEASE_MINUTES),
        updated_at=now,
    )
    if result.rows_affected != 1:
        raise RuntimeError(f"backlink {backlink_id} lost its enrichment claim before analysis")


async def complete_enrichment_item(
    backlink_id: str,
    *,
    ai_assessment: dict[str, Any],
    resolved_assessment: dict[str, Any],
    assessment_version: str,
) -> None:
    now = datetime.now(UTC)
    result = await m.Backlink.update_where(
        {"id": backlink_id, "enrichment_status": "analyzing"},
        enrichment_status="completed",
        ai_assessment=ai_assessment,
        resolved_assessment=resolved_assessment,
        assessment_version=assessment_version,
        analyzed_at=now,
        next_enrichment_at=now + timedelta(days=30),
        claimed_by=None,
        claimed_at=None,
        claim_expires_at=None,
        last_error=None,
        updated_at=now,
    )
    if result.rows_affected != 1:
        raise RuntimeError(f"backlink {backlink_id} lost its enrichment claim before completion")


async def fail_enrichment_item(
    backlink_id: str,
    *,
    error: dict[str, Any],
    retryable: bool,
) -> None:
    row = await m.Backlink.load_by_id(backlink_id)
    attempts = int(row.enrichment_attempt_count or 0)
    dead = not retryable or attempts >= MAX_ENRICHMENT_ATTEMPTS
    delay_hours = min(24 * 7, 2 ** max(0, attempts - 1))
    now = datetime.now(UTC)
    await m.Backlink.update_where(
        {"id": backlink_id},
        enrichment_status="dead_letter" if dead else "failed",
        next_enrichment_at=None if dead else now + timedelta(hours=delay_hours),
        last_error=error,
        claimed_by=None,
        claimed_at=None,
        claim_expires_at=None,
        updated_at=now,
    )


async def enrichment_queue_summary(site_id: str) -> EnrichmentQueueSummary:
    rows = await m.Backlink.filter(site_id=site_id).values("enrichment_status")
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[str(row["enrichment_status"])] += 1
    return EnrichmentQueueSummary(
        total=len(rows),
        pending=counts["pending"],
        in_progress=counts["capturing"] + counts["analyzing"],
        completed=counts["completed"],
        failed=counts["failed"],
        dead_letter=counts["dead_letter"],
    )


__all__ = [
    "ASSESSMENT_VERSION",
    "DeterministicBacklinkAssessment",
    "EnrichmentQueueSummary",
    "backlink_identity_key",
    "claim_enrichment_item",
    "complete_enrichment_item",
    "deterministic_assessment",
    "enrichment_queue_summary",
    "fail_enrichment_item",
    "list_enrichment_candidates",
    "mark_enrichment_analyzing",
    "reclaim_expired_enrichment_claims",
    "upsert_current_backlinks",
]
