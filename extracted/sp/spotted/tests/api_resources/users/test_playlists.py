# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.users import PlaylistCreateResponse
from spotted.types.shared import SimplifiedPlaylistObject

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPlaylists:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = client.users.playlists.create(
                user_id="smedjan",
                name="New Playlist",
            )

        assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = client.users.playlists.create(
                user_id="smedjan",
                name="New Playlist",
                collaborative=True,
                description="New playlist description",
                published=True,
            )

        assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.users.playlists.with_raw_response.create(
                user_id="smedjan",
                name="New Playlist",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = response.parse()
        assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.users.playlists.with_streaming_response.create(
                user_id="smedjan",
                name="New Playlist",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                playlist = response.parse()
                assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
                client.users.playlists.with_raw_response.create(
                    user_id="",
                    name="New Playlist",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = client.users.playlists.list(
                user_id="smedjan",
            )

        assert_matches_type(SyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = client.users.playlists.list(
                user_id="smedjan",
                limit=10,
                offset=5,
            )

        assert_matches_type(SyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.users.playlists.with_raw_response.list(
                user_id="smedjan",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = response.parse()
        assert_matches_type(SyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.users.playlists.with_streaming_response.list(
                user_id="smedjan",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                playlist = response.parse()
                assert_matches_type(SyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
                client.users.playlists.with_raw_response.list(
                    user_id="",
                )


class TestAsyncPlaylists:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = await async_client.users.playlists.create(
                user_id="smedjan",
                name="New Playlist",
            )

        assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = await async_client.users.playlists.create(
                user_id="smedjan",
                name="New Playlist",
                collaborative=True,
                description="New playlist description",
                published=True,
            )

        assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.users.playlists.with_raw_response.create(
                user_id="smedjan",
                name="New Playlist",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = await response.parse()
        assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.users.playlists.with_streaming_response.create(
                user_id="smedjan",
                name="New Playlist",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                playlist = await response.parse()
                assert_matches_type(PlaylistCreateResponse, playlist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
                await async_client.users.playlists.with_raw_response.create(
                    user_id="",
                    name="New Playlist",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = await async_client.users.playlists.list(
                user_id="smedjan",
            )

        assert_matches_type(AsyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            playlist = await async_client.users.playlists.list(
                user_id="smedjan",
                limit=10,
                offset=5,
            )

        assert_matches_type(AsyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.users.playlists.with_raw_response.list(
                user_id="smedjan",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = await response.parse()
        assert_matches_type(AsyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.users.playlists.with_streaming_response.list(
                user_id="smedjan",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                playlist = await response.parse()
                assert_matches_type(AsyncCursorURLPage[SimplifiedPlaylistObject], playlist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
                await async_client.users.playlists.with_raw_response.list(
                    user_id="",
                )
