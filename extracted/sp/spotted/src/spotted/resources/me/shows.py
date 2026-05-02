# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ...types.me import show_list_params, show_save_params, show_check_params, show_remove_params
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.me.show_list_response import ShowListResponse
from ...types.me.show_check_response import ShowCheckResponse

__all__ = ["ShowsResource", "AsyncShowsResource"]


class ShowsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ShowsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return ShowsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ShowsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return ShowsResourceWithStreamingResponse(self)

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
    ) -> SyncCursorURLPage[ShowListResponse]:
        """Get a list of shows saved in the current Spotify user's library.

        Optional
        parameters can be used to limit the number of shows returned.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/shows",
            page=SyncCursorURLPage[ShowListResponse],
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
                    show_list_params.ShowListParams,
                ),
            ),
            model=ShowListResponse,
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
    ) -> ShowCheckResponse:
        """
        Check if one or more shows is already saved in the current Spotify user's
        library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the shows.
              Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/me/shows/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, show_check_params.ShowCheckParams),
            ),
            cast_to=ShowCheckResponse,
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
        Delete one or more shows from current Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids).
              A maximum of 50 items can be specified in one request. _Note: if the `ids`
              parameter is present in the query string, any IDs listed here in the body will
              be ignored._

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
            "/me/shows",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                show_remove_params.ShowRemoveParams,
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
        Save one or more shows to current Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids).
              A maximum of 50 items can be specified in one request. _Note: if the `ids`
              parameter is present in the query string, any IDs listed here in the body will
              be ignored._

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
            "/me/shows",
            body=maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                show_save_params.ShowSaveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncShowsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncShowsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncShowsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncShowsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncShowsResourceWithStreamingResponse(self)

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
    ) -> AsyncPaginator[ShowListResponse, AsyncCursorURLPage[ShowListResponse]]:
        """Get a list of shows saved in the current Spotify user's library.

        Optional
        parameters can be used to limit the number of shows returned.

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/shows",
            page=AsyncCursorURLPage[ShowListResponse],
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
                    show_list_params.ShowListParams,
                ),
            ),
            model=ShowListResponse,
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
    ) -> ShowCheckResponse:
        """
        Check if one or more shows is already saved in the current Spotify user's
        library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the shows.
              Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/me/shows/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, show_check_params.ShowCheckParams),
            ),
            cast_to=ShowCheckResponse,
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
        Delete one or more shows from current Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids).
              A maximum of 50 items can be specified in one request. _Note: if the `ids`
              parameter is present in the query string, any IDs listed here in the body will
              be ignored._

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
            "/me/shows",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                show_remove_params.ShowRemoveParams,
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
        Save one or more shows to current Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A JSON array of the
              [Spotify IDs](https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids).
              A maximum of 50 items can be specified in one request. _Note: if the `ids`
              parameter is present in the query string, any IDs listed here in the body will
              be ignored._

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
            "/me/shows",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "published": published,
                },
                show_save_params.ShowSaveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ShowsResourceWithRawResponse:
    def __init__(self, shows: ShowsResource) -> None:
        self._shows = shows

        self.list = to_raw_response_wrapper(
            shows.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                shows.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                shows.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                shows.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncShowsResourceWithRawResponse:
    def __init__(self, shows: AsyncShowsResource) -> None:
        self._shows = shows

        self.list = async_to_raw_response_wrapper(
            shows.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                shows.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                shows.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                shows.save,  # pyright: ignore[reportDeprecated],
            )
        )


class ShowsResourceWithStreamingResponse:
    def __init__(self, shows: ShowsResource) -> None:
        self._shows = shows

        self.list = to_streamed_response_wrapper(
            shows.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                shows.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                shows.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                shows.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncShowsResourceWithStreamingResponse:
    def __init__(self, shows: AsyncShowsResource) -> None:
        self._shows = shows

        self.list = async_to_streamed_response_wrapper(
            shows.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                shows.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                shows.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                shows.save,  # pyright: ignore[reportDeprecated],
            )
        )
