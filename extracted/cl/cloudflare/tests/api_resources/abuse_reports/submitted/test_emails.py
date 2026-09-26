# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.pagination import SyncV4PagePagination, AsyncV4PagePagination
from cloudflare.types.abuse_reports.submitted import EmailListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEmails:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_method_list(self, client: Cloudflare) -> None:
        email = client.abuse_reports.submitted.emails.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(SyncV4PagePagination[EmailListResponse], email, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_method_list_with_all_params(self, client: Cloudflare) -> None:
        email = client.abuse_reports.submitted.emails.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            page=0,
            per_page=0,
        )
        assert_matches_type(SyncV4PagePagination[EmailListResponse], email, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_raw_response_list(self, client: Cloudflare) -> None:
        response = client.abuse_reports.submitted.emails.with_raw_response.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = response.parse()
        assert_matches_type(SyncV4PagePagination[EmailListResponse], email, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_streaming_response_list(self, client: Cloudflare) -> None:
        with client.abuse_reports.submitted.emails.with_streaming_response.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = response.parse()
            assert_matches_type(SyncV4PagePagination[EmailListResponse], email, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    def test_path_params_list(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.abuse_reports.submitted.emails.with_raw_response.list(
                report_id="report_id",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `report_id` but received ''"):
            client.abuse_reports.submitted.emails.with_raw_response.list(
                report_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncEmails:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_method_list(self, async_client: AsyncCloudflare) -> None:
        email = await async_client.abuse_reports.submitted.emails.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(AsyncV4PagePagination[EmailListResponse], email, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCloudflare) -> None:
        email = await async_client.abuse_reports.submitted.emails.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            page=0,
            per_page=0,
        )
        assert_matches_type(AsyncV4PagePagination[EmailListResponse], email, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.abuse_reports.submitted.emails.with_raw_response.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = await response.parse()
        assert_matches_type(AsyncV4PagePagination[EmailListResponse], email, path=["response"])

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCloudflare) -> None:
        async with async_client.abuse_reports.submitted.emails.with_streaming_response.list(
            report_id="report_id",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = await response.parse()
            assert_matches_type(AsyncV4PagePagination[EmailListResponse], email, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="TODO: support api token auth scheme")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.abuse_reports.submitted.emails.with_raw_response.list(
                report_id="report_id",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `report_id` but received ''"):
            await async_client.abuse_reports.submitted.emails.with_raw_response.list(
                report_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
