# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import EmbeddingResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEmbeddings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        embedding = client.models.embeddings.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
        )
        assert_matches_type(EmbeddingResponse, embedding, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        embedding = client.models.embeddings.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
            model_request_parameters={"bindings": {"foo": "string"}},
        )
        assert_matches_type(EmbeddingResponse, embedding, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.models.embeddings.with_raw_response.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        embedding = response.parse()
        assert_matches_type(EmbeddingResponse, embedding, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.models.embeddings.with_streaming_response.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            embedding = response.parse()
            assert_matches_type(EmbeddingResponse, embedding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.embeddings.with_raw_response.create(
                model_deployment_id="",
                texts=["string"],
            )


class TestAsyncEmbeddings:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        embedding = await async_client.models.embeddings.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
        )
        assert_matches_type(EmbeddingResponse, embedding, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        embedding = await async_client.models.embeddings.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
            model_request_parameters={"bindings": {"foo": "string"}},
        )
        assert_matches_type(EmbeddingResponse, embedding, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.embeddings.with_raw_response.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        embedding = await response.parse()
        assert_matches_type(EmbeddingResponse, embedding, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.embeddings.with_streaming_response.create(
            model_deployment_id="model_deployment_id",
            texts=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            embedding = await response.parse()
            assert_matches_type(EmbeddingResponse, embedding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.embeddings.with_raw_response.create(
                model_deployment_id="",
                texts=["string"],
            )
