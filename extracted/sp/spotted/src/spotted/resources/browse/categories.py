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
from ..._base_client import AsyncPaginator, make_request_options
from ...types.browse import category_list_params, category_retrieve_params, category_get_playlists_params
from ...types.browse.category_list_response import CategoryListResponse
from ...types.browse.category_retrieve_response import CategoryRetrieveResponse
from ...types.browse.category_get_playlists_response import CategoryGetPlaylistsResponse

__all__ = ["CategoriesResource", "AsyncCategoriesResource"]


class CategoriesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CategoriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return CategoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CategoriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return CategoriesResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def retrieve(
        self,
        category_id: str,
        *,
        locale: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CategoryRetrieveResponse:
        """
        Get a single category used to tag items in Spotify (on, for example, the Spotify
        player’s “Browse” tab).

        Args:
          category_id: The [Spotify category ID](/documentation/web-api/concepts/spotify-uris-ids) for
              the category.

          locale: The desired language, consisting of an
              [ISO 639-1](http://en.wikipedia.org/wiki/ISO_639-1) language code and an
              [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2),
              joined by an underscore. For example: `es_MX`, meaning &quot;Spanish
              (Mexico)&quot;. Provide this parameter if you want the category strings returned
              in a particular language.<br/> _**Note**: if `locale` is not supplied, or if the
              specified language is not available, the category strings returned will be in
              the Spotify default language (American English)._

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not category_id:
            raise ValueError(f"Expected a non-empty value for `category_id` but received {category_id!r}")
        return self._get(
            path_template("/browse/categories/{category_id}", category_id=category_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"locale": locale}, category_retrieve_params.CategoryRetrieveParams),
            ),
            cast_to=CategoryRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list(
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
    ) -> SyncCursorURLPage[CategoryListResponse]:
        """
        Get a list of categories used to tag items in Spotify (on, for example, the
        Spotify player’s “Browse” tab).

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
        return self._get_api_list(
            "/browse/categories",
            page=SyncCursorURLPage[CategoryListResponse],
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
                    category_list_params.CategoryListParams,
                ),
            ),
            model=CategoryListResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def get_playlists(
        self,
        category_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CategoryGetPlaylistsResponse:
        """
        Get a list of Spotify playlists tagged with a particular category.

        Args:
          category_id: The [Spotify category ID](/documentation/web-api/concepts/spotify-uris-ids) for
              the category.

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not category_id:
            raise ValueError(f"Expected a non-empty value for `category_id` but received {category_id!r}")
        return self._get(
            path_template("/browse/categories/{category_id}/playlists", category_id=category_id),
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
                    category_get_playlists_params.CategoryGetPlaylistsParams,
                ),
            ),
            cast_to=CategoryGetPlaylistsResponse,
        )


class AsyncCategoriesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCategoriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncCategoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCategoriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncCategoriesResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def retrieve(
        self,
        category_id: str,
        *,
        locale: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CategoryRetrieveResponse:
        """
        Get a single category used to tag items in Spotify (on, for example, the Spotify
        player’s “Browse” tab).

        Args:
          category_id: The [Spotify category ID](/documentation/web-api/concepts/spotify-uris-ids) for
              the category.

          locale: The desired language, consisting of an
              [ISO 639-1](http://en.wikipedia.org/wiki/ISO_639-1) language code and an
              [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2),
              joined by an underscore. For example: `es_MX`, meaning &quot;Spanish
              (Mexico)&quot;. Provide this parameter if you want the category strings returned
              in a particular language.<br/> _**Note**: if `locale` is not supplied, or if the
              specified language is not available, the category strings returned will be in
              the Spotify default language (American English)._

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not category_id:
            raise ValueError(f"Expected a non-empty value for `category_id` but received {category_id!r}")
        return await self._get(
            path_template("/browse/categories/{category_id}", category_id=category_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"locale": locale}, category_retrieve_params.CategoryRetrieveParams),
            ),
            cast_to=CategoryRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list(
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
    ) -> AsyncPaginator[CategoryListResponse, AsyncCursorURLPage[CategoryListResponse]]:
        """
        Get a list of categories used to tag items in Spotify (on, for example, the
        Spotify player’s “Browse” tab).

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
        return self._get_api_list(
            "/browse/categories",
            page=AsyncCursorURLPage[CategoryListResponse],
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
                    category_list_params.CategoryListParams,
                ),
            ),
            model=CategoryListResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def get_playlists(
        self,
        category_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CategoryGetPlaylistsResponse:
        """
        Get a list of Spotify playlists tagged with a particular category.

        Args:
          category_id: The [Spotify category ID](/documentation/web-api/concepts/spotify-uris-ids) for
              the category.

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not category_id:
            raise ValueError(f"Expected a non-empty value for `category_id` but received {category_id!r}")
        return await self._get(
            path_template("/browse/categories/{category_id}/playlists", category_id=category_id),
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
                    category_get_playlists_params.CategoryGetPlaylistsParams,
                ),
            ),
            cast_to=CategoryGetPlaylistsResponse,
        )


class CategoriesResourceWithRawResponse:
    def __init__(self, categories: CategoriesResource) -> None:
        self._categories = categories

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                categories.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                categories.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_playlists = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                categories.get_playlists,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncCategoriesResourceWithRawResponse:
    def __init__(self, categories: AsyncCategoriesResource) -> None:
        self._categories = categories

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                categories.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                categories.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_playlists = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                categories.get_playlists,  # pyright: ignore[reportDeprecated],
            )
        )


class CategoriesResourceWithStreamingResponse:
    def __init__(self, categories: CategoriesResource) -> None:
        self._categories = categories

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                categories.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                categories.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_playlists = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                categories.get_playlists,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncCategoriesResourceWithStreamingResponse:
    def __init__(self, categories: AsyncCategoriesResource) -> None:
        self._categories = categories

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                categories.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                categories.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.get_playlists = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                categories.get_playlists,  # pyright: ignore[reportDeprecated],
            )
        )
