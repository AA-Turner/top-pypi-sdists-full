# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import FineTuningJob
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFineTuningJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        fine_tuning_job = client.fine_tuning_jobs.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
        )
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        fine_tuning_job = client.fine_tuning_jobs.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
            base_model_id="base_model_id",
            fine_tuned_model_id="fine_tuned_model_id",
            validation_dataset_id="validation_dataset_id",
            vendor_configuration={
                "hyperparameters": {"foo": "bar"},
                "output": "output",
                "suffix": "suffix",
                "vendor": "LAUNCH",
                "wandb_config": {"foo": "bar"},
            },
        )
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.fine_tuning_jobs.with_raw_response.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.fine_tuning_jobs.with_streaming_response.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        fine_tuning_job = client.fine_tuning_jobs.retrieve(
            "fine_tuning_job_id",
        )
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.fine_tuning_jobs.with_raw_response.retrieve(
            "fine_tuning_job_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.fine_tuning_jobs.with_streaming_response.retrieve(
            "fine_tuning_job_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            client.fine_tuning_jobs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        fine_tuning_job = client.fine_tuning_jobs.list()
        assert_matches_type(SyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        fine_tuning_job = client.fine_tuning_jobs.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.fine_tuning_jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(SyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.fine_tuning_jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(SyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        fine_tuning_job = client.fine_tuning_jobs.delete(
            "fine_tuning_job_id",
        )
        assert_matches_type(GenericDeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.fine_tuning_jobs.with_raw_response.delete(
            "fine_tuning_job_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(GenericDeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.fine_tuning_jobs.with_streaming_response.delete(
            "fine_tuning_job_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(GenericDeleteResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            client.fine_tuning_jobs.with_raw_response.delete(
                "",
            )


class TestAsyncFineTuningJobs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
        )
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
            base_model_id="base_model_id",
            fine_tuned_model_id="fine_tuned_model_id",
            validation_dataset_id="validation_dataset_id",
            vendor_configuration={
                "hyperparameters": {"foo": "bar"},
                "output": "output",
                "suffix": "suffix",
                "vendor": "LAUNCH",
                "wandb_config": {"foo": "bar"},
            },
        )
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.create(
            account_id="account_id",
            training_dataset_id="training_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.retrieve(
            "fine_tuning_job_id",
        )
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.retrieve(
            "fine_tuning_job_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.retrieve(
            "fine_tuning_job_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(FineTuningJob, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            await async_client.fine_tuning_jobs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.list()
        assert_matches_type(AsyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(AsyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(AsyncPageResponse[FineTuningJob], fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.delete(
            "fine_tuning_job_id",
        )
        assert_matches_type(GenericDeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.delete(
            "fine_tuning_job_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(GenericDeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.delete(
            "fine_tuning_job_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(GenericDeleteResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            await async_client.fine_tuning_jobs.with_raw_response.delete(
                "",
            )
