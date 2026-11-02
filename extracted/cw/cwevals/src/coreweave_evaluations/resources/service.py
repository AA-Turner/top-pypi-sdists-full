# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.service_get_response import ServiceGetResponse

__all__ = ["ServiceResource", "AsyncServiceResource"]


class ServiceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ServiceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return ServiceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ServiceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return ServiceResourceWithStreamingResponse(self)

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceGetResponse:
        """Get"""
        return self._get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceGetResponse,
        )


class AsyncServiceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncServiceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncServiceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncServiceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncServiceResourceWithStreamingResponse(self)

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceGetResponse:
        """Get"""
        return await self._get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceGetResponse,
        )


class ServiceResourceWithRawResponse:
    def __init__(self, service: ServiceResource) -> None:
        self._service = service

        self.get = to_raw_response_wrapper(
            service.get,
        )


class AsyncServiceResourceWithRawResponse:
    def __init__(self, service: AsyncServiceResource) -> None:
        self._service = service

        self.get = async_to_raw_response_wrapper(
            service.get,
        )


class ServiceResourceWithStreamingResponse:
    def __init__(self, service: ServiceResource) -> None:
        self._service = service

        self.get = to_streamed_response_wrapper(
            service.get,
        )


class AsyncServiceResourceWithStreamingResponse:
    def __init__(self, service: AsyncServiceResource) -> None:
        self._service = service

        self.get = async_to_streamed_response_wrapper(
            service.get,
        )
