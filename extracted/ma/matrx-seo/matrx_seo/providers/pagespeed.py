from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable, Mapping, Sequence
from contextvars import ContextVar
from datetime import UTC, datetime
from decimal import Decimal
from time import monotonic
from typing import Any, Literal, Protocol
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..adapters import ProviderExecutionContext, SeoProviderAdapter, SeoProviderOperation
from ..contracts import (
    CollectionReceipt,
    CollectionRequest,
    CollectionTrigger,
    CredentialReferenceKind,
    HostBindingRequest,
    NormalizationContext,
    PagePerformanceObservation,
    ProviderCallRecord,
    ProviderResponse,
    ResolvedCredential,
    SeoCapability,
    SeoObservation,
)
from ..identity import stable_hash
from ..rank_matching import canonicalize_rank_url
from ..service import SeoCollectionService

PAGESPEED_INSIGHTS_OPERATION = SeoProviderOperation(
    name="page_audit",
    capability=SeoCapability.PAGE_PERFORMANCE,
    credential_keys=("GOOGLE_PSI_API_KEY",),
)

# Evidence-only mirror of matrx_scraper.performance.PSI_ENDPOINT — the real
# transport lives host-side behind PsiClientLike; this package cannot depend
# on matrx-scraper, so the well-known public PSI v5 endpoint is duplicated
# here purely to label outbound-request evidence, never to perform the call.
PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

_RETRYABLE_HTTP_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})
_LAB_AUDITS = {
    "cumulative-layout-shift": "cls",
    "first-contentful-paint": "fcp_ms",
    "interactive": "tti_ms",
    "interaction-to-next-paint": "inp_ms",
    "largest-contentful-paint": "lcp_ms",
    "server-response-time": "ttfb_ms",
    "speed-index": "speed_index_ms",
    "total-blocking-time": "tbt_ms",
}
_ATTEMPT_BODY_LIMIT_BYTES = 16_000

# Score display modes worth persisting. `metricSavings` is Lighthouse 13's mode
# for EVERY performance opportunity (the `*-insight` audits plus the surviving
# `unused-*` / `unminified-*` ones); excluding it silently discarded the whole
# delivery fix-list, so it is kept and its savings are lifted out below.
_KEPT_SCORE_DISPLAY_MODES = frozenset(
    {"numeric", "binary", "error", "informative", "notApplicable", "metricSavings"}
)

# The delivery fix-list, by Lighthouse 13 audit id. `cache-insight` is
# deliberately ABSENT: caching is scored by its own catalogue item
# (`caching_policy`), and counting it here would double-charge one defect.
_DELIVERY_SAVINGS_AUDITS: tuple[str, ...] = (
    "render-blocking-insight",
    "document-latency-insight",
    "image-delivery-insight",
    "legacy-javascript-insight",
    "duplicated-javascript-insight",
    "font-display-insight",
    "unminified-css",
    "unminified-javascript",
    "unused-css-rules",
    "unused-javascript",
)

# Request kinds a cache policy is expected to cover. The HTML document is
# excluded — it is normally uncacheable by design, and counting it would push
# every dynamic site's caching score down for doing the right thing.
_STATIC_RESOURCE_TYPES = frozenset({"Script", "Stylesheet", "Image", "Font", "Media"})

_CACHE_OFFENDER_LIMIT = 50
_CACHE_URL_LIMIT = 300


class PageSpeedInsightsSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host_page_id: str
    url: str
    strategy: Literal["mobile", "desktop"]

    @field_validator("host_page_id")
    @classmethod
    def require_host_page(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("host_page_id must be nonblank")
        return normalized

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        parts = urlsplit(value.strip())
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            raise ValueError("PageSpeed URL must be an absolute HTTP(S) URL")
        if parts.username or parts.password:
            raise ValueError("PageSpeed URL cannot contain credentials")
        if parts.fragment:
            raise ValueError("PageSpeed URL cannot contain a fragment")
        normalized = canonicalize_rank_url(value)
        if not normalized:
            raise ValueError("PageSpeed URL could not be canonicalized")
        return normalized


class PageSpeedSampleJob(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    # Canonical web.site the sampled page belongs to. Required — PSI is always
    # page-scoped, and CollectionRequest.page_id requires a site_id (DEF-18:
    # settings.host_page_id must never be the only place page attribution lives).
    site_id: str
    target_ref: str
    observation_period: str
    settings: PageSpeedInsightsSettings
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND
    credential_reference_id: str | None = None
    credential_reference_kind: CredentialReferenceKind = CredentialReferenceKind.PLATFORM_SECRET
    request_id: str | None = None

    def to_collection_request(self) -> CollectionRequest:
        return CollectionRequest(
            organization_id=self.organization_id,
            created_by=self.created_by,
            capability=SeoCapability.PAGE_PERFORMANCE,
            operation=PAGESPEED_INSIGHTS_OPERATION.name,
            target_ref=self.target_ref,
            site_id=self.site_id,
            page_id=self.settings.host_page_id,
            observation_period=self.observation_period,
            settings=self.settings.model_dump(mode="json"),
            trigger=self.trigger,
            credential_reference_id=self.credential_reference_id,
            credential_reference_kind=self.credential_reference_kind,
            request_id=self.request_id,
        )


class PageSpeedAttemptEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    attempt: int
    fetched_at: datetime
    http_status: int | None = None
    error_message: str | None = None
    quota_headers: dict[str, str] = Field(default_factory=dict)
    body: dict[str, Any] | None = None
    body_preview_json: str | None = None
    body_truncated: bool = False
    body_checksum: str
    request_count: int = 1


class PsiSnapshotLike(Protocol):
    url: str
    strategy: str
    raw: dict[str, Any]
    error_message: str | None
    fetched_at: datetime
    request_count: int


class PsiClientLike(Protocol):
    async def fetch(self, url: str, *, strategy: str = "mobile") -> PsiSnapshotLike: ...


PsiClientFactory = Callable[[str], PsiClientLike]


class PageSpeedInsightsAdapter(SeoProviderAdapter):
    provider = "pagespeed_insights"
    capabilities = (SeoCapability.PAGE_PERFORMANCE,)
    operations = (PAGESPEED_INSIGHTS_OPERATION,)

    def __init__(
        self,
        *,
        client_factory: PsiClientFactory,
        max_concurrency: int = 2,
        min_interval_seconds: float = 0,
        max_attempts: int = 3,
        base_backoff_seconds: float = 1,
        sleeper: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if max_concurrency < 1 or max_attempts < 1:
            raise ValueError("max_concurrency and max_attempts must be positive")
        if min_interval_seconds < 0 or base_backoff_seconds < 0:
            raise ValueError("rate interval and retry backoff cannot be negative")
        self.client_factory = client_factory
        self.max_attempts = max_attempts
        self.min_interval_seconds = min_interval_seconds
        self.base_backoff_seconds = base_backoff_seconds
        self._sleeper = sleeper
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._pace_lock = asyncio.Lock()
        self._last_request_at = 0.0
        self._api_key: ContextVar[str | None] = ContextVar(
            f"pagespeed_api_key_{id(self)}", default=None
        )

    async def authenticate(self, credential: ResolvedCredential) -> None:
        api_key = credential.values.get("GOOGLE_PSI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GOOGLE_PSI_API_KEY credential is required")
        self._api_key.set(api_key)

    async def collect_response(
        self, request: CollectionRequest, execution: ProviderExecutionContext
    ) -> ProviderResponse:
        del execution
        if request.operation != PAGESPEED_INSIGHTS_OPERATION.name:
            raise ValueError(f"unsupported PageSpeed operation {request.operation!r}")
        settings = PageSpeedInsightsSettings.model_validate(request.settings)
        api_key = self._api_key.get()
        if not api_key:
            raise RuntimeError("PageSpeed adapter must be authenticated before collection")
        client = self.client_factory(api_key)
        snapshot, attempt_evidence = await self._fetch_with_retry(client, settings)
        payload = snapshot.raw if isinstance(snapshot.raw, dict) else {}
        fetched_at = _provider_timestamp(payload) or snapshot.fetched_at.astimezone(UTC)
        runtime_error = _mapping(_mapping(payload.get("lighthouseResult")).get("runtimeError"))
        error_message = snapshot.error_message
        if runtime_error:
            error_message = str(runtime_error.get("message") or runtime_error.get("code"))
        if error_message and not payload:
            payload = {
                "request": settings.model_dump(mode="json"),
                "error": {
                    "message": error_message,
                    "http_status": getattr(snapshot, "http_status", None),
                },
            }
        raw_envelope = {
            "provider_response": payload,
            "attempts": [evidence.model_dump(mode="json") for evidence in attempt_evidence],
        }
        call_key = "psi:" + stable_hash(
            {
                "url": settings.url,
                "strategy": settings.strategy,
                "analysis": _analysis_identity(payload) or fetched_at.isoformat(),
            }
        )
        status = getattr(snapshot, "http_status", None)
        request_evidence = {
            "method": "GET",
            "url": PSI_ENDPOINT,
            "headers": {},
            # PSI takes the credential as a `key` query parameter, not a
            # header — redact it in place so evidence never persists it.
            "params": {
                "url": settings.url,
                "strategy": settings.strategy,
                "category": ["PERFORMANCE", "ACCESSIBILITY", "BEST_PRACTICES", "SEO"],
                "key": "***",
            },
        }
        return ProviderResponse(
            raw=raw_envelope,
            fetched_at=fetched_at,
            provider_schema_version=_provider_schema_version(payload),
            external_task_id=call_key,
            call_records=[
                ProviderCallRecord(
                    provider_call_key=call_key,
                    external_task_id=call_key,
                    request_count=sum(evidence.request_count for evidence in attempt_evidence),
                    reported_cost=Decimal(0),
                    currency="USD",
                    fetched_at=fetched_at,
                    metadata={
                        "url": settings.url,
                        "strategy": settings.strategy,
                        "categories": [
                            "PERFORMANCE",
                            "ACCESSIBILITY",
                            "BEST_PRACTICES",
                            "SEO",
                        ],
                        "http_status": status,
                        "response_status": status,
                        "attempts": len(attempt_evidence),
                        "quota_headers": _quota_headers(getattr(snapshot, "response_headers", {})),
                        "request": request_evidence,
                        "pricing": "no_per_request_charge",
                    },
                )
            ],
            error=(
                {
                    "type": "PageSpeedInsightsError",
                    "message": error_message,
                    "http_status": status,
                    "runtime_error": runtime_error or None,
                }
                if error_message
                else None
            ),
        )

    async def normalize(
        self, response: ProviderResponse, context: NormalizationContext
    ) -> list[SeoObservation]:
        if not isinstance(response.raw, dict):
            raise TypeError("PageSpeed response must be an object")
        payload = _provider_payload(response.raw)
        settings = PageSpeedInsightsSettings.model_validate(context.request.settings)
        page = await context.resolve_host_binding(
            HostBindingRequest(resource_kind="web_page", resource_id=settings.host_page_id)
        )
        if canonicalize_rank_url(page.canonical_url) != settings.url:
            raise ValueError("PageSpeed URL does not match the canonical host page binding")

        lighthouse = _mapping(payload.get("lighthouseResult"))
        categories = _mapping(lighthouse.get("categories"))
        audits = _mapping(lighthouse.get("audits"))
        page_field = _field_experience(payload.get("loadingExperience"))
        origin_field = _field_experience(payload.get("originLoadingExperience"))
        observed_at = _provider_timestamp(payload) or response.fetched_at
        return [
            PagePerformanceObservation(
                page_id=page.page_id,
                site_id=page.site_id,
                strategy=settings.strategy,
                performance_score=_category_score(categories, "performance"),
                accessibility_score=_category_score(categories, "accessibility"),
                best_practices_score=_category_score(categories, "best-practices"),
                seo_score=_category_score(categories, "seo"),
                lighthouse={
                    "data_kind": "lab",
                    "strategy": settings.strategy,
                    "version": lighthouse.get("lighthouseVersion"),
                    "requested_url": lighthouse.get("requestedUrl"),
                    "final_url": lighthouse.get("finalUrl"),
                    "fetch_time": lighthouse.get("fetchTime"),
                    "category_scores": {
                        key: _category_score(categories, key)
                        for key in ("performance", "accessibility", "best-practices", "seo")
                    },
                    "metrics": _lab_metrics(audits),
                    "delivery": _delivery_facts(audits),
                    "environment": _mapping(lighthouse.get("environment")),
                    "config_settings": _mapping(lighthouse.get("configSettings")),
                    "timing": _mapping(lighthouse.get("timing")),
                },
                crux={
                    "data_kind": "field",
                    "window": "rolling_28_day",
                    "strategy_applies_to": "lighthouse_lab_only",
                    "page": page_field,
                    "origin": origin_field,
                },
                diagnostics={
                    "analysis_utc_timestamp": payload.get("analysisUTCTimestamp"),
                    "pagespeed_version": _mapping(payload.get("version")),
                    "captcha_result": payload.get("captchaResult"),
                    "run_warnings": lighthouse.get("runWarnings") or [],
                    "runtime_error": _mapping(lighthouse.get("runtimeError")),
                    "audits": _diagnostic_audits(audits),
                },
                observed_at=observed_at,
            )
        ]

    async def _fetch_with_retry(
        self,
        client: PsiClientLike,
        settings: PageSpeedInsightsSettings,
    ) -> tuple[PsiSnapshotLike, list[PageSpeedAttemptEvidence]]:
        snapshot: PsiSnapshotLike | None = None
        evidence: list[PageSpeedAttemptEvidence] = []
        for attempt in range(1, self.max_attempts + 1):
            async with self._semaphore:
                await self._pace()
                snapshot = await client.fetch(settings.url, strategy=settings.strategy)
            evidence.append(_attempt_evidence(attempt, snapshot))
            if not snapshot.error_message or not _retryable_snapshot(snapshot):
                return snapshot, evidence
            if attempt < self.max_attempts:
                await self._sleeper(self.base_backoff_seconds * (2 ** (attempt - 1)))
        if snapshot is None:
            raise RuntimeError("PageSpeed retry loop did not execute")
        return snapshot, evidence

    async def _pace(self) -> None:
        if self.min_interval_seconds <= 0:
            return
        async with self._pace_lock:
            remaining = self.min_interval_seconds - (monotonic() - self._last_request_at)
            if remaining > 0:
                await self._sleeper(remaining)
            self._last_request_at = monotonic()


class PageSpeedBatchItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int
    target_ref: str
    receipt: CollectionReceipt | None = None
    error: dict[str, str] | None = None


async def collect_pagespeed_batch(
    service: SeoCollectionService,
    adapter: PageSpeedInsightsAdapter,
    jobs: Sequence[PageSpeedSampleJob],
    *,
    concurrency: int = 2,
    max_samples: int = 20,
) -> list[PageSpeedBatchItem]:
    if concurrency < 1 or max_samples < 1:
        raise ValueError("batch concurrency and sample budget must be positive")
    if len(jobs) > max_samples:
        raise ValueError(f"PageSpeed batch has {len(jobs)} samples but its budget is {max_samples}")
    semaphore = asyncio.Semaphore(concurrency)

    async def collect_one(index: int, job: PageSpeedSampleJob) -> PageSpeedBatchItem:
        async with semaphore:
            try:
                receipt = await service.collect(adapter, job.to_collection_request())
                return PageSpeedBatchItem(
                    index=index,
                    target_ref=job.target_ref,
                    receipt=receipt,
                )
            except Exception as exc:
                return PageSpeedBatchItem(
                    index=index,
                    target_ref=job.target_ref,
                    error={"type": type(exc).__name__, "message": str(exc)},
                )

    return list(await asyncio.gather(*(collect_one(index, job) for index, job in enumerate(jobs))))


def select_scheduled_pagespeed_jobs(
    homepage_jobs: Sequence[PageSpeedSampleJob],
    key_page_jobs: Sequence[PageSpeedSampleJob],
    *,
    max_samples: int = 10,
) -> list[PageSpeedSampleJob]:
    if max_samples < 1:
        raise ValueError("scheduled PageSpeed sample budget must be positive")
    selected: list[PageSpeedSampleJob] = []
    seen: set[tuple[str, str]] = set()
    for job in (*homepage_jobs, *key_page_jobs):
        identity = (job.settings.host_page_id, job.settings.strategy)
        if identity in seen:
            continue
        seen.add(identity)
        selected.append(job.model_copy(update={"trigger": CollectionTrigger.SCHEDULED}))
        if len(selected) == max_samples:
            break
    return selected


def _attempt_evidence(
    attempt: int,
    snapshot: PsiSnapshotLike,
) -> PageSpeedAttemptEvidence:
    raw = (
        snapshot.raw
        if isinstance(snapshot.raw, dict)
        else {
            "malformed_response": {
                "reason": "snapshot raw body must be an object",
                "body": snapshot.raw,
            }
        }
    )
    encoded = json.dumps(
        raw,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )
    encoded_size = len(encoded.encode())
    return PageSpeedAttemptEvidence(
        attempt=attempt,
        fetched_at=snapshot.fetched_at.astimezone(UTC),
        http_status=getattr(snapshot, "http_status", None),
        error_message=snapshot.error_message,
        quota_headers=_quota_headers(getattr(snapshot, "response_headers", {})),
        body=raw if encoded_size <= _ATTEMPT_BODY_LIMIT_BYTES else None,
        body_preview_json=(
            encoded.encode()[:_ATTEMPT_BODY_LIMIT_BYTES].decode(errors="replace")
            if encoded_size > _ATTEMPT_BODY_LIMIT_BYTES
            else None
        ),
        body_truncated=encoded_size > _ATTEMPT_BODY_LIMIT_BYTES,
        body_checksum=stable_hash(raw),
        request_count=max(1, int(getattr(snapshot, "request_count", 1))),
    )


def _provider_payload(raw: Mapping[str, Any]) -> dict[str, Any]:
    if "provider_response" not in raw:
        return dict(raw)
    payload = raw.get("provider_response")
    if not isinstance(payload, Mapping):
        raise TypeError("PageSpeed provider_response must be an object")
    return dict(payload)


def _retryable_snapshot(snapshot: PsiSnapshotLike) -> bool:
    status = getattr(snapshot, "http_status", None)
    if status in _RETRYABLE_HTTP_STATUSES:
        return True
    message = (snapshot.error_message or "").casefold()
    return any(
        marker in message
        for marker in ("timeout", "connecterror", "networkerror", "remoteprotocolerror")
    )


def _provider_timestamp(payload: Mapping[str, Any]) -> datetime | None:
    lighthouse = _mapping(payload.get("lighthouseResult"))
    for value in (payload.get("analysisUTCTimestamp"), lighthouse.get("fetchTime")):
        if not isinstance(value, str) or not value.strip():
            continue
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            continue
        return parsed.replace(tzinfo=parsed.tzinfo or UTC).astimezone(UTC)
    return None


def _analysis_identity(payload: Mapping[str, Any]) -> str | None:
    lighthouse = _mapping(payload.get("lighthouseResult"))
    value = payload.get("analysisUTCTimestamp") or lighthouse.get("fetchTime")
    return str(value) if value else None


def _provider_schema_version(payload: Mapping[str, Any]) -> str:
    lighthouse = _mapping(payload.get("lighthouseResult"))
    version = _mapping(payload.get("version"))
    api_version = ".".join(
        str(value) for value in (version.get("major"), version.get("minor")) if value is not None
    )
    lighthouse_version = str(lighthouse.get("lighthouseVersion") or "unknown")
    return f"psi-v5:{api_version or 'unknown'}:lighthouse-{lighthouse_version}"


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _category_score(categories: Mapping[str, Any], name: str) -> Decimal | None:
    value = _mapping(categories.get(name)).get("score")
    return Decimal(str(value)) if value is not None else None


def _lab_metrics(audits: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {}
    for audit_name, metric_name in _LAB_AUDITS.items():
        audit = _mapping(audits.get(audit_name))
        if not audit:
            continue
        metrics[metric_name] = {
            "numeric_value": audit.get("numericValue"),
            "numeric_unit": audit.get("numericUnit"),
            "score": audit.get("score"),
            "display_value": audit.get("displayValue"),
        }
    return metrics


def _field_experience(value: Any) -> dict[str, Any]:
    experience = _mapping(value)
    metrics = _mapping(experience.get("metrics"))
    return {
        "available": bool(metrics),
        "id": experience.get("id"),
        "initial_url": experience.get("initial_url"),
        "origin_fallback": bool(experience.get("origin_fallback", False)),
        "overall_category": experience.get("overall_category"),
        "metrics": {
            name: {
                "percentile": _mapping(metric).get("percentile"),
                "category": _mapping(metric).get("category"),
                "distributions": _mapping(metric).get("distributions") or [],
            }
            for name, metric in metrics.items()
        },
    }


def _diagnostic_audits(audits: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    diagnostics: dict[str, dict[str, Any]] = {}
    for name, raw in audits.items():
        audit = _mapping(raw)
        mode = str(audit.get("scoreDisplayMode") or "")
        if mode not in _KEPT_SCORE_DISPLAY_MODES:
            continue
        if mode == "binary" and audit.get("score") == 1:
            continue
        entry: dict[str, Any] = {
            "title": audit.get("title"),
            "score": audit.get("score"),
            "score_display_mode": mode,
            "numeric_value": audit.get("numericValue"),
            "numeric_unit": audit.get("numericUnit"),
            "display_value": audit.get("displayValue"),
        }
        if mode == "metricSavings":
            entry["metric_savings"] = _metric_savings(audit)
        diagnostics[name] = entry
    return diagnostics


def _metric_savings(audit: Mapping[str, Any]) -> dict[str, float]:
    """The per-metric millisecond savings Lighthouse attributes to one audit."""
    savings: dict[str, float] = {}
    for metric, value in _mapping(audit.get("metricSavings")).items():
        number = _number(value)
        if number is not None:
            savings[str(metric)] = number
    return savings


def _audit_savings_ms(audit: Mapping[str, Any]) -> float:
    """Estimated savings for ONE delivery audit, in milliseconds.

    Lighthouse reports an opportunity's benefit per metric (``metricSavings``:
    ``{"LCP": 300, "FCP": 0}``). Summing those double-counts the same blocked
    milliseconds against two metrics, so the audit's savings is the LARGEST
    single-metric win. Pre-13 payloads carried ``details.overallSavingsMs``
    instead and are read as the fallback so an older stored response still
    scores.
    """
    savings = _metric_savings(audit)
    if savings:
        return max(savings.values())
    fallback = _number(_mapping(audit.get("details")).get("overallSavingsMs"))
    return fallback or 0.0


def _delivery_facts(audits: Mapping[str, Any]) -> dict[str, Any]:
    """The delivery + caching evidence the `asset_delivery` / `caching_policy`
    catalogue checks score, projected to a BOUNDED shape.

    🚨 Lighthouse 13 (PSI's current engine) retired the audit names every SEO
    tool was written against — ``render-blocking-resources``,
    ``uses-text-compression``, ``uses-long-cache-ttl`` no longer exist; their
    successors are the ``*-insight`` audits, all of which report
    ``scoreDisplayMode: "metricSavings"``. That mode was not in this module's
    keep-list, so the ENTIRE performance-opportunity family was being dropped
    on the floor before it ever reached `seo.page_performance` (fixed 2026-08-09).

    Bounded on purpose: per-audit scalars plus a capped list of poorly cached
    resources — never the raw audit `details`, which run to megabytes.
    """
    per_audit: dict[str, dict[str, Any]] = {}
    total_savings_ms = 0.0
    for name in _DELIVERY_SAVINGS_AUDITS:
        audit = _mapping(audits.get(name))
        if not audit:
            continue
        savings_ms = _audit_savings_ms(audit)
        total_savings_ms += savings_ms
        per_audit[name] = {
            "score": audit.get("score"),
            "savings_ms": savings_ms,
            "wasted_bytes": _number(_mapping(audit.get("details")).get("overallSavingsBytes")),
        }
    return {
        "audits": per_audit,
        "total_savings_ms": total_savings_ms,
        "measured_audits": sorted(per_audit),
        "cache": _cache_facts(audits),
    }


def _cache_facts(audits: Mapping[str, Any]) -> dict[str, Any]:
    """Static-asset caching evidence: the byte denominator and the offenders.

    The TTL threshold is deliberately NOT applied here — it belongs to the
    check that scores it (``matrx_scraper.seo_audit``), which owns its own
    named constant. This function only reports what Lighthouse observed.
    """
    static_bytes = 0.0
    static_requests = 0
    requests = _audit_items(audits.get("network-requests"))
    for item in requests:
        resource = str(_mapping(item).get("resourceType") or "")
        if resource not in _STATIC_RESOURCE_TYPES:
            continue
        transferred = _number(_mapping(item).get("transferSize")) or 0.0
        static_bytes += transferred
        static_requests += 1
    offenders: list[dict[str, Any]] = []
    for item in _audit_items(audits.get("cache-insight"))[:_CACHE_OFFENDER_LIMIT]:
        entry = _mapping(item)
        lifetime = _number(entry.get("cacheLifetimeMs"))
        total = _number(entry.get("totalBytes"))
        if lifetime is None or total is None:
            continue
        offenders.append(
            {
                "url": str(entry.get("url") or "")[:_CACHE_URL_LIMIT],
                "cache_lifetime_ms": lifetime,
                "total_bytes": total,
            }
        )
    return {
        # `measured` distinguishes "no static assets" from "PSI never reported
        # a request table", which the check must answer n_a for.
        "measured": bool(requests),
        "static_bytes": static_bytes,
        "static_requests": static_requests,
        "short_ttl_resources": offenders,
    }


def _audit_items(raw: Any) -> list[Any]:
    items = _mapping(_mapping(raw).get("details")).get("items")
    return list(items) if isinstance(items, list) else []


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def _quota_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower().startswith(("x-goog-", "x-ratelimit-")) or key.lower() == "retry-after"
    }


__all__ = [
    "PAGESPEED_INSIGHTS_OPERATION",
    "PageSpeedAttemptEvidence",
    "PageSpeedBatchItem",
    "PageSpeedInsightsAdapter",
    "PageSpeedInsightsSettings",
    "PageSpeedSampleJob",
    "PsiClientFactory",
    "PsiClientLike",
    "PsiSnapshotLike",
    "collect_pagespeed_batch",
    "select_scheduled_pagespeed_jobs",
]
