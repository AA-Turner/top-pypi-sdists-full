import os

import pytest

from matrx_seo import (
    InMemorySeoRepository,
    ResolvedCredential,
    ResolvedHostBinding,
    ResolvedSeoIdentity,
)
from matrx_seo.providers.serpapi import (
    SerpApiGoogleRankAdapter,
    SerpApiGoogleRankSettings,
    SerpApiRankJob,
)
from matrx_seo.service import SeoCollectionService


class LiveIdentityResolver:
    async def resolve(self, _request, _identity):
        return ResolvedSeoIdentity(
            keyword_id="live-keyword",
            location_id="live-location",
            rank_target_id="live-rank-target",
        )


class LiveHostResolver:
    async def resolve(self, _request, binding):
        if binding.resource_kind == "web_site":
            return ResolvedHostBinding(
                site_id="live-site",
                canonical_url="https://example.com",
            )
        return ResolvedHostBinding(
            site_id="live-site",
            page_id="live-page",
            canonical_url="https://example.com/austin-seo",
        )


async def authorize(collection_request):
    return collection_request


@pytest.mark.live
@pytest.mark.asyncio
async def test_one_credit_live_google_rank_collection(request) -> None:
    if not request.config.getoption("--run-paid-serpapi"):
        pytest.skip("requires explicit --run-paid-serpapi approval")
    if request.config.getoption("--serpapi-credit-cap") != 1:
        pytest.fail("live SerpAPI test requires an explicit --serpapi-credit-cap=1")
    api_key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if not api_key:
        pytest.fail("SERPAPI_API_KEY must already be available to run the approved live test")

    async def credentials(_request, _provider):
        return ResolvedCredential(values={"SERPAPI_API_KEY": api_key})

    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=LiveIdentityResolver(),
        host_binding_resolver=LiveHostResolver(),
        collection_authorizer=authorize,
    )
    live_settings = SerpApiGoogleRankSettings(
        keyword="site:example.com",
        host_site_id="live-web-site",
        location="Austin,Texas,United States",
        country_code="US",
        region="Texas",
        city="Austin",
        gl="us",
        hl="en",
        device="desktop",
        safe="active",
        start=0,
    )
    job = SerpApiRankJob(
        organization_id="live-org",
        created_by="live-user",
        target_ref="live-rank-target:start-0",
        observation_period="manual-live-acceptance",
        settings=live_settings,
    )

    receipt = await service.collect(
        SerpApiGoogleRankAdapter(max_attempts=2),
        job.to_collection_request(),
    )

    assert receipt.raw_payload_id
    assert len(repository.provider_calls) == 1
    assert next(iter(repository.runs.values()))["request_count"] == 1
