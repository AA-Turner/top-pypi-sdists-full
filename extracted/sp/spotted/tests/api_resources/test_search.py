# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import SearchQueryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_query(self, client: Spotted) -> None:
        search = client.search.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
        )
        assert_matches_type(SearchQueryResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_query_with_all_params(self, client: Spotted) -> None:
        search = client.search.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
            include_external="audio",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SearchQueryResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_query(self, client: Spotted) -> None:
        response = client.search.with_raw_response.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchQueryResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_query(self, client: Spotted) -> None:
        with client.search.with_streaming_response.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchQueryResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_query(self, async_client: AsyncSpotted) -> None:
        search = await async_client.search.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
        )
        assert_matches_type(SearchQueryResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncSpotted) -> None:
        search = await async_client.search.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
            include_external="audio",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SearchQueryResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncSpotted) -> None:
        response = await async_client.search.with_raw_response.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchQueryResponse, search, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncSpotted) -> None:
        async with async_client.search.with_streaming_response.query(
            q="remaster%20track:Doxy%20artist:Miles%20Davis",
            type=["album"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchQueryResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
