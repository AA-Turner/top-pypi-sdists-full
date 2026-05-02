# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import audiobook_retrieve_params, audiobook_bulk_retrieve_params, audiobook_list_chapters_params
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
from ..types.simplified_chapter_object import SimplifiedChapterObject
from ..types.audiobook_retrieve_response import AudiobookRetrieveResponse
from ..types.audiobook_bulk_retrieve_response import AudiobookBulkRetrieveResponse

__all__ = ["AudiobooksResource", "AsyncAudiobooksResource"]


class AudiobooksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AudiobooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AudiobooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AudiobooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AudiobooksResourceWithStreamingResponse(self)

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
    ) -> AudiobookRetrieveResponse:
        """Get Spotify catalog information for a single audiobook.

        Audiobooks are only
        available within the US, UK, Canada, Ireland, New Zealand and Australia markets.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              audiobook.

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
            path_template("/audiobooks/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"market": market}, audiobook_retrieve_params.AudiobookRetrieveParams),
            ),
            cast_to=AudiobookRetrieveResponse,
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
    ) -> AudiobookBulkRetrieveResponse:
        """
        Get Spotify catalog information for several audiobooks identified by their
        Spotify IDs. Audiobooks are only available within the US, UK, Canada, Ireland,
        New Zealand and Australia markets.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

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
            "/audiobooks",
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
                    audiobook_bulk_retrieve_params.AudiobookBulkRetrieveParams,
                ),
            ),
            cast_to=AudiobookBulkRetrieveResponse,
        )

    def list_chapters(
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
    ) -> SyncCursorURLPage[SimplifiedChapterObject]:
        """Get Spotify catalog information about an audiobook's chapters.

        Audiobooks are
        only available within the US, UK, Canada, Ireland, New Zealand and Australia
        markets.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              audiobook.

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
            path_template("/audiobooks/{id}/chapters", id=id),
            page=SyncCursorURLPage[SimplifiedChapterObject],
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
                    audiobook_list_chapters_params.AudiobookListChaptersParams,
                ),
            ),
            model=SimplifiedChapterObject,
        )


class AsyncAudiobooksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAudiobooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncAudiobooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAudiobooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncAudiobooksResourceWithStreamingResponse(self)

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
    ) -> AudiobookRetrieveResponse:
        """Get Spotify catalog information for a single audiobook.

        Audiobooks are only
        available within the US, UK, Canada, Ireland, New Zealand and Australia markets.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              audiobook.

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
            path_template("/audiobooks/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"market": market}, audiobook_retrieve_params.AudiobookRetrieveParams
                ),
            ),
            cast_to=AudiobookRetrieveResponse,
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
    ) -> AudiobookBulkRetrieveResponse:
        """
        Get Spotify catalog information for several audiobooks identified by their
        Spotify IDs. Audiobooks are only available within the US, UK, Canada, Ireland,
        New Zealand and Australia markets.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

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
            "/audiobooks",
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
                    audiobook_bulk_retrieve_params.AudiobookBulkRetrieveParams,
                ),
            ),
            cast_to=AudiobookBulkRetrieveResponse,
        )

    def list_chapters(
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
    ) -> AsyncPaginator[SimplifiedChapterObject, AsyncCursorURLPage[SimplifiedChapterObject]]:
        """Get Spotify catalog information about an audiobook's chapters.

        Audiobooks are
        only available within the US, UK, Canada, Ireland, New Zealand and Australia
        markets.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              audiobook.

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
            path_template("/audiobooks/{id}/chapters", id=id),
            page=AsyncCursorURLPage[SimplifiedChapterObject],
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
                    audiobook_list_chapters_params.AudiobookListChaptersParams,
                ),
            ),
            model=SimplifiedChapterObject,
        )


class AudiobooksResourceWithRawResponse:
    def __init__(self, audiobooks: AudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.retrieve = to_raw_response_wrapper(
            audiobooks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audiobooks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_chapters = to_raw_response_wrapper(
            audiobooks.list_chapters,
        )


class AsyncAudiobooksResourceWithRawResponse:
    def __init__(self, audiobooks: AsyncAudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.retrieve = async_to_raw_response_wrapper(
            audiobooks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audiobooks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_chapters = async_to_raw_response_wrapper(
            audiobooks.list_chapters,
        )


class AudiobooksResourceWithStreamingResponse:
    def __init__(self, audiobooks: AudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.retrieve = to_streamed_response_wrapper(
            audiobooks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audiobooks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_chapters = to_streamed_response_wrapper(
            audiobooks.list_chapters,
        )


class AsyncAudiobooksResourceWithStreamingResponse:
    def __init__(self, audiobooks: AsyncAudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.retrieve = async_to_streamed_response_wrapper(
            audiobooks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audiobooks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_chapters = async_to_streamed_response_wrapper(
            audiobooks.list_chapters,
        )
