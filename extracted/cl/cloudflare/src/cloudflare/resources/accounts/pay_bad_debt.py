# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
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
from ...types.accounts import pay_bad_debt_create_params
from ...types.accounts.pay_bad_debt_create_response import PayBadDebtCreateResponse

__all__ = ["PayBadDebtResource", "AsyncPayBadDebtResource"]


class PayBadDebtResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PayBadDebtResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return PayBadDebtResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PayBadDebtResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return PayBadDebtResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        payment_method_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PayBadDebtCreateResponse:
        """Pays outstanding bad debt for an account.

        Discovers all debt automatically and
        handles invoice deduplication.

        Args:
          account_id: Identifier

          payment_method_id: The payment method to use. If omitted, the default payment method is used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/pay-bad-debt", account_id=account_id),
            body=maybe_transform(
                {"payment_method_id": payment_method_id}, pay_bad_debt_create_params.PayBadDebtCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PayBadDebtCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PayBadDebtCreateResponse], ResultWrapper[PayBadDebtCreateResponse]),
        )


class AsyncPayBadDebtResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPayBadDebtResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPayBadDebtResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPayBadDebtResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncPayBadDebtResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        payment_method_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PayBadDebtCreateResponse:
        """Pays outstanding bad debt for an account.

        Discovers all debt automatically and
        handles invoice deduplication.

        Args:
          account_id: Identifier

          payment_method_id: The payment method to use. If omitted, the default payment method is used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/pay-bad-debt", account_id=account_id),
            body=await async_maybe_transform(
                {"payment_method_id": payment_method_id}, pay_bad_debt_create_params.PayBadDebtCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PayBadDebtCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PayBadDebtCreateResponse], ResultWrapper[PayBadDebtCreateResponse]),
        )


class PayBadDebtResourceWithRawResponse:
    def __init__(self, pay_bad_debt: PayBadDebtResource) -> None:
        self._pay_bad_debt = pay_bad_debt

        self.create = to_raw_response_wrapper(
            pay_bad_debt.create,
        )


class AsyncPayBadDebtResourceWithRawResponse:
    def __init__(self, pay_bad_debt: AsyncPayBadDebtResource) -> None:
        self._pay_bad_debt = pay_bad_debt

        self.create = async_to_raw_response_wrapper(
            pay_bad_debt.create,
        )


class PayBadDebtResourceWithStreamingResponse:
    def __init__(self, pay_bad_debt: PayBadDebtResource) -> None:
        self._pay_bad_debt = pay_bad_debt

        self.create = to_streamed_response_wrapper(
            pay_bad_debt.create,
        )


class AsyncPayBadDebtResourceWithStreamingResponse:
    def __init__(self, pay_bad_debt: AsyncPayBadDebtResource) -> None:
        self._pay_bad_debt = pay_bad_debt

        self.create = async_to_streamed_response_wrapper(
            pay_bad_debt.create,
        )
