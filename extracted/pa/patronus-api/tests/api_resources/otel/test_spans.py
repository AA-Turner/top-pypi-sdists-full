# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types.otel import SpanSearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpans:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_delete(self, client: PatronusAPI) -> None:
        span = client.otel.spans.delete()
        assert span is None

    @parametrize
    def test_method_delete_with_all_params(self, client: PatronusAPI) -> None:
        span = client.otel.spans.delete(
            app="app",
            experiment_id=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            trace_id="trace_id",
        )
        assert span is None

    @parametrize
    def test_raw_response_delete(self, client: PatronusAPI) -> None:
        response = client.otel.spans.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert span is None

    @parametrize
    def test_streaming_response_delete(self, client: PatronusAPI) -> None:
        with client.otel.spans.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert span is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search(self, client: PatronusAPI) -> None:
        span = client.otel.spans.search()
        assert_matches_type(SpanSearchResponse, span, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: PatronusAPI) -> None:
        span = client.otel.spans.search(
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
        assert_matches_type(SpanSearchResponse, span, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: PatronusAPI) -> None:
        response = client.otel.spans.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(SpanSearchResponse, span, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: PatronusAPI) -> None:
        with client.otel.spans.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(SpanSearchResponse, span, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSpans:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_delete(self, async_client: AsyncPatronusAPI) -> None:
        span = await async_client.otel.spans.delete()
        assert span is None

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        span = await async_client.otel.spans.delete(
            app="app",
            experiment_id=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            trace_id="trace_id",
        )
        assert span is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.otel.spans.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert span is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.otel.spans.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert span is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search(self, async_client: AsyncPatronusAPI) -> None:
        span = await async_client.otel.spans.search()
        assert_matches_type(SpanSearchResponse, span, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        span = await async_client.otel.spans.search(
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
        assert_matches_type(SpanSearchResponse, span, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.otel.spans.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(SpanSearchResponse, span, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.otel.spans.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(SpanSearchResponse, span, path=["response"])

        assert cast(Any, response.is_closed) is True
