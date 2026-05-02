# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.browse import (
    CategoryListResponse,
    CategoryRetrieveResponse,
    CategoryGetPlaylistsResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCategories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = client.browse.categories.retrieve(
                category_id="dinner",
            )

        assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = client.browse.categories.retrieve(
                category_id="dinner",
                locale="sv_SE",
            )

        assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.browse.categories.with_raw_response.retrieve(
                category_id="dinner",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.browse.categories.with_streaming_response.retrieve(
                category_id="dinner",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                category = response.parse()
                assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
                client.browse.categories.with_raw_response.retrieve(
                    category_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = client.browse.categories.list()

        assert_matches_type(SyncCursorURLPage[CategoryListResponse], category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = client.browse.categories.list(
                limit=10,
                locale="sv_SE",
                offset=5,
            )

        assert_matches_type(SyncCursorURLPage[CategoryListResponse], category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.browse.categories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(SyncCursorURLPage[CategoryListResponse], category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.browse.categories.with_streaming_response.list() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                category = response.parse()
                assert_matches_type(SyncCursorURLPage[CategoryListResponse], category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = client.browse.categories.get_playlists(
                category_id="dinner",
            )

        assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_playlists_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = client.browse.categories.get_playlists(
                category_id="dinner",
                limit=10,
                offset=5,
            )

        assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.browse.categories.with_raw_response.get_playlists(
                category_id="dinner",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.browse.categories.with_streaming_response.get_playlists(
                category_id="dinner",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                category = response.parse()
                assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_get_playlists(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
                client.browse.categories.with_raw_response.get_playlists(
                    category_id="",
                )


class TestAsyncCategories:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = await async_client.browse.categories.retrieve(
                category_id="dinner",
            )

        assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = await async_client.browse.categories.retrieve(
                category_id="dinner",
                locale="sv_SE",
            )

        assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.browse.categories.with_raw_response.retrieve(
                category_id="dinner",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.browse.categories.with_streaming_response.retrieve(
                category_id="dinner",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                category = await response.parse()
                assert_matches_type(CategoryRetrieveResponse, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
                await async_client.browse.categories.with_raw_response.retrieve(
                    category_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = await async_client.browse.categories.list()

        assert_matches_type(AsyncCursorURLPage[CategoryListResponse], category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = await async_client.browse.categories.list(
                limit=10,
                locale="sv_SE",
                offset=5,
            )

        assert_matches_type(AsyncCursorURLPage[CategoryListResponse], category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.browse.categories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(AsyncCursorURLPage[CategoryListResponse], category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.browse.categories.with_streaming_response.list() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                category = await response.parse()
                assert_matches_type(AsyncCursorURLPage[CategoryListResponse], category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = await async_client.browse.categories.get_playlists(
                category_id="dinner",
            )

        assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_playlists_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            category = await async_client.browse.categories.get_playlists(
                category_id="dinner",
                limit=10,
                offset=5,
            )

        assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.browse.categories.with_raw_response.get_playlists(
                category_id="dinner",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.browse.categories.with_streaming_response.get_playlists(
                category_id="dinner",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                category = await response.parse()
                assert_matches_type(CategoryGetPlaylistsResponse, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_get_playlists(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
                await async_client.browse.categories.with_raw_response.get_playlists(
                    category_id="",
                )
