# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import TrackBulkRetrieveResponse
from spotted.types.shared import TrackObject

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTracks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        track = client.tracks.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
        )
        assert_matches_type(TrackObject, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        track = client.tracks.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
            market="ES",
        )
        assert_matches_type(TrackObject, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.tracks.with_raw_response.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackObject, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.tracks.with_streaming_response.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            track = response.parse()
            assert_matches_type(TrackObject, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.tracks.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.tracks.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = client.tracks.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
                market="ES",
            )

        assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.tracks.with_raw_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.tracks.with_streaming_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = response.parse()
                assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTracks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        track = await async_client.tracks.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
        )
        assert_matches_type(TrackObject, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        track = await async_client.tracks.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
            market="ES",
        )
        assert_matches_type(TrackObject, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.tracks.with_raw_response.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackObject, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.tracks.with_streaming_response.retrieve(
            id="11dFghVXANMlKmJXsNCbNl",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            track = await response.parse()
            assert_matches_type(TrackObject, track, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.tracks.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.tracks.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            track = await async_client.tracks.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
                market="ES",
            )

        assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.tracks.with_raw_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.tracks.with_streaming_response.bulk_retrieve(
                ids="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                track = await response.parse()
                assert_matches_type(TrackBulkRetrieveResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True
