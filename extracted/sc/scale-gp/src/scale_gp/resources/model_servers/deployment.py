# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.model_servers.deployment_retrieve_response import DeploymentRetrieveResponse

__all__ = ["DeploymentResource", "AsyncDeploymentResource"]


class DeploymentResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeploymentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return DeploymentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return DeploymentResourceWithStreamingResponse(self)

    def retrieve(
        self,
        model_server_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentRetrieveResponse:
        """
        Get current deployment of the Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return self._get(
            f"/v4/serving/{model_server_id}/deployment",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentRetrieveResponse,
        )


class AsyncDeploymentResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeploymentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncDeploymentResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        model_server_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeploymentRetrieveResponse:
        """
        Get current deployment of the Model Server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_server_id:
            raise ValueError(f"Expected a non-empty value for `model_server_id` but received {model_server_id!r}")
        return await self._get(
            f"/v4/serving/{model_server_id}/deployment",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentRetrieveResponse,
        )


class DeploymentResourceWithRawResponse:
    def __init__(self, deployment: DeploymentResource) -> None:
        self._deployment = deployment

        self.retrieve = to_raw_response_wrapper(
            deployment.retrieve,
        )


class AsyncDeploymentResourceWithRawResponse:
    def __init__(self, deployment: AsyncDeploymentResource) -> None:
        self._deployment = deployment

        self.retrieve = async_to_raw_response_wrapper(
            deployment.retrieve,
        )


class DeploymentResourceWithStreamingResponse:
    def __init__(self, deployment: DeploymentResource) -> None:
        self._deployment = deployment

        self.retrieve = to_streamed_response_wrapper(
            deployment.retrieve,
        )


class AsyncDeploymentResourceWithStreamingResponse:
    def __init__(self, deployment: AsyncDeploymentResource) -> None:
        self._deployment = deployment

        self.retrieve = async_to_streamed_response_wrapper(
            deployment.retrieve,
        )
