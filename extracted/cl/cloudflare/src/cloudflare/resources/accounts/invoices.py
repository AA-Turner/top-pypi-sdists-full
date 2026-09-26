# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

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
from ...types.accounts import invoice_edit_params
from ...types.accounts.invoice_edit_response import InvoiceEditResponse

__all__ = ["InvoicesResource", "AsyncInvoicesResource"]


class InvoicesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InvoicesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return InvoicesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InvoicesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return InvoicesResourceWithStreamingResponse(self)

    def edit(
        self,
        *,
        account_id: str,
        toggle: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InvoiceEditResponse:
        """
        Toggles PDF invoice generation for an account.

        Args:
          account_id: Identifier

          toggle: Whether to enable or disable PDF invoice generation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return cast(
            InvoiceEditResponse,
            self._patch(
                path_template("/accounts/{account_id}/invoices", account_id=account_id),
                body=maybe_transform({"toggle": toggle}, invoice_edit_params.InvoiceEditParams),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[InvoiceEditResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[InvoiceEditResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncInvoicesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInvoicesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInvoicesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInvoicesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncInvoicesResourceWithStreamingResponse(self)

    async def edit(
        self,
        *,
        account_id: str,
        toggle: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InvoiceEditResponse:
        """
        Toggles PDF invoice generation for an account.

        Args:
          account_id: Identifier

          toggle: Whether to enable or disable PDF invoice generation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return cast(
            InvoiceEditResponse,
            await self._patch(
                path_template("/accounts/{account_id}/invoices", account_id=account_id),
                body=await async_maybe_transform({"toggle": toggle}, invoice_edit_params.InvoiceEditParams),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[InvoiceEditResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[InvoiceEditResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class InvoicesResourceWithRawResponse:
    def __init__(self, invoices: InvoicesResource) -> None:
        self._invoices = invoices

        self.edit = to_raw_response_wrapper(
            invoices.edit,
        )


class AsyncInvoicesResourceWithRawResponse:
    def __init__(self, invoices: AsyncInvoicesResource) -> None:
        self._invoices = invoices

        self.edit = async_to_raw_response_wrapper(
            invoices.edit,
        )


class InvoicesResourceWithStreamingResponse:
    def __init__(self, invoices: InvoicesResource) -> None:
        self._invoices = invoices

        self.edit = to_streamed_response_wrapper(
            invoices.edit,
        )


class AsyncInvoicesResourceWithStreamingResponse:
    def __init__(self, invoices: AsyncInvoicesResource) -> None:
        self._invoices = invoices

        self.edit = async_to_streamed_response_wrapper(
            invoices.edit,
        )
