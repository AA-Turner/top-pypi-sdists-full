from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Mapping
from contextvars import ContextVar
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Any, Literal, Protocol
from zoneinfo import ZoneInfo

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
    SearchPerformanceObservation,
    SeoCapability,
    SeoIdentityRequest,
    SeoObservation,
)
from ..identity import stable_hash

GSC_SEARCH_ANALYTICS_OPERATION = SeoProviderOperation(
    name="gsc.search_analytics.query",
    capabilities=(SeoCapability.SEARCH_PERFORMANCE,),
    credential_keys=("refresh_token", "client_id", "client_secret"),
    reference_kinds=(CredentialReferenceKind.INTEGRATION_CONNECTION,),
)

# Google's Search Analytics day boundaries are Pacific Time WITH daylight
# saving (`America/Los_Angeles`), never UTC — there is no UTC option in the
# API, and `metadata.first_incomplete_date` is documented in that same zone.
# Deriving "today" from a UTC clock is wrong for the 7-8 hours after UTC
# midnight, every single day.
GSC_TIMEZONE = ZoneInfo("America/Los_Angeles")

GSC_DEFAULT_INITIAL_BACKFILL_DAYS = 90
# How far back the fresh edge is re-asked, and — equally — how far back an
# ATTEMPT alone is not enough to call a day covered. Google documents a 2-3
# day lag and delays run longer during incidents, so no attempt inside this
# tail is trusted without rows to back it.
GSC_DEFAULT_LATE_REFRESH_DAYS = 7


def gsc_today(now: datetime | None = None) -> date:
    """Today in Google's Search Console day-boundary zone (Pacific)."""
    return (now or datetime.now(UTC)).astimezone(GSC_TIMEZONE).date()


class GscDimensionProfile(StrEnum):
    PROPERTY = "property"
    PAGE = "page"
    QUERY = "query"
    QUERY_PAGE = "query_page"
    COUNTRY_DEVICE = "country_device"
    SEARCH_APPEARANCE = "search_appearance"

    @property
    def dimensions(self) -> tuple[str, ...]:
        return {
            GscDimensionProfile.PROPERTY: ("date",),
            GscDimensionProfile.PAGE: ("date", "page"),
            GscDimensionProfile.QUERY: ("date", "query"),
            GscDimensionProfile.QUERY_PAGE: ("date", "query", "page"),
            GscDimensionProfile.COUNTRY_DEVICE: ("date", "country", "device"),
            # Search Console rejects searchAppearance combined with any other
            # dimension. The adapter requests one day at a time and infers the
            # observation date from that single-day request.
            GscDimensionProfile.SEARCH_APPEARANCE: ("searchAppearance",),
        }[self]


DEFAULT_GSC_PROFILES = (
    GscDimensionProfile.PROPERTY,
    GscDimensionProfile.PAGE,
    GscDimensionProfile.QUERY,
    GscDimensionProfile.QUERY_PAGE,
    GscDimensionProfile.COUNTRY_DEVICE,
    GscDimensionProfile.SEARCH_APPEARANCE,
)


class GscSearchAnalyticsSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    property_ref: str
    host_site_id: str
    start_date: date
    end_date: date
    profiles: tuple[GscDimensionProfile, ...] = DEFAULT_GSC_PROFILES
    search_type: Literal["web", "image", "video", "news", "discover", "googleNews"] = "web"
    row_limit: int = Field(default=25_000, ge=1, le=25_000)
    max_pages_per_profile: int = Field(default=20, ge=1, le=100)

    @field_validator("property_ref", "host_site_id")
    @classmethod
    def require_nonblank(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("GSC property and host site references must be nonblank")
        return normalized

    @model_validator(mode="after")
    def validate_window_and_profiles(self) -> GscSearchAnalyticsSettings:
        if self.end_date < self.start_date:
            raise ValueError("GSC end_date must be on or after start_date")
        if not self.profiles:
            raise ValueError("GSC collection requires at least one dimension profile")
        if len(self.profiles) != len(set(self.profiles)):
            raise ValueError("GSC dimension profiles must be unique")
        if len(self.profiles) > len(DEFAULT_GSC_PROFILES):
            raise ValueError("GSC dimension profile count exceeds the approved bound")
        return self

    def request_body(
        self,
        profile: GscDimensionProfile,
        start_row: int,
        *,
        observed_date: date | None = None,
    ) -> dict[str, Any]:
        if profile is GscDimensionProfile.SEARCH_APPEARANCE:
            if observed_date is None:
                raise ValueError("GSC search appearance requests require one observed date")
            start_date = end_date = observed_date
        else:
            if observed_date is not None:
                raise ValueError("GSC observed_date is only valid for search appearance")
            start_date = self.start_date
            end_date = self.end_date
        return {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "dimensions": list(profile.dimensions),
            "type": self.search_type,
            "rowLimit": self.row_limit,
            "startRow": start_row,
            "dataState": "final",
        }


class GscApiResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any]
    status_code: int = 200
    # Exact outbound request evidence (DEF-1x parity contract). Optional so
    # existing fixture/fake clients built before this field keep working —
    # a client that doesn't populate it simply yields no request evidence.
    request_url: str = ""
    request_method: str = "POST"
    headers: dict[str, str] = Field(default_factory=dict)


class GscSearchAnalyticsClient(Protocol):
    async def query(self, property_ref: str, request_body: Mapping[str, Any]) -> GscApiResponse: ...


GscClientFactory = Callable[[ResolvedCredential], GscSearchAnalyticsClient]
GscPageResourceResolver = Callable[[CollectionRequest, str, list[str]], Awaitable[dict[str, str]]]


class GscCollectionError(RuntimeError):
    def __init__(
        self,
        *,
        attempts: int,
        message: str,
        response: GscApiResponse | None = None,
    ) -> None:
        self.attempts = attempts
        self.response = response
        super().__init__(message)


class GscTransportError(RuntimeError):
    pass


def plan_gsc_window(
    *,
    as_of: date,
    last_successful_end: date | None = None,
    initial_backfill_days: int = GSC_DEFAULT_INITIAL_BACKFILL_DAYS,
    late_refresh_days: int = GSC_DEFAULT_LATE_REFRESH_DAYS,
) -> tuple[date, date]:
    if initial_backfill_days < 1 or late_refresh_days < 1:
        raise ValueError("GSC backfill and late-refresh windows must be positive")
    # THE ASK REACHES TODAY. Every request carries `dataState=final`, so
    # Google OMITS days it has not finalized rather than returning
    # provisional numbers for them — asking through today can therefore
    # never import unsettled data, and stopping short of today is pure
    # self-harm (it is how the Sync button became unable to fetch the
    # freshest day Google actually had). There is no published publish-hour
    # to schedule around: Google states the export runs "once per day,
    # though not necessarily at the same time". Coverage is decided by what
    # comes BACK, never by how far we asked — see `gsc_last_successful_end`.
    end = as_of
    late_start = end - timedelta(days=late_refresh_days - 1)
    if last_successful_end is None:
        start = end - timedelta(days=initial_backfill_days - 1)
    else:
        start = min(last_successful_end + timedelta(days=1), late_start)
    return start, end


class GscSearchConsoleAdapter(SeoProviderAdapter):
    provider = "gsc"
    capabilities = (SeoCapability.SEARCH_PERFORMANCE,)
    operations = (GSC_SEARCH_ANALYTICS_OPERATION,)
    _RETRYABLE_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})

    def __init__(
        self,
        *,
        client_factory: GscClientFactory,
        page_resource_resolver: GscPageResourceResolver | None = None,
        max_attempts: int = 3,
        base_backoff_seconds: float = 0.5,
        max_retry_delay_seconds: float = 8.0,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("GSC max_attempts must be positive")
        if base_backoff_seconds < 0 or max_retry_delay_seconds < 0:
            raise ValueError("GSC retry delays cannot be negative")
        self._client_factory = client_factory
        self._page_resource_resolver = page_resource_resolver
        self._max_attempts = max_attempts
        self._base_backoff = base_backoff_seconds
        self._max_retry_delay = max_retry_delay_seconds
        self._sleep = sleep
        self._client: ContextVar[GscSearchAnalyticsClient | None] = ContextVar(
            f"gsc_search_analytics_client_{id(self)}", default=None
        )

    async def authenticate(self, credential: ResolvedCredential) -> None:
        missing = [
            key
            for key in GSC_SEARCH_ANALYTICS_OPERATION.credential_keys
            if not credential.values.get(key)
        ]
        if missing:
            raise ValueError(f"GSC OAuth credential is missing: {', '.join(missing)}")
        if credential.reference_kind not in {
            None,
            CredentialReferenceKind.INTEGRATION_CONNECTION,
        }:
            raise ValueError("GSC requires a per-client integration connection")
        self._client.set(self._client_factory(credential))

    async def collect_response(
        self,
        request: CollectionRequest,
        execution: ProviderExecutionContext,
    ) -> ProviderResponse:
        if request.operation != GSC_SEARCH_ANALYTICS_OPERATION.name:
            raise ValueError(f"unsupported GSC operation {request.operation!r}")
        client = self._client.get()
        if client is None:
            raise RuntimeError("GSC adapter must be authenticated before collection")
        settings = GscSearchAnalyticsSettings.model_validate(request.settings)
        checkpoints = {
            task.external_task_id: task
            for task in await execution.resumable_tasks()
            if task.endpoint == GSC_SEARCH_ANALYTICS_OPERATION.name and task.status == "completed"
        }
        raw_pages: list[dict[str, Any]] = []
        call_records: list[ProviderCallRecord] = []
        failures: list[dict[str, Any]] = []
        for profile in settings.profiles:
            if profile is GscDimensionProfile.SEARCH_APPEARANCE:
                day_count = (settings.end_date - settings.start_date).days + 1
                observed_dates: tuple[date | None, ...] = tuple(
                    settings.start_date + timedelta(days=offset) for offset in range(day_count)
                )
            else:
                observed_dates = (None,)
            for observed_date in observed_dates:
                start_row = 0
                for page_index in range(settings.max_pages_per_profile):
                    request_body = settings.request_body(
                        profile,
                        start_row,
                        observed_date=observed_date,
                    )
                    checkpoint_id = stable_hash(
                        [
                            self.provider,
                            execution.run.id,
                            settings.property_ref,
                            profile.value,
                            request_body,
                        ]
                    )
                    checkpoint = checkpoints.get(checkpoint_id)
                    if checkpoint is not None:
                        page = _page_from_checkpoint(checkpoint, profile)
                        raw_pages.append(page)
                        call_records.append(_call_from_checkpoint(checkpoint, page))
                        row_count = _row_count(page["response"])
                    else:
                        fetched_at = datetime.now(UTC)
                        provider_call_key = stable_hash(
                            [checkpoint_id, fetched_at.isoformat(), request.request_id]
                        )
                        try:
                            api_response, attempts = await self._query_with_retry(
                                client,
                                settings.property_ref,
                                request_body,
                            )
                        except GscCollectionError as exc:
                            failure = {
                                "profile": profile.value,
                                "observed_date": (
                                    observed_date.isoformat() if observed_date is not None else None
                                ),
                                "start_row": start_row,
                                "type": type(exc).__name__,
                                "message": str(exc),
                            }
                            failures.append(failure)
                            failed_at = datetime.now(UTC)
                            checkpoint = ProviderTaskCheckpoint(
                                external_task_id=checkpoint_id,
                                endpoint=GSC_SEARCH_ANALYTICS_OPERATION.name,
                                status="failed",
                                request_payload={
                                    "profile": profile.value,
                                    "property_ref": settings.property_ref,
                                    "request": request_body,
                                    "provider_call_key": provider_call_key,
                                    "request_evidence": _request_evidence(exc.response),
                                },
                                request_count=exc.attempts,
                                provider_cost=Decimal(0),
                                currency="USD",
                                submitted_at=fetched_at,
                                last_polled_at=failed_at,
                                completed_at=failed_at,
                                response_payload=(
                                    exc.response.payload if exc.response is not None else None
                                ),
                                error=failure,
                            )
                            await execution.checkpoint(checkpoint)
                            page = {
                                "profile": profile.value,
                                "request": request_body,
                                "response": (
                                    exc.response.payload
                                    if exc.response is not None
                                    else {"transport_error": failure}
                                ),
                                "status_code": (
                                    exc.response.status_code if exc.response is not None else None
                                ),
                                "quota_headers": (
                                    _quota_headers(exc.response.headers)
                                    if exc.response is not None
                                    else {}
                                ),
                                "request_evidence": _request_evidence(exc.response),
                                "error": failure,
                            }
                            raw_pages.append(page)
                            call_records.append(_call_from_checkpoint(checkpoint, page))
                            break
                        page = {
                            "profile": profile.value,
                            "request": request_body,
                            "response": api_response.payload,
                            "status_code": api_response.status_code,
                            "quota_headers": _quota_headers(api_response.headers),
                            "request_evidence": _request_evidence(api_response),
                        }
                        raw_pages.append(page)
                        row_count = _row_count(api_response.payload)
                        completed_at = datetime.now(UTC)
                        checkpoint = ProviderTaskCheckpoint(
                            external_task_id=checkpoint_id,
                            endpoint=GSC_SEARCH_ANALYTICS_OPERATION.name,
                            status="completed",
                            request_payload={
                                "profile": profile.value,
                                "property_ref": settings.property_ref,
                                "request": request_body,
                                "provider_call_key": provider_call_key,
                                "quota_headers": page["quota_headers"],
                                "request_evidence": page["request_evidence"],
                            },
                            response_payload=api_response.payload,
                            request_count=attempts,
                            provider_cost=Decimal(0),
                            currency="USD",
                            submitted_at=fetched_at,
                            last_polled_at=completed_at,
                            completed_at=completed_at,
                        )
                        await execution.checkpoint(checkpoint)
                        call_records.append(_call_from_checkpoint(checkpoint, page))
                    if row_count < settings.row_limit:
                        break
                    start_row += row_count
                else:
                    failures.append(
                        {
                            "profile": profile.value,
                            "observed_date": (
                                observed_date.isoformat() if observed_date is not None else None
                            ),
                            "start_row": start_row,
                            "type": "GscPaginationLimit",
                            "message": "approved max_pages_per_profile was exhausted",
                        }
                    )
        fetched_at = datetime.now(UTC)
        error = None
        if failures:
            error = {
                "type": "GscPartialCollectionError",
                "message": f"{len(failures)} GSC profile page(s) failed",
                "failures": failures,
            }
        return ProviderResponse(
            raw={
                "property_ref": settings.property_ref,
                "window": {
                    "start_date": settings.start_date.isoformat(),
                    "end_date": settings.end_date.isoformat(),
                    "data_state": "final",
                    "search_type": settings.search_type,
                },
                "profiles": [profile.value for profile in settings.profiles],
                "pages": raw_pages,
                "failures": failures,
            },
            fetched_at=fetched_at,
            provider_schema_version="gsc-search-analytics-v1",
            call_records=call_records,
            currency="USD",
            error=error,
        )

    async def _query_with_retry(
        self,
        client: GscSearchAnalyticsClient,
        property_ref: str,
        request_body: Mapping[str, Any],
    ) -> tuple[GscApiResponse, int]:
        last_error: Exception | None = None
        last_response: GscApiResponse | None = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                response = await client.query(property_ref, request_body)
            except (httpx.TimeoutException, httpx.TransportError, GscTransportError) as exc:
                last_error = exc
                if attempt < self._max_attempts:
                    await self._sleep(
                        min(
                            self._base_backoff * (2 ** (attempt - 1)),
                            self._max_retry_delay,
                        )
                    )
                    continue
                break
            if response.status_code < 400:
                return response, attempt
            last_response = response
            if response.status_code not in self._RETRYABLE_STATUSES:
                raise GscCollectionError(
                    attempts=attempt,
                    message=f"GSC Search Analytics HTTP {response.status_code}",
                    response=response,
                )
            last_error = RuntimeError(f"HTTP {response.status_code}")
            if attempt < self._max_attempts:
                await self._sleep(
                    min(
                        self._base_backoff * (2 ** (attempt - 1)),
                        self._max_retry_delay,
                    )
                )
        raise GscCollectionError(
            attempts=self._max_attempts,
            message=f"GSC Search Analytics retries exhausted: {last_error}",
            response=last_response,
        )

    async def normalize(
        self,
        response: ProviderResponse,
        context: NormalizationContext,
    ) -> list[SeoObservation]:
        if not isinstance(response.raw, dict):
            raise TypeError("GSC raw response must be an object")
        settings = GscSearchAnalyticsSettings.model_validate(context.request.settings)
        site = await context.resolve_host_binding(
            HostBindingRequest(resource_kind="web_site", resource_id=settings.host_site_id)
        )
        pages = response.raw.get("pages")
        if not isinstance(pages, list):
            raise TypeError("GSC raw response must contain pages")
        parsed_rows, page_urls, queries = await asyncio.to_thread(_parse_and_index_rows, pages)
        page_ids_by_url: dict[str, str] = {}
        if page_urls and self._page_resource_resolver is None:
            raise RuntimeError("GSC page observations require the canonical host page resolver")
        if page_urls and self._page_resource_resolver is not None:
            resources = await self._page_resource_resolver(
                context.request,
                settings.host_site_id,
                page_urls,
            )
            missing_urls = sorted(set(page_urls) - set(resources))
            if missing_urls:
                raise ValueError(
                    f"GSC could not resolve {len(missing_urls)} page URL(s) "
                    "to canonical in-scope web pages"
                )
            for page_url, resource_id in resources.items():
                binding = await context.resolve_host_binding(
                    HostBindingRequest(resource_kind="web_page", resource_id=resource_id)
                )
                if binding.site_id != site.site_id:
                    raise ValueError("GSC page binding resolved outside the requested site")
                if binding.page_id is None:
                    raise ValueError("GSC web_page binding resolved without a page id")
                page_ids_by_url[page_url] = binding.page_id
        identity_requests = await asyncio.to_thread(_identity_requests, queries)
        identities = await context.resolve_identities(identity_requests)
        keyword_ids = {
            query: identity.keyword_id for query, identity in zip(queries, identities, strict=True)
        }
        return await asyncio.to_thread(
            _build_observations,
            parsed_rows,
            site.site_id,
            page_ids_by_url,
            keyword_ids,
            settings.search_type,
        )


def _row_count(payload: dict[str, Any]) -> int:
    rows = payload.get("rows")
    if rows is None:
        return 0
    if not isinstance(rows, list):
        raise ValueError("GSC response rows must be a list")
    return len(rows)


def _quota_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower().startswith(("x-goog-", "x-ratelimit-", "retry-after"))
    }


def _request_evidence(response: GscApiResponse | None) -> dict[str, Any]:
    """Exact outbound request evidence (DEF-1x parity contract) — GSC's OAuth
    bearer token is redacted; the resolved per-property URL and HTTP method
    are the real values the transport used."""

    return {
        "method": response.request_method if response is not None else "POST",
        "url": response.request_url if response is not None else "",
        "headers": {"Authorization": "Bearer ***"},
    }


def _page_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint,
    profile: GscDimensionProfile,
) -> dict[str, Any]:
    if not isinstance(checkpoint.response_payload, dict):
        raise ValueError("completed GSC checkpoint has no response payload")
    request_payload = checkpoint.request_payload
    return {
        "profile": profile.value,
        "request": request_payload["request"],
        "response": checkpoint.response_payload,
        "status_code": 200,
        "quota_headers": request_payload.get("quota_headers", {}),
        "request_evidence": request_payload.get("request_evidence", _request_evidence(None)),
        "resumed_from_checkpoint": True,
    }


def _call_from_checkpoint(
    checkpoint: ProviderTaskCheckpoint,
    page: dict[str, Any],
) -> ProviderCallRecord:
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
            "profile": page["profile"],
            "request": page["request"],
            "row_count": _row_count(page["response"]),
            "status_code": page.get("status_code"),
            "response_status": page.get("status_code"),
            "attempts": checkpoint.request_count,
            "quota_headers": page.get("quota_headers", {}),
            "request_evidence": page.get("request_evidence", _request_evidence(None)),
            "error": page.get("error"),
        },
    )


def _parse_rows(pages: list[Any]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        request = page.get("request")
        response = page.get("response")
        if not isinstance(request, dict) or not isinstance(response, dict):
            continue
        dimensions = request.get("dimensions")
        rows = response.get("rows") or []
        if not isinstance(dimensions, list) or not isinstance(rows, list):
            raise ValueError("GSC page dimensions and rows must be lists")
        for raw in rows:
            if not isinstance(raw, dict):
                continue
            keys = raw.get("keys")
            if not isinstance(keys, list) or len(keys) != len(dimensions):
                raise ValueError("GSC row keys do not match requested dimensions")
            values = dict(zip(dimensions, keys, strict=True))
            raw_date = values.pop("date", None)
            if raw_date is None and page.get("profile") == "search_appearance":
                start_date = request.get("startDate")
                end_date = request.get("endDate")
                if start_date != end_date:
                    raise ValueError("GSC search appearance rows require a single-day request")
                raw_date = start_date
            try:
                observed_date = date.fromisoformat(str(raw_date))
            except ValueError as exc:
                raise ValueError("GSC daily row has an invalid date") from exc
            parsed.append(
                {
                    **values,
                    "date": observed_date,
                    "clicks": _nonnegative_metric(raw.get("clicks", 0), "clicks"),
                    "impressions": _nonnegative_metric(raw.get("impressions", 0), "impressions"),
                    "ctr": _bounded_decimal(raw.get("ctr", 0), "ctr", Decimal(1)),
                    "position": _bounded_decimal(raw.get("position", 0), "position", None),
                    "profile": page["profile"],
                    "responseAggregationType": response.get("responseAggregationType"),
                }
            )
    return parsed


def _parse_and_index_rows(
    pages: list[Any],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    parsed_rows = _parse_rows(pages)
    page_urls = sorted({row["page"] for row in parsed_rows if row.get("page")})
    queries = sorted({row["query"] for row in parsed_rows if row.get("query")})
    return parsed_rows, page_urls, queries


def _identity_requests(queries: list[str]) -> list[SeoIdentityRequest]:
    return [
        SeoIdentityRequest(
            keyword=query,
            language="und",
            settings={"source": "gsc_search_analytics"},
        )
        for query in queries
    ]


def _build_observations(
    parsed_rows: list[dict[str, Any]],
    site_id: str,
    page_ids_by_url: dict[str, str],
    keyword_ids: dict[str, str],
    search_type: str,
) -> list[SeoObservation]:
    observations: list[SeoObservation] = []
    for row in parsed_rows:
        country = row.get("country")
        if country is not None:
            country = _validated_country(country)
        page_url = row.get("page")
        observations.append(
            SearchPerformanceObservation(
                site_id=site_id,
                page_id=page_ids_by_url.get(page_url),
                keyword_id=keyword_ids.get(row.get("query")),
                date=row["date"],
                query=row.get("query"),
                country=country,
                device=(
                    str(row["device"]).strip().lower() if row.get("device") is not None else None
                ),
                dimension_profile=row["profile"],
                search_appearance=row.get("searchAppearance"),
                clicks=int(row["clicks"]),
                impressions=int(row["impressions"]),
                ctr=Decimal(str(row["ctr"])),
                average_position=Decimal(str(row["position"])),
                extras={
                    "page_url": page_url,
                    "search_type": search_type,
                    "data_state": "final",
                    "response_aggregation_type": row.get("responseAggregationType"),
                },
            )
        )
    return observations


def _nonnegative_metric(value: Any, name: str) -> int:
    metric = Decimal(str(value))
    if not metric.is_finite() or metric < 0 or metric != metric.to_integral_value():
        raise ValueError(f"GSC {name} must be a nonnegative whole number")
    return int(metric)


def _bounded_decimal(value: Any, name: str, maximum: Decimal | None) -> Decimal:
    metric = Decimal(str(value))
    if not metric.is_finite() or metric < 0 or (maximum is not None and metric > maximum):
        raise ValueError(f"GSC {name} is outside its documented bounds")
    return metric


def _validated_country(value: Any) -> str:
    country = str(value).strip().lower()
    if len(country) != 3 or not country.isalpha():
        raise ValueError("GSC country must be its documented three-letter code")
    return country


__all__ = [
    "DEFAULT_GSC_PROFILES",
    "GSC_TIMEZONE",
    "GSC_SEARCH_ANALYTICS_OPERATION",
    "GscApiResponse",
    "GscDimensionProfile",
    "GscSearchAnalyticsSettings",
    "GscSearchConsoleAdapter",
    "GscTransportError",
    "gsc_today",
    "plan_gsc_window",
]
