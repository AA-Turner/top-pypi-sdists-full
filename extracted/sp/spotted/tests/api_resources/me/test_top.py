# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.shared import TrackObject, ArtistObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTop:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_top_artists(self, client: Spotted) -> None:
        top = client.me.top.list_top_artists()
        assert_matches_type(SyncCursorURLPage[ArtistObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_top_artists_with_all_params(self, client: Spotted) -> None:
        top = client.me.top.list_top_artists(
            limit=10,
            offset=5,
            time_range="medium_term",
        )
        assert_matches_type(SyncCursorURLPage[ArtistObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_top_artists(self, client: Spotted) -> None:
        response = client.me.top.with_raw_response.list_top_artists()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        top = response.parse()
        assert_matches_type(SyncCursorURLPage[ArtistObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_top_artists(self, client: Spotted) -> None:
        with client.me.top.with_streaming_response.list_top_artists() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            top = response.parse()
            assert_matches_type(SyncCursorURLPage[ArtistObject], top, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_top_tracks(self, client: Spotted) -> None:
        top = client.me.top.list_top_tracks()
        assert_matches_type(SyncCursorURLPage[TrackObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_top_tracks_with_all_params(self, client: Spotted) -> None:
        top = client.me.top.list_top_tracks(
            limit=10,
            offset=5,
            time_range="medium_term",
        )
        assert_matches_type(SyncCursorURLPage[TrackObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_top_tracks(self, client: Spotted) -> None:
        response = client.me.top.with_raw_response.list_top_tracks()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        top = response.parse()
        assert_matches_type(SyncCursorURLPage[TrackObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_top_tracks(self, client: Spotted) -> None:
        with client.me.top.with_streaming_response.list_top_tracks() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            top = response.parse()
            assert_matches_type(SyncCursorURLPage[TrackObject], top, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTop:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_top_artists(self, async_client: AsyncSpotted) -> None:
        top = await async_client.me.top.list_top_artists()
        assert_matches_type(AsyncCursorURLPage[ArtistObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_top_artists_with_all_params(self, async_client: AsyncSpotted) -> None:
        top = await async_client.me.top.list_top_artists(
            limit=10,
            offset=5,
            time_range="medium_term",
        )
        assert_matches_type(AsyncCursorURLPage[ArtistObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_top_artists(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.top.with_raw_response.list_top_artists()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        top = await response.parse()
        assert_matches_type(AsyncCursorURLPage[ArtistObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_top_artists(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.top.with_streaming_response.list_top_artists() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            top = await response.parse()
            assert_matches_type(AsyncCursorURLPage[ArtistObject], top, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_top_tracks(self, async_client: AsyncSpotted) -> None:
        top = await async_client.me.top.list_top_tracks()
        assert_matches_type(AsyncCursorURLPage[TrackObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_top_tracks_with_all_params(self, async_client: AsyncSpotted) -> None:
        top = await async_client.me.top.list_top_tracks(
            limit=10,
            offset=5,
            time_range="medium_term",
        )
        assert_matches_type(AsyncCursorURLPage[TrackObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_top_tracks(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.top.with_raw_response.list_top_tracks()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        top = await response.parse()
        assert_matches_type(AsyncCursorURLPage[TrackObject], top, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_top_tracks(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.top.with_streaming_response.list_top_tracks() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            top = await response.parse()
            assert_matches_type(AsyncCursorURLPage[TrackObject], top, path=["response"])

        assert cast(Any, response.is_closed) is True
