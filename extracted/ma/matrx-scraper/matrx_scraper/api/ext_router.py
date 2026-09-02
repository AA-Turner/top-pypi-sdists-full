"""
External endpoints — batch scrape, content save, retry queue, domain config.

Depends on: matrx_connect (AppContext, context_dep)
No aidream imports.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from matrx_connect import AppContext, context_dep
from matrx_orm import Count, F
from pydantic import BaseModel, Field

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.db.models_scraper import ScrapeRetryQueue
from matrx_scraper.orchestrator import scrape_many
from matrx_scraper.utils.url import get_url_info

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class BatchScrapeRequest(BaseModel):
    urls: list[str] = Field(..., min_length=1, max_length=100)
    use_proxy: bool = True
    fast: bool = False


class BatchScrapeResponse(BaseModel):
    status: str
    execution_time_ms: float
    results: list[dict[str, Any]]


class ContentSaveRequest(BaseModel):
    url: str
    page_name: str
    content: dict[str, Any]
    content_type: str = "html"
    char_count: int = 0


class RetryClaimRequest(BaseModel):
    item_ids: list[str]
    client_id: str
    claim_ttl_minutes: int = 10


class RetrySubmitRequest(BaseModel):
    queue_item_id: str


class RetryFailRequest(BaseModel):
    queue_item_id: str
    error: str
    promote_to_extension: bool = False


class DomainUpsertRequest(BaseModel):
    url: str
    common_name: str | None = None
    scrape_allowed: bool = True
    enabled: bool = True
    proxy_type: str = "datacenter"


# ---------------------------------------------------------------------------
# Batch scrape
# ---------------------------------------------------------------------------


@router.post("/batch")
async def batch_scrape(
    request: BatchScrapeRequest,
    ctx: AppContext = Depends(context_dep),
) -> BatchScrapeResponse:
    start = time.monotonic()
    results = await scrape_many(
        request.urls,
        use_proxy=request.use_proxy,
        fast=request.fast,
    )
    elapsed = round((time.monotonic() - start) * 1000, 1)
    return BatchScrapeResponse(
        status="success",
        execution_time_ms=elapsed,
        results=[r.to_dict() for r in results],
    )


# ---------------------------------------------------------------------------
# Content save
# ---------------------------------------------------------------------------


@router.post("/content/save")
async def content_save(
    request: ContentSaveRequest,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, str]:
    if not has_ext("cache"):
        raise HTTPException(status_code=503, detail="Cache backend not configured")

    cache = get_ext("cache")
    url_info = get_url_info(request.url)
    await cache.set(
        key=url_info.unique_page_name,
        url=request.url,
        domain=url_info.full_domain,
        content=request.content,
        content_type=request.content_type,
        char_count=request.char_count,
    )
    return {"status": "saved", "page_name": url_info.unique_page_name}


# ---------------------------------------------------------------------------
# Retry queue
# ---------------------------------------------------------------------------


@router.get("/queue/pending")
async def queue_pending(
    tier: str = "desktop",
    limit: int = 10,
    domain: str | None = None,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, Any]:
    now = datetime.now(UTC)
    await ScrapeRetryQueue.update_where(
        {"status": "claimed", "claim_expires_at__lt": now},
        status="pending",
        claimed_by=None,
        claimed_at=None,
        claim_expires_at=None,
    )

    query = ScrapeRetryQueue.filter(status="pending", tier=tier)
    if domain:
        query = query.filter(domain_name=domain)
    rows = (
        await query.order_by("created_at")
        .limit(limit)
        .values("id", "target_url", "domain_name", "failure_reason", "tier", "created_at")
    )

    total = await ScrapeRetryQueue.count(status="pending", tier=tier)

    return {
        "items": [
            {
                "id": str(r["id"]),
                "target_url": r["target_url"],
                "domain_name": r["domain_name"],
                "failure_reason": r["failure_reason"],
                "tier": r["tier"],
                "created_at": r["created_at"].isoformat(),
            }
            for r in rows
        ],
        "total_pending": total,
    }


@router.post("/queue/claim")
async def queue_claim(
    request: RetryClaimRequest,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, list[str]]:
    now = datetime.now(UTC)
    expires = now + timedelta(minutes=request.claim_ttl_minutes)
    claimed: list[str] = []
    already_claimed: list[str] = []

    for item_id in request.item_ids:
        result = await ScrapeRetryQueue.update_where(
            {"id": item_id, "status": "pending"},
            status="claimed",
            claimed_by=request.client_id,
            claimed_at=now,
            claim_expires_at=expires,
        )
        if result.rows_affected == 1:
            claimed.append(item_id)
        else:
            already_claimed.append(item_id)

    return {"claimed": claimed, "already_claimed": already_claimed}


@router.post("/queue/submit")
async def queue_submit(
    request: RetrySubmitRequest,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, bool]:
    now = datetime.now(UTC)
    result = await ScrapeRetryQueue.update_where(
        {"id": request.queue_item_id, "status": "claimed"},
        status="completed",
        completed_at=now,
        attempt_count=F("attempt_count") + 1,
    )
    return {"success": result.rows_affected == 1}


@router.post("/queue/fail")
async def queue_fail(
    request: RetryFailRequest,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, bool]:
    if request.promote_to_extension:
        result = await ScrapeRetryQueue.update_where(
            {"id": request.queue_item_id, "status": "claimed", "tier": "desktop"},
            status="pending",
            tier="extension",
            last_error=request.error,
            attempt_count=F("attempt_count") + 1,
            claimed_by=None,
            claimed_at=None,
            claim_expires_at=None,
        )
    else:
        result = await ScrapeRetryQueue.update_where(
            {"id": request.queue_item_id, "status": "claimed"},
            status="failed",
            last_error=request.error,
            attempt_count=F("attempt_count") + 1,
        )
    return {"success": result.rows_affected == 1}


@router.get("/queue/stats")
async def queue_stats(ctx: AppContext = Depends(context_dep)) -> dict[str, Any]:
    rows = await (
        ScrapeRetryQueue.filter()
        .annotate(count=Count("*"))
        .group_by("status", "tier")
        .order_by("status", "tier")
        .values("status", "tier", "count")
    )
    stats: dict[str, Any] = {"total": 0, "by_status": {}, "by_tier": {}}
    for r in rows:
        s, t, c = r["status"], r["tier"], r["count"]
        stats["total"] += c
        stats["by_status"][s] = stats["by_status"].get(s, 0) + c
        stats["by_tier"].setdefault(t, {})[s] = c
    return stats


# ---------------------------------------------------------------------------
# Domain config
# ---------------------------------------------------------------------------


@router.get("/config/domains")
async def list_domains(ctx: AppContext = Depends(context_dep)) -> dict[str, Any]:
    if not has_ext("domain_config"):
        return {"domains": []}
    config_store = get_ext("domain_config")
    domains = config_store.all_domains
    return {
        "domains": [
            {
                "id": str(d.id),
                "url": d.url,
                "common_name": d.common_name,
                "scrape_allowed": d.scrape_allowed,
                "proxy_type": d.settings.proxy_type if d.settings else "datacenter",
            }
            for d in domains
        ]
    }


@router.post("/config/domains")
async def upsert_domain(
    request: DomainUpsertRequest,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, Any]:
    if not has_ext("domain_config"):
        raise HTTPException(status_code=503, detail="Domain config store not configured")
    config_store = get_ext("domain_config")
    result = await config_store.upsert_domain(
        url=request.url,
        common_name=request.common_name,
        scrape_allowed=request.scrape_allowed,
        enabled=request.enabled,
        proxy_type=request.proxy_type,
    )
    return result
