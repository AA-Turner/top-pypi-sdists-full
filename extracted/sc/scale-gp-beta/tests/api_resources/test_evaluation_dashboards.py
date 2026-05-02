# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    EvaluationDashboard,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationDashboards:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.create(
            name="x",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.create(
            name="x",
            description="description",
            evaluation_group_id="evaluation_group_id",
            evaluation_id="evaluation_id",
            tags=["string"],
            template_dashboard_id="template_dashboard_id",
            widget_order=["string"],
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.retrieve(
            dashboard_id="dashboard_id",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.retrieve(
            dashboard_id="dashboard_id",
            include_archived=True,
            views=["widgets"],
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.with_raw_response.retrieve(
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.with_streaming_response.retrieve(
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.evaluation_dashboards.with_raw_response.retrieve(
                dashboard_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.update(
            dashboard_id="dashboard_id",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.update(
            dashboard_id="dashboard_id",
            description="description",
            name="x",
            tags=["string"],
            widget_order=["string"],
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.with_raw_response.update(
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.with_streaming_response.update(
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.evaluation_dashboards.with_raw_response.update(
                dashboard_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.list()
        assert_matches_type(SyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.list(
            created_by_ids=["string"],
            ending_before="ending_before",
            evaluation_group_id="evaluation_group_id",
            evaluation_id="evaluation_id",
            include_archived=True,
            limit=1,
            search="search",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
        )
        assert_matches_type(SyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = response.parse()
        assert_matches_type(SyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = response.parse()
            assert_matches_type(SyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        evaluation_dashboard = client.evaluation_dashboards.archive(
            "dashboard_id",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.with_raw_response.archive(
            "dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.with_streaming_response.archive(
            "dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.evaluation_dashboards.with_raw_response.archive(
                "",
            )


class TestAsyncEvaluationDashboards:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.create(
            name="x",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.create(
            name="x",
            description="description",
            evaluation_group_id="evaluation_group_id",
            evaluation_id="evaluation_id",
            tags=["string"],
            template_dashboard_id="template_dashboard_id",
            widget_order=["string"],
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = await response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = await response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.retrieve(
            dashboard_id="dashboard_id",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.retrieve(
            dashboard_id="dashboard_id",
            include_archived=True,
            views=["widgets"],
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.with_raw_response.retrieve(
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = await response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.with_streaming_response.retrieve(
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = await response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.evaluation_dashboards.with_raw_response.retrieve(
                dashboard_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.update(
            dashboard_id="dashboard_id",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.update(
            dashboard_id="dashboard_id",
            description="description",
            name="x",
            tags=["string"],
            widget_order=["string"],
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.with_raw_response.update(
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = await response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.with_streaming_response.update(
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = await response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.evaluation_dashboards.with_raw_response.update(
                dashboard_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.list()
        assert_matches_type(AsyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.list(
            created_by_ids=["string"],
            ending_before="ending_before",
            evaluation_group_id="evaluation_group_id",
            evaluation_id="evaluation_id",
            include_archived=True,
            limit=1,
            search="search",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
        )
        assert_matches_type(AsyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = await response.parse()
        assert_matches_type(AsyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = await response.parse()
            assert_matches_type(AsyncCursorPage[EvaluationDashboard], evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        evaluation_dashboard = await async_client.evaluation_dashboards.archive(
            "dashboard_id",
        )
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.with_raw_response.archive(
            "dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dashboard = await response.parse()
        assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.with_streaming_response.archive(
            "dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dashboard = await response.parse()
            assert_matches_type(EvaluationDashboard, evaluation_dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.evaluation_dashboards.with_raw_response.archive(
                "",
            )
