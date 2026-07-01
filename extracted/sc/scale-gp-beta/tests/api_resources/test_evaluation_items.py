# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    EvaluationItem,
    EvaluationItemExport,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationItems:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation_item = client.evaluation_items.retrieve(
            evaluation_item_id="evaluation_item_id",
        )
        assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        evaluation_item = client.evaluation_items.retrieve(
            evaluation_item_id="evaluation_item_id",
            include_archived=True,
        )
        assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_items.with_raw_response.retrieve(
            evaluation_item_id="evaluation_item_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_item = response.parse()
        assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_items.with_streaming_response.retrieve(
            evaluation_item_id="evaluation_item_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_item = response.parse()
            assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_item_id` but received ''"):
            client.evaluation_items.with_raw_response.retrieve(
                evaluation_item_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation_item = client.evaluation_items.list()
        assert_matches_type(SyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation_item = client.evaluation_items.list(
            completion_status="failed",
            ending_before="ending_before",
            evaluation_id="evaluation_id",
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_items.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_item = response.parse()
        assert_matches_type(SyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_items.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_item = response.parse()
            assert_matches_type(SyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_export(self, client: SGPClient) -> None:
        evaluation_item = client.evaluation_items.export(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

    @parametrize
    def test_method_export_with_all_params(self, client: SGPClient) -> None:
        evaluation_item = client.evaluation_items.export(
            evaluation_id="evaluation_id",
            export_format="json",
            export_method="signed_url",
            include_archived=True,
        )
        assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

    @parametrize
    def test_raw_response_export(self, client: SGPClient) -> None:
        response = client.evaluation_items.with_raw_response.export(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_item = response.parse()
        assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

    @parametrize
    def test_streaming_response_export(self, client: SGPClient) -> None:
        with client.evaluation_items.with_streaming_response.export(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_item = response.parse()
            assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvaluationItems:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation_item = await async_client.evaluation_items.retrieve(
            evaluation_item_id="evaluation_item_id",
        )
        assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_item = await async_client.evaluation_items.retrieve(
            evaluation_item_id="evaluation_item_id",
            include_archived=True,
        )
        assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_items.with_raw_response.retrieve(
            evaluation_item_id="evaluation_item_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_item = await response.parse()
        assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_items.with_streaming_response.retrieve(
            evaluation_item_id="evaluation_item_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_item = await response.parse()
            assert_matches_type(EvaluationItem, evaluation_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_item_id` but received ''"):
            await async_client.evaluation_items.with_raw_response.retrieve(
                evaluation_item_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation_item = await async_client.evaluation_items.list()
        assert_matches_type(AsyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_item = await async_client.evaluation_items.list(
            completion_status="failed",
            ending_before="ending_before",
            evaluation_id="evaluation_id",
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_items.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_item = await response.parse()
        assert_matches_type(AsyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_items.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_item = await response.parse()
            assert_matches_type(AsyncCursorPage[EvaluationItem], evaluation_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_export(self, async_client: AsyncSGPClient) -> None:
        evaluation_item = await async_client.evaluation_items.export(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

    @parametrize
    async def test_method_export_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_item = await async_client.evaluation_items.export(
            evaluation_id="evaluation_id",
            export_format="json",
            export_method="signed_url",
            include_archived=True,
        )
        assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

    @parametrize
    async def test_raw_response_export(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_items.with_raw_response.export(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_item = await response.parse()
        assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

    @parametrize
    async def test_streaming_response_export(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_items.with_streaming_response.export(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_item = await response.parse()
            assert_matches_type(EvaluationItemExport, evaluation_item, path=["response"])

        assert cast(Any, response.is_closed) is True
