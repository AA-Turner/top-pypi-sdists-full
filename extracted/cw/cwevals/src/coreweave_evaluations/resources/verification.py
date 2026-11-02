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
from ..types.verification_get_response import VerificationGetResponse

__all__ = ["VerificationResource", "AsyncVerificationResource"]


class VerificationResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VerificationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return VerificationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VerificationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return VerificationResourceWithStreamingResponse(self)

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VerificationGetResponse:
        """Get test"""
        return self._get(
            "/test",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationGetResponse,
        )


class AsyncVerificationResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVerificationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncVerificationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVerificationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncVerificationResourceWithStreamingResponse(self)

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VerificationGetResponse:
        """Get test"""
        return await self._get(
            "/test",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationGetResponse,
        )


class VerificationResourceWithRawResponse:
    def __init__(self, verification: VerificationResource) -> None:
        self._verification = verification

        self.get = to_raw_response_wrapper(
            verification.get,
        )


class AsyncVerificationResourceWithRawResponse:
    def __init__(self, verification: AsyncVerificationResource) -> None:
        self._verification = verification

        self.get = async_to_raw_response_wrapper(
            verification.get,
        )


class VerificationResourceWithStreamingResponse:
    def __init__(self, verification: VerificationResource) -> None:
        self._verification = verification

        self.get = to_streamed_response_wrapper(
            verification.get,
        )


class AsyncVerificationResourceWithStreamingResponse:
    def __init__(self, verification: AsyncVerificationResource) -> None:
        self._verification = verification

        self.get = async_to_streamed_response_wrapper(
            verification.get,
        )
