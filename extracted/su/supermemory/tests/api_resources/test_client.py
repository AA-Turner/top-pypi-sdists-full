# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from supermemory import Supermemory, AsyncSupermemory
from tests.utils import assert_matches_type
from supermemory.types import AddResponse, ProfileResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add(self, client: Supermemory) -> None:
        client_ = client.add(
            content="content",
        )
        assert_matches_type(AddResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add_with_all_params(self, client: Supermemory) -> None:
        client_ = client.add(
            content="content",
            container_tag="containerTag",
            container_tags=["string"],
            custom_id="customId",
            document_date="documentDate",
            dreaming="instant",
            entity_context="entityContext",
            filepath="filepath",
            filter_by_metadata={"foo": "string"},
            metadata={"foo": "string"},
            task_type="memory",
        )
        assert_matches_type(AddResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_add(self, client: Supermemory) -> None:
        response = client.with_raw_response.add(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(AddResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_add(self, client: Supermemory) -> None:
        with client.with_streaming_response.add(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(AddResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_profile(self, client: Supermemory) -> None:
        client_ = client.profile(
            container_tag="containerTag",
        )
        assert_matches_type(ProfileResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_profile_with_all_params(self, client: Supermemory) -> None:
        client_ = client.profile(
            container_tag="containerTag",
            buckets=["string"],
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
            include=["static"],
            q="q",
            threshold=0,
        )
        assert_matches_type(ProfileResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_profile(self, client: Supermemory) -> None:
        response = client.with_raw_response.profile(
            container_tag="containerTag",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ProfileResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_profile(self, client: Supermemory) -> None:
        with client.with_streaming_response.profile(
            container_tag="containerTag",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ProfileResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add(self, async_client: AsyncSupermemory) -> None:
        client = await async_client.add(
            content="content",
        )
        assert_matches_type(AddResponse, client, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncSupermemory) -> None:
        client = await async_client.add(
            content="content",
            container_tag="containerTag",
            container_tags=["string"],
            custom_id="customId",
            document_date="documentDate",
            dreaming="instant",
            entity_context="entityContext",
            filepath="filepath",
            filter_by_metadata={"foo": "string"},
            metadata={"foo": "string"},
            task_type="memory",
        )
        assert_matches_type(AddResponse, client, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.with_raw_response.add(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(AddResponse, client, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncSupermemory) -> None:
        async with async_client.with_streaming_response.add(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(AddResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_profile(self, async_client: AsyncSupermemory) -> None:
        client = await async_client.profile(
            container_tag="containerTag",
        )
        assert_matches_type(ProfileResponse, client, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_profile_with_all_params(self, async_client: AsyncSupermemory) -> None:
        client = await async_client.profile(
            container_tag="containerTag",
            buckets=["string"],
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
            include=["static"],
            q="q",
            threshold=0,
        )
        assert_matches_type(ProfileResponse, client, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_profile(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.with_raw_response.profile(
            container_tag="containerTag",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ProfileResponse, client, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_profile(self, async_client: AsyncSupermemory) -> None:
        async with async_client.with_streaming_response.profile(
            container_tag="containerTag",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ProfileResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True
