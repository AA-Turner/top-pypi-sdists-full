# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    VectorStore,
    VectorStoreDropResponse,
    VectorStoreCountResponse,
    VectorStoreQueryResponse,
    VectorStoreDeleteResponse,
    VectorStoreUpsertResponse,
)
from scale_gp_beta.pagination import SyncCursorPageByName, AsyncCursorPageByName

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVectorStores:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.create(
            name="name",
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.create(
            name="name",
            dimensions=1,
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            embedding_model="sentence-transformers/all-MiniLM-L12-v2",
            indexed_metadata_fields={"foo": "string"},
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStore, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.retrieve(
            "vector_store_name",
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.retrieve(
            "vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.retrieve(
            "vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStore, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.list()
        assert_matches_type(SyncCursorPageByName[VectorStore], vector_store, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.list(
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPageByName[VectorStore], vector_store, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(SyncCursorPageByName[VectorStore], vector_store, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(SyncCursorPageByName[VectorStore], vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.delete(
            vector_store_name="vector_store_name",
        )
        assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.delete(
            vector_store_name="vector_store_name",
            filter={"foo": "bar"},
            ids=["string"],
        )
        assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.delete(
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.delete(
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.delete(
                vector_store_name="",
            )

    @parametrize
    def test_method_configure(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.configure(
            vector_store_name="vector_store_name",
            indexed_metadata_fields={"foo": "string"},
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_raw_response_configure(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.configure(
            vector_store_name="vector_store_name",
            indexed_metadata_fields={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_configure(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.configure(
            vector_store_name="vector_store_name",
            indexed_metadata_fields={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStore, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_configure(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.configure(
                vector_store_name="",
                indexed_metadata_fields={"foo": "string"},
            )

    @parametrize
    def test_method_count(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.count(
            vector_store_name="vector_store_name",
        )
        assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

    @parametrize
    def test_method_count_with_all_params(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.count(
            vector_store_name="vector_store_name",
            filter={"foo": "bar"},
        )
        assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

    @parametrize
    def test_raw_response_count(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.count(
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_count(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.count(
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_count(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.count(
                vector_store_name="",
            )

    @parametrize
    def test_method_drop(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.drop(
            "vector_store_name",
        )
        assert_matches_type(VectorStoreDropResponse, vector_store, path=["response"])

    @parametrize
    def test_raw_response_drop(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.drop(
            "vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStoreDropResponse, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_drop(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.drop(
            "vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStoreDropResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_drop(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.drop(
                "",
            )

    @parametrize
    def test_method_query(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.query(
            vector_store_name="vector_store_name",
            content={"text": "text"},
        )
        assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.query(
            vector_store_name="vector_store_name",
            content={
                "text": "text",
                "type": "text",
            },
            filter={"foo": "bar"},
            include_vectors=True,
            query_type="semantic",
            rerank=True,
            rerank_config={
                "instruction": "instruction",
                "model": "model",
                "top_n": 1,
                "type": "base",
            },
            rerank_instruction="rerank_instruction",
            rerank_model="rerank_model",
            rerank_top_n=1,
            top_k=1,
        )
        assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.query(
            vector_store_name="vector_store_name",
            content={"text": "text"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.query(
            vector_store_name="vector_store_name",
            content={"text": "text"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.query(
                vector_store_name="",
                content={"text": "text"},
            )

    @parametrize
    def test_method_upsert(self, client: SGPClient) -> None:
        vector_store = client.vector_stores.upsert(
            vector_store_name="vector_store_name",
            vectors=[{"id": "id"}],
        )
        assert_matches_type(VectorStoreUpsertResponse, vector_store, path=["response"])

    @parametrize
    def test_raw_response_upsert(self, client: SGPClient) -> None:
        response = client.vector_stores.with_raw_response.upsert(
            vector_store_name="vector_store_name",
            vectors=[{"id": "id"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = response.parse()
        assert_matches_type(VectorStoreUpsertResponse, vector_store, path=["response"])

    @parametrize
    def test_streaming_response_upsert(self, client: SGPClient) -> None:
        with client.vector_stores.with_streaming_response.upsert(
            vector_store_name="vector_store_name",
            vectors=[{"id": "id"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = response.parse()
            assert_matches_type(VectorStoreUpsertResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_upsert(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            client.vector_stores.with_raw_response.upsert(
                vector_store_name="",
                vectors=[{"id": "id"}],
            )


class TestAsyncVectorStores:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.create(
            name="name",
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.create(
            name="name",
            dimensions=1,
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            embedding_model="sentence-transformers/all-MiniLM-L12-v2",
            indexed_metadata_fields={"foo": "string"},
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStore, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.retrieve(
            "vector_store_name",
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.retrieve(
            "vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.retrieve(
            "vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStore, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.list()
        assert_matches_type(AsyncCursorPageByName[VectorStore], vector_store, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.list(
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPageByName[VectorStore], vector_store, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(AsyncCursorPageByName[VectorStore], vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(AsyncCursorPageByName[VectorStore], vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.delete(
            vector_store_name="vector_store_name",
        )
        assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.delete(
            vector_store_name="vector_store_name",
            filter={"foo": "bar"},
            ids=["string"],
        )
        assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.delete(
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.delete(
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStoreDeleteResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.delete(
                vector_store_name="",
            )

    @parametrize
    async def test_method_configure(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.configure(
            vector_store_name="vector_store_name",
            indexed_metadata_fields={"foo": "string"},
        )
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_configure(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.configure(
            vector_store_name="vector_store_name",
            indexed_metadata_fields={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStore, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_configure(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.configure(
            vector_store_name="vector_store_name",
            indexed_metadata_fields={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStore, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_configure(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.configure(
                vector_store_name="",
                indexed_metadata_fields={"foo": "string"},
            )

    @parametrize
    async def test_method_count(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.count(
            vector_store_name="vector_store_name",
        )
        assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

    @parametrize
    async def test_method_count_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.count(
            vector_store_name="vector_store_name",
            filter={"foo": "bar"},
        )
        assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_count(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.count(
            vector_store_name="vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_count(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.count(
            vector_store_name="vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStoreCountResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_count(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.count(
                vector_store_name="",
            )

    @parametrize
    async def test_method_drop(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.drop(
            "vector_store_name",
        )
        assert_matches_type(VectorStoreDropResponse, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_drop(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.drop(
            "vector_store_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStoreDropResponse, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_drop(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.drop(
            "vector_store_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStoreDropResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_drop(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.drop(
                "",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.query(
            vector_store_name="vector_store_name",
            content={"text": "text"},
        )
        assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.query(
            vector_store_name="vector_store_name",
            content={
                "text": "text",
                "type": "text",
            },
            filter={"foo": "bar"},
            include_vectors=True,
            query_type="semantic",
            rerank=True,
            rerank_config={
                "instruction": "instruction",
                "model": "model",
                "top_n": 1,
                "type": "base",
            },
            rerank_instruction="rerank_instruction",
            rerank_model="rerank_model",
            rerank_top_n=1,
            top_k=1,
        )
        assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.query(
            vector_store_name="vector_store_name",
            content={"text": "text"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.query(
            vector_store_name="vector_store_name",
            content={"text": "text"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStoreQueryResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.query(
                vector_store_name="",
                content={"text": "text"},
            )

    @parametrize
    async def test_method_upsert(self, async_client: AsyncSGPClient) -> None:
        vector_store = await async_client.vector_stores.upsert(
            vector_store_name="vector_store_name",
            vectors=[{"id": "id"}],
        )
        assert_matches_type(VectorStoreUpsertResponse, vector_store, path=["response"])

    @parametrize
    async def test_raw_response_upsert(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.vector_stores.with_raw_response.upsert(
            vector_store_name="vector_store_name",
            vectors=[{"id": "id"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vector_store = await response.parse()
        assert_matches_type(VectorStoreUpsertResponse, vector_store, path=["response"])

    @parametrize
    async def test_streaming_response_upsert(self, async_client: AsyncSGPClient) -> None:
        async with async_client.vector_stores.with_streaming_response.upsert(
            vector_store_name="vector_store_name",
            vectors=[{"id": "id"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vector_store = await response.parse()
            assert_matches_type(VectorStoreUpsertResponse, vector_store, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_upsert(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vector_store_name` but received ''"):
            await async_client.vector_stores.with_raw_response.upsert(
                vector_store_name="",
                vectors=[{"id": "id"}],
            )
