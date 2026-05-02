# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import PlaylistRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPlaylists:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        playlist = client.playlists.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )
        assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        playlist = client.playlists.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            additional_types="additional_types",
            fields="items(added_by.id,track(name,href,album(name,href)))",
            market="ES",
        )
        assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.playlists.with_raw_response.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = response.parse()
        assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.playlists.with_streaming_response.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            playlist = response.parse()
            assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            client.playlists.with_raw_response.retrieve(
                playlist_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Spotted) -> None:
        playlist = client.playlists.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )
        assert playlist is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Spotted) -> None:
        playlist = client.playlists.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            collaborative=True,
            description="Updated playlist description",
            name="Updated Playlist Name",
            published=True,
        )
        assert playlist is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Spotted) -> None:
        response = client.playlists.with_raw_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = response.parse()
        assert playlist is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Spotted) -> None:
        with client.playlists.with_streaming_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            playlist = response.parse()
            assert playlist is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            client.playlists.with_raw_response.update(
                playlist_id="",
            )


class TestAsyncPlaylists:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        playlist = await async_client.playlists.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )
        assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        playlist = await async_client.playlists.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            additional_types="additional_types",
            fields="items(added_by.id,track(name,href,album(name,href)))",
            market="ES",
        )
        assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.playlists.with_raw_response.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = await response.parse()
        assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.playlists.with_streaming_response.retrieve(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            playlist = await response.parse()
            assert_matches_type(PlaylistRetrieveResponse, playlist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            await async_client.playlists.with_raw_response.retrieve(
                playlist_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncSpotted) -> None:
        playlist = await async_client.playlists.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )
        assert playlist is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSpotted) -> None:
        playlist = await async_client.playlists.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            collaborative=True,
            description="Updated playlist description",
            name="Updated Playlist Name",
            published=True,
        )
        assert playlist is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSpotted) -> None:
        response = await async_client.playlists.with_raw_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        playlist = await response.parse()
        assert playlist is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSpotted) -> None:
        async with async_client.playlists.with_streaming_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            playlist = await response.parse()
            assert playlist is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            await async_client.playlists.with_raw_response.update(
                playlist_id="",
            )
