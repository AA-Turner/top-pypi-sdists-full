# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api._utils import parse_datetime
from boltz_api.pagination import SyncOpaqueCursorPage, AsyncOpaqueCursorPage
from boltz_api.types.admin import UsageListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        usage = client.admin.usage.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
        )
        assert_matches_type(SyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        usage = client.admin.usage.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
            applications="structure_and_binding",
            group_by="workspace_id",
            limit=1,
            page="page",
            workspace_ids="string",
        )
        assert_matches_type(SyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.admin.usage.with_raw_response.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = response.parse()
        assert_matches_type(SyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.admin.usage.with_streaming_response.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = response.parse()
            assert_matches_type(SyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsage:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        usage = await async_client.admin.usage.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
        )
        assert_matches_type(AsyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        usage = await async_client.admin.usage.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
            applications="structure_and_binding",
            group_by="workspace_id",
            limit=1,
            page="page",
            workspace_ids="string",
        )
        assert_matches_type(AsyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.usage.with_raw_response.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = await response.parse()
        assert_matches_type(AsyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.usage.with_streaming_response.list(
            ending_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="HOUR",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = await response.parse()
            assert_matches_type(AsyncOpaqueCursorPage[UsageListResponse], usage, path=["response"])

        assert cast(Any, response.is_closed) is True
