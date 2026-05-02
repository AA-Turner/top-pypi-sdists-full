# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types.me import (
    PlayerGetStateResponse,
    PlayerGetDevicesResponse,
    PlayerListRecentlyPlayedResponse,
    PlayerGetCurrentlyPlayingResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPlayer:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_currently_playing(self, client: Spotted) -> None:
        player = client.me.player.get_currently_playing()
        assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_currently_playing_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.get_currently_playing(
            additional_types="additional_types",
            market="ES",
        )
        assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_currently_playing(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.get_currently_playing()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_currently_playing(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.get_currently_playing() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_devices(self, client: Spotted) -> None:
        player = client.me.player.get_devices()
        assert_matches_type(PlayerGetDevicesResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_devices(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.get_devices()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert_matches_type(PlayerGetDevicesResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_devices(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.get_devices() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert_matches_type(PlayerGetDevicesResponse, player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_state(self, client: Spotted) -> None:
        player = client.me.player.get_state()
        assert_matches_type(PlayerGetStateResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_state_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.get_state(
            additional_types="additional_types",
            market="ES",
        )
        assert_matches_type(PlayerGetStateResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_state(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.get_state()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert_matches_type(PlayerGetStateResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_state(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.get_state() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert_matches_type(PlayerGetStateResponse, player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_recently_played(self, client: Spotted) -> None:
        player = client.me.player.list_recently_played()
        assert_matches_type(SyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_recently_played_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.list_recently_played(
            after=1484811043508,
            before=0,
            limit=10,
        )
        assert_matches_type(SyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_recently_played(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.list_recently_played()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert_matches_type(SyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_recently_played(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.list_recently_played() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert_matches_type(SyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_pause_playback(self, client: Spotted) -> None:
        player = client.me.player.pause_playback()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_pause_playback_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.pause_playback(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_pause_playback(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.pause_playback()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_pause_playback(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.pause_playback() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_seek_to_position(self, client: Spotted) -> None:
        player = client.me.player.seek_to_position(
            position_ms=25000,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_seek_to_position_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.seek_to_position(
            position_ms=25000,
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_seek_to_position(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.seek_to_position(
            position_ms=25000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_seek_to_position(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.seek_to_position(
            position_ms=25000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_set_repeat_mode(self, client: Spotted) -> None:
        player = client.me.player.set_repeat_mode(
            state="context",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_set_repeat_mode_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.set_repeat_mode(
            state="context",
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_set_repeat_mode(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.set_repeat_mode(
            state="context",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_set_repeat_mode(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.set_repeat_mode(
            state="context",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_set_volume(self, client: Spotted) -> None:
        player = client.me.player.set_volume(
            volume_percent=50,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_set_volume_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.set_volume(
            volume_percent=50,
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_set_volume(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.set_volume(
            volume_percent=50,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_set_volume(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.set_volume(
            volume_percent=50,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_skip_next(self, client: Spotted) -> None:
        player = client.me.player.skip_next()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_skip_next_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.skip_next(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_skip_next(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.skip_next()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_skip_next(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.skip_next() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_skip_previous(self, client: Spotted) -> None:
        player = client.me.player.skip_previous()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_skip_previous_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.skip_previous(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_skip_previous(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.skip_previous()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_skip_previous(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.skip_previous() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_playback(self, client: Spotted) -> None:
        player = client.me.player.start_playback()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_playback_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.start_playback(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
            context_uri="spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
            offset={"position": "bar"},
            position_ms=0,
            published=True,
            uris=["string"],
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start_playback(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.start_playback()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start_playback(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.start_playback() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_toggle_shuffle(self, client: Spotted) -> None:
        player = client.me.player.toggle_shuffle(
            state=True,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_toggle_shuffle_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.toggle_shuffle(
            state=True,
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_toggle_shuffle(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.toggle_shuffle(
            state=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_toggle_shuffle(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.toggle_shuffle(
            state=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_transfer(self, client: Spotted) -> None:
        player = client.me.player.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_transfer_with_all_params(self, client: Spotted) -> None:
        player = client.me.player.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
            play=True,
            published=True,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_transfer(self, client: Spotted) -> None:
        response = client.me.player.with_raw_response.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_transfer(self, client: Spotted) -> None:
        with client.me.player.with_streaming_response.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True


class TestAsyncPlayer:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_currently_playing(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.get_currently_playing()
        assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_currently_playing_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.get_currently_playing(
            additional_types="additional_types",
            market="ES",
        )
        assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_currently_playing(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.get_currently_playing()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_currently_playing(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.get_currently_playing() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert_matches_type(PlayerGetCurrentlyPlayingResponse, player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_devices(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.get_devices()
        assert_matches_type(PlayerGetDevicesResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_devices(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.get_devices()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert_matches_type(PlayerGetDevicesResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_devices(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.get_devices() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert_matches_type(PlayerGetDevicesResponse, player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_state(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.get_state()
        assert_matches_type(PlayerGetStateResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_state_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.get_state(
            additional_types="additional_types",
            market="ES",
        )
        assert_matches_type(PlayerGetStateResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_state(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.get_state()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert_matches_type(PlayerGetStateResponse, player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_state(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.get_state() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert_matches_type(PlayerGetStateResponse, player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_recently_played(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.list_recently_played()
        assert_matches_type(AsyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_recently_played_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.list_recently_played(
            after=1484811043508,
            before=0,
            limit=10,
        )
        assert_matches_type(AsyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_recently_played(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.list_recently_played()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert_matches_type(AsyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_recently_played(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.list_recently_played() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert_matches_type(AsyncCursorURLPage[PlayerListRecentlyPlayedResponse], player, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_pause_playback(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.pause_playback()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_pause_playback_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.pause_playback(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_pause_playback(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.pause_playback()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_pause_playback(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.pause_playback() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_seek_to_position(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.seek_to_position(
            position_ms=25000,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_seek_to_position_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.seek_to_position(
            position_ms=25000,
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_seek_to_position(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.seek_to_position(
            position_ms=25000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_seek_to_position(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.seek_to_position(
            position_ms=25000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_set_repeat_mode(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.set_repeat_mode(
            state="context",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_set_repeat_mode_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.set_repeat_mode(
            state="context",
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_set_repeat_mode(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.set_repeat_mode(
            state="context",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_set_repeat_mode(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.set_repeat_mode(
            state="context",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_set_volume(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.set_volume(
            volume_percent=50,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_set_volume_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.set_volume(
            volume_percent=50,
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_set_volume(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.set_volume(
            volume_percent=50,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_set_volume(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.set_volume(
            volume_percent=50,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_skip_next(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.skip_next()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_skip_next_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.skip_next(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_skip_next(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.skip_next()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_skip_next(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.skip_next() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_skip_previous(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.skip_previous()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_skip_previous_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.skip_previous(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_skip_previous(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.skip_previous()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_skip_previous(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.skip_previous() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_playback(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.start_playback()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_playback_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.start_playback(
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
            context_uri="spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
            offset={"position": "bar"},
            position_ms=0,
            published=True,
            uris=["string"],
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start_playback(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.start_playback()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start_playback(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.start_playback() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_toggle_shuffle(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.toggle_shuffle(
            state=True,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_toggle_shuffle_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.toggle_shuffle(
            state=True,
            device_id="0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_toggle_shuffle(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.toggle_shuffle(
            state=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_toggle_shuffle(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.toggle_shuffle(
            state=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_transfer(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_transfer_with_all_params(self, async_client: AsyncSpotted) -> None:
        player = await async_client.me.player.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
            play=True,
            published=True,
        )
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_transfer(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.player.with_raw_response.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        player = await response.parse()
        assert player is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_transfer(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.player.with_streaming_response.transfer(
            device_ids=["74ASZWbe4lXaubB36ztrGX"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            player = await response.parse()
            assert player is None

        assert cast(Any, response.is_closed) is True
