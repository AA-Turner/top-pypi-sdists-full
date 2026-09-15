# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from supermemory import Supermemory, AsyncSupermemory
from tests.utils import assert_matches_type
from supermemory.types import SettingGetResponse, SettingUpdateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSettings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Supermemory) -> None:
        setting = client.settings.update()
        assert_matches_type(SettingUpdateResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Supermemory) -> None:
        setting = client.settings.update(
            chunk_size=-2147483648,
            exclude_items="string",
            filter_prompt="filterPrompt",
            github_client_id="githubClientId",
            github_client_secret="githubClientSecret",
            github_custom_key_enabled=True,
            google_drive_client_id="googleDriveClientId",
            google_drive_client_secret="googleDriveClientSecret",
            google_drive_custom_key_enabled=True,
            include_items="string",
            notion_client_id="notionClientId",
            notion_client_secret="notionClientSecret",
            notion_custom_key_enabled=True,
            onedrive_client_id="onedriveClientId",
            onedrive_client_secret="onedriveClientSecret",
            onedrive_custom_key_enabled=True,
            profile_buckets=[
                {
                    "key": "key",
                    "description": "description",
                }
            ],
            should_llm_filter=True,
        )
        assert_matches_type(SettingUpdateResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Supermemory) -> None:
        response = client.settings.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        setting = response.parse()
        assert_matches_type(SettingUpdateResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Supermemory) -> None:
        with client.settings.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            setting = response.parse()
            assert_matches_type(SettingUpdateResponse, setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get(self, client: Supermemory) -> None:
        setting = client.settings.get()
        assert_matches_type(SettingGetResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get(self, client: Supermemory) -> None:
        response = client.settings.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        setting = response.parse()
        assert_matches_type(SettingGetResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get(self, client: Supermemory) -> None:
        with client.settings.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            setting = response.parse()
            assert_matches_type(SettingGetResponse, setting, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSettings:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncSupermemory) -> None:
        setting = await async_client.settings.update()
        assert_matches_type(SettingUpdateResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSupermemory) -> None:
        setting = await async_client.settings.update(
            chunk_size=-2147483648,
            exclude_items="string",
            filter_prompt="filterPrompt",
            github_client_id="githubClientId",
            github_client_secret="githubClientSecret",
            github_custom_key_enabled=True,
            google_drive_client_id="googleDriveClientId",
            google_drive_client_secret="googleDriveClientSecret",
            google_drive_custom_key_enabled=True,
            include_items="string",
            notion_client_id="notionClientId",
            notion_client_secret="notionClientSecret",
            notion_custom_key_enabled=True,
            onedrive_client_id="onedriveClientId",
            onedrive_client_secret="onedriveClientSecret",
            onedrive_custom_key_enabled=True,
            profile_buckets=[
                {
                    "key": "key",
                    "description": "description",
                }
            ],
            should_llm_filter=True,
        )
        assert_matches_type(SettingUpdateResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.settings.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        setting = await response.parse()
        assert_matches_type(SettingUpdateResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSupermemory) -> None:
        async with async_client.settings.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            setting = await response.parse()
            assert_matches_type(SettingUpdateResponse, setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get(self, async_client: AsyncSupermemory) -> None:
        setting = await async_client.settings.get()
        assert_matches_type(SettingGetResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.settings.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        setting = await response.parse()
        assert_matches_type(SettingGetResponse, setting, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSupermemory) -> None:
        async with async_client.settings.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            setting = await response.parse()
            assert_matches_type(SettingGetResponse, setting, path=["response"])

        assert cast(Any, response.is_closed) is True
