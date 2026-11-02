# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the spotify platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult
from .._pagination import (
    AsyncPaginator,
    Paginator,
    apaginate,
    paginate,
)

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SpotifyAlbumInput(TypedDict, total=False):
    """Input for Spotify Album."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Spotify album ID (alternative to url)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Spotify album URL (e.g. https://open.spotify.com/album/0pgrg7phBbnwGJ2HBEl9EG)."""


class SpotifyArtistInput(TypedDict, total=False):
    """Input for Spotify Artist."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Spotify artist ID (alternative to url)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Spotify artist URL (e.g. https://open.spotify.com/artist/3DiDSECUqqY1AuBP8qtaIa)."""


class SpotifyPlayCountInput(TypedDict, total=False):
    """Input for Spotify Play Count."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Spotify track, album, or artist URL to fetch stream counts for (e.g. https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp)."""


class SpotifyPodcastInput(TypedDict, total=False):
    """Input for Spotify Podcast."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Spotify podcast show ID (alternative to url)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Spotify podcast show URL (e.g. https://open.spotify.com/show/3mliji9352UAk3XnWElnDV)."""


class SpotifyPodcastEpisodesInput(TypedDict, total=False):
    """Input for Spotify Podcast Episodes."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response for subsequent pages."""
    id: NotRequired[str]
    """Spotify podcast show ID (alternative to url)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Spotify podcast show URL (e.g. https://open.spotify.com/show/4rOoJ6Egrf8K2IrywzwOMk)."""


class SpotifySearchInput(TypedDict, total=False):
    """Input for Spotify Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search term (e.g. "my first million")."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class SpotifyTrackInput(TypedDict, total=False):
    """Input for Spotify Track."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    id: NotRequired[str]
    """Spotify track ID (alternative to url)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Spotify track URL (e.g. https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT)."""


class SpotifyAlbumData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    artist_name: str | None = Field(
        default=None, alias="artistName", description="Name of the primary artist."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="URL of the cover art image.")
    label: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    popularity: int
    release_date: str = Field(
        alias="releaseDate",
        description="Populated whenever the provider has data for the entity.",
    )
    tracks: list[SpotifyAlbumTrack] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    type_: str = Field(
        alias="type",
        description="Populated whenever the provider has data for the entity.",
    )
    uri: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Canonical Spotify web URL, tracking query parameters stripped.",
    )


class SpotifyAlbumTrack(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    artist_name: str | None = Field(
        default=None, alias="artistName", description="Name of the primary artist."
    )
    duration_ms: int = Field(alias="durationMs")
    name: str
    playcount: int
    track_number: int | None = Field(
        default=None,
        alias="trackNumber",
        description="Position of the track within the album.",
    )
    uri: str


class SpotifyArtistData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    albums: list[SpotifyArtistAlbum] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    bio: str | None = Field(default=None, description="Artist biography text.")
    followers: int | None = Field(
        default=None, description="Number of Spotify followers the artist has."
    )
    id: str | None = Field(default=None, description="Spotify artist ID.")
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str | None = Field(default=None, description="Artist display name.")
    popularity: int | None = Field(
        default=None, description="Spotify popularity score for the artist, 0 to 100."
    )
    top_tracks: list[SpotifyArtistTopTrack] = Field(
        alias="topTracks",
        description="Populated whenever the provider has data for the entity.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical Spotify web URL, tracking query parameters stripped.",
    )
    verified: bool | None = Field(
        default=None, description="Whether the artist profile is verified on Spotify."
    )


class SpotifyArtistAlbum(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="URL of the cover art image.")
    label: str | None = Field(
        default=None, description="Record label that released the album."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    track_count: int = Field(alias="trackCount")
    type_: str = Field(
        alias="type",
        description="Populated whenever the provider has data for the entity.",
    )
    uri: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Canonical Spotify web URL, tracking query parameters stripped.",
    )
    year: int = Field(
        description="Populated whenever the provider has data for the entity."
    )


class SpotifyArtistTopTrack(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    artist_name: str | None = Field(
        default=None, alias="artistName", description="Name of the primary artist."
    )
    duration_ms: int | None = Field(
        default=None,
        alias="durationMs",
        description="Length of the track in milliseconds.",
    )
    id: str
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str
    playcount: int
    popularity: int | None = Field(
        default=None, description="Spotify popularity score for the track, 0 to 100."
    )
    uri: str


class SpotifyPlayCountData(BaseModel):
    items: list[SpotifyPlayCountItem] = Field(
        description="Play-count records for the requested Spotify entity (one per track). Populated whenever the provider has data for the entity."
    )


class SpotifyPlayCountItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    album_name: str | None = Field(
        default=None,
        alias="albumName",
        description="Name of the album the track belongs to. Empty when the upstream omits it.",
    )
    artist_name: str | None = Field(
        default=None,
        alias="artistName",
        description="Name of the primary artist. Empty when the upstream omits it.",
    )
    duration_ms: int | None = Field(
        default=None, alias="durationMs", description="Track duration in milliseconds."
    )
    id: str = Field(
        description="The Spotify entity ID. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str = Field(
        description="The track (or entity) name. Populated whenever the provider has data for the entity."
    )
    play_count: int = Field(
        alias="playCount",
        description="Total number of streams/plays for the track. Populated whenever the provider has data for the entity.",
    )
    preview_url: str | None = Field(
        default=None,
        alias="previewUrl",
        description="URL of the 30-second audio preview.",
    )
    release_date: str | None = Field(
        default=None,
        alias="releaseDate",
        description="Release date as an ISO 8601 string.",
    )
    track_number: int | None = Field(
        default=None,
        alias="trackNumber",
        description="Position of the track within its album.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='The Spotify entity type (e.g. "track").',
    )
    url: str = Field(
        description="Canonical open.spotify.com URL for the entity, with tracking query params stripped. Populated whenever the provider has data for the entity."
    )


class SpotifyPodcastData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    average_rating: float = Field(alias="averageRating")
    description: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    publisher: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    total_ratings: int = Field(alias="totalRatings")
    uri: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Canonical Spotify web URL, tracking query parameters stripped.",
    )


class SpotifyPodcastEpisodesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    episodes: list[SpotifyPodcastEpisodesEpisode] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of episodes, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total_count: int = Field(alias="totalCount")


class SpotifyPodcastEpisodesEpisode(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    duration_ms: int = Field(alias="durationMs")
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    release_date: str = Field(
        alias="releaseDate",
        description="Populated whenever the provider has data for the entity.",
    )
    uri: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class SpotifySearchData(BaseModel):
    albums: list[SpotifySearchAlbum] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    artists: list[SpotifySearchArtist] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    podcasts: list[SpotifySearchPodcast] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    tracks: list[SpotifySearchTrack] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class SpotifySearchAlbum(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    artist_name: str | None = Field(
        default=None, alias="artistName", description="Name of the primary artist."
    )
    id: str
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str
    type_: str | None = Field(
        default=None,
        alias="type",
        description="Album type, for example ALBUM, SINGLE or COMPILATION.",
    )
    uri: str
    year: int


class SpotifySearchArtist(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    uri: str
    verified: bool


class SpotifySearchPodcast(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str
    publisher: str
    uri: str | None = Field(
        default=None, description="Spotify URI of the podcast show."
    )


class SpotifySearchTrack(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    album_name: str | None = Field(
        default=None,
        alias="albumName",
        description="Name of the album the track appears on.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    uri: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class SpotifyTrackData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    album_name: str | None = Field(
        default=None,
        alias="albumName",
        description="Name of the album the track appears on.",
    )
    artist_name: str | None = Field(
        default=None, alias="artistName", description="Name of the primary artist."
    )
    duration_ms: int = Field(
        alias="durationMs",
        description="Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="URL of the cover art image.")
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    playcount: int
    popularity: int
    release_date: str | None = Field(
        default=None,
        alias="releaseDate",
        description="Album release date as an ISO 8601 string.",
    )
    share_url: str = Field(
        alias="shareUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    track_number: int = Field(
        alias="trackNumber",
        description="Populated whenever the provider has data for the entity.",
    )
    uri: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class SpotifyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def album(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyAlbumInput],
    ) -> RunResult[SpotifyAlbumData]:
        """Spotify Album

        Fetch a Spotify album's tracklist, play counts, label, and release details
        by album URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.album(url="https://open.spotify.com/album/0pgrg7phBbnwGJ2HBEl9EG")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.album", dict(input), options
        )
        return RunResult[SpotifyAlbumData].model_validate(raw)

    def artist(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyArtistInput],
    ) -> RunResult[SpotifyArtistData]:
        """Spotify Artist

        Fetch a Spotify artist's discography (albums, singles, top tracks) and
        metadata by artist URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.artist(url="https://open.spotify.com/artist/3DiDSECUqqY1AuBP8qtaIa")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.artist", dict(input), options
        )
        return RunResult[SpotifyArtistData].model_validate(raw)

    def play_count(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPlayCountInput],
    ) -> RunResult[SpotifyPlayCountData]:
        """Spotify Play Count

        Fetch stream counts and stats for a Spotify track, album, or artist URL.

        Price: $0 per request plus $0.0033 per result (maximum $0.0033).

        Example:
            res = client.spotify.play_count(url="https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.play_count", dict(input), options
        )
        return RunResult[SpotifyPlayCountData].model_validate(raw)

    def podcast(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPodcastInput],
    ) -> RunResult[SpotifyPodcastData]:
        """Spotify Podcast

        Fetch a Spotify podcast show's name, publisher, description, rating, and
        topics by show URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.podcast(url="https://open.spotify.com/show/3mliji9352UAk3XnWElnDV")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.podcast", dict(input), options
        )
        return RunResult[SpotifyPodcastData].model_validate(raw)

    def podcast_episodes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPodcastEpisodesInput],
    ) -> RunResult[SpotifyPodcastEpisodesData]:
        """Spotify Podcast Episodes

        List a Spotify podcast show's episodes with titles, durations, descriptions,
        and release dates by show URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.podcast_episodes(url="https://open.spotify.com/show/4rOoJ6Egrf8K2IrywzwOMk")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.podcast_episodes", dict(input), options
        )
        return RunResult[SpotifyPodcastEpisodesData].model_validate(raw)

    def iter_podcast_episodes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPodcastEpisodesInput],
    ) -> Paginator[SpotifyPodcastEpisodesEpisode, SpotifyPodcastEpisodesData]:
        """Iterate Spotify Podcast Episodes results, following pagination cursors.

        Yields validated `SpotifyPodcastEpisodesEpisode` items from the `episodes` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "spotify.podcast_episodes",
            dict(input),
            "episodes",
            item_model=SpotifyPodcastEpisodesEpisode,
            data_model=SpotifyPodcastEpisodesData,
            bare=False,
            options=options,
        )

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifySearchInput],
    ) -> RunResult[SpotifySearchData]:
        """Spotify Search

        Search Spotify for matching tracks, albums, artists, podcasts, and playlists
        by keyword.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.search(query="my first million")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.search", dict(input), options
        )
        return RunResult[SpotifySearchData].model_validate(raw)

    def track(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyTrackInput],
    ) -> RunResult[SpotifyTrackData]:
        """Spotify Track

        Fetch a Spotify track's play count, popularity, duration, and album details
        by track URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.track(url="https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.track", dict(input), options
        )
        return RunResult[SpotifyTrackData].model_validate(raw)


class AsyncSpotifyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def album(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyAlbumInput],
    ) -> RunResult[SpotifyAlbumData]:
        """Spotify Album

        Fetch a Spotify album's tracklist, play counts, label, and release details
        by album URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.album(url="https://open.spotify.com/album/0pgrg7phBbnwGJ2HBEl9EG")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.album", dict(input), options
        )
        return RunResult[SpotifyAlbumData].model_validate(raw)

    async def artist(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyArtistInput],
    ) -> RunResult[SpotifyArtistData]:
        """Spotify Artist

        Fetch a Spotify artist's discography (albums, singles, top tracks) and
        metadata by artist URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.artist(url="https://open.spotify.com/artist/3DiDSECUqqY1AuBP8qtaIa")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.artist", dict(input), options
        )
        return RunResult[SpotifyArtistData].model_validate(raw)

    async def play_count(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPlayCountInput],
    ) -> RunResult[SpotifyPlayCountData]:
        """Spotify Play Count

        Fetch stream counts and stats for a Spotify track, album, or artist URL.

        Price: $0 per request plus $0.0033 per result (maximum $0.0033).

        Example:
            res = client.spotify.play_count(url="https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.play_count", dict(input), options
        )
        return RunResult[SpotifyPlayCountData].model_validate(raw)

    async def podcast(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPodcastInput],
    ) -> RunResult[SpotifyPodcastData]:
        """Spotify Podcast

        Fetch a Spotify podcast show's name, publisher, description, rating, and
        topics by show URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.podcast(url="https://open.spotify.com/show/3mliji9352UAk3XnWElnDV")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.podcast", dict(input), options
        )
        return RunResult[SpotifyPodcastData].model_validate(raw)

    async def podcast_episodes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPodcastEpisodesInput],
    ) -> RunResult[SpotifyPodcastEpisodesData]:
        """Spotify Podcast Episodes

        List a Spotify podcast show's episodes with titles, durations, descriptions,
        and release dates by show URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.podcast_episodes(url="https://open.spotify.com/show/4rOoJ6Egrf8K2IrywzwOMk")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.podcast_episodes", dict(input), options
        )
        return RunResult[SpotifyPodcastEpisodesData].model_validate(raw)

    def iter_podcast_episodes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyPodcastEpisodesInput],
    ) -> AsyncPaginator[SpotifyPodcastEpisodesEpisode, SpotifyPodcastEpisodesData]:
        """Iterate Spotify Podcast Episodes results, following pagination cursors.

        Yields validated `SpotifyPodcastEpisodesEpisode` items from the `episodes` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "spotify.podcast_episodes",
            dict(input),
            "episodes",
            item_model=SpotifyPodcastEpisodesEpisode,
            data_model=SpotifyPodcastEpisodesData,
            bare=False,
            options=options,
        )

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifySearchInput],
    ) -> RunResult[SpotifySearchData]:
        """Spotify Search

        Search Spotify for matching tracks, albums, artists, podcasts, and playlists
        by keyword.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.search(query="my first million")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.search", dict(input), options
        )
        return RunResult[SpotifySearchData].model_validate(raw)

    async def track(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SpotifyTrackInput],
    ) -> RunResult[SpotifyTrackData]:
        """Spotify Track

        Fetch a Spotify track's play count, popularity, duration, and album details
        by track URL or ID.

        Price: $0.0012 per request.

        Example:
            res = client.spotify.track(url="https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "spotify.track", dict(input), options
        )
        return RunResult[SpotifyTrackData].model_validate(raw)
