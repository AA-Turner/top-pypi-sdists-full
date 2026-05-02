# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ...types.me import album_list_params, album_save_params, album_check_params, album_remove_params
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.me.album_list_response import AlbumListResponse
from ...types.me.album_check_response import AlbumCheckResponse

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
    ) -> SyncCursorURLPage[AlbumListResponse]:
        """
        Get a list of the albums saved in the current Spotify user's 'Your Music'
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
            "/me/albums",
            page=SyncCursorURLPage[AlbumListResponse],
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
                    album_list_params.AlbumListParams,
                ),
            ),
            model=AlbumListResponse,
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
    ) -> AlbumCheckResponse:
        """
        Check if one or more albums is already saved in the current Spotify user's 'Your
        Music' library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the albums.
              Maximum: 20 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/me/albums/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, album_check_params.AlbumCheckParams),
            ),
            cast_to=AlbumCheckResponse,
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
        Remove one or more albums from the current user's 'Your Music' library.

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
            "/me/albums",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                album_remove_params.AlbumRemoveParams,
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
        Save one or more albums to the current user's 'Your Music' library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
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
        return self._put(
            "/me/albums",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                album_save_params.AlbumSaveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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
    ) -> AsyncPaginator[AlbumListResponse, AsyncCursorURLPage[AlbumListResponse]]:
        """
        Get a list of the albums saved in the current Spotify user's 'Your Music'
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
            "/me/albums",
            page=AsyncCursorURLPage[AlbumListResponse],
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
                    album_list_params.AlbumListParams,
                ),
            ),
            model=AlbumListResponse,
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
    ) -> AlbumCheckResponse:
        """
        Check if one or more albums is already saved in the current Spotify user's 'Your
        Music' library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the albums.
              Maximum: 20 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/me/albums/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, album_check_params.AlbumCheckParams),
            ),
            cast_to=AlbumCheckResponse,
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
        Remove one or more albums from the current user's 'Your Music' library.

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
            "/me/albums",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                album_remove_params.AlbumRemoveParams,
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
        Save one or more albums to the current user's 'Your Music' library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
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
        return await self._put(
            "/me/albums",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                album_save_params.AlbumSaveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AlbumsResourceWithRawResponse:
    def __init__(self, albums: AlbumsResource) -> None:
        self._albums = albums

        self.list = to_raw_response_wrapper(
            albums.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                albums.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                albums.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                albums.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAlbumsResourceWithRawResponse:
    def __init__(self, albums: AsyncAlbumsResource) -> None:
        self._albums = albums

        self.list = async_to_raw_response_wrapper(
            albums.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                albums.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                albums.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                albums.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AlbumsResourceWithStreamingResponse:
    def __init__(self, albums: AlbumsResource) -> None:
        self._albums = albums

        self.list = to_streamed_response_wrapper(
            albums.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                albums.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                albums.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                albums.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAlbumsResourceWithStreamingResponse:
    def __init__(self, albums: AsyncAlbumsResource) -> None:
        self._albums = albums

        self.list = async_to_streamed_response_wrapper(
            albums.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                albums.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                albums.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                albums.save,  # pyright: ignore[reportDeprecated],
            )
        )
