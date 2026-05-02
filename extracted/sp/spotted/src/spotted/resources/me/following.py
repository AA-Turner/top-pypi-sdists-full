# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ...types.me import (
    following_check_params,
    following_follow_params,
    following_unfollow_params,
    following_bulk_retrieve_params,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.me.following_check_response import FollowingCheckResponse
from ...types.me.following_bulk_retrieve_response import FollowingBulkRetrieveResponse

__all__ = ["FollowingResource", "AsyncFollowingResource"]


class FollowingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FollowingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return FollowingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FollowingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return FollowingResourceWithStreamingResponse(self)

    def bulk_retrieve(
        self,
        *,
        type: Literal["artist"],
        after: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FollowingBulkRetrieveResponse:
        """
        Get the current user's followed artists.

        Args:
          type: The ID type: currently only `artist` is supported.

          after: The last artist ID retrieved from the previous request.

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/me/following",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "type": type,
                        "after": after,
                        "limit": limit,
                    },
                    following_bulk_retrieve_params.FollowingBulkRetrieveParams,
                ),
            ),
            cast_to=FollowingBulkRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def check(
        self,
        *,
        ids: str,
        type: Literal["artist", "user"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FollowingCheckResponse:
        """
        Check to see if the current user is following one or more artists or other
        Spotify users.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the artist or the user
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) to check. For
              example: `ids=74ASZWbe4lXaubB36ztrGX,08td7MxkoHQkXnWAYD8d6Q`. A maximum of 50
              IDs can be sent in one request.

          type: The ID type: either `artist` or `user`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/me/following/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "type": type,
                    },
                    following_check_params.FollowingCheckParams,
                ),
            ),
            cast_to=FollowingCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def follow(
        self,
        *,
        ids: SequenceNotStr[str],
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Add the current user as a follower of one or more artists or other Spotify
        users.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A JSON array of the artist or user
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `{ids:["74ASZWbe4lXaubB36ztrGX", "08td7MxkoHQkXnWAYD8d6Q"]}`. A maximum of 50
              IDs can be sent in one request. _**Note**: if the `ids` parameter is present in
              the query string, any IDs listed here in the body will be ignored._

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/following",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                following_follow_params.FollowingFollowParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    def unfollow(
        self,
        *,
        ids: SequenceNotStr[str] | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove the current user as a follower of one or more artists or other Spotify
        users.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A JSON array of the artist or user
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `{ids:["74ASZWbe4lXaubB36ztrGX", "08td7MxkoHQkXnWAYD8d6Q"]}`. A maximum of 50
              IDs can be sent in one request. _**Note**: if the `ids` parameter is present in
              the query string, any IDs listed here in the body will be ignored._

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/me/following",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                following_unfollow_params.FollowingUnfollowParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncFollowingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFollowingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncFollowingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFollowingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncFollowingResourceWithStreamingResponse(self)

    async def bulk_retrieve(
        self,
        *,
        type: Literal["artist"],
        after: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FollowingBulkRetrieveResponse:
        """
        Get the current user's followed artists.

        Args:
          type: The ID type: currently only `artist` is supported.

          after: The last artist ID retrieved from the previous request.

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/me/following",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "type": type,
                        "after": after,
                        "limit": limit,
                    },
                    following_bulk_retrieve_params.FollowingBulkRetrieveParams,
                ),
            ),
            cast_to=FollowingBulkRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def check(
        self,
        *,
        ids: str,
        type: Literal["artist", "user"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FollowingCheckResponse:
        """
        Check to see if the current user is following one or more artists or other
        Spotify users.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the artist or the user
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) to check. For
              example: `ids=74ASZWbe4lXaubB36ztrGX,08td7MxkoHQkXnWAYD8d6Q`. A maximum of 50
              IDs can be sent in one request.

          type: The ID type: either `artist` or `user`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/me/following/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "type": type,
                    },
                    following_check_params.FollowingCheckParams,
                ),
            ),
            cast_to=FollowingCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def follow(
        self,
        *,
        ids: SequenceNotStr[str],
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Add the current user as a follower of one or more artists or other Spotify
        users.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A JSON array of the artist or user
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `{ids:["74ASZWbe4lXaubB36ztrGX", "08td7MxkoHQkXnWAYD8d6Q"]}`. A maximum of 50
              IDs can be sent in one request. _**Note**: if the `ids` parameter is present in
              the query string, any IDs listed here in the body will be ignored._

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/following",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                following_follow_params.FollowingFollowParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    async def unfollow(
        self,
        *,
        ids: SequenceNotStr[str] | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove the current user as a follower of one or more artists or other Spotify
        users.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A JSON array of the artist or user
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `{ids:["74ASZWbe4lXaubB36ztrGX", "08td7MxkoHQkXnWAYD8d6Q"]}`. A maximum of 50
              IDs can be sent in one request. _**Note**: if the `ids` parameter is present in
              the query string, any IDs listed here in the body will be ignored._

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/me/following",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                following_unfollow_params.FollowingUnfollowParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class FollowingResourceWithRawResponse:
    def __init__(self, following: FollowingResource) -> None:
        self._following = following

        self.bulk_retrieve = to_raw_response_wrapper(
            following.bulk_retrieve,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                following.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                following.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                following.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncFollowingResourceWithRawResponse:
    def __init__(self, following: AsyncFollowingResource) -> None:
        self._following = following

        self.bulk_retrieve = async_to_raw_response_wrapper(
            following.bulk_retrieve,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                following.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                following.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                following.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )


class FollowingResourceWithStreamingResponse:
    def __init__(self, following: FollowingResource) -> None:
        self._following = following

        self.bulk_retrieve = to_streamed_response_wrapper(
            following.bulk_retrieve,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                following.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                following.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                following.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncFollowingResourceWithStreamingResponse:
    def __init__(self, following: AsyncFollowingResource) -> None:
        self._following = following

        self.bulk_retrieve = async_to_streamed_response_wrapper(
            following.bulk_retrieve,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                following.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                following.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                following.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )
