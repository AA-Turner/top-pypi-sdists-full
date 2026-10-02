"""Site-wide competitor link gap — *"who links to my competitors and not to me?"*

**Arman, 2026-08-14:** *"When we're doing things to try to get backlinks, it's
not so much who's linking to us — it's about analyzing who's linking to our
competitors."* This module is the answer to that sentence at the whole-site
level; :mod:`matrx_seo.page_link_gap` is its page-level twin, and the two share
their request shaping (:mod:`matrx_seo.link_gap_request`), their normalizer and
their persistence.

**The seed rule is the whole design** (system of record:
``common-docs/systems/marketing/competitor-classification/FEATURE.md`` §5). A gap run is a
paid call whose entire output is judged by who was in the request, so:

* only a **human-confirmed** competitor may seed one, and
* only one that passes the link-gap eligibility test — a *business* in our
  industry, whose linkers would plausibly link to us too. Wikipedia's linkers
  and a marketplace's linkers are worthless to chase, which is exactly why
  ``entity_role`` exists.

**Zero eligible competitors is a correct, explainable outcome, not a failure.**
Today the platform holds 84 proposed competitors and none confirmed, so a
correct implementation seeds nothing until a human rules — and it must say so in
words a non-technical expert can act on, never as a bare error.
"""

from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import urlparse
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from .adapters import SeoProgressCallback
from .authority_enrichment import MAX_BULK_TARGETS, AuthorityEnrichmentService
from .contracts import (
    CollectionReceipt,
    CollectionRequest,
    CollectionTrigger,
    SeoCapability,
)
from .db import models_seo as m
from .db.models_host import WebSite
from .link_gap_request import (
    DOMAIN_RANK_FIELD,
    DOMAIN_SPAM_FIELD,
    MAX_INTERSECTION_TARGETS,
    numbered_targets,
    rank_order_by,
    spam_score_filter,
)
from .page_link_gap import competitor_is_link_gap_eligible
from .providers.dataforseo import DataForSeoAdapter
from .providers.dataforseo.link_gap import DOMAIN_INTERSECTION
from .service import SeoCollectionService


class NoEligibleCompetitors(ValueError):
    """Raised when nothing may legitimately seed a paid gap run.

    Carries the counts behind the refusal so the surface can render the real
    next step ("confirm your competitors") instead of a dead end.
    """

    def __init__(self, *, site_id: str, total: int, confirmed: int, eligible: int) -> None:
        self.site_id = site_id
        self.total = total
        self.confirmed = confirmed
        self.eligible = eligible
        if total == 0:
            message = (
                "No competitors have been identified for this site yet. Add or "
                "discover competitors first, then confirm the real ones."
            )
        elif confirmed == 0:
            subject = "1 competitor is" if total == 1 else f"{total} competitors are"
            message = (
                f"{subject} waiting for your review and none are confirmed yet. "
                "Confirm the ones that are genuinely your competitors and this "
                "analysis can run."
            )
        else:
            subject = (
                "Your 1 confirmed competitor is not"
                if confirmed == 1
                else f"None of your {confirmed} confirmed competitors are"
            )
            message = (
                f"{subject} the kind whose backlinks are worth chasing — sites "
                "like marketplaces, directories and publishers get linked to for "
                "what they are, not for the industry. Confirm a competing "
                "business, or mark one of these as usable for link gap analysis."
            )
        super().__init__(message)


class DomainLinkGapOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    site_id: str
    #: Explicit competitor selection. Empty means "every confirmed, eligible
    #: competitor on this site" — the ordinary path.
    competitor_ids: list[str] = Field(default_factory=list)
    limit: int = Field(default=1000, ge=1, le=1000)
    max_spam_score: int = Field(default=30, ge=0, le=100)
    #: Fill each gap domain's OWN link-profile metrics after the gap pass, so
    #: the Matrx Authority Score is measured rather than partial. See
    #: :meth:`DomainLinkGapService._enrich_gap_domains`.
    enrich_authority: bool = True
    force_refresh: bool = False
    request_id: str | None = None
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND


class SeededCompetitor(BaseModel):
    """One competitor that made it into the request, and why it qualified."""

    model_config = ConfigDict(extra="forbid")

    competitor_id: str
    domain: str
    entity_role: str | None = None
    business_overlap: str | None = None
    market_overlap: str | None = None
    #: True when a human explicitly overrode the taxonomy default.
    explicitly_enabled: bool = False


class DomainLinkGapReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    site_domain: str
    seeded: list[SeededCompetitor]
    #: Confirmed competitors deliberately left out, with the reason, so the user
    #: can see what was NOT asked about.
    excluded: list[str] = Field(default_factory=list)
    receipt: CollectionReceipt
    #: Gap domains whose OWN authority metrics were measured this pass.
    enriched_domains: int = 0
    #: Gap domains that remain "Not measured" after the pass.
    unmeasured_domains: int = 0


def site_domain_from_root_url(root_url: object) -> str:
    """The site's own domain — what the gap is measured AGAINST."""
    text = str(root_url or "").strip()
    parsed = urlparse(text if "://" in text else f"https://{text}")
    host = (parsed.netloc or "").strip().lower()
    host = host.split("@")[-1].split(":")[0].removeprefix("www.").rstrip(".")
    if not host or "." not in host:
        raise ValueError(f"site root_url {root_url!r} has no usable domain")
    return host


class DomainLinkGapService:
    def __init__(self, collection_service: SeoCollectionService) -> None:
        self.collection_service = collection_service

    async def select_competitors(
        self, options: DomainLinkGapOptions
    ) -> tuple[list[SeededCompetitor], list[str]]:
        """Apply the seed rule. Raises :class:`NoEligibleCompetitors` when empty.

        Separate from :meth:`collect` on purpose: a surface must be able to show
        the user exactly who WOULD be asked about, and what it would cost, before
        anyone spends money.
        """
        competitors = await m.Competitor.filter(site_id=options.site_id).all()
        if options.competitor_ids:
            wanted = set(options.competitor_ids)
            found = {str(row.id) for row in competitors}
            missing = wanted - found
            if missing:
                raise ValueError(
                    "these competitors do not belong to this site: " + ", ".join(sorted(missing))
                )
            competitors = [row for row in competitors if str(row.id) in wanted]

        confirmed = [row for row in competitors if str(row.classification_status) == "confirmed"]
        seeded: list[SeededCompetitor] = []
        excluded: list[str] = []
        for row in confirmed:
            domain = str(row.normalized_domain or "").strip().lower().removeprefix("www.")
            if not domain:
                excluded.append("a confirmed competitor has no domain recorded")
                continue
            if not competitor_is_link_gap_eligible(row):
                excluded.append(
                    f"{domain} — a {str(row.entity_role or 'site').replace('_', ' ')} "
                    "whose linkers would not plausibly link to you"
                )
                continue
            seeded.append(
                SeededCompetitor(
                    competitor_id=str(row.id),
                    domain=domain,
                    entity_role=str(row.entity_role) if row.entity_role else None,
                    business_overlap=(str(row.business_overlap) if row.business_overlap else None),
                    market_overlap=(str(row.market_overlap) if row.market_overlap else None),
                    explicitly_enabled=row.use_for_link_gap is True,
                )
            )

        if not seeded:
            raise NoEligibleCompetitors(
                site_id=options.site_id,
                total=len(competitors),
                confirmed=len(confirmed),
                eligible=0,
            )

        # Deduplicate on domain — two competitor rows for one domain would spend
        # a target slot twice and make the numbered map ambiguous.
        by_domain: dict[str, SeededCompetitor] = {}
        for candidate in seeded:
            by_domain.setdefault(candidate.domain, candidate)
        ordered = list(by_domain.values())
        if len(ordered) > MAX_INTERSECTION_TARGETS:
            for dropped in ordered[MAX_INTERSECTION_TARGETS:]:
                excluded.append(
                    f"{dropped.domain} — over the provider's "
                    f"{MAX_INTERSECTION_TARGETS}-competitor limit for one run"
                )
            ordered = ordered[:MAX_INTERSECTION_TARGETS]
        return ordered, excluded

    async def collect(
        self,
        options: DomainLinkGapOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> DomainLinkGapReceipt:
        site = await WebSite.load_by_id_or_none(options.site_id)
        if site is None or str(site.organization_id) != options.organization_id:
            raise ValueError("site_id is not a site in this organization")
        own_domain = site_domain_from_root_url(site.root_url)

        seeded, excluded = await self.select_competitors(options)
        targets = numbered_targets([row.domain for row in seeded])

        requested_at = datetime.now(UTC)
        task = {
            "targets": targets,
            "exclude_targets": [own_domain],
            "intersection_mode": "partial",
            "backlinks_status_type": "live",
            "include_subdomains": False,
            "include_indirect_links": False,
            "exclude_internal_backlinks": True,
            "limit": options.limit,
            "order_by": rank_order_by(DOMAIN_RANK_FIELD),
            "filters": spam_score_filter(
                len(targets), options.max_spam_score, field=DOMAIN_SPAM_FIELD
            ),
        }
        request = CollectionRequest(
            organization_id=options.organization_id,
            created_by=options.created_by,
            capability=SeoCapability.BACKLINKS,
            operation="backlinks.intersections",
            target_ref=f"web.site:{options.site_id}",
            site_id=options.site_id,
            observation_period=requested_at.isoformat(),
            trigger=options.trigger,
            settings={
                "workflow": "live",
                "endpoint": DOMAIN_INTERSECTION,
                "tasks": [task],
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
            enriched, unmeasured = await self._enrich_gap_domains(options, progress=progress)
        return DomainLinkGapReceipt(
            site_id=options.site_id,
            site_domain=own_domain,
            seeded=seeded,
            excluded=excluded,
            receipt=receipt,
            enriched_domains=enriched,
            unmeasured_domains=unmeasured,
        )

    async def _enrich_gap_domains(
        self,
        options: DomainLinkGapOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> tuple[int, int]:
        """Measure each un-enriched gap domain's OWN link profile, then score it.

        **This closes round 1's honest gap.** ``backlinks/domain_intersection``
        answers "who links to my competitors" and returns rank and spam for each
        referring domain — but no own-profile link counts, and the
        ``total_backlinks`` it does return is a RELATIONSHIP number (links sent
        to the COMPETITORS) that must never be scored as authority. So a gap
        domain shipped scored on two signals out of three, at ``partial``
        confidence, forever.

        The bulk own-metrics pass built for SERP prospecting answers exactly the
        missing question, so the gap now runs the SAME pass, through the SAME
        writer, producing the SAME score on the SAME scale — which is what makes
        "authority 67" mean one thing whether the domain came from a competitor
        backlink or a search result.

        Un-enriched rows only: a re-run of the gap says nothing new about a
        domain's own link profile, and re-measuring is paid work.
        """
        rows = (
            await m.LinkGapDomain.filter(site_id=options.site_id, enriched_at=None)
            .limit(MAX_BULK_TARGETS)
            .all()
        )
        outcome = await AuthorityEnrichmentService(self.collection_service).enrich_rows(
            rows,
            organization_id=options.organization_id,
            created_by=options.created_by,
            site_id=options.site_id,
            trigger=options.trigger,
            progress=progress,
        )
        return outcome.enriched, outcome.unmeasured


__all__ = [
    "DomainLinkGapOptions",
    "DomainLinkGapReceipt",
    "DomainLinkGapService",
    "NoEligibleCompetitors",
    "SeededCompetitor",
    "site_domain_from_root_url",
]
