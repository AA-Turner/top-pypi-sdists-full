from __future__ import annotations

import os

import pytest

from matrx_seo.providers.dataforseo.client import DataForSeoClient
from matrx_seo.providers.dataforseo.contracts import (
    DataForSeoOperationName,
    DataForSeoOperationRequest,
)
from matrx_seo.providers.dataforseo.transport import AsyncHttpTransport


@pytest.mark.live
@pytest.mark.asyncio
async def test_budget_capped_dataforseo_live_keyword_volume(request) -> None:
    if not request.config.getoption("--run-paid-dataforseo"):
        pytest.skip("requires explicit --run-paid-dataforseo approval")
    budget = request.config.getoption("--dataforseo-budget-usd")
    if budget <= 0 or budget > 0.10:
        pytest.fail("live DataForSEO test requires 0 < --dataforseo-budget-usd <= 0.10")
    email = os.environ.get("DATA_FOR_SEO_EMAIL", "").strip()
    password = os.environ.get("DATA_FOR_SEO_PASSWORD", "").strip()
    if not email or not password:
        pytest.fail("canonical DataForSEO credentials must already be configured")
    transport = AsyncHttpTransport(username=email, password=password, max_attempts=2)
    client = DataForSeoClient(transport)
    try:
        account = await client.account_snapshot()
        assert account["status_code"] == 20000
        response = await client.execute(
            DataForSeoOperationRequest(
                operation=DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME,
                tasks=[
                    {
                        "keywords": ["synthetic matrx seo acceptance"],
                        "location_code": 2840,
                        "language_code": "en",
                        "tag": "matrx-seo-live-acceptance",
                    }
                ],
            )
        )
        assert response.error is None
        assert response.reported_cost is not None
        assert response.reported_cost <= budget
    finally:
        await transport.aclose()
