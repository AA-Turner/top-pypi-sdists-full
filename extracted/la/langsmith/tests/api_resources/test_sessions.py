# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types import SessionResolveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resolve(self, client: Langsmith) -> None:
        session = client.sessions.resolve(
            kind="AGENT",
        )
        assert_matches_type(SessionResolveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resolve_with_all_params(self, client: Langsmith) -> None:
        session = client.sessions.resolve(
            kind="AGENT",
            id="id",
            environment="LOCAL",
        )
        assert_matches_type(SessionResolveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_resolve(self, client: Langsmith) -> None:

        response = client.sessions.with_raw_response.resolve(
            kind="AGENT",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionResolveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_resolve(self, client: Langsmith) -> None:
        with client.sessions.with_streaming_response.resolve(
            kind="AGENT",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionResolveResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resolve(self, async_client: AsyncLangsmith) -> None:
        session = await async_client.sessions.resolve(
            kind="AGENT",
        )
        assert_matches_type(SessionResolveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resolve_with_all_params(self, async_client: AsyncLangsmith) -> None:
        session = await async_client.sessions.resolve(
            kind="AGENT",
            id="id",
            environment="LOCAL",
        )
        assert_matches_type(SessionResolveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_resolve(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.sessions.with_raw_response.resolve(
            kind="AGENT",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionResolveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_resolve(self, async_client: AsyncLangsmith) -> None:
        async with async_client.sessions.with_streaming_response.resolve(
            kind="AGENT",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionResolveResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True
