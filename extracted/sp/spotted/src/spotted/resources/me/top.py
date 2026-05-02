# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ...types.me import top_list_top_tracks_params, top_list_top_artists_params
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.shared.track_object import TrackObject
from ...types.shared.artist_object import ArtistObject

__all__ = ["TopResource", "AsyncTopResource"]


class TopResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return TopResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return TopResourceWithStreamingResponse(self)

    def list_top_artists(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        time_range: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[ArtistObject]:
        """
        Get the current user's top artists based on calculated affinity.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          time_range: Over what time frame the affinities are computed. Valid values: `long_term`
              (calculated from ~1 year of data and including all new data as it becomes
              available), `medium_term` (approximately last 6 months), `short_term`
              (approximately last 4 weeks). Default: `medium_term`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/top/artists",
            page=SyncCursorURLPage[ArtistObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "time_range": time_range,
                    },
                    top_list_top_artists_params.TopListTopArtistsParams,
                ),
            ),
            model=ArtistObject,
        )

    def list_top_tracks(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        time_range: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[TrackObject]:
        """
        Get the current user's top tracks based on calculated affinity.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          time_range: Over what time frame the affinities are computed. Valid values: `long_term`
              (calculated from ~1 year of data and including all new data as it becomes
              available), `medium_term` (approximately last 6 months), `short_term`
              (approximately last 4 weeks). Default: `medium_term`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/top/tracks",
            page=SyncCursorURLPage[TrackObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "time_range": time_range,
                    },
                    top_list_top_tracks_params.TopListTopTracksParams,
                ),
            ),
            model=TrackObject,
        )


class AsyncTopResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncTopResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncTopResourceWithStreamingResponse(self)

    def list_top_artists(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        time_range: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ArtistObject, AsyncCursorURLPage[ArtistObject]]:
        """
        Get the current user's top artists based on calculated affinity.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          time_range: Over what time frame the affinities are computed. Valid values: `long_term`
              (calculated from ~1 year of data and including all new data as it becomes
              available), `medium_term` (approximately last 6 months), `short_term`
              (approximately last 4 weeks). Default: `medium_term`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/top/artists",
            page=AsyncCursorURLPage[ArtistObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "time_range": time_range,
                    },
                    top_list_top_artists_params.TopListTopArtistsParams,
                ),
            ),
            model=ArtistObject,
        )

    def list_top_tracks(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        time_range: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[TrackObject, AsyncCursorURLPage[TrackObject]]:
        """
        Get the current user's top tracks based on calculated affinity.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          time_range: Over what time frame the affinities are computed. Valid values: `long_term`
              (calculated from ~1 year of data and including all new data as it becomes
              available), `medium_term` (approximately last 6 months), `short_term`
              (approximately last 4 weeks). Default: `medium_term`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/top/tracks",
            page=AsyncCursorURLPage[TrackObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "time_range": time_range,
                    },
                    top_list_top_tracks_params.TopListTopTracksParams,
                ),
            ),
            model=TrackObject,
        )


class TopResourceWithRawResponse:
    def __init__(self, top: TopResource) -> None:
        self._top = top

        self.list_top_artists = to_raw_response_wrapper(
            top.list_top_artists,
        )
        self.list_top_tracks = to_raw_response_wrapper(
            top.list_top_tracks,
        )


class AsyncTopResourceWithRawResponse:
    def __init__(self, top: AsyncTopResource) -> None:
        self._top = top

        self.list_top_artists = async_to_raw_response_wrapper(
            top.list_top_artists,
        )
        self.list_top_tracks = async_to_raw_response_wrapper(
            top.list_top_tracks,
        )


class TopResourceWithStreamingResponse:
    def __init__(self, top: TopResource) -> None:
        self._top = top

        self.list_top_artists = to_streamed_response_wrapper(
            top.list_top_artists,
        )
        self.list_top_tracks = to_streamed_response_wrapper(
            top.list_top_tracks,
        )


class AsyncTopResourceWithStreamingResponse:
    def __init__(self, top: AsyncTopResource) -> None:
        self._top = top

        self.list_top_artists = async_to_streamed_response_wrapper(
            top.list_top_artists,
        )
        self.list_top_tracks = async_to_streamed_response_wrapper(
            top.list_top_tracks,
        )
