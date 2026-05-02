# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    ChapterRetrieveResponse,
    ChapterBulkRetrieveResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChapters:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        chapter = client.chapters.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
        )
        assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        chapter = client.chapters.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
            market="ES",
        )
        assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.chapters.with_raw_response.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chapter = response.parse()
        assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.chapters.with_streaming_response.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chapter = response.parse()
            assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.chapters.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            chapter = client.chapters.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
            )

        assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            chapter = client.chapters.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
                market="ES",
            )

        assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.chapters.with_raw_response.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chapter = response.parse()
        assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.chapters.with_streaming_response.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                chapter = response.parse()
                assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChapters:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        chapter = await async_client.chapters.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
        )
        assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        chapter = await async_client.chapters.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
            market="ES",
        )
        assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.chapters.with_raw_response.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chapter = await response.parse()
        assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.chapters.with_streaming_response.retrieve(
            id="0D5wENdkdwbqlrHoaJ9g29",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chapter = await response.parse()
            assert_matches_type(ChapterRetrieveResponse, chapter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.chapters.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            chapter = await async_client.chapters.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
            )

        assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            chapter = await async_client.chapters.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
                market="ES",
            )

        assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.chapters.with_raw_response.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chapter = await response.parse()
        assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.chapters.with_streaming_response.bulk_retrieve(
                ids="0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU,0D5wENdkdwbqlrHoaJ9g29",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                chapter = await response.parse()
                assert_matches_type(ChapterBulkRetrieveResponse, chapter, path=["response"])

        assert cast(Any, response.is_closed) is True
