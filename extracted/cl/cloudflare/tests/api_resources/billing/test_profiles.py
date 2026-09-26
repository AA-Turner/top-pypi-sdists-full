# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.types.billing import (
    ProfileGetResponse,
    ProfileCreateResponse,
    ProfileUpdateResponse,
    ProfileUpdateBillingEmailResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProfiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileCreateResponse, profile, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="123 Main Street",
            address2="Apt 1",
            billing_email="billing@example.com",
            buying_rate_plan="buying_rate_plan",
            captcha_challenge_jwt="captcha_challenge_jwt",
            cf_turnstile_response="cf_turnstile_response",
            city="Anytown",
            company="Example Inc",
            country="US",
            first_name="John",
            h_captcha_response="h_captcha_response",
            last_name="Doe",
            preferred_locale="en-US",
            secondary_billing_email="secondary@example.com",
            state="CA",
            tax_id_type="tax_id_type",
            telephone="+1-555-555-5555",
            vat="vat",
            zipcode="94103",
        )
        assert_matches_type(ProfileCreateResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Cloudflare) -> None:
        response = client.billing.profiles.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(ProfileCreateResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Cloudflare) -> None:
        with client.billing.profiles.with_streaming_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(ProfileCreateResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.billing.profiles.with_raw_response.create(
                account_id="",
            )

    @parametrize
    def test_method_update(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="123 Main Street",
            address2="Apt 1",
            billing_email="billing@example.com",
            buying_rate_plan="buying_rate_plan",
            captcha_challenge_jwt="captcha_challenge_jwt",
            cf_turnstile_response="cf_turnstile_response",
            city="Anytown",
            company="Example Inc",
            country="US",
            first_name="John",
            h_captcha_response="h_captcha_response",
            last_name="Doe",
            preferred_locale="en-US",
            secondary_billing_email="secondary@example.com",
            state="CA",
            tax_id_type="tax_id_type",
            telephone="+1-555-555-5555",
            vat="vat",
            zipcode="94103",
        )
        assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Cloudflare) -> None:
        response = client.billing.profiles.with_raw_response.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Cloudflare) -> None:
        with client.billing.profiles.with_streaming_response.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.billing.profiles.with_raw_response.update(
                account_id="",
            )

    @parametrize
    def test_method_delete(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.delete(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert profile is None

    @parametrize
    def test_raw_response_delete(self, client: Cloudflare) -> None:
        response = client.billing.profiles.with_raw_response.delete(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert profile is None

    @parametrize
    def test_streaming_response_delete(self, client: Cloudflare) -> None:
        with client.billing.profiles.with_streaming_response.delete(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert profile is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.billing.profiles.with_raw_response.delete(
                account_id="",
            )

    @parametrize
    def test_method_get(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.get(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileGetResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Cloudflare) -> None:
        response = client.billing.profiles.with_raw_response.get(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(ProfileGetResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Cloudflare) -> None:
        with client.billing.profiles.with_streaming_response.get(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(ProfileGetResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.billing.profiles.with_raw_response.get(
                account_id="",
            )

    @parametrize
    def test_method_update_billing_email(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

    @parametrize
    def test_method_update_billing_email_with_all_params(self, client: Cloudflare) -> None:
        profile = client.billing.profiles.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            billing_email="billing@example.com",
            preferred_locale="en-US",
            secondary_billing_email="secondary@example.com",
        )
        assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_update_billing_email(self, client: Cloudflare) -> None:
        response = client.billing.profiles.with_raw_response.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_update_billing_email(self, client: Cloudflare) -> None:
        with client.billing.profiles.with_streaming_response.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_billing_email(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.billing.profiles.with_raw_response.update_billing_email(
                account_id="",
            )


class TestAsyncProfiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileCreateResponse, profile, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="123 Main Street",
            address2="Apt 1",
            billing_email="billing@example.com",
            buying_rate_plan="buying_rate_plan",
            captcha_challenge_jwt="captcha_challenge_jwt",
            cf_turnstile_response="cf_turnstile_response",
            city="Anytown",
            company="Example Inc",
            country="US",
            first_name="John",
            h_captcha_response="h_captcha_response",
            last_name="Doe",
            preferred_locale="en-US",
            secondary_billing_email="secondary@example.com",
            state="CA",
            tax_id_type="tax_id_type",
            telephone="+1-555-555-5555",
            vat="vat",
            zipcode="94103",
        )
        assert_matches_type(ProfileCreateResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.billing.profiles.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(ProfileCreateResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCloudflare) -> None:
        async with async_client.billing.profiles.with_streaming_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(ProfileCreateResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.billing.profiles.with_raw_response.create(
                account_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            address="123 Main Street",
            address2="Apt 1",
            billing_email="billing@example.com",
            buying_rate_plan="buying_rate_plan",
            captcha_challenge_jwt="captcha_challenge_jwt",
            cf_turnstile_response="cf_turnstile_response",
            city="Anytown",
            company="Example Inc",
            country="US",
            first_name="John",
            h_captcha_response="h_captcha_response",
            last_name="Doe",
            preferred_locale="en-US",
            secondary_billing_email="secondary@example.com",
            state="CA",
            tax_id_type="tax_id_type",
            telephone="+1-555-555-5555",
            vat="vat",
            zipcode="94103",
        )
        assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.billing.profiles.with_raw_response.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCloudflare) -> None:
        async with async_client.billing.profiles.with_streaming_response.update(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(ProfileUpdateResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.billing.profiles.with_raw_response.update(
                account_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.delete(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert profile is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.billing.profiles.with_raw_response.delete(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert profile is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCloudflare) -> None:
        async with async_client.billing.profiles.with_streaming_response.delete(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert profile is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.billing.profiles.with_raw_response.delete(
                account_id="",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.get(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileGetResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.billing.profiles.with_raw_response.get(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(ProfileGetResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncCloudflare) -> None:
        async with async_client.billing.profiles.with_streaming_response.get(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(ProfileGetResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.billing.profiles.with_raw_response.get(
                account_id="",
            )

    @parametrize
    async def test_method_update_billing_email(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

    @parametrize
    async def test_method_update_billing_email_with_all_params(self, async_client: AsyncCloudflare) -> None:
        profile = await async_client.billing.profiles.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            billing_email="billing@example.com",
            preferred_locale="en-US",
            secondary_billing_email="secondary@example.com",
        )
        assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_update_billing_email(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.billing.profiles.with_raw_response.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_update_billing_email(self, async_client: AsyncCloudflare) -> None:
        async with async_client.billing.profiles.with_streaming_response.update_billing_email(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(ProfileUpdateBillingEmailResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_billing_email(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.billing.profiles.with_raw_response.update_billing_email(
                account_id="",
            )
