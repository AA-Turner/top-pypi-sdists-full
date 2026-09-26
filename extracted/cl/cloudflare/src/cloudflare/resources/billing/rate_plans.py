# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._wrappers import ResultWrapper
from ..._base_client import make_request_options
from ...types.billing.rate_plan_get_response import RatePlanGetResponse

__all__ = ["RatePlansResource", "AsyncRatePlansResource"]


class RatePlansResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RatePlansResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return RatePlansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RatePlansResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return RatePlansResourceWithStreamingResponse(self)

    def get(
        self,
        public_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RatePlanGetResponse:
        """
        Gets a rate plan's details by its public key (e.g., 'teams_free',
        'cf_pro_20_20'). This is a public catalog endpoint, so authentication is not
        enforced and credentials are accepted but not required.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not public_key:
            raise ValueError(f"Expected a non-empty value for `public_key` but received {public_key!r}")
        return self._get(
            path_template("/billing/rate_plans/{public_key}", public_key=public_key),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[RatePlanGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[RatePlanGetResponse], ResultWrapper[RatePlanGetResponse]),
        )


class AsyncRatePlansResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRatePlansResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRatePlansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRatePlansResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncRatePlansResourceWithStreamingResponse(self)

    async def get(
        self,
        public_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RatePlanGetResponse:
        """
        Gets a rate plan's details by its public key (e.g., 'teams_free',
        'cf_pro_20_20'). This is a public catalog endpoint, so authentication is not
        enforced and credentials are accepted but not required.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not public_key:
            raise ValueError(f"Expected a non-empty value for `public_key` but received {public_key!r}")
        return await self._get(
            path_template("/billing/rate_plans/{public_key}", public_key=public_key),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[RatePlanGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[RatePlanGetResponse], ResultWrapper[RatePlanGetResponse]),
        )


class RatePlansResourceWithRawResponse:
    def __init__(self, rate_plans: RatePlansResource) -> None:
        self._rate_plans = rate_plans

        self.get = to_raw_response_wrapper(
            rate_plans.get,
        )


class AsyncRatePlansResourceWithRawResponse:
    def __init__(self, rate_plans: AsyncRatePlansResource) -> None:
        self._rate_plans = rate_plans

        self.get = async_to_raw_response_wrapper(
            rate_plans.get,
        )


class RatePlansResourceWithStreamingResponse:
    def __init__(self, rate_plans: RatePlansResource) -> None:
        self._rate_plans = rate_plans

        self.get = to_streamed_response_wrapper(
            rate_plans.get,
        )


class AsyncRatePlansResourceWithStreamingResponse:
    def __init__(self, rate_plans: AsyncRatePlansResource) -> None:
        self._rate_plans = rate_plans

        self.get = async_to_streamed_response_wrapper(
            rate_plans.get,
        )
