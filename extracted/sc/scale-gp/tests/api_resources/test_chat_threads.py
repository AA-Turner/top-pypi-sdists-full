# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import ChatThread

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChatThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        chat_thread = client.chat_threads.update(
            thread_id="thread_id",
        )
        assert_matches_type(ChatThread, chat_thread, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        chat_thread = client.chat_threads.update(
            thread_id="thread_id",
            archived_at="archived_at",
            thread_metadata={"foo": "bar"},
            title="title",
        )
        assert_matches_type(ChatThread, chat_thread, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.chat_threads.with_raw_response.update(
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_thread = response.parse()
        assert_matches_type(ChatThread, chat_thread, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.chat_threads.with_streaming_response.update(
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_thread = response.parse()
            assert_matches_type(ChatThread, chat_thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.chat_threads.with_raw_response.update(
                thread_id="",
            )

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        chat_thread = client.chat_threads.delete(
            "thread_id",
        )
        assert_matches_type(object, chat_thread, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.chat_threads.with_raw_response.delete(
            "thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_thread = response.parse()
        assert_matches_type(object, chat_thread, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.chat_threads.with_streaming_response.delete(
            "thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_thread = response.parse()
            assert_matches_type(object, chat_thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.chat_threads.with_raw_response.delete(
                "",
            )


class TestAsyncChatThreads:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        chat_thread = await async_client.chat_threads.update(
            thread_id="thread_id",
        )
        assert_matches_type(ChatThread, chat_thread, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        chat_thread = await async_client.chat_threads.update(
            thread_id="thread_id",
            archived_at="archived_at",
            thread_metadata={"foo": "bar"},
            title="title",
        )
        assert_matches_type(ChatThread, chat_thread, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chat_threads.with_raw_response.update(
            thread_id="thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_thread = await response.parse()
        assert_matches_type(ChatThread, chat_thread, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chat_threads.with_streaming_response.update(
            thread_id="thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_thread = await response.parse()
            assert_matches_type(ChatThread, chat_thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.chat_threads.with_raw_response.update(
                thread_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        chat_thread = await async_client.chat_threads.delete(
            "thread_id",
        )
        assert_matches_type(object, chat_thread, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chat_threads.with_raw_response.delete(
            "thread_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_thread = await response.parse()
        assert_matches_type(object, chat_thread, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chat_threads.with_streaming_response.delete(
            "thread_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_thread = await response.parse()
            assert_matches_type(object, chat_thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.chat_threads.with_raw_response.delete(
                "",
            )
