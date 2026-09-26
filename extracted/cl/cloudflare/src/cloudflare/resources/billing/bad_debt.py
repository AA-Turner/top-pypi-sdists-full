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
from ...types.billing.bad_debt_get_response import BadDebtGetResponse

__all__ = ["BadDebtResource", "AsyncBadDebtResource"]


class BadDebtResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BadDebtResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return BadDebtResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BadDebtResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return BadDebtResourceWithStreamingResponse(self)

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
    ) -> BadDebtGetResponse:
        """
        Gets bad debt information for an account, including outstanding invoices and
        total debt amount.

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
            path_template("/accounts/{account_id}/billing/bad-debt", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BadDebtGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[BadDebtGetResponse], ResultWrapper[BadDebtGetResponse]),
        )


class AsyncBadDebtResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBadDebtResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBadDebtResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBadDebtResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncBadDebtResourceWithStreamingResponse(self)

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
    ) -> BadDebtGetResponse:
        """
        Gets bad debt information for an account, including outstanding invoices and
        total debt amount.

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
            path_template("/accounts/{account_id}/billing/bad-debt", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BadDebtGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[BadDebtGetResponse], ResultWrapper[BadDebtGetResponse]),
        )


class BadDebtResourceWithRawResponse:
    def __init__(self, bad_debt: BadDebtResource) -> None:
        self._bad_debt = bad_debt

        self.get = to_raw_response_wrapper(
            bad_debt.get,
        )


class AsyncBadDebtResourceWithRawResponse:
    def __init__(self, bad_debt: AsyncBadDebtResource) -> None:
        self._bad_debt = bad_debt

        self.get = async_to_raw_response_wrapper(
            bad_debt.get,
        )


class BadDebtResourceWithStreamingResponse:
    def __init__(self, bad_debt: BadDebtResource) -> None:
        self._bad_debt = bad_debt

        self.get = to_streamed_response_wrapper(
            bad_debt.get,
        )


class AsyncBadDebtResourceWithStreamingResponse:
    def __init__(self, bad_debt: AsyncBadDebtResource) -> None:
        self._bad_debt = bad_debt

        self.get = async_to_streamed_response_wrapper(
            bad_debt.get,
        )
