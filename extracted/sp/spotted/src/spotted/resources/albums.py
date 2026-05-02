# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import album_retrieve_params, album_list_tracks_params, album_bulk_retrieve_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorURLPage, AsyncCursorURLPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.album_retrieve_response import AlbumRetrieveResponse
from ..types.album_bulk_retrieve_response import AlbumBulkRetrieveResponse
from ..types.shared.simplified_track_object import SimplifiedTrackObject

__all__ = ["AlbumsResource", "AsyncAlbumsResource"]


class AlbumsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AlbumsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AlbumsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AlbumsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AlbumsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AlbumRetrieveResponse:
        """
        Get Spotify catalog information for a single album.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the album.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/albums/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"market": market}, album_retrieve_params.AlbumRetrieveParams),
            ),
            cast_to=AlbumRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def bulk_retrieve(
        self,
        *,
        ids: str,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AlbumBulkRetrieveResponse:
        """
        Get Spotify catalog information for multiple albums identified by their Spotify
        IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the albums.
              Maximum: 20 IDs.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/albums",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "market": market,
                    },
                    album_bulk_retrieve_params.AlbumBulkRetrieveParams,
                ),
            ),
            cast_to=AlbumBulkRetrieveResponse,
        )

    def list_tracks(
        self,
        id: str,
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
    ) -> SyncCursorURLPage[SimplifiedTrackObject]:
        """Get Spotify catalog information about an album’s tracks.

        Optional parameters can
        be used to limit the number of tracks returned.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the album.

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
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            path_template("/albums/{id}/tracks", id=id),
            page=SyncCursorURLPage[SimplifiedTrackObject],
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
                    album_list_tracks_params.AlbumListTracksParams,
                ),
            ),
            model=SimplifiedTrackObject,
        )


class AsyncAlbumsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAlbumsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncAlbumsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAlbumsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncAlbumsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AlbumRetrieveResponse:
        """
        Get Spotify catalog information for a single album.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the album.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/albums/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"market": market}, album_retrieve_params.AlbumRetrieveParams),
            ),
            cast_to=AlbumRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def bulk_retrieve(
        self,
        *,
        ids: str,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AlbumBulkRetrieveResponse:
        """
        Get Spotify catalog information for multiple albums identified by their Spotify
        IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the albums.
              Maximum: 20 IDs.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/albums",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "market": market,
                    },
                    album_bulk_retrieve_params.AlbumBulkRetrieveParams,
                ),
            ),
            cast_to=AlbumBulkRetrieveResponse,
        )

    def list_tracks(
        self,
        id: str,
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
    ) -> AsyncPaginator[SimplifiedTrackObject, AsyncCursorURLPage[SimplifiedTrackObject]]:
        """Get Spotify catalog information about an album’s tracks.

        Optional parameters can
        be used to limit the number of tracks returned.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the album.

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
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            path_template("/albums/{id}/tracks", id=id),
            page=AsyncCursorURLPage[SimplifiedTrackObject],
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
                    album_list_tracks_params.AlbumListTracksParams,
                ),
            ),
            model=SimplifiedTrackObject,
        )


class AlbumsResourceWithRawResponse:
    def __init__(self, albums: AlbumsResource) -> None:
        self._albums = albums

        self.retrieve = to_raw_response_wrapper(
            albums.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                albums.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_tracks = to_raw_response_wrapper(
            albums.list_tracks,
        )


class AsyncAlbumsResourceWithRawResponse:
    def __init__(self, albums: AsyncAlbumsResource) -> None:
        self._albums = albums

        self.retrieve = async_to_raw_response_wrapper(
            albums.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                albums.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_tracks = async_to_raw_response_wrapper(
            albums.list_tracks,
        )


class AlbumsResourceWithStreamingResponse:
    def __init__(self, albums: AlbumsResource) -> None:
        self._albums = albums

        self.retrieve = to_streamed_response_wrapper(
            albums.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                albums.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_tracks = to_streamed_response_wrapper(
            albums.list_tracks,
        )


class AsyncAlbumsResourceWithStreamingResponse:
    def __init__(self, albums: AsyncAlbumsResource) -> None:
        self._albums = albums

        self.retrieve = async_to_streamed_response_wrapper(
            albums.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                albums.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_tracks = async_to_streamed_response_wrapper(
            albums.list_tracks,
        )
