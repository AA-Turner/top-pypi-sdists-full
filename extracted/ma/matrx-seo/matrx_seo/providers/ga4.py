from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable, Mapping
from contextvars import ContextVar
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Literal, Protocol
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..adapters import ProviderExecutionContext, SeoProviderAdapter, SeoProviderOperation
from ..contracts import (
    CollectionRequest,
    CredentialReferenceKind,
    HostBindingRequest,
    NormalizationContext,
    ProviderCallRecord,
    ProviderResponse,
    ProviderTaskCheckpoint,
    ResolvedCredential,
    SeoCapability,
    SeoObservation,
    WebAnalyticsObservation,
)
from ..identity import stable_hash
from ..rank_matching import canonicalize_rank_url

GA4_LANDING_PAGE_DAILY_OPERATION = SeoProviderOperation(
    name="ga4.landing_page_daily",
    capabilities=(SeoCapability.WEB_ANALYTICS,),
    credential_keys=("refresh_token", "client_id", "client_secret"),
    reference_kinds=(CredentialReferenceKind.INTEGRATION_CONNECTION,),
)

GA4_DATA_LAG_DAYS = 2
GA4_DEFAULT_INITIAL_BACKFILL_DAYS = 90
GA4_DEFAULT_LATE_REFRESH_DAYS = 7

GA4_APPROVED_DIMENSIONS = (
    "date",
    "landingPage",
    "sessionSource",
    "sessionMedium",
    "sessionDefaultChannelGroup",
    "sessionCampaignName",
    "deviceCategory",
)
GA4_APPROVED_METRICS = (
    "sessions",
    "totalUsers",
    "engagedSessions",
    "engagementRate",
    "screenPageViews",
    "keyEvents",
    "totalRevenue",
)

_METADATA_ENDPOINT = "ga4.properties.getMetadata"
_REPORT_ENDPOINT = "ga4.properties.runReport"
_RETRYABLE_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})
_UNBOUND_LANDING_VALUES = frozenset({"", "(not set)", "(other)"})
_ATTEMPT_BODY_LIMIT_BYTES = 16_000


class Ga4LandingPageSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    property_ref: str
    host_site_id: str
    start_date: date
    end_date: date
    query_string_policy: Literal["exclude"] = "exclude"
    row_limit: int = Field(default=100_000, ge=1, le=250_000)
    max_pages: int = Field(default=20, ge=1, le=100)

    @field_validator("property_ref")
    @classmethod
    def validate_property_ref(cls, value: str) -> str:
        normalized = value.strip()
        prefix, separator, property_id = normalized.partition("/")
        if prefix != "properties" or separator != "/" or not property_id.isdigit():
            raise ValueError("GA4 property_ref must use properties/<numeric-id>")
        return normalized

    @field_validator("host_site_id")
    @classmethod
    def require_site(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("GA4 host_site_id must be nonblank")
        return normalized

    @model_validator(mode="after")
    def validate_window(self) -> Ga4LandingPageSettings:
        if self.end_date < self.start_date:
            raise ValueError("GA4 end_date must be on or after start_date")
        return self

    def report_body(self, offset: int) -> dict[str, Any]:
        return {
            "dateRanges": [
                {
                    "startDate": self.start_date.isoformat(),
                    "endDate": self.end_date.isoformat(),
                }
            ],
            "dimensions": [{"name": name} for name in GA4_APPROVED_DIMENSIONS],
            "metrics": [{"name": name} for name in GA4_APPROVED_METRICS],
            "offset": str(offset),
            "limit": str(self.row_limit),
            "keepEmptyRows": False,
            "returnPropertyQuota": True,
            "orderBys": [
                {"dimension": {"dimensionName": name}} for name in GA4_APPROVED_DIMENSIONS
            ],
        }


class Ga4ReportDateRange(BaseModel):
    """The report window the GA4 honesty flags actually describe."""

    model_config = ConfigDict(extra="forbid")

    start: date
    end: date


class Ga4CollectionMetadata(BaseModel):
    """The GA4 honesty envelope persisted on every day-row (`extras.ga4_collection_metadata`).

    Google's `ResponseMetaData` omits a false boolean and an empty list, so a
    consumer reading the wire shape cannot tell "Google said nothing was
    withheld" from "nobody ever looked". This schema persists the negatives
    EXPLICITLY: an absent key means NOT CAPTURED, `false`/`[]` means Google
    affirmed the report clean. The flags describe the whole REPORT, not one day,
    so the window they cover and the instant they were captured are declared
    here too — a consumer says "flagged for Sep 1-28, captured at T" instead of
    pretending the flag is per-day. Unknown Google keys (and a `__kind` marker,
    if this object ever becomes a registered kind) are preserved, never
    stripped.
    """

    model_config = ConfigDict(extra="allow")

    timeZone: str
    currencyCode: str
    schemaRestrictionResponse: dict[str, Any] = Field(default_factory=dict)
    subjectToThresholding: bool
    samplingMetadatas: list[dict[str, Any]] = Field(default_factory=list)
    dataLossFromOtherRow: bool
    report_date_range: Ga4ReportDateRange
    captured_at: datetime

    @field_validator("timeZone", "currencyCode")
    @classmethod
    def require_nonblank(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("GA4 report metadata requires nonblank timeZone and currencyCode")
        return normalized


class Ga4ApiResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any]
    status_code: int = 200
    headers: dict[str, str] = Field(default_factory=dict)
    # Exact outbound request evidence (DEF-1x parity contract). Optional so
    # existing fixture/fake clients keep working without it.
    request_url: str = ""
    request_method: str = ""


class Ga4DataClient(Protocol):
    async def get_metadata(self, property_ref: str) -> Ga4ApiResponse: ...

    async def run_report(
        self, property_ref: str, request_body: Mapping[str, Any]
    ) -> Ga4ApiResponse: ...


Ga4ClientFactory = Callable[[ResolvedCredential], Ga4DataClient]
Ga4PageResourceResolver = Callable[[CollectionRequest, str, list[str]], Awaitable[dict[str, str]]]


class Ga4TransportError(RuntimeError):
    pass


def _google_api_error_summary(response: Ga4ApiResponse | None) -> str:
    """Compact human-parseable reason from a Google API error body.

    "GA4 Data API HTTP 403" alone is useless — the body says WHY (e.g.
    SERVICE_DISABLED: "Google Analytics Data API has not been used in
    project ... or it is disabled", the exact 2026-07-27 incident). Never
    swallow it."""

    if response is None or not isinstance(response.payload, dict):
        return ""
    error = response.payload.get("error")
    if not isinstance(error, dict):
        return ""
    status = error.get("status")
    message = error.get("message")
    parts = [str(part) for part in (status, message) if part]
    summary = ": ".join(parts)
    return summary[:400]


class Ga4CollectionError(RuntimeError):
    def __init__(
        self,
        *,
        attempts: int,
        message: str,
        response: Ga4ApiResponse | None = None,
        attempt_evidence: list[dict[str, Any]] | None = None,
    ) -> None:
        self.attempts = attempts
        self.response = response
        self.attempt_evidence = attempt_evidence or []
        super().__init__(message)


def plan_ga4_window(
    *,
    as_of: date,
    last_successful_end: date | None = None,
    initial_backfill_days: int = GA4_DEFAULT_INITIAL_BACKFILL_DAYS,
    late_refresh_days: int = GA4_DEFAULT_LATE_REFRESH_DAYS,
) -> tuple[date, date]:
    if initial_backfill_days < 1 or late_refresh_days < 1:
        raise ValueError("GA4 backfill and late-refresh windows must be positive")
    end = as_of - timedelta(days=GA4_DATA_LAG_DAYS)
    late_start = end - timedelta(days=late_refresh_days - 1)
    if last_successful_end is None:
        start = end - timedelta(days=initial_backfill_days - 1)
    else:
        start = min(last_successful_end + timedelta(days=1), late_start)
    return start, end


class Ga4AnalyticsAdapter(SeoProviderAdapter):
    provider = "ga4"
    capabilities = (SeoCapability.WEB_ANALYTICS,)
    operations = (GA4_LANDING_PAGE_DAILY_OPERATION,)

    def __init__(
        self,
        *,
        client_factory: Ga4ClientFactory,
        page_resource_resolver: Ga4PageResourceResolver | None = None,
        max_attempts: int = 3,
        base_backoff_seconds: float = 0.5,
        max_retry_delay_seconds: float = 8,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("GA4 max_attempts must be positive")
        if base_backoff_seconds < 0 or max_retry_delay_seconds < 0:
            raise ValueError("GA4 retry delays cannot be negative")
        self._client_factory = client_factory
        self._page_resource_resolver = page_resource_resolver
        self._max_attempts = max_attempts
        self._base_backoff = base_backoff_seconds
        self._max_retry_delay = max_retry_delay_seconds
        self._sleep = sleep
        self._client: ContextVar[Ga4DataClient | None] = ContextVar(
            f"ga4_data_client_{id(self)}", default=None
        )

    async def authenticate(self, credential: ResolvedCredential) -> None:
        missing = [
            key
            for key in GA4_LANDING_PAGE_DAILY_OPERATION.credential_keys
            if not credential.values.get(key)
        ]
        if missing:
            raise ValueError(f"GA4 OAuth credential is missing: {', '.join(missing)}")
        if credential.reference_kind not in {
            None,
            CredentialReferenceKind.INTEGRATION_CONNECTION,
        }:
            raise ValueError("GA4 requires a per-client integration connection")
        self._client.set(self._client_factory(credential))

    async def collect_response(
        self,
        request: CollectionRequest,
        execution: ProviderExecutionContext,
    ) -> ProviderResponse:
        if request.operation != GA4_LANDING_PAGE_DAILY_OPERATION.name:
            raise ValueError(f"unsupported GA4 operation {request.operation!r}")
        client = self._client.get()
        if client is None:
            raise RuntimeError("GA4 adapter must be authenticated before collection")
        settings = Ga4LandingPageSettings.model_validate(request.settings)
        checkpoints = {
            task.external_task_id: task
            for task in await execution.resumable_tasks()
            if task.endpoint in {_METADATA_ENDPOINT, _REPORT_ENDPOINT}
            and task.status in {"completed", "failed"}
        }
        raw_pages: list[dict[str, Any]] = []
        calls: list[ProviderCallRecord] = []
        failures: list[dict[str, Any]] = []
        run_identity = str(execution.run.id)

        metadata_request = {"property_ref": settings.property_ref}
        metadata_task_id = stable_hash(
            [self.provider, run_identity, _METADATA_ENDPOINT, metadata_request]
        )
        metadata_checkpoint = checkpoints.get(metadata_task_id)
        if metadata_checkpoint is not None and metadata_checkpoint.status == "completed":
            property_metadata = _raw_from_checkpoint(metadata_checkpoint, "metadata")
            calls.extend(_calls_from_checkpoint(metadata_checkpoint, property_metadata))
        else:
            property_metadata, metadata_calls, metadata_failure = await self._collect_call(
                execution=execution,
                endpoint=_METADATA_ENDPOINT,
                task_id=metadata_task_id,
                kind="metadata",
                request_payload=metadata_request,
                invoke=lambda: client.get_metadata(settings.property_ref),
                request=request,
                prior_checkpoint=metadata_checkpoint,
            )
            calls.extend(metadata_calls)
            if metadata_failure is not None:
                failures.append(metadata_failure)

        if not failures:
            try:
                _validate_metadata_catalog(property_metadata.get("response"))
            except (TypeError, ValueError) as exc:
                failures.append(
                    {
                        "kind": "metadata",
                        "type": type(exc).__name__,
                        "message": str(exc),
                    }
                )

        report_metadata: dict[str, Any] | None = None
        captured_instants: list[datetime] = []
        if not failures:
            offset = 0
            for _page_index in range(settings.max_pages):
                body = settings.report_body(offset)
                task_id = stable_hash(
                    [
                        self.provider,
                        run_identity,
                        _REPORT_ENDPOINT,
                        settings.property_ref,
                        body,
                    ]
                )
                checkpoint = checkpoints.get(task_id)
                if checkpoint is not None and checkpoint.status == "completed":
                    page = _raw_from_checkpoint(checkpoint, "report")
                    calls.extend(_calls_from_checkpoint(checkpoint, page))
                    failure = None
                else:
                    page, page_calls, failure = await self._collect_call(
                        execution=execution,
                        endpoint=_REPORT_ENDPOINT,
                        task_id=task_id,
                        kind="report",
                        request_payload={
                            "property_ref": settings.property_ref,
                            "request": body,
                        },
                        invoke=lambda body=body: client.run_report(settings.property_ref, body),
                        request=request,
                        prior_checkpoint=checkpoint,
                    )
                    # A resumed GA4 task can carry a long provider-call history.
                    # Extending that history is synchronous list work and has
                    # previously frozen the shared API loop for more than a
                    # second. Keep the provider evidence exact, but copy it at
                    # the package's CPU-isolation boundary.
                    await asyncio.to_thread(calls.extend, page_calls)
                raw_pages.append(page)
                if failure is not None:
                    failures.append(failure)
                    break
                payload = page["response"]
                try:
                    _validate_headers(payload)
                    current_metadata = _validate_report_metadata(payload)
                    row_count = _response_row_count(payload)
                    rows = _response_rows(payload)
                except (TypeError, ValueError) as exc:
                    failures.append(
                        {
                            "kind": "report",
                            "offset": offset,
                            "type": type(exc).__name__,
                            "message": str(exc),
                        }
                    )
                    break
                if report_metadata is None:
                    report_metadata = current_metadata
                elif _property_metadata_identity(current_metadata) != _property_metadata_identity(
                    report_metadata
                ):
                    failures.append(
                        {
                            "kind": "report",
                            "offset": offset,
                            "type": "Ga4PropertyMetadataChanged",
                            "message": "GA4 timezone or currency changed during pagination",
                        }
                    )
                    break
                else:
                    # A flag Google raises on page 2 described the same report as
                    # page 1. Taking the first page's metadata and discarding the
                    # rest threw thresholding and (other)-row loss away silently.
                    report_metadata = _merge_report_metadata(report_metadata, current_metadata)
                page_captured_at = _page_captured_at(page)
                if page_captured_at is not None:
                    captured_instants.append(page_captured_at)
                offset += len(rows)
                if offset >= row_count:
                    break
                if not rows:
                    failures.append(
                        {
                            "kind": "report",
                            "offset": offset,
                            "type": "Ga4PaginationStalled",
                            "message": "GA4 returned no rows before advertised rowCount",
                        }
                    )
                    break
            else:
                failures.append(
                    {
                        "kind": "report",
                        "offset": offset,
                        "type": "Ga4PaginationLimit",
                        "message": "approved GA4 max_pages was exhausted",
                    }
                )

        custom_definitions = _custom_definitions(property_metadata.get("response", {}))
        unbound_values = _unbound_landing_values(
            [page for page in raw_pages if not page.get("error")]
        )
        error = None
        if failures:
            error = {
                "type": "Ga4PartialCollectionError",
                "message": f"{len(failures)} GA4 request or pagination failure(s)",
                "failures": failures,
            }
        return ProviderResponse(
            raw={
                "property_ref": settings.property_ref,
                "window": {
                    "start_date": settings.start_date.isoformat(),
                    "end_date": settings.end_date.isoformat(),
                    "data_lag_days": GA4_DATA_LAG_DAYS,
                },
                "grain": {
                    "dimensions": list(GA4_APPROVED_DIMENSIONS),
                    "metrics": list(GA4_APPROVED_METRICS),
                    "query_string_policy": settings.query_string_policy,
                },
                "property_metadata": property_metadata,
                "custom_definitions": custom_definitions,
                "report_metadata": (
                    _collection_metadata(
                        report_metadata,
                        start_date=settings.start_date,
                        end_date=settings.end_date,
                        captured_at=max(captured_instants, default=None),
                    )
                    if report_metadata is not None
                    else {}
                ),
                "unbound_landing_values": unbound_values,
                "pages": raw_pages,
                "failures": failures,
            },
            fetched_at=datetime.now(UTC),
            provider_schema_version="ga4-data-v1beta-landing-page-v1",
            call_records=calls,
            currency="USD",
            error=error,
        )

    async def _collect_call(
        self,
        *,
        execution: ProviderExecutionContext,
        endpoint: str,
        task_id: str,
        kind: Literal["metadata", "report"],
        request_payload: dict[str, Any],
        invoke: Callable[[], Awaitable[Ga4ApiResponse]],
        request: CollectionRequest,
        prior_checkpoint: ProviderTaskCheckpoint | None = None,
    ) -> tuple[dict[str, Any], list[ProviderCallRecord], dict[str, Any] | None]:
        started_at = datetime.now(UTC)
        provider_call_key = stable_hash([task_id, started_at.isoformat(), request.request_id])
        failure: dict[str, Any] | None = None
        try:
            response, attempt_evidence = await self._request_with_retry(invoke)
            attempts = len(attempt_evidence)
            status = "completed"
        except Ga4CollectionError as exc:
            response = exc.response or Ga4ApiResponse(
                payload={
                    "transport_error": {
                        "type": type(exc).__name__,
                        "message": str(exc),
                    }
                },
                status_code=0,
            )
            attempts = exc.attempts
            attempt_evidence = exc.attempt_evidence
            status = "failed"
            provider_message = _ga4_provider_error_message(response.payload)
            failure = {
                "kind": kind,
                "type": type(exc).__name__,
                "message": provider_message or str(exc),
                "status_code": response.status_code,
            }
        finished_at = datetime.now(UTC)
        prior_raw = (
            _raw_from_checkpoint(prior_checkpoint, kind) if prior_checkpoint is not None else None
        )
        prior_attempts = list(prior_raw.get("attempts", [])) if prior_raw is not None else []
        attempt_evidence = [
            {**item, "attempt": len(prior_attempts) + index}
            for index, item in enumerate(attempt_evidence, start=1)
        ]
        cumulative_attempts = prior_attempts + attempt_evidence
        request_evidence = {
            "method": response.request_method or ("GET" if kind == "metadata" else "POST"),
            "url": response.request_url,
            "headers": {"Authorization": "Bearer ***"},
            "body": request_payload,
        }
        raw = {
            "kind": kind,
            "request": request_payload,
            "response": response.payload,
            "status_code": response.status_code,
            "quota_headers": _quota_headers(response.headers),
            "property_quota": _mapping(response.payload.get("propertyQuota")),
            "attempts": cumulative_attempts,
            "request_evidence": request_evidence,
        }
        if failure is not None:
            raw["error"] = failure
        current_call = ProviderCallRecord(
            provider_call_key=provider_call_key,
            external_task_id=task_id,
            request_count=attempts,
            reported_cost=Decimal(0),
            currency="USD",
            fetched_at=finished_at,
            metadata={
                "kind": kind,
                "request": request_payload,
                "status_code": response.status_code,
                "response_status": response.status_code,
                "quota_headers": raw["quota_headers"],
                "property_quota": raw["property_quota"],
                "attempts": attempt_evidence,
                "request_evidence": request_evidence,
                "error": failure,
                "pricing": "no_per_request_charge",
            },
        )
        prior_calls = (
            _calls_from_checkpoint(prior_checkpoint, prior_raw)
            if prior_checkpoint is not None and prior_raw is not None
            else []
        )
        call_history = prior_calls + [current_call]
        checkpoint = ProviderTaskCheckpoint(
            external_task_id=task_id,
            endpoint=endpoint,
            status=status,
            request_payload={
                "kind": kind,
                "request": request_payload,
                "provider_call_key": provider_call_key,
                "status_code": response.status_code,
                "quota_headers": raw["quota_headers"],
                "property_quota": raw["property_quota"],
                "attempts": raw["attempts"],
                "request_evidence": request_evidence,
                "call_history": [call.model_dump(mode="json") for call in call_history],
            },
            response_payload=response.payload,
            request_count=sum(call.request_count for call in call_history),
            provider_cost=Decimal(0),
            currency="USD",
            submitted_at=started_at,
            last_polled_at=finished_at,
            completed_at=finished_at,
            error=failure,
        )
        await execution.checkpoint(checkpoint)
        return raw, call_history, failure

    async def _request_with_retry(
        self,
        invoke: Callable[[], Awaitable[Ga4ApiResponse]],
    ) -> tuple[Ga4ApiResponse, list[dict[str, Any]]]:
        last_error: Exception | None = None
        last_response: Ga4ApiResponse | None = None
        evidence: list[dict[str, Any]] = []
        for attempt in range(1, self._max_attempts + 1):
            try:
                response = await invoke()
            except (httpx.TimeoutException, httpx.TransportError, Ga4TransportError) as exc:
                last_error = exc
                transport_error = {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
                evidence.append(
                    {
                        "attempt": attempt,
                        "fetched_at": datetime.now(UTC).isoformat(),
                        "status_code": None,
                        "quota_headers": {},
                        "property_quota": {},
                        "transport_error": transport_error,
                        "body": None,
                        "body_preview_json": None,
                        "body_truncated": False,
                        "body_checksum": stable_hash(transport_error),
                    }
                )
                if attempt < self._max_attempts:
                    await self._sleep(self._retry_delay(attempt))
                    continue
                break
            evidence.append(_attempt_evidence(attempt, response))
            if response.status_code < 400:
                return response, evidence
            last_response = response
            if response.status_code not in _RETRYABLE_STATUSES:
                summary = _google_api_error_summary(response)
                raise Ga4CollectionError(
                    attempts=attempt,
                    message=(
                        f"GA4 Data API HTTP {response.status_code}"
                        + (f" — {summary}" if summary else "")
                    ),
                    response=response,
                    attempt_evidence=evidence,
                )
            last_error = RuntimeError(f"HTTP {response.status_code}")
            if attempt < self._max_attempts:
                await self._sleep(self._retry_delay(attempt, response.headers))
        summary = _google_api_error_summary(last_response)
        raise Ga4CollectionError(
            attempts=self._max_attempts,
            message=(
                f"GA4 Data API retries exhausted: {last_error}"
                + (f" — {summary}" if summary else "")
            ),
            response=last_response,
            attempt_evidence=evidence,
        )

    def _retry_delay(
        self,
        attempt: int,
        headers: Mapping[str, str] | None = None,
    ) -> float:
        retry_after: float | None = None
        if headers is not None:
            raw_retry_after = next(
                (value for key, value in headers.items() if key.lower() == "retry-after"),
                None,
            )
            if raw_retry_after is not None:
                try:
                    parsed = float(raw_retry_after)
                except ValueError:
                    parsed = -1
                if parsed >= 0:
                    retry_after = parsed
        exponential = self._base_backoff * (2 ** (attempt - 1))
        requested = max(exponential, retry_after or 0)
        return min(requested, self._max_retry_delay)

    async def normalize(
        self,
        response: ProviderResponse,
        context: NormalizationContext,
    ) -> list[SeoObservation]:
        if not isinstance(response.raw, dict):
            raise TypeError("GA4 raw response must be an object")
        settings = Ga4LandingPageSettings.model_validate(context.request.settings)
        site = await context.resolve_host_binding(
            HostBindingRequest(resource_kind="web_site", resource_id=settings.host_site_id)
        )
        pages = response.raw.get("pages")
        if not isinstance(pages, list):
            raise TypeError("GA4 raw response must contain report pages")
        parsed_rows = _parse_report_rows(pages)
        stored_metadata = _validate_normalized_report_metadata(response.raw.get("report_metadata"))
        report_metadata = _collection_metadata(
            stored_metadata,
            start_date=settings.start_date,
            end_date=settings.end_date,
            captured_at=_parse_instant(stored_metadata.get("captured_at")) or response.fetched_at,
        )
        resolved_rows: list[tuple[dict[str, Any], str | None]] = []
        for row in parsed_rows:
            landing_url = _landing_url(site.canonical_url, row["landingPage"])
            resolved_rows.append((row, landing_url))
        urls = sorted(
            {landing_url for _row, landing_url in resolved_rows if landing_url is not None}
        )
        if urls and self._page_resource_resolver is None:
            raise RuntimeError("GA4 landing-page facts require the canonical page resolver")
        page_ids_by_url: dict[str, str] = {}
        if urls and self._page_resource_resolver is not None:
            resources = await self._page_resource_resolver(
                context.request,
                settings.host_site_id,
                urls,
            )
            missing = sorted(set(urls) - set(resources))
            if missing:
                raise ValueError(
                    f"GA4 could not resolve {len(missing)} landing page URL(s) "
                    "to canonical in-scope web pages"
                )
            for url, resource_id in resources.items():
                binding = await context.resolve_host_binding(
                    HostBindingRequest(resource_kind="web_page", resource_id=resource_id)
                )
                if binding.site_id != site.site_id:
                    raise ValueError("GA4 page binding resolved outside the requested site")
                if binding.page_id is None:
                    raise ValueError("GA4 web_page binding resolved without a page id")
                page_ids_by_url[url] = binding.page_id
        return [
            WebAnalyticsObservation(
                site_id=site.site_id,
                page_id=(page_ids_by_url[landing_url] if landing_url is not None else None),
                date=row["date"],
                source=_optional_dimension(row["sessionSource"]),
                medium=_optional_dimension(row["sessionMedium"]),
                channel=_optional_dimension(row["sessionDefaultChannelGroup"]),
                campaign=_optional_dimension(row["sessionCampaignName"]),
                device=_optional_dimension(row["deviceCategory"], lowercase=True),
                landing_page=(
                    landing_url
                    if landing_url is not None
                    else row["landingPage"].strip() or "(empty)"
                ),
                currency_code=report_metadata["currencyCode"],
                property_timezone=report_metadata["timeZone"],
                sessions=_whole_metric(row["sessions"], "sessions"),
                users=_whole_metric(row["totalUsers"], "totalUsers"),
                engaged_sessions=_whole_metric(row["engagedSessions"], "engagedSessions"),
                engagement_rate=_rate_metric(row["engagementRate"]),
                views=_whole_metric(row["screenPageViews"], "screenPageViews"),
                key_events=_decimal_metric(row["keyEvents"], "keyEvents"),
                conversions=Decimal(0),
                revenue=_revenue_metric(row["totalRevenue"]),
                extras={
                    "query_string_policy": settings.query_string_policy,
                    "ga4_collection_metadata": report_metadata,
                },
            )
            for row, landing_url in resolved_rows
        ]


def _ga4_provider_error_message(payload: Mapping[str, Any]) -> str | None:
    error = payload.get("error")
    if not isinstance(error, Mapping):
        return None
    message = error.get("message")
    if not isinstance(message, str) or not message.strip():
        return None
    status = error.get("status")
    prefix = f"GA4 Data API {status}" if isinstance(status, str) and status else "GA4 Data API"
    return f"{prefix}: {message.strip()}"


def _raw_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint,
    kind: Literal["metadata", "report"],
) -> dict[str, Any]:
    if not isinstance(checkpoint.response_payload, dict):
        raise ValueError("completed GA4 checkpoint has no response payload")
    raw = {
        "kind": kind,
        "request": checkpoint.request_payload["request"],
        "response": checkpoint.response_payload,
        "status_code": checkpoint.request_payload.get("status_code", 200),
        "quota_headers": checkpoint.request_payload.get("quota_headers", {}),
        "property_quota": checkpoint.request_payload.get("property_quota", {}),
        "attempts": checkpoint.request_payload.get("attempts", []),
        "request_evidence": checkpoint.request_payload.get("request_evidence", {}),
        "resumed_from_checkpoint": True,
    }
    if checkpoint.error is not None:
        raw["error"] = checkpoint.error
    return raw


def _calls_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint,
    raw: Mapping[str, Any],
) -> list[ProviderCallRecord]:
    history = checkpoint.request_payload.get("call_history")
    if isinstance(history, list) and history:
        return [ProviderCallRecord.model_validate(item) for item in history]
    return [_call_from_checkpoint(checkpoint, raw)]


def _call_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint,
    raw: Mapping[str, Any],
) -> ProviderCallRecord:
    response = raw.get("response")
    row_count = len(_response_rows(response)) if isinstance(response, dict) else 0
    return ProviderCallRecord(
        provider_call_key=str(
            checkpoint.request_payload.get("provider_call_key") or checkpoint.external_task_id
        ),
        external_task_id=checkpoint.external_task_id,
        request_count=checkpoint.request_count,
        reported_cost=Decimal(0),
        currency="USD",
        fetched_at=(
            checkpoint.completed_at or checkpoint.last_polled_at or checkpoint.submitted_at
        ),
        metadata={
            "kind": raw.get("kind"),
            "request": raw.get("request"),
            "status_code": raw.get("status_code"),
            "response_status": raw.get("status_code"),
            "row_count": row_count,
            "quota_headers": raw.get("quota_headers", {}),
            "property_quota": raw.get("property_quota", {}),
            "attempts": raw.get("attempts", []),
            "request_evidence": raw.get("request_evidence", {}),
            "error": raw.get("error"),
            "pricing": "no_per_request_charge",
        },
    )


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _response_rows(payload: Mapping[str, Any]) -> list[Any]:
    rows = payload.get("rows")
    if rows is None:
        return []
    if not isinstance(rows, list):
        raise ValueError("GA4 response rows must be a list")
    return rows


def _response_row_count(payload: Mapping[str, Any]) -> int:
    raw = payload.get("rowCount", len(_response_rows(payload)))
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("GA4 rowCount must be an integer") from exc
    if value < 0:
        raise ValueError("GA4 rowCount cannot be negative")
    return value


def _header_names(payload: Mapping[str, Any], key: str) -> tuple[str, ...]:
    headers = payload.get(key)
    if not isinstance(headers, list):
        raise ValueError(f"GA4 response {key} must be a list")
    names: list[str] = []
    for header in headers:
        if not isinstance(header, dict) or not isinstance(header.get("name"), str):
            raise ValueError(f"GA4 response {key} contains an invalid header")
        names.append(header["name"])
    return tuple(names)


def _validate_headers(payload: Mapping[str, Any]) -> None:
    if _header_names(payload, "dimensionHeaders") != GA4_APPROVED_DIMENSIONS:
        raise ValueError("GA4 response dimension headers do not match approved grain")
    if _header_names(payload, "metricHeaders") != GA4_APPROVED_METRICS:
        raise ValueError("GA4 response metric headers do not match approved metrics")


def _validate_report_metadata(payload: Mapping[str, Any]) -> dict[str, Any]:
    return _validate_normalized_report_metadata(payload.get("metadata"))


def _validate_normalized_report_metadata(value: Any) -> dict[str, Any]:
    metadata = _mapping(value)
    for key in ("timeZone", "currencyCode"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError(f"GA4 report metadata requires nonblank {key}")
        metadata[key] = metadata[key].strip()
    # Google omits a false boolean and an empty list, so on the wire "clean" and
    # "never captured" look identical. Persist the negatives explicitly.
    metadata["subjectToThresholding"] = _metadata_flag(
        metadata.get("subjectToThresholding"), "subjectToThresholding"
    )
    metadata["dataLossFromOtherRow"] = _metadata_flag(
        metadata.get("dataLossFromOtherRow"), "dataLossFromOtherRow"
    )
    metadata["samplingMetadatas"] = _sampling_metadatas(metadata.get("samplingMetadatas"))
    metadata["schemaRestrictionResponse"] = _mapping(metadata.get("schemaRestrictionResponse"))
    return metadata


def _metadata_flag(value: Any, name: str) -> bool:
    if value is None:
        return False
    if not isinstance(value, bool):
        raise ValueError(f"GA4 report metadata {name} must be a boolean")
    return value


def _sampling_metadatas(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("GA4 report metadata samplingMetadatas must be a list")
    entries: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise ValueError("GA4 report metadata samplingMetadatas entries must be objects")
        entries.append(dict(item))
    return entries


def _merge_report_metadata(base: Mapping[str, Any], current: Mapping[str, Any]) -> dict[str, Any]:
    """OR the honesty flags and concatenate sampling across report pages."""

    merged = dict(base)
    for key in ("subjectToThresholding", "dataLossFromOtherRow"):
        merged[key] = bool(base.get(key)) or bool(current.get(key))
    merged["samplingMetadatas"] = list(base.get("samplingMetadatas") or []) + list(
        current.get("samplingMetadatas") or []
    )
    merged["schemaRestrictionResponse"] = _merge_schema_restrictions(
        _mapping(base.get("schemaRestrictionResponse")),
        _mapping(current.get("schemaRestrictionResponse")),
    )
    for key, value in current.items():
        if key not in merged:
            merged[key] = value
    return merged


def _merge_schema_restrictions(
    base: Mapping[str, Any], current: Mapping[str, Any]
) -> dict[str, Any]:
    merged: dict[str, Any] = {**current, **base}
    restrictions: list[Any] = []
    seen: set[str] = set()
    for source in (base, current):
        entries = source.get("activeMetricRestrictions")
        if not isinstance(entries, list):
            continue
        for entry in entries:
            fingerprint = stable_hash(entry)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            restrictions.append(entry)
    if restrictions:
        merged["activeMetricRestrictions"] = restrictions
    return merged


def _page_captured_at(page: Mapping[str, Any]) -> datetime | None:
    attempts = page.get("attempts")
    if not isinstance(attempts, list):
        return None
    for attempt in reversed(attempts):
        if not isinstance(attempt, Mapping):
            continue
        parsed = _parse_instant(attempt.get("fetched_at"))
        if parsed is not None:
            return parsed
    return None


def _parse_instant(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def _collection_metadata(
    base: Mapping[str, Any],
    *,
    start_date: date,
    end_date: date,
    captured_at: datetime | None,
) -> dict[str, Any]:
    """The persisted honesty envelope: Google's flags plus what makes them readable.

    The flags describe the whole report, so the window they cover and the
    instant of capture travel with them; without those a client counting
    "collected days" is really counting one run's rows.
    """

    payload = dict(base)
    payload["report_date_range"] = {
        "start": start_date.isoformat(),
        "end": end_date.isoformat(),
    }
    payload["captured_at"] = (captured_at or datetime.now(UTC)).astimezone(UTC).isoformat()
    return Ga4CollectionMetadata.model_validate(payload).model_dump(mode="json")


def _parse_report_rows(pages: list[Any]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("GA4 report page must be an object")
        payload = page.get("response")
        if not isinstance(payload, dict):
            raise ValueError("GA4 report page response must be an object")
        _validate_headers(payload)
        for raw_row in _response_rows(payload):
            if not isinstance(raw_row, dict):
                raise ValueError("GA4 report row must be an object")
            dimensions = raw_row.get("dimensionValues")
            metrics = raw_row.get("metricValues")
            if not isinstance(dimensions, list) or len(dimensions) != len(GA4_APPROVED_DIMENSIONS):
                raise ValueError("GA4 row dimension values do not match headers")
            if not isinstance(metrics, list) or len(metrics) != len(GA4_APPROVED_METRICS):
                raise ValueError("GA4 row metric values do not match headers")
            dimension_values = [_cell_value(item) for item in dimensions]
            metric_values = [_cell_value(item) for item in metrics]
            values = dict(zip(GA4_APPROVED_DIMENSIONS, dimension_values, strict=True))
            values.update(dict(zip(GA4_APPROVED_METRICS, metric_values, strict=True)))
            try:
                values["date"] = datetime.strptime(values["date"], "%Y%m%d").date()
            except (TypeError, ValueError) as exc:
                raise ValueError("GA4 date dimension must use YYYYMMDD") from exc
            parsed.append(values)
    return parsed


def _cell_value(value: Any) -> str:
    if not isinstance(value, dict) or not isinstance(value.get("value"), str):
        raise ValueError("GA4 row cells must contain string values")
    return value["value"]


def _landing_url(site_url: str, landing_page: str) -> str | None:
    value = landing_page.strip()
    if value.casefold() in _UNBOUND_LANDING_VALUES:
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        absolute = value
    else:
        if not value.startswith("/"):
            raise ValueError("GA4 landingPage must be an absolute path")
        absolute = urljoin(site_url.rstrip("/") + "/", value)
    parts = urlsplit(absolute)
    without_query = urlunsplit((parts.scheme, parts.netloc, parts.path or "/", "", ""))
    normalized = canonicalize_rank_url(without_query)
    if not normalized:
        raise ValueError("GA4 landing page could not be canonicalized")
    return normalized


def _optional_dimension(value: str, *, lowercase: bool = False) -> str | None:
    normalized = value.strip()
    if not normalized:
        return None
    return normalized.lower() if lowercase else normalized


def _decimal_metric(value: str, name: str) -> Decimal:
    try:
        metric = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"GA4 {name} must be numeric") from exc
    if not metric.is_finite() or metric < 0:
        raise ValueError(f"GA4 {name} must be finite and nonnegative")
    return metric


def _revenue_metric(value: str) -> Decimal:
    try:
        metric = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("GA4 totalRevenue must be numeric") from exc
    if not metric.is_finite():
        raise ValueError("GA4 totalRevenue must be finite")
    return metric


def _whole_metric(value: str, name: str) -> int:
    metric = _decimal_metric(value, name)
    if metric != metric.to_integral_value():
        raise ValueError(f"GA4 {name} must be a whole number")
    return int(metric)


def _rate_metric(value: str) -> Decimal:
    metric = _decimal_metric(value, "engagementRate")
    if metric > 1:
        raise ValueError("GA4 engagementRate must be a fraction between zero and one")
    return metric


def _property_metadata_identity(metadata: Mapping[str, Any]) -> tuple[Any, Any]:
    return metadata.get("timeZone"), metadata.get("currencyCode")


def _custom_definitions(payload: Any) -> dict[str, list[dict[str, Any]]]:
    source = _mapping(payload)
    return {
        key: [
            item
            for item in source.get(key, [])
            if isinstance(item, dict) and item.get("customDefinition") is True
        ]
        for key in ("dimensions", "metrics")
        if isinstance(source.get(key), list)
    }


def _validate_metadata_catalog(value: Any) -> None:
    payload = _mapping(value)
    for key in ("dimensions", "metrics"):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"GA4 metadata response requires a {key} list")


def _unbound_landing_values(pages: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for page in pages:
        try:
            rows = _parse_report_rows([page])
        except (TypeError, ValueError):
            continue
        for row in rows:
            value = row["landingPage"].strip()
            if value.casefold() in _UNBOUND_LANDING_VALUES:
                counts[value or "(empty)"] = counts.get(value or "(empty)", 0) + 1
    return counts


def _quota_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower().startswith(("x-goog-", "x-ratelimit-", "retry-after"))
    }


def _attempt_evidence(attempt: int, response: Ga4ApiResponse) -> dict[str, Any]:
    encoded = json.dumps(
        response.payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )
    encoded_bytes = encoded.encode()
    return {
        "attempt": attempt,
        "fetched_at": datetime.now(UTC).isoformat(),
        "status_code": response.status_code,
        "quota_headers": _quota_headers(response.headers),
        "property_quota": _mapping(response.payload.get("propertyQuota")),
        "body": response.payload if len(encoded_bytes) <= _ATTEMPT_BODY_LIMIT_BYTES else None,
        "body_preview_json": (
            encoded_bytes[:_ATTEMPT_BODY_LIMIT_BYTES].decode(errors="replace")
            if len(encoded_bytes) > _ATTEMPT_BODY_LIMIT_BYTES
            else None
        ),
        "body_truncated": len(encoded_bytes) > _ATTEMPT_BODY_LIMIT_BYTES,
        "body_checksum": stable_hash(response.payload),
    }


__all__ = [
    "GA4_APPROVED_DIMENSIONS",
    "GA4_APPROVED_METRICS",
    "GA4_DATA_LAG_DAYS",
    "GA4_LANDING_PAGE_DAILY_OPERATION",
    "Ga4AnalyticsAdapter",
    "Ga4ApiResponse",
    "Ga4CollectionMetadata",
    "Ga4LandingPageSettings",
    "Ga4ReportDateRange",
    "Ga4TransportError",
    "plan_ga4_window",
]
