# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncTopLevelArray, AsyncTopLevelArray
from scale_gp.types.knowledge_bases import AsyncJobListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAsyncJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        async_job = client.knowledge_bases.async_jobs.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(SyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        async_job = client.knowledge_bases.async_jobs.list(
            knowledge_base_id="knowledge_base_id",
            limit=1,
            page=1,
            status="Active",
        )
        assert_matches_type(SyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_bases.async_jobs.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_job = response.parse()
        assert_matches_type(SyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_bases.async_jobs.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_job = response.parse()
            assert_matches_type(SyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.async_jobs.with_raw_response.list(
                knowledge_base_id="",
            )


class TestAsyncAsyncJobs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        async_job = await async_client.knowledge_bases.async_jobs.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(AsyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        async_job = await async_client.knowledge_bases.async_jobs.list(
            knowledge_base_id="knowledge_base_id",
            limit=1,
            page=1,
            status="Active",
        )
        assert_matches_type(AsyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.async_jobs.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_job = await response.parse()
        assert_matches_type(AsyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.async_jobs.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_job = await response.parse()
            assert_matches_type(AsyncTopLevelArray[AsyncJobListResponse], async_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.async_jobs.with_raw_response.list(
                knowledge_base_id="",
            )
