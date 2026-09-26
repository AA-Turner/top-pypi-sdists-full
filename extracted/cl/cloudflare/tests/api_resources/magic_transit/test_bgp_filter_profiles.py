# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.pagination import SyncSinglePage, AsyncSinglePage
from cloudflare.types.magic_transit import (
    BGPFilterProfileGetResponse,
    BGPFilterProfileListResponse,
    BGPFilterProfileCreateResponse,
    BGPFilterProfileDeleteResponse,
    BGPFilterProfileUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBGPFilterProfiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        )
        assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
            description="Allowed corporate subnets from on-premises",
        )
        assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Cloudflare) -> None:
        response = client.magic_transit.bgp_filter_profiles.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = response.parse()
        assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Cloudflare) -> None:
        with client.magic_transit.bgp_filter_profiles.with_streaming_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = response.parse()
            assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.create(
                account_id="",
                match_action="allow",
                name="Allowed On-Prem Imports",
                targets=["10.0.0.0/8{8,32}"],
            )

    @parametrize
    def test_method_update(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            description="Allowed corporate subnets from on-premises",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        )
        assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Cloudflare) -> None:
        response = client.magic_transit.bgp_filter_profiles.with_raw_response.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = response.parse()
        assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Cloudflare) -> None:
        with client.magic_transit.bgp_filter_profiles.with_streaming_response.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = response.parse()
            assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.update(
                profile_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.update(
                profile_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    def test_method_list(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(SyncSinglePage[BGPFilterProfileListResponse], bgp_filter_profile, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Cloudflare) -> None:
        response = client.magic_transit.bgp_filter_profiles.with_raw_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = response.parse()
        assert_matches_type(SyncSinglePage[BGPFilterProfileListResponse], bgp_filter_profile, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Cloudflare) -> None:
        with client.magic_transit.bgp_filter_profiles.with_streaming_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = response.parse()
            assert_matches_type(SyncSinglePage[BGPFilterProfileListResponse], bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.list(
                account_id="",
            )

    @parametrize
    def test_method_delete(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.delete(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(BGPFilterProfileDeleteResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Cloudflare) -> None:
        response = client.magic_transit.bgp_filter_profiles.with_raw_response.delete(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = response.parse()
        assert_matches_type(BGPFilterProfileDeleteResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Cloudflare) -> None:
        with client.magic_transit.bgp_filter_profiles.with_streaming_response.delete(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = response.parse()
            assert_matches_type(BGPFilterProfileDeleteResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.delete(
                profile_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.delete(
                profile_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    def test_method_get(self, client: Cloudflare) -> None:
        bgp_filter_profile = client.magic_transit.bgp_filter_profiles.get(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(BGPFilterProfileGetResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Cloudflare) -> None:
        response = client.magic_transit.bgp_filter_profiles.with_raw_response.get(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = response.parse()
        assert_matches_type(BGPFilterProfileGetResponse, bgp_filter_profile, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Cloudflare) -> None:
        with client.magic_transit.bgp_filter_profiles.with_streaming_response.get(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = response.parse()
            assert_matches_type(BGPFilterProfileGetResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.get(
                profile_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            client.magic_transit.bgp_filter_profiles.with_raw_response.get(
                profile_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncBGPFilterProfiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        )
        assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
            description="Allowed corporate subnets from on-premises",
        )
        assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.magic_transit.bgp_filter_profiles.with_raw_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = await response.parse()
        assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCloudflare) -> None:
        async with async_client.magic_transit.bgp_filter_profiles.with_streaming_response.create(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = await response.parse()
            assert_matches_type(BGPFilterProfileCreateResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.create(
                account_id="",
                match_action="allow",
                name="Allowed On-Prem Imports",
                targets=["10.0.0.0/8{8,32}"],
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            description="Allowed corporate subnets from on-premises",
            match_action="allow",
            name="Allowed On-Prem Imports",
            targets=["10.0.0.0/8{8,32}"],
        )
        assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.magic_transit.bgp_filter_profiles.with_raw_response.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = await response.parse()
        assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCloudflare) -> None:
        async with async_client.magic_transit.bgp_filter_profiles.with_streaming_response.update(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = await response.parse()
            assert_matches_type(BGPFilterProfileUpdateResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.update(
                profile_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.update(
                profile_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(AsyncSinglePage[BGPFilterProfileListResponse], bgp_filter_profile, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.magic_transit.bgp_filter_profiles.with_raw_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = await response.parse()
        assert_matches_type(AsyncSinglePage[BGPFilterProfileListResponse], bgp_filter_profile, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCloudflare) -> None:
        async with async_client.magic_transit.bgp_filter_profiles.with_streaming_response.list(
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = await response.parse()
            assert_matches_type(AsyncSinglePage[BGPFilterProfileListResponse], bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.list(
                account_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.delete(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(BGPFilterProfileDeleteResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.magic_transit.bgp_filter_profiles.with_raw_response.delete(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = await response.parse()
        assert_matches_type(BGPFilterProfileDeleteResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCloudflare) -> None:
        async with async_client.magic_transit.bgp_filter_profiles.with_streaming_response.delete(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = await response.parse()
            assert_matches_type(BGPFilterProfileDeleteResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.delete(
                profile_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.delete(
                profile_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncCloudflare) -> None:
        bgp_filter_profile = await async_client.magic_transit.bgp_filter_profiles.get(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(BGPFilterProfileGetResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.magic_transit.bgp_filter_profiles.with_raw_response.get(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bgp_filter_profile = await response.parse()
        assert_matches_type(BGPFilterProfileGetResponse, bgp_filter_profile, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncCloudflare) -> None:
        async with async_client.magic_transit.bgp_filter_profiles.with_streaming_response.get(
            profile_id="023e105f4ecef8ad9ca31a8372d0c353",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bgp_filter_profile = await response.parse()
            assert_matches_type(BGPFilterProfileGetResponse, bgp_filter_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.get(
                profile_id="023e105f4ecef8ad9ca31a8372d0c353",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            await async_client.magic_transit.bgp_filter_profiles.with_raw_response.get(
                profile_id="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
