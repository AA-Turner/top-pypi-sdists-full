# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import path_template
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.audio_analysis_retrieve_response import AudioAnalysisRetrieveResponse

__all__ = ["AudioAnalysisResource", "AsyncAudioAnalysisResource"]


class AudioAnalysisResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AudioAnalysisResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AudioAnalysisResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AudioAnalysisResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AudioAnalysisResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AudioAnalysisRetrieveResponse:
        """Get a low-level audio analysis for a track in the Spotify catalog.

        The audio
        analysis describes the track’s structure and musical content, including rhythm,
        pitch, and timbre.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              track.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/audio-analysis/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AudioAnalysisRetrieveResponse,
        )


class AsyncAudioAnalysisResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAudioAnalysisResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncAudioAnalysisResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAudioAnalysisResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncAudioAnalysisResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AudioAnalysisRetrieveResponse:
        """Get a low-level audio analysis for a track in the Spotify catalog.

        The audio
        analysis describes the track’s structure and musical content, including rhythm,
        pitch, and timbre.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              track.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/audio-analysis/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AudioAnalysisRetrieveResponse,
        )


class AudioAnalysisResourceWithRawResponse:
    def __init__(self, audio_analysis: AudioAnalysisResource) -> None:
        self._audio_analysis = audio_analysis

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audio_analysis.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAudioAnalysisResourceWithRawResponse:
    def __init__(self, audio_analysis: AsyncAudioAnalysisResource) -> None:
        self._audio_analysis = audio_analysis

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audio_analysis.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AudioAnalysisResourceWithStreamingResponse:
    def __init__(self, audio_analysis: AudioAnalysisResource) -> None:
        self._audio_analysis = audio_analysis

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audio_analysis.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAudioAnalysisResourceWithStreamingResponse:
    def __init__(self, audio_analysis: AsyncAudioAnalysisResource) -> None:
        self._audio_analysis = audio_analysis

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audio_analysis.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
