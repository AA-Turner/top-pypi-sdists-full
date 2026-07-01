# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.pagination import SyncCursorPageVectors, AsyncCursorPageVectors
from scale_gp_beta.types.vector_stores import VectorDocument

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVectors:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        vector = client.vector_stores.vectors.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
        )
        assert_matches_type(VectorDocument, vector, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        vector = client.vector_stores.vectors.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
            include_vectors=True,
        )
        assert_matches_type(VectorDocument, vector, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.vector_stores.vectors.with_raw_response.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector = response.parse()
        assert_matches_type(VectorDocument, vector, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.vector_stores.vectors.with_streaming_response.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector = response.parse()
            assert_matches_type(VectorDocument, vector, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.vectors.with_raw_response.retrieve(
                vector_id="vector_id",
                vector_store_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_id` but received ''"):
            client.vector_stores.vectors.with_raw_response.retrieve(
                vector_id="",
                vector_store_name="vector_store_name",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        vector = client.vector_stores.vectors.list(
            vector_store_name="vector_store_name",
        )
        assert_matches_type(SyncCursorPageVectors[VectorDocument], vector, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        vector = client.vector_stores.vectors.list(
            vector_store_name="vector_store_name",
            cursor="cursor",
            ending_before="ending_before",
            filter="filter",
            include_vectors=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPageVectors[VectorDocument], vector, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.vector_stores.vectors.with_raw_response.list(
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector = response.parse()
        assert_matches_type(SyncCursorPageVectors[VectorDocument], vector, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.vector_stores.vectors.with_streaming_response.list(
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector = response.parse()
            assert_matches_type(SyncCursorPageVectors[VectorDocument], vector, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.vectors.with_raw_response.list(
                vector_store_name="",
            )


class TestAsyncVectors:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        vector = await async_client.vector_stores.vectors.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
        )
        assert_matches_type(VectorDocument, vector, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector = await async_client.vector_stores.vectors.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
            include_vectors=True,
        )
        assert_matches_type(VectorDocument, vector, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.vectors.with_raw_response.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector = await response.parse()
        assert_matches_type(VectorDocument, vector, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.vectors.with_streaming_response.retrieve(
            vector_id="vector_id",
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector = await response.parse()
            assert_matches_type(VectorDocument, vector, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.vectors.with_raw_response.retrieve(
                vector_id="vector_id",
                vector_store_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_id` but received ''"):
            await async_client.vector_stores.vectors.with_raw_response.retrieve(
                vector_id="",
                vector_store_name="vector_store_name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        vector = await async_client.vector_stores.vectors.list(
            vector_store_name="vector_store_name",
        )
        assert_matches_type(AsyncCursorPageVectors[VectorDocument], vector, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector = await async_client.vector_stores.vectors.list(
            vector_store_name="vector_store_name",
            cursor="cursor",
            ending_before="ending_before",
            filter="filter",
            include_vectors=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPageVectors[VectorDocument], vector, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.vectors.with_raw_response.list(
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector = await response.parse()
        assert_matches_type(AsyncCursorPageVectors[VectorDocument], vector, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.vectors.with_streaming_response.list(
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector = await response.parse()
            assert_matches_type(AsyncCursorPageVectors[VectorDocument], vector, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.vectors.with_raw_response.list(
                vector_store_name="",
            )
