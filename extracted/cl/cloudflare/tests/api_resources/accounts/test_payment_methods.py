# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.pagination import SyncV4PagePaginationArray, AsyncV4PagePaginationArray
from cloudflare.types.accounts import (
    PaymentMethodGetResponse,
    PaymentMethodListResponse,
    PaymentMethodCreateResponse,
    PaymentMethodDeleteResponse,
    PaymentMethodUpdateResponse,
    PaymentMethodSetAsDefaultResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPaymentMethods:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="address",
            address2="address2",
            bank_account_type="bank_account_type",
            bank_code="bank_code",
            bank_country="bank_country",
            bank_name="bank_name",
            bank_routing_number="bank_routing_number",
            cashapp_cash_tag="cashapp_cash_tag",
            city="city",
            country="country",
            default=True,
            device_data="device_data",
            first_name="first_name",
            last_name="last_name",
            nick_name="nick_name",
            payment_account_email="payment_account_email",
            payment_email="payment_email",
            payment_gateway="payment_gateway",
            payment_nonce="payment_nonce",
            state="state",
            type="CREDIT_CARD",
            zipcode="zipcode",
        )
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Cloudflare) -> None:
        response = client.accounts.payment_methods.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Cloudflare) -> None:
        with client.accounts.payment_methods.with_streaming_response.create(
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
            client.accounts.payment_methods.with_raw_response.create(
                account_id="",
            )

    @parametrize
    def test_method_update(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="address",
            address2="address2",
            bank_account_type="bank_account_type",
            bank_code="bank_code",
            bank_country="bank_country",
            bank_name="bank_name",
            bank_routing_number="bank_routing_number",
            cashapp_cash_tag="cashapp_cash_tag",
            city="city",
            country="country",
            default=True,
            device_data="device_data",
            first_name="first_name",
            last_name="last_name",
            nick_name="nick_name",
            payment_account_email="payment_account_email",
            payment_email="payment_email",
            payment_gateway="payment_gateway",
            payment_nonce="payment_nonce",
            state="state",
            type="CREDIT_CARD",
            zipcode="zipcode",
        )
        assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Cloudflare) -> None:
        response = client.accounts.payment_methods.with_raw_response.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Cloudflare) -> None:
        with client.accounts.payment_methods.with_streaming_response.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = response.parse()
            assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.update(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.update(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    def test_method_list(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(SyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            page=1,
            per_page=1,
        )
        assert_matches_type(SyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Cloudflare) -> None:
        response = client.accounts.payment_methods.with_raw_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(SyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Cloudflare) -> None:
        with client.accounts.payment_methods.with_streaming_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = response.parse()
            assert_matches_type(SyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.list(
                account_id="",
            )

    @parametrize
    def test_method_delete(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.delete(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodDeleteResponse, payment_method, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Cloudflare) -> None:
        response = client.accounts.payment_methods.with_raw_response.delete(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(PaymentMethodDeleteResponse, payment_method, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Cloudflare) -> None:
        with client.accounts.payment_methods.with_streaming_response.delete(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = response.parse()
            assert_matches_type(PaymentMethodDeleteResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.delete(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.delete(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    def test_method_get(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.get(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodGetResponse, payment_method, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Cloudflare) -> None:
        response = client.accounts.payment_methods.with_raw_response.get(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(PaymentMethodGetResponse, payment_method, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Cloudflare) -> None:
        with client.accounts.payment_methods.with_streaming_response.get(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = response.parse()
            assert_matches_type(PaymentMethodGetResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.get(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.get(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    def test_method_set_as_default(self, client: Cloudflare) -> None:
        payment_method = client.accounts.payment_methods.set_as_default(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodSetAsDefaultResponse, payment_method, path=["response"])

    @parametrize
    def test_raw_response_set_as_default(self, client: Cloudflare) -> None:
        response = client.accounts.payment_methods.with_raw_response.set_as_default(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = response.parse()
        assert_matches_type(PaymentMethodSetAsDefaultResponse, payment_method, path=["response"])

    @parametrize
    def test_streaming_response_set_as_default(self, client: Cloudflare) -> None:
        with client.accounts.payment_methods.with_streaming_response.set_as_default(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = response.parse()
            assert_matches_type(PaymentMethodSetAsDefaultResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_set_as_default(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.set_as_default(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            client.accounts.payment_methods.with_raw_response.set_as_default(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncPaymentMethods:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="address",
            address2="address2",
            bank_account_type="bank_account_type",
            bank_code="bank_code",
            bank_country="bank_country",
            bank_name="bank_name",
            bank_routing_number="bank_routing_number",
            cashapp_cash_tag="cashapp_cash_tag",
            city="city",
            country="country",
            default=True,
            device_data="device_data",
            first_name="first_name",
            last_name="last_name",
            nick_name="nick_name",
            payment_account_email="payment_account_email",
            payment_email="payment_email",
            payment_gateway="payment_gateway",
            payment_nonce="payment_nonce",
            state="state",
            type="CREDIT_CARD",
            zipcode="zipcode",
        )
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.payment_methods.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(PaymentMethodCreateResponse, payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.payment_methods.with_streaming_response.create(
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
            await async_client.accounts.payment_methods.with_raw_response.create(
                account_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="address",
            address2="address2",
            bank_account_type="bank_account_type",
            bank_code="bank_code",
            bank_country="bank_country",
            bank_name="bank_name",
            bank_routing_number="bank_routing_number",
            cashapp_cash_tag="cashapp_cash_tag",
            city="city",
            country="country",
            default=True,
            device_data="device_data",
            first_name="first_name",
            last_name="last_name",
            nick_name="nick_name",
            payment_account_email="payment_account_email",
            payment_email="payment_email",
            payment_gateway="payment_gateway",
            payment_nonce="payment_nonce",
            state="state",
            type="CREDIT_CARD",
            zipcode="zipcode",
        )
        assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.payment_methods.with_raw_response.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.payment_methods.with_streaming_response.update(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = await response.parse()
            assert_matches_type(PaymentMethodUpdateResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.update(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.update(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(AsyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            page=1,
            per_page=1,
        )
        assert_matches_type(AsyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.payment_methods.with_raw_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(AsyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.payment_methods.with_streaming_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = await response.parse()
            assert_matches_type(
                AsyncV4PagePaginationArray[PaymentMethodListResponse], payment_method, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.list(
                account_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.delete(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodDeleteResponse, payment_method, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.payment_methods.with_raw_response.delete(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(PaymentMethodDeleteResponse, payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.payment_methods.with_streaming_response.delete(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = await response.parse()
            assert_matches_type(PaymentMethodDeleteResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.delete(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.delete(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.get(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodGetResponse, payment_method, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.payment_methods.with_raw_response.get(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(PaymentMethodGetResponse, payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.payment_methods.with_streaming_response.get(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = await response.parse()
            assert_matches_type(PaymentMethodGetResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.get(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.get(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    async def test_method_set_as_default(self, async_client: AsyncCloudflare) -> None:
        payment_method = await async_client.accounts.payment_methods.set_as_default(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(PaymentMethodSetAsDefaultResponse, payment_method, path=["response"])

    @parametrize
    async def test_raw_response_set_as_default(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.payment_methods.with_raw_response.set_as_default(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_method = await response.parse()
        assert_matches_type(PaymentMethodSetAsDefaultResponse, payment_method, path=["response"])

    @parametrize
    async def test_streaming_response_set_as_default(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.payment_methods.with_streaming_response.set_as_default(
            payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_method = await response.parse()
            assert_matches_type(PaymentMethodSetAsDefaultResponse, payment_method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_set_as_default(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.set_as_default(
                payment_method_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_method_id` but received ''"):
            await async_client.accounts.payment_methods.with_raw_response.set_as_default(
                payment_method_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
