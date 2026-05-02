# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template
from ..._compat import cached_property
from .playlists import (
    PlaylistsResource,
    AsyncPlaylistsResource,
    PlaylistsResourceWithRawResponse,
    AsyncPlaylistsResourceWithRawResponse,
    PlaylistsResourceWithStreamingResponse,
    AsyncPlaylistsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.user_retrieve_profile_response import UserRetrieveProfileResponse

__all__ = ["UsersResource", "AsyncUsersResource"]


class UsersResource(SyncAPIResource):
    @cached_property
    def playlists(self) -> PlaylistsResource:
        return PlaylistsResource(self._client)

    @cached_property
    def with_raw_response(self) -> UsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return UsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return UsersResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def retrieve_profile(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UserRetrieveProfileResponse:
        """
        Get public profile information about a Spotify user.

        Args:
          user_id: The user's [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get(
            path_template("/users/{user_id}", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserRetrieveProfileResponse,
        )


class AsyncUsersResource(AsyncAPIResource):
    @cached_property
    def playlists(self) -> AsyncPlaylistsResource:
        return AsyncPlaylistsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncUsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncUsersResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def retrieve_profile(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UserRetrieveProfileResponse:
        """
        Get public profile information about a Spotify user.

        Args:
          user_id: The user's [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._get(
            path_template("/users/{user_id}", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserRetrieveProfileResponse,
        )


class UsersResourceWithRawResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.retrieve_profile = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                users.retrieve_profile,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def playlists(self) -> PlaylistsResourceWithRawResponse:
        return PlaylistsResourceWithRawResponse(self._users.playlists)


class AsyncUsersResourceWithRawResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.retrieve_profile = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                users.retrieve_profile,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def playlists(self) -> AsyncPlaylistsResourceWithRawResponse:
        return AsyncPlaylistsResourceWithRawResponse(self._users.playlists)


class UsersResourceWithStreamingResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.retrieve_profile = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                users.retrieve_profile,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def playlists(self) -> PlaylistsResourceWithStreamingResponse:
        return PlaylistsResourceWithStreamingResponse(self._users.playlists)


class AsyncUsersResourceWithStreamingResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.retrieve_profile = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                users.retrieve_profile,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def playlists(self) -> AsyncPlaylistsResourceWithStreamingResponse:
        return AsyncPlaylistsResourceWithStreamingResponse(self._users.playlists)
