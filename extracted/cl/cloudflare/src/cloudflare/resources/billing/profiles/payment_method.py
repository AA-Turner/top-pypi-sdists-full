# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._utils import path_template
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._wrappers import ResultWrapper
from ...._base_client import make_request_options
from ....types.billing.profiles.payment_method_create_response import PaymentMethodCreateResponse

__all__ = ["PaymentMethodResource", "AsyncPaymentMethodResource"]


class PaymentMethodResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PaymentMethodResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return PaymentMethodResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PaymentMethodResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return PaymentMethodResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodCreateResponse:
        """
        Creates a Stripe payment intent for adding or updating a payment method on the
        account's billing profile. Returns a client secret for frontend payment method
        collection.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/billing/profile/payment-method", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodCreateResponse], ResultWrapper[PaymentMethodCreateResponse]),
        )


class AsyncPaymentMethodResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPaymentMethodResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPaymentMethodResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPaymentMethodResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncPaymentMethodResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodCreateResponse:
        """
        Creates a Stripe payment intent for adding or updating a payment method on the
        account's billing profile. Returns a client secret for frontend payment method
        collection.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/billing/profile/payment-method", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodCreateResponse], ResultWrapper[PaymentMethodCreateResponse]),
        )


class PaymentMethodResourceWithRawResponse:
    def __init__(self, payment_method: PaymentMethodResource) -> None:
        self._payment_method = payment_method

        self.create = to_raw_response_wrapper(
            payment_method.create,
        )


class AsyncPaymentMethodResourceWithRawResponse:
    def __init__(self, payment_method: AsyncPaymentMethodResource) -> None:
        self._payment_method = payment_method

        self.create = async_to_raw_response_wrapper(
            payment_method.create,
        )


class PaymentMethodResourceWithStreamingResponse:
    def __init__(self, payment_method: PaymentMethodResource) -> None:
        self._payment_method = payment_method

        self.create = to_streamed_response_wrapper(
            payment_method.create,
        )


class AsyncPaymentMethodResourceWithStreamingResponse:
    def __init__(self, payment_method: AsyncPaymentMethodResource) -> None:
        self._payment_method = payment_method

        self.create = async_to_streamed_response_wrapper(
            payment_method.create,
        )
