# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.types.registrar import WorkflowStatus

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransferIn:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Cloudflare) -> None:
        transfer_in = client.registrar.transfer_in.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Cloudflare) -> None:
        transfer_in = client.registrar.transfer_in.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            auth_code="bml4b3M+Pj5hcmNoLWxpbnV4",
            auto_renew=False,
            contact_extensions={
                "application_purpose": "bar",
                "nexus_category": "bar",
            },
            contacts={
                "administrator": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
                "billing": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
                "registrant": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
                "technical": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
            },
            privacy_mode="redaction",
            prefer="Prefer",
        )
        assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Cloudflare) -> None:
        response = client.registrar.transfer_in.with_raw_response.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transfer_in = response.parse()
        assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Cloudflare) -> None:
        with client.registrar.transfer_in.with_streaming_response.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transfer_in = response.parse()
            assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.registrar.transfer_in.with_raw_response.create(
                domain_name="example.com",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `domain_name` but received ''"):
            client.registrar.transfer_in.with_raw_response.create(
                domain_name="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )


class TestAsyncTransferIn:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncCloudflare) -> None:
        transfer_in = await async_client.registrar.transfer_in.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCloudflare) -> None:
        transfer_in = await async_client.registrar.transfer_in.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
            auth_code="bml4b3M+Pj5hcmNoLWxpbnV4",
            auto_renew=False,
            contact_extensions={
                "application_purpose": "bar",
                "nexus_category": "bar",
            },
            contacts={
                "administrator": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
                "billing": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
                "registrant": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
                "technical": {
                    "email": "ada@example.com",
                    "phone": "+1.5555555555",
                    "postal_info": {
                        "address": {
                            "city": "Austin",
                            "country_code": "US",
                            "postal_code": "78701",
                            "state": "TX",
                            "street": "123 Main St",
                        },
                        "name": "Ada Lovelace",
                        "organization": "Example Inc",
                    },
                    "fax": "+1.5555555555",
                },
            },
            privacy_mode="redaction",
            prefer="Prefer",
        )
        assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.registrar.transfer_in.with_raw_response.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transfer_in = await response.parse()
        assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCloudflare) -> None:
        async with async_client.registrar.transfer_in.with_streaming_response.create(
            domain_name="example.com",
            account_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transfer_in = await response.parse()
            assert_matches_type(WorkflowStatus, transfer_in, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.registrar.transfer_in.with_raw_response.create(
                domain_name="example.com",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `domain_name` but received ''"):
            await async_client.registrar.transfer_in.with_raw_response.create(
                domain_name="",
                account_id="023e105f4ecef8ad9ca31a8372d0c353",
            )
