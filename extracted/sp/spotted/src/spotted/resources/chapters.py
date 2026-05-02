# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import chapter_retrieve_params, chapter_bulk_retrieve_params
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
from .._base_client import make_request_options
from ..types.chapter_retrieve_response import ChapterRetrieveResponse
from ..types.chapter_bulk_retrieve_response import ChapterBulkRetrieveResponse

__all__ = ["ChaptersResource", "AsyncChaptersResource"]


class ChaptersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChaptersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return ChaptersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChaptersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return ChaptersResourceWithStreamingResponse(self)

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
    ) -> ChapterRetrieveResponse:
        """Get Spotify catalog information for a single audiobook chapter.

        Chapters are
        only available within the US, UK, Canada, Ireland, New Zealand and Australia
        markets.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              chapter.

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
            path_template("/chapters/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"market": market}, chapter_retrieve_params.ChapterRetrieveParams),
            ),
            cast_to=ChapterRetrieveResponse,
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
    ) -> ChapterBulkRetrieveResponse:
        """
        Get Spotify catalog information for several audiobook chapters identified by
        their Spotify IDs. Chapters are only available within the US, UK, Canada,
        Ireland, New Zealand and Australia markets.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU`. Maximum: 50 IDs.

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
            "/chapters",
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
                    chapter_bulk_retrieve_params.ChapterBulkRetrieveParams,
                ),
            ),
            cast_to=ChapterBulkRetrieveResponse,
        )


class AsyncChaptersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChaptersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncChaptersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChaptersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncChaptersResourceWithStreamingResponse(self)

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
    ) -> ChapterRetrieveResponse:
        """Get Spotify catalog information for a single audiobook chapter.

        Chapters are
        only available within the US, UK, Canada, Ireland, New Zealand and Australia
        markets.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              chapter.

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
            path_template("/chapters/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"market": market}, chapter_retrieve_params.ChapterRetrieveParams),
            ),
            cast_to=ChapterRetrieveResponse,
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
    ) -> ChapterBulkRetrieveResponse:
        """
        Get Spotify catalog information for several audiobook chapters identified by
        their Spotify IDs. Chapters are only available within the US, UK, Canada,
        Ireland, New Zealand and Australia markets.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=0IsXVP0JmcB2adSE338GkK,3ZXb8FKZGU0EHALYX6uCzU`. Maximum: 50 IDs.

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
            "/chapters",
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
                    chapter_bulk_retrieve_params.ChapterBulkRetrieveParams,
                ),
            ),
            cast_to=ChapterBulkRetrieveResponse,
        )


class ChaptersResourceWithRawResponse:
    def __init__(self, chapters: ChaptersResource) -> None:
        self._chapters = chapters

        self.retrieve = to_raw_response_wrapper(
            chapters.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                chapters.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncChaptersResourceWithRawResponse:
    def __init__(self, chapters: AsyncChaptersResource) -> None:
        self._chapters = chapters

        self.retrieve = async_to_raw_response_wrapper(
            chapters.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                chapters.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class ChaptersResourceWithStreamingResponse:
    def __init__(self, chapters: ChaptersResource) -> None:
        self._chapters = chapters

        self.retrieve = to_streamed_response_wrapper(
            chapters.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                chapters.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncChaptersResourceWithStreamingResponse:
    def __init__(self, chapters: AsyncChaptersResource) -> None:
        self._chapters = chapters

        self.retrieve = async_to_streamed_response_wrapper(
            chapters.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                chapters.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
