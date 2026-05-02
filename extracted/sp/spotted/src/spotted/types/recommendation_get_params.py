# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["RecommendationGetParams"]


class RecommendationGetParams(TypedDict, total=False):
    limit: int
    """The target size of the list of recommended tracks.

    For seeds with unusually small pools or when highly restrictive filtering is
    applied, it may be impossible to generate the requested number of recommended
    tracks. Debugging information for such cases is available in the response.
    Default: 20\\.. Minimum: 1\\.. Maximum: 100.
    """

    market: str
    """
    An
    [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    If a country code is specified, only content that is available in that market
    will be returned.<br/> If a valid user access token is specified in the request
    header, the country associated with the user account will take priority over
    this parameter.<br/> _**Note**: If neither market or user country are provided,
    the content is considered unavailable for the client._<br/> Users can view the
    country that is associated with their account in the
    [account settings](https://www.spotify.com/account/overview/).
    """

    max_acousticness: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_danceability: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_duration_ms: int
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_energy: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_instrumentalness: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_key: int
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_liveness: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_loudness: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_mode: int
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_popularity: int
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_speechiness: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_tempo: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_time_signature: int
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    max_valence: float
    """
    For each tunable track attribute, a hard ceiling on the selected track
    attribute’s value can be provided. See tunable track attributes below for the
    list of available options. For example, `max_instrumentalness=0.35` would filter
    out most tracks that are likely to be instrumental.
    """

    min_acousticness: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_danceability: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_duration_ms: int
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_energy: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_instrumentalness: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_key: int
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_liveness: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_loudness: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_mode: int
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_popularity: int
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_speechiness: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_tempo: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_time_signature: int
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    min_valence: float
    """
    For each tunable track attribute, a hard floor on the selected track attribute’s
    value can be provided. See tunable track attributes below for the list of
    available options. For example, `min_tempo=140` would restrict results to only
    those tracks with a tempo of greater than 140 beats per minute.
    """

    seed_artists: str
    """
    A comma separated list of
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for seed
    artists. Up to 5 seed values may be provided in any combination of
    `seed_artists`, `seed_tracks` and `seed_genres`.<br/> _**Note**: only required
    if `seed_genres` and `seed_tracks` are not set_.
    """

    seed_genres: str
    """
    A comma separated list of any genres in the set of
    [available genre seeds](/documentation/web-api/reference/get-recommendation-genres).
    Up to 5 seed values may be provided in any combination of `seed_artists`,
    `seed_tracks` and `seed_genres`.<br/> _**Note**: only required if `seed_artists`
    and `seed_tracks` are not set_.
    """

    seed_tracks: str
    """
    A comma separated list of
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for a seed
    track. Up to 5 seed values may be provided in any combination of `seed_artists`,
    `seed_tracks` and `seed_genres`.<br/> _**Note**: only required if `seed_artists`
    and `seed_genres` are not set_.
    """

    target_acousticness: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_danceability: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_duration_ms: int
    """Target duration of the track (ms)"""

    target_energy: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_instrumentalness: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_key: int
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_liveness: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_loudness: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_mode: int
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_popularity: int
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_speechiness: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_tempo: float
    """Target tempo (BPM)"""

    target_time_signature: int
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """

    target_valence: float
    """For each of the tunable track attributes (below) a target value may be provided.

    Tracks with the attribute values nearest to the target values will be preferred.
    For example, you might request `target_energy=0.6` and
    `target_danceability=0.8`. All target values will be weighed equally in ranking
    results.
    """
