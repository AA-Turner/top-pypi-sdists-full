# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    Evaluation,
    EvaluationSchemaResponse,
    EvaluationRetrieveTaxonomyResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        evaluation = client.evaluations.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
            },
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
                "description": "description",
                "files": [{"foo": "string"}],
                "metadata": {"foo": "bar"},
                "tags": ["string"],
                "tasks": [
                    {
                        "configuration": {
                            "messages": [{"foo": "bar"}],
                            "model": "model",
                            "audio": {"foo": "bar"},
                            "frequency_penalty": -2,
                            "function_call": {"foo": "bar"},
                            "functions": [{"foo": "bar"}],
                            "logit_bias": {"foo": 0},
                            "logprobs": True,
                            "max_completion_tokens": 0,
                            "max_tokens": 0,
                            "metadata": {"foo": "string"},
                            "modalities": ["string"],
                            "n": 0,
                            "parallel_tool_calls": True,
                            "prediction": {"foo": "bar"},
                            "presence_penalty": -2,
                            "reasoning_effort": "reasoning_effort",
                            "response_format": {"foo": "bar"},
                            "seed": 0,
                            "stop": "string",
                            "store": True,
                            "temperature": 0,
                            "tool_choice": "string",
                            "tools": [{"foo": "bar"}],
                            "top_k": 0,
                            "top_logprobs": 0,
                            "top_p": 0,
                        },
                        "alias": "alias",
                        "task_type": "chat_completion",
                    }
                ],
                "taxonomy_params": {"foo": "bar"},
            },
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve(
            evaluation_id="evaluation_id",
            include_archived=True,
            views=["tasks"],
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.retrieve(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.retrieve(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.retrieve(
                evaluation_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        evaluation = client.evaluations.update(
            evaluation_id="evaluation_id",
            evaluation={},
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.update(
            evaluation_id="evaluation_id",
            evaluation={
                "description": "description",
                "metadata": {"foo": "bar"},
                "name": "name",
                "tags": ["string"],
            },
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.update(
            evaluation_id="evaluation_id",
            evaluation={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.update(
            evaluation_id="evaluation_id",
            evaluation={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.update(
                evaluation_id="",
                evaluation={},
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation = client.evaluations.list()
        assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.list(
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
            views=["tasks"],
        )
        assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        evaluation = client.evaluations.archive(
            "evaluation_id",
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.archive(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.archive(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.archive(
                "",
            )

    @parametrize
    def test_method_filter(self, client: SGPClient) -> None:
        evaluation = client.evaluations.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                }
            ],
        )
        assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    def test_method_filter_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                    "object": "metadata_filter",
                }
            ],
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            views=["tasks"],
        )
        assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    def test_raw_response_filter(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    def test_streaming_response_filter(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(SyncCursorPage[Evaluation], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve_schema(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve_schema(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

    @parametrize
    def test_method_retrieve_schema_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve_schema(
            evaluation_id="evaluation_id",
            include_archived=True,
        )
        assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_retrieve_schema(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.retrieve_schema(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_schema(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.retrieve_schema(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_schema(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.retrieve_schema(
                evaluation_id="",
            )

    @parametrize
    def test_method_retrieve_taxonomy(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve_taxonomy(
            "evaluation_id",
        )
        assert_matches_type(EvaluationRetrieveTaxonomyResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_retrieve_taxonomy(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.retrieve_taxonomy(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationRetrieveTaxonomyResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_taxonomy(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.retrieve_taxonomy(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationRetrieveTaxonomyResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_taxonomy(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.retrieve_taxonomy(
                "",
            )


class TestAsyncEvaluations:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
            },
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
                "description": "description",
                "files": [{"foo": "string"}],
                "metadata": {"foo": "bar"},
                "tags": ["string"],
                "tasks": [
                    {
                        "configuration": {
                            "messages": [{"foo": "bar"}],
                            "model": "model",
                            "audio": {"foo": "bar"},
                            "frequency_penalty": -2,
                            "function_call": {"foo": "bar"},
                            "functions": [{"foo": "bar"}],
                            "logit_bias": {"foo": 0},
                            "logprobs": True,
                            "max_completion_tokens": 0,
                            "max_tokens": 0,
                            "metadata": {"foo": "string"},
                            "modalities": ["string"],
                            "n": 0,
                            "parallel_tool_calls": True,
                            "prediction": {"foo": "bar"},
                            "presence_penalty": -2,
                            "reasoning_effort": "reasoning_effort",
                            "response_format": {"foo": "bar"},
                            "seed": 0,
                            "stop": "string",
                            "store": True,
                            "temperature": 0,
                            "tool_choice": "string",
                            "tools": [{"foo": "bar"}],
                            "top_k": 0,
                            "top_logprobs": 0,
                            "top_p": 0,
                        },
                        "alias": "alias",
                        "task_type": "chat_completion",
                    }
                ],
                "taxonomy_params": {"foo": "bar"},
            },
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.create(
            evaluation={
                "data": [{"foo": "bar"}],
                "name": "name",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve(
            evaluation_id="evaluation_id",
            include_archived=True,
            views=["tasks"],
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.retrieve(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.retrieve(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.retrieve(
                evaluation_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.update(
            evaluation_id="evaluation_id",
            evaluation={},
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.update(
            evaluation_id="evaluation_id",
            evaluation={
                "description": "description",
                "metadata": {"foo": "bar"},
                "name": "name",
                "tags": ["string"],
            },
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.update(
            evaluation_id="evaluation_id",
            evaluation={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.update(
            evaluation_id="evaluation_id",
            evaluation={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.update(
                evaluation_id="",
                evaluation={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.list()
        assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.list(
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
            views=["tasks"],
        )
        assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.archive(
            "evaluation_id",
        )
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.archive(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(Evaluation, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.archive(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(Evaluation, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.archive(
                "",
            )

    @parametrize
    async def test_method_filter(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                }
            ],
        )
        assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    async def test_method_filter_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                    "object": "metadata_filter",
                }
            ],
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            views=["tasks"],
        )
        assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    async def test_raw_response_filter(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_filter(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.filter(
            filters=[
                {
                    "key": "key",
                    "operator": "==",
                    "value": "value",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(AsyncCursorPage[Evaluation], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve_schema(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_retrieve_schema_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve_schema(
            evaluation_id="evaluation_id",
            include_archived=True,
        )
        assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.retrieve_schema(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.retrieve_schema(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationSchemaResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.retrieve_schema(
                evaluation_id="",
            )

    @parametrize
    async def test_method_retrieve_taxonomy(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve_taxonomy(
            "evaluation_id",
        )
        assert_matches_type(EvaluationRetrieveTaxonomyResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_taxonomy(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.retrieve_taxonomy(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationRetrieveTaxonomyResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_taxonomy(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.retrieve_taxonomy(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationRetrieveTaxonomyResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_taxonomy(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.retrieve_taxonomy(
                "",
            )
