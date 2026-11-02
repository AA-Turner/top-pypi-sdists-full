# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types import ServiceGetResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestService:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: Client) -> None:
        service = client.service.get()
        assert_matches_type(ServiceGetResponse, service, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.service.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service = response.parse()
        assert_matches_type(ServiceGetResponse, service, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.service.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service = response.parse()
            assert_matches_type(ServiceGetResponse, service, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncService:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        service = await async_client.service.get()
        assert_matches_type(ServiceGetResponse, service, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.service.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service = await response.parse()
        assert_matches_type(ServiceGetResponse, service, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.service.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service = await response.parse()
            assert_matches_type(ServiceGetResponse, service, path=["response"])

        assert cast(Any, response.is_closed) is True
