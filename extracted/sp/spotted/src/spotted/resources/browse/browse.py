# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ...types import browse_get_new_releases_params, browse_get_featured_playlists_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .categories import (
    CategoriesResource,
    AsyncCategoriesResource,
    CategoriesResourceWithRawResponse,
    AsyncCategoriesResourceWithRawResponse,
    CategoriesResourceWithStreamingResponse,
    AsyncCategoriesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.browse_get_new_releases_response import BrowseGetNewReleasesResponse
from ...types.browse_get_featured_playlists_response import BrowseGetFeaturedPlaylistsResponse

__all__ = ["BrowseResource", "AsyncBrowseResource"]


class BrowseResource(SyncAPIResource):
    @cached_property
    def categories(self) -> CategoriesResource:
        return CategoriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> BrowseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return BrowseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BrowseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return BrowseResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def get_featured_playlists(
        self,
        *,
        limit: int | Omit = omit,
        locale: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BrowseGetFeaturedPlaylistsResponse:
        """
        Get a list of Spotify featured playlists (shown, for example, on a Spotify
        player's 'Browse' tab).

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          locale: The desired language, consisting of an
              [ISO 639-1](http://en.wikipedia.org/wiki/ISO_639-1) language code and an
              [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2),
              joined by an underscore. For example: `es_MX`, meaning &quot;Spanish
              (Mexico)&quot;. Provide this parameter if you want the category strings returned
              in a particular language.<br/> _**Note**: if `locale` is not supplied, or if the
              specified language is not available, the category strings returned will be in
              the Spotify default language (American English)._

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/browse/featured-playlists",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "locale": locale,
                        "offset": offset,
                    },
                    browse_get_featured_playlists_params.BrowseGetFeaturedPlaylistsParams,
                ),
            ),
            cast_to=BrowseGetFeaturedPlaylistsResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def get_new_releases(
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
    ) -> BrowseGetNewReleasesResponse:
        """
        Get a list of new album releases featured in Spotify (shown, for example, on a
        Spotify player’s “Browse” tab).

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/browse/new-releases",
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
                    browse_get_new_releases_params.BrowseGetNewReleasesParams,
                ),
            ),
            cast_to=BrowseGetNewReleasesResponse,
        )


class AsyncBrowseResource(AsyncAPIResource):
    @cached_property
    def categories(self) -> AsyncCategoriesResource:
        return AsyncCategoriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBrowseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncBrowseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBrowseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncBrowseResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def get_featured_playlists(
        self,
        *,
        limit: int | Omit = omit,
        locale: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BrowseGetFeaturedPlaylistsResponse:
        """
        Get a list of Spotify featured playlists (shown, for example, on a Spotify
        player's 'Browse' tab).

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          locale: The desired language, consisting of an
              [ISO 639-1](http://en.wikipedia.org/wiki/ISO_639-1) language code and an
              [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2),
              joined by an underscore. For example: `es_MX`, meaning &quot;Spanish
              (Mexico)&quot;. Provide this parameter if you want the category strings returned
              in a particular language.<br/> _**Note**: if `locale` is not supplied, or if the
              specified language is not available, the category strings returned will be in
              the Spotify default language (American English)._

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/browse/featured-playlists",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "locale": locale,
                        "offset": offset,
                    },
                    browse_get_featured_playlists_params.BrowseGetFeaturedPlaylistsParams,
                ),
            ),
            cast_to=BrowseGetFeaturedPlaylistsResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def get_new_releases(
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
    ) -> BrowseGetNewReleasesResponse:
        """
        Get a list of new album releases featured in Spotify (shown, for example, on a
        Spotify player’s “Browse” tab).

        Args:
          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/browse/new-releases",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    browse_get_new_releases_params.BrowseGetNewReleasesParams,
                ),
            ),
            cast_to=BrowseGetNewReleasesResponse,
        )


class BrowseResourceWithRawResponse:
    def __init__(self, browse: BrowseResource) -> None:
        self._browse = browse

        self.get_featured_playlists = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                browse.get_featured_playlists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_new_releases = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                browse.get_new_releases,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def categories(self) -> CategoriesResourceWithRawResponse:
        return CategoriesResourceWithRawResponse(self._browse.categories)


class AsyncBrowseResourceWithRawResponse:
    def __init__(self, browse: AsyncBrowseResource) -> None:
        self._browse = browse

        self.get_featured_playlists = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                browse.get_featured_playlists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_new_releases = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                browse.get_new_releases,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def categories(self) -> AsyncCategoriesResourceWithRawResponse:
        return AsyncCategoriesResourceWithRawResponse(self._browse.categories)


class BrowseResourceWithStreamingResponse:
    def __init__(self, browse: BrowseResource) -> None:
        self._browse = browse

        self.get_featured_playlists = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                browse.get_featured_playlists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_new_releases = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                browse.get_new_releases,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def categories(self) -> CategoriesResourceWithStreamingResponse:
        return CategoriesResourceWithStreamingResponse(self._browse.categories)


class AsyncBrowseResourceWithStreamingResponse:
    def __init__(self, browse: AsyncBrowseResource) -> None:
        self._browse = browse

        self.get_featured_playlists = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                browse.get_featured_playlists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_new_releases = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                browse.get_new_releases,  # pyright: ignore[reportDeprecated],
            )
        )

    @cached_property
    def categories(self) -> AsyncCategoriesResourceWithStreamingResponse:
        return AsyncCategoriesResourceWithStreamingResponse(self._browse.categories)
