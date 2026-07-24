# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from supermemory import Supermemory, AsyncSupermemory
from tests.utils import assert_matches_type
from supermemory.types import (
    SearchExecuteResponse,
    SearchMemoriesResponse,
    SearchDocumentsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_documents(self, client: Supermemory) -> None:
        search = client.search.documents(
            q="what are the API rate limits",
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_documents_with_all_params(self, client: Supermemory) -> None:
        search = client.search.documents(
            q="what are the API rate limits",
            categories_filter=["string"],
            chunk_threshold=0.5,
            container_tag="user_alex",
            container_tags=["_:_k--W2K_1V"],
            doc_id="docId",
            document_threshold=0,
            filepath="filepath",
            filters={
                "or_": [
                    {
                        "key": "key",
                        "value": "value",
                        "filter_type": "metadata",
                        "ignore_case": "true",
                        "negate": "true",
                        "numeric_operator": ">",
                    }
                ]
            },
            include_full_docs=False,
            include_summary=True,
            limit=10,
            only_matching_chunks=True,
            rerank=False,
            rewrite_query=False,
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_documents(self, client: Supermemory) -> None:
        response = client.search.with_raw_response.documents(
            q="what are the API rate limits",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_documents(self, client: Supermemory) -> None:
        with client.search.with_streaming_response.documents(
            q="what are the API rate limits",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchDocumentsResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_execute(self, client: Supermemory) -> None:
        search = client.search.execute(
            q="what are the API rate limits",
        )
        assert_matches_type(SearchExecuteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_execute_with_all_params(self, client: Supermemory) -> None:
        search = client.search.execute(
            q="what are the API rate limits",
            categories_filter=["string"],
            chunk_threshold=0.5,
            container_tag="user_alex",
            container_tags=["_:_k--W2K_1V"],
            doc_id="docId",
            document_threshold=0,
            filepath="filepath",
            filters={
                "or_": [
                    {
                        "key": "key",
                        "value": "value",
                        "filter_type": "metadata",
                        "ignore_case": "true",
                        "negate": "true",
                        "numeric_operator": ">",
                    }
                ]
            },
            include_full_docs=False,
            include_summary=True,
            limit=10,
            only_matching_chunks=True,
            rerank=False,
            rewrite_query=False,
        )
        assert_matches_type(SearchExecuteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_execute(self, client: Supermemory) -> None:
        response = client.search.with_raw_response.execute(
            q="what are the API rate limits",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchExecuteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_execute(self, client: Supermemory) -> None:
        with client.search.with_streaming_response.execute(
            q="what are the API rate limits",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchExecuteResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_memories(self, client: Supermemory) -> None:
        search = client.search.memories(
            q="what are the API rate limits",
        )
        assert_matches_type(SearchMemoriesResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_memories_with_all_params(self, client: Supermemory) -> None:
        search = client.search.memories(
            q="what are the API rate limits",
            aggregate=False,
            container_tag="user_alex",
            container_tags=["user_alex"],
            filepath="filepath",
            filters={
                "or_": [
                    {
                        "key": "key",
                        "value": "value",
                        "filter_type": "metadata",
                        "ignore_case": "true",
                        "negate": "true",
                        "numeric_operator": ">",
                    }
                ]
            },
            include={
                "chunks": False,
                "documents": True,
                "forgotten_memories": False,
                "related_memories": True,
                "summaries": True,
            },
            limit=10,
            rerank=False,
            rewrite_query=False,
            search_mode="memories",
            threshold=0.5,
        )
        assert_matches_type(SearchMemoriesResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_memories(self, client: Supermemory) -> None:
        response = client.search.with_raw_response.memories(
            q="what are the API rate limits",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchMemoriesResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_memories(self, client: Supermemory) -> None:
        with client.search.with_streaming_response.memories(
            q="what are the API rate limits",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchMemoriesResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_documents(self, async_client: AsyncSupermemory) -> None:
        search = await async_client.search.documents(
            q="what are the API rate limits",
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_documents_with_all_params(self, async_client: AsyncSupermemory) -> None:
        search = await async_client.search.documents(
            q="what are the API rate limits",
            categories_filter=["string"],
            chunk_threshold=0.5,
            container_tag="user_alex",
            container_tags=["_:_k--W2K_1V"],
            doc_id="docId",
            document_threshold=0,
            filepath="filepath",
            filters={
                "or_": [
                    {
                        "key": "key",
                        "value": "value",
                        "filter_type": "metadata",
                        "ignore_case": "true",
                        "negate": "true",
                        "numeric_operator": ">",
                    }
                ]
            },
            include_full_docs=False,
            include_summary=True,
            limit=10,
            only_matching_chunks=True,
            rerank=False,
            rewrite_query=False,
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_documents(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.search.with_raw_response.documents(
            q="what are the API rate limits",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_documents(self, async_client: AsyncSupermemory) -> None:
        async with async_client.search.with_streaming_response.documents(
            q="what are the API rate limits",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchDocumentsResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_execute(self, async_client: AsyncSupermemory) -> None:
        search = await async_client.search.execute(
            q="what are the API rate limits",
        )
        assert_matches_type(SearchExecuteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncSupermemory) -> None:
        search = await async_client.search.execute(
            q="what are the API rate limits",
            categories_filter=["string"],
            chunk_threshold=0.5,
            container_tag="user_alex",
            container_tags=["_:_k--W2K_1V"],
            doc_id="docId",
            document_threshold=0,
            filepath="filepath",
            filters={
                "or_": [
                    {
                        "key": "key",
                        "value": "value",
                        "filter_type": "metadata",
                        "ignore_case": "true",
                        "negate": "true",
                        "numeric_operator": ">",
                    }
                ]
            },
            include_full_docs=False,
            include_summary=True,
            limit=10,
            only_matching_chunks=True,
            rerank=False,
            rewrite_query=False,
        )
        assert_matches_type(SearchExecuteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.search.with_raw_response.execute(
            q="what are the API rate limits",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchExecuteResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSupermemory) -> None:
        async with async_client.search.with_streaming_response.execute(
            q="what are the API rate limits",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchExecuteResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_memories(self, async_client: AsyncSupermemory) -> None:
        search = await async_client.search.memories(
            q="what are the API rate limits",
        )
        assert_matches_type(SearchMemoriesResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_memories_with_all_params(self, async_client: AsyncSupermemory) -> None:
        search = await async_client.search.memories(
            q="what are the API rate limits",
            aggregate=False,
            container_tag="user_alex",
            container_tags=["user_alex"],
            filepath="filepath",
            filters={
                "or_": [
                    {
                        "key": "key",
                        "value": "value",
                        "filter_type": "metadata",
                        "ignore_case": "true",
                        "negate": "true",
                        "numeric_operator": ">",
                    }
                ]
            },
            include={
                "chunks": False,
                "documents": True,
                "forgotten_memories": False,
                "related_memories": True,
                "summaries": True,
            },
            limit=10,
            rerank=False,
            rewrite_query=False,
            search_mode="memories",
            threshold=0.5,
        )
        assert_matches_type(SearchMemoriesResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_memories(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.search.with_raw_response.memories(
            q="what are the API rate limits",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchMemoriesResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_memories(self, async_client: AsyncSupermemory) -> None:
        async with async_client.search.with_streaming_response.memories(
            q="what are the API rate limits",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchMemoriesResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
