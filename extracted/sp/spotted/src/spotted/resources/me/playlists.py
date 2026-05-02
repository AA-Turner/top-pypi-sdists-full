# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ...types.me import playlist_list_params
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
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

    def list(
        self,
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
        Get a list of the playlists owned or followed by the current Spotify user.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: 'The index of the first playlist to return. Default: 0 (the first object).
              Maximum offset: 100.000\\.. Use with `limit` to get the next set of playlists.'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/playlists",
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

    def list(
        self,
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
        Get a list of the playlists owned or followed by the current Spotify user.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: 'The index of the first playlist to return. Default: 0 (the first object).
              Maximum offset: 100.000\\.. Use with `limit` to get the next set of playlists.'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/playlists",
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

        self.list = to_raw_response_wrapper(
            playlists.list,
        )


class AsyncPlaylistsResourceWithRawResponse:
    def __init__(self, playlists: AsyncPlaylistsResource) -> None:
        self._playlists = playlists

        self.list = async_to_raw_response_wrapper(
            playlists.list,
        )


class PlaylistsResourceWithStreamingResponse:
    def __init__(self, playlists: PlaylistsResource) -> None:
        self._playlists = playlists

        self.list = to_streamed_response_wrapper(
            playlists.list,
        )


class AsyncPlaylistsResourceWithStreamingResponse:
    def __init__(self, playlists: AsyncPlaylistsResource) -> None:
        self._playlists = playlists

        self.list = async_to_streamed_response_wrapper(
            playlists.list,
        )
