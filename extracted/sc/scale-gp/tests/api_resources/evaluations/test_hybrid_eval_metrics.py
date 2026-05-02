# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import HybridEvaluationMetrics

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHybridEvalMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        hybrid_eval_metric = client.evaluations.hybrid_eval_metrics.retrieve(
            "evaluation_id",
        )
        assert_matches_type(HybridEvaluationMetrics, hybrid_eval_metric, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluations.hybrid_eval_metrics.with_raw_response.retrieve(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hybrid_eval_metric = response.parse()
        assert_matches_type(HybridEvaluationMetrics, hybrid_eval_metric, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluations.hybrid_eval_metrics.with_streaming_response.retrieve(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hybrid_eval_metric = response.parse()
            assert_matches_type(HybridEvaluationMetrics, hybrid_eval_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.hybrid_eval_metrics.with_raw_response.retrieve(
                "",
            )


class TestAsyncHybridEvalMetrics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        hybrid_eval_metric = await async_client.evaluations.hybrid_eval_metrics.retrieve(
            "evaluation_id",
        )
        assert_matches_type(HybridEvaluationMetrics, hybrid_eval_metric, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.hybrid_eval_metrics.with_raw_response.retrieve(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hybrid_eval_metric = await response.parse()
        assert_matches_type(HybridEvaluationMetrics, hybrid_eval_metric, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.hybrid_eval_metrics.with_streaming_response.retrieve(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hybrid_eval_metric = await response.parse()
            assert_matches_type(HybridEvaluationMetrics, hybrid_eval_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.hybrid_eval_metrics.with_raw_response.retrieve(
                "",
            )
