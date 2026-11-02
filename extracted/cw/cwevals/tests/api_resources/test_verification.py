# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types import VerificationGetResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVerification:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: Client) -> None:
        verification = client.verification.get()
        assert_matches_type(VerificationGetResponse, verification, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.verification.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification = response.parse()
        assert_matches_type(VerificationGetResponse, verification, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.verification.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification = response.parse()
            assert_matches_type(VerificationGetResponse, verification, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncVerification:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        verification = await async_client.verification.get()
        assert_matches_type(VerificationGetResponse, verification, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.verification.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification = await response.parse()
        assert_matches_type(VerificationGetResponse, verification, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.verification.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification = await response.parse()
            assert_matches_type(VerificationGetResponse, verification, path=["response"])

        assert cast(Any, response.is_closed) is True
