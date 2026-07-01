# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import Evaluation

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        task = client.evaluations.tasks.update(
            alias="alias",
            evaluation_id="evaluation_id",
            configuration={"foo": "bar"},
        )
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluations.tasks.with_raw_response.update(
            alias="alias",
            evaluation_id="evaluation_id",
            configuration={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluations.tasks.with_streaming_response.update(
            alias="alias",
            evaluation_id="evaluation_id",
            configuration={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(Evaluation, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.tasks.with_raw_response.update(
                alias="alias",
                evaluation_id="",
                configuration={"foo": "bar"},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `alias` but received ''"):
            client.evaluations.tasks.with_raw_response.update(
                alias="",
                evaluation_id="evaluation_id",
                configuration={"foo": "bar"},
            )

    @parametrize
    def test_method_add(self, client: SGPClient) -> None:
        task = client.evaluations.tasks.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                },
                "task_type": "chat_completion",
            },
        )
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    def test_method_add_with_all_params(self, client: SGPClient) -> None:
        task = client.evaluations.tasks.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                    "audio": {"foo": "bar"},
                    "frequency_penalty": 0,
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
                    "presence_penalty": 0,
                    "reasoning_effort": "reasoning_effort",
                    "response_format": {"foo": "bar"},
                    "seed": 0,
                    "stop": "stop",
                    "store": True,
                    "temperature": 0,
                    "tool_choice": "tool_choice",
                    "tools": [{"foo": "bar"}],
                    "top_k": 0,
                    "top_logprobs": 0,
                    "top_p": 0,
                },
                "alias": "alias",
                "task_type": "chat_completion",
            },
        )
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: SGPClient) -> None:
        response = client.evaluations.tasks.with_raw_response.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                },
                "task_type": "chat_completion",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: SGPClient) -> None:
        with client.evaluations.tasks.with_streaming_response.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                },
                "task_type": "chat_completion",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(Evaluation, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.tasks.with_raw_response.add(
                evaluation_id="",
                task={
                    "configuration": {
                        "messages": [{"foo": "bar"}],
                        "model": "model",
                    },
                    "task_type": "chat_completion",
                },
            )


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        task = await async_client.evaluations.tasks.update(
            alias="alias",
            evaluation_id="evaluation_id",
            configuration={"foo": "bar"},
        )
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.tasks.with_raw_response.update(
            alias="alias",
            evaluation_id="evaluation_id",
            configuration={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.tasks.with_streaming_response.update(
            alias="alias",
            evaluation_id="evaluation_id",
            configuration={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(Evaluation, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.update(
                alias="alias",
                evaluation_id="",
                configuration={"foo": "bar"},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `alias` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.update(
                alias="",
                evaluation_id="evaluation_id",
                configuration={"foo": "bar"},
            )

    @parametrize
    async def test_method_add(self, async_client: AsyncSGPClient) -> None:
        task = await async_client.evaluations.tasks.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                },
                "task_type": "chat_completion",
            },
        )
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncSGPClient) -> None:
        task = await async_client.evaluations.tasks.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                    "audio": {"foo": "bar"},
                    "frequency_penalty": 0,
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
                    "presence_penalty": 0,
                    "reasoning_effort": "reasoning_effort",
                    "response_format": {"foo": "bar"},
                    "seed": 0,
                    "stop": "stop",
                    "store": True,
                    "temperature": 0,
                    "tool_choice": "tool_choice",
                    "tools": [{"foo": "bar"}],
                    "top_k": 0,
                    "top_logprobs": 0,
                    "top_p": 0,
                },
                "alias": "alias",
                "task_type": "chat_completion",
            },
        )
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.tasks.with_raw_response.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                },
                "task_type": "chat_completion",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(Evaluation, task, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.tasks.with_streaming_response.add(
            evaluation_id="evaluation_id",
            task={
                "configuration": {
                    "messages": [{"foo": "bar"}],
                    "model": "model",
                },
                "task_type": "chat_completion",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(Evaluation, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.add(
                evaluation_id="",
                task={
                    "configuration": {
                        "messages": [{"foo": "bar"}],
                        "model": "model",
                    },
                    "task_type": "chat_completion",
                },
            )
