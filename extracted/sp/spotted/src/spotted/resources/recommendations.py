# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import recommendation_get_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.recommendation_get_response import RecommendationGetResponse
from ..types.recommendation_list_available_genre_seeds_response import RecommendationListAvailableGenreSeedsResponse

__all__ = ["RecommendationsResource", "AsyncRecommendationsResource"]


class RecommendationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RecommendationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return RecommendationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RecommendationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return RecommendationsResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def get(
        self,
        *,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        max_acousticness: float | Omit = omit,
        max_danceability: float | Omit = omit,
        max_duration_ms: int | Omit = omit,
        max_energy: float | Omit = omit,
        max_instrumentalness: float | Omit = omit,
        max_key: int | Omit = omit,
        max_liveness: float | Omit = omit,
        max_loudness: float | Omit = omit,
        max_mode: int | Omit = omit,
        max_popularity: int | Omit = omit,
        max_speechiness: float | Omit = omit,
        max_tempo: float | Omit = omit,
        max_time_signature: int | Omit = omit,
        max_valence: float | Omit = omit,
        min_acousticness: float | Omit = omit,
        min_danceability: float | Omit = omit,
        min_duration_ms: int | Omit = omit,
        min_energy: float | Omit = omit,
        min_instrumentalness: float | Omit = omit,
        min_key: int | Omit = omit,
        min_liveness: float | Omit = omit,
        min_loudness: float | Omit = omit,
        min_mode: int | Omit = omit,
        min_popularity: int | Omit = omit,
        min_speechiness: float | Omit = omit,
        min_tempo: float | Omit = omit,
        min_time_signature: int | Omit = omit,
        min_valence: float | Omit = omit,
        seed_artists: str | Omit = omit,
        seed_genres: str | Omit = omit,
        seed_tracks: str | Omit = omit,
        target_acousticness: float | Omit = omit,
        target_danceability: float | Omit = omit,
        target_duration_ms: int | Omit = omit,
        target_energy: float | Omit = omit,
        target_instrumentalness: float | Omit = omit,
        target_key: int | Omit = omit,
        target_liveness: float | Omit = omit,
        target_loudness: float | Omit = omit,
        target_mode: int | Omit = omit,
        target_popularity: int | Omit = omit,
        target_speechiness: float | Omit = omit,
        target_tempo: float | Omit = omit,
        target_time_signature: int | Omit = omit,
        target_valence: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RecommendationGetResponse:
        """
        Recommendations are generated based on the available information for a given
        seed entity and matched against similar artists and tracks. If there is
        sufficient information about the provided seeds, a list of tracks will be
        returned together with pool size details.

        For artists and tracks that are very new or obscure there might not be enough
        data to generate a list of tracks.

        Args:
          limit: The target size of the list of recommended tracks. For seeds with unusually
              small pools or when highly restrictive filtering is applied, it may be
              impossible to generate the requested number of recommended tracks. Debugging
              information for such cases is available in the response. Default: 20\\.. Minimum:
              1\\.. Maximum: 100.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          max_acousticness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_danceability: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_duration_ms: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_energy: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_instrumentalness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_key: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_liveness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_loudness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_mode: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_popularity: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_speechiness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_tempo: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_time_signature: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_valence: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          min_acousticness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_danceability: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_duration_ms: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_energy: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_instrumentalness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_key: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_liveness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_loudness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_mode: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_popularity: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_speechiness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_tempo: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_time_signature: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_valence: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          seed_artists: A comma separated list of
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for seed
              artists. Up to 5 seed values may be provided in any combination of
              `seed_artists`, `seed_tracks` and `seed_genres`.<br/> _**Note**: only required
              if `seed_genres` and `seed_tracks` are not set_.

          seed_genres: A comma separated list of any genres in the set of
              [available genre seeds](/documentation/web-api/reference/get-recommendation-genres).
              Up to 5 seed values may be provided in any combination of `seed_artists`,
              `seed_tracks` and `seed_genres`.<br/> _**Note**: only required if `seed_artists`
              and `seed_tracks` are not set_.

          seed_tracks: A comma separated list of
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for a seed
              track. Up to 5 seed values may be provided in any combination of `seed_artists`,
              `seed_tracks` and `seed_genres`.<br/> _**Note**: only required if `seed_artists`
              and `seed_genres` are not set_.

          target_acousticness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_danceability: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_duration_ms: Target duration of the track (ms)

          target_energy: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_instrumentalness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_key: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_liveness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_loudness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_mode: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_popularity: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_speechiness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_tempo: Target tempo (BPM)

          target_time_signature: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_valence: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/recommendations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "market": market,
                        "max_acousticness": max_acousticness,
                        "max_danceability": max_danceability,
                        "max_duration_ms": max_duration_ms,
                        "max_energy": max_energy,
                        "max_instrumentalness": max_instrumentalness,
                        "max_key": max_key,
                        "max_liveness": max_liveness,
                        "max_loudness": max_loudness,
                        "max_mode": max_mode,
                        "max_popularity": max_popularity,
                        "max_speechiness": max_speechiness,
                        "max_tempo": max_tempo,
                        "max_time_signature": max_time_signature,
                        "max_valence": max_valence,
                        "min_acousticness": min_acousticness,
                        "min_danceability": min_danceability,
                        "min_duration_ms": min_duration_ms,
                        "min_energy": min_energy,
                        "min_instrumentalness": min_instrumentalness,
                        "min_key": min_key,
                        "min_liveness": min_liveness,
                        "min_loudness": min_loudness,
                        "min_mode": min_mode,
                        "min_popularity": min_popularity,
                        "min_speechiness": min_speechiness,
                        "min_tempo": min_tempo,
                        "min_time_signature": min_time_signature,
                        "min_valence": min_valence,
                        "seed_artists": seed_artists,
                        "seed_genres": seed_genres,
                        "seed_tracks": seed_tracks,
                        "target_acousticness": target_acousticness,
                        "target_danceability": target_danceability,
                        "target_duration_ms": target_duration_ms,
                        "target_energy": target_energy,
                        "target_instrumentalness": target_instrumentalness,
                        "target_key": target_key,
                        "target_liveness": target_liveness,
                        "target_loudness": target_loudness,
                        "target_mode": target_mode,
                        "target_popularity": target_popularity,
                        "target_speechiness": target_speechiness,
                        "target_tempo": target_tempo,
                        "target_time_signature": target_time_signature,
                        "target_valence": target_valence,
                    },
                    recommendation_get_params.RecommendationGetParams,
                ),
            ),
            cast_to=RecommendationGetResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list_available_genre_seeds(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RecommendationListAvailableGenreSeedsResponse:
        """
        Retrieve a list of available genres seed parameter values for
        [recommendations](/documentation/web-api/reference/get-recommendations).
        """
        return self._get(
            "/recommendations/available-genre-seeds",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RecommendationListAvailableGenreSeedsResponse,
        )


class AsyncRecommendationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRecommendationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncRecommendationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRecommendationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncRecommendationsResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def get(
        self,
        *,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        max_acousticness: float | Omit = omit,
        max_danceability: float | Omit = omit,
        max_duration_ms: int | Omit = omit,
        max_energy: float | Omit = omit,
        max_instrumentalness: float | Omit = omit,
        max_key: int | Omit = omit,
        max_liveness: float | Omit = omit,
        max_loudness: float | Omit = omit,
        max_mode: int | Omit = omit,
        max_popularity: int | Omit = omit,
        max_speechiness: float | Omit = omit,
        max_tempo: float | Omit = omit,
        max_time_signature: int | Omit = omit,
        max_valence: float | Omit = omit,
        min_acousticness: float | Omit = omit,
        min_danceability: float | Omit = omit,
        min_duration_ms: int | Omit = omit,
        min_energy: float | Omit = omit,
        min_instrumentalness: float | Omit = omit,
        min_key: int | Omit = omit,
        min_liveness: float | Omit = omit,
        min_loudness: float | Omit = omit,
        min_mode: int | Omit = omit,
        min_popularity: int | Omit = omit,
        min_speechiness: float | Omit = omit,
        min_tempo: float | Omit = omit,
        min_time_signature: int | Omit = omit,
        min_valence: float | Omit = omit,
        seed_artists: str | Omit = omit,
        seed_genres: str | Omit = omit,
        seed_tracks: str | Omit = omit,
        target_acousticness: float | Omit = omit,
        target_danceability: float | Omit = omit,
        target_duration_ms: int | Omit = omit,
        target_energy: float | Omit = omit,
        target_instrumentalness: float | Omit = omit,
        target_key: int | Omit = omit,
        target_liveness: float | Omit = omit,
        target_loudness: float | Omit = omit,
        target_mode: int | Omit = omit,
        target_popularity: int | Omit = omit,
        target_speechiness: float | Omit = omit,
        target_tempo: float | Omit = omit,
        target_time_signature: int | Omit = omit,
        target_valence: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RecommendationGetResponse:
        """
        Recommendations are generated based on the available information for a given
        seed entity and matched against similar artists and tracks. If there is
        sufficient information about the provided seeds, a list of tracks will be
        returned together with pool size details.

        For artists and tracks that are very new or obscure there might not be enough
        data to generate a list of tracks.

        Args:
          limit: The target size of the list of recommended tracks. For seeds with unusually
              small pools or when highly restrictive filtering is applied, it may be
              impossible to generate the requested number of recommended tracks. Debugging
              information for such cases is available in the response. Default: 20\\.. Minimum:
              1\\.. Maximum: 100.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          max_acousticness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_danceability: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_duration_ms: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_energy: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_instrumentalness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_key: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_liveness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_loudness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_mode: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_popularity: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_speechiness: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_tempo: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_time_signature: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          max_valence: For each tunable track attribute, a hard ceiling on the selected track
              attribute’s value can be provided. See tunable track attributes below for the
              list of available options. For example, `max_instrumentalness=0.35` would filter
              out most tracks that are likely to be instrumental.

          min_acousticness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_danceability: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_duration_ms: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_energy: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_instrumentalness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_key: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_liveness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_loudness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_mode: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_popularity: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_speechiness: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_tempo: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_time_signature: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          min_valence: For each tunable track attribute, a hard floor on the selected track attribute’s
              value can be provided. See tunable track attributes below for the list of
              available options. For example, `min_tempo=140` would restrict results to only
              those tracks with a tempo of greater than 140 beats per minute.

          seed_artists: A comma separated list of
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for seed
              artists. Up to 5 seed values may be provided in any combination of
              `seed_artists`, `seed_tracks` and `seed_genres`.<br/> _**Note**: only required
              if `seed_genres` and `seed_tracks` are not set_.

          seed_genres: A comma separated list of any genres in the set of
              [available genre seeds](/documentation/web-api/reference/get-recommendation-genres).
              Up to 5 seed values may be provided in any combination of `seed_artists`,
              `seed_tracks` and `seed_genres`.<br/> _**Note**: only required if `seed_artists`
              and `seed_tracks` are not set_.

          seed_tracks: A comma separated list of
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for a seed
              track. Up to 5 seed values may be provided in any combination of `seed_artists`,
              `seed_tracks` and `seed_genres`.<br/> _**Note**: only required if `seed_artists`
              and `seed_genres` are not set_.

          target_acousticness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_danceability: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_duration_ms: Target duration of the track (ms)

          target_energy: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_instrumentalness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_key: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_liveness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_loudness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_mode: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_popularity: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_speechiness: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_tempo: Target tempo (BPM)

          target_time_signature: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          target_valence: For each of the tunable track attributes (below) a target value may be provided.
              Tracks with the attribute values nearest to the target values will be preferred.
              For example, you might request `target_energy=0.6` and
              `target_danceability=0.8`. All target values will be weighed equally in ranking
              results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/recommendations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "market": market,
                        "max_acousticness": max_acousticness,
                        "max_danceability": max_danceability,
                        "max_duration_ms": max_duration_ms,
                        "max_energy": max_energy,
                        "max_instrumentalness": max_instrumentalness,
                        "max_key": max_key,
                        "max_liveness": max_liveness,
                        "max_loudness": max_loudness,
                        "max_mode": max_mode,
                        "max_popularity": max_popularity,
                        "max_speechiness": max_speechiness,
                        "max_tempo": max_tempo,
                        "max_time_signature": max_time_signature,
                        "max_valence": max_valence,
                        "min_acousticness": min_acousticness,
                        "min_danceability": min_danceability,
                        "min_duration_ms": min_duration_ms,
                        "min_energy": min_energy,
                        "min_instrumentalness": min_instrumentalness,
                        "min_key": min_key,
                        "min_liveness": min_liveness,
                        "min_loudness": min_loudness,
                        "min_mode": min_mode,
                        "min_popularity": min_popularity,
                        "min_speechiness": min_speechiness,
                        "min_tempo": min_tempo,
                        "min_time_signature": min_time_signature,
                        "min_valence": min_valence,
                        "seed_artists": seed_artists,
                        "seed_genres": seed_genres,
                        "seed_tracks": seed_tracks,
                        "target_acousticness": target_acousticness,
                        "target_danceability": target_danceability,
                        "target_duration_ms": target_duration_ms,
                        "target_energy": target_energy,
                        "target_instrumentalness": target_instrumentalness,
                        "target_key": target_key,
                        "target_liveness": target_liveness,
                        "target_loudness": target_loudness,
                        "target_mode": target_mode,
                        "target_popularity": target_popularity,
                        "target_speechiness": target_speechiness,
                        "target_tempo": target_tempo,
                        "target_time_signature": target_time_signature,
                        "target_valence": target_valence,
                    },
                    recommendation_get_params.RecommendationGetParams,
                ),
            ),
            cast_to=RecommendationGetResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def list_available_genre_seeds(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RecommendationListAvailableGenreSeedsResponse:
        """
        Retrieve a list of available genres seed parameter values for
        [recommendations](/documentation/web-api/reference/get-recommendations).
        """
        return await self._get(
            "/recommendations/available-genre-seeds",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RecommendationListAvailableGenreSeedsResponse,
        )


class RecommendationsResourceWithRawResponse:
    def __init__(self, recommendations: RecommendationsResource) -> None:
        self._recommendations = recommendations

        self.get = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                recommendations.get,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_available_genre_seeds = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                recommendations.list_available_genre_seeds,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncRecommendationsResourceWithRawResponse:
    def __init__(self, recommendations: AsyncRecommendationsResource) -> None:
        self._recommendations = recommendations

        self.get = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                recommendations.get,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_available_genre_seeds = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                recommendations.list_available_genre_seeds,  # pyright: ignore[reportDeprecated],
            )
        )


class RecommendationsResourceWithStreamingResponse:
    def __init__(self, recommendations: RecommendationsResource) -> None:
        self._recommendations = recommendations

        self.get = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                recommendations.get,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_available_genre_seeds = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                recommendations.list_available_genre_seeds,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncRecommendationsResourceWithStreamingResponse:
    def __init__(self, recommendations: AsyncRecommendationsResource) -> None:
        self._recommendations = recommendations

        self.get = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                recommendations.get,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_available_genre_seeds = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                recommendations.list_available_genre_seeds,  # pyright: ignore[reportDeprecated],
            )
        )
