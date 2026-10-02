import os

import pytest

from matrx_seo import (
    CollectionRequest,
    CollectionTrigger,
    InMemorySeoRepository,
    ResolvedCredential,
    ResolvedHostBinding,
    ResolvedSeoIdentity,
    SeoCapability,
    SeoCollectionService,
    fake_collection_authorizer,
)
from matrx_seo.providers.brave import BraveSeoRankAdapter


class LiveIdentityResolver:
    async def resolve(self, _request, _identity):
        return ResolvedSeoIdentity(
            keyword_id="live-keyword",
            location_id="live-location",
            rank_target_id="live-rank-target",
        )


class LiveHostResolver:
    async def resolve(self, _request, binding):
        return ResolvedHostBinding(
            site_id="live-site",
            page_id=("live-page" if binding.resource_kind == "web_page" else None),
            canonical_url=(
                "https://example.com/live-page"
                if binding.resource_kind == "web_page"
                else "https://example.com"
            ),
        )


@pytest.mark.live
@pytest.mark.asyncio
async def test_one_request_live_brave_rank_collection(request) -> None:
    if not request.config.getoption("--run-paid-brave"):
        pytest.skip("requires explicit --run-paid-brave approval")
    if request.config.getoption("--brave-request-cap") != 1:
        pytest.fail("live Brave test requires an explicit --brave-request-cap=1")
    # The ENV var is the platform's one Brave key; the vault key NAME below
    # stays `BRAVE_SEARCH_API_KEY` because that is a per-organization secret a
    # customer owns, not an env var, and renaming it would orphan stored keys.
    api_key = os.environ.get("BRAVE_SEARCH_API_KEY_PRO_AI", "").strip()
    if not api_key:
        pytest.fail(
            "BRAVE_SEARCH_API_KEY_PRO_AI must already be available for the approved live test"
        )

    async def credentials(_request, _provider):
        return ResolvedCredential(values={"BRAVE_SEARCH_API_KEY": api_key})

    repository = InMemorySeoRepository()
    receipt = await SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=LiveIdentityResolver(),
        host_binding_resolver=LiveHostResolver(),
        collection_authorizer=fake_collection_authorizer,
    ).collect(
        BraveSeoRankAdapter(max_attempts=2),
        CollectionRequest(
            organization_id="live-org",
            created_by="live-user",
            capability=SeoCapability.SERP_RANK,
            operation="brave.web.rank",
            target_ref="live-brave-rank",
            observation_period="manual-live-acceptance",
            trigger=CollectionTrigger.TEST,
            settings={
                "query": "site:example.com",
                "host_site_id": "live-web-site",
                "host_page_id": "live-web-page",
                "max_pages": 1,
            },
        ),
    )

    assert receipt.raw_payload_id
    assert len(repository.provider_calls) == 1
    assert next(iter(repository.runs.values()))["request_count"] == 1
