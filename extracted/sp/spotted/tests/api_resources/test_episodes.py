# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import EpisodeBulkRetrieveResponse
from spotted.types.shared import EpisodeObject

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEpisodes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        episode = client.episodes.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
        )
        assert_matches_type(EpisodeObject, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        episode = client.episodes.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
            market="ES",
        )
        assert_matches_type(EpisodeObject, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.episodes.with_raw_response.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        episode = response.parse()
        assert_matches_type(EpisodeObject, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.episodes.with_streaming_response.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            episode = response.parse()
            assert_matches_type(EpisodeObject, episode, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.episodes.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            episode = client.episodes.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
            )

        assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            episode = client.episodes.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
                market="ES",
            )

        assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.episodes.with_raw_response.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        episode = response.parse()
        assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.episodes.with_streaming_response.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                episode = response.parse()
                assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEpisodes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        episode = await async_client.episodes.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
        )
        assert_matches_type(EpisodeObject, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        episode = await async_client.episodes.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
            market="ES",
        )
        assert_matches_type(EpisodeObject, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.episodes.with_raw_response.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        episode = await response.parse()
        assert_matches_type(EpisodeObject, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.episodes.with_streaming_response.retrieve(
            id="512ojhOuo1ktJprKbVcKyQ",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            episode = await response.parse()
            assert_matches_type(EpisodeObject, episode, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.episodes.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            episode = await async_client.episodes.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
            )

        assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            episode = await async_client.episodes.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
                market="ES",
            )

        assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.episodes.with_raw_response.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        episode = await response.parse()
        assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.episodes.with_streaming_response.bulk_retrieve(
                ids="77o6BIVlYM3msb4MMIL1jH,0Q86acNRm6V9GYx55SXKwf",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                episode = await response.parse()
                assert_matches_type(EpisodeBulkRetrieveResponse, episode, path=["response"])

        assert cast(Any, response.is_closed) is True
