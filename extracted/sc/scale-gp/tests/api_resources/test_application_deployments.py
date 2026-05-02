# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ApplicationDeployment,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        application_deployment = client.application_deployments.create(
            account_id="account_id",
            application_variant_id="application_variant_id",
            endpoint="endpoint",
            is_active=True,
            name="name",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.application_deployments.with_raw_response.create(
            account_id="account_id",
            application_variant_id="application_variant_id",
            endpoint="endpoint",
            is_active=True,
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = response.parse()
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.application_deployments.with_streaming_response.create(
            account_id="account_id",
            application_variant_id="application_variant_id",
            endpoint="endpoint",
            is_active=True,
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = response.parse()
            assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        application_deployment = client.application_deployments.retrieve(
            "application_deployment_id",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.application_deployments.with_raw_response.retrieve(
            "application_deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = response.parse()
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.application_deployments.with_streaming_response.retrieve(
            "application_deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = response.parse()
            assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_deployment_id` but received ''"
        ):
            client.application_deployments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        application_deployment = client.application_deployments.update(
            application_deployment_id="application_deployment_id",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        application_deployment = client.application_deployments.update(
            application_deployment_id="application_deployment_id",
            is_active=True,
            name="name",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.application_deployments.with_raw_response.update(
            application_deployment_id="application_deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = response.parse()
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.application_deployments.with_streaming_response.update(
            application_deployment_id="application_deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = response.parse()
            assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_deployment_id` but received ''"
        ):
            client.application_deployments.with_raw_response.update(
                application_deployment_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        application_deployment = client.application_deployments.list()
        assert_matches_type(SyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        application_deployment = client.application_deployments.list(
            account_id="account_id",
            application_variant_id=0,
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.application_deployments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = response.parse()
        assert_matches_type(SyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.application_deployments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = response.parse()
            assert_matches_type(SyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationDeployments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        application_deployment = await async_client.application_deployments.create(
            account_id="account_id",
            application_variant_id="application_variant_id",
            endpoint="endpoint",
            is_active=True,
            name="name",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_deployments.with_raw_response.create(
            account_id="account_id",
            application_variant_id="application_variant_id",
            endpoint="endpoint",
            is_active=True,
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = await response.parse()
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_deployments.with_streaming_response.create(
            account_id="account_id",
            application_variant_id="application_variant_id",
            endpoint="endpoint",
            is_active=True,
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = await response.parse()
            assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        application_deployment = await async_client.application_deployments.retrieve(
            "application_deployment_id",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_deployments.with_raw_response.retrieve(
            "application_deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = await response.parse()
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_deployments.with_streaming_response.retrieve(
            "application_deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = await response.parse()
            assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_deployment_id` but received ''"
        ):
            await async_client.application_deployments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        application_deployment = await async_client.application_deployments.update(
            application_deployment_id="application_deployment_id",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_deployment = await async_client.application_deployments.update(
            application_deployment_id="application_deployment_id",
            is_active=True,
            name="name",
        )
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_deployments.with_raw_response.update(
            application_deployment_id="application_deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = await response.parse()
        assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_deployments.with_streaming_response.update(
            application_deployment_id="application_deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = await response.parse()
            assert_matches_type(ApplicationDeployment, application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_deployment_id` but received ''"
        ):
            await async_client.application_deployments.with_raw_response.update(
                application_deployment_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        application_deployment = await async_client.application_deployments.list()
        assert_matches_type(AsyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_deployment = await async_client.application_deployments.list(
            account_id="account_id",
            application_variant_id=0,
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_deployments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_deployment = await response.parse()
        assert_matches_type(AsyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_deployments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_deployment = await response.parse()
            assert_matches_type(AsyncPageResponse[ApplicationDeployment], application_deployment, path=["response"])

        assert cast(Any, response.is_closed) is True
