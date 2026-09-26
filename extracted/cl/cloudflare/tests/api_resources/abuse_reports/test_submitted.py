# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare._utils import parse_datetime
from cloudflare.pagination import SyncV4PagePagination, AsyncV4PagePagination
from cloudflare.types.abuse_reports import SubmittedGetResponse, SubmittedListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubmitted:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_method_list(self, client: Cloudflare) -> None:
        submitted = client.abuse_reports.submitted.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(SyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_method_list_with_all_params(self, client: Cloudflare) -> None:
        submitted = client.abuse_reports.submitted.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            id="id",
            created_after=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_before=parse_datetime("2019-12-27T18:11:19.117Z"),
            domain=["string"],
            page=1,
            per_page=1,
            sort="sort",
            status=["submitted"],
            type=["PHISH"],
        )
        assert_matches_type(SyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_raw_response_list(self, client: Cloudflare) -> None:
        response = client.abuse_reports.submitted.with_raw_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        submitted = response.parse()
        assert_matches_type(SyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_streaming_response_list(self, client: Cloudflare) -> None:
        with client.abuse_reports.submitted.with_streaming_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            submitted = response.parse()
            assert_matches_type(SyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_path_params_list(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.abuse_reports.submitted.with_raw_response.list(
                account_id="",
            )

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_method_get(self, client: Cloudflare) -> None:
        submitted = client.abuse_reports.submitted.get(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(SubmittedGetResponse, submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_raw_response_get(self, client: Cloudflare) -> None:
        response = client.abuse_reports.submitted.with_raw_response.get(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        submitted = response.parse()
        assert_matches_type(SubmittedGetResponse, submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_streaming_response_get(self, client: Cloudflare) -> None:
        with client.abuse_reports.submitted.with_streaming_response.get(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            submitted = response.parse()
            assert_matches_type(SubmittedGetResponse, submitted, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_path_params_get(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.abuse_reports.submitted.with_raw_response.get(
                report_id="report_id",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `report_id` but received ''"):
            client.abuse_reports.submitted.with_raw_response.get(
                report_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncSubmitted:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_method_list(self, async_client: AsyncCloudflare) -> None:
        submitted = await async_client.abuse_reports.submitted.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(AsyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCloudflare) -> None:
        submitted = await async_client.abuse_reports.submitted.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            id="id",
            created_after=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_before=parse_datetime("2019-12-27T18:11:19.117Z"),
            domain=["string"],
            page=1,
            per_page=1,
            sort="sort",
            status=["submitted"],
            type=["PHISH"],
        )
        assert_matches_type(AsyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.abuse_reports.submitted.with_raw_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        submitted = await response.parse()
        assert_matches_type(AsyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCloudflare) -> None:
        async with async_client.abuse_reports.submitted.with_streaming_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            submitted = await response.parse()
            assert_matches_type(AsyncV4PagePagination[SubmittedListResponse], submitted, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.abuse_reports.submitted.with_raw_response.list(
                account_id="",
            )

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_method_get(self, async_client: AsyncCloudflare) -> None:
        submitted = await async_client.abuse_reports.submitted.get(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(SubmittedGetResponse, submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.abuse_reports.submitted.with_raw_response.get(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        submitted = await response.parse()
        assert_matches_type(SubmittedGetResponse, submitted, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncCloudflare) -> None:
        async with async_client.abuse_reports.submitted.with_streaming_response.get(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            submitted = await response.parse()
            assert_matches_type(SubmittedGetResponse, submitted, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_path_params_get(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.abuse_reports.submitted.with_raw_response.get(
                report_id="report_id",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `report_id` but received ''"):
            await async_client.abuse_reports.submitted.with_raw_response.get(
                report_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
