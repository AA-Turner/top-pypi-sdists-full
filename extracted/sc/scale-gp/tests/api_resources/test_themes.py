# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import Theme
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThemes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        theme = client.themes.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={},
            title="title",
        )
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        theme = client.themes.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={
                "accent_primary": "accentPrimary",
                "accent_secondary": "accentSecondary",
                "background": "background",
                "foreground": "foreground",
            },
            title="title",
        )
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.themes.with_raw_response.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={},
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = response.parse()
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.themes.with_streaming_response.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={},
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = response.parse()
            assert_matches_type(Theme, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        theme = client.themes.retrieve(
            "theme_id",
        )
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.themes.with_raw_response.retrieve(
            "theme_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = response.parse()
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.themes.with_streaming_response.retrieve(
            "theme_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = response.parse()
            assert_matches_type(Theme, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `theme_id` but received ''"):
            client.themes.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        theme = client.themes.list()
        assert_matches_type(SyncPageResponse[Theme], theme, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        theme = client.themes.list(
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[Theme], theme, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.themes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = response.parse()
        assert_matches_type(SyncPageResponse[Theme], theme, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.themes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = response.parse()
            assert_matches_type(SyncPageResponse[Theme], theme, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncThemes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        theme = await async_client.themes.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={},
            title="title",
        )
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        theme = await async_client.themes.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={
                "accent_primary": "accentPrimary",
                "accent_secondary": "accentSecondary",
                "background": "background",
                "foreground": "foreground",
            },
            title="title",
        )
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.themes.with_raw_response.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={},
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = await response.parse()
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.themes.with_streaming_response.create(
            account_id="account_id",
            logo_blob="logo_blob",
            theme_vars={},
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = await response.parse()
            assert_matches_type(Theme, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        theme = await async_client.themes.retrieve(
            "theme_id",
        )
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.themes.with_raw_response.retrieve(
            "theme_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = await response.parse()
        assert_matches_type(Theme, theme, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.themes.with_streaming_response.retrieve(
            "theme_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = await response.parse()
            assert_matches_type(Theme, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `theme_id` but received ''"):
            await async_client.themes.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        theme = await async_client.themes.list()
        assert_matches_type(AsyncPageResponse[Theme], theme, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        theme = await async_client.themes.list(
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[Theme], theme, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.themes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = await response.parse()
        assert_matches_type(AsyncPageResponse[Theme], theme, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.themes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = await response.parse()
            assert_matches_type(AsyncPageResponse[Theme], theme, path=["response"])

        assert cast(Any, response.is_closed) is True
