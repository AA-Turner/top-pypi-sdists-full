# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import InferenceCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInference:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        inference = client.inference.create(
            model="model",
        )
        assert_matches_type(InferenceCreateResponse, inference, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        inference = client.inference.create(
            model="model",
            args={"foo": "bar"},
            inference_configuration={
                "num_retries": 0,
                "timeout_seconds": 0,
            },
        )
        assert_matches_type(InferenceCreateResponse, inference, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.inference.with_raw_response.create(
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = response.parse()
        assert_matches_type(InferenceCreateResponse, inference, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.inference.with_streaming_response.create(
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = response.parse()
            assert_matches_type(InferenceCreateResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInference:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        inference = await async_client.inference.create(
            model="model",
        )
        assert_matches_type(InferenceCreateResponse, inference, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        inference = await async_client.inference.create(
            model="model",
            args={"foo": "bar"},
            inference_configuration={
                "num_retries": 0,
                "timeout_seconds": 0,
            },
        )
        assert_matches_type(InferenceCreateResponse, inference, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.inference.with_raw_response.create(
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = await response.parse()
        assert_matches_type(InferenceCreateResponse, inference, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.inference.with_streaming_response.create(
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = await response.parse()
            assert_matches_type(InferenceCreateResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True
