"""Shared API contracts for the SEO vertical (M-12 / WS-13).

Response/request DTOs, the run-status/evidence projections, and the
DataForSEO operation catalog used by BOTH the standalone FastAPI app
(``matrx_seo.standalone.app``) and the aidream host router
(``aidream/api/routers/seo_collections.py``). One implementation — host and
standalone import the SAME public contracts here; neither forks its own copy
and the host never reaches into ``standalone.app`` for them.

``standalone/app.py`` stays a thin FastAPI shell: request parsing, dependency
wiring, and HTTP error mapping only. Everything shape- or projection-related
lives here.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from matrx_seo.backlink_refresh import BacklinkRefreshProfile
from matrx_seo.contracts import (
    CollectionReceipt,
    CollectionRun,
    CollectionTrigger,
    CredentialReferenceKind,
    SeoCapability,
)
from matrx_seo.providers.dataforseo.backlinks import supports_backlink_endpoint
from matrx_seo.providers.dataforseo.link_gap import supports_intersection_endpoint
from matrx_seo.providers.dataforseo.operations import APPROVED_OPERATIONS


class CollectionCreateRequest(BaseModel):
    """Body for ``POST /collections`` — :class:`CollectionRequest` minus
    ``created_by`` (always the authenticated user, never caller-supplied)."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    organization_id: str
    capability: SeoCapability
    operation: str
    target_ref: str
    site_id: str | None = None
    page_id: str | None = None
    source_crawl_session_id: str | None = None
    observation_period: str
    settings: dict[str, Any] = Field(default_factory=dict)  # api-any-ok: provider passthrough
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND
    credential_reference_id: str | None = None
    credential_reference_kind: CredentialReferenceKind = CredentialReferenceKind.PLATFORM_SECRET
    request_id: str | None = None
    execution_id: UUID | None = None
    resume_existing: bool = False
    force_refresh: bool = False

    @field_validator("provider", "organization_id", mode="before")
    @classmethod
    def require_nonblank(cls, value: Any) -> str:
        normalized = str(value).strip()
        if not normalized:
            raise ValueError("must be nonblank")
        return normalized


class RunStatusResponse(BaseModel):
    id: str
    provider: str
    capability: str
    operation: str
    trigger: str
    status: str
    target_ref: str
    site_id: str | None = None
    page_id: str | None = None
    source_crawl_session_id: str | None = None
    observation_period: str
    organization_id: str
    created_by: str
    attempt_count: int
    requested_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    request_count: int = 0
    reported_cost: Decimal | None = None
    estimated_cost: Decimal | None = None
    currency: str = "USD"
    error: dict[str, Any] | None = None  # api-any-ok: structured provider error passthrough
    receipt: CollectionReceipt | None = None
    result: dict[str, Any] | None = None  # api-any-ok: command-run final result document


class RunListResponse(BaseModel):
    organization_id: str
    runs: list[RunStatusResponse]


class BacklinkRefreshCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    profile: BacklinkRefreshProfile = BacklinkRefreshProfile.BOOTSTRAP
    detail_limit: int = Field(default=1000, ge=1, le=1000)
    detail_max_rows: int = Field(default=10_000, ge=1, le=100_000)
    force_refresh: bool = True
    request_id: str | None = None
    source_crawl_session_id: str | None = None

    @field_validator("organization_id", mode="before")
    @classmethod
    def require_nonblank(cls, value: Any) -> str:
        normalized = str(value).strip()
        if not normalized:
            raise ValueError("must be nonblank")
        return normalized


class WhoAmIResponse(BaseModel):
    user_id: str
    organization_id: str


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user_id: str
    email: str


class RankObservationOut(BaseModel):
    organic_rank: int | None = None
    absolute_rank: int | None = None
    matched_domain: str | None = None
    matched_url: str | None = None
    engine: str
    device: str
    observed_at: datetime


class RunObservationsResponse(BaseModel):
    run_id: str
    observations: list[RankObservationOut]


class DataForSeoEndpointExampleOut(BaseModel):
    endpoint: str
    workflow: str
    task: dict[str, Any]


class DataForSeoOperationOut(BaseModel):
    name: str
    family: str
    capabilities: list[str]
    endpoints: list[str]
    workflows: list[str]
    pricing_key: str
    raw_only: bool
    canonical_normalizer: bool
    freshness_ttl_seconds: int
    endpoint_examples: list[DataForSeoEndpointExampleOut]


class DataForSeoOperationsResponse(BaseModel):
    operations: list[DataForSeoOperationOut]


class ProviderCallEvidenceOut(BaseModel):
    id: str
    provider_call_key: str
    external_task_id: str | None = None
    request_count: int
    reported_cost: Decimal | None = None
    estimated_cost: Decimal | None = None
    currency: str
    fetched_at: datetime
    metadata: dict[str, Any]  # api-any-ok: exact provider evidence


class ProviderTaskEvidenceOut(BaseModel):
    id: str
    external_task_id: str
    endpoint: str | None = None
    status: str
    request_payload: dict[str, Any]  # api-any-ok: exact provider task body
    response_payload: dict[str, Any] | None = None  # api-any-ok: exact task envelope
    request_count: int
    provider_cost: Decimal | None = None
    estimated_cost: Decimal | None = None
    currency: str
    submitted_at: datetime
    last_polled_at: datetime | None = None
    completed_at: datetime | None = None
    error: dict[str, Any] | None = None  # api-any-ok: provider error shape


class RawPayloadEvidenceOut(BaseModel):
    id: str
    checksum: str
    size_bytes: int
    content_type: str
    payload: dict[str, Any] | list[Any] | None  # api-any-ok: literal provider JSON
    cloud_file_id: str | None = None
    provider_schema_version: str | None = None
    external_task_id: str | None = None
    fetched_at: datetime
    offload_error: dict[str, Any] | None = None  # api-any-ok: structured storage error
    created_at: datetime


class RunEvidenceResponse(BaseModel):
    run_id: str
    provider: str
    operation: str
    request: dict[str, Any]  # api-any-ok: persisted collection request
    provider_calls: list[ProviderCallEvidenceOut]
    provider_tasks: list[ProviderTaskEvidenceOut]
    raw_payloads: list[RawPayloadEvidenceOut]


def dataforseo_operations_catalog() -> DataForSeoOperationsResponse:
    """The approved DataForSEO operation catalog, projected for the API."""
    return DataForSeoOperationsResponse(
        operations=[
            DataForSeoOperationOut(
                name=operation.name.value,
                family=operation.family,
                capabilities=[capability.value for capability in operation.capabilities],
                endpoints=list(operation.endpoints),
                workflows=[workflow.value for workflow in operation.workflows],
                pricing_key=operation.pricing_key,
                raw_only=operation.raw_only,
                canonical_normalizer=(
                    operation.name.value == "keywords.google_ads.search_volume"
                    or (
                        SeoCapability.BACKLINKS in operation.capabilities
                        and any(
                            supports_backlink_endpoint(endpoint)
                            or supports_intersection_endpoint(endpoint)
                            for endpoint in operation.endpoints
                        )
                    )
                ),
                freshness_ttl_seconds=operation.provider_operation.freshness_ttl_seconds,
                endpoint_examples=[
                    DataForSeoEndpointExampleOut(
                        endpoint=example.endpoint,
                        workflow=example.workflow.value,
                        task=example.task,
                    )
                    for example in operation.endpoint_examples
                ],
            )
            for operation in APPROVED_OPERATIONS
        ]
    )


def _contract_run(row: Any) -> CollectionRun:
    """Rebuild the contract-level run from a ``seo.collection_run`` row so the
    ONE receipt implementation (``OrmSeoRepository.receipt_for_run``) serves
    reads too — never a second receipt computation. Delegates to the ONE
    row→contract projection (``orm_repository.run_from_row``)."""
    from matrx_seo.orm_repository import run_from_row

    return run_from_row(row)


async def run_status_response(
    repository: Any, row: Any, *, receipt: CollectionReceipt | None = None
) -> RunStatusResponse:
    """Project a ``seo.collection_run`` row into :class:`RunStatusResponse`,
    computing the receipt for a completed run through the ONE repository
    receipt implementation."""
    if receipt is None and row.status == "completed":
        receipt = await repository.receipt_for_run(_contract_run(row))
    return RunStatusResponse(
        id=str(row.id),
        provider=row.provider,
        capability=row.capability,
        operation=row.operation,
        trigger=row.trigger,
        status=row.status,
        target_ref=row.target_ref,
        site_id=str(row.site_id) if row.site_id else None,
        page_id=str(row.page_id) if row.page_id else None,
        source_crawl_session_id=(
            str(row.source_crawl_session_id) if row.source_crawl_session_id else None
        ),
        observation_period=row.observation_period,
        organization_id=str(row.organization_id),
        created_by=str(row.created_by),
        attempt_count=row.attempt_count,
        requested_at=row.requested_at,
        started_at=row.started_at,
        completed_at=row.completed_at,
        request_count=row.request_count,
        reported_cost=row.reported_cost,
        estimated_cost=row.estimated_cost,
        currency=row.currency,
        error=row.error,
        receipt=receipt,
        result=row.result if isinstance(row.result, dict) else None,
    )


def _stored_counts(rows: list[Any]) -> dict[str, int]:
    """``{run id: observation count}`` for the rows that recorded one when they finished."""
    from matrx_seo.orm_repository import stored_observation_count

    out: dict[str, int] = {}
    for r in rows:
        count = stored_observation_count(r)
        if count is not None:
            out[str(r.id)] = count
    return out


async def run_status_responses(
    repository: Any, rows: list[Any], *, receipts: dict[str, CollectionReceipt] | None = None
) -> list[RunStatusResponse]:
    """:func:`run_status_response` for a LIST of rows: every completed run's receipt comes from
    ONE batched repository read (``receipts_for_runs``), never one query set per row. ``receipts``
    are ones already read (a run without one is asked for in a single further batch)."""
    have = dict(receipts or {})
    missing = [_contract_run(r) for r in rows if r.status == "completed" and str(r.id) not in have]
    batched = getattr(repository, "receipts_for_runs", None)
    if missing and batched is not None:
        have.update(await batched(missing, stored_counts=_stored_counts(rows)))
    return [await run_status_response(repository, r, receipt=have.get(str(r.id))) for r in rows]


async def discoverable_run_status_page(
    repository: Any, user_id: str | None, *, organization_id: str | None = None, limit: int = 25
) -> list[RunStatusResponse]:
    """The runs list both routes serve: the newest ``limit`` runs the person may enumerate (all
    her organizations, or the one named), with receipts — the receipt batch for the newest rows
    runs WHILE the kernel answers which runs are hers, so the page costs one wait, not two."""
    from matrx_seo.access import list_discoverable_runs

    batched = getattr(repository, "receipts_for_runs", None)

    async def early(first: list[Any]) -> dict[str, CollectionReceipt]:
        done = [_contract_run(r) for r in first if r.status == "completed"]
        if batched is None or not done:
            return {}
        return await batched(done, stored_counts=_stored_counts(first))

    rows, receipts = await list_discoverable_runs(
        user_id, organization_id=organization_id, limit=limit, while_waiting=early
    )
    return await run_status_responses(repository, rows, receipts=receipts or {})


async def run_evidence_response(row: Any) -> RunEvidenceResponse:
    """Project a ``seo.collection_run`` row plus its provider-call/task/raw-
    payload evidence into :class:`RunEvidenceResponse`."""
    from matrx_seo.db import models_seo as m

    run_id = str(row.id)
    calls = await m.ProviderCall.filter(run_id=run_id).order_by("fetched_at").all()
    tasks = await m.ProviderTask.filter(run_id=run_id).order_by("submitted_at").all()
    payloads = await m.RawPayload.filter(run_id=run_id).order_by("created_at").all()
    return RunEvidenceResponse(
        run_id=run_id,
        provider=row.provider,
        operation=row.operation,
        request={
            "provider": row.provider,
            "organization_id": str(row.organization_id),
            "capability": row.capability,
            "operation": row.operation,
            "target_ref": row.target_ref,
            "site_id": str(row.site_id) if row.site_id else None,
            "page_id": str(row.page_id) if row.page_id else None,
            "source_crawl_session_id": (
                str(row.source_crawl_session_id) if row.source_crawl_session_id else None
            ),
            "observation_period": row.observation_period,
            "settings": row.settings or {},
            "trigger": row.trigger,
            "credential_reference_id": row.credential_reference_id,
            "credential_reference_kind": row.credential_reference_kind,
            "request_id": row.request_id,
            "execution_id": str(row.execution_id) if row.execution_id else None,
        },
        provider_calls=[
            ProviderCallEvidenceOut(
                id=str(call.id),
                provider_call_key=call.provider_call_key,
                external_task_id=call.external_task_id,
                request_count=call.request_count,
                reported_cost=call.reported_cost,
                estimated_cost=call.estimated_cost,
                currency=call.currency,
                fetched_at=call.fetched_at,
                metadata=call.metadata or {},
            )
            for call in calls
        ],
        provider_tasks=[
            ProviderTaskEvidenceOut(
                id=str(task.id),
                external_task_id=task.external_task_id,
                endpoint=task.endpoint,
                status=task.status,
                request_payload=task.request_payload or {},
                response_payload=task.response_payload,
                request_count=task.request_count,
                provider_cost=task.provider_cost,
                estimated_cost=task.estimated_cost,
                currency=task.currency,
                submitted_at=task.submitted_at,
                last_polled_at=task.last_polled_at,
                completed_at=task.completed_at,
                error=task.error,
            )
            for task in tasks
        ],
        raw_payloads=[
            RawPayloadEvidenceOut(
                id=str(payload.id),
                checksum=payload.checksum,
                size_bytes=payload.size_bytes,
                content_type=payload.content_type,
                payload=payload.payload if isinstance(payload.payload, dict | list) else None,
                cloud_file_id=payload.cloud_file_id,
                provider_schema_version=payload.provider_schema_version,
                external_task_id=payload.external_task_id,
                fetched_at=payload.fetched_at,
                offload_error=payload.offload_error,
                created_at=payload.created_at,
            )
            for payload in payloads
        ],
    )


__all__ = [
    "BacklinkRefreshCreateRequest",
    "CollectionCreateRequest",
    "DataForSeoEndpointExampleOut",
    "DataForSeoOperationOut",
    "DataForSeoOperationsResponse",
    "LoginRequest",
    "LoginResponse",
    "ProviderCallEvidenceOut",
    "ProviderTaskEvidenceOut",
    "RankObservationOut",
    "RawPayloadEvidenceOut",
    "RunEvidenceResponse",
    "RunListResponse",
    "RunObservationsResponse",
    "RunStatusResponse",
    "WhoAmIResponse",
    "dataforseo_operations_catalog",
    "run_evidence_response",
    "run_status_response",
]
