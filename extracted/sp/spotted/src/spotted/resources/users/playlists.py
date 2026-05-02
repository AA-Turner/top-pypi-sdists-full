# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

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
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ...types.users import playlist_list_params, playlist_create_params
from ..._base_client import AsyncPaginator, make_request_options
from ...types.users.playlist_create_response import PlaylistCreateResponse
from ...types.shared.simplified_playlist_object import SimplifiedPlaylistObject

__all__ = ["PlaylistsResource", "AsyncPlaylistsResource"]


class PlaylistsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PlaylistsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return PlaylistsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PlaylistsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return PlaylistsResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def create(
        self,
        user_id: str,
        *,
        name: str,
        collaborative: bool | Omit = omit,
        description: str | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlaylistCreateResponse:
        """
        **Deprecated**: Use
        [Create Playlist](/documentation/web-api/reference/create-playlist) instead.

        Create a playlist for a Spotify user. (The playlist will be empty until you
        [add tracks](/documentation/web-api/reference/add-tracks-to-playlist).) Each
        user is generally limited to a maximum of 11000 playlists.

        Args:
          user_id: The user's [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids).

          name: The name for the new playlist, for example `"Your Coolest Playlist"`. This name
              does not need to be unique; a user may have several playlists with the same
              name.

          collaborative: Defaults to `false`. If `true` the playlist will be collaborative. _**Note**: to
              create a collaborative playlist you must also set `public` to `false`. To create
              collaborative playlists you must have granted `playlist-modify-private` and
              `playlist-modify-public`
              [scopes](/documentation/web-api/concepts/scopes/#list-of-scopes)._

          description: value for playlist description as displayed in Spotify Clients and in the Web
              API.

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
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._post(
            path_template("/users/{user_id}/playlists", user_id=user_id),
            body=maybe_transform(
                {
                    "name": name,
                    "collaborative": collaborative,
                    "description": description,
                    "published": published,
                },
                playlist_create_params.PlaylistCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PlaylistCreateResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list(
        self,
        user_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[SimplifiedPlaylistObject]:
        """
        Get a list of the playlists owned or followed by a Spotify user.

        Args:
          user_id: The user's [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids).

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first playlist to return. Default: 0 (the first object).
              Maximum offset: 100.000\\.. Use with `limit` to get the next set of playlists.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get_api_list(
            path_template("/users/{user_id}/playlists", user_id=user_id),
            page=SyncCursorURLPage[SimplifiedPlaylistObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    playlist_list_params.PlaylistListParams,
                ),
            ),
            model=SimplifiedPlaylistObject,
        )


class AsyncPlaylistsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPlaylistsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncPlaylistsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPlaylistsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncPlaylistsResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def create(
        self,
        user_id: str,
        *,
        name: str,
        collaborative: bool | Omit = omit,
        description: str | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlaylistCreateResponse:
        """
        **Deprecated**: Use
        [Create Playlist](/documentation/web-api/reference/create-playlist) instead.

        Create a playlist for a Spotify user. (The playlist will be empty until you
        [add tracks](/documentation/web-api/reference/add-tracks-to-playlist).) Each
        user is generally limited to a maximum of 11000 playlists.

        Args:
          user_id: The user's [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids).

          name: The name for the new playlist, for example `"Your Coolest Playlist"`. This name
              does not need to be unique; a user may have several playlists with the same
              name.

          collaborative: Defaults to `false`. If `true` the playlist will be collaborative. _**Note**: to
              create a collaborative playlist you must also set `public` to `false`. To create
              collaborative playlists you must have granted `playlist-modify-private` and
              `playlist-modify-public`
              [scopes](/documentation/web-api/concepts/scopes/#list-of-scopes)._

          description: value for playlist description as displayed in Spotify Clients and in the Web
              API.

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
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._post(
            path_template("/users/{user_id}/playlists", user_id=user_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "collaborative": collaborative,
                    "description": description,
                    "published": published,
                },
                playlist_create_params.PlaylistCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PlaylistCreateResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list(
        self,
        user_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SimplifiedPlaylistObject, AsyncCursorURLPage[SimplifiedPlaylistObject]]:
        """
        Get a list of the playlists owned or followed by a Spotify user.

        Args:
          user_id: The user's [Spotify user ID](/documentation/web-api/concepts/spotify-uris-ids).

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first playlist to return. Default: 0 (the first object).
              Maximum offset: 100.000\\.. Use with `limit` to get the next set of playlists.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get_api_list(
            path_template("/users/{user_id}/playlists", user_id=user_id),
            page=AsyncCursorURLPage[SimplifiedPlaylistObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    playlist_list_params.PlaylistListParams,
                ),
            ),
            model=SimplifiedPlaylistObject,
        )


class PlaylistsResourceWithRawResponse:
    def __init__(self, playlists: PlaylistsResource) -> None:
        self._playlists = playlists

        self.create = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                playlists.create,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                playlists.list,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncPlaylistsResourceWithRawResponse:
    def __init__(self, playlists: AsyncPlaylistsResource) -> None:
        self._playlists = playlists

        self.create = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                playlists.create,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                playlists.list,  # pyright: ignore[reportDeprecated],
            )
        )


class PlaylistsResourceWithStreamingResponse:
    def __init__(self, playlists: PlaylistsResource) -> None:
        self._playlists = playlists

        self.create = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                playlists.create,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                playlists.list,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncPlaylistsResourceWithStreamingResponse:
    def __init__(self, playlists: AsyncPlaylistsResource) -> None:
        self._playlists = playlists

        self.create = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                playlists.create,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                playlists.list,  # pyright: ignore[reportDeprecated],
            )
        )
