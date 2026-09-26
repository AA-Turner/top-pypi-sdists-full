# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
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
from ...pagination import SyncSinglePage, AsyncSinglePage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.magic_transit import bgp_filter_profile_create_params, bgp_filter_profile_update_params
from ...types.magic_transit.bgp_filter_profile_get_response import BGPFilterProfileGetResponse
from ...types.magic_transit.bgp_filter_profile_list_response import BGPFilterProfileListResponse
from ...types.magic_transit.bgp_filter_profile_create_response import BGPFilterProfileCreateResponse
from ...types.magic_transit.bgp_filter_profile_delete_response import BGPFilterProfileDeleteResponse
from ...types.magic_transit.bgp_filter_profile_update_response import BGPFilterProfileUpdateResponse

__all__ = ["BGPFilterProfilesResource", "AsyncBGPFilterProfilesResource"]


class BGPFilterProfilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BGPFilterProfilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return BGPFilterProfilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BGPFilterProfilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return BGPFilterProfilesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        match_action: Literal["allow", "deny"],
        name: str,
        targets: SequenceNotStr[str],
        description: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileCreateResponse:
        """
        Creates a new BGP filter profile for an account.

        Args:
          account_id: Identifier

          match_action: Action to take when a route matches one of the targets in this profile

          name: Friendly name for the filter profile

          targets: List of CIDR prefixes. Each entry may carry an optional suffix that specifies
              which prefix lengths to match relative to the prefix length N: '{X,Y}' matches
              prefix lengths in the inclusive range [X, Y] where N <= X <= Y <= max (max is 32
              for IPv4, 128 for IPv6), '{X}' matches exactly length X (equivalent to {X,X}),
              '+' is shorthand for {N, max} (the prefix and all more-specific subnets,
              including at length N itself; valid even when N is the maximum length). Omit the
              suffix to match the prefix exactly at length N.

          description: Description of the filter profile

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/magic/bgp/filter_profiles", account_id=account_id),
            body=maybe_transform(
                {
                    "match_action": match_action,
                    "name": name,
                    "targets": targets,
                    "description": description,
                },
                bgp_filter_profile_create_params.BGPFilterProfileCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileCreateResponse], ResultWrapper[BGPFilterProfileCreateResponse]),
        )

    def update(
        self,
        profile_id: str,
        *,
        account_id: str,
        description: str | Omit = omit,
        match_action: Literal["allow", "deny"] | Omit = omit,
        name: str | Omit = omit,
        targets: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileUpdateResponse:
        """Updates a BGP filter profile.

        Omitted properties are left unchanged. To clear an
        existing description send `description: ""`.

        Args:
          account_id: Identifier

          profile_id: Identifier

          description: Description of the filter profile

          match_action: Action to take when a route matches one of the targets in this profile

          name: Friendly name for the filter profile

          targets: List of CIDR prefixes. Each entry may carry an optional suffix that specifies
              which prefix lengths to match relative to the prefix length N: '{X,Y}' matches
              prefix lengths in the inclusive range [X, Y] where N <= X <= Y <= max (max is 32
              for IPv4, 128 for IPv6), '{X}' matches exactly length X (equivalent to {X,X}),
              '+' is shorthand for {N, max} (the prefix and all more-specific subnets,
              including at length N itself; valid even when N is the maximum length). Omit the
              suffix to match the prefix exactly at length N.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not profile_id:
            raise ValueError(f"Expected a non-empty value for `profile_id` but received {profile_id!r}")
        return self._put(
            path_template(
                "/accounts/{account_id}/magic/bgp/filter_profiles/{profile_id}",
                account_id=account_id,
                profile_id=profile_id,
            ),
            body=maybe_transform(
                {
                    "description": description,
                    "match_action": match_action,
                    "name": name,
                    "targets": targets,
                },
                bgp_filter_profile_update_params.BGPFilterProfileUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileUpdateResponse], ResultWrapper[BGPFilterProfileUpdateResponse]),
        )

    def list(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncSinglePage[BGPFilterProfileListResponse]:
        """
        Lists all BGP filter profiles for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/magic/bgp/filter_profiles", account_id=account_id),
            page=SyncSinglePage[BGPFilterProfileListResponse],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=BGPFilterProfileListResponse,
        )

    def delete(
        self,
        profile_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileDeleteResponse:
        """
        Deletes a BGP filter profile.

        Args:
          account_id: Identifier

          profile_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not profile_id:
            raise ValueError(f"Expected a non-empty value for `profile_id` but received {profile_id!r}")
        return self._delete(
            path_template(
                "/accounts/{account_id}/magic/bgp/filter_profiles/{profile_id}",
                account_id=account_id,
                profile_id=profile_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileDeleteResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileDeleteResponse], ResultWrapper[BGPFilterProfileDeleteResponse]),
        )

    def get(
        self,
        profile_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileGetResponse:
        """
        Gets a specific BGP filter profile for an account.

        Args:
          account_id: Identifier

          profile_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not profile_id:
            raise ValueError(f"Expected a non-empty value for `profile_id` but received {profile_id!r}")
        return self._get(
            path_template(
                "/accounts/{account_id}/magic/bgp/filter_profiles/{profile_id}",
                account_id=account_id,
                profile_id=profile_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileGetResponse], ResultWrapper[BGPFilterProfileGetResponse]),
        )


class AsyncBGPFilterProfilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBGPFilterProfilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBGPFilterProfilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBGPFilterProfilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncBGPFilterProfilesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        match_action: Literal["allow", "deny"],
        name: str,
        targets: SequenceNotStr[str],
        description: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileCreateResponse:
        """
        Creates a new BGP filter profile for an account.

        Args:
          account_id: Identifier

          match_action: Action to take when a route matches one of the targets in this profile

          name: Friendly name for the filter profile

          targets: List of CIDR prefixes. Each entry may carry an optional suffix that specifies
              which prefix lengths to match relative to the prefix length N: '{X,Y}' matches
              prefix lengths in the inclusive range [X, Y] where N <= X <= Y <= max (max is 32
              for IPv4, 128 for IPv6), '{X}' matches exactly length X (equivalent to {X,X}),
              '+' is shorthand for {N, max} (the prefix and all more-specific subnets,
              including at length N itself; valid even when N is the maximum length). Omit the
              suffix to match the prefix exactly at length N.

          description: Description of the filter profile

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/magic/bgp/filter_profiles", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "match_action": match_action,
                    "name": name,
                    "targets": targets,
                    "description": description,
                },
                bgp_filter_profile_create_params.BGPFilterProfileCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileCreateResponse], ResultWrapper[BGPFilterProfileCreateResponse]),
        )

    async def update(
        self,
        profile_id: str,
        *,
        account_id: str,
        description: str | Omit = omit,
        match_action: Literal["allow", "deny"] | Omit = omit,
        name: str | Omit = omit,
        targets: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileUpdateResponse:
        """Updates a BGP filter profile.

        Omitted properties are left unchanged. To clear an
        existing description send `description: ""`.

        Args:
          account_id: Identifier

          profile_id: Identifier

          description: Description of the filter profile

          match_action: Action to take when a route matches one of the targets in this profile

          name: Friendly name for the filter profile

          targets: List of CIDR prefixes. Each entry may carry an optional suffix that specifies
              which prefix lengths to match relative to the prefix length N: '{X,Y}' matches
              prefix lengths in the inclusive range [X, Y] where N <= X <= Y <= max (max is 32
              for IPv4, 128 for IPv6), '{X}' matches exactly length X (equivalent to {X,X}),
              '+' is shorthand for {N, max} (the prefix and all more-specific subnets,
              including at length N itself; valid even when N is the maximum length). Omit the
              suffix to match the prefix exactly at length N.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not profile_id:
            raise ValueError(f"Expected a non-empty value for `profile_id` but received {profile_id!r}")
        return await self._put(
            path_template(
                "/accounts/{account_id}/magic/bgp/filter_profiles/{profile_id}",
                account_id=account_id,
                profile_id=profile_id,
            ),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "match_action": match_action,
                    "name": name,
                    "targets": targets,
                },
                bgp_filter_profile_update_params.BGPFilterProfileUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileUpdateResponse], ResultWrapper[BGPFilterProfileUpdateResponse]),
        )

    def list(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BGPFilterProfileListResponse, AsyncSinglePage[BGPFilterProfileListResponse]]:
        """
        Lists all BGP filter profiles for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/magic/bgp/filter_profiles", account_id=account_id),
            page=AsyncSinglePage[BGPFilterProfileListResponse],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=BGPFilterProfileListResponse,
        )

    async def delete(
        self,
        profile_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileDeleteResponse:
        """
        Deletes a BGP filter profile.

        Args:
          account_id: Identifier

          profile_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not profile_id:
            raise ValueError(f"Expected a non-empty value for `profile_id` but received {profile_id!r}")
        return await self._delete(
            path_template(
                "/accounts/{account_id}/magic/bgp/filter_profiles/{profile_id}",
                account_id=account_id,
                profile_id=profile_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileDeleteResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileDeleteResponse], ResultWrapper[BGPFilterProfileDeleteResponse]),
        )

    async def get(
        self,
        profile_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BGPFilterProfileGetResponse:
        """
        Gets a specific BGP filter profile for an account.

        Args:
          account_id: Identifier

          profile_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not profile_id:
            raise ValueError(f"Expected a non-empty value for `profile_id` but received {profile_id!r}")
        return await self._get(
            path_template(
                "/accounts/{account_id}/magic/bgp/filter_profiles/{profile_id}",
                account_id=account_id,
                profile_id=profile_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[BGPFilterProfileGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[BGPFilterProfileGetResponse], ResultWrapper[BGPFilterProfileGetResponse]),
        )


class BGPFilterProfilesResourceWithRawResponse:
    def __init__(self, bgp_filter_profiles: BGPFilterProfilesResource) -> None:
        self._bgp_filter_profiles = bgp_filter_profiles

        self.create = to_raw_response_wrapper(
            bgp_filter_profiles.create,
        )
        self.update = to_raw_response_wrapper(
            bgp_filter_profiles.update,
        )
        self.list = to_raw_response_wrapper(
            bgp_filter_profiles.list,
        )
        self.delete = to_raw_response_wrapper(
            bgp_filter_profiles.delete,
        )
        self.get = to_raw_response_wrapper(
            bgp_filter_profiles.get,
        )


class AsyncBGPFilterProfilesResourceWithRawResponse:
    def __init__(self, bgp_filter_profiles: AsyncBGPFilterProfilesResource) -> None:
        self._bgp_filter_profiles = bgp_filter_profiles

        self.create = async_to_raw_response_wrapper(
            bgp_filter_profiles.create,
        )
        self.update = async_to_raw_response_wrapper(
            bgp_filter_profiles.update,
        )
        self.list = async_to_raw_response_wrapper(
            bgp_filter_profiles.list,
        )
        self.delete = async_to_raw_response_wrapper(
            bgp_filter_profiles.delete,
        )
        self.get = async_to_raw_response_wrapper(
            bgp_filter_profiles.get,
        )


class BGPFilterProfilesResourceWithStreamingResponse:
    def __init__(self, bgp_filter_profiles: BGPFilterProfilesResource) -> None:
        self._bgp_filter_profiles = bgp_filter_profiles

        self.create = to_streamed_response_wrapper(
            bgp_filter_profiles.create,
        )
        self.update = to_streamed_response_wrapper(
            bgp_filter_profiles.update,
        )
        self.list = to_streamed_response_wrapper(
            bgp_filter_profiles.list,
        )
        self.delete = to_streamed_response_wrapper(
            bgp_filter_profiles.delete,
        )
        self.get = to_streamed_response_wrapper(
            bgp_filter_profiles.get,
        )


class AsyncBGPFilterProfilesResourceWithStreamingResponse:
    def __init__(self, bgp_filter_profiles: AsyncBGPFilterProfilesResource) -> None:
        self._bgp_filter_profiles = bgp_filter_profiles

        self.create = async_to_streamed_response_wrapper(
            bgp_filter_profiles.create,
        )
        self.update = async_to_streamed_response_wrapper(
            bgp_filter_profiles.update,
        )
        self.list = async_to_streamed_response_wrapper(
            bgp_filter_profiles.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            bgp_filter_profiles.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            bgp_filter_profiles.get,
        )
