# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.evaluations import (
    TestCaseResult,
    TestCaseResultWithViews,
    TestCaseResultBatchResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTestCaseResults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
            account_id="account_id",
            annotated_by_identity_type="user",
            annotated_by_user_id="annotated_by_user_id",
            audit_comment="audit_comment",
            audit_required=True,
            audit_status="UNAUDITED",
            edited_by_identity_type="user",
            label_status="PENDING",
            result={"foo": "string"},
            time_spent_labeling_s=0,
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluations.test_case_results.with_raw_response.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluations.test_case_results.with_streaming_response.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResult, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.create(
                evaluation_id="",
                application_spec_id="application_spec_id",
                evaluation_dataset_version_num="evaluation_dataset_version_num",
                test_case_evaluation_data={"foo": "bar"},
                test_case_id="test_case_id",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
            view=["AnnotationResults"],
        )
        assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluations.test_case_results.with_raw_response.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluations.test_case_results.with_streaming_response.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.retrieve(
                test_case_result_id="test_case_result_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.retrieve(
                test_case_result_id="",
                evaluation_id="evaluation_id",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
            account_id="account_id",
            annotated_by_identity_type="user",
            annotated_by_user_id="annotated_by_user_id",
            application_spec_id="application_spec_id",
            audit_comment="audit_comment",
            audit_required=True,
            audit_status="UNAUDITED",
            edited_by_identity_type="user",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            label_status="PENDING",
            result={"foo": "string"},
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
            time_spent_labeling_s=0,
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluations.test_case_results.with_raw_response.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluations.test_case_results.with_streaming_response.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResult, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.update(
                test_case_result_id="test_case_result_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.update(
                test_case_result_id="",
                evaluation_id="evaluation_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.list(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(SyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.list(
            evaluation_id="evaluation_id",
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
            view=["AnnotationResults"],
        )
        assert_matches_type(SyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluations.test_case_results.with_raw_response.list(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(SyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluations.test_case_results.with_streaming_response.list(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(SyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.list(
                evaluation_id="",
            )

    @parametrize
    def test_method_batch(self, client: SGPClient) -> None:
        test_case_result = client.evaluations.test_case_results.batch(
            evaluation_id="evaluation_id",
            items=[
                {
                    "application_spec_id": "application_spec_id",
                    "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                    "test_case_evaluation_data": {"foo": "bar"},
                    "test_case_id": "test_case_id",
                }
            ],
        )
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: SGPClient) -> None:
        response = client.evaluations.test_case_results.with_raw_response.batch(
            evaluation_id="evaluation_id",
            items=[
                {
                    "application_spec_id": "application_spec_id",
                    "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                    "test_case_evaluation_data": {"foo": "bar"},
                    "test_case_id": "test_case_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: SGPClient) -> None:
        with client.evaluations.test_case_results.with_streaming_response.batch(
            evaluation_id="evaluation_id",
            items=[
                {
                    "application_spec_id": "application_spec_id",
                    "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                    "test_case_evaluation_data": {"foo": "bar"},
                    "test_case_id": "test_case_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_batch(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.batch(
                evaluation_id="",
                items=[
                    {
                        "application_spec_id": "application_spec_id",
                        "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                        "test_case_evaluation_data": {"foo": "bar"},
                        "test_case_id": "test_case_id",
                    }
                ],
            )


class TestAsyncTestCaseResults:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
            account_id="account_id",
            annotated_by_identity_type="user",
            annotated_by_user_id="annotated_by_user_id",
            audit_comment="audit_comment",
            audit_required=True,
            audit_status="UNAUDITED",
            edited_by_identity_type="user",
            label_status="PENDING",
            result={"foo": "string"},
            time_spent_labeling_s=0,
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.create(
            evaluation_id="evaluation_id",
            application_spec_id="application_spec_id",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResult, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.create(
                evaluation_id="",
                application_spec_id="application_spec_id",
                evaluation_dataset_version_num="evaluation_dataset_version_num",
                test_case_evaluation_data={"foo": "bar"},
                test_case_id="test_case_id",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
            view=["AnnotationResults"],
        )
        assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.retrieve(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultWithViews, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.retrieve(
                test_case_result_id="test_case_result_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.retrieve(
                test_case_result_id="",
                evaluation_id="evaluation_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
            account_id="account_id",
            annotated_by_identity_type="user",
            annotated_by_user_id="annotated_by_user_id",
            application_spec_id="application_spec_id",
            audit_comment="audit_comment",
            audit_required=True,
            audit_status="UNAUDITED",
            edited_by_identity_type="user",
            evaluation_dataset_version_num="evaluation_dataset_version_num",
            label_status="PENDING",
            result={"foo": "string"},
            test_case_evaluation_data={"foo": "bar"},
            test_case_id="test_case_id",
            time_spent_labeling_s=0,
        )
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResult, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.update(
            test_case_result_id="test_case_result_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResult, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.update(
                test_case_result_id="test_case_result_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.update(
                test_case_result_id="",
                evaluation_id="evaluation_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.list(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(AsyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.list(
            evaluation_id="evaluation_id",
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
            view=["AnnotationResults"],
        )
        assert_matches_type(AsyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.list(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(AsyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.list(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(AsyncPageResponse[TestCaseResultWithViews], test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.list(
                evaluation_id="",
            )

    @parametrize
    async def test_method_batch(self, async_client: AsyncSGPClient) -> None:
        test_case_result = await async_client.evaluations.test_case_results.batch(
            evaluation_id="evaluation_id",
            items=[
                {
                    "application_spec_id": "application_spec_id",
                    "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                    "test_case_evaluation_data": {"foo": "bar"},
                    "test_case_id": "test_case_id",
                }
            ],
        )
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.batch(
            evaluation_id="evaluation_id",
            items=[
                {
                    "application_spec_id": "application_spec_id",
                    "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                    "test_case_evaluation_data": {"foo": "bar"},
                    "test_case_id": "test_case_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.batch(
            evaluation_id="evaluation_id",
            items=[
                {
                    "application_spec_id": "application_spec_id",
                    "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                    "test_case_evaluation_data": {"foo": "bar"},
                    "test_case_id": "test_case_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_batch(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.batch(
                evaluation_id="",
                items=[
                    {
                        "application_spec_id": "application_spec_id",
                        "evaluation_dataset_version_num": "evaluation_dataset_version_num",
                        "test_case_evaluation_data": {"foo": "bar"},
                        "test_case_id": "test_case_id",
                    }
                ],
            )
