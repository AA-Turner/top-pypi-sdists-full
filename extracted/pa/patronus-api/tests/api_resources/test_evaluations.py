# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    EvaluationSearchResponse,
    EvaluationEvaluateResponse,
    EvaluationRetrieveResponse,
    EvaluationBatchCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.retrieve(
            0,
        )
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: PatronusAPI) -> None:
        response = client.evaluations.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: PatronusAPI) -> None:
        with client.evaluations.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.delete(
            0,
        )
        assert evaluation is None

    @parametrize
    def test_raw_response_delete(self, client: PatronusAPI) -> None:
        response = client.evaluations.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert evaluation is None

    @parametrize
    def test_streaming_response_delete(self, client: PatronusAPI) -> None:
        with client.evaluations.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert evaluation is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_batch_create(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.batch_create(
            evaluations=[
                {
                    "evaluator_id": "evaluator_id",
                    "log_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )
        assert_matches_type(EvaluationBatchCreateResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_batch_create(self, client: PatronusAPI) -> None:
        response = client.evaluations.with_raw_response.batch_create(
            evaluations=[
                {
                    "evaluator_id": "evaluator_id",
                    "log_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationBatchCreateResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_batch_create(self, client: PatronusAPI) -> None:
        with client.evaluations.with_streaming_response.batch_create(
            evaluations=[
                {
                    "evaluator_id": "evaluator_id",
                    "log_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationBatchCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_batch_delete(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.batch_delete()
        assert_matches_type(object, evaluation, path=["response"])

    @parametrize
    def test_method_batch_delete_with_all_params(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.batch_delete(
            app="app",
            batch_size=0,
            evaluator_criteria_id="evaluator_criteria_id",
            evaluator_family="evaluator_family",
            experiment_id=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            trace_id="trace_id",
        )
        assert_matches_type(object, evaluation, path=["response"])

    @parametrize
    def test_raw_response_batch_delete(self, client: PatronusAPI) -> None:
        response = client.evaluations.with_raw_response.batch_delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(object, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_batch_delete(self, client: PatronusAPI) -> None:
        with client.evaluations.with_streaming_response.batch_delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(object, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_evaluate(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.evaluate(
            evaluators=[{"evaluator": "evaluator"}],
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    def test_method_evaluate_with_all_params(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.evaluate(
            evaluators=[
                {
                    "evaluator": "evaluator",
                    "criteria": "x",
                    "explain_strategy": "never",
                }
            ],
            app="xx",
            capture="all",
            confidence_interval_strategy="none",
            dataset_id="dataset_id",
            dataset_sample_id="dataset_sample_id",
            evaluated_model_attachments=[
                {
                    "media_type": "image/jpeg",
                    "url": "url",
                    "usage_type": "evaluated_model_system_prompt",
                }
            ],
            experiment_id="experiment_id",
            gold_answer="gold_answer",
            log_id="log_id",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            span_id="span_id",
            system_prompt="system_prompt",
            tags={},
            task_context=["string"],
            task_input="task_input",
            task_output="task_output",
            trace_id="trace_id",
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_evaluate(self, client: PatronusAPI) -> None:
        response = client.evaluations.with_raw_response.evaluate(
            evaluators=[{"evaluator": "evaluator"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_evaluate(self, client: PatronusAPI) -> None:
        with client.evaluations.with_streaming_response.evaluate(
            evaluators=[{"evaluator": "evaluator"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.search()
        assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: PatronusAPI) -> None:
        evaluation = client.evaluations.search(
            filters=[
                {
                    "and_": [{}],
                    "field": "field",
                    "operation": "starts_with",
                    "or_": [{}],
                    "value": [{}],
                }
            ],
            log_id_in=["string"],
            trace_id="trace_id",
        )
        assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: PatronusAPI) -> None:
        response = client.evaluations.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: PatronusAPI) -> None:
        with client.evaluations.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvaluations:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.retrieve(
            0,
        )
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluations.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluations.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.delete(
            0,
        )
        assert evaluation is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluations.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert evaluation is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluations.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert evaluation is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_batch_create(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.batch_create(
            evaluations=[
                {
                    "evaluator_id": "evaluator_id",
                    "log_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )
        assert_matches_type(EvaluationBatchCreateResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_batch_create(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluations.with_raw_response.batch_create(
            evaluations=[
                {
                    "evaluator_id": "evaluator_id",
                    "log_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationBatchCreateResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_batch_create(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluations.with_streaming_response.batch_create(
            evaluations=[
                {
                    "evaluator_id": "evaluator_id",
                    "log_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationBatchCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_batch_delete(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.batch_delete()
        assert_matches_type(object, evaluation, path=["response"])

    @parametrize
    async def test_method_batch_delete_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.batch_delete(
            app="app",
            batch_size=0,
            evaluator_criteria_id="evaluator_criteria_id",
            evaluator_family="evaluator_family",
            experiment_id=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            trace_id="trace_id",
        )
        assert_matches_type(object, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_batch_delete(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluations.with_raw_response.batch_delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(object, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_batch_delete(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluations.with_streaming_response.batch_delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(object, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_evaluate(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.evaluate(
            evaluators=[{"evaluator": "evaluator"}],
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_evaluate_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.evaluate(
            evaluators=[
                {
                    "evaluator": "evaluator",
                    "criteria": "x",
                    "explain_strategy": "never",
                }
            ],
            app="xx",
            capture="all",
            confidence_interval_strategy="none",
            dataset_id="dataset_id",
            dataset_sample_id="dataset_sample_id",
            evaluated_model_attachments=[
                {
                    "media_type": "image/jpeg",
                    "url": "url",
                    "usage_type": "evaluated_model_system_prompt",
                }
            ],
            experiment_id="experiment_id",
            gold_answer="gold_answer",
            log_id="log_id",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            span_id="span_id",
            system_prompt="system_prompt",
            tags={},
            task_context=["string"],
            task_input="task_input",
            task_output="task_output",
            trace_id="trace_id",
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_evaluate(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluations.with_raw_response.evaluate(
            evaluators=[{"evaluator": "evaluator"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_evaluate(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluations.with_streaming_response.evaluate(
            evaluators=[{"evaluator": "evaluator"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.search()
        assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluation = await async_client.evaluations.search(
            filters=[
                {
                    "and_": [{}],
                    "field": "field",
                    "operation": "starts_with",
                    "or_": [{}],
                    "value": [{}],
                }
            ],
            log_id_in=["string"],
            trace_id="trace_id",
        )
        assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluations.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluations.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationSearchResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True
