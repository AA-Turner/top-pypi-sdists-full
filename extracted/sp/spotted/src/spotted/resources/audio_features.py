# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import audio_feature_bulk_retrieve_params
from .._types import Body, Query, Headers, NotGiven, not_given
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
from ..types.audio_feature_retrieve_response import AudioFeatureRetrieveResponse
from ..types.audio_feature_bulk_retrieve_response import AudioFeatureBulkRetrieveResponse

__all__ = ["AudioFeaturesResource", "AsyncAudioFeaturesResource"]


class AudioFeaturesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AudioFeaturesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AudioFeaturesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AudioFeaturesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AudioFeaturesResourceWithStreamingResponse(self)

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
    ) -> AudioFeatureRetrieveResponse:
        """
        Get audio feature information for a single track identified by its unique
        Spotify ID.

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
            path_template("/audio-features/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AudioFeatureRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def bulk_retrieve(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AudioFeatureBulkRetrieveResponse:
        """
        Get audio features for multiple tracks based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the tracks.
              Maximum: 100 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/audio-features",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, audio_feature_bulk_retrieve_params.AudioFeatureBulkRetrieveParams),
            ),
            cast_to=AudioFeatureBulkRetrieveResponse,
        )


class AsyncAudioFeaturesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAudioFeaturesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncAudioFeaturesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAudioFeaturesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncAudioFeaturesResourceWithStreamingResponse(self)

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
    ) -> AudioFeatureRetrieveResponse:
        """
        Get audio feature information for a single track identified by its unique
        Spotify ID.

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
            path_template("/audio-features/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AudioFeatureRetrieveResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def bulk_retrieve(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AudioFeatureBulkRetrieveResponse:
        """
        Get audio features for multiple tracks based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the tracks.
              Maximum: 100 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/audio-features",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"ids": ids}, audio_feature_bulk_retrieve_params.AudioFeatureBulkRetrieveParams
                ),
            ),
            cast_to=AudioFeatureBulkRetrieveResponse,
        )


class AudioFeaturesResourceWithRawResponse:
    def __init__(self, audio_features: AudioFeaturesResource) -> None:
        self._audio_features = audio_features

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audio_features.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                audio_features.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAudioFeaturesResourceWithRawResponse:
    def __init__(self, audio_features: AsyncAudioFeaturesResource) -> None:
        self._audio_features = audio_features

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audio_features.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                audio_features.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AudioFeaturesResourceWithStreamingResponse:
    def __init__(self, audio_features: AudioFeaturesResource) -> None:
        self._audio_features = audio_features

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audio_features.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                audio_features.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncAudioFeaturesResourceWithStreamingResponse:
    def __init__(self, audio_features: AsyncAudioFeaturesResource) -> None:
        self._audio_features = audio_features

        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audio_features.retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                audio_features.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
