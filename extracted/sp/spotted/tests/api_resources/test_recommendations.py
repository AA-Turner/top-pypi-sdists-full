# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    RecommendationGetResponse,
    RecommendationListAvailableGenreSeedsResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRecommendations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            recommendation = client.recommendations.get()

        assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            recommendation = client.recommendations.get(
                limit=10,
                market="ES",
                max_acousticness=0,
                max_danceability=0,
                max_duration_ms=0,
                max_energy=0,
                max_instrumentalness=0,
                max_key=0,
                max_liveness=0,
                max_loudness=0,
                max_mode=0,
                max_popularity=0,
                max_speechiness=0,
                max_tempo=0,
                max_time_signature=0,
                max_valence=0,
                min_acousticness=0,
                min_danceability=0,
                min_duration_ms=0,
                min_energy=0,
                min_instrumentalness=0,
                min_key=0,
                min_liveness=0,
                min_loudness=0,
                min_mode=0,
                min_popularity=0,
                min_speechiness=0,
                min_tempo=0,
                min_time_signature=11,
                min_valence=0,
                seed_artists="4NHQUGzhtTLFvgF5SZesLK",
                seed_genres="classical,country",
                seed_tracks="0c6xIDDpzE81m2q797ordA",
                target_acousticness=0,
                target_danceability=0,
                target_duration_ms=0,
                target_energy=0,
                target_instrumentalness=0,
                target_key=0,
                target_liveness=0,
                target_loudness=0,
                target_mode=0,
                target_popularity=0,
                target_speechiness=0,
                target_tempo=0,
                target_time_signature=0,
                target_valence=0,
            )

        assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.recommendations.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        recommendation = response.parse()
        assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.recommendations.with_streaming_response.get() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                recommendation = response.parse()
                assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_available_genre_seeds(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            recommendation = client.recommendations.list_available_genre_seeds()

        assert_matches_type(RecommendationListAvailableGenreSeedsResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_available_genre_seeds(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.recommendations.with_raw_response.list_available_genre_seeds()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        recommendation = response.parse()
        assert_matches_type(RecommendationListAvailableGenreSeedsResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_available_genre_seeds(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.recommendations.with_streaming_response.list_available_genre_seeds() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                recommendation = response.parse()
                assert_matches_type(RecommendationListAvailableGenreSeedsResponse, recommendation, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRecommendations:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            recommendation = await async_client.recommendations.get()

        assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            recommendation = await async_client.recommendations.get(
                limit=10,
                market="ES",
                max_acousticness=0,
                max_danceability=0,
                max_duration_ms=0,
                max_energy=0,
                max_instrumentalness=0,
                max_key=0,
                max_liveness=0,
                max_loudness=0,
                max_mode=0,
                max_popularity=0,
                max_speechiness=0,
                max_tempo=0,
                max_time_signature=0,
                max_valence=0,
                min_acousticness=0,
                min_danceability=0,
                min_duration_ms=0,
                min_energy=0,
                min_instrumentalness=0,
                min_key=0,
                min_liveness=0,
                min_loudness=0,
                min_mode=0,
                min_popularity=0,
                min_speechiness=0,
                min_tempo=0,
                min_time_signature=11,
                min_valence=0,
                seed_artists="4NHQUGzhtTLFvgF5SZesLK",
                seed_genres="classical,country",
                seed_tracks="0c6xIDDpzE81m2q797ordA",
                target_acousticness=0,
                target_danceability=0,
                target_duration_ms=0,
                target_energy=0,
                target_instrumentalness=0,
                target_key=0,
                target_liveness=0,
                target_loudness=0,
                target_mode=0,
                target_popularity=0,
                target_speechiness=0,
                target_tempo=0,
                target_time_signature=0,
                target_valence=0,
            )

        assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.recommendations.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        recommendation = await response.parse()
        assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.recommendations.with_streaming_response.get() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                recommendation = await response.parse()
                assert_matches_type(RecommendationGetResponse, recommendation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_available_genre_seeds(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            recommendation = await async_client.recommendations.list_available_genre_seeds()

        assert_matches_type(RecommendationListAvailableGenreSeedsResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_available_genre_seeds(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.recommendations.with_raw_response.list_available_genre_seeds()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        recommendation = await response.parse()
        assert_matches_type(RecommendationListAvailableGenreSeedsResponse, recommendation, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_available_genre_seeds(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.recommendations.with_streaming_response.list_available_genre_seeds() as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                recommendation = await response.parse()
                assert_matches_type(RecommendationListAvailableGenreSeedsResponse, recommendation, path=["response"])

        assert cast(Any, response.is_closed) is True
