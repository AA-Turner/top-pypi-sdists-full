import os

import pytest

from matrx_seo import (
    InMemorySeoRepository,
    ResolvedCredential,
    ResolvedHostBinding,
    SeoCollectionService,
    fake_collection_authorizer,
)
from matrx_seo.providers.pagespeed import (
    PageSpeedInsightsAdapter,
    PageSpeedInsightsSettings,
    PageSpeedSampleJob,
)


class LiveHostResolver:
    async def resolve(self, _request, binding):
        return ResolvedHostBinding(
            site_id="live-site",
            page_id="live-page",
            canonical_url="https://example.com/",
        )


@pytest.mark.live
@pytest.mark.asyncio
async def test_one_request_live_pagespeed_collection(request) -> None:
    if not request.config.getoption("--run-live-pagespeed"):
        pytest.skip("requires explicit --run-live-pagespeed approval")
    if request.config.getoption("--pagespeed-request-cap") != 1:
        pytest.fail("live PageSpeed test requires --pagespeed-request-cap=1")
    api_key = os.environ.get("GOOGLE_PSI_API_KEY", "").strip()
    if not api_key:
        pytest.fail("GOOGLE_PSI_API_KEY must already be available for the live test")

    from matrx_scraper.performance import PsiClient

    async def credentials(_request, _provider):
        return ResolvedCredential(values={"GOOGLE_PSI_API_KEY": api_key})

    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        host_binding_resolver=LiveHostResolver(),
        collection_authorizer=fake_collection_authorizer,
    )
    job = PageSpeedSampleJob(
        organization_id="live-org",
        created_by="live-user",
        site_id="live-site",
        target_ref="live-page-binding:mobile",
        observation_period="manual-live-acceptance",
        settings=PageSpeedInsightsSettings(
            host_page_id="live-web-page",
            url="https://example.com/",
            strategy="mobile",
        ),
    )
    receipt = await service.collect(
        PageSpeedInsightsAdapter(
            client_factory=lambda key: PsiClient(api_key=key),
            max_attempts=1,
        ),
        job.to_collection_request(),
    )

    assert receipt.raw_payload_id
    assert len(repository.provider_calls) == 1
    assert next(iter(repository.runs.values()))["request_count"] == 1
