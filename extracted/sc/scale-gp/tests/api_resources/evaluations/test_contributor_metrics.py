# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.evaluations import ContributorMetrics

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestContributorMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        contributor_metric = client.evaluations.contributor_metrics.retrieve(
            contributor_id="contributor_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Optional[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluations.contributor_metrics.with_raw_response.retrieve(
            contributor_id="contributor_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = response.parse()
        assert_matches_type(Optional[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluations.contributor_metrics.with_streaming_response.retrieve(
            contributor_id="contributor_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = response.parse()
            assert_matches_type(Optional[ContributorMetrics], contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.contributor_metrics.with_raw_response.retrieve(
                contributor_id="contributor_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `contributor_id` but received ''"):
            client.evaluations.contributor_metrics.with_raw_response.retrieve(
                contributor_id="",
                evaluation_id="evaluation_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        contributor_metric = client.evaluations.contributor_metrics.list(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(SyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        contributor_metric = client.evaluations.contributor_metrics.list(
            evaluation_id="evaluation_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluations.contributor_metrics.with_raw_response.list(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = response.parse()
        assert_matches_type(SyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluations.contributor_metrics.with_streaming_response.list(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = response.parse()
            assert_matches_type(SyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.contributor_metrics.with_raw_response.list(
                evaluation_id="",
            )


class TestAsyncContributorMetrics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.retrieve(
            contributor_id="contributor_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Optional[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.contributor_metrics.with_raw_response.retrieve(
            contributor_id="contributor_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = await response.parse()
        assert_matches_type(Optional[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.contributor_metrics.with_streaming_response.retrieve(
            contributor_id="contributor_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = await response.parse()
            assert_matches_type(Optional[ContributorMetrics], contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.contributor_metrics.with_raw_response.retrieve(
                contributor_id="contributor_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `contributor_id` but received ''"):
            await async_client.evaluations.contributor_metrics.with_raw_response.retrieve(
                contributor_id="",
                evaluation_id="evaluation_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.list(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(AsyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.list(
            evaluation_id="evaluation_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.contributor_metrics.with_raw_response.list(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = await response.parse()
        assert_matches_type(AsyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.contributor_metrics.with_streaming_response.list(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = await response.parse()
            assert_matches_type(AsyncPageResponse[ContributorMetrics], contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.contributor_metrics.with_raw_response.list(
                evaluation_id="",
            )
