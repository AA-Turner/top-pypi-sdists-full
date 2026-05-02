# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFeedback:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        feedback = client.chat_threads.messages.feedback.delete(
            application_interaction_id="application_interaction_id",
            thread_id="thread_id",
        )
        assert_matches_type(object, feedback, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.chat_threads.messages.feedback.with_raw_response.delete(
            application_interaction_id="application_interaction_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feedback = response.parse()
        assert_matches_type(object, feedback, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.chat_threads.messages.feedback.with_streaming_response.delete(
            application_interaction_id="application_interaction_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feedback = response.parse()
            assert_matches_type(object, feedback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.chat_threads.messages.feedback.with_raw_response.delete(
                application_interaction_id="application_interaction_id",
                thread_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_interaction_id` but received ''"
        ):
            client.chat_threads.messages.feedback.with_raw_response.delete(
                application_interaction_id="",
                thread_id="thread_id",
            )


class TestAsyncFeedback:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        feedback = await async_client.chat_threads.messages.feedback.delete(
            application_interaction_id="application_interaction_id",
            thread_id="thread_id",
        )
        assert_matches_type(object, feedback, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chat_threads.messages.feedback.with_raw_response.delete(
            application_interaction_id="application_interaction_id",
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feedback = await response.parse()
        assert_matches_type(object, feedback, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chat_threads.messages.feedback.with_streaming_response.delete(
            application_interaction_id="application_interaction_id",
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feedback = await response.parse()
            assert_matches_type(object, feedback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.chat_threads.messages.feedback.with_raw_response.delete(
                application_interaction_id="application_interaction_id",
                thread_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_interaction_id` but received ''"
        ):
            await async_client.chat_threads.messages.feedback.with_raw_response.delete(
                application_interaction_id="",
                thread_id="thread_id",
            )
