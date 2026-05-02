# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types.me import (
    AlbumListResponse,
    AlbumCheckResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAlbums:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Spotted) -> None:
        album = client.me.albums.list()
        assert_matches_type(SyncCursorURLPage[AlbumListResponse], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Spotted) -> None:
        album = client.me.albums.list(
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SyncCursorURLPage[AlbumListResponse], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Spotted) -> None:
        response = client.me.albums.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert_matches_type(SyncCursorURLPage[AlbumListResponse], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Spotted) -> None:
        with client.me.albums.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            album = response.parse()
            assert_matches_type(SyncCursorURLPage[AlbumListResponse], album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.me.albums.check(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert_matches_type(AlbumCheckResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.albums.with_raw_response.check(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert_matches_type(AlbumCheckResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_check(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.albums.with_streaming_response.check(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = response.parse()
                assert_matches_type(AlbumCheckResponse, album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.me.albums.remove()

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_remove_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.me.albums.remove(
                ids=["string"],
                published=True,
            )

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.albums.with_raw_response.remove()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_remove(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.albums.with_streaming_response.remove() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = response.parse()
                assert album is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_save(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.me.albums.save()

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_save_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.me.albums.save(
                ids=["string"],
                published=True,
            )

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_save(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.me.albums.with_raw_response.save()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_save(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.me.albums.with_streaming_response.save() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = response.parse()
                assert album is None

        assert cast(Any, response.is_closed) is True


class TestAsyncAlbums:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSpotted) -> None:
        album = await async_client.me.albums.list()
        assert_matches_type(AsyncCursorURLPage[AlbumListResponse], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSpotted) -> None:
        album = await async_client.me.albums.list(
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(AsyncCursorURLPage[AlbumListResponse], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSpotted) -> None:
        response = await async_client.me.albums.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert_matches_type(AsyncCursorURLPage[AlbumListResponse], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSpotted) -> None:
        async with async_client.me.albums.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            album = await response.parse()
            assert_matches_type(AsyncCursorURLPage[AlbumListResponse], album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.me.albums.check(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert_matches_type(AlbumCheckResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.albums.with_raw_response.check(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert_matches_type(AlbumCheckResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_check(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.albums.with_streaming_response.check(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = await response.parse()
                assert_matches_type(AlbumCheckResponse, album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.me.albums.remove()

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_remove_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.me.albums.remove(
                ids=["string"],
                published=True,
            )

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.albums.with_raw_response.remove()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.albums.with_streaming_response.remove() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = await response.parse()
                assert album is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_save(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.me.albums.save()

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_save_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.me.albums.save(
                ids=["string"],
                published=True,
            )

        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_save(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.me.albums.with_raw_response.save()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert album is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_save(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.me.albums.with_streaming_response.save() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = await response.parse()
                assert album is None

        assert cast(Any, response.is_closed) is True
