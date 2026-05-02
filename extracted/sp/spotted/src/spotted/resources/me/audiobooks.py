# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ...types.me import audiobook_list_params, audiobook_save_params, audiobook_check_params, audiobook_remove_params
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.me.audiobook_list_response import AudiobookListResponse
from ...types.me.audiobook_check_response import AudiobookCheckResponse

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
    ) -> SyncCursorURLPage[AudiobookListResponse]:
        """
        Get a list of the audiobooks saved in the current Spotify user's 'Your Music'
        library.

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
            "/me/audiobooks",
            page=SyncCursorURLPage[AudiobookListResponse],
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
                    audiobook_list_params.AudiobookListParams,
                ),
            ),
            model=AudiobookListResponse,
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
    ) -> AudiobookCheckResponse:
        """
        Check if one or more audiobooks are already saved in the current Spotify user's
        library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/me/audiobooks/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, audiobook_check_params.AudiobookCheckParams),
            ),
            cast_to=AudiobookCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def remove(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove one or more audiobooks from the Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/me/audiobooks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, audiobook_remove_params.AudiobookRemoveParams),
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    def save(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Save one or more audiobooks to the current Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/audiobooks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, audiobook_save_params.AudiobookSaveParams),
            ),
            cast_to=NoneType,
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
    ) -> AsyncPaginator[AudiobookListResponse, AsyncCursorURLPage[AudiobookListResponse]]:
        """
        Get a list of the audiobooks saved in the current Spotify user's 'Your Music'
        library.

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
            "/me/audiobooks",
            page=AsyncCursorURLPage[AudiobookListResponse],
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
                    audiobook_list_params.AudiobookListParams,
                ),
            ),
            model=AudiobookListResponse,
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
    ) -> AudiobookCheckResponse:
        """
        Check if one or more audiobooks are already saved in the current Spotify user's
        library.

        **Note:** This endpoint is deprecated. Use
        [Check User's Saved Items](/documentation/web-api/reference/check-library-contains)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/me/audiobooks/contains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, audiobook_check_params.AudiobookCheckParams),
            ),
            cast_to=AudiobookCheckResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def remove(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove one or more audiobooks from the Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Remove Items from Library](/documentation/web-api/reference/remove-library-items)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/me/audiobooks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, audiobook_remove_params.AudiobookRemoveParams),
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("deprecated")
    async def save(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Save one or more audiobooks to the current Spotify user's library.

        **Note:** This endpoint is deprecated. Use
        [Save Items to Library](/documentation/web-api/reference/save-library-items)
        instead.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/audiobooks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, audiobook_save_params.AudiobookSaveParams),
            ),
            cast_to=NoneType,
        )


class AudiobooksResourceWithRawResponse:
    def __init__(self, audiobooks: AudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.list = to_raw_response_wrapper(
            audiobooks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audiobooks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audiobooks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audiobooks.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAudiobooksResourceWithRawResponse:
    def __init__(self, audiobooks: AsyncAudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.list = async_to_raw_response_wrapper(
            audiobooks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audiobooks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audiobooks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audiobooks.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AudiobooksResourceWithStreamingResponse:
    def __init__(self, audiobooks: AudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.list = to_streamed_response_wrapper(
            audiobooks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audiobooks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audiobooks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audiobooks.save,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAudiobooksResourceWithStreamingResponse:
    def __init__(self, audiobooks: AsyncAudiobooksResource) -> None:
        self._audiobooks = audiobooks

        self.list = async_to_streamed_response_wrapper(
            audiobooks.list,
        )
        self.check = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audiobooks.check,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audiobooks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
        self.save = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audiobooks.save,  # pyright: ignore[reportDeprecated],
            )
        )
