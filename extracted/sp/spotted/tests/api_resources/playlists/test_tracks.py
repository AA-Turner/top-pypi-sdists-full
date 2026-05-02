# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.shared import PlaylistTrackObject
from spotted.types.playlists import (
    TrackAddResponse,
    TrackRemoveResponse,
    TrackUpdateResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTracks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(TrackUpdateResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                insert_before=3,
                published=True,
                range_length=2,
                range_start=1,
                snapshot_id="snapshot_id",
                uris=["string"],
            )

        assert_matches_type(TrackUpdateResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.tracks.with_raw_response.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackUpdateResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.tracks.with_streaming_response.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert_matches_type(TrackUpdateResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.tracks.with_raw_response.update(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(SyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                additional_types="additional_types",
                fields="items(added_by.id,track(name,href,album(name,href)))",
                limit=10,
                market="ES",
                offset=5,
            )

        assert_matches_type(SyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.tracks.with_raw_response.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(SyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.tracks.with_streaming_response.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert_matches_type(SyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.tracks.with_raw_response.list(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(TrackAddResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                position=0,
                published=True,
                uris=["string"],
            )

        assert_matches_type(TrackAddResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_add(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.tracks.with_raw_response.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackAddResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_add(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.tracks.with_streaming_response.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert_matches_type(TrackAddResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_add(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.tracks.with_raw_response.add(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{}],
            )

        assert_matches_type(TrackRemoveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_remove_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.playlists.tracks.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{"uri": "uri"}],
                published=True,
                snapshot_id="snapshot_id",
            )

        assert_matches_type(TrackRemoveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.tracks.with_raw_response.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{}],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackRemoveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.tracks.with_streaming_response.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{}],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert_matches_type(TrackRemoveResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.tracks.with_raw_response.remove(
                    playlist_id="",
                    tracks=[{}],
                )


class TestAsyncTracks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(TrackUpdateResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                insert_before=3,
                published=True,
                range_length=2,
                range_start=1,
                snapshot_id="snapshot_id",
                uris=["string"],
            )

        assert_matches_type(TrackUpdateResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.tracks.with_raw_response.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackUpdateResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.tracks.with_streaming_response.update(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert_matches_type(TrackUpdateResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.tracks.with_raw_response.update(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(AsyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                additional_types="additional_types",
                fields="items(added_by.id,track(name,href,album(name,href)))",
                limit=10,
                market="ES",
                offset=5,
            )

        assert_matches_type(AsyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.tracks.with_raw_response.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(AsyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.tracks.with_streaming_response.list(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert_matches_type(AsyncCursorURLPage[PlaylistTrackObject], track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.tracks.with_raw_response.list(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(TrackAddResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                position=0,
                published=True,
                uris=["string"],
            )

        assert_matches_type(TrackAddResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.tracks.with_raw_response.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackAddResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.tracks.with_streaming_response.add(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert_matches_type(TrackAddResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_add(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.tracks.with_raw_response.add(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{}],
            )

        assert_matches_type(TrackRemoveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_remove_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.playlists.tracks.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{"uri": "uri"}],
                published=True,
                snapshot_id="snapshot_id",
            )

        assert_matches_type(TrackRemoveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.tracks.with_raw_response.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{}],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackRemoveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.tracks.with_streaming_response.remove(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                tracks=[{}],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert_matches_type(TrackRemoveResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.tracks.with_raw_response.remove(
                    playlist_id="",
                    tracks=[{}],
                )
