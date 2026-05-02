# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union

import httpx

from ..types import (
    application_deployment_list_params,
    application_deployment_create_params,
    application_deployment_update_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncPageResponse, AsyncPageResponse
from .._base_client import AsyncPaginator, make_request_options
from ..types.application_deployment import ApplicationDeployment

__all__ = ["ApplicationDeploymentsResource", "AsyncApplicationDeploymentsResource"]


class ApplicationDeploymentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationDeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationDeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationDeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationDeploymentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        application_variant_id: str,
        endpoint: str,
        is_active: bool,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationDeployment:
        """
        ### Description

        Creates a application deployment

        ### Details

        This API can be used to create a application deployment. To use this API, review
        the request schema and pass in all fields that are required to create a
        application deployment.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/application-deployments",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "application_variant_id": application_variant_id,
                    "endpoint": endpoint,
                    "is_active": is_active,
                    "name": name,
                },
                application_deployment_create_params.ApplicationDeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDeployment,
        )

    def retrieve(
        self,
        application_deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationDeployment:
        """
        ### Description

        Gets the details of a application deployment

        ### Details

        This API can be used to get information about a single application deployment by
        ID. To use this API, pass in the `id` that was returned from your Create
        Application Deployment API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `application_deployment_id` but received {application_deployment_id!r}"
            )
        return self._get(
            f"/v4/application-deployments/{application_deployment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDeployment,
        )

    def update(
        self,
        application_deployment_id: str,
        *,
        is_active: bool | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationDeployment:
        """
        ### Description

        Updates a application deployment

        ### Details

        This API can be used to update the application deployment that matches the ID
        that was passed in as a path parameter. To use this API, pass in the `id` that
        was returned from your Create Application Deployment API call as a path
        parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `application_deployment_id` but received {application_deployment_id!r}"
            )
        return self._patch(
            f"/v4/application-deployments/{application_deployment_id}",
            body=maybe_transform(
                {
                    "is_active": is_active,
                    "name": name,
                },
                application_deployment_update_params.ApplicationDeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDeployment,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_variant_id: Union[int, str] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[ApplicationDeployment]:
        """
        ### Description

        Lists all application deployments accessible to the user.

        ### Details

        This API can be used to list application deployments. If a user has access to
        multiple accounts, all application deployments from all accounts the user is
        associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/application-deployments",
            page=SyncPageResponse[ApplicationDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_variant_id": application_variant_id,
                        "limit": limit,
                        "page": page,
                    },
                    application_deployment_list_params.ApplicationDeploymentListParams,
                ),
            ),
            model=ApplicationDeployment,
        )


class AsyncApplicationDeploymentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationDeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationDeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationDeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationDeploymentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        application_variant_id: str,
        endpoint: str,
        is_active: bool,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationDeployment:
        """
        ### Description

        Creates a application deployment

        ### Details

        This API can be used to create a application deployment. To use this API, review
        the request schema and pass in all fields that are required to create a
        application deployment.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/application-deployments",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "application_variant_id": application_variant_id,
                    "endpoint": endpoint,
                    "is_active": is_active,
                    "name": name,
                },
                application_deployment_create_params.ApplicationDeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDeployment,
        )

    async def retrieve(
        self,
        application_deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationDeployment:
        """
        ### Description

        Gets the details of a application deployment

        ### Details

        This API can be used to get information about a single application deployment by
        ID. To use this API, pass in the `id` that was returned from your Create
        Application Deployment API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `application_deployment_id` but received {application_deployment_id!r}"
            )
        return await self._get(
            f"/v4/application-deployments/{application_deployment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDeployment,
        )

    async def update(
        self,
        application_deployment_id: str,
        *,
        is_active: bool | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationDeployment:
        """
        ### Description

        Updates a application deployment

        ### Details

        This API can be used to update the application deployment that matches the ID
        that was passed in as a path parameter. To use this API, pass in the `id` that
        was returned from your Create Application Deployment API call as a path
        parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `application_deployment_id` but received {application_deployment_id!r}"
            )
        return await self._patch(
            f"/v4/application-deployments/{application_deployment_id}",
            body=await async_maybe_transform(
                {
                    "is_active": is_active,
                    "name": name,
                },
                application_deployment_update_params.ApplicationDeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDeployment,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_variant_id: Union[int, str] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ApplicationDeployment, AsyncPageResponse[ApplicationDeployment]]:
        """
        ### Description

        Lists all application deployments accessible to the user.

        ### Details

        This API can be used to list application deployments. If a user has access to
        multiple accounts, all application deployments from all accounts the user is
        associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/application-deployments",
            page=AsyncPageResponse[ApplicationDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_variant_id": application_variant_id,
                        "limit": limit,
                        "page": page,
                    },
                    application_deployment_list_params.ApplicationDeploymentListParams,
                ),
            ),
            model=ApplicationDeployment,
        )


class ApplicationDeploymentsResourceWithRawResponse:
    def __init__(self, application_deployments: ApplicationDeploymentsResource) -> None:
        self._application_deployments = application_deployments

        self.create = to_raw_response_wrapper(
            application_deployments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            application_deployments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            application_deployments.update,
        )
        self.list = to_raw_response_wrapper(
            application_deployments.list,
        )


class AsyncApplicationDeploymentsResourceWithRawResponse:
    def __init__(self, application_deployments: AsyncApplicationDeploymentsResource) -> None:
        self._application_deployments = application_deployments

        self.create = async_to_raw_response_wrapper(
            application_deployments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            application_deployments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            application_deployments.update,
        )
        self.list = async_to_raw_response_wrapper(
            application_deployments.list,
        )


class ApplicationDeploymentsResourceWithStreamingResponse:
    def __init__(self, application_deployments: ApplicationDeploymentsResource) -> None:
        self._application_deployments = application_deployments

        self.create = to_streamed_response_wrapper(
            application_deployments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            application_deployments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            application_deployments.update,
        )
        self.list = to_streamed_response_wrapper(
            application_deployments.list,
        )


class AsyncApplicationDeploymentsResourceWithStreamingResponse:
    def __init__(self, application_deployments: AsyncApplicationDeploymentsResource) -> None:
        self._application_deployments = application_deployments

        self.create = async_to_streamed_response_wrapper(
            application_deployments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            application_deployments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            application_deployments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            application_deployments.list,
        )
