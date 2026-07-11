# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types.evaluation_dashboards import (
    EvaluationDashboardWidgetWithResult,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWidgets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        widget = client.evaluation_dashboards.widgets.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        widget = client.evaluation_dashboards.widgets.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
            config={"foo": "bar"},
            query={
                "select": [
                    {
                        "expression": {
                            "column": "column",
                            "source": "source",
                            "type": "COLUMN",
                        },
                        "alias": "alias",
                    }
                ],
                "evaluation_ids": ["string"],
                "filter": {
                    "conditions": [
                        {
                            "column": "column",
                            "operator": "=",
                            "source": "source",
                            "value": "string",
                        }
                    ],
                    "logical_operators": ["AND"],
                },
                "group_by": ["string"],
                "latest_only": True,
                "limit": 1,
                "order_by": [
                    {
                        "column": "column",
                        "direction": "ASC",
                        "source": "source",
                    }
                ],
            },
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.widgets.with_raw_response.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        widget = response.parse()
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.widgets.with_streaming_response.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            widget = response.parse()
            assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.evaluation_dashboards.widgets.with_raw_response.create(
                dashboard_id="",
                title="x",
                type="bar",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        widget = client.evaluation_dashboards.widgets.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        widget = client.evaluation_dashboards.widgets.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
            config={"foo": "bar"},
            query={
                "select": [
                    {
                        "expression": {
                            "column": "column",
                            "source": "source",
                            "type": "COLUMN",
                        },
                        "alias": "alias",
                    }
                ],
                "evaluation_ids": ["string"],
                "filter": {
                    "conditions": [
                        {
                            "column": "column",
                            "operator": "=",
                            "source": "source",
                            "value": "string",
                        }
                    ],
                    "logical_operators": ["AND"],
                },
                "group_by": ["string"],
                "latest_only": True,
                "limit": 1,
                "order_by": [
                    {
                        "column": "column",
                        "direction": "ASC",
                        "source": "source",
                    }
                ],
            },
            title="x",
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.widgets.with_raw_response.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        widget = response.parse()
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.widgets.with_streaming_response.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            widget = response.parse()
            assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.evaluation_dashboards.widgets.with_raw_response.update(
                widget_id="widget_id",
                dashboard_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `widget_id` but received ''"):
            client.evaluation_dashboards.widgets.with_raw_response.update(
                widget_id="",
                dashboard_id="dashboard_id",
            )

    @parametrize
    def test_method_remove(self, client: SGPClient) -> None:
        widget = client.evaluation_dashboards.widgets.remove(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )
        assert widget is None

    @parametrize
    def test_raw_response_remove(self, client: SGPClient) -> None:
        response = client.evaluation_dashboards.widgets.with_raw_response.remove(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        widget = response.parse()
        assert widget is None

    @parametrize
    def test_streaming_response_remove(self, client: SGPClient) -> None:
        with client.evaluation_dashboards.widgets.with_streaming_response.remove(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            widget = response.parse()
            assert widget is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.evaluation_dashboards.widgets.with_raw_response.remove(
                widget_id="widget_id",
                dashboard_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `widget_id` but received ''"):
            client.evaluation_dashboards.widgets.with_raw_response.remove(
                widget_id="",
                dashboard_id="dashboard_id",
            )


class TestAsyncWidgets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        widget = await async_client.evaluation_dashboards.widgets.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        widget = await async_client.evaluation_dashboards.widgets.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
            config={"foo": "bar"},
            query={
                "select": [
                    {
                        "expression": {
                            "column": "column",
                            "source": "source",
                            "type": "COLUMN",
                        },
                        "alias": "alias",
                    }
                ],
                "evaluation_ids": ["string"],
                "filter": {
                    "conditions": [
                        {
                            "column": "column",
                            "operator": "=",
                            "source": "source",
                            "value": "string",
                        }
                    ],
                    "logical_operators": ["AND"],
                },
                "group_by": ["string"],
                "latest_only": True,
                "limit": 1,
                "order_by": [
                    {
                        "column": "column",
                        "direction": "ASC",
                        "source": "source",
                    }
                ],
            },
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.widgets.with_raw_response.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        widget = await response.parse()
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.widgets.with_streaming_response.create(
            dashboard_id="dashboard_id",
            title="x",
            type="bar",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            widget = await response.parse()
            assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.evaluation_dashboards.widgets.with_raw_response.create(
                dashboard_id="",
                title="x",
                type="bar",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        widget = await async_client.evaluation_dashboards.widgets.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        widget = await async_client.evaluation_dashboards.widgets.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
            config={"foo": "bar"},
            query={
                "select": [
                    {
                        "expression": {
                            "column": "column",
                            "source": "source",
                            "type": "COLUMN",
                        },
                        "alias": "alias",
                    }
                ],
                "evaluation_ids": ["string"],
                "filter": {
                    "conditions": [
                        {
                            "column": "column",
                            "operator": "=",
                            "source": "source",
                            "value": "string",
                        }
                    ],
                    "logical_operators": ["AND"],
                },
                "group_by": ["string"],
                "latest_only": True,
                "limit": 1,
                "order_by": [
                    {
                        "column": "column",
                        "direction": "ASC",
                        "source": "source",
                    }
                ],
            },
            title="x",
        )
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.widgets.with_raw_response.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        widget = await response.parse()
        assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.widgets.with_streaming_response.update(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            widget = await response.parse()
            assert_matches_type(EvaluationDashboardWidgetWithResult, widget, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.evaluation_dashboards.widgets.with_raw_response.update(
                widget_id="widget_id",
                dashboard_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `widget_id` but received ''"):
            await async_client.evaluation_dashboards.widgets.with_raw_response.update(
                widget_id="",
                dashboard_id="dashboard_id",
            )

    @parametrize
    async def test_method_remove(self, async_client: AsyncSGPClient) -> None:
        widget = await async_client.evaluation_dashboards.widgets.remove(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )
        assert widget is None

    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_dashboards.widgets.with_raw_response.remove(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        widget = await response.parse()
        assert widget is None

    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_dashboards.widgets.with_streaming_response.remove(
            widget_id="widget_id",
            dashboard_id="dashboard_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            widget = await response.parse()
            assert widget is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.evaluation_dashboards.widgets.with_raw_response.remove(
                widget_id="widget_id",
                dashboard_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `widget_id` but received ''"):
            await async_client.evaluation_dashboards.widgets.with_raw_response.remove(
                widget_id="",
                dashboard_id="dashboard_id",
            )
