# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.pagination import SyncCursorPaginationAfter, AsyncCursorPaginationAfter
from cloudflare.types.zero_trust.casb.posture import (
    PolicyGetResponse,
    PolicyListResponse,
    PolicyCreateResponse,
    PolicyDeleteResponse,
    PolicyUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPolicies:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
        )
        assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={
                "remediation_types": [{"remediation_type_id": "5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a"}],
                "webhook_configs": [{"webhook_config_id": "3f7b8c9d-6e5a-4f3b-9c2d-1e0a8b7c6d5e"}],
            },
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
            description="Automatically remove public access from files when detected",
            integration_ids=["497f6eca-6276-4993-bfeb-53cbbbba6f08"],
        )
        assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Cloudflare) -> None:
        response = client.zero_trust.casb.posture.policies.with_raw_response.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Cloudflare) -> None:
        with client.zero_trust.casb.posture.policies.with_streaming_response.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.create(
                account_id="",
                actions={},
                applies_to_all_integrations=False,
                display_name="Auto-remediate public files",
                enabled=True,
                finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
            )

    @parametrize
    def test_method_update(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
        )
        assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={
                "remediation_types": [{"remediation_type_id": "5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a"}],
                "webhook_configs": [{"webhook_config_id": "3f7b8c9d-6e5a-4f3b-9c2d-1e0a8b7c6d5e"}],
            },
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            description="Automatically remove public access from files when detected",
            integration_ids=["497f6eca-6276-4993-bfeb-53cbbbba6f08"],
        )
        assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Cloudflare) -> None:
        response = client.zero_trust.casb.posture.policies.with_raw_response.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Cloudflare) -> None:
        with client.zero_trust.casb.posture.policies.with_streaming_response.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.update(
                policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
                actions={},
                applies_to_all_integrations=False,
                display_name="Auto-remediate public files",
                enabled=True,
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.update(
                policy_id="",
                account_id="46148281d8a93d002ef242d8b0d5f9f6",
                actions={},
                applies_to_all_integrations=False,
                display_name="Auto-remediate public files",
                enabled=True,
            )

    @parametrize
    def test_method_list(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )
        assert_matches_type(SyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            cursor="cursor",
        )
        assert_matches_type(SyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Cloudflare) -> None:
        response = client.zero_trust.casb.posture.policies.with_raw_response.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(SyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Cloudflare) -> None:
        with client.zero_trust.casb.posture.policies.with_streaming_response.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(SyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.list(
                account_id="",
            )

    @parametrize
    def test_method_delete(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.delete(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )
        assert_matches_type(Optional[PolicyDeleteResponse], policy, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Cloudflare) -> None:
        response = client.zero_trust.casb.posture.policies.with_raw_response.delete(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(Optional[PolicyDeleteResponse], policy, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Cloudflare) -> None:
        with client.zero_trust.casb.posture.policies.with_streaming_response.delete(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(Optional[PolicyDeleteResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.delete(
                policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.delete(
                policy_id="",
                account_id="46148281d8a93d002ef242d8b0d5f9f6",
            )

    @parametrize
    def test_method_get(self, client: Cloudflare) -> None:
        policy = client.zero_trust.casb.posture.policies.get(
            policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )
        assert_matches_type(Optional[PolicyGetResponse], policy, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Cloudflare) -> None:
        response = client.zero_trust.casb.posture.policies.with_raw_response.get(
            policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(Optional[PolicyGetResponse], policy, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Cloudflare) -> None:
        with client.zero_trust.casb.posture.policies.with_streaming_response.get(
            policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(Optional[PolicyGetResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.get(
                policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_id` but received ''"):
            client.zero_trust.casb.posture.policies.with_raw_response.get(
                policy_id="",
                account_id="46148281d8a93d002ef242d8b0d5f9f6",
            )


class TestAsyncPolicies:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
        )
        assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={
                "remediation_types": [{"remediation_type_id": "5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a"}],
                "webhook_configs": [{"webhook_config_id": "3f7b8c9d-6e5a-4f3b-9c2d-1e0a8b7c6d5e"}],
            },
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
            description="Automatically remove public access from files when detected",
            integration_ids=["497f6eca-6276-4993-bfeb-53cbbbba6f08"],
        )
        assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.zero_trust.casb.posture.policies.with_raw_response.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCloudflare) -> None:
        async with async_client.zero_trust.casb.posture.policies.with_streaming_response.create(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(Optional[PolicyCreateResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.create(
                account_id="",
                actions={},
                applies_to_all_integrations=False,
                display_name="Auto-remediate public files",
                enabled=True,
                finding_type_id="5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
        )
        assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={
                "remediation_types": [{"remediation_type_id": "5a7d9e2f-1b3c-4d5e-8f6a-7b8c9d0e1f2a"}],
                "webhook_configs": [{"webhook_config_id": "3f7b8c9d-6e5a-4f3b-9c2d-1e0a8b7c6d5e"}],
            },
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
            description="Automatically remove public access from files when detected",
            integration_ids=["497f6eca-6276-4993-bfeb-53cbbbba6f08"],
        )
        assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.zero_trust.casb.posture.policies.with_raw_response.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCloudflare) -> None:
        async with async_client.zero_trust.casb.posture.policies.with_streaming_response.update(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            actions={},
            applies_to_all_integrations=False,
            display_name="Auto-remediate public files",
            enabled=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(Optional[PolicyUpdateResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.update(
                policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
                actions={},
                applies_to_all_integrations=False,
                display_name="Auto-remediate public files",
                enabled=True,
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.update(
                policy_id="",
                account_id="46148281d8a93d002ef242d8b0d5f9f6",
                actions={},
                applies_to_all_integrations=False,
                display_name="Auto-remediate public files",
                enabled=True,
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )
        assert_matches_type(AsyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
            cursor="cursor",
        )
        assert_matches_type(AsyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.zero_trust.casb.posture.policies.with_raw_response.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(AsyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCloudflare) -> None:
        async with async_client.zero_trust.casb.posture.policies.with_streaming_response.list(
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(AsyncCursorPaginationAfter[PolicyListResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.list(
                account_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.delete(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )
        assert_matches_type(Optional[PolicyDeleteResponse], policy, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.zero_trust.casb.posture.policies.with_raw_response.delete(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(Optional[PolicyDeleteResponse], policy, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCloudflare) -> None:
        async with async_client.zero_trust.casb.posture.policies.with_streaming_response.delete(
            policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(Optional[PolicyDeleteResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.delete(
                policy_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.delete(
                policy_id="",
                account_id="46148281d8a93d002ef242d8b0d5f9f6",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncCloudflare) -> None:
        policy = await async_client.zero_trust.casb.posture.policies.get(
            policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )
        assert_matches_type(Optional[PolicyGetResponse], policy, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.zero_trust.casb.posture.policies.with_raw_response.get(
            policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(Optional[PolicyGetResponse], policy, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncCloudflare) -> None:
        async with async_client.zero_trust.casb.posture.policies.with_streaming_response.get(
            policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
            account_id="46148281d8a93d002ef242d8b0d5f9f6",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(Optional[PolicyGetResponse], policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.get(
                policy_id="497f6eca-6276-4993-bfeb-53cbbbba6f08",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_id` but received ''"):
            await async_client.zero_trust.casb.posture.policies.with_raw_response.get(
                policy_id="",
                account_id="46148281d8a93d002ef242d8b0d5f9f6",
            )
