# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.types.billing.profiles import PaymentMethodCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPaymentMethod:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Cloudflare) -> None:
        payment_method = client.billing.profiles.payment_method.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Cloudflare) -> None:
        response = client.billing.profiles.payment_method.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Cloudflare) -> None:
        with client.billing.profiles.payment_method.with_streaming_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = response.parse()
            assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.billing.profiles.payment_method.with_raw_response.create(
                account_id="",
            )


class TestAsyncPaymentMethod:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.billing.profiles.payment_method.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.billing.profiles.payment_method.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCloudflare) -> None:
        async with async_client.billing.profiles.payment_method.with_streaming_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = await response.parse()
            assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.billing.profiles.payment_method.with_raw_response.create(
                account_id="",
            )
