# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.playlists import follower_check_params, follower_follow_params
from ...types.playlists.follower_check_response import FollowerCheckResponse

__all__ = ["FollowersResource", "AsyncFollowersResource"]


class FollowersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FollowersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return FollowersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FollowersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return FollowersResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def check(
        self,
        playlist_id: str,
        *,
        ids: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FollowerCheckResponse:
        """
        Check to see if the current user is following a specified playlist.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          ids: **Deprecated** A single item list containing current user's
              [Spotify Username](/documentation/web-api/concepts/spotify-uris-ids). Maximum: 1
              id.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._get(
            path_template("/playlists/{playlist_id}/followers/contains", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, follower_check_params.FollowerCheckParams),
            ),
            cast_to=FollowerCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def follow(
        self,
        playlist_id: str,
        *,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Add the current user as a follower of a playlist.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

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
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            path_template("/playlists/{playlist_id}/followers", playlist_id=playlist_id),
            body=maybe_transform({"published": published}, follower_follow_params.FollowerFollowParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    def unfollow(
        self,
        playlist_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove the current user as a follower of a playlist.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/playlists/{playlist_id}/followers", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncFollowersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFollowersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncFollowersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFollowersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncFollowersResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def check(
        self,
        playlist_id: str,
        *,
        ids: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FollowerCheckResponse:
        """
        Check to see if the current user is following a specified playlist.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          ids: **Deprecated** A single item list containing current user's
              [Spotify Username](/documentation/web-api/concepts/spotify-uris-ids). Maximum: 1
              id.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return await self._get(
            path_template("/playlists/{playlist_id}/followers/contains", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, follower_check_params.FollowerCheckParams),
            ),
            cast_to=FollowerCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def follow(
        self,
        playlist_id: str,
        *,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Add the current user as a follower of a playlist.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

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
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            path_template("/playlists/{playlist_id}/followers", playlist_id=playlist_id),
            body=await async_maybe_transform({"published": published}, follower_follow_params.FollowerFollowParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    async def unfollow(
        self,
        playlist_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove the current user as a follower of a playlist.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/playlists/{playlist_id}/followers", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class FollowersResourceWithRawResponse:
    def __init__(self, followers: FollowersResource) -> None:
        self._followers = followers

        self.check = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                followers.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                followers.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                followers.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncFollowersResourceWithRawResponse:
    def __init__(self, followers: AsyncFollowersResource) -> None:
        self._followers = followers

        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                followers.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                followers.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                followers.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )


class FollowersResourceWithStreamingResponse:
    def __init__(self, followers: FollowersResource) -> None:
        self._followers = followers

        self.check = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                followers.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                followers.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                followers.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncFollowersResourceWithStreamingResponse:
    def __init__(self, followers: AsyncFollowersResource) -> None:
        self._followers = followers

        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                followers.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.follow = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                followers.follow,  # pyright: ignore[reportDeprecated],
            )
        )
        self.unfollow = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                followers.unfollow,  # pyright: ignore[reportDeprecated],
            )
        )
