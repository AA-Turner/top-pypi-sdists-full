# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import track_retrieve_params, track_bulk_retrieve_params
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
from ..types.shared.track_object import TrackObject
from ..types.track_bulk_retrieve_response import TrackBulkRetrieveResponse

__all__ = ["TracksResource", "AsyncTracksResource"]


class TracksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TracksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return TracksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TracksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return TracksResourceWithStreamingResponse(self)

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
    ) -> TrackObject:
        """
        Get Spotify catalog information for a single track identified by its unique
        Spotify ID.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              track.

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
            path_template("/tracks/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"market": market}, track_retrieve_params.TrackRetrieveParams),
            ),
            cast_to=TrackObject,
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
    ) -> TrackBulkRetrieveResponse:
        """
        Get Spotify catalog information for multiple tracks based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=4iV5W9uYEdYUVa79Axb7Rh,1301WleyT98MSxVHPZCA6M`. Maximum: 50 IDs.

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
            "/tracks",
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
                    track_bulk_retrieve_params.TrackBulkRetrieveParams,
                ),
            ),
            cast_to=TrackBulkRetrieveResponse,
        )


class AsyncTracksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTracksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncTracksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTracksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncTracksResourceWithStreamingResponse(self)

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
    ) -> TrackObject:
        """
        Get Spotify catalog information for a single track identified by its unique
        Spotify ID.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              track.

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
            path_template("/tracks/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"market": market}, track_retrieve_params.TrackRetrieveParams),
            ),
            cast_to=TrackObject,
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
    ) -> TrackBulkRetrieveResponse:
        """
        Get Spotify catalog information for multiple tracks based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
              `ids=4iV5W9uYEdYUVa79Axb7Rh,1301WleyT98MSxVHPZCA6M`. Maximum: 50 IDs.

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
            "/tracks",
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
                    track_bulk_retrieve_params.TrackBulkRetrieveParams,
                ),
            ),
            cast_to=TrackBulkRetrieveResponse,
        )


class TracksResourceWithRawResponse:
    def __init__(self, tracks: TracksResource) -> None:
        self._tracks = tracks

        self.retrieve = to_raw_response_wrapper(
            tracks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncTracksResourceWithRawResponse:
    def __init__(self, tracks: AsyncTracksResource) -> None:
        self._tracks = tracks

        self.retrieve = async_to_raw_response_wrapper(
            tracks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class TracksResourceWithStreamingResponse:
    def __init__(self, tracks: TracksResource) -> None:
        self._tracks = tracks

        self.retrieve = to_streamed_response_wrapper(
            tracks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncTracksResourceWithStreamingResponse:
    def __init__(self, tracks: AsyncTracksResource) -> None:
        self._tracks = tracks

        self.retrieve = async_to_streamed_response_wrapper(
            tracks.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
