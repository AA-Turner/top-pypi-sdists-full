"""Google Search Console sync — pulls the bound property's Search Analytics
into ``web.gsc_page_stat`` and feeds unknown URLs into the canonical
``web.page`` registry (provenance ``'gsc'`` for NEW rows only).

Importable service functions only (no HTTP-framework concerns) so the same
operation runs as the standalone streaming command and — later — as a
workflow node. All DB access is matrx-orm; writes are batched and idempotent
(stats upsert on ``(page_id, date)``, pages on ``(site_id, url_hash)``).

The site binds GSC via ``web.site.integrations.marketing.providers.
google_search_console`` = ``{enabled, credential_ref, resource_ref}`` where
``credential_ref`` points at ``users.integration_connections`` — safe
metadata plus a canonical-vault reference. The refresh token itself is NOT
owned by this package, so resolving it is an **injection seam**, not a
hardcoded destination:

* **Any host** (aidream in-process, matrx-local, a customer with their own
  Google OAuth store) registers a resolver once —
  ``configure_ext(google_credential_resolver=<async callable>)`` — and this
  module calls it. That is the ONE sanctioned path.
* **The Matrx standalone scraper microservice** has no vault of its own and
  no host process to inject one, so when no resolver is registered it falls
  back to the platform bridge it is deployed alongside:
  ``GET {AIDREAM_URL}/api/google-integrations/internal/credential``
  (``Authorization: Bearer $AIDREAM_SERVICE_TOKEN`` + ``X-Matrx-User-Id``).
  That bridge needs no shared encryption env. A consumer that is not that
  deployment never touches it — it injects a resolver instead, and the
  "not configured" error says so first.

Every failure is loud; nothing falls back silently.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date as date_type, timedelta
from typing import Any
from urllib.parse import quote, urlparse

import httpx

from matrx_orm import transaction
from matrx_utils import utcnow

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.crawler import _is_same_host, _normalise_url
from matrx_scraper.db.models_web import (
    GscPageStat,
    Site as WebSite,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.performance import GscClient
from matrx_scraper.web_crawl.contracts import GscSyncSummary
from matrx_scraper.web_crawl.url_identity import upsert_observed_page_urls

logger = logging.getLogger(__name__)

_PAGE_BATCH_SIZE = 500
_SEARCH_ANALYTICS_ROW_LIMIT = 25_000
_SEARCH_ANALYTICS_ENDPOINT = (
    "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
)
_SITEMAPS_ENDPOINT = "https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps"

# GSC data lags reality; the freshest reliably-complete day is ~2 days back.
_GSC_DATA_LAG_DAYS = 2

ProgressCallback = Callable[[str, GscSyncSummary], Awaitable[None]]


class GscSyncResult:
    """Outcome of one GSC sync run."""

    def __init__(self, summary: GscSyncSummary) -> None:
        self.summary = summary


# ---------------------------------------------------------------------------
# Pure parts (unit-tested without a DB or network)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GscBinding:
    enabled: bool
    credential_ref: str
    resource_ref: str


def parse_gsc_binding(integrations: Any) -> GscBinding:
    """Extract and validate the site's GSC binding. Loud on every gap."""

    if not isinstance(integrations, dict):
        raise ValueError("site.integrations is not an object; cannot resolve a GSC binding")
    marketing = integrations.get("marketing")
    providers = marketing.get("providers") if isinstance(marketing, dict) else None
    binding = providers.get("google_search_console") if isinstance(providers, dict) else None
    if not isinstance(binding, dict):
        raise ValueError(
            "site has no integrations.marketing.providers.google_search_console binding"
        )
    enabled = bool(binding.get("enabled"))
    credential_ref = binding.get("credential_ref")
    resource_ref = binding.get("resource_ref")
    if not enabled:
        raise ValueError("the site's Google Search Console binding is disabled")
    if not isinstance(credential_ref, str) or not credential_ref.strip():
        raise ValueError("the GSC binding is missing credential_ref")
    if not isinstance(resource_ref, str) or not resource_ref.strip():
        raise ValueError("the GSC binding is missing resource_ref (the GSC property)")
    return GscBinding(
        enabled=True,
        credential_ref=credential_ref.strip(),
        resource_ref=resource_ref.strip(),
    )


@dataclass(frozen=True)
class GscDailyPageRow:
    date: date_type
    page_url: str
    clicks: int
    impressions: int
    ctr: float
    position: float | None


@dataclass(frozen=True)
class GscSearchAnalyticsPage:
    payload: dict[str, Any]
    headers: dict[str, str]
    status_code: int
    # Exact outbound request evidence (DEF-1x evidence-parity contract) — the
    # method is always POST for searchAnalytics.query; endpoint is the fully
    # resolved per-property URL actually called.
    endpoint: str = ""
    method: str = "POST"


def parse_search_analytics_rows(payload: dict[str, Any]) -> list[GscDailyPageRow]:
    """Convert one searchAnalytics.query response page (dimensions
    ``["date", "page"]``) into typed daily rows. Malformed rows are skipped
    loudly via the returned count difference — the caller compares lengths."""

    rows = payload.get("rows")
    if rows is None:
        return []
    if not isinstance(rows, list):
        raise ValueError("search analytics response 'rows' is not a list")
    parsed: list[GscDailyPageRow] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        keys = row.get("keys")
        if not isinstance(keys, list) or len(keys) != 2:
            continue
        raw_date, raw_page = keys
        try:
            parsed_date = date_type.fromisoformat(str(raw_date))
        except ValueError:
            continue
        page_url = str(raw_page).strip()
        if not page_url:
            continue
        position = row.get("position")
        parsed.append(
            GscDailyPageRow(
                date=parsed_date,
                page_url=page_url,
                clicks=int(row.get("clicks", 0) or 0),
                impressions=int(row.get("impressions", 0) or 0),
                ctr=float(row.get("ctr", 0) or 0),
                position=float(position) if position is not None else None,
            )
        )
    return parsed


def partition_rows_by_scope(
    rows: list[GscDailyPageRow],
    *,
    root_host: str,
) -> tuple[dict[str, list[GscDailyPageRow]], int]:
    """Group in-scope rows by NORMALIZED page URL; count out-of-scope rows.

    A row is in scope when its URL's host matches the site's root host
    (subdomains included — an ``sc-domain:`` property reports every
    subdomain, and www/apex variants must not be dropped)."""

    in_scope: dict[str, list[GscDailyPageRow]] = {}
    skipped = 0
    for row in rows:
        parsed = urlparse(row.page_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            skipped += 1
            continue
        if not _is_same_host(row.page_url, root_host, True):
            skipped += 1
            continue
        normalized = _normalise_url(row.page_url)
        in_scope.setdefault(normalized, []).append(row)
    # Distinct GSC URLs (www/apex, trailing slash) can normalize to the same
    # page, leaving two rows for one (page, date) — which a single
    # ``ON CONFLICT (page_id, date)`` upsert batch rejects outright
    # (CardinalityViolation). Merge them here with GSC's own aggregation
    # semantics so every downstream consumer sees one row per page per day.
    return (
        {url: merge_rows_by_date(url, rows) for url, rows in in_scope.items()},
        skipped,
    )


def merge_rows_by_date(normalized_url: str, rows: list[GscDailyPageRow]) -> list[GscDailyPageRow]:
    """Collapse same-date rows for one normalized page: clicks/impressions
    sum; ctr is recomputed from the sums; position is the
    impressions-weighted mean (plain mean when no impressions)."""

    by_date: dict[date_type, list[GscDailyPageRow]] = {}
    for row in rows:
        by_date.setdefault(row.date, []).append(row)
    merged: list[GscDailyPageRow] = []
    for day, day_rows in sorted(by_date.items()):
        if len(day_rows) == 1:
            merged.append(day_rows[0])
            continue
        clicks = sum(r.clicks for r in day_rows)
        impressions = sum(r.impressions for r in day_rows)
        positions = [r.position for r in day_rows if r.position is not None]
        weighted_impressions = sum(r.impressions for r in day_rows if r.position is not None)
        if not positions:
            position: float | None = None
        elif weighted_impressions > 0:
            position = (
                sum(r.position * r.impressions for r in day_rows if r.position is not None)
                / weighted_impressions
            )
        else:
            position = sum(positions) / len(positions)
        merged.append(
            GscDailyPageRow(
                date=day,
                page_url=normalized_url,
                clicks=clicks,
                impressions=impressions,
                ctr=(clicks / impressions) if impressions else 0.0,
                position=position,
            )
        )
    return merged


def parse_submitted_sitemaps(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize the GSC submitted-sitemaps listing into summary entries."""

    entries = payload.get("sitemap")
    if entries is None:
        return []
    if not isinstance(entries, list):
        raise ValueError("GSC sitemaps response 'sitemap' is not a list")
    parsed: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            continue
        parsed.append(
            {
                "path": path,
                "last_submitted": entry.get("lastSubmitted"),
                "last_downloaded": entry.get("lastDownloaded"),
                "is_pending": bool(entry.get("isPending", False)),
                "errors": int(entry.get("errors", 0) or 0),
                "warnings": int(entry.get("warnings", 0) or 0),
            }
        )
    return parsed


def compute_sync_window(
    *, days: int, today: date_type | None = None
) -> tuple[date_type, date_type]:
    """Last ``days`` daily buckets ending at GSC's freshest complete day."""

    if days < 1:
        raise ValueError("days must be >= 1")
    end = (today or date_type.today()) - timedelta(days=_GSC_DATA_LAG_DAYS)
    start = end - timedelta(days=days - 1)
    return start, end


# ---------------------------------------------------------------------------
# Credential resolution (canonical vault, via aidream's internal endpoint)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GoogleConnectionCredential:
    refresh_token: str
    client_id: str
    client_secret: str


def _aidream_internal_config() -> tuple[str, str]:
    base = os.environ.get("AIDREAM_URL", "").strip().rstrip("/")
    token = os.environ.get("AIDREAM_SERVICE_TOKEN", "").strip()
    if not base or not token:
        raise RuntimeError(
            "GSC credential resolution is not configured. Register a resolver — "
            "matrx_scraper.configure_ext(google_credential_resolver=<async callable "
            "returning refresh_token/client_id/client_secret>) — which is how every "
            "host (aidream in-process, matrx-local, a standalone install with its own "
            "Google OAuth store) supplies this. The Matrx standalone scraper "
            "microservice instead relies on the platform bridge and needs AIDREAM_URL "
            "+ AIDREAM_SERVICE_TOKEN set on that deployment."
        )
    return base, token


def _coerce_credential(payload: Any, *, source: str) -> GoogleConnectionCredential:
    """Accept either a GoogleConnectionCredential or any object/mapping carrying
    the three required fields, so a host resolver never has to import our type."""

    if isinstance(payload, GoogleConnectionCredential):
        return payload
    if isinstance(payload, dict):
        refresh_token = payload.get("refresh_token")
        client_id = payload.get("client_id")
        client_secret = payload.get("client_secret")
    else:
        refresh_token = getattr(payload, "refresh_token", None)
        client_id = getattr(payload, "client_id", None)
        client_secret = getattr(payload, "client_secret", None)
    if not refresh_token or not client_id or not client_secret:
        raise RuntimeError(
            f"{source} returned an incomplete Google credential — "
            "refresh_token/client_id/client_secret are all required"
        )
    return GoogleConnectionCredential(
        refresh_token=str(refresh_token),
        client_id=str(client_id),
        client_secret=str(client_secret),
    )


async def resolve_google_credential(
    *,
    credential_ref: str,
    site_organization_id: str,
    user_id: str,
    resource_type: str | None = None,
    resource_ref: str | None = None,
    site_id: str | None = None,
    provider_binding_key: str | None = None,
) -> GoogleConnectionCredential:
    """Resolve the bound connection's refresh token + OAuth client.

    Uses the host-injected ``google_credential_resolver`` when one is
    registered (``configure_ext``) — that is the path every embedded host
    takes, and it is what makes this module usable outside the Matrx
    scraper microservice. With no resolver registered it falls back to the
    platform bridge that microservice is deployed alongside. The host
    re-authorizes ownership (requesting user or the site's organization);
    every failure is loud.

    ``resource_type``/``resource_ref`` (+ optional ``site_id``/
    ``provider_binding_key``) forward the WS-6 exact-resource-binding check
    (DEF-24) through to aidream — this legacy GSC-sync credential chain now
    verifies the same live ``(connection, resource)`` tuple the SEO
    collector verifies, not just connection ownership."""

    if has_ext("google_credential_resolver"):
        resolved = await get_ext("google_credential_resolver")(
            credential_ref=credential_ref,
            site_organization_id=site_organization_id,
            user_id=user_id,
            resource_type=resource_type,
            resource_ref=resource_ref,
            site_id=site_id,
            provider_binding_key=provider_binding_key,
        )
        return _coerce_credential(resolved, source="google_credential_resolver")

    base, token = _aidream_internal_config()
    url = f"{base}/api/google-integrations/internal/credential"
    params: dict[str, str] = {
        "connection_id": credential_ref,
        "organization_id": site_organization_id,
    }
    if resource_type:
        params["resource_type"] = resource_type
    if resource_ref:
        params["resource_ref"] = resource_ref
    if site_id:
        params["site_id"] = site_id
    if provider_binding_key:
        params["provider_binding_key"] = provider_binding_key
    async with httpx.AsyncClient(timeout=30.0) as http:
        response = await http.get(
            url,
            params=params,
            headers={
                "Authorization": f"Bearer {token}",
                "X-Matrx-User-Id": user_id,
            },
        )
    if response.status_code >= 400:
        raise RuntimeError(
            f"aidream could not resolve GSC credential {credential_ref}: "
            f"HTTP {response.status_code} {response.text[:300]}"
        )
    payload = response.json()
    refresh_token = payload.get("refresh_token") if isinstance(payload, dict) else None
    client_id = payload.get("client_id") if isinstance(payload, dict) else None
    client_secret = payload.get("client_secret") if isinstance(payload, dict) else None
    if not refresh_token or not client_id or not client_secret:
        raise RuntimeError(
            f"aidream returned an incomplete credential for {credential_ref} — "
            "refresh_token/client_id/client_secret are all required"
        )
    return GoogleConnectionCredential(
        refresh_token=str(refresh_token),
        client_id=str(client_id),
        client_secret=str(client_secret),
    )


def build_gsc_client(credential: GoogleConnectionCredential) -> GscClient:
    """A refresh-token GscClient on the connection's own OAuth client (the
    token refresh MUST use the client the token was minted for)."""

    return GscClient(
        client_id=credential.client_id,
        client_secret=credential.client_secret,
        refresh_token=credential.refresh_token,
    )


# ---------------------------------------------------------------------------
# Google API fetchers
# ---------------------------------------------------------------------------


async def fetch_search_analytics_rows(
    client: GscClient,
    *,
    property_ref: str,
    start: date_type,
    end: date_type,
    row_limit: int = _SEARCH_ANALYTICS_ROW_LIMIT,
) -> list[GscDailyPageRow]:
    """Fully paginated daily (date, page) Search Analytics query."""

    rows: list[GscDailyPageRow] = []
    start_row = 0
    while True:
        body = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": ["date", "page"],
            "rowLimit": row_limit,
            "startRow": start_row,
            "dataState": "final",
        }
        response = await fetch_search_analytics_page(
            client,
            property_ref=property_ref,
            request_body=body,
        )
        payload = response.payload
        raw_count = len(payload.get("rows") or [])
        rows.extend(parse_search_analytics_rows(payload))
        if raw_count < row_limit:
            return rows
        start_row += raw_count


async def fetch_search_analytics_page(
    client: GscClient,
    *,
    property_ref: str,
    request_body: dict[str, Any],
    raise_for_status: bool = True,
) -> GscSearchAnalyticsPage:
    """Execute one raw Search Analytics page through the canonical GSC auth client."""

    endpoint = _SEARCH_ANALYTICS_ENDPOINT.format(site=quote(property_ref, safe=""))
    access_token = await client.access_token()
    async with httpx.AsyncClient(timeout=client.timeout) as http:
        response = await http.post(
            endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            json=request_body,
        )
    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"GSC search analytics returned non-JSON HTTP {response.status_code}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError("GSC search analytics response must be a JSON object")
    result = GscSearchAnalyticsPage(
        payload=payload,
        headers=dict(response.headers),
        status_code=response.status_code,
        endpoint=endpoint,
        method="POST",
    )
    if raise_for_status and response.status_code >= 400:
        raise RuntimeError(
            f"GSC search analytics query failed for {property_ref!r}: "
            f"HTTP {response.status_code} {response.text[:300]}"
        )
    return result


async def fetch_submitted_sitemaps(
    client: GscClient,
    *,
    property_ref: str,
) -> list[dict[str, Any]]:
    endpoint = _SITEMAPS_ENDPOINT.format(site=quote(property_ref, safe=""))
    access_token = await client.access_token()
    async with httpx.AsyncClient(timeout=client.timeout) as http:
        response = await http.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code >= 400:
        raise RuntimeError(
            f"GSC sitemaps listing failed for {property_ref!r}: "
            f"HTTP {response.status_code} {response.text[:300]}"
        )
    return parse_submitted_sitemaps(response.json())


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


async def upsert_gsc_pages_for_urls(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    normalized_urls: list[str],
) -> dict[str, str]:
    """Ensure a canonical ``web.page`` row per URL; return url -> page_id.

    New rows are born with ``provenance='gsc'``. Existing rows only advance
    ``last_seen`` — provenance, status, intent fields stay untouched (same
    discipline as sitemap sync)."""

    return await upsert_observed_pages_for_urls(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        normalized_urls=normalized_urls,
        provenance="gsc",
    )


async def upsert_observed_pages_for_urls(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    normalized_urls: list[str],
    provenance: str,
) -> dict[str, str]:
    """Ensure canonical pages for URLs observed by an external site provider."""

    resolutions = await upsert_observed_page_urls(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        urls=normalized_urls,
        provenance=provenance,
    )
    return {
        normalized: resolution.canonical_page_id for normalized, resolution in resolutions.items()
    }


async def _upsert_page_stats(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    grouped: dict[str, list[GscDailyPageRow]],
    page_ids: dict[str, str],
) -> int:
    stat_rows: list[dict[str, Any]] = []
    for normalized, rows in grouped.items():
        page_id = page_ids[normalized]
        for row in rows:
            stat_rows.append(
                {
                    "organization_id": organization_id,
                    "created_by": user_id,
                    "site_id": site_id,
                    "page_id": page_id,
                    "date": row.date,
                    "clicks": row.clicks,
                    "impressions": row.impressions,
                    "ctr": row.ctr,
                    "position": row.position,
                }
            )
    # Last line of defense for the (page_id, date) arbiter: if any two rows
    # still target one key (e.g. two normalized URLs resolving to one page),
    # merge instead of letting the whole sync die on CardinalityViolation.
    by_key: dict[tuple[str, Any], dict[str, Any]] = {}
    for row in stat_rows:
        key = (row["page_id"], row["date"])
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = row
            continue
        merged_impressions = existing["impressions"] + row["impressions"]
        positions = [
            (p, i)
            for p, i in (
                (existing["position"], existing["impressions"]),
                (row["position"], row["impressions"]),
            )
            if p is not None
        ]
        weighted = sum(i for _, i in positions)
        existing["clicks"] += row["clicks"]
        existing["impressions"] = merged_impressions
        existing["ctr"] = existing["clicks"] / merged_impressions if merged_impressions else 0.0
        existing["position"] = (
            sum(p * i for p, i in positions) / weighted
            if positions and weighted > 0
            else (sum(p for p, _ in positions) / len(positions) if positions else None)
        )
    deduped_rows = list(by_key.values())
    for start in range(0, len(deduped_rows), _PAGE_BATCH_SIZE):
        batch = deduped_rows[start : start + _PAGE_BATCH_SIZE]
        async with transaction(WEB_DB_NAME):
            await GscPageStat.bulk_upsert(
                batch,
                on_conflict=["page_id", "date"],
                update_fields=["clicks", "impressions", "ctr", "position"],
            )
    return len(deduped_rows)


async def _write_site_sync_state(
    site_id: str,
    summary: GscSyncSummary,
    *,
    completed: bool,
) -> None:
    updates: dict[str, Any] = {"gsc_sync": summary.model_dump(mode="json")}
    if completed:
        updates["gsc_synced_at"] = utcnow()
    async with transaction(WEB_DB_NAME):
        updated = await WebSite.update_where({"id": site_id}, **updates)
    if updated.rows_affected != 1:
        raise LookupError(f"site {site_id} could not record its GSC sync state")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


async def _report(
    on_progress: ProgressCallback | None,
    message: str,
    summary: GscSyncSummary,
) -> None:
    if on_progress is not None:
        await on_progress(message, summary)


async def sync_site_gsc(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    root_url: str,
    integrations: Any,
    days: int = 28,
    on_progress: ProgressCallback | None = None,
) -> GscSyncResult:
    """Pull the bound GSC property into ``web.gsc_page_stat`` + ``web.page``.

    Re-runnable and idempotent. On ANY failure the error is recorded to
    ``web.site.gsc_sync`` before re-raising — a failed sync is never silent
    and never masquerades as a completed one (``gsc_synced_at`` only advances
    on success)."""

    binding = parse_gsc_binding(integrations)
    start, end = compute_sync_window(days=days)
    summary = GscSyncSummary(property=binding.resource_ref, days=days)
    try:
        await _report(
            on_progress,
            f"Resolving the Google credential for {binding.resource_ref}…",
            summary,
        )
        credential = await resolve_google_credential(
            credential_ref=binding.credential_ref,
            site_organization_id=organization_id,
            user_id=user_id,
            resource_type="search_console_property",
            resource_ref=binding.resource_ref,
            site_id=site_id,
            provider_binding_key="google_search_console",
        )
        client = build_gsc_client(credential)

        await _report(
            on_progress,
            f"Querying Search Analytics {start.isoformat()} → {end.isoformat()}…",
            summary,
        )
        analytics_rows = await fetch_search_analytics_rows(
            client,
            property_ref=binding.resource_ref,
            start=start,
            end=end,
        )
        root_host = urlparse(root_url).netloc.lower()
        grouped, skipped = partition_rows_by_scope(analytics_rows, root_host=root_host)
        summary.skipped_out_of_scope = skipped
        if skipped:
            summary.errors.append(
                f"skipped {skipped} search-analytics rows outside host {root_host}"
            )
        summary.pages = len(grouped)
        await _report(
            on_progress,
            f"Fetched {len(analytics_rows)} daily rows across {len(grouped)} pages…",
            summary,
        )

        page_ids = await upsert_gsc_pages_for_urls(
            site_id=site_id,
            organization_id=organization_id,
            user_id=user_id,
            normalized_urls=list(grouped),
        )
        summary.stats_rows = await _upsert_page_stats(
            site_id=site_id,
            organization_id=organization_id,
            user_id=user_id,
            grouped=grouped,
            page_ids=page_ids,
        )
        await _report(
            on_progress,
            f"Upserted {summary.stats_rows} daily page stats…",
            summary,
        )

        try:
            summary.submitted_sitemaps = await fetch_submitted_sitemaps(
                client,
                property_ref=binding.resource_ref,
            )
        except Exception as exc:  # non-fatal, but LOUD in the summary
            summary.errors.append(f"submitted-sitemaps listing failed: {exc}")
            logger.warning(
                "GSC submitted-sitemaps listing failed for site %s", site_id, exc_info=True
            )
    except Exception as exc:
        summary.errors.append(f"{type(exc).__name__}: {exc}"[:2_000])
        try:
            await _write_site_sync_state(site_id, summary, completed=False)
        except Exception:
            logger.exception("failed to record failed GSC sync state for site %s", site_id)
        raise

    await _write_site_sync_state(site_id, summary, completed=True)
    return GscSyncResult(summary)


__all__ = [
    "GoogleConnectionCredential",
    "GscBinding",
    "GscDailyPageRow",
    "GscSearchAnalyticsPage",
    "GscSyncResult",
    "ProgressCallback",
    "build_gsc_client",
    "compute_sync_window",
    "fetch_search_analytics_rows",
    "fetch_search_analytics_page",
    "fetch_submitted_sitemaps",
    "parse_gsc_binding",
    "parse_search_analytics_rows",
    "parse_submitted_sitemaps",
    "partition_rows_by_scope",
    "resolve_google_credential",
    "sync_site_gsc",
    "upsert_gsc_pages_for_urls",
    "upsert_observed_pages_for_urls",
]
