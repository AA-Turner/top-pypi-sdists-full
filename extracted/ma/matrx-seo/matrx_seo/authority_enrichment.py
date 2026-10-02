"""Bulk own-authority enrichment — the pass FEATURE.md said "does not exist yet".

Prospecting methods discover DOMAINS without their own link-profile metrics: a
SERP result carries no rank, no spam score, no referring-domain count, so every
SERP opportunity would sit at "Not measured" forever. DataForSEO's bulk
endpoints answer exactly this, cheaply, up to 1,000 targets per request:

* ``/v3/backlinks/bulk_ranks/live``              → the domain's OWN ``rank``
* ``/v3/backlinks/bulk_spam_score/live``         → its OWN ``spam_score``
* ``/v3/backlinks/bulk_referring_domains/live``  → its OWN ``referring_domains``

These are the domain's own numbers — the misfeeding trap in
:mod:`matrx_seo.authority_score` does not apply, which is the whole reason this
pass exists instead of reusing relationship metrics.

Collections run as ``RAW_PROVIDER`` through the ordinary
:class:`SeoCollectionService` funnel, so cost, budget gates, evidence and cache
all keep their one path. The parse reads the persisted raw payload via
``repository.load_raw_payload`` — identical for a fresh call and a cache hit.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from .adapters import SeoProgressCallback
from .authority_score import AuthorityInputs, score_authority
from .contracts import CollectionRequest, CollectionTrigger, SeoCapability
from .providers.dataforseo import DataForSeoAdapter
from .service import SeoCollectionService

logger = logging.getLogger(__name__)

BULK_RANKS_ENDPOINT = "/v3/backlinks/bulk_ranks/live"
BULK_SPAM_ENDPOINT = "/v3/backlinks/bulk_spam_score/live"
BULK_REFERRING_ENDPOINT = "/v3/backlinks/bulk_referring_domains/live"

#: Provider ceiling per bulk request.
MAX_BULK_TARGETS = 1000

#: DataForSEO bills the backlinks bulk endpoints per REQUEST, not per target, so
#: one pass costs the same whether it measures 3 domains or 1,000. Shown in
#: previews so nobody is surprised; the run records the provider's real reported
#: cost like every other collection.
ESTIMATED_COST_PER_BULK_REQUEST = Decimal("0.02")

#: What one full enrichment pass estimates at — three endpoints, one request each.
ESTIMATED_ENRICHMENT_PASS_COST = ESTIMATED_COST_PER_BULK_REQUEST * 3

_ENDPOINT_FIELDS: dict[str, str] = {
    BULK_RANKS_ENDPOINT: "rank",
    BULK_SPAM_ENDPOINT: "spam_score",
    BULK_REFERRING_ENDPOINT: "referring_domains",
}


class DomainAuthorityMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: str
    domain_rank: Decimal | None = None
    spam_score: Decimal | None = None
    referring_domains: int | None = None

    def to_inputs(self) -> AuthorityInputs:
        return AuthorityInputs(
            domain_rank=self.domain_rank,
            own_referring_domains=self.referring_domains,
            spam_score=self.spam_score,
        )


class AuthorityEnrichmentOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    #: Anchors run identity/evidence to the site the prospecting ran for.
    site_id: str
    domains: list[str] = Field(min_length=1, max_length=MAX_BULK_TARGETS)
    force_refresh: bool = False
    request_id: str | None = None
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND


class AuthorityEnrichmentOutcome(BaseModel):
    """What one enrichment pass changed, in the words a surface reports."""

    model_config = ConfigDict(extra="forbid")

    #: Rows handed to the pass.
    scanned: int = 0
    #: Rows that came back with enough evidence to carry a score.
    enriched: int = 0
    #: Rows that remain "Not measured" — reported, never silently zero.
    unmeasured: int = 0


class AuthorityEnrichmentService:
    def __init__(self, collection_service: SeoCollectionService) -> None:
        self.collection_service = collection_service

    async def enrich_rows(
        self,
        rows: list[Any],
        *,
        organization_id: str,
        created_by: str,
        site_id: str,
        force_refresh: bool = False,
        trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND,
        progress: SeoProgressCallback | None = None,
    ) -> AuthorityEnrichmentOutcome:
        """Measure and score a batch of opportunity rows, whatever found them.

        **ONE writer for every prospecting method.** ``seo.link_gap_domain`` and
        ``seo.serp_opportunity`` carry the same authority columns on purpose, so
        a competitor-gap domain and a SERP domain are measured by the same call,
        scored by the same function, and explained by the same prose — which is
        the only way "authority 67" can mean one thing across methods. Any row
        with ``normalized_domain`` and those columns qualifies; a third method
        needs no new code here.

        🚨 **``total_backlinks`` is never written and never read.** On a gap row
        it is a RELATIONSHIP number (links this domain sends to the competitors)
        and scoring it as authority put a regional newspaper below link farms —
        see the misfeeding trap in :class:`~matrx_seo.authority_score.AuthorityInputs`.
        This pass writes the three OWN-profile numbers the bulk endpoints return
        and nothing else.

        A domain the provider had nothing for keeps a NULL score, never a 0, and
        is counted as ``unmeasured`` so the caller can say so out loud.
        """
        outcome = AuthorityEnrichmentOutcome(scanned=len(rows))
        if not rows:
            return outcome
        metrics = await self.collect_metrics(
            AuthorityEnrichmentOptions(
                organization_id=organization_id,
                created_by=created_by,
                site_id=site_id,
                domains=[str(row.normalized_domain) for row in rows],
                force_refresh=force_refresh,
                trigger=trigger,
            ),
            progress=progress,
        )
        now = datetime.now(UTC)
        for row in rows:
            entry = metrics.get(str(row.normalized_domain))
            if entry is None:
                outcome.unmeasured += 1
                continue
            score = score_authority(entry.to_inputs())
            metadata = dict(row.metadata or {})
            metadata["matrx_authority"] = score.model_dump(mode="json")
            values: dict[str, Any] = {
                "domain_rank": entry.domain_rank,
                "spam_score": entry.spam_score,
                "referring_domains": entry.referring_domains,
                "enriched_at": now,
                "metadata": metadata,
                "updated_at": now,
            }
            if score.is_measured:
                values["priority_score"] = score.value
                values["priority_reason"] = score.why
                outcome.enriched += 1
            else:
                outcome.unmeasured += 1
            await row.update(**values)
        return outcome

    async def collect_metrics(
        self,
        options: AuthorityEnrichmentOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> dict[str, DomainAuthorityMetrics]:
        """Three bulk collections → one metrics map keyed by domain."""
        domains = sorted({d.strip().lower() for d in options.domains if d.strip()})
        if not domains:
            return {}
        metrics = {domain: DomainAuthorityMetrics(domain=domain) for domain in domains}
        requested_at = datetime.now(UTC)
        for endpoint, field in _ENDPOINT_FIELDS.items():
            request = CollectionRequest(
                organization_id=options.organization_id,
                created_by=options.created_by,
                capability=SeoCapability.RAW_PROVIDER,
                operation="backlinks.bulk_metrics",
                target_ref=f"web.site:{options.site_id}:authority:{field}",
                site_id=options.site_id,
                observation_period=requested_at.date().isoformat(),
                trigger=options.trigger,
                settings={
                    "workflow": "live",
                    "endpoint": endpoint,
                    "tasks": [{"targets": domains}],
                },
                request_id=options.request_id or str(uuid4()),
                force_refresh=options.force_refresh,
            )
            receipt = await self.collection_service.collect(
                DataForSeoAdapter(), request, progress=progress
            )
            if not receipt.raw_payload_id:
                raise ValueError(
                    f"bulk authority collection {field} completed without a raw "
                    "payload — metrics cannot be read back"
                )
            payload = await self.collection_service.repository.load_raw_payload(
                receipt.raw_payload_id
            )
            if not isinstance(payload, dict):
                raise ValueError(f"bulk authority payload for {field} is not an object")
            self._fold_payload(payload, field, metrics)
        return metrics

    @staticmethod
    def _fold_payload(
        payload: dict[str, Any], field: str, metrics: dict[str, DomainAuthorityMetrics]
    ) -> None:
        tasks = payload.get("tasks")
        if not isinstance(tasks, list):
            raise ValueError("bulk authority payload tasks must be a list")
        matched = 0
        for task in tasks:
            if not isinstance(task, dict):
                continue
            for result in task.get("result") or []:
                if not isinstance(result, dict):
                    continue
                for item in result.get("items") or []:
                    if not isinstance(item, dict):
                        continue
                    target = str(item.get("target") or "").strip().lower()
                    target = target.removeprefix("www.").rstrip(".")
                    entry = metrics.get(target)
                    if entry is None:
                        continue
                    value = item.get(field)
                    if value is None or isinstance(value, bool):
                        continue
                    if field == "rank":
                        entry.domain_rank = Decimal(str(value))
                    elif field == "spam_score":
                        entry.spam_score = Decimal(str(value))
                    elif field == "referring_domains":
                        entry.referring_domains = int(value)
                    matched += 1
        if matched == 0:
            # A whole bulk response matching nothing means the target list and
            # the response disagree — scream, never silently leave every domain
            # "Not measured" (silent emptiness is the defect class WP4 filed).
            logger.error(
                "bulk authority %s response matched 0 of %d requested domains",
                field,
                len(metrics),
            )


__all__ = [
    "ESTIMATED_COST_PER_BULK_REQUEST",
    "ESTIMATED_ENRICHMENT_PASS_COST",
    "MAX_BULK_TARGETS",
    "AuthorityEnrichmentOptions",
    "AuthorityEnrichmentOutcome",
    "AuthorityEnrichmentService",
    "DomainAuthorityMetrics",
]
