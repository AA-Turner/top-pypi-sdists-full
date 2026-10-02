"""Human-gated page-level competitor link-gap collection.

The page picker is ``seo.competitor_opportunity``: ``target_page_id`` names
our canonical page and ``competitor_url`` names the page that beats it. This
module validates those accepted proposals against the confirmed competitor
taxonomy, then runs DataForSEO's page intersection through the canonical SEO
collection service.
"""

from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import urlparse
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from .adapters import SeoProgressCallback
from .contracts import (
    CollectionReceipt,
    CollectionRequest,
    CollectionTrigger,
    SeoCapability,
)
from .db import models_seo as m
from .db.models_host import WebPage
from .link_gap_request import (
    MAX_INTERSECTION_TARGETS,
    PAGE_RANK_FIELD,
    PAGE_SPAM_FIELD,
    numbered_targets,
    rank_order_by,
    spam_score_filter,
)
from .providers.dataforseo import DataForSeoAdapter
from .providers.dataforseo.link_gap import PAGE_INTERSECTION
from .service import SeoCollectionService


class PageLinkGapOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    site_id: str
    page_id: str
    opportunity_ids: list[str] = Field(min_length=2, max_length=MAX_INTERSECTION_TARGETS)
    limit: int = Field(default=1000, ge=1, le=1000)
    max_spam_score: int = Field(default=30, ge=0, le=100)
    force_refresh: bool = True
    request_id: str | None = None
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND


class PageLinkGapReceipt(BaseModel):
    page_id: str
    page_url: str
    competitor_pages: list[str]
    opportunity_ids: list[str]
    receipt: CollectionReceipt


def competitor_is_link_gap_eligible(competitor: m.Competitor) -> bool:
    """Apply the canonical explicit-override-else-taxonomy rule."""

    if str(competitor.classification_status) != "confirmed":
        return False
    if competitor.use_for_link_gap is not None:
        return bool(competitor.use_for_link_gap)
    return str(competitor.entity_role) == "business" and str(competitor.business_overlap) in {
        "direct",
        "adjacent",
    }


def _absolute_http_url(value: object, *, field: str) -> str:
    text = str(value or "").strip()
    parsed = urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{field} must be an absolute http(s) URL")
    return text


class PageLinkGapService:
    def __init__(self, collection_service: SeoCollectionService) -> None:
        self.collection_service = collection_service

    async def collect(
        self,
        options: PageLinkGapOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> PageLinkGapReceipt:
        page = await WebPage.load_by_id_or_none(options.page_id)
        if page is None or str(page.site_id) != options.site_id:
            raise ValueError("page_id is not a canonical page on this site")
        page_url = _absolute_http_url(page.url, field="web.page.url")

        unique_ids = list(dict.fromkeys(options.opportunity_ids))
        if len(unique_ids) != len(options.opportunity_ids):
            raise ValueError("opportunity_ids must not contain duplicates")
        opportunities = await m.CompetitorOpportunity.filter(id__in=unique_ids).all()
        by_id = {str(row.id): row for row in opportunities}
        if set(by_id) != set(unique_ids):
            raise ValueError("one or more competitor opportunities do not exist")

        competitor_ids = {
            str(row.competitor_id) for row in opportunities if row.competitor_id is not None
        }
        competitors = await m.Competitor.filter(id__in=list(competitor_ids)).all()
        competitor_by_id = {str(row.id): row for row in competitors}

        competitor_pages: list[str] = []
        for opportunity_id in unique_ids:
            opportunity = by_id[opportunity_id]
            if (
                str(opportunity.site_id) != options.site_id
                or str(opportunity.target_page_id) != options.page_id
            ):
                raise ValueError("every opportunity must belong to this page and site")
            if str(opportunity.status) != "accepted":
                raise ValueError(f"competitor opportunity {opportunity_id} is not human-accepted")
            competitor = competitor_by_id.get(str(opportunity.competitor_id))
            if competitor is None or not competitor_is_link_gap_eligible(competitor):
                raise ValueError(
                    f"competitor opportunity {opportunity_id} is not confirmed "
                    "and link-gap eligible"
                )
            competitor_pages.append(
                _absolute_http_url(
                    opportunity.competitor_url,
                    field=f"competitor opportunity {opportunity_id} URL",
                )
            )

        requested_at = datetime.now(UTC)
        targets = numbered_targets(competitor_pages)
        task = {
            "targets": targets,
            "exclude_targets": [page_url],
            "intersection_mode": "partial",
            "backlinks_status_type": "live",
            "include_subdomains": False,
            "include_indirect_links": False,
            "exclude_internal_backlinks": True,
            "limit": options.limit,
            "order_by": rank_order_by(PAGE_RANK_FIELD),
            "filters": spam_score_filter(
                len(targets), options.max_spam_score, field=PAGE_SPAM_FIELD
            ),
        }
        request = CollectionRequest(
            organization_id=options.organization_id,
            created_by=options.created_by,
            capability=SeoCapability.BACKLINKS,
            operation="backlinks.intersections",
            target_ref=f"web.page:{options.page_id}",
            site_id=options.site_id,
            page_id=options.page_id,
            observation_period=requested_at.isoformat(),
            trigger=options.trigger,
            settings={"workflow": "live", "endpoint": PAGE_INTERSECTION, "tasks": [task]},
            request_id=options.request_id or str(uuid4()),
            force_refresh=options.force_refresh,
        )
        receipt = await self.collection_service.collect(
            DataForSeoAdapter(), request, progress=progress
        )
        return PageLinkGapReceipt(
            page_id=options.page_id,
            page_url=page_url,
            competitor_pages=competitor_pages,
            opportunity_ids=unique_ids,
            receipt=receipt,
        )


__all__ = [
    "PageLinkGapOptions",
    "PageLinkGapReceipt",
    "PageLinkGapService",
    "competitor_is_link_gap_eligible",
]
