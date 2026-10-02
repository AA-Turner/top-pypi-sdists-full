from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from matrx_seo.adapters import ProviderExecutionContext
from matrx_seo.contracts import (
    BacklinkSnapshotObservation,
    CollectionRequest,
    NormalizationContext,
    ResolvedCredential,
    SeoCapability,
)
from matrx_seo.providers.dataforseo import DataForSeoAdapter, DataForSeoWorkflow
from matrx_seo.providers.dataforseo.contracts import DataForSeoCollectionSettings
from matrx_seo.providers.dataforseo.transport import ReplayTransport
from matrx_seo.repository import InMemorySeoRepository
from matrx_seo.service import SeoCollectionService


def _summary_envelope() -> dict[str, object]:
    return {
        "version": "0.1.20260722",
        "status_code": 20000,
        "status_message": "Ok.",
        "cost": 0.02,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": "backlink-summary-task",
                "status_code": 20000,
                "status_message": "Ok.",
                "cost": 0.02,
                "result_count": 1,
                "result": [
                    {
                        "target": "example.com",
                        "rank": 321,
                        "backlinks": 12,
                        "backlinks_nofollow": 2,
                        "referring_domains": 5,
                    }
                ],
            }
        ],
    }


def _request(*, site_id: str | None = "site-1") -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=SeoCapability.BACKLINKS,
        operation="backlinks.core",
        target_ref=f"web.site:{site_id or 'missing'}",
        site_id=site_id,
        observation_period=datetime.now(UTC).isoformat(),
        settings={
            "workflow": "live",
            "endpoint": "/v3/backlinks/summary/live",
            "tasks": [{"target": "example.com"}],
        },
        force_refresh=True,
    )


async def _credential(*_args: object) -> ResolvedCredential:
    return ResolvedCredential(
        values={
            "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
            "DATA_FOR_SEO_PASSWORD": "fixture",
        }
    )


async def _authorize(request: CollectionRequest) -> CollectionRequest:
    return request


@pytest.mark.asyncio
async def test_adapter_normalizes_backlink_response_for_bound_site() -> None:
    adapter = DataForSeoAdapter(transport=ReplayTransport([_summary_envelope()]))
    await adapter.authenticate(await _credential())
    repository = InMemorySeoRepository()
    request = _request()
    run = await repository.start_run("dataforseo", request)
    response = await adapter.collect_response(
        request,
        ProviderExecutionContext(repository, run),
    )

    observations = await adapter.normalize(
        response,
        NormalizationContext(
            request=request,
            run=run,
            raw_payload_id="raw-id",
            identity_resolver=object(),
            host_binding_resolver=object(),
        ),
    )

    assert len(observations) == 1
    snapshot = observations[0]
    assert isinstance(snapshot, BacklinkSnapshotObservation)
    assert snapshot.site_id == "site-1"
    assert snapshot.dataset == "summary"
    assert snapshot.total_backlinks == 12
    assert snapshot.dofollow_backlinks == 10


@pytest.mark.asyncio
async def test_collection_service_persists_raw_and_normalized_backlink_evidence() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credential,
        collection_authorizer=_authorize,
    )

    receipt = await service.collect(
        DataForSeoAdapter(transport=ReplayTransport([_summary_envelope()])),
        _request(),
    )

    assert receipt.raw_payload_id is not None
    assert receipt.created_observations == 1
    assert len(repository.raw_payloads) == 1
    assert len(repository.observations) == 1
    stored = next(iter(repository.observations.values()))["observation"]
    assert isinstance(stored, BacklinkSnapshotObservation)
    assert stored.referring_domains == 5


@pytest.mark.asyncio
async def test_canonical_backlink_normalization_rejects_unbound_site() -> None:
    adapter = DataForSeoAdapter(transport=ReplayTransport([_summary_envelope()]))
    await adapter.authenticate(await _credential())
    repository = InMemorySeoRepository()
    request = _request(site_id=None)
    run = await repository.start_run("dataforseo", request)
    response = await adapter.collect_response(
        request,
        ProviderExecutionContext(repository, run),
    )

    with pytest.raises(ValueError, match="requires site_id"):
        await adapter.normalize(
            response,
            NormalizationContext(
                request=request,
                run=run,
                raw_payload_id="raw-id",
                identity_resolver=object(),
                host_binding_resolver=object(),
            ),
        )


def test_mixed_target_backlink_batch_is_rejected_before_the_request_exists() -> None:
    """Two targets can never reach canonical backlink normalization.

    Every SUPPORTED_BACKLINK_ENDPOINTS entry is a `/live` endpoint, and a live
    endpoint completes inside the POST with exactly one task — so a two-target
    backlink batch is now rejected while the settings are being BUILT, before a
    seo.collection_run row exists.  This used to be caught much later, inside
    `_normalize_backlinks` ("one shared target"); that check remains as a
    backstop for any future non-live backlink endpoint, but the failure class is
    now structurally impossible one layer earlier.
    """

    with pytest.raises(ValidationError, match="accept exactly one task"):
        DataForSeoCollectionSettings(
            workflow=DataForSeoWorkflow.LIVE,
            endpoint="/v3/backlinks/summary/live",
            tasks=[{"target": "example.com"}, {"target": "other.example"}],
        )
