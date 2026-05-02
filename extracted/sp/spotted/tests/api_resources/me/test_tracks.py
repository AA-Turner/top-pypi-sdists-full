# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted._utils import parse_datetime
from spotted.types.me import (
    TrackListResponse,
    TrackCheckResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTracks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Spotted) -> None:
        track = client.me.tracks.list()
        assert_matches_type(SyncCursorURLPage[TrackListResponse], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Spotted) -> None:
        track = client.me.tracks.list(
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SyncCursorURLPage[TrackListResponse], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Spotted) -> None:
        response = client.me.tracks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(SyncCursorURLPage[TrackListResponse], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Spotted) -> None:
        with client.me.tracks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            track = response.parse()
            assert_matches_type(SyncCursorURLPage[TrackListResponse], track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.me.tracks.check(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert_matches_type(TrackCheckResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.tracks.with_raw_response.check(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackCheckResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.tracks.with_streaming_response.check(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert_matches_type(TrackCheckResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.me.tracks.remove()

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_remove_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.me.tracks.remove(
                ids=["string"],
                published=True,
            )

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.tracks.with_raw_response.remove()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.tracks.with_streaming_response.remove() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert track is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_save(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.me.tracks.save(
                ids=["string"],
            )

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_save_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.me.tracks.save(
                ids=["string"],
                published=True,
                timestamped_ids=[
                    {
                        "id": "id",
                        "added_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            )

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_save(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.tracks.with_raw_response.save(
                ids=["string"],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_save(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.tracks.with_streaming_response.save(
                ids=["string"],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert track is None

        assert cast(Any, response.is_closed) is True


class TestAsyncTracks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSpotted) -> None:
        track = await async_client.me.tracks.list()
        assert_matches_type(AsyncCursorURLPage[TrackListResponse], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSpotted) -> None:
        track = await async_client.me.tracks.list(
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(AsyncCursorURLPage[TrackListResponse], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.tracks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(AsyncCursorURLPage[TrackListResponse], track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.tracks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            track = await response.parse()
            assert_matches_type(AsyncCursorURLPage[TrackListResponse], track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.me.tracks.check(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert_matches_type(TrackCheckResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.tracks.with_raw_response.check(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackCheckResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.tracks.with_streaming_response.check(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert_matches_type(TrackCheckResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.me.tracks.remove()

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_remove_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.me.tracks.remove(
                ids=["string"],
                published=True,
            )

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.tracks.with_raw_response.remove()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.tracks.with_streaming_response.remove() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert track is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_save(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.me.tracks.save(
                ids=["string"],
            )

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_save_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.me.tracks.save(
                ids=["string"],
                published=True,
                timestamped_ids=[
                    {
                        "id": "id",
                        "added_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            )

        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_save(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.tracks.with_raw_response.save(
                ids=["string"],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert track is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_save(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.tracks.with_streaming_response.save(
                ids=["string"],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert track is None

        assert cast(Any, response.is_closed) is True
