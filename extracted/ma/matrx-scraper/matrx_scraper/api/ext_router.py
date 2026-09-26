"""
External endpoints — batch scrape, content save, retry queue, domain config.

Depends on: matrx_connect (AppContext, context_dep)
No aidream imports.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from matrx_connect import AppContext, context_dep
from matrx_orm import Count, F
from pydantic import BaseModel, Field

# ``confirm_request_organization`` first ships in matrx-connect 0.1.116 (this
# package's floor). The import is guarded because CI's dependency-floor test
# reads PUBLISHED tags as truth and the symbol ships in the same change as its
# first use here: a stale matrx-connect refuses every organization-scoped call
# by name instead of failing to import the router. The sibling-floor guard
# keeps our own deployment on the floor.
try:
    from matrx_connect.service_auth import confirm_request_organization
except ImportError:  # pragma: no cover — matrx-connect < 0.1.116

    def confirm_request_organization(ctx: AppContext, claimed: str | None = None) -> str:  # type: ignore[misc]
        raise RuntimeError(
            "the installed matrx-connect does not export confirm_request_organization; "
            "upgrade matrx-connect to >= 0.1.117 (the floor this package declares)."
        )


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
    #: SOURCE-CONVERGENCE §4.1 — the batch's "Save" is a Keep: every page lands as a Source, and
    #: these say whether the person kept them and where they are filed (``platform.associations``
    #: targets: ``{"entity_type", "entity_id", "label"?}``). Unkept pages still land, deferred.
    keep: bool = False
    attach_to: list[dict[str, Any]] = Field(default_factory=list)


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
    #: Who captured it (SOURCE-CONVERGENCE §4.4 / §4.2). Desktop (matrx-local) reads through the
    #: person's own computer (`residential`); the extension's scrape tool reads in the person's own
    #: browser (`own_browser`). Explicit, never guessed from a header.
    origin_client: Literal["local", "extension"] = "local"
    keep: bool = False
    attach_to: list[dict[str, Any]] = Field(default_factory=list)


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
    # The organization this batch acts in — the admitted one, and only it,
    # resolved HERE at the boundary and carried down. This lane runs uncached
    # today, so nothing lands in `scraper.scrape_parsed_page` from it; the
    # moment it is given a cache, the org-scoped write already has its tenant
    # instead of discovering it needs one at the INSERT.
    organization_id = confirm_request_organization(ctx)
    start = time.monotonic()
    results = await scrape_many(
        request.urls,
        use_proxy=request.use_proxy,
        fast=request.fast,
        organization_id=organization_id,
        # WHO this batch is for: only this person's own home computer may be
        # used to retry a page the site blocked.
        acting_user_id=ctx.user_id,
    )
    # THE RESULT BOUNDARY (SOURCE-CONVERGENCE §4.1): each successful page becomes a Source before
    # the response. Unwired raises; a page that did not land carries `notices` saying why.
    from matrx_scraper.source_landing import land_page_result, stamp_page

    payload: list[dict[str, Any]] = []
    for r in results:
        page = r.to_dict()
        if r.success:
            outcome = await land_page_result(
                r,
                organization_id=organization_id,
                user_id=str(ctx.user_id or "") or None,
                origin_client="web",
                keep=request.keep,
                attach_to=request.attach_to,
            )
            page = stamp_page(page, outcome)
        payload.append(page)
    elapsed = round((time.monotonic() - start) * 1000, 1)
    return BatchScrapeResponse(
        status="success",
        execution_time_ms=elapsed,
        results=payload,
    )


# ---------------------------------------------------------------------------
# Content save
# ---------------------------------------------------------------------------


@router.post("/content/save")
async def content_save(
    request: ContentSaveRequest,
    ctx: AppContext = Depends(context_dep),
) -> dict[str, Any]:
    """Save a page a person's own computer or browser read — as a Source (SOURCE-CONVERGENCE §4.4).

    Desktop (matrx-local) and the extension's scrape tool push the parse they made here. It lands
    through the landing door (the identity row in ``scraper.scrape_parsed_page`` is created there,
    owned by the person) and the answer carries the Source id. The person is the one this request
    was admitted for (the forwarded JWT); the organization is the admitted one. Nothing is written
    to the page cache: the cache is the scraper's own, never a Source body (§1 rule 5).
    """
    from matrx_scraper.source_landing import (
        SourceLandingFailed,
        land_result,
        page_landing,
    )

    organization_id = confirm_request_organization(ctx)
    user_id = str(ctx.user_id or "").strip()
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "sign_in_required",
                "message": "Sign in to save a page; a saved page always belongs to a person.",
                "remedy": "sign_in",
            },
        )
    url_info = get_url_info(request.url)
    parsed = {
        "success": True,
        "url": request.url,
        "response_url": request.content.get("response_url") or request.content.get("final_url") or request.url,
        "title": request.content.get("title") or request.page_name,
        **request.content,
    }
    landing = page_landing(
        parsed,
        organization_id=organization_id,
        user_id=user_id,
        origin_client=request.origin_client,
        capture_method="own_browser" if request.origin_client == "extension" else "residential",
        keep=request.keep,
        visibility="personal",
        attach_to=request.attach_to,
    )
    if landing is None:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "nothing_captured",
                "message": "There was no text in this page, so there is nothing to save.",
                "remedy": "capture_the_page_again",
            },
        )
    try:
        landed = await land_result(landing)
    except SourceLandingFailed as exc:
        raise HTTPException(status_code=502, detail=exc.as_notice()) from None
    return {
        "status": "saved",
        "page_name": url_info.unique_page_name,
        "processed_document_id": landed["processed_document_id"],
        "source_id": landed.get("source_id"),
        "notices": list(landed.get("notices") or []),
    }


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
