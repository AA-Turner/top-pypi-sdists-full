# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types.me.player import QueueGetResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQueue:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add(self, client: Spotted) -> None:
        queue = client.me.player.queue.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        )
        assert queue is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add_with_all_params(self, client: Spotted) -> None:
        queue = client.me.player.queue.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert queue is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_add(self, client: Spotted) -> None:
        response = client.me.player.queue.with_raw_response.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        queue = response.parse()
        assert queue is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_add(self, client: Spotted) -> None:
        with client.me.player.queue.with_streaming_response.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            queue = response.parse()
            assert queue is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get(self, client: Spotted) -> None:
        queue = client.me.player.queue.get()
        assert_matches_type(QueueGetResponse, queue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get(self, client: Spotted) -> None:
        response = client.me.player.queue.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        queue = response.parse()
        assert_matches_type(QueueGetResponse, queue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get(self, client: Spotted) -> None:
        with client.me.player.queue.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            queue = response.parse()
            assert_matches_type(QueueGetResponse, queue, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncQueue:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add(self, async_client: AsyncSpotted) -> None:
        queue = await async_client.me.player.queue.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        )
        assert queue is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncSpotted) -> None:
        queue = await async_client.me.player.queue.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert queue is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.queue.with_raw_response.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        queue = await response.parse()
        assert queue is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.queue.with_streaming_response.add(
            uri="spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            queue = await response.parse()
            assert queue is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get(self, async_client: AsyncSpotted) -> None:
        queue = await async_client.me.player.queue.get()
        assert_matches_type(QueueGetResponse, queue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.queue.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        queue = await response.parse()
        assert_matches_type(QueueGetResponse, queue, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.queue.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            queue = await response.parse()
            assert_matches_type(QueueGetResponse, queue, path=["response"])

        assert cast(Any, response.is_closed) is True
