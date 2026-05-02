# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types.otel import LogSearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLogs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_search(self, client: PatronusAPI) -> None:
        log = client.otel.logs.search()
        assert_matches_type(LogSearchResponse, log, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: PatronusAPI) -> None:
        log = client.otel.logs.search(
            filters=[
                {
                    "and_": [{}],
                    "field": "field",
                    "op": "eq",
                    "or_": [{}],
                    "value": {},
                }
            ],
            limit=1,
            order="timestamp asc",
        )
        assert_matches_type(LogSearchResponse, log, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: PatronusAPI) -> None:
        response = client.otel.logs.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        log = response.parse()
        assert_matches_type(LogSearchResponse, log, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: PatronusAPI) -> None:
        with client.otel.logs.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            log = response.parse()
            assert_matches_type(LogSearchResponse, log, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLogs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_search(self, async_client: AsyncPatronusAPI) -> None:
        log = await async_client.otel.logs.search()
        assert_matches_type(LogSearchResponse, log, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        log = await async_client.otel.logs.search(
            filters=[
                {
                    "and_": [{}],
                    "field": "field",
                    "op": "eq",
                    "or_": [{}],
                    "value": {},
                }
            ],
            limit=1,
            order="timestamp asc",
        )
        assert_matches_type(LogSearchResponse, log, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.otel.logs.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        log = await response.parse()
        assert_matches_type(LogSearchResponse, log, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.otel.logs.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            log = await response.parse()
            assert_matches_type(LogSearchResponse, log, path=["response"])

        assert cast(Any, response.is_closed) is True
