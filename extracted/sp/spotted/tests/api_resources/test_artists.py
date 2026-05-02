# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    ArtistTopTracksResponse,
    ArtistListAlbumsResponse,
    ArtistBulkRetrieveResponse,
    ArtistListRelatedArtistsResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.shared import ArtistObject

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArtists:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        artist = client.artists.retrieve(
            "0TnOYISbd1XYRBk9myaseg",
        )
        assert_matches_type(ArtistObject, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.artists.with_raw_response.retrieve(
            "0TnOYISbd1XYRBk9myaseg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = response.parse()
        assert_matches_type(ArtistObject, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.artists.with_streaming_response.retrieve(
            "0TnOYISbd1XYRBk9myaseg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artist = response.parse()
            assert_matches_type(ArtistObject, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.artists.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = client.artists.bulk_retrieve(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
            )

        assert_matches_type(ArtistBulkRetrieveResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.artists.with_raw_response.bulk_retrieve(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = response.parse()
        assert_matches_type(ArtistBulkRetrieveResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.artists.with_streaming_response.bulk_retrieve(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                artist = response.parse()
                assert_matches_type(ArtistBulkRetrieveResponse, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_albums(self, client: Spotted) -> None:
        artist = client.artists.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
        )
        assert_matches_type(SyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_albums_with_all_params(self, client: Spotted) -> None:
        artist = client.artists.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
            include_groups="single,appears_on",
            limit=5,
            market="ES",
            offset=5,
        )
        assert_matches_type(SyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_albums(self, client: Spotted) -> None:
        response = client.artists.with_raw_response.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = response.parse()
        assert_matches_type(SyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_albums(self, client: Spotted) -> None:
        with client.artists.with_streaming_response.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artist = response.parse()
            assert_matches_type(SyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_albums(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.artists.with_raw_response.list_albums(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_related_artists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = client.artists.list_related_artists(
                "0TnOYISbd1XYRBk9myaseg",
            )

        assert_matches_type(ArtistListRelatedArtistsResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_related_artists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.artists.with_raw_response.list_related_artists(
                "0TnOYISbd1XYRBk9myaseg",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = response.parse()
        assert_matches_type(ArtistListRelatedArtistsResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_related_artists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.artists.with_streaming_response.list_related_artists(
                "0TnOYISbd1XYRBk9myaseg",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                artist = response.parse()
                assert_matches_type(ArtistListRelatedArtistsResponse, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_related_artists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                client.artists.with_raw_response.list_related_artists(
                    "",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_top_tracks(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = client.artists.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
            )

        assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_top_tracks_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = client.artists.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
                market="ES",
            )

        assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_top_tracks(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.artists.with_raw_response.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = response.parse()
        assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_top_tracks(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.artists.with_streaming_response.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                artist = response.parse()
                assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_top_tracks(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                client.artists.with_raw_response.top_tracks(
                    id="",
                )


class TestAsyncArtists:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        artist = await async_client.artists.retrieve(
            "0TnOYISbd1XYRBk9myaseg",
        )
        assert_matches_type(ArtistObject, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.artists.with_raw_response.retrieve(
            "0TnOYISbd1XYRBk9myaseg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = await response.parse()
        assert_matches_type(ArtistObject, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.artists.with_streaming_response.retrieve(
            "0TnOYISbd1XYRBk9myaseg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artist = await response.parse()
            assert_matches_type(ArtistObject, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.artists.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = await async_client.artists.bulk_retrieve(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
            )

        assert_matches_type(ArtistBulkRetrieveResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.artists.with_raw_response.bulk_retrieve(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = await response.parse()
        assert_matches_type(ArtistBulkRetrieveResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.artists.with_streaming_response.bulk_retrieve(
                ids="2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                artist = await response.parse()
                assert_matches_type(ArtistBulkRetrieveResponse, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_albums(self, async_client: AsyncSpotted) -> None:
        artist = await async_client.artists.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
        )
        assert_matches_type(AsyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_albums_with_all_params(self, async_client: AsyncSpotted) -> None:
        artist = await async_client.artists.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
            include_groups="single,appears_on",
            limit=5,
            market="ES",
            offset=5,
        )
        assert_matches_type(AsyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_albums(self, async_client: AsyncSpotted) -> None:
        response = await async_client.artists.with_raw_response.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = await response.parse()
        assert_matches_type(AsyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_albums(self, async_client: AsyncSpotted) -> None:
        async with async_client.artists.with_streaming_response.list_albums(
            id="0TnOYISbd1XYRBk9myaseg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artist = await response.parse()
            assert_matches_type(AsyncCursorURLPage[ArtistListAlbumsResponse], artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_albums(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.artists.with_raw_response.list_albums(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_related_artists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = await async_client.artists.list_related_artists(
                "0TnOYISbd1XYRBk9myaseg",
            )

        assert_matches_type(ArtistListRelatedArtistsResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_related_artists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.artists.with_raw_response.list_related_artists(
                "0TnOYISbd1XYRBk9myaseg",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = await response.parse()
        assert_matches_type(ArtistListRelatedArtistsResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_related_artists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.artists.with_streaming_response.list_related_artists(
                "0TnOYISbd1XYRBk9myaseg",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                artist = await response.parse()
                assert_matches_type(ArtistListRelatedArtistsResponse, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_related_artists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                await async_client.artists.with_raw_response.list_related_artists(
                    "",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_top_tracks(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = await async_client.artists.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
            )

        assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_top_tracks_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            artist = await async_client.artists.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
                market="ES",
            )

        assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_top_tracks(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.artists.with_raw_response.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artist = await response.parse()
        assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_top_tracks(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.artists.with_streaming_response.top_tracks(
                id="0TnOYISbd1XYRBk9myaseg",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                artist = await response.parse()
                assert_matches_type(ArtistTopTracksResponse, artist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_top_tracks(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                await async_client.artists.with_raw_response.top_tracks(
                    id="",
                )
