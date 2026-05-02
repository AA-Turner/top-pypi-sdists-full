# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types.me import (
    FollowingCheckResponse,
    FollowingBulkRetrieveResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFollowing:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        following = client.me.following.bulk_retrieve(
            type="artist",
        )
        assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        following = client.me.following.bulk_retrieve(
            type="artist",
            after="0I2XqVXqHScXjHhk6AYYRe",
            limit=10,
        )
        assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        response = client.me.following.with_raw_response.bulk_retrieve(
            type="artist",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = response.parse()
        assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with client.me.following.with_streaming_response.bulk_retrieve(
            type="artist",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            following = response.parse()
            assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = client.me.following.check(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
                type="artist",
            )

        assert_matches_type(FollowingCheckResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.following.with_raw_response.check(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
                type="artist",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = response.parse()
        assert_matches_type(FollowingCheckResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.following.with_streaming_response.check(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
                type="artist",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                following = response.parse()
                assert_matches_type(FollowingCheckResponse, following, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = client.me.following.follow(
                ids=["string"],
            )

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_follow_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = client.me.following.follow(
                ids=["string"],
                published=True,
            )

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.following.with_raw_response.follow(
                ids=["string"],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = response.parse()
        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_follow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.following.with_streaming_response.follow(
                ids=["string"],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                following = response.parse()
                assert following is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = client.me.following.unfollow()

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_unfollow_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = client.me.following.unfollow(
                ids=["string"],
                published=True,
            )

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.following.with_raw_response.unfollow()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = response.parse()
        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_unfollow(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.following.with_streaming_response.unfollow() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                following = response.parse()
                assert following is None

        assert cast(Any, response.is_closed) is True


class TestAsyncFollowing:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        following = await async_client.me.following.bulk_retrieve(
            type="artist",
        )
        assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        following = await async_client.me.following.bulk_retrieve(
            type="artist",
            after="0I2XqVXqHScXjHhk6AYYRe",
            limit=10,
        )
        assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.following.with_raw_response.bulk_retrieve(
            type="artist",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = await response.parse()
        assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.following.with_streaming_response.bulk_retrieve(
            type="artist",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            following = await response.parse()
            assert_matches_type(FollowingBulkRetrieveResponse, following, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = await async_client.me.following.check(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
                type="artist",
            )

        assert_matches_type(FollowingCheckResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.following.with_raw_response.check(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
                type="artist",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = await response.parse()
        assert_matches_type(FollowingCheckResponse, following, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.following.with_streaming_response.check(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
                type="artist",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                following = await response.parse()
                assert_matches_type(FollowingCheckResponse, following, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = await async_client.me.following.follow(
                ids=["string"],
            )

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_follow_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = await async_client.me.following.follow(
                ids=["string"],
                published=True,
            )

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.following.with_raw_response.follow(
                ids=["string"],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = await response.parse()
        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_follow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.following.with_streaming_response.follow(
                ids=["string"],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                following = await response.parse()
                assert following is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = await async_client.me.following.unfollow()

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_unfollow_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            following = await async_client.me.following.unfollow(
                ids=["string"],
                published=True,
            )

        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.following.with_raw_response.unfollow()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        following = await response.parse()
        assert following is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_unfollow(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.following.with_streaming_response.unfollow() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                following = await response.parse()
                assert following is None

        assert cast(Any, response.is_closed) is True
