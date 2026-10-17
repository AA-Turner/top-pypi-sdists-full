# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types import Issue
from langsmith.pagination import SyncOffsetPaginationIssues, AsyncOffsetPaginationIssues

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIssues:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Langsmith) -> None:
        issue = client.issues.retrieve(
            id="id",
        )
        assert_matches_type(Issue, issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Langsmith) -> None:
        issue = client.issues.retrieve(
            id="id",
            include_linear_context=True,
        )
        assert_matches_type(Issue, issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Langsmith) -> None:

        response = client.issues.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issue = response.parse()
        assert_matches_type(Issue, issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Langsmith) -> None:
        with client.issues.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issue = response.parse()
            assert_matches_type(Issue, issue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.issues.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Langsmith) -> None:
        issue = client.issues.list()
        assert_matches_type(SyncOffsetPaginationIssues[Issue], issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Langsmith) -> None:
        issue = client.issues.list(
            activity=["fixing"],
            limit=0,
            offset=0,
            session_id="session_id",
            session_name="session_name",
            severity=0,
            severity_exact=[0],
            sort_by="default",
            status="open",
            status_first=True,
            tag="tag",
            trace_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            updated_at="updated_at",
        )
        assert_matches_type(SyncOffsetPaginationIssues[Issue], issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Langsmith) -> None:

        response = client.issues.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issue = response.parse()
        assert_matches_type(SyncOffsetPaginationIssues[Issue], issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Langsmith) -> None:
        with client.issues.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issue = response.parse()
            assert_matches_type(SyncOffsetPaginationIssues[Issue], issue, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncIssues:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLangsmith) -> None:
        issue = await async_client.issues.retrieve(
            id="id",
        )
        assert_matches_type(Issue, issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncLangsmith) -> None:
        issue = await async_client.issues.retrieve(
            id="id",
            include_linear_context=True,
        )
        assert_matches_type(Issue, issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.issues.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issue = await response.parse()
        assert_matches_type(Issue, issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLangsmith) -> None:
        async with async_client.issues.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issue = await response.parse()
            assert_matches_type(Issue, issue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.issues.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLangsmith) -> None:
        issue = await async_client.issues.list()
        assert_matches_type(AsyncOffsetPaginationIssues[Issue], issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLangsmith) -> None:
        issue = await async_client.issues.list(
            activity=["fixing"],
            limit=0,
            offset=0,
            session_id="session_id",
            session_name="session_name",
            severity=0,
            severity_exact=[0],
            sort_by="default",
            status="open",
            status_first=True,
            tag="tag",
            trace_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            updated_at="updated_at",
        )
        assert_matches_type(AsyncOffsetPaginationIssues[Issue], issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.issues.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        issue = await response.parse()
        assert_matches_type(AsyncOffsetPaginationIssues[Issue], issue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLangsmith) -> None:
        async with async_client.issues.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            issue = await response.parse()
            assert_matches_type(AsyncOffsetPaginationIssues[Issue], issue, path=["response"])

        assert cast(Any, response.is_closed) is True
