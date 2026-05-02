# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted.types import (
    ShowRetrieveResponse,
    ShowBulkRetrieveResponse,
)
from spotted.pagination import SyncCursorURLPage, AsyncCursorURLPage
from spotted.types.shared import SimplifiedEpisodeObject

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestShows:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Spotted) -> None:
        show = client.shows.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )
        assert_matches_type(ShowRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Spotted) -> None:
        show = client.shows.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
            market="ES",
        )
        assert_matches_type(ShowRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Spotted) -> None:
        response = client.shows.with_raw_response.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        show = response.parse()
        assert_matches_type(ShowRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Spotted) -> None:
        with client.shows.with_streaming_response.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            show = response.parse()
            assert_matches_type(ShowRetrieveResponse, show, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.shows.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            show = client.shows.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
            )

        assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_bulk_retrieve_with_all_params(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            show = client.shows.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
                market="ES",
            )

        assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.shows.with_raw_response.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        show = response.parse()
        assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_bulk_retrieve(self, client: Spotted) -> None:
        with pytest.warns(DeprecationWarning):
            with client.shows.with_streaming_response.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                show = response.parse()
                assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_episodes(self, client: Spotted) -> None:
        show = client.shows.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )
        assert_matches_type(SyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_episodes_with_all_params(self, client: Spotted) -> None:
        show = client.shows.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(SyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_episodes(self, client: Spotted) -> None:
        response = client.shows.with_raw_response.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        show = response.parse()
        assert_matches_type(SyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_episodes(self, client: Spotted) -> None:
        with client.shows.with_streaming_response.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            show = response.parse()
            assert_matches_type(SyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_episodes(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.shows.with_raw_response.list_episodes(
                id="",
            )


class TestAsyncShows:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSpotted) -> None:
        show = await async_client.shows.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )
        assert_matches_type(ShowRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        show = await async_client.shows.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
            market="ES",
        )
        assert_matches_type(ShowRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSpotted) -> None:
        response = await async_client.shows.with_raw_response.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        show = await response.parse()
        assert_matches_type(ShowRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSpotted) -> None:
        async with async_client.shows.with_streaming_response.retrieve(
            id="38bS44xjbVVZ3No3ByF1dJ",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            show = await response.parse()
            assert_matches_type(ShowRetrieveResponse, show, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.shows.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            show = await async_client.shows.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
            )

        assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_bulk_retrieve_with_all_params(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            show = await async_client.shows.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
                market="ES",
            )

        assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.shows.with_raw_response.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        show = await response.parse()
        assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_bulk_retrieve(self, async_client: AsyncSpotted) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.shows.with_streaming_response.bulk_retrieve(
                ids="5CfCWKI5pZ28U0uOzXkDHe,5as3aKmN2k11yfDDDSrvaZ",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                show = await response.parse()
                assert_matches_type(ShowBulkRetrieveResponse, show, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_episodes(self, async_client: AsyncSpotted) -> None:
        show = await async_client.shows.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )
        assert_matches_type(AsyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_episodes_with_all_params(self, async_client: AsyncSpotted) -> None:
        show = await async_client.shows.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
            limit=10,
            market="ES",
            offset=5,
        )
        assert_matches_type(AsyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_episodes(self, async_client: AsyncSpotted) -> None:
        response = await async_client.shows.with_raw_response.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        show = await response.parse()
        assert_matches_type(AsyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_episodes(self, async_client: AsyncSpotted) -> None:
        async with async_client.shows.with_streaming_response.list_episodes(
            id="38bS44xjbVVZ3No3ByF1dJ",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            show = await response.parse()
            assert_matches_type(AsyncCursorURLPage[SimplifiedEpisodeObject], show, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_episodes(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.shows.with_raw_response.list_episodes(
                id="",
            )
