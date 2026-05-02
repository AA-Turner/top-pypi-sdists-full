# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import InteractionCreateResponse
from scale_gp._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInteractions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        interaction = client.interactions.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={"response": "response"},
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        interaction = client.interactions.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={
                "response": "response",
                "context": [
                    {
                        "text": "text",
                        "score": 0,
                    }
                ],
            },
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            duration_ms=0,
            operation_metadata={"foo": "bar"},
            operation_status="SUCCESS",
            thread_id="thread_id",
            trace_spans=[
                {
                    "node_id": "node_id",
                    "operation_type": "COMPLETION",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "account_id": "account_id",
                    "duration_ms": 0,
                    "end_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "operation_input": {"foo": "bar"},
                    "operation_metadata": {"foo": "bar"},
                    "operation_output": {"foo": "bar"},
                    "operation_status": "SUCCESS",
                }
            ],
        )
        assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.interactions.with_raw_response.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={"response": "response"},
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        interaction = response.parse()
        assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.interactions.with_streaming_response.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={"response": "response"},
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            interaction = response.parse()
            assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInteractions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        interaction = await async_client.interactions.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={"response": "response"},
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        interaction = await async_client.interactions.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={
                "response": "response",
                "context": [
                    {
                        "text": "text",
                        "score": 0,
                    }
                ],
            },
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            duration_ms=0,
            operation_metadata={"foo": "bar"},
            operation_status="SUCCESS",
            thread_id="thread_id",
            trace_spans=[
                {
                    "node_id": "node_id",
                    "operation_type": "COMPLETION",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "account_id": "account_id",
                    "duration_ms": 0,
                    "end_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "operation_input": {"foo": "bar"},
                    "operation_metadata": {"foo": "bar"},
                    "operation_output": {"foo": "bar"},
                    "operation_status": "SUCCESS",
                }
            ],
        )
        assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.interactions.with_raw_response.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={"response": "response"},
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        interaction = await response.parse()
        assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.interactions.with_streaming_response.create(
            application_variant_id="application_variant_id",
            input={"query": "query"},
            output={"response": "response"},
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            interaction = await response.parse()
            assert_matches_type(InteractionCreateResponse, interaction, path=["response"])

        assert cast(Any, response.is_closed) is True
