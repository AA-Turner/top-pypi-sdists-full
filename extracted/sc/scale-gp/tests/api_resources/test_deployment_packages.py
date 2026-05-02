# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    DeploymentPackageJob,
    InstallDeploymentPackageResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeploymentPackages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_install(self, client: SGPClient) -> None:
        deployment_package = client.deployment_packages.install(
            account_id="account_id",
        )
        assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

    @parametrize
    def test_method_install_with_all_params(self, client: SGPClient) -> None:
        deployment_package = client.deployment_packages.install(
            account_id="account_id",
            deployment_package_id="deployment_package_id",
            deployment_package_name="deployment_package_name",
            deployment_package_type="EGP_CONFIGURATION",
            version_constraint={
                "minimum_version": "minimum_version",
                "version_constraint_type": "SEMVER_MIN",
            },
        )
        assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

    @parametrize
    def test_raw_response_install(self, client: SGPClient) -> None:
        response = client.deployment_packages.with_raw_response.install(
            account_id="account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_package = response.parse()
        assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

    @parametrize
    def test_streaming_response_install(self, client: SGPClient) -> None:
        with client.deployment_packages.with_streaming_response.install(
            account_id="account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_package = response.parse()
            assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_install(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.deployment_packages.with_raw_response.install(
                account_id="",
            )

    @parametrize
    def test_method_install_async(self, client: SGPClient) -> None:
        deployment_package = client.deployment_packages.install_async(
            account_id="account_id",
        )
        assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

    @parametrize
    def test_method_install_async_with_all_params(self, client: SGPClient) -> None:
        deployment_package = client.deployment_packages.install_async(
            account_id="account_id",
            deployment_package_id="deployment_package_id",
            deployment_package_name="deployment_package_name",
            deployment_package_type="EGP_CONFIGURATION",
            version_constraint={
                "minimum_version": "minimum_version",
                "version_constraint_type": "SEMVER_MIN",
            },
        )
        assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

    @parametrize
    def test_raw_response_install_async(self, client: SGPClient) -> None:
        response = client.deployment_packages.with_raw_response.install_async(
            account_id="account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_package = response.parse()
        assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

    @parametrize
    def test_streaming_response_install_async(self, client: SGPClient) -> None:
        with client.deployment_packages.with_streaming_response.install_async(
            account_id="account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_package = response.parse()
            assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_install_async(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.deployment_packages.with_raw_response.install_async(
                account_id="",
            )


class TestAsyncDeploymentPackages:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_install(self, async_client: AsyncSGPClient) -> None:
        deployment_package = await async_client.deployment_packages.install(
            account_id="account_id",
        )
        assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

    @parametrize
    async def test_method_install_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment_package = await async_client.deployment_packages.install(
            account_id="account_id",
            deployment_package_id="deployment_package_id",
            deployment_package_name="deployment_package_name",
            deployment_package_type="EGP_CONFIGURATION",
            version_constraint={
                "minimum_version": "minimum_version",
                "version_constraint_type": "SEMVER_MIN",
            },
        )
        assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

    @parametrize
    async def test_raw_response_install(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deployment_packages.with_raw_response.install(
            account_id="account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_package = await response.parse()
        assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

    @parametrize
    async def test_streaming_response_install(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deployment_packages.with_streaming_response.install(
            account_id="account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_package = await response.parse()
            assert_matches_type(InstallDeploymentPackageResponse, deployment_package, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_install(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.deployment_packages.with_raw_response.install(
                account_id="",
            )

    @parametrize
    async def test_method_install_async(self, async_client: AsyncSGPClient) -> None:
        deployment_package = await async_client.deployment_packages.install_async(
            account_id="account_id",
        )
        assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

    @parametrize
    async def test_method_install_async_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment_package = await async_client.deployment_packages.install_async(
            account_id="account_id",
            deployment_package_id="deployment_package_id",
            deployment_package_name="deployment_package_name",
            deployment_package_type="EGP_CONFIGURATION",
            version_constraint={
                "minimum_version": "minimum_version",
                "version_constraint_type": "SEMVER_MIN",
            },
        )
        assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

    @parametrize
    async def test_raw_response_install_async(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deployment_packages.with_raw_response.install_async(
            account_id="account_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_package = await response.parse()
        assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

    @parametrize
    async def test_streaming_response_install_async(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deployment_packages.with_streaming_response.install_async(
            account_id="account_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_package = await response.parse()
            assert_matches_type(DeploymentPackageJob, deployment_package, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_install_async(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.deployment_packages.with_raw_response.install_async(
                account_id="",
            )
