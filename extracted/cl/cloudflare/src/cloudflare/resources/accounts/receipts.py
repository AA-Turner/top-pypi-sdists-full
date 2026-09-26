# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.accounts import receipt_pdf_params

__all__ = ["ReceiptsResource", "AsyncReceiptsResource"]


class ReceiptsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ReceiptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return ReceiptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReceiptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return ReceiptsResourceWithStreamingResponse(self)

    def pdf(
        self,
        receipt_id: str,
        *,
        account_id: str,
        doctype: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Downloads a receipt as a PDF document.

        Args:
          account_id: Identifier

          receipt_id: Identifier

          doctype: The document type to generate.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not receipt_id:
            raise ValueError(f"Expected a non-empty value for `receipt_id` but received {receipt_id!r}")
        extra_headers = {"Accept": "application/pdf", **(extra_headers or {})}
        return self._get(
            path_template(
                "/accounts/{account_id}/receipts/{receipt_id}/pdf", account_id=account_id, receipt_id=receipt_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"doctype": doctype}, receipt_pdf_params.ReceiptPDFParams),
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncReceiptsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncReceiptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncReceiptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReceiptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncReceiptsResourceWithStreamingResponse(self)

    async def pdf(
        self,
        receipt_id: str,
        *,
        account_id: str,
        doctype: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Downloads a receipt as a PDF document.

        Args:
          account_id: Identifier

          receipt_id: Identifier

          doctype: The document type to generate.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not receipt_id:
            raise ValueError(f"Expected a non-empty value for `receipt_id` but received {receipt_id!r}")
        extra_headers = {"Accept": "application/pdf", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/accounts/{account_id}/receipts/{receipt_id}/pdf", account_id=account_id, receipt_id=receipt_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"doctype": doctype}, receipt_pdf_params.ReceiptPDFParams),
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ReceiptsResourceWithRawResponse:
    def __init__(self, receipts: ReceiptsResource) -> None:
        self._receipts = receipts

        self.pdf = to_custom_raw_response_wrapper(
            receipts.pdf,
            BinaryAPIResponse,
        )


class AsyncReceiptsResourceWithRawResponse:
    def __init__(self, receipts: AsyncReceiptsResource) -> None:
        self._receipts = receipts

        self.pdf = async_to_custom_raw_response_wrapper(
            receipts.pdf,
            AsyncBinaryAPIResponse,
        )


class ReceiptsResourceWithStreamingResponse:
    def __init__(self, receipts: ReceiptsResource) -> None:
        self._receipts = receipts

        self.pdf = to_custom_streamed_response_wrapper(
            receipts.pdf,
            StreamedBinaryAPIResponse,
        )


class AsyncReceiptsResourceWithStreamingResponse:
    def __init__(self, receipts: AsyncReceiptsResource) -> None:
        self._receipts = receipts

        self.pdf = async_to_custom_streamed_response_wrapper(
            receipts.pdf,
            AsyncStreamedBinaryAPIResponse,
        )
