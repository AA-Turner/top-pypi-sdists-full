# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ApplicationVariantWithScores,
    ApplicationVariantWithScoresAndViews,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationVariantReports:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        application_variant_report = client.application_variant_reports.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
        )
        assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        application_variant_report = client.application_variant_reports.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
            account_id="account_id",
            application_test_case_output_group_ids=["string"],
        )
        assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.application_variant_reports.with_raw_response.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant_report = response.parse()
        assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.application_variant_reports.with_streaming_response.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant_report = response.parse()
            assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        application_variant_report = client.application_variant_reports.retrieve(
            application_variant_report_id="application_variant_report_id",
        )
        assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        application_variant_report = client.application_variant_reports.retrieve(
            application_variant_report_id="application_variant_report_id",
            view=["AsyncJobs"],
        )
        assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.application_variant_reports.with_raw_response.retrieve(
            application_variant_report_id="application_variant_report_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant_report = response.parse()
        assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.application_variant_reports.with_streaming_response.retrieve(
            application_variant_report_id="application_variant_report_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant_report = response.parse()
            assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_report_id` but received ''"
        ):
            client.application_variant_reports.with_raw_response.retrieve(
                application_variant_report_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        application_variant_report = client.application_variant_reports.list()
        assert_matches_type(
            SyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
        )

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        application_variant_report = client.application_variant_reports.list(
            account_id="account_id",
            application_spec_id=0,
            application_variant_id=0,
            limit=1,
            page=1,
            view=["AsyncJobs"],
        )
        assert_matches_type(
            SyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
        )

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.application_variant_reports.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant_report = response.parse()
        assert_matches_type(
            SyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
        )

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.application_variant_reports.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant_report = response.parse()
            assert_matches_type(
                SyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
            )

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationVariantReports:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        application_variant_report = await async_client.application_variant_reports.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
        )
        assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_variant_report = await async_client.application_variant_reports.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
            account_id="account_id",
            application_test_case_output_group_ids=["string"],
        )
        assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variant_reports.with_raw_response.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant_report = await response.parse()
        assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variant_reports.with_streaming_response.create(
            application_variant_id="application_variant_id",
            evaluation_dataset_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant_report = await response.parse()
            assert_matches_type(ApplicationVariantWithScores, application_variant_report, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        application_variant_report = await async_client.application_variant_reports.retrieve(
            application_variant_report_id="application_variant_report_id",
        )
        assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_variant_report = await async_client.application_variant_reports.retrieve(
            application_variant_report_id="application_variant_report_id",
            view=["AsyncJobs"],
        )
        assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variant_reports.with_raw_response.retrieve(
            application_variant_report_id="application_variant_report_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant_report = await response.parse()
        assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variant_reports.with_streaming_response.retrieve(
            application_variant_report_id="application_variant_report_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant_report = await response.parse()
            assert_matches_type(ApplicationVariantWithScoresAndViews, application_variant_report, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_report_id` but received ''"
        ):
            await async_client.application_variant_reports.with_raw_response.retrieve(
                application_variant_report_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        application_variant_report = await async_client.application_variant_reports.list()
        assert_matches_type(
            AsyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
        )

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_variant_report = await async_client.application_variant_reports.list(
            account_id="account_id",
            application_spec_id=0,
            application_variant_id=0,
            limit=1,
            page=1,
            view=["AsyncJobs"],
        )
        assert_matches_type(
            AsyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variant_reports.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant_report = await response.parse()
        assert_matches_type(
            AsyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variant_reports.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant_report = await response.parse()
            assert_matches_type(
                AsyncPageResponse[ApplicationVariantWithScoresAndViews], application_variant_report, path=["response"]
            )

        assert cast(Any, response.is_closed) is True
