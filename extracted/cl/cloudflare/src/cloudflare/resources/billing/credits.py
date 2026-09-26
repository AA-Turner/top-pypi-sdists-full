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
from ...types.billing.credit_get_response import CreditGetResponse

__all__ = ["CreditsResource", "AsyncCreditsResource"]


class CreditsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CreditsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return CreditsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CreditsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return CreditsResourceWithStreamingResponse(self)

    def get(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CreditGetResponse:
        """
        Gets the credit balance and eligibility for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            path_template("/accounts/{account_id}/billing/credits", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[CreditGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[CreditGetResponse], ResultWrapper[CreditGetResponse]),
        )


class AsyncCreditsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCreditsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCreditsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCreditsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncCreditsResourceWithStreamingResponse(self)

    async def get(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CreditGetResponse:
        """
        Gets the credit balance and eligibility for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            path_template("/accounts/{account_id}/billing/credits", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[CreditGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[CreditGetResponse], ResultWrapper[CreditGetResponse]),
        )


class CreditsResourceWithRawResponse:
    def __init__(self, credits: CreditsResource) -> None:
        self._credits = credits

        self.get = to_raw_response_wrapper(
            credits.get,
        )


class AsyncCreditsResourceWithRawResponse:
    def __init__(self, credits: AsyncCreditsResource) -> None:
        self._credits = credits

        self.get = async_to_raw_response_wrapper(
            credits.get,
        )


class CreditsResourceWithStreamingResponse:
    def __init__(self, credits: CreditsResource) -> None:
        self._credits = credits

        self.get = to_streamed_response_wrapper(
            credits.get,
        )


class AsyncCreditsResourceWithStreamingResponse:
    def __init__(self, credits: AsyncCreditsResource) -> None:
        self._credits = credits

        self.get = async_to_streamed_response_wrapper(
            credits.get,
        )
