# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.knowledge_bases.artifacts import (
    ChunkPutResponse,
    ChunkListResponse,
    ChunkCreateResponse,
    ChunkDeleteResponse,
    ChunkRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChunks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
        )
        assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
            metadata={"foo": "bar"},
        )
        assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.chunks.with_raw_response.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.chunks.with_streaming_response.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.create(
                artifact_id="artifact_id",
                knowledge_base_id="",
                chunk_position=0,
                text="text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.create(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
                chunk_position=0,
                text="text",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.retrieve(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )
        assert_matches_type(ChunkRetrieveResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(ChunkRetrieveResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.chunks.with_streaming_response.retrieve(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(ChunkRetrieveResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
                chunk_id="chunk_id",
                knowledge_base_id="",
                artifact_id="artifact_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
                chunk_id="chunk_id",
                knowledge_base_id="knowledge_base_id",
                artifact_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `chunk_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
                chunk_id="",
                knowledge_base_id="knowledge_base_id",
                artifact_id="artifact_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(SyncPageResponse[ChunkListResponse], chunk, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_status="Pending",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[ChunkListResponse], chunk, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.chunks.with_raw_response.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(SyncPageResponse[ChunkListResponse], chunk, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.chunks.with_streaming_response.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(SyncPageResponse[ChunkListResponse], chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.list(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.list(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.delete(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )
        assert_matches_type(ChunkDeleteResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(ChunkDeleteResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.chunks.with_streaming_response.delete(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(ChunkDeleteResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
                chunk_id="chunk_id",
                knowledge_base_id="",
                artifact_id="artifact_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
                chunk_id="chunk_id",
                knowledge_base_id="knowledge_base_id",
                artifact_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `chunk_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
                chunk_id="",
                knowledge_base_id="knowledge_base_id",
                artifact_id="artifact_id",
            )

    @parametrize
    def test_method_put(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
        )
        assert_matches_type(ChunkPutResponse, chunk, path=["response"])

    @parametrize
    def test_method_put_with_all_params(self, client: SGPClient) -> None:
        chunk = client.knowledge_bases.artifacts.chunks.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
            metadata={"foo": "bar"},
        )
        assert_matches_type(ChunkPutResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_put(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.chunks.with_raw_response.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(ChunkPutResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_put(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.chunks.with_streaming_response.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(ChunkPutResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_put(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.put(
                chunk_id="chunk_id",
                knowledge_base_id="",
                artifact_id="artifact_id",
                chunk_position=0,
                text="text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.put(
                chunk_id="chunk_id",
                knowledge_base_id="knowledge_base_id",
                artifact_id="",
                chunk_position=0,
                text="text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `chunk_id` but received ''"):
            client.knowledge_bases.artifacts.chunks.with_raw_response.put(
                chunk_id="",
                knowledge_base_id="knowledge_base_id",
                artifact_id="artifact_id",
                chunk_position=0,
                text="text",
            )


class TestAsyncChunks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
        )
        assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
            metadata={"foo": "bar"},
        )
        assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.chunks.with_raw_response.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.chunks.with_streaming_response.create(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_position=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(ChunkCreateResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.create(
                artifact_id="artifact_id",
                knowledge_base_id="",
                chunk_position=0,
                text="text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.create(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
                chunk_position=0,
                text="text",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.retrieve(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )
        assert_matches_type(ChunkRetrieveResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(ChunkRetrieveResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.chunks.with_streaming_response.retrieve(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(ChunkRetrieveResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
                chunk_id="chunk_id",
                knowledge_base_id="",
                artifact_id="artifact_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
                chunk_id="chunk_id",
                knowledge_base_id="knowledge_base_id",
                artifact_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `chunk_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.retrieve(
                chunk_id="",
                knowledge_base_id="knowledge_base_id",
                artifact_id="artifact_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(AsyncPageResponse[ChunkListResponse], chunk, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            chunk_status="Pending",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[ChunkListResponse], chunk, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.chunks.with_raw_response.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(AsyncPageResponse[ChunkListResponse], chunk, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.chunks.with_streaming_response.list(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(AsyncPageResponse[ChunkListResponse], chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.list(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.list(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.delete(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )
        assert_matches_type(ChunkDeleteResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(ChunkDeleteResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.chunks.with_streaming_response.delete(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(ChunkDeleteResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
                chunk_id="chunk_id",
                knowledge_base_id="",
                artifact_id="artifact_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
                chunk_id="chunk_id",
                knowledge_base_id="knowledge_base_id",
                artifact_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `chunk_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.delete(
                chunk_id="",
                knowledge_base_id="knowledge_base_id",
                artifact_id="artifact_id",
            )

    @parametrize
    async def test_method_put(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
        )
        assert_matches_type(ChunkPutResponse, chunk, path=["response"])

    @parametrize
    async def test_method_put_with_all_params(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.knowledge_bases.artifacts.chunks.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
            metadata={"foo": "bar"},
        )
        assert_matches_type(ChunkPutResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_put(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.chunks.with_raw_response.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(ChunkPutResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_put(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.chunks.with_streaming_response.put(
            chunk_id="chunk_id",
            knowledge_base_id="knowledge_base_id",
            artifact_id="artifact_id",
            chunk_position=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(ChunkPutResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_put(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.put(
                chunk_id="chunk_id",
                knowledge_base_id="",
                artifact_id="artifact_id",
                chunk_position=0,
                text="text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.put(
                chunk_id="chunk_id",
                knowledge_base_id="knowledge_base_id",
                artifact_id="",
                chunk_position=0,
                text="text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `chunk_id` but received ''"):
            await async_client.knowledge_bases.artifacts.chunks.with_raw_response.put(
                chunk_id="",
                knowledge_base_id="knowledge_base_id",
                artifact_id="artifact_id",
                chunk_position=0,
                text="text",
            )
