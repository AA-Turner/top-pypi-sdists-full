# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ApplicationTestCaseOutputBatchResponse,
    ApplicationTestCaseOutputRetrieveResponse,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.paginated_application_test_case_output_with_views import Item

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationTestCaseOutputs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        application_test_case_output = client.application_test_case_outputs.retrieve(
            application_test_case_output_id="application_test_case_output_id",
        )
        assert_matches_type(ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        application_test_case_output = client.application_test_case_outputs.retrieve(
            application_test_case_output_id="application_test_case_output_id",
            view=["MetricScores"],
        )
        assert_matches_type(ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.application_test_case_outputs.with_raw_response.retrieve(
            application_test_case_output_id="application_test_case_output_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = response.parse()
        assert_matches_type(ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.application_test_case_outputs.with_streaming_response.retrieve(
            application_test_case_output_id="application_test_case_output_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = response.parse()
            assert_matches_type(
                ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_test_case_output_id` but received ''"
        ):
            client.application_test_case_outputs.with_raw_response.retrieve(
                application_test_case_output_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        application_test_case_output = client.application_test_case_outputs.list()
        assert_matches_type(SyncPageResponse[Item], application_test_case_output, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        application_test_case_output = client.application_test_case_outputs.list(
            account_id="account_id",
            application_test_case_output_group_id=0,
            application_variant_id=0,
            application_variant_report_id=0,
            evaluation_dataset_id=0,
            evaluation_dataset_version_num=0,
            limit=1,
            page=1,
            view=["MetricScores"],
        )
        assert_matches_type(SyncPageResponse[Item], application_test_case_output, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.application_test_case_outputs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = response.parse()
        assert_matches_type(SyncPageResponse[Item], application_test_case_output, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.application_test_case_outputs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = response.parse()
            assert_matches_type(SyncPageResponse[Item], application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_batch(self, client: SGPClient) -> None:
        application_test_case_output = client.application_test_case_outputs.batch(
            items=[
                {
                    "account_id": "account_id",
                    "application_variant_id": "application_variant_id",
                    "evaluation_dataset_version_num": 0,
                    "output": {"generation_output": "generation_output"},
                    "test_case_id": "test_case_id",
                }
            ],
        )
        assert_matches_type(ApplicationTestCaseOutputBatchResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: SGPClient) -> None:
        response = client.application_test_case_outputs.with_raw_response.batch(
            items=[
                {
                    "account_id": "account_id",
                    "application_variant_id": "application_variant_id",
                    "evaluation_dataset_version_num": 0,
                    "output": {"generation_output": "generation_output"},
                    "test_case_id": "test_case_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = response.parse()
        assert_matches_type(ApplicationTestCaseOutputBatchResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: SGPClient) -> None:
        with client.application_test_case_outputs.with_streaming_response.batch(
            items=[
                {
                    "account_id": "account_id",
                    "application_variant_id": "application_variant_id",
                    "evaluation_dataset_version_num": 0,
                    "output": {"generation_output": "generation_output"},
                    "test_case_id": "test_case_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = response.parse()
            assert_matches_type(ApplicationTestCaseOutputBatchResponse, application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationTestCaseOutputs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.retrieve(
            application_test_case_output_id="application_test_case_output_id",
        )
        assert_matches_type(ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.retrieve(
            application_test_case_output_id="application_test_case_output_id",
            view=["MetricScores"],
        )
        assert_matches_type(ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_test_case_outputs.with_raw_response.retrieve(
            application_test_case_output_id="application_test_case_output_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = await response.parse()
        assert_matches_type(ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_test_case_outputs.with_streaming_response.retrieve(
            application_test_case_output_id="application_test_case_output_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = await response.parse()
            assert_matches_type(
                ApplicationTestCaseOutputRetrieveResponse, application_test_case_output, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_test_case_output_id` but received ''"
        ):
            await async_client.application_test_case_outputs.with_raw_response.retrieve(
                application_test_case_output_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.list()
        assert_matches_type(AsyncPageResponse[Item], application_test_case_output, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.list(
            account_id="account_id",
            application_test_case_output_group_id=0,
            application_variant_id=0,
            application_variant_report_id=0,
            evaluation_dataset_id=0,
            evaluation_dataset_version_num=0,
            limit=1,
            page=1,
            view=["MetricScores"],
        )
        assert_matches_type(AsyncPageResponse[Item], application_test_case_output, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_test_case_outputs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = await response.parse()
        assert_matches_type(AsyncPageResponse[Item], application_test_case_output, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_test_case_outputs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = await response.parse()
            assert_matches_type(AsyncPageResponse[Item], application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_batch(self, async_client: AsyncSGPClient) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.batch(
            items=[
                {
                    "account_id": "account_id",
                    "application_variant_id": "application_variant_id",
                    "evaluation_dataset_version_num": 0,
                    "output": {"generation_output": "generation_output"},
                    "test_case_id": "test_case_id",
                }
            ],
        )
        assert_matches_type(ApplicationTestCaseOutputBatchResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_test_case_outputs.with_raw_response.batch(
            items=[
                {
                    "account_id": "account_id",
                    "application_variant_id": "application_variant_id",
                    "evaluation_dataset_version_num": 0,
                    "output": {"generation_output": "generation_output"},
                    "test_case_id": "test_case_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = await response.parse()
        assert_matches_type(ApplicationTestCaseOutputBatchResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_test_case_outputs.with_streaming_response.batch(
            items=[
                {
                    "account_id": "account_id",
                    "application_variant_id": "application_variant_id",
                    "evaluation_dataset_version_num": 0,
                    "output": {"generation_output": "generation_output"},
                    "test_case_id": "test_case_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = await response.parse()
            assert_matches_type(ApplicationTestCaseOutputBatchResponse, application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True
