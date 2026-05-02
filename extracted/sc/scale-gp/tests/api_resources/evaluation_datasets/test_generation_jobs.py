# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncGenerationJobsPagination, AsyncGenerationJobsPagination
from scale_gp.types.evaluation_datasets import (
    EvaluationDatasetGenerationJob,
    EvaluationDatasetGenerationJobResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGenerationJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.create(
            evaluation_dataset_id="evaluation_dataset_id",
            advanced_config={"foo": ["string"]},
            custom_instructions="custom_instructions",
            group_by_artifact_id=True,
            harms_list=["string"],
            num_test_cases=0,
        )
        assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.create(
                evaluation_dataset_id="",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.retrieve(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetGenerationJob, generation_job, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(EvaluationDatasetGenerationJob, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.retrieve(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(EvaluationDatasetGenerationJob, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                generation_job_id="generation_job_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                generation_job_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.list(
            "evaluation_dataset_id",
        )
        assert_matches_type(
            SyncGenerationJobsPagination[EvaluationDatasetGenerationJob], generation_job, path=["response"]
        )

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.list(
            "evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(
            SyncGenerationJobsPagination[EvaluationDatasetGenerationJob], generation_job, path=["response"]
        )

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.list(
            "evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(
                SyncGenerationJobsPagination[EvaluationDatasetGenerationJob], generation_job, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_cancel(self, client: SGPClient) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.cancel(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: SGPClient) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.cancel(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(object, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                generation_job_id="generation_job_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                generation_job_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )


class TestAsyncGenerationJobs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.create(
            evaluation_dataset_id="evaluation_dataset_id",
            advanced_config={"foo": ["string"]},
            custom_instructions="custom_instructions",
            group_by_artifact_id=True,
            harms_list=["string"],
            num_test_cases=0,
        )
        assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(EvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.create(
                evaluation_dataset_id="",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.retrieve(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetGenerationJob, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(EvaluationDatasetGenerationJob, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.retrieve(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(EvaluationDatasetGenerationJob, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                generation_job_id="generation_job_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                generation_job_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.list(
            "evaluation_dataset_id",
        )
        assert_matches_type(
            AsyncGenerationJobsPagination[EvaluationDatasetGenerationJob], generation_job, path=["response"]
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.list(
            "evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(
            AsyncGenerationJobsPagination[EvaluationDatasetGenerationJob], generation_job, path=["response"]
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.list(
            "evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(
                AsyncGenerationJobsPagination[EvaluationDatasetGenerationJob], generation_job, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncSGPClient) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.cancel(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.cancel(
            generation_job_id="generation_job_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(object, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                generation_job_id="generation_job_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                generation_job_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )
