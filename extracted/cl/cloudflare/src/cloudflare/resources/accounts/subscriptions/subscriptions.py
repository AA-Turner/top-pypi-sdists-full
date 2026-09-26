# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Type, cast
from typing_extensions import Literal

import httpx

from .bulk import (
    BulkResource,
    AsyncBulkResource,
    BulkResourceWithRawResponse,
    AsyncBulkResourceWithRawResponse,
    BulkResourceWithStreamingResponse,
    AsyncBulkResourceWithStreamingResponse,
)
from .actions import (
    ActionsResource,
    AsyncActionsResource,
    ActionsResourceWithRawResponse,
    AsyncActionsResourceWithRawResponse,
    ActionsResourceWithStreamingResponse,
    AsyncActionsResourceWithStreamingResponse,
)
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
from ....pagination import SyncSinglePage, AsyncSinglePage
from .cancel_reason import (
    CancelReasonResource,
    AsyncCancelReasonResource,
    CancelReasonResourceWithRawResponse,
    AsyncCancelReasonResourceWithRawResponse,
    CancelReasonResourceWithStreamingResponse,
    AsyncCancelReasonResourceWithStreamingResponse,
)
from ...._base_client import AsyncPaginator, make_request_options
from ....types.accounts import (
    subscription_create_params,
    subscription_update_params,
    subscription_cancel_downgrade_params,
)
from ....types.shared.subscription import Subscription
from ....types.shared_params.rate_plan import RatePlan
from ....types.accounts.subscription_delete_response import SubscriptionDeleteResponse
from ....types.accounts.subscription_cancel_downgrade_response import SubscriptionCancelDowngradeResponse

__all__ = ["SubscriptionsResource", "AsyncSubscriptionsResource"]


class SubscriptionsResource(SyncAPIResource):
    @cached_property
    def cancel_reason(self) -> CancelReasonResource:
        return CancelReasonResource(self._client)

    @cached_property
    def actions(self) -> ActionsResource:
        return ActionsResource(self._client)

    @cached_property
    def bulk(self) -> BulkResource:
        return BulkResource(self._client)

    @cached_property
    def with_raw_response(self) -> SubscriptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return SubscriptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SubscriptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return SubscriptionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str | Omit = omit,
        zone_id: str | Omit = omit,
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
        Creates an account or zone subscription.

        Args:
          account_id: The Account ID to use for this endpoint. Mutually exclusive with the Zone ID.

          zone_id: The Zone ID to use for this endpoint. Mutually exclusive with the Account ID.

          frequency: How often the subscription is renewed automatically.

          rate_plan: The rate plan applied to the subscription.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if account_id and zone_id:
            raise ValueError("You cannot provide both account_id and zone_id")

        if account_id:
            account_or_zone = "accounts"
            account_or_zone_id = account_id
        else:
            if not zone_id:
                raise ValueError("You must provide either account_id or zone_id")

            account_or_zone = "zones"
            account_or_zone_id = zone_id
        return self._post(
            path_template(
                "/{account_or_zone}/{account_or_zone_id}/subscriptions",
                account_or_zone=account_or_zone,
                account_or_zone_id=account_or_zone_id,
            ),
            body=maybe_transform(
                {
                    "frequency": frequency,
                    "rate_plan": rate_plan,
                },
                subscription_create_params.SubscriptionCreateParams,
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

    def update(
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
        Updates an account subscription.

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
        return self._put(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            body=maybe_transform(
                {
                    "frequency": frequency,
                    "rate_plan": rate_plan,
                },
                subscription_update_params.SubscriptionUpdateParams,
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

    def delete(
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
    ) -> SubscriptionDeleteResponse:
        """
        Deletes an account's subscription.

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
        return self._delete(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SubscriptionDeleteResponse]._unwrapper,
            ),
            cast_to=cast(Type[SubscriptionDeleteResponse], ResultWrapper[SubscriptionDeleteResponse]),
        )

    def cancel_downgrade(
        self,
        *,
        account_id: str,
        subscription_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionCancelDowngradeResponse:
        """
        Cancels pending delayed downgrades for the specified subscriptions.

        Args:
          account_id: Identifier

          subscription_ids: List of subscription identifiers to cancel downgrades for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return cast(
            SubscriptionCancelDowngradeResponse,
            self._post(
                path_template("/accounts/{account_id}/subscriptions/cancel-downgrade", account_id=account_id),
                body=maybe_transform(
                    {"subscription_ids": subscription_ids},
                    subscription_cancel_downgrade_params.SubscriptionCancelDowngradeParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[SubscriptionCancelDowngradeResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[SubscriptionCancelDowngradeResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def get(
        self,
        *,
        account_id: str | Omit = omit,
        zone_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncSinglePage[Subscription]:
        """
        Lists all of an account or zone's subscriptions.

        Args:
          account_id: The Account ID to use for this endpoint. Mutually exclusive with the Zone ID.

          zone_id: The Zone ID to use for this endpoint. Mutually exclusive with the Account ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if account_id and zone_id:
            raise ValueError("You cannot provide both account_id and zone_id")

        if account_id:
            account_or_zone = "accounts"
            account_or_zone_id = account_id
        else:
            if not zone_id:
                raise ValueError("You must provide either account_id or zone_id")

            account_or_zone = "zones"
            account_or_zone_id = zone_id
        return self._get_api_list(
            path_template(
                "/{account_or_zone}/{account_or_zone_id}/subscriptions",
                account_or_zone=account_or_zone,
                account_or_zone_id=account_or_zone_id,
            ),
            page=SyncSinglePage[Subscription],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=Subscription,
        )

    def get_by_identifier(
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
    ) -> Subscription:
        """
        Gets an account subscription by identifier.

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
                "/accounts/{account_id}/subscriptions/{subscription_identifier}",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
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


class AsyncSubscriptionsResource(AsyncAPIResource):
    @cached_property
    def cancel_reason(self) -> AsyncCancelReasonResource:
        return AsyncCancelReasonResource(self._client)

    @cached_property
    def actions(self) -> AsyncActionsResource:
        return AsyncActionsResource(self._client)

    @cached_property
    def bulk(self) -> AsyncBulkResource:
        return AsyncBulkResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSubscriptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSubscriptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSubscriptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncSubscriptionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str | Omit = omit,
        zone_id: str | Omit = omit,
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
        Creates an account or zone subscription.

        Args:
          account_id: The Account ID to use for this endpoint. Mutually exclusive with the Zone ID.

          zone_id: The Zone ID to use for this endpoint. Mutually exclusive with the Account ID.

          frequency: How often the subscription is renewed automatically.

          rate_plan: The rate plan applied to the subscription.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if account_id and zone_id:
            raise ValueError("You cannot provide both account_id and zone_id")

        if account_id:
            account_or_zone = "accounts"
            account_or_zone_id = account_id
        else:
            if not zone_id:
                raise ValueError("You must provide either account_id or zone_id")

            account_or_zone = "zones"
            account_or_zone_id = zone_id
        return await self._post(
            path_template(
                "/{account_or_zone}/{account_or_zone_id}/subscriptions",
                account_or_zone=account_or_zone,
                account_or_zone_id=account_or_zone_id,
            ),
            body=await async_maybe_transform(
                {
                    "frequency": frequency,
                    "rate_plan": rate_plan,
                },
                subscription_create_params.SubscriptionCreateParams,
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

    async def update(
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
        Updates an account subscription.

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
        return await self._put(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            body=await async_maybe_transform(
                {
                    "frequency": frequency,
                    "rate_plan": rate_plan,
                },
                subscription_update_params.SubscriptionUpdateParams,
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

    async def delete(
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
    ) -> SubscriptionDeleteResponse:
        """
        Deletes an account's subscription.

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
        return await self._delete(
            path_template(
                "/accounts/{account_id}/subscriptions/{subscription_identifier}",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SubscriptionDeleteResponse]._unwrapper,
            ),
            cast_to=cast(Type[SubscriptionDeleteResponse], ResultWrapper[SubscriptionDeleteResponse]),
        )

    async def cancel_downgrade(
        self,
        *,
        account_id: str,
        subscription_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionCancelDowngradeResponse:
        """
        Cancels pending delayed downgrades for the specified subscriptions.

        Args:
          account_id: Identifier

          subscription_ids: List of subscription identifiers to cancel downgrades for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return cast(
            SubscriptionCancelDowngradeResponse,
            await self._post(
                path_template("/accounts/{account_id}/subscriptions/cancel-downgrade", account_id=account_id),
                body=await async_maybe_transform(
                    {"subscription_ids": subscription_ids},
                    subscription_cancel_downgrade_params.SubscriptionCancelDowngradeParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[SubscriptionCancelDowngradeResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[SubscriptionCancelDowngradeResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def get(
        self,
        *,
        account_id: str | Omit = omit,
        zone_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Subscription, AsyncSinglePage[Subscription]]:
        """
        Lists all of an account or zone's subscriptions.

        Args:
          account_id: The Account ID to use for this endpoint. Mutually exclusive with the Zone ID.

          zone_id: The Zone ID to use for this endpoint. Mutually exclusive with the Account ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if account_id and zone_id:
            raise ValueError("You cannot provide both account_id and zone_id")

        if account_id:
            account_or_zone = "accounts"
            account_or_zone_id = account_id
        else:
            if not zone_id:
                raise ValueError("You must provide either account_id or zone_id")

            account_or_zone = "zones"
            account_or_zone_id = zone_id
        return self._get_api_list(
            path_template(
                "/{account_or_zone}/{account_or_zone_id}/subscriptions",
                account_or_zone=account_or_zone,
                account_or_zone_id=account_or_zone_id,
            ),
            page=AsyncSinglePage[Subscription],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=Subscription,
        )

    async def get_by_identifier(
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
    ) -> Subscription:
        """
        Gets an account subscription by identifier.

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
                "/accounts/{account_id}/subscriptions/{subscription_identifier}",
                account_id=account_id,
                subscription_identifier=subscription_identifier,
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


class SubscriptionsResourceWithRawResponse:
    def __init__(self, subscriptions: SubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = to_raw_response_wrapper(
            subscriptions.create,
        )
        self.update = to_raw_response_wrapper(
            subscriptions.update,
        )
        self.delete = to_raw_response_wrapper(
            subscriptions.delete,
        )
        self.cancel_downgrade = to_raw_response_wrapper(
            subscriptions.cancel_downgrade,
        )
        self.get = to_raw_response_wrapper(
            subscriptions.get,
        )
        self.get_by_identifier = to_raw_response_wrapper(
            subscriptions.get_by_identifier,
        )

    @cached_property
    def cancel_reason(self) -> CancelReasonResourceWithRawResponse:
        return CancelReasonResourceWithRawResponse(self._subscriptions.cancel_reason)

    @cached_property
    def actions(self) -> ActionsResourceWithRawResponse:
        return ActionsResourceWithRawResponse(self._subscriptions.actions)

    @cached_property
    def bulk(self) -> BulkResourceWithRawResponse:
        return BulkResourceWithRawResponse(self._subscriptions.bulk)


class AsyncSubscriptionsResourceWithRawResponse:
    def __init__(self, subscriptions: AsyncSubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = async_to_raw_response_wrapper(
            subscriptions.create,
        )
        self.update = async_to_raw_response_wrapper(
            subscriptions.update,
        )
        self.delete = async_to_raw_response_wrapper(
            subscriptions.delete,
        )
        self.cancel_downgrade = async_to_raw_response_wrapper(
            subscriptions.cancel_downgrade,
        )
        self.get = async_to_raw_response_wrapper(
            subscriptions.get,
        )
        self.get_by_identifier = async_to_raw_response_wrapper(
            subscriptions.get_by_identifier,
        )

    @cached_property
    def cancel_reason(self) -> AsyncCancelReasonResourceWithRawResponse:
        return AsyncCancelReasonResourceWithRawResponse(self._subscriptions.cancel_reason)

    @cached_property
    def actions(self) -> AsyncActionsResourceWithRawResponse:
        return AsyncActionsResourceWithRawResponse(self._subscriptions.actions)

    @cached_property
    def bulk(self) -> AsyncBulkResourceWithRawResponse:
        return AsyncBulkResourceWithRawResponse(self._subscriptions.bulk)


class SubscriptionsResourceWithStreamingResponse:
    def __init__(self, subscriptions: SubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = to_streamed_response_wrapper(
            subscriptions.create,
        )
        self.update = to_streamed_response_wrapper(
            subscriptions.update,
        )
        self.delete = to_streamed_response_wrapper(
            subscriptions.delete,
        )
        self.cancel_downgrade = to_streamed_response_wrapper(
            subscriptions.cancel_downgrade,
        )
        self.get = to_streamed_response_wrapper(
            subscriptions.get,
        )
        self.get_by_identifier = to_streamed_response_wrapper(
            subscriptions.get_by_identifier,
        )

    @cached_property
    def cancel_reason(self) -> CancelReasonResourceWithStreamingResponse:
        return CancelReasonResourceWithStreamingResponse(self._subscriptions.cancel_reason)

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._subscriptions.actions)

    @cached_property
    def bulk(self) -> BulkResourceWithStreamingResponse:
        return BulkResourceWithStreamingResponse(self._subscriptions.bulk)


class AsyncSubscriptionsResourceWithStreamingResponse:
    def __init__(self, subscriptions: AsyncSubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = async_to_streamed_response_wrapper(
            subscriptions.create,
        )
        self.update = async_to_streamed_response_wrapper(
            subscriptions.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            subscriptions.delete,
        )
        self.cancel_downgrade = async_to_streamed_response_wrapper(
            subscriptions.cancel_downgrade,
        )
        self.get = async_to_streamed_response_wrapper(
            subscriptions.get,
        )
        self.get_by_identifier = async_to_streamed_response_wrapper(
            subscriptions.get_by_identifier,
        )

    @cached_property
    def cancel_reason(self) -> AsyncCancelReasonResourceWithStreamingResponse:
        return AsyncCancelReasonResourceWithStreamingResponse(self._subscriptions.cancel_reason)

    @cached_property
    def actions(self) -> AsyncActionsResourceWithStreamingResponse:
        return AsyncActionsResourceWithStreamingResponse(self._subscriptions.actions)

    @cached_property
    def bulk(self) -> AsyncBulkResourceWithStreamingResponse:
        return AsyncBulkResourceWithStreamingResponse(self._subscriptions.bulk)
