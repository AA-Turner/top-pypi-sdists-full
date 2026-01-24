# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import EvaluatorListResponse, EvaluatorListFamiliesResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluators:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: PatronusAPI) -> None:
        evaluator = client.evaluators.list()
        assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: PatronusAPI) -> None:
        evaluator = client.evaluators.list(
            by_alias_or_id="by_alias_or_id",
        )
        assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: PatronusAPI) -> None:
        response = client.evaluators.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator = response.parse()
        assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: PatronusAPI) -> None:
        with client.evaluators.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator = response.parse()
            assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_families(self, client: PatronusAPI) -> None:
        evaluator = client.evaluators.list_families()
        assert_matches_type(EvaluatorListFamiliesResponse, evaluator, path=["response"])

    @parametrize
    def test_raw_response_list_families(self, client: PatronusAPI) -> None:
        response = client.evaluators.with_raw_response.list_families()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator = response.parse()
        assert_matches_type(EvaluatorListFamiliesResponse, evaluator, path=["response"])

    @parametrize
    def test_streaming_response_list_families(self, client: PatronusAPI) -> None:
        with client.evaluators.with_streaming_response.list_families() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator = response.parse()
            assert_matches_type(EvaluatorListFamiliesResponse, evaluator, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvaluators:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncPatronusAPI) -> None:
        evaluator = await async_client.evaluators.list()
        assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluator = await async_client.evaluators.list(
            by_alias_or_id="by_alias_or_id",
        )
        assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluators.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator = await response.parse()
        assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluators.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator = await response.parse()
            assert_matches_type(EvaluatorListResponse, evaluator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_families(self, async_client: AsyncPatronusAPI) -> None:
        evaluator = await async_client.evaluators.list_families()
        assert_matches_type(EvaluatorListFamiliesResponse, evaluator, path=["response"])

    @parametrize
    async def test_raw_response_list_families(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluators.with_raw_response.list_families()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator = await response.parse()
        assert_matches_type(EvaluatorListFamiliesResponse, evaluator, path=["response"])

    @parametrize
    async def test_streaming_response_list_families(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluators.with_streaming_response.list_families() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator = await response.parse()
            assert_matches_type(EvaluatorListFamiliesResponse, evaluator, path=["response"])

        assert cast(Any, response.is_closed) is True
