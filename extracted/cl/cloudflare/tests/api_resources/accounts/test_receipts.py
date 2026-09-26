# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from cloudflare import Cloudflare, AsyncCloudflare
from cloudflare._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReceipts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_pdf(self, client: Cloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        receipt = client.accounts.receipts.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert receipt.is_closed
        assert receipt.json() == {"foo": "bar"}
        assert cast(Any, receipt.is_closed) is True
        assert isinstance(receipt, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_pdf_with_all_params(self, client: Cloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        receipt = client.accounts.receipts.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            doctype="doctype",
        )
        assert receipt.is_closed
        assert receipt.json() == {"foo": "bar"}
        assert cast(Any, receipt.is_closed) is True
        assert isinstance(receipt, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_pdf(self, client: Cloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        receipt = client.accounts.receipts.with_raw_response.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert receipt.is_closed is True
        assert receipt.http_request.headers.get("X-Stainless-Lang") == "python"
        assert receipt.json() == {"foo": "bar"}
        assert isinstance(receipt, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_pdf(self, client: Cloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.accounts.receipts.with_streaming_response.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as receipt:
            assert not receipt.is_closed
            assert receipt.http_request.headers.get("X-Stainless-Lang") == "python"

            assert receipt.json() == {"foo": "bar"}
            assert cast(Any, receipt.is_closed) is True
            assert isinstance(receipt, StreamedBinaryAPIResponse)

        assert cast(Any, receipt.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_pdf(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.receipts.with_raw_response.pdf(
                receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `receipt_id` but received ''"):
            client.accounts.receipts.with_raw_response.pdf(
                receipt_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncReceipts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_pdf(self, async_client: AsyncCloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        receipt = await async_client.accounts.receipts.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert receipt.is_closed
        assert await receipt.json() == {"foo": "bar"}
        assert cast(Any, receipt.is_closed) is True
        assert isinstance(receipt, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_pdf_with_all_params(self, async_client: AsyncCloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        receipt = await async_client.accounts.receipts.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            doctype="doctype",
        )
        assert receipt.is_closed
        assert await receipt.json() == {"foo": "bar"}
        assert cast(Any, receipt.is_closed) is True
        assert isinstance(receipt, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_pdf(self, async_client: AsyncCloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        receipt = await async_client.accounts.receipts.with_raw_response.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert receipt.is_closed is True
        assert receipt.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await receipt.json() == {"foo": "bar"}
        assert isinstance(receipt, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_pdf(self, async_client: AsyncCloudflare, respx_mock: MockRouter) -> None:
        respx_mock.get("/accounts/023e105f4ecef8ad9ca31a8372d0c353/receipts/023e105f4ecef8ad9ca31a8372d0c353/pdf").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.accounts.receipts.with_streaming_response.pdf(
            receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as receipt:
            assert not receipt.is_closed
            assert receipt.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await receipt.json() == {"foo": "bar"}
            assert cast(Any, receipt.is_closed) is True
            assert isinstance(receipt, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, receipt.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_pdf(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.receipts.with_raw_response.pdf(
                receipt_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `receipt_id` but received ''"):
            await async_client.accounts.receipts.with_raw_response.pdf(
                receipt_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
