# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import deployment_package_install_params, deployment_package_install_async_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.deployment_package_job import DeploymentPackageJob
from ..types.install_deployment_package_response import InstallDeploymentPackageResponse

__all__ = ["DeploymentPackagesResource", "AsyncDeploymentPackagesResource"]


class DeploymentPackagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeploymentPackagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return DeploymentPackagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentPackagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return DeploymentPackagesResourceWithStreamingResponse(self)

    def install(
        self,
        account_id: str,
        *,
        deployment_package_id: str | Omit = omit,
        deployment_package_name: str | Omit = omit,
        deployment_package_type: Literal[
            "EGP_CONFIGURATION",
            "BLOB_STORAGE_FILE",
            "DOCKER_IMAGE",
            "EGP_ENTITY",
            "EGP_USER",
            "INTERNAL_MODEL_INFO",
            "EVALUATION_DATASET",
            "MODEL",
            "KNOWLEDGE_BASE",
            "AGENTS_CONFIG",
        ]
        | Omit = omit,
        version_constraint: deployment_package_install_params.VersionConstraint | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InstallDeploymentPackageResponse:
        """
        Install a deployment packages

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/v4/deployment-packages/{account_id}/install", account_id=account_id),
            body=maybe_transform(
                {
                    "deployment_package_id": deployment_package_id,
                    "deployment_package_name": deployment_package_name,
                    "deployment_package_type": deployment_package_type,
                    "version_constraint": version_constraint,
                },
                deployment_package_install_params.DeploymentPackageInstallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InstallDeploymentPackageResponse,
        )

    def install_async(
        self,
        account_id: str,
        *,
        deployment_package_id: str | Omit = omit,
        deployment_package_name: str | Omit = omit,
        deployment_package_type: Literal[
            "EGP_CONFIGURATION",
            "BLOB_STORAGE_FILE",
            "DOCKER_IMAGE",
            "EGP_ENTITY",
            "EGP_USER",
            "INTERNAL_MODEL_INFO",
            "EVALUATION_DATASET",
            "MODEL",
            "KNOWLEDGE_BASE",
            "AGENTS_CONFIG",
        ]
        | Omit = omit,
        version_constraint: deployment_package_install_async_params.VersionConstraint | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentPackageJob:
        """
        Install a deployment packages

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/v4/deployment-packages/{account_id}/install_async", account_id=account_id),
            body=maybe_transform(
                {
                    "deployment_package_id": deployment_package_id,
                    "deployment_package_name": deployment_package_name,
                    "deployment_package_type": deployment_package_type,
                    "version_constraint": version_constraint,
                },
                deployment_package_install_async_params.DeploymentPackageInstallAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentPackageJob,
        )


class AsyncDeploymentPackagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeploymentPackagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentPackagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentPackagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncDeploymentPackagesResourceWithStreamingResponse(self)

    async def install(
        self,
        account_id: str,
        *,
        deployment_package_id: str | Omit = omit,
        deployment_package_name: str | Omit = omit,
        deployment_package_type: Literal[
            "EGP_CONFIGURATION",
            "BLOB_STORAGE_FILE",
            "DOCKER_IMAGE",
            "EGP_ENTITY",
            "EGP_USER",
            "INTERNAL_MODEL_INFO",
            "EVALUATION_DATASET",
            "MODEL",
            "KNOWLEDGE_BASE",
            "AGENTS_CONFIG",
        ]
        | Omit = omit,
        version_constraint: deployment_package_install_params.VersionConstraint | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InstallDeploymentPackageResponse:
        """
        Install a deployment packages

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/v4/deployment-packages/{account_id}/install", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "deployment_package_id": deployment_package_id,
                    "deployment_package_name": deployment_package_name,
                    "deployment_package_type": deployment_package_type,
                    "version_constraint": version_constraint,
                },
                deployment_package_install_params.DeploymentPackageInstallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InstallDeploymentPackageResponse,
        )

    async def install_async(
        self,
        account_id: str,
        *,
        deployment_package_id: str | Omit = omit,
        deployment_package_name: str | Omit = omit,
        deployment_package_type: Literal[
            "EGP_CONFIGURATION",
            "BLOB_STORAGE_FILE",
            "DOCKER_IMAGE",
            "EGP_ENTITY",
            "EGP_USER",
            "INTERNAL_MODEL_INFO",
            "EVALUATION_DATASET",
            "MODEL",
            "KNOWLEDGE_BASE",
            "AGENTS_CONFIG",
        ]
        | Omit = omit,
        version_constraint: deployment_package_install_async_params.VersionConstraint | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentPackageJob:
        """
        Install a deployment packages

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/v4/deployment-packages/{account_id}/install_async", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "deployment_package_id": deployment_package_id,
                    "deployment_package_name": deployment_package_name,
                    "deployment_package_type": deployment_package_type,
                    "version_constraint": version_constraint,
                },
                deployment_package_install_async_params.DeploymentPackageInstallAsyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentPackageJob,
        )


class DeploymentPackagesResourceWithRawResponse:
    def __init__(self, deployment_packages: DeploymentPackagesResource) -> None:
        self._deployment_packages = deployment_packages

        self.install = to_raw_response_wrapper(
            deployment_packages.install,
        )
        self.install_async = to_raw_response_wrapper(
            deployment_packages.install_async,
        )


class AsyncDeploymentPackagesResourceWithRawResponse:
    def __init__(self, deployment_packages: AsyncDeploymentPackagesResource) -> None:
        self._deployment_packages = deployment_packages

        self.install = async_to_raw_response_wrapper(
            deployment_packages.install,
        )
        self.install_async = async_to_raw_response_wrapper(
            deployment_packages.install_async,
        )


class DeploymentPackagesResourceWithStreamingResponse:
    def __init__(self, deployment_packages: DeploymentPackagesResource) -> None:
        self._deployment_packages = deployment_packages

        self.install = to_streamed_response_wrapper(
            deployment_packages.install,
        )
        self.install_async = to_streamed_response_wrapper(
            deployment_packages.install_async,
        )


class AsyncDeploymentPackagesResourceWithStreamingResponse:
    def __init__(self, deployment_packages: AsyncDeploymentPackagesResource) -> None:
        self._deployment_packages = deployment_packages

        self.install = async_to_streamed_response_wrapper(
            deployment_packages.install,
        )
        self.install_async = async_to_streamed_response_wrapper(
            deployment_packages.install_async,
        )
