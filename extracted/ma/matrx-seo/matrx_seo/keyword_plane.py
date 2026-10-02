"""Keyword-plane service paths: research ingestion, edge rejection, and the
volume-refresh staleness filter.

The rebuilt ``seo`` keyword plane owns its write logic in DB functions —
this module is the ONLY Python surface over them. Never re-implement any of
it in app code:

- ``seo.fn_ingest_keyword_research`` — upserts every phrase in a
  keyword-relationship research artifact and mints the typed edges
  (Parent → primary ``refines`` parent · Child → child ``refines`` primary ·
  Natural LSIs → ``variant_of`` primary (proposed) · Related → ``related``).
  Rejected edges are PERMANENT memory: re-ingestion counts them in
  ``edges_skipped_rejected`` and never resurrects them.
- ``seo.fn_reject_keyword_edge`` — the ONLY way to reject an edge. NEVER
  ``delete`` a ``seo.keyword_edge`` row to "remove" a relationship; deletion
  un-teaches the rejection and the edge comes back on the next research run.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from matrx_orm.operations.db_functions import call_db_function

from .db import models_seo as m
from .orm_identity import normalize_keyword_phrase

logger = logging.getLogger(__name__)

VOLUME_REFRESH_TTL_DAYS = 30
DEFAULT_LOCATION_CODE = 2840  # United States (Google Ads / DataForSEO int)


async def ingest_keyword_research(
    research: dict[str, Any] | list[dict[str, Any]],
    *,
    language: str = "en",
    research_doc_id: str | None = None,
    site_id: str | None = None,
) -> dict[str, Any]:
    """Persist a keyword_relationship_research artifact — ONE RPC, no Python
    duplication. ``research`` is the exact agent artifact (object or array of
    objects). Returns the RPC summary::

        {primary_keyword_ids, keywords_created, keywords_already_existed,
         edges_written, edges_skipped_rejected, edges_skipped_self,
         site_keyword_values_created}

    ``site_id`` (MSR-26) makes every discovered keyword land on the site via
    ``seo.site_keyword_value`` (idempotent — never duplicates an existing
    row); the phrase identity itself stays in the shared global library.
    """
    rows = await call_db_function(
        m.Keyword,
        "seo.fn_ingest_keyword_research",
        research,
        language,
        research_doc_id,
        site_id,
    )
    if not rows:
        raise RuntimeError("seo.fn_ingest_keyword_research returned no summary")
    summary = next(iter(rows[0].values()))
    if isinstance(summary, str):
        summary = json.loads(summary)
    logger.info("seo keyword research ingested: %s", summary)
    return summary


async def reject_keyword_edge(edge_id: str, reason: str) -> None:
    """Reject a keyword edge through ``seo.fn_reject_keyword_edge`` — the only
    sanctioned rejection path (rejection is durable memory; never DELETE)."""
    if not reason.strip():
        raise ValueError("keyword edge rejection requires a nonblank reason")
    await call_db_function(m.KeywordEdge, "seo.fn_reject_keyword_edge", edge_id, reason)
    logger.info("seo keyword edge %s rejected: %s", edge_id, reason)


async def keywords_needing_volume_refresh(
    phrases: list[str],
    *,
    language: str = "en",
    location_code: int = DEFAULT_LOCATION_CODE,
    ttl_days: int = VOLUME_REFRESH_TTL_DAYS,
    force_refresh: bool = False,
) -> list[str]:
    """Filter ``phrases`` down to the ones whose ``seo.keyword_market`` row is
    missing or stale (``metrics_fetched_at`` older than ``ttl_days``) for
    ``location_code``. Callers batch the survivors into as few provider
    requests as possible (≤1,000 keywords/request — cost is per REQUEST).

    A missing row means never fetched; ``search_volume = 0`` on a fresh row
    means fetched and genuinely zero — that row is FRESH and is filtered out.
    ``force_refresh=True`` (an explicit user request) bypasses the TTL and
    returns every phrase.
    """
    deduped: dict[str, str] = {}
    for phrase in phrases:
        if phrase.strip():
            deduped.setdefault(normalize_keyword_phrase(phrase), phrase)
    if not deduped or force_refresh:
        return list(deduped.values())

    keywords = await m.Keyword.filter(
        normalized_phrase__in=list(deduped.keys()),
        language=language,
        deleted_at__isnull=True,
    ).all()
    keyword_by_id = {str(keyword.id): str(keyword.normalized_phrase) for keyword in keywords}
    fresh_cutoff = datetime.now(UTC) - timedelta(days=ttl_days)
    fresh: set[str] = set()
    if keyword_by_id:
        markets = await m.KeywordMarket.filter(
            keyword_id__in=list(keyword_by_id.keys()),
            location_code=location_code,
            deleted_at__isnull=True,
        ).all()
        for market in markets:
            fetched_at = market.metrics_fetched_at
            if fetched_at is not None and fetched_at >= fresh_cutoff:
                fresh.add(keyword_by_id[str(market.keyword_id)])
    return [phrase for normalized, phrase in deduped.items() if normalized not in fresh]


__all__ = [
    "DEFAULT_LOCATION_CODE",
    "VOLUME_REFRESH_TTL_DAYS",
    "ingest_keyword_research",
    "keywords_needing_volume_refresh",
    "reject_keyword_edge",
]
