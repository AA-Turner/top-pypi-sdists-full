# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
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
from ....types.accounts.subscriptions import cancel_reason_create_params
from ....types.accounts.subscriptions.cancel_reason_get_response import CancelReasonGetResponse
from ....types.accounts.subscriptions.cancel_reason_create_response import CancelReasonCreateResponse

__all__ = ["CancelReasonResource", "AsyncCancelReasonResource"]


class CancelReasonResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CancelReasonResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return CancelReasonResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CancelReasonResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return CancelReasonResourceWithStreamingResponse(self)

    def create(
        self,
        subscription_identifier: str,
        *,
        account_id: str,
        other: str | Omit = omit,
        reason_code: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CancelReasonCreateResponse:
        """
        Records a cancellation reason for an account subscription.

        Args:
          account_id: Identifier

          subscription_identifier: Subscription identifier tag.

          other: Additional cancellation details.

          reason_code: The cancellation reason codes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not subscription_identifier:
            raise ValueError(
                f"Expected a non-empty value for `subscription_identifier` but received {subscription_identifier!r}"
            )
        return self._post(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}/cancel-reason",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            body=maybe_transform(
                {
                    "other": other,
                    "reason_code": reason_code,
                },
                cancel_reason_create_params.CancelReasonCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[CancelReasonCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[CancelReasonCreateResponse], ResultWrapper[CancelReasonCreateResponse]),
        )

    def get(
        self,
        subscription_identifier: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CancelReasonGetResponse:
        """
        Gets the cancellation reason for an account subscription.

        Args:
          account_id: Identifier

          subscription_identifier: Subscription identifier tag.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not subscription_identifier:
            raise ValueError(
                f"Expected a non-empty value for `subscription_identifier` but received {subscription_identifier!r}"
            )
        return self._get(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}/cancel-reason",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[CancelReasonGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[CancelReasonGetResponse], ResultWrapper[CancelReasonGetResponse]),
        )


class AsyncCancelReasonResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCancelReasonResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCancelReasonResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCancelReasonResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncCancelReasonResourceWithStreamingResponse(self)

    async def create(
        self,
        subscription_identifier: str,
        *,
        account_id: str,
        other: str | Omit = omit,
        reason_code: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CancelReasonCreateResponse:
        """
        Records a cancellation reason for an account subscription.

        Args:
          account_id: Identifier

          subscription_identifier: Subscription identifier tag.

          other: Additional cancellation details.

          reason_code: The cancellation reason codes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not subscription_identifier:
            raise ValueError(
                f"Expected a non-empty value for `subscription_identifier` but received {subscription_identifier!r}"
            )
        return await self._post(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}/cancel-reason",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            body=await async_maybe_transform(
                {
                    "other": other,
                    "reason_code": reason_code,
                },
                cancel_reason_create_params.CancelReasonCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[CancelReasonCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[CancelReasonCreateResponse], ResultWrapper[CancelReasonCreateResponse]),
        )

    async def get(
        self,
        subscription_identifier: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CancelReasonGetResponse:
        """
        Gets the cancellation reason for an account subscription.

        Args:
          account_id: Identifier

          subscription_identifier: Subscription identifier tag.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not subscription_identifier:
            raise ValueError(
                f"Expected a non-empty value for `subscription_identifier` but received {subscription_identifier!r}"
            )
        return await self._get(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}/cancel-reason",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[CancelReasonGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[CancelReasonGetResponse], ResultWrapper[CancelReasonGetResponse]),
        )


class CancelReasonResourceWithRawResponse:
    def __init__(self, cancel_reason: CancelReasonResource) -> None:
        self._cancel_reason = cancel_reason

        self.create = to_raw_response_wrapper(
            cancel_reason.create,
        )
        self.get = to_raw_response_wrapper(
            cancel_reason.get,
        )


class AsyncCancelReasonResourceWithRawResponse:
    def __init__(self, cancel_reason: AsyncCancelReasonResource) -> None:
        self._cancel_reason = cancel_reason

        self.create = async_to_raw_response_wrapper(
            cancel_reason.create,
        )
        self.get = async_to_raw_response_wrapper(
            cancel_reason.get,
        )


class CancelReasonResourceWithStreamingResponse:
    def __init__(self, cancel_reason: CancelReasonResource) -> None:
        self._cancel_reason = cancel_reason

        self.create = to_streamed_response_wrapper(
            cancel_reason.create,
        )
        self.get = to_streamed_response_wrapper(
            cancel_reason.get,
        )


class AsyncCancelReasonResourceWithStreamingResponse:
    def __init__(self, cancel_reason: AsyncCancelReasonResource) -> None:
        self._cancel_reason = cancel_reason

        self.create = async_to_streamed_response_wrapper(
            cancel_reason.create,
        )
        self.get = async_to_streamed_response_wrapper(
            cancel_reason.get,
        )
