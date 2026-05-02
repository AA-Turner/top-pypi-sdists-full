# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types.playlists import FollowerCheckResponse

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFollowers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = client.playlists.followers.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(FollowerCheckResponse, follower, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_check_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = client.playlists.followers.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                ids="jmperezperez",
            )

        assert_matches_type(FollowerCheckResponse, follower, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.followers.with_raw_response.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        follower = response.parse()
        assert_matches_type(FollowerCheckResponse, follower, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.followers.with_streaming_response.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                follower = response.parse()
                assert_matches_type(FollowerCheckResponse, follower, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.followers.with_raw_response.check(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = client.playlists.followers.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_follow_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = client.playlists.followers.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                published=True,
            )

        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.followers.with_raw_response.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        follower = response.parse()
        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.followers.with_streaming_response.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                follower = response.parse()
                assert follower is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.followers.with_raw_response.follow(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = client.playlists.followers.unfollow(
                "3cEYpjA9oz9GiPac4AsH4n",
            )

        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.playlists.followers.with_raw_response.unfollow(
                "3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        follower = response.parse()
        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.playlists.followers.with_streaming_response.unfollow(
                "3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                follower = response.parse()
                assert follower is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                client.playlists.followers.with_raw_response.unfollow(
                    "",
                )


class TestAsyncFollowers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = await async_client.playlists.followers.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert_matches_type(FollowerCheckResponse, follower, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_check_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = await async_client.playlists.followers.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                ids="jmperezperez",
            )

        assert_matches_type(FollowerCheckResponse, follower, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.followers.with_raw_response.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        follower = await response.parse()
        assert_matches_type(FollowerCheckResponse, follower, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.followers.with_streaming_response.check(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                follower = await response.parse()
                assert_matches_type(FollowerCheckResponse, follower, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.followers.with_raw_response.check(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = await async_client.playlists.followers.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_follow_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = await async_client.playlists.followers.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
                published=True,
            )

        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.followers.with_raw_response.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        follower = await response.parse()
        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.followers.with_streaming_response.follow(
                playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                follower = await response.parse()
                assert follower is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.followers.with_raw_response.follow(
                    playlist_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            follower = await async_client.playlists.followers.unfollow(
                "3cEYpjA9oz9GiPac4AsH4n",
            )

        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.playlists.followers.with_raw_response.unfollow(
                "3cEYpjA9oz9GiPac4AsH4n",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        follower = await response.parse()
        assert follower is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.playlists.followers.with_streaming_response.unfollow(
                "3cEYpjA9oz9GiPac4AsH4n",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                follower = await response.parse()
                assert follower is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
                await async_client.playlists.followers.with_raw_response.unfollow(
                    "",
                )
