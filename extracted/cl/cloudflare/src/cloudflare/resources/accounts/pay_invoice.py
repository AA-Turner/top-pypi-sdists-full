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
from ...types.accounts import pay_invoice_create_params
from ...types.accounts.pay_invoice_create_response import PayInvoiceCreateResponse

__all__ = ["PayInvoiceResource", "AsyncPayInvoiceResource"]


class PayInvoiceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PayInvoiceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return PayInvoiceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PayInvoiceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return PayInvoiceResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        invoice_id: str | Omit = omit,
        payment_method_id: str | Omit = omit,
        validate_payment_method: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PayInvoiceCreateResponse:
        """Pays an outstanding invoice for an account.

        Returns a Stripe client secret when
        Strong Customer Authentication (SCA) is required to complete the payment.

        Args:
          account_id: Identifier

          invoice_id: The identifier of the invoice to pay.

          payment_method_id: The payment method to use. If omitted, the default payment method is used.

          validate_payment_method: Whether to validate the payment method before processing.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/pay-invoice", account_id=account_id),
            body=maybe_transform(
                {
                    "invoice_id": invoice_id,
                    "payment_method_id": payment_method_id,
                    "validate_payment_method": validate_payment_method,
                },
                pay_invoice_create_params.PayInvoiceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PayInvoiceCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PayInvoiceCreateResponse], ResultWrapper[PayInvoiceCreateResponse]),
        )


class AsyncPayInvoiceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPayInvoiceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPayInvoiceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPayInvoiceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncPayInvoiceResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        invoice_id: str | Omit = omit,
        payment_method_id: str | Omit = omit,
        validate_payment_method: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PayInvoiceCreateResponse:
        """Pays an outstanding invoice for an account.

        Returns a Stripe client secret when
        Strong Customer Authentication (SCA) is required to complete the payment.

        Args:
          account_id: Identifier

          invoice_id: The identifier of the invoice to pay.

          payment_method_id: The payment method to use. If omitted, the default payment method is used.

          validate_payment_method: Whether to validate the payment method before processing.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/pay-invoice", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "invoice_id": invoice_id,
                    "payment_method_id": payment_method_id,
                    "validate_payment_method": validate_payment_method,
                },
                pay_invoice_create_params.PayInvoiceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PayInvoiceCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PayInvoiceCreateResponse], ResultWrapper[PayInvoiceCreateResponse]),
        )


class PayInvoiceResourceWithRawResponse:
    def __init__(self, pay_invoice: PayInvoiceResource) -> None:
        self._pay_invoice = pay_invoice

        self.create = to_raw_response_wrapper(
            pay_invoice.create,
        )


class AsyncPayInvoiceResourceWithRawResponse:
    def __init__(self, pay_invoice: AsyncPayInvoiceResource) -> None:
        self._pay_invoice = pay_invoice

        self.create = async_to_raw_response_wrapper(
            pay_invoice.create,
        )


class PayInvoiceResourceWithStreamingResponse:
    def __init__(self, pay_invoice: PayInvoiceResource) -> None:
        self._pay_invoice = pay_invoice

        self.create = to_streamed_response_wrapper(
            pay_invoice.create,
        )


class AsyncPayInvoiceResourceWithStreamingResponse:
    def __init__(self, pay_invoice: AsyncPayInvoiceResource) -> None:
        self._pay_invoice = pay_invoice

        self.create = async_to_streamed_response_wrapper(
            pay_invoice.create,
        )
