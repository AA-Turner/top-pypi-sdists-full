# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import ResponseCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResponses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        response = client.responses.create(
            input="string",
            model="model",
        )
        assert_matches_type(ResponseCreateResponse, response, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        response = client.responses.create(
            input="string",
            model="model",
            include=["string"],
            instructions="instructions",
            max_output_tokens=0,
            metadata={"foo": "bar"},
            parallel_tool_calls=True,
            previous_response_id="previous_response_id",
            reasoning={"foo": "bar"},
            store=True,
            stream=True,
            temperature=0,
            text={"foo": "bar"},
            tool_choice="string",
            tools=[{"foo": "bar"}],
            top_p=0,
            truncation="auto",
        )
        assert_matches_type(ResponseCreateResponse, response, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        http_response = client.responses.with_raw_response.create(
            input="string",
            model="model",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseCreateResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.responses.with_streaming_response.create(
            input="string",
            model="model",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseCreateResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True


class TestAsyncResponses:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.responses.create(
            input="string",
            model="model",
        )
        assert_matches_type(ResponseCreateResponse, response, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.responses.create(
            input="string",
            model="model",
            include=["string"],
            instructions="instructions",
            max_output_tokens=0,
            metadata={"foo": "bar"},
            parallel_tool_calls=True,
            previous_response_id="previous_response_id",
            reasoning={"foo": "bar"},
            store=True,
            stream=True,
            temperature=0,
            text={"foo": "bar"},
            tool_choice="string",
            tools=[{"foo": "bar"}],
            top_p=0,
            truncation="auto",
        )
        assert_matches_type(ResponseCreateResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        http_response = await async_client.responses.with_raw_response.create(
            input="string",
            model="model",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseCreateResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.responses.with_streaming_response.create(
            input="string",
            model="model",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseCreateResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True
