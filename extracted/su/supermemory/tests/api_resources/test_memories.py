# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from supermemory import Supermemory, AsyncSupermemory
from tests.utils import assert_matches_type
from supermemory.types import (
    MemoryForgetResponse,
    MemoryUpdateMemoryResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_forget(self, client: Supermemory) -> None:
        memory = client.memories.forget(
            container_tag="user_123",
        )
        assert_matches_type(MemoryForgetResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_forget_with_all_params(self, client: Supermemory) -> None:
        memory = client.memories.forget(
            container_tag="user_123",
            id="mem_abc123",
            content="John prefers dark mode",
            reason="outdated information",
        )
        assert_matches_type(MemoryForgetResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_forget(self, client: Supermemory) -> None:
        response = client.memories.with_raw_response.forget(
            container_tag="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryForgetResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_forget(self, client: Supermemory) -> None:
        with client.memories.with_streaming_response.forget(
            container_tag="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryForgetResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_memory(self, client: Supermemory) -> None:
        memory = client.memories.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
        )
        assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_memory_with_all_params(self, client: Supermemory) -> None:
        memory = client.memories.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
            id="mem_abc123",
            content="John prefers dark mode",
            forget_after="2026-06-01T00:00:00Z",
            forget_reason="temporary project deadline",
            metadata={"foo": "string"},
            temporal_context={
                "document_date": "documentDate",
                "event_date": ["string"],
            },
        )
        assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update_memory(self, client: Supermemory) -> None:
        response = client.memories.with_raw_response.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update_memory(self, client: Supermemory) -> None:
        with client.memories.with_streaming_response.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMemories:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_forget(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memories.forget(
            container_tag="user_123",
        )
        assert_matches_type(MemoryForgetResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_forget_with_all_params(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memories.forget(
            container_tag="user_123",
            id="mem_abc123",
            content="John prefers dark mode",
            reason="outdated information",
        )
        assert_matches_type(MemoryForgetResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_forget(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.memories.with_raw_response.forget(
            container_tag="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryForgetResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_forget(self, async_client: AsyncSupermemory) -> None:
        async with async_client.memories.with_streaming_response.forget(
            container_tag="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryForgetResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_memory(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memories.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
        )
        assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_memory_with_all_params(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memories.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
            id="mem_abc123",
            content="John prefers dark mode",
            forget_after="2026-06-01T00:00:00Z",
            forget_reason="temporary project deadline",
            metadata={"foo": "string"},
            temporal_context={
                "document_date": "documentDate",
                "event_date": ["string"],
            },
        )
        assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update_memory(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.memories.with_raw_response.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update_memory(self, async_client: AsyncSupermemory) -> None:
        async with async_client.memories.with_streaming_response.update_memory(
            container_tag="user_123",
            new_content="John now prefers light mode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryUpdateMemoryResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True
