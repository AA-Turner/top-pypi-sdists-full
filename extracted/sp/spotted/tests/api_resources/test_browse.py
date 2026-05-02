# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    BrowseGetNewReleasesResponse,
    BrowseGetFeaturedPlaylistsResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBrowse:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_featured_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = client.browse.get_featured_playlists()

        assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_featured_playlists_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = client.browse.get_featured_playlists(
                limit=10,
                locale="sv_SE",
                offset=5,
            )

        assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_featured_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.browse.with_raw_response.get_featured_playlists()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browse = response.parse()
        assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_featured_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.browse.with_streaming_response.get_featured_playlists() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                browse = response.parse()
                assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_new_releases(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = client.browse.get_new_releases()

        assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_new_releases_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = client.browse.get_new_releases(
                limit=10,
                offset=5,
            )

        assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_new_releases(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.browse.with_raw_response.get_new_releases()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browse = response.parse()
        assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_new_releases(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.browse.with_streaming_response.get_new_releases() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                browse = response.parse()
                assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBrowse:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_featured_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = await async_client.browse.get_featured_playlists()

        assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_featured_playlists_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = await async_client.browse.get_featured_playlists(
                limit=10,
                locale="sv_SE",
                offset=5,
            )

        assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_featured_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.browse.with_raw_response.get_featured_playlists()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browse = await response.parse()
        assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_featured_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.browse.with_streaming_response.get_featured_playlists() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                browse = await response.parse()
                assert_matches_type(BrowseGetFeaturedPlaylistsResponse, browse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_new_releases(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = await async_client.browse.get_new_releases()

        assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_new_releases_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            browse = await async_client.browse.get_new_releases(
                limit=10,
                offset=5,
            )

        assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_new_releases(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.browse.with_raw_response.get_new_releases()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browse = await response.parse()
        assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_new_releases(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.browse.with_streaming_response.get_new_releases() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                browse = await response.parse()
                assert_matches_type(BrowseGetNewReleasesResponse, browse, path=["response"])

        assert cast(Any, response.is_closed) is True
