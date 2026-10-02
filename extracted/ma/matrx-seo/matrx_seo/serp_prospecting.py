"""SERP/keyword prospecting — *"who already ranks for my topics is who I write to."*

The SECOND prospecting method (outreach WP2, round 2). The competitor link gap
asks "who links to my competitors"; this asks "who Google already surfaces for
the campaign's queries" — via five query variants over the existing DataForSEO
SERP operation:

* ``keyword``           — the seed phrase itself.
* ``advanced_operator`` — guest-post footprints (``"kw" "write for us"``).
* ``resource_page``     — curated link pages (``kw intitle:resources``).
* ``listicle``          — "best/top" round-ups worth being added to.
* ``hot_off_press``     — the last 24 hours (``tbs=qdr:d``), Pitchbox's
  reply-rate differentiator: pages published yesterday have an author reading
  replies today.

**Design rules inherited from the link gap, deliberately:**

* Queries are recorded as text evidence, never minted as universal
  ``seo.keyword`` rows — an operator string is not a keyword.
* One collection run per prospecting pass (standard workflow, ≤100 tasks in
  one POST), so cost, cache, resume and evidence keep one path.
* ``preview()`` shows every query and the estimated cost BEFORE money moves.
* Results order by mention count then authority; the score ORDERS and never
  filters — only the human review gate removes a row.
* Our own domain is excluded inside the normalizer (tag-carried), and the
  blocklist is enforced at CRM ingestion by the fold, never in the UI.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from .adapters import SeoProgressCallback
from .authority_enrichment import (
    MAX_BULK_TARGETS,
    AuthorityEnrichmentService,
)
from .contracts import (
    CollectionReceipt,
    CollectionRequest,
    CollectionTrigger,
    SeoCapability,
)
from .db import models_seo as m
from .db.models_host import WebSite
from .domain_link_gap import site_domain_from_root_url
from .providers.dataforseo import DataForSeoAdapter
from .providers.dataforseo.serp_prospect import (
    SERP_ORGANIC_OPERATION,
    encode_prospect_tag,
)
from .service import SeoCollectionService


class QueryVariant(str, Enum):
    KEYWORD = "keyword"
    ADVANCED_OPERATOR = "advanced_operator"
    RESOURCE_PAGE = "resource_page"
    LISTICLE = "listicle"
    HOT_OFF_PRESS = "hot_off_press"


#: The expert reflexes, encoded (canvas doctrine): the footprints practitioners
#: actually type. Few per variant on purpose — every template is a paid task
#: per seed keyword. Tuning happens here, in code, per the "config is not an
#: env var" rule.
VARIANT_TEMPLATES: dict[QueryVariant, tuple[str, ...]] = {
    QueryVariant.KEYWORD: ("{kw}",),
    QueryVariant.ADVANCED_OPERATOR: (
        '"{kw}" "write for us"',
        '"{kw}" "guest post"',
    ),
    QueryVariant.RESOURCE_PAGE: (
        "{kw} intitle:resources",
        '{kw} "useful resources"',
    ),
    QueryVariant.LISTICLE: (
        'intitle:"best" {kw}',
        'intitle:"top" {kw}',
    ),
    QueryVariant.HOT_OFF_PRESS: ("{kw}",),
}

#: Google URL parameter for "past 24 hours" — the whole hot-off-press variant.
HOT_OFF_PRESS_SEARCH_PARAM = "tbs=qdr:d"

#: One standard task POST accepts at most 100 tasks; this is also the cost cap.
MAX_PROSPECT_QUERIES = 100

#: DataForSEO standard-priority SERP price per 10 results (estimate shown in
#: preview; the run records the provider's real reported cost).
ESTIMATED_COST_PER_10_RESULTS = Decimal("0.0006")

DEFAULT_DEPTH = 30
DEFAULT_LOCATION_CODE = 2840  # United States
DEFAULT_LANGUAGE_CODE = "en"

#: The suffix that marks a collection run as a PROSPECTING pass rather than
#: ordinary SERP rank tracking. Both use ``SeoCapability.SERP_RANK``, so the
#: target ref is what tells them apart — and the post-collection CRM fold hook
#: needs exactly that distinction to know whether new prospects can exist.
#: Defined here, beside the run that writes it, so there is ONE spelling.
PROSPECTING_TARGET_SUFFIX = "serp_prospecting"


def prospecting_target_ref(site_id: str) -> str:
    return f"web.site:{site_id}:{PROSPECTING_TARGET_SUFFIX}"


def is_prospecting_target(target_ref: object) -> bool:
    """True when this collection run was a prospecting pass."""
    return isinstance(target_ref, str) and target_ref.endswith(f":{PROSPECTING_TARGET_SUFFIX}")


DEFAULT_VARIANTS: tuple[QueryVariant, ...] = (
    QueryVariant.KEYWORD,
    QueryVariant.ADVANCED_OPERATOR,
    QueryVariant.RESOURCE_PAGE,
    QueryVariant.LISTICLE,
)


class ProspectQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    variant: QueryVariant
    seed_keyword: str


class SerpProspectingOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    site_id: str
    #: Plain seed phrases — validated non-operator text; the variants add the
    #: operators themselves.
    keywords: list[str] = Field(min_length=1, max_length=20)
    variants: list[QueryVariant] = Field(
        default_factory=lambda: list(DEFAULT_VARIANTS), min_length=1
    )
    depth: int = Field(default=DEFAULT_DEPTH, ge=10, le=100)
    location_code: int = DEFAULT_LOCATION_CODE
    language_code: str = DEFAULT_LANGUAGE_CODE
    #: Fill own-authority metrics + Matrx Authority Score after the SERP pass.
    enrich_authority: bool = True
    force_refresh: bool = False
    request_id: str | None = None
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND


class SerpProspectingPreview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    site_domain: str
    queries: list[ProspectQuery]
    estimated_cost_usd: Decimal
    #: Queries dropped to stay under the per-run cap, named so the user sees
    #: what was NOT asked.
    dropped: list[str] = Field(default_factory=list)


class SerpProspectingReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    site_domain: str
    queries: list[ProspectQuery]
    receipt: CollectionReceipt
    #: Domains whose own-authority metrics were measured this pass.
    enriched_domains: int = 0
    #: Opportunities that remain "Not measured" after the pass.
    unmeasured_domains: int = 0


def build_prospect_queries(
    keywords: list[str], variants: list[QueryVariant]
) -> tuple[list[ProspectQuery], list[str]]:
    """Expand seeds × variant templates, deduped, capped at the run limit."""
    queries: list[ProspectQuery] = []
    seen: set[tuple[str, bool]] = set()
    dropped: list[str] = []
    for keyword in keywords:
        seed = " ".join(keyword.split()).strip()
        if not seed:
            continue
        for variant in variants:
            for template in VARIANT_TEMPLATES[variant]:
                query = template.format(kw=seed)
                # Hot-off-press reuses the seed's literal text but is a
                # DIFFERENT paid request (tbs=qdr:d), so it dedupes in its own
                # bucket — text-only dedupe silently dropped the whole variant.
                dedupe_key = (
                    query.lower(),
                    variant is QueryVariant.HOT_OFF_PRESS,
                )
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                if len(queries) >= MAX_PROSPECT_QUERIES:
                    dropped.append(query)
                    continue
                queries.append(ProspectQuery(query=query, variant=variant, seed_keyword=seed))
    if not queries:
        raise ValueError("no usable prospecting queries — keywords were blank")
    return queries, dropped


class SerpProspectingService:
    def __init__(self, collection_service: SeoCollectionService) -> None:
        self.collection_service = collection_service
        self.enrichment = AuthorityEnrichmentService(collection_service)

    async def _site_domain(self, options: SerpProspectingOptions) -> str:
        site = await WebSite.load_by_id_or_none(options.site_id)
        if site is None or str(site.organization_id) != options.organization_id:
            raise ValueError("site_id is not a site in this organization")
        return site_domain_from_root_url(site.root_url)

    async def preview(self, options: SerpProspectingOptions) -> SerpProspectingPreview:
        """Every query and the cost, BEFORE any money moves."""
        own_domain = await self._site_domain(options)
        queries, dropped = build_prospect_queries(options.keywords, options.variants)
        estimated = (
            ESTIMATED_COST_PER_10_RESULTS
            * len(queries)
            * (options.depth // 10 + (1 if options.depth % 10 else 0))
        )
        return SerpProspectingPreview(
            site_id=options.site_id,
            site_domain=own_domain,
            queries=queries,
            estimated_cost_usd=estimated,
            dropped=dropped,
        )

    def _task(
        self, query: ProspectQuery, options: SerpProspectingOptions, own_domain: str
    ) -> dict[str, Any]:
        task: dict[str, Any] = {
            "keyword": query.query,
            "location_code": options.location_code,
            "language_code": options.language_code,
            "depth": options.depth,
            "tag": encode_prospect_tag(
                variant=query.variant.value,
                seed_keyword=query.seed_keyword,
                exclude_domain=own_domain,
            ),
        }
        # A user watching the stream should not wait on the provider's
        # normal-priority queue (measured 25+ min for a 16-task batch,
        # 2026-08-16). Priority 2 doubles a price measured in tenths of a
        # cent and polls at 5s; scheduled/background runs stay cheap.
        if options.trigger is CollectionTrigger.ON_DEMAND:
            task["priority"] = 2
        if query.variant is QueryVariant.HOT_OFF_PRESS:
            task["search_param"] = HOT_OFF_PRESS_SEARCH_PARAM
        return task

    async def collect(
        self,
        options: SerpProspectingOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> SerpProspectingReceipt:
        own_domain = await self._site_domain(options)
        queries, _ = build_prospect_queries(options.keywords, options.variants)

        requested_at = datetime.now(UTC)
        request = CollectionRequest(
            organization_id=options.organization_id,
            created_by=options.created_by,
            capability=SeoCapability.SERP_RANK,
            operation=SERP_ORGANIC_OPERATION,
            target_ref=prospecting_target_ref(options.site_id),
            site_id=options.site_id,
            # Date, not timestamp: a timestamped period makes every retry a
            # NEW paid identity, so the 24h SERP freshness cache could never
            # fire. Same keywords + variants + depth on the same day reuse the
            # completed run; force_refresh stays the explicit escape hatch.
            observation_period=requested_at.date().isoformat(),
            trigger=options.trigger,
            settings={
                "workflow": "standard",
                "tasks": [self._task(query, options, own_domain) for query in queries],
            },
            request_id=options.request_id or str(uuid4()),
            force_refresh=options.force_refresh,
        )
        receipt = await self.collection_service.collect(
            DataForSeoAdapter(), request, progress=progress
        )

        enriched = 0
        unmeasured = 0
        if options.enrich_authority:
            enriched, unmeasured = await self._enrich_site(options, progress=progress)
        return SerpProspectingReceipt(
            site_id=options.site_id,
            site_domain=own_domain,
            queries=queries,
            receipt=receipt,
            enriched_domains=enriched,
            unmeasured_domains=unmeasured,
        )

    async def _enrich_site(
        self,
        options: SerpProspectingOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> tuple[int, int]:
        """Measure own-authority for every un-enriched opportunity on the site.

        A row that was enriched before keeps its metrics (a SERP re-run says
        nothing new about a domain's link profile); re-measuring is the
        30-day cache's job via ``force_refresh`` on a future refresh pass.

        The measure-score-write half lives in
        :meth:`AuthorityEnrichmentService.enrich_rows` so the competitor link
        gap runs the identical pass — one score, one prose, one meaning.
        """
        rows = (
            await m.SerpOpportunity.filter(site_id=options.site_id, enriched_at=None)
            .limit(MAX_BULK_TARGETS)
            .all()
        )
        outcome = await self.enrichment.enrich_rows(
            rows,
            organization_id=options.organization_id,
            created_by=options.created_by,
            site_id=options.site_id,
            trigger=options.trigger,
            progress=progress,
        )
        return outcome.enriched, outcome.unmeasured


__all__ = [
    "DEFAULT_VARIANTS",
    "HOT_OFF_PRESS_SEARCH_PARAM",
    "MAX_PROSPECT_QUERIES",
    "PROSPECTING_TARGET_SUFFIX",
    "ProspectQuery",
    "QueryVariant",
    "SerpProspectingOptions",
    "SerpProspectingPreview",
    "SerpProspectingReceipt",
    "SerpProspectingService",
    "VARIANT_TEMPLATES",
    "build_prospect_queries",
    "is_prospecting_target",
    "prospecting_target_ref",
]
