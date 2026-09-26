# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.types.shared import Subscription

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestActions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_append(self, client: Cloudflare) -> None:
        action = client.accounts.subscriptions.actions.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(Subscription, action, path=["response"])

    @parametrize
    def test_method_append_with_all_params(self, client: Cloudflare) -> None:
        action = client.accounts.subscriptions.actions.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            frequency="monthly",
            rate_plan={
                "id": "free",
                "currency": "USD",
                "externally_managed": False,
                "is_contract": False,
                "public_name": "Business Plan",
                "scope": "zone",
                "sets": ["string"],
            },
        )
        assert_matches_type(Subscription, action, path=["response"])

    @parametrize
    def test_raw_response_append(self, client: Cloudflare) -> None:
        response = client.accounts.subscriptions.actions.with_raw_response.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(Subscription, action, path=["response"])

    @parametrize
    def test_streaming_response_append(self, client: Cloudflare) -> None:
        with client.accounts.subscriptions.actions.with_streaming_response.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(Subscription, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_append(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.accounts.subscriptions.actions.with_raw_response.append(
                subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
                account_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `subscription_identifier` but received ''"
        ):
            client.accounts.subscriptions.actions.with_raw_response.append(
                subscription_identifier="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncActions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_append(self, async_client: AsyncCloudflare) -> None:
        action = await async_client.accounts.subscriptions.actions.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(Subscription, action, path=["response"])

    @parametrize
    async def test_method_append_with_all_params(self, async_client: AsyncCloudflare) -> None:
        action = await async_client.accounts.subscriptions.actions.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            frequency="monthly",
            rate_plan={
                "id": "free",
                "currency": "USD",
                "externally_managed": False,
                "is_contract": False,
                "public_name": "Business Plan",
                "scope": "zone",
                "sets": ["string"],
            },
        )
        assert_matches_type(Subscription, action, path=["response"])

    @parametrize
    async def test_raw_response_append(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.accounts.subscriptions.actions.with_raw_response.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(Subscription, action, path=["response"])

    @parametrize
    async def test_streaming_response_append(self, async_client: AsyncCloudflare) -> None:
        async with async_client.accounts.subscriptions.actions.with_streaming_response.append(
            subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(Subscription, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_append(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.accounts.subscriptions.actions.with_raw_response.append(
                subscription_identifier="506e3185e9c882d175a2d0cb0093d9f2",
                account_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `subscription_identifier` but received ''"
        ):
            await async_client.accounts.subscriptions.actions.with_raw_response.append(
                subscription_identifier="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
