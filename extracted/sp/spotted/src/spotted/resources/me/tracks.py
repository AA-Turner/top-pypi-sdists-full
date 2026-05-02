# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Iterable

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ...types.me import track_list_params, track_save_params, track_check_params, track_remove_params
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.me.track_list_response import TrackListResponse
from ...types.me.track_check_response import TrackCheckResponse

__all__ = ["TracksResource", "AsyncTracksResource"]


class TracksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TracksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return TracksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TracksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return TracksResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[TrackListResponse]:
        """
        Get a list of the songs saved in the current Spotify user's 'Your Music'
        library.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/tracks",
            page=SyncCursorURLPage[TrackListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    track_list_params.TrackListParams,
                ),
            ),
            model=TrackListResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def check(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackCheckResponse:
        """
        Check if one or more tracks is already saved in the current Spotify user's 'Your
        Music' library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=4iV5W9uYEdYUVa79Axb7Rh,1301WleyT98MSxVHPZCA6M`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/me/tracks/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, track_check_params.TrackCheckParams),
            ),
            cast_to=TrackCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def remove(
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
        Remove one or more tracks from the current user's 'Your Music' library.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]`<br/>A maximum of 50 items
              can be specified in one request. _**Note**: if the `ids` parameter is present in
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
            "/me/tracks",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                track_remove_params.TrackRemoveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    def save(
        self,
        *,
        ids: SequenceNotStr[str],
        published: bool | Omit = omit,
        timestamped_ids: Iterable[track_save_params.TimestampedID] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Save one or more tracks to the current user's 'Your Music' library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]`<br/>A maximum of 50 items
              can be specified in one request. _**Note**: if the `timestamped_ids` is present
              in the body, any IDs listed in the query parameters (deprecated) or the `ids`
              field in the body will be ignored._

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          timestamped_ids: A JSON array of objects containing track IDs with their corresponding
              timestamps. Each object must include a track ID and an `added_at` timestamp.
              This allows you to specify when tracks were added to maintain a specific
              chronological order in the user's library.<br/>A maximum of 50 items can be
              specified in one request. _**Note**: if the `timestamped_ids` is present in the
              body, any IDs listed in the query parameters (deprecated) or the `ids` field in
              the body will be ignored._

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/tracks",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                    "timestamped_ids": timestamped_ids,
                },
                track_save_params.TrackSaveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncTracksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTracksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncTracksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTracksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncTracksResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[TrackListResponse, AsyncCursorURLPage[TrackListResponse]]:
        """
        Get a list of the songs saved in the current Spotify user's 'Your Music'
        library.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/tracks",
            page=AsyncCursorURLPage[TrackListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    track_list_params.TrackListParams,
                ),
            ),
            model=TrackListResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def check(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackCheckResponse:
        """
        Check if one or more tracks is already saved in the current Spotify user's 'Your
        Music' library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=4iV5W9uYEdYUVa79Axb7Rh,1301WleyT98MSxVHPZCA6M`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/me/tracks/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, track_check_params.TrackCheckParams),
            ),
            cast_to=TrackCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def remove(
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
        Remove one or more tracks from the current user's 'Your Music' library.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]`<br/>A maximum of 50 items
              can be specified in one request. _**Note**: if the `ids` parameter is present in
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
            "/me/tracks",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                track_remove_params.TrackRemoveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    async def save(
        self,
        *,
        ids: SequenceNotStr[str],
        published: bool | Omit = omit,
        timestamped_ids: Iterable[track_save_params.TimestampedID] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Save one or more tracks to the current user's 'Your Music' library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]`<br/>A maximum of 50 items
              can be specified in one request. _**Note**: if the `timestamped_ids` is present
              in the body, any IDs listed in the query parameters (deprecated) or the `ids`
              field in the body will be ignored._

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          timestamped_ids: A JSON array of objects containing track IDs with their corresponding
              timestamps. Each object must include a track ID and an `added_at` timestamp.
              This allows you to specify when tracks were added to maintain a specific
              chronological order in the user's library.<br/>A maximum of 50 items can be
              specified in one request. _**Note**: if the `timestamped_ids` is present in the
              body, any IDs listed in the query parameters (deprecated) or the `ids` field in
              the body will be ignored._

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/tracks",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                    "timestamped_ids": timestamped_ids,
                },
                track_save_params.TrackSaveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class TracksResourceWithRawResponse:
    def __init__(self, tracks: TracksResource) -> None:
        self._tracks = tracks

        self.list = to_raw_response_wrapper(
            tracks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncTracksResourceWithRawResponse:
    def __init__(self, tracks: AsyncTracksResource) -> None:
        self._tracks = tracks

        self.list = async_to_raw_response_wrapper(
            tracks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.save,  # pyright: ignore[reportDeprecated],
            )
        )


class TracksResourceWithStreamingResponse:
    def __init__(self, tracks: TracksResource) -> None:
        self._tracks = tracks

        self.list = to_streamed_response_wrapper(
            tracks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncTracksResourceWithStreamingResponse:
    def __init__(self, tracks: AsyncTracksResource) -> None:
        self._tracks = tracks

        self.list = async_to_streamed_response_wrapper(
            tracks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.save,  # pyright: ignore[reportDeprecated],
            )
        )
