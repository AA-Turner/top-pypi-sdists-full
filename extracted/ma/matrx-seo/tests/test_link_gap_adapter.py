"""The link-gap collection path, driven through the REAL adapter.

**Why this file exists.** `tests/test_domain_link_gap.py` and
`tests/test_page_link_gap.py` inject a fake collection service, so the
adapter's capability check never runs there — and
`tests/test_link_gap.py` calls the normalizer directly, so it never runs
there either. Between the two, `backlinks.intersections` shipped declaring
only `RAW_PROVIDER` while both real callers collected under `BACKLINKS`,
and `DataForSeoAdapter.collect_response` raised
"backlinks.intersections cannot collect backlinks" before any HTTP call.
Nothing failed in CI; `seo.link_gap_domain` was simply empty in production.

These tests use the real `DataForSeoAdapter`, the real
`SeoCollectionService`, and the real captured provider payload. Only the
HTTP transport is replaced.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from matrx_seo.adapters import ProviderExecutionContext
from matrx_seo.contracts import (
    CollectionRequest,
    LinkGapObservation,
    NormalizationContext,
    ResolvedCredential,
    SeoCapability,
)
from matrx_seo.link_gap_request import (
    DOMAIN_RANK_FIELD,
    DOMAIN_SPAM_FIELD,
    numbered_targets,
    rank_order_by,
    spam_score_filter,
)
from matrx_seo.providers.dataforseo import DataForSeoAdapter
from matrx_seo.providers.dataforseo.contracts import DataForSeoOperationName
from matrx_seo.providers.dataforseo.link_gap import (
    DOMAIN_INTERSECTION,
    PAGE_INTERSECTION,
)
from matrx_seo.providers.dataforseo.operations import get_operation
from matrx_seo.providers.dataforseo.transport import ReplayTransport
from matrx_seo.repository import InMemorySeoRepository
from matrx_seo.service import SeoCollectionService

FIXTURE = Path(__file__).parent / "fixtures" / "dataforseo_domain_intersection_live.json"
SITE_ID = "38eff4c9-b021-451a-b995-7d9b3d17db5e"
OPERATION = DataForSeoOperationName.BACKLINKS_INTERSECTIONS.value


def _payload() -> dict:
    return json.loads(FIXTURE.read_text())


def _task() -> dict:
    """The task the real `DomainLinkGapService` builds, shaped identically."""
    targets = numbered_targets(["shredit.com", "shrednations.com"])
    return {
        "targets": targets,
        "exclude_targets": ["datadestruction.com"],
        "intersection_mode": "partial",
        "backlinks_status_type": "live",
        "include_subdomains": False,
        "include_indirect_links": False,
        "exclude_internal_backlinks": True,
        "limit": 100,
        "order_by": rank_order_by(DOMAIN_RANK_FIELD),
        "filters": spam_score_filter(len(targets), 30, field=DOMAIN_SPAM_FIELD),
    }


def _request(*, endpoint: str = DOMAIN_INTERSECTION) -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        # Exactly what domain_link_gap.py / page_link_gap.py send.
        capability=SeoCapability.BACKLINKS,
        operation=OPERATION,
        target_ref=f"web.site:{SITE_ID}",
        site_id=SITE_ID,
        observation_period=datetime.now(UTC).isoformat(),
        settings={"workflow": "live", "endpoint": endpoint, "tasks": [_task()]},
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


class TestTheDeclaredCapability:
    """The declaration and the callers must agree, or nothing collects."""

    def test_intersections_declares_the_capability_its_callers_collect_under(self):
        operation = get_operation(OPERATION)
        assert SeoCapability.BACKLINKS in operation.capabilities
        assert SeoCapability.RAW_PROVIDER in operation.capabilities

    def test_raw_only_is_still_set(self):
        # `raw_only` exempts the operation from the "must have a registered
        # canonical normalizer" precondition; it does NOT suppress
        # normalization. Clearing it is the wrong fix and has been attempted
        # twice — see matrx-frontend/docs/handoffs/competitor-link-gap.md.
        assert get_operation(OPERATION).raw_only is True

    @pytest.mark.parametrize("endpoint", [DOMAIN_INTERSECTION, PAGE_INTERSECTION])
    def test_both_intersection_endpoints_are_reachable(self, endpoint):
        operation = get_operation(OPERATION)
        assert endpoint in operation.endpoints


@pytest.mark.asyncio
async def test_the_real_adapter_collects_and_normalizes_a_link_gap_request():
    """The end-to-end path the bug broke: no fake service anywhere."""
    adapter = DataForSeoAdapter(transport=ReplayTransport([_payload()]))
    await adapter.authenticate(await _credential())
    repository = InMemorySeoRepository()
    request = _request()
    run = await repository.start_run("dataforseo", request)

    # Before the fix this raised
    # ValueError("backlinks.intersections cannot collect backlinks").
    response = await adapter.collect_response(request, ProviderExecutionContext(repository, run))

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
    observation = observations[0]
    assert isinstance(observation, LinkGapObservation)
    assert observation.site_id == SITE_ID
    assert observation.competitor_targets == {
        "1": "shredit.com",
        "2": "shrednations.com",
    }
    assert observation.excluded_targets == ["datadestruction.com"]
    # Real gap domains, and never the competitors themselves.
    domains = {domain.normalized_domain for domain in observation.domains}
    assert domains
    assert "shredit.com" not in domains
    assert "shrednations.com" not in domains


@pytest.mark.asyncio
async def test_the_collection_service_persists_link_gap_observations():
    """`seo.link_gap_domain` being empty is what this proves cannot recur."""
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credential,
        collection_authorizer=_authorize,
    )

    receipt = await service.collect(
        DataForSeoAdapter(transport=ReplayTransport([_payload()])),
        _request(),
    )

    assert receipt.raw_payload_id is not None
    assert receipt.created_observations == 1
    stored = next(iter(repository.observations.values()))["observation"]
    assert isinstance(stored, LinkGapObservation)
    assert stored.domains


class TestTheRequestShapingThatNeverShipsDefaults:
    """The provider's default ordering returns link-farm domains."""

    def test_every_link_gap_task_orders_by_rank_and_filters_spam(self):
        task = _task()
        assert task["order_by"] == ["1.rank,desc"]
        assert task["filters"] == [
            ["1.backlinks_spam_score", "<=", 30],
            "or",
            ["2.backlinks_spam_score", "<=", 30],
        ]
