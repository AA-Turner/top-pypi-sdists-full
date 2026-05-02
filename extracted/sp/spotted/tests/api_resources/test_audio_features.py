# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    AudioFeatureRetrieveResponse,
    AudioFeatureBulkRetrieveResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAudioFeatures:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            audio_feature = client.audio_features.retrieve(
                "11dFghVXANMlKmJXsNCbNl",
            )

        assert_matches_type(AudioFeatureRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.audio_features.with_raw_response.retrieve(
                "11dFghVXANMlKmJXsNCbNl",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audio_feature = response.parse()
        assert_matches_type(AudioFeatureRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.audio_features.with_streaming_response.retrieve(
                "11dFghVXANMlKmJXsNCbNl",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                audio_feature = response.parse()
                assert_matches_type(AudioFeatureRetrieveResponse, audio_feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                client.audio_features.with_raw_response.retrieve(
                    "",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            audio_feature = client.audio_features.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert_matches_type(AudioFeatureBulkRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.audio_features.with_raw_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audio_feature = response.parse()
        assert_matches_type(AudioFeatureBulkRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.audio_features.with_streaming_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                audio_feature = response.parse()
                assert_matches_type(AudioFeatureBulkRetrieveResponse, audio_feature, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAudioFeatures:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            audio_feature = await async_client.audio_features.retrieve(
                "11dFghVXANMlKmJXsNCbNl",
            )

        assert_matches_type(AudioFeatureRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.audio_features.with_raw_response.retrieve(
                "11dFghVXANMlKmJXsNCbNl",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audio_feature = await response.parse()
        assert_matches_type(AudioFeatureRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.audio_features.with_streaming_response.retrieve(
                "11dFghVXANMlKmJXsNCbNl",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                audio_feature = await response.parse()
                assert_matches_type(AudioFeatureRetrieveResponse, audio_feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                await async_client.audio_features.with_raw_response.retrieve(
                    "",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            audio_feature = await async_client.audio_features.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert_matches_type(AudioFeatureBulkRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.audio_features.with_raw_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audio_feature = await response.parse()
        assert_matches_type(AudioFeatureBulkRetrieveResponse, audio_feature, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.audio_features.with_streaming_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                audio_feature = await response.parse()
                assert_matches_type(AudioFeatureBulkRetrieveResponse, audio_feature, path=["response"])

        assert cast(Any, response.is_closed) is True
