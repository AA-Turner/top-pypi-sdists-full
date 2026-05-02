# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    SimplifiedChapterObject,
    AudiobookRetrieveResponse,
    AudiobookBulkRetrieveResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAudiobooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        audiobook = client.audiobooks.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )
        assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        audiobook = client.audiobooks.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
            market="ES",
        )
        assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.audiobooks.with_raw_response.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audiobook = response.parse()
        assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.audiobooks.with_streaming_response.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audiobook = response.parse()
            assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.audiobooks.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            audiobook = client.audiobooks.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
            )

        assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            audiobook = client.audiobooks.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
                market="ES",
            )

        assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.audiobooks.with_raw_response.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audiobook = response.parse()
        assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.audiobooks.with_streaming_response.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                audiobook = response.parse()
                assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_chapters(self, client: Spotted) -> None:
        audiobook = client.audiobooks.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )
        assert_matches_type(SyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_chapters_with_all_params(self, client: Spotted) -> None:
        audiobook = client.audiobooks.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_chapters(self, client: Spotted) -> None:
        response = client.audiobooks.with_raw_response.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audiobook = response.parse()
        assert_matches_type(SyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_chapters(self, client: Spotted) -> None:
        with client.audiobooks.with_streaming_response.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audiobook = response.parse()
            assert_matches_type(SyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_chapters(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.audiobooks.with_raw_response.list_chapters(
                id="",
            )


class TestAsyncAudiobooks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        audiobook = await async_client.audiobooks.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )
        assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        audiobook = await async_client.audiobooks.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
            market="ES",
        )
        assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.audiobooks.with_raw_response.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audiobook = await response.parse()
        assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.audiobooks.with_streaming_response.retrieve(
            id="7iHfbu1YPACw6oZPAFJtqe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audiobook = await response.parse()
            assert_matches_type(AudiobookRetrieveResponse, audiobook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.audiobooks.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            audiobook = await async_client.audiobooks.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
            )

        assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            audiobook = await async_client.audiobooks.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
                market="ES",
            )

        assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.audiobooks.with_raw_response.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audiobook = await response.parse()
        assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.audiobooks.with_streaming_response.bulk_retrieve(
                ids="18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ,7iHfbu1YPACw6oZPAFJtqe",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                audiobook = await response.parse()
                assert_matches_type(AudiobookBulkRetrieveResponse, audiobook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_chapters(self, async_client: AsyncSpotted) -> None:
        audiobook = await async_client.audiobooks.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )
        assert_matches_type(AsyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_chapters_with_all_params(self, async_client: AsyncSpotted) -> None:
        audiobook = await async_client.audiobooks.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(AsyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_chapters(self, async_client: AsyncSpotted) -> None:
        response = await async_client.audiobooks.with_raw_response.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audiobook = await response.parse()
        assert_matches_type(AsyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_chapters(self, async_client: AsyncSpotted) -> None:
        async with async_client.audiobooks.with_streaming_response.list_chapters(
            id="7iHfbu1YPACw6oZPAFJtqe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audiobook = await response.parse()
            assert_matches_type(AsyncCursorURLPage[SimplifiedChapterObject], audiobook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_chapters(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.audiobooks.with_raw_response.list_chapters(
                id="",
            )
