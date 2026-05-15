# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import ExecuteAgentResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_execute(self, client: SGPClient) -> None:
        agent = client.agents.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {"type": "object"},
                    "description": "description",
                    "name": "name",
                }
            ],
        )
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: SGPClient) -> None:
        agent = client.agents.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "description": "description",
                                "type": "string",
                                "default": "default",
                                "examples": ["string"],
                            }
                        },
                        "required": ["string"],
                    },
                    "description": "description",
                    "name": "name",
                }
            ],
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
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: SGPClient) -> None:
        response = client.agents.with_raw_response.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {"type": "object"},
                    "description": "description",
                    "name": "name",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: SGPClient) -> None:
        with client.agents.with_streaming_response.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {"type": "object"},
                    "description": "description",
                    "name": "name",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_execute(self, async_client: AsyncSGPClient) -> None:
        agent = await async_client.agents.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {"type": "object"},
                    "description": "description",
                    "name": "name",
                }
            ],
        )
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncSGPClient) -> None:
        agent = await async_client.agents.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "description": "description",
                                "type": "string",
                                "default": "default",
                                "examples": ["string"],
                            }
                        },
                        "required": ["string"],
                    },
                    "description": "description",
                    "name": "name",
                }
            ],
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
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agents.with_raw_response.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {"type": "object"},
                    "description": "description",
                    "name": "name",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agents.with_streaming_response.execute(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="gpt-4",
            tools=[
                {
                    "arguments": {"type": "object"},
                    "description": "description",
                    "name": "name",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True
