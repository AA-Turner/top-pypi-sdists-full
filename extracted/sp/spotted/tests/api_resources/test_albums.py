# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    AlbumRetrieveResponse,
    AlbumBulkRetrieveResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.shared import SimplifiedTrackObject

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAlbums:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        album = client.albums.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )
        assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        album = client.albums.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
            market="ES",
        )
        assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.albums.with_raw_response.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.albums.with_streaming_response.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            album = response.parse()
            assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.albums.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.albums.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = client.albums.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
                market="ES",
            )

        assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.albums.with_raw_response.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.albums.with_streaming_response.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = response.parse()
                assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_tracks(self, client: Spotted) -> None:
        album = client.albums.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )
        assert_matches_type(SyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_tracks_with_all_params(self, client: Spotted) -> None:
        album = client.albums.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_tracks(self, client: Spotted) -> None:
        response = client.albums.with_raw_response.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = response.parse()
        assert_matches_type(SyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_tracks(self, client: Spotted) -> None:
        with client.albums.with_streaming_response.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            album = response.parse()
            assert_matches_type(SyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_tracks(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.albums.with_raw_response.list_tracks(
                id="",
            )


class TestAsyncAlbums:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        album = await async_client.albums.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )
        assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        album = await async_client.albums.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
            market="ES",
        )
        assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.albums.with_raw_response.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.albums.with_streaming_response.retrieve(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            album = await response.parse()
            assert_matches_type(AlbumRetrieveResponse, album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.albums.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.albums.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            album = await async_client.albums.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
                market="ES",
            )

        assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.albums.with_raw_response.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.albums.with_streaming_response.bulk_retrieve(
                ids="382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                album = await response.parse()
                assert_matches_type(AlbumBulkRetrieveResponse, album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_tracks(self, async_client: AsyncSpotted) -> None:
        album = await async_client.albums.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )
        assert_matches_type(AsyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_tracks_with_all_params(self, async_client: AsyncSpotted) -> None:
        album = await async_client.albums.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(AsyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_tracks(self, async_client: AsyncSpotted) -> None:
        response = await async_client.albums.with_raw_response.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        album = await response.parse()
        assert_matches_type(AsyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_tracks(self, async_client: AsyncSpotted) -> None:
        async with async_client.albums.with_streaming_response.list_tracks(
            id="4aawyAB9vmqN3uQ7FjRGTy",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            album = await response.parse()
            assert_matches_type(AsyncCursorURLPage[SimplifiedTrackObject], album, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_tracks(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.albums.with_raw_response.list_tracks(
                id="",
            )
