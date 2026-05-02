# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import episode_retrieve_params, episode_bulk_retrieve_params
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
from ..types.shared.episode_object import EpisodeObject
from ..types.episode_bulk_retrieve_response import EpisodeBulkRetrieveResponse

__all__ = ["EpisodesResource", "AsyncEpisodesResource"]


class EpisodesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EpisodesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return EpisodesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EpisodesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return EpisodesResourceWithStreamingResponse(self)

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
    ) -> EpisodeObject:
        """
        Get Spotify catalog information for a single episode identified by its unique
        Spotify ID.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              episode.

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
            path_template("/episodes/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"market": market}, episode_retrieve_params.EpisodeRetrieveParams),
            ),
            cast_to=EpisodeObject,
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
    ) -> EpisodeBulkRetrieveResponse:
        """
        Get Spotify catalog information for several episodes based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the
              episodes. Maximum: 50 IDs.

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
            "/episodes",
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
                    episode_bulk_retrieve_params.EpisodeBulkRetrieveParams,
                ),
            ),
            cast_to=EpisodeBulkRetrieveResponse,
        )


class AsyncEpisodesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEpisodesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncEpisodesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEpisodesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncEpisodesResourceWithStreamingResponse(self)

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
    ) -> EpisodeObject:
        """
        Get Spotify catalog information for a single episode identified by its unique
        Spotify ID.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
              episode.

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
            path_template("/episodes/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"market": market}, episode_retrieve_params.EpisodeRetrieveParams),
            ),
            cast_to=EpisodeObject,
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
    ) -> EpisodeBulkRetrieveResponse:
        """
        Get Spotify catalog information for several episodes based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the
              episodes. Maximum: 50 IDs.

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
            "/episodes",
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
                    episode_bulk_retrieve_params.EpisodeBulkRetrieveParams,
                ),
            ),
            cast_to=EpisodeBulkRetrieveResponse,
        )


class EpisodesResourceWithRawResponse:
    def __init__(self, episodes: EpisodesResource) -> None:
        self._episodes = episodes

        self.retrieve = to_raw_response_wrapper(
            episodes.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                episodes.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncEpisodesResourceWithRawResponse:
    def __init__(self, episodes: AsyncEpisodesResource) -> None:
        self._episodes = episodes

        self.retrieve = async_to_raw_response_wrapper(
            episodes.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                episodes.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class EpisodesResourceWithStreamingResponse:
    def __init__(self, episodes: EpisodesResource) -> None:
        self._episodes = episodes

        self.retrieve = to_streamed_response_wrapper(
            episodes.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                episodes.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncEpisodesResourceWithStreamingResponse:
    def __init__(self, episodes: AsyncEpisodesResource) -> None:
        self._episodes = episodes

        self.retrieve = async_to_streamed_response_wrapper(
            episodes.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                episodes.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
