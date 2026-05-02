# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import ChatCompletionsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChatCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGPClient) -> None:
        chat_completion = client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
        )
        assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGPClient) -> None:
        chat_completion = client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            account_id="account_id",
            chat_template="chat_template",
            instructions="instructions",
            memory_strategy={
                "params": {"k": 1},
                "name": "last_k",
            },
            model_parameters={
                "frequency_penalty": 0,
                "max_tokens": 0,
                "presence_penalty": 0,
                "reasoning_effort": "low",
                "stop_sequences": ["string"],
                "temperature": 0,
                "top_k": 0,
                "top_p": 0,
            },
            stream=False,
        )
        assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGPClient) -> None:
        response = client.chat_completions.with_raw_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_completion = response.parse()
        assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGPClient) -> None:
        with client.chat_completions.with_streaming_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_completion = response.parse()
            assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: SGPClient) -> None:
        chat_completion_stream = client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
        )
        chat_completion_stream.response.close()

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGPClient) -> None:
        chat_completion_stream = client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
            account_id="account_id",
            chat_template="chat_template",
            instructions="instructions",
            memory_strategy={
                "params": {"k": 1},
                "name": "last_k",
            },
            model_parameters={
                "frequency_penalty": 0,
                "max_tokens": 0,
                "presence_penalty": 0,
                "reasoning_effort": "low",
                "stop_sequences": ["string"],
                "temperature": 0,
                "top_k": 0,
                "top_p": 0,
            },
        )
        chat_completion_stream.response.close()

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGPClient) -> None:
        response = client.chat_completions.with_raw_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGPClient) -> None:
        with client.chat_completions.with_streaming_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncChatCompletions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        chat_completion = await async_client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
        )
        assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        chat_completion = await async_client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            account_id="account_id",
            chat_template="chat_template",
            instructions="instructions",
            memory_strategy={
                "params": {"k": 1},
                "name": "last_k",
            },
            model_parameters={
                "frequency_penalty": 0,
                "max_tokens": 0,
                "presence_penalty": 0,
                "reasoning_effort": "low",
                "stop_sequences": ["string"],
                "temperature": 0,
                "top_k": 0,
                "top_p": 0,
            },
            stream=False,
        )
        assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chat_completions.with_raw_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_completion = await response.parse()
        assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chat_completions.with_streaming_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_completion = await response.parse()
            assert_matches_type(ChatCompletionsResponse, chat_completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        chat_completion_stream = await async_client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
        )
        await chat_completion_stream.response.aclose()

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGPClient) -> None:
        chat_completion_stream = await async_client.chat_completions.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
            account_id="account_id",
            chat_template="chat_template",
            instructions="instructions",
            memory_strategy={
                "params": {"k": 1},
                "name": "last_k",
            },
            model_parameters={
                "frequency_penalty": 0,
                "max_tokens": 0,
                "presence_penalty": 0,
                "reasoning_effort": "low",
                "stop_sequences": ["string"],
                "temperature": 0,
                "top_k": 0,
                "top_p": 0,
            },
        )
        await chat_completion_stream.response.aclose()

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chat_completions.with_raw_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chat_completions.with_streaming_response.create(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-oss-120b",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
