# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ....types.shared.subscription import Subscription
from ....types.accounts.subscriptions import action_append_params
from ....types.shared_params.rate_plan import RatePlan

__all__ = ["ActionsResource", "AsyncActionsResource"]


class ActionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ActionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return ActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ActionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return ActionsResourceWithStreamingResponse(self)

    def append(
        self,
        subscription_identifier: str,
        *,
        account_id: str,
        frequency: Literal["weekly", "monthly", "quarterly", "yearly"] | Omit = omit,
        rate_plan: RatePlan | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Subscription:
        """
        Smartly applies the incoming subscription into the lifecycle of the
        subscription.

        Args:
          account_id: Identifier

          subscription_identifier: Subscription identifier tag.

          frequency: How often the subscription is renewed automatically.

          rate_plan: The rate plan applied to the subscription.

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
                "/accounts/{account_id}/subscriptions/{subscription_identifier}/action/append",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            body=maybe_transform(
                {
                    "frequency": frequency,
                    "rate_plan": rate_plan,
                },
                action_append_params.ActionAppendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Subscription]._unwrapper,
            ),
            cast_to=cast(Type[Subscription], ResultWrapper[Subscription]),
        )


class AsyncActionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncActionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncActionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncActionsResourceWithStreamingResponse(self)

    async def append(
        self,
        subscription_identifier: str,
        *,
        account_id: str,
        frequency: Literal["weekly", "monthly", "quarterly", "yearly"] | Omit = omit,
        rate_plan: RatePlan | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Subscription:
        """
        Smartly applies the incoming subscription into the lifecycle of the
        subscription.

        Args:
          account_id: Identifier

          subscription_identifier: Subscription identifier tag.

          frequency: How often the subscription is renewed automatically.

          rate_plan: The rate plan applied to the subscription.

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
                "/accounts/{account_id}/subscriptions/{subscription_identifier}/action/append",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            body=await async_maybe_transform(
                {
                    "frequency": frequency,
                    "rate_plan": rate_plan,
                },
                action_append_params.ActionAppendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Subscription]._unwrapper,
            ),
            cast_to=cast(Type[Subscription], ResultWrapper[Subscription]),
        )


class ActionsResourceWithRawResponse:
    def __init__(self, actions: ActionsResource) -> None:
        self._actions = actions

        self.append = to_raw_response_wrapper(
            actions.append,
        )


class AsyncActionsResourceWithRawResponse:
    def __init__(self, actions: AsyncActionsResource) -> None:
        self._actions = actions

        self.append = async_to_raw_response_wrapper(
            actions.append,
        )


class ActionsResourceWithStreamingResponse:
    def __init__(self, actions: ActionsResource) -> None:
        self._actions = actions

        self.append = to_streamed_response_wrapper(
            actions.append,
        )


class AsyncActionsResourceWithStreamingResponse:
    def __init__(self, actions: AsyncActionsResource) -> None:
        self._actions = actions

        self.append = async_to_streamed_response_wrapper(
            actions.append,
        )
