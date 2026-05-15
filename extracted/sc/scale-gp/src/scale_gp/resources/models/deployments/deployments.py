# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPageResponse, AsyncPageResponse
from ...._base_client import AsyncPaginator, make_request_options
from ....types.models import (
    deployment_list_params,
    deployment_create_params,
    deployment_update_params,
    deployment_execute_params,
    deployment_list_all_params,
)
from .usage_statistics import (
    UsageStatisticsResource,
    AsyncUsageStatisticsResource,
    UsageStatisticsResourceWithRawResponse,
    AsyncUsageStatisticsResourceWithRawResponse,
    UsageStatisticsResourceWithStreamingResponse,
    AsyncUsageStatisticsResourceWithStreamingResponse,
)
from ....types.models.model_deployment import ModelDeployment
from ....types.shared.generic_delete_response import GenericDeleteResponse

__all__ = ["DeploymentsResource", "AsyncDeploymentsResource"]


class DeploymentsResource(SyncAPIResource):
    """Model API."""

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResource:
        """Model API."""
        return UsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return DeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return DeploymentsResourceWithStreamingResponse(self)

    def create(
        self,
        model_instance_id: str,
        *,
        name: str,
        account_id: str | Omit = omit,
        deployment_metadata: Dict[str, object] | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        vendor_configuration: deployment_create_params.VendorConfiguration | Omit = omit,
        wait_for_ready: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeployment:
        """
        ### Description

        Model Deployments are unique endpoints created for custom models in the Scale
        GenAI Platform. They enable users to interact with and utilize specific
        instances of models through the API/SDK. Each deployment is associated with a
        model instance, containing the necessary model template and model-metadata.
        Model templates describe the creation parameters that are configured on the
        deployment. The model deployments provide a means to call upon models for
        inference, logging calls, and monitoring usage.

        Built-in models also have deployments for creating a consistent interface for
        all models. But they don't represent a real deployment, they are just a way to
        interact with the built-in models. These deployments are created automatically
        when the model is created and they are immutable.

        ### Endpoint details

        This endpoint is used to deploy a model instance. The request payload schema
        depends on the `model_request_parameters_schema` of the Model Template that the
        created model was created from.

        Args:
          account_id: The ID of the account that owns the given entity.

          wait_for_ready: If true, the request will block until the Launch endpoint is READY. Defaults to
              true.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        return self._post(
            path_template("/v4/models/{model_instance_id}/deployments", model_instance_id=model_instance_id),
            body=maybe_transform(
                {
                    "name": name,
                    "account_id": account_id,
                    "deployment_metadata": deployment_metadata,
                    "model_creation_parameters": model_creation_parameters,
                    "vendor_configuration": vendor_configuration,
                    "wait_for_ready": wait_for_ready,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeployment,
        )

    def retrieve(
        self,
        deployment_id: str,
        *,
        model_instance_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeployment:
        """
        ### Description

        Gets the details of a deployment

        ### Details

        This API can be used to get information about a single deployment by ID. To use
        this API, pass in the `id` that was returned from your Create Deployment API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{deployment_id}",
                model_instance_id=model_instance_id,
                deployment_id=deployment_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeployment,
        )

    def update(
        self,
        deployment_id: str,
        *,
        model_instance_id: str,
        deployment_metadata: Dict[str, object] | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        vendor_configuration: deployment_update_params.VendorConfiguration | Omit = omit,
        wait_for_ready: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeployment:
        """
        ### Description

        Updates a deployment

        ### Details

        This API can be used to update the deployment that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Deployment API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          wait_for_ready: If true, the request will block until the Launch endpoint is READY. Defaults to
              true.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._patch(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{deployment_id}",
                model_instance_id=model_instance_id,
                deployment_id=deployment_id,
            ),
            body=maybe_transform(
                {
                    "deployment_metadata": deployment_metadata,
                    "model_creation_parameters": model_creation_parameters,
                    "name": name,
                    "vendor_configuration": vendor_configuration,
                    "wait_for_ready": wait_for_ready,
                },
                deployment_update_params.DeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeployment,
        )

    def list(
        self,
        model_instance_id: str,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_endpoint_id:asc",
                "model_endpoint_id:desc",
                "model_instance_id:asc",
                "model_instance_id:desc",
                "vendor_configuration:asc",
                "vendor_configuration:desc",
                "deployment_metadata:asc",
                "deployment_metadata:desc",
                "status:asc",
                "status:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "name:asc",
                "name:desc",
            ]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[ModelDeployment]:
        """
        TODO: Document

        Args:
          account_id: Optional filter by account id

          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        return self._get_api_list(
            path_template("/v4/models/{model_instance_id}/deployments", model_instance_id=model_instance_id),
            page=SyncPageResponse[ModelDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                        "sort_by": sort_by,
                    },
                    deployment_list_params.DeploymentListParams,
                ),
            ),
            model=ModelDeployment,
        )

    def delete(
        self,
        deployment_id: str,
        *,
        model_instance_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a deployment

        ### Details

        This API can be used to delete a deployment by ID. To use this API, pass in the
        `id` that was returned from your Create Deployment API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._delete(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{deployment_id}",
                model_instance_id=model_instance_id,
                deployment_id=deployment_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    def execute(
        self,
        model_deployment_id: str,
        *,
        model_instance_id: str,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Execute Model Deployment

        Args:
          stream: Flag indicating whether to stream the completion response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not model_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `model_deployment_id` but received {model_deployment_id!r}"
            )
        return self._post(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{model_deployment_id}/execute",
                model_instance_id=model_instance_id,
                model_deployment_id=model_deployment_id,
            ),
            body=maybe_transform({"stream": stream}, deployment_execute_params.DeploymentExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def list_all(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_endpoint_id:asc",
                "model_endpoint_id:desc",
                "model_instance_id:asc",
                "model_instance_id:desc",
                "vendor_configuration:asc",
                "vendor_configuration:desc",
                "deployment_metadata:asc",
                "deployment_metadata:desc",
                "status:asc",
                "status:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "name:asc",
                "name:desc",
            ]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[ModelDeployment]:
        """
        TODO: Document

        Args:
          account_id: Optional filter by account id

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
            "/v4/model-deployments",
            page=SyncPageResponse[ModelDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                        "sort_by": sort_by,
                    },
                    deployment_list_all_params.DeploymentListAllParams,
                ),
            ),
            model=ModelDeployment,
        )


class AsyncDeploymentsResource(AsyncAPIResource):
    """Model API."""

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResource:
        """Model API."""
        return AsyncUsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncDeploymentsResourceWithStreamingResponse(self)

    async def create(
        self,
        model_instance_id: str,
        *,
        name: str,
        account_id: str | Omit = omit,
        deployment_metadata: Dict[str, object] | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        vendor_configuration: deployment_create_params.VendorConfiguration | Omit = omit,
        wait_for_ready: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeployment:
        """
        ### Description

        Model Deployments are unique endpoints created for custom models in the Scale
        GenAI Platform. They enable users to interact with and utilize specific
        instances of models through the API/SDK. Each deployment is associated with a
        model instance, containing the necessary model template and model-metadata.
        Model templates describe the creation parameters that are configured on the
        deployment. The model deployments provide a means to call upon models for
        inference, logging calls, and monitoring usage.

        Built-in models also have deployments for creating a consistent interface for
        all models. But they don't represent a real deployment, they are just a way to
        interact with the built-in models. These deployments are created automatically
        when the model is created and they are immutable.

        ### Endpoint details

        This endpoint is used to deploy a model instance. The request payload schema
        depends on the `model_request_parameters_schema` of the Model Template that the
        created model was created from.

        Args:
          account_id: The ID of the account that owns the given entity.

          wait_for_ready: If true, the request will block until the Launch endpoint is READY. Defaults to
              true.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        return await self._post(
            path_template("/v4/models/{model_instance_id}/deployments", model_instance_id=model_instance_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "account_id": account_id,
                    "deployment_metadata": deployment_metadata,
                    "model_creation_parameters": model_creation_parameters,
                    "vendor_configuration": vendor_configuration,
                    "wait_for_ready": wait_for_ready,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeployment,
        )

    async def retrieve(
        self,
        deployment_id: str,
        *,
        model_instance_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeployment:
        """
        ### Description

        Gets the details of a deployment

        ### Details

        This API can be used to get information about a single deployment by ID. To use
        this API, pass in the `id` that was returned from your Create Deployment API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{deployment_id}",
                model_instance_id=model_instance_id,
                deployment_id=deployment_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeployment,
        )

    async def update(
        self,
        deployment_id: str,
        *,
        model_instance_id: str,
        deployment_metadata: Dict[str, object] | Omit = omit,
        model_creation_parameters: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        vendor_configuration: deployment_update_params.VendorConfiguration | Omit = omit,
        wait_for_ready: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelDeployment:
        """
        ### Description

        Updates a deployment

        ### Details

        This API can be used to update the deployment that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Deployment API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          wait_for_ready: If true, the request will block until the Launch endpoint is READY. Defaults to
              true.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._patch(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{deployment_id}",
                model_instance_id=model_instance_id,
                deployment_id=deployment_id,
            ),
            body=await async_maybe_transform(
                {
                    "deployment_metadata": deployment_metadata,
                    "model_creation_parameters": model_creation_parameters,
                    "name": name,
                    "vendor_configuration": vendor_configuration,
                    "wait_for_ready": wait_for_ready,
                },
                deployment_update_params.DeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelDeployment,
        )

    def list(
        self,
        model_instance_id: str,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_endpoint_id:asc",
                "model_endpoint_id:desc",
                "model_instance_id:asc",
                "model_instance_id:desc",
                "vendor_configuration:asc",
                "vendor_configuration:desc",
                "deployment_metadata:asc",
                "deployment_metadata:desc",
                "status:asc",
                "status:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "name:asc",
                "name:desc",
            ]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ModelDeployment, AsyncPageResponse[ModelDeployment]]:
        """
        TODO: Document

        Args:
          account_id: Optional filter by account id

          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        return self._get_api_list(
            path_template("/v4/models/{model_instance_id}/deployments", model_instance_id=model_instance_id),
            page=AsyncPageResponse[ModelDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                        "sort_by": sort_by,
                    },
                    deployment_list_params.DeploymentListParams,
                ),
            ),
            model=ModelDeployment,
        )

    async def delete(
        self,
        deployment_id: str,
        *,
        model_instance_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a deployment

        ### Details

        This API can be used to delete a deployment by ID. To use this API, pass in the
        `id` that was returned from your Create Deployment API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._delete(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{deployment_id}",
                model_instance_id=model_instance_id,
                deployment_id=deployment_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    async def execute(
        self,
        model_deployment_id: str,
        *,
        model_instance_id: str,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Execute Model Deployment

        Args:
          stream: Flag indicating whether to stream the completion response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_instance_id:
            raise ValueError(f"Expected a non-empty value for `model_instance_id` but received {model_instance_id!r}")
        if not model_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `model_deployment_id` but received {model_deployment_id!r}"
            )
        return await self._post(
            path_template(
                "/v4/models/{model_instance_id}/deployments/{model_deployment_id}/execute",
                model_instance_id=model_instance_id,
                model_deployment_id=model_deployment_id,
            ),
            body=await async_maybe_transform({"stream": stream}, deployment_execute_params.DeploymentExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def list_all(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_endpoint_id:asc",
                "model_endpoint_id:desc",
                "model_instance_id:asc",
                "model_instance_id:desc",
                "vendor_configuration:asc",
                "vendor_configuration:desc",
                "deployment_metadata:asc",
                "deployment_metadata:desc",
                "status:asc",
                "status:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "name:asc",
                "name:desc",
            ]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ModelDeployment, AsyncPageResponse[ModelDeployment]]:
        """
        TODO: Document

        Args:
          account_id: Optional filter by account id

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
            "/v4/model-deployments",
            page=AsyncPageResponse[ModelDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                        "sort_by": sort_by,
                    },
                    deployment_list_all_params.DeploymentListAllParams,
                ),
            ),
            model=ModelDeployment,
        )


class DeploymentsResourceWithRawResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.create = to_raw_response_wrapper(
            deployments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            deployments.update,
        )
        self.list = to_raw_response_wrapper(
            deployments.list,
        )
        self.delete = to_raw_response_wrapper(
            deployments.delete,
        )
        self.execute = to_raw_response_wrapper(
            deployments.execute,
        )
        self.list_all = to_raw_response_wrapper(
            deployments.list_all,
        )

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithRawResponse:
        """Model API."""
        return UsageStatisticsResourceWithRawResponse(self._deployments.usage_statistics)


class AsyncDeploymentsResourceWithRawResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.create = async_to_raw_response_wrapper(
            deployments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            deployments.update,
        )
        self.list = async_to_raw_response_wrapper(
            deployments.list,
        )
        self.delete = async_to_raw_response_wrapper(
            deployments.delete,
        )
        self.execute = async_to_raw_response_wrapper(
            deployments.execute,
        )
        self.list_all = async_to_raw_response_wrapper(
            deployments.list_all,
        )

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithRawResponse:
        """Model API."""
        return AsyncUsageStatisticsResourceWithRawResponse(self._deployments.usage_statistics)


class DeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.create = to_streamed_response_wrapper(
            deployments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            deployments.update,
        )
        self.list = to_streamed_response_wrapper(
            deployments.list,
        )
        self.delete = to_streamed_response_wrapper(
            deployments.delete,
        )
        self.execute = to_streamed_response_wrapper(
            deployments.execute,
        )
        self.list_all = to_streamed_response_wrapper(
            deployments.list_all,
        )

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithStreamingResponse:
        """Model API."""
        return UsageStatisticsResourceWithStreamingResponse(self._deployments.usage_statistics)


class AsyncDeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.create = async_to_streamed_response_wrapper(
            deployments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            deployments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            deployments.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            deployments.delete,
        )
        self.execute = async_to_streamed_response_wrapper(
            deployments.execute,
        )
        self.list_all = async_to_streamed_response_wrapper(
            deployments.list_all,
        )

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithStreamingResponse:
        """Model API."""
        return AsyncUsageStatisticsResourceWithStreamingResponse(self._deployments.usage_statistics)
