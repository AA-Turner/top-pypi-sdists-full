# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .image_object import ImageObject
from .external_id_object import ExternalIDObject
from .external_url_object import ExternalURLObject
from .linked_track_object import LinkedTrackObject
from .album_restriction_object import AlbumRestrictionObject
from .simplified_artist_object import SimplifiedArtistObject
from .track_restriction_object import TrackRestrictionObject

__all__ = ["TrackObject", "Album"]


class Album(BaseModel):
    """The album on which the track appears.

    The album object includes a link in `href` to full information about the album.
    """

    id: str
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    album.
    """

    album_type: Literal["album", "single", "compilation"]
    """The type of the album."""

    artists: List[SimplifiedArtistObject]
    """The artists of the album.

    Each artist object includes a link in `href` to more detailed information about
    the artist.
    """

    available_markets: List[str]
    """
    The markets in which the album is available:
    [ISO 3166-1 alpha-2 country codes](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    _**NOTE**: an album is considered available in a market when at least 1 of its
    tracks is available in that market._
    """

    external_urls: ExternalURLObject
    """Known external URLs for this album."""

    href: str
    """A link to the Web API endpoint providing full details of the album."""

    images: List[ImageObject]
    """The cover art for the album in various sizes, widest first."""

    name: str
    """The name of the album.

    In case of an album takedown, the value may be an empty string.
    """

    release_date: str
    """The date the album was first released."""

    release_date_precision: Literal["year", "month", "day"]
    """The precision with which `release_date` value is known."""

    total_tracks: int
    """The number of tracks in the album."""

    type: Literal["album"]
    """The object type."""

    uri: str
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    album.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    restrictions: Optional[AlbumRestrictionObject] = None
    """Included in the response when a content restriction is applied."""


class TrackObject(BaseModel):
    id: Optional[str] = None
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    track.
    """

    album: Optional[Album] = None
    """The album on which the track appears.

    The album object includes a link in `href` to full information about the album.
    """

    artists: Optional[List[SimplifiedArtistObject]] = None
    """The artists who performed the track.

    Each artist object includes a link in `href` to more detailed information about
    the artist.
    """

    available_markets: Optional[List[str]] = None
    """
    A list of the countries in which the track can be played, identified by their
    [ISO 3166-1 alpha-2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code.
    """

    disc_number: Optional[int] = None
    """The disc number (usually `1` unless the album consists of more than one disc)."""

    duration_ms: Optional[int] = None
    """The track length in milliseconds."""

    explicit: Optional[bool] = None
    """
    Whether or not the track has explicit lyrics ( `true` = yes it does; `false` =
    no it does not OR unknown).
    """

    external_ids: Optional[ExternalIDObject] = None
    """Known external IDs for the track."""

    external_urls: Optional[ExternalURLObject] = None
    """Known external URLs for this track."""

    href: Optional[str] = None
    """A link to the Web API endpoint providing full details of the track."""

    is_local: Optional[bool] = None
    """Whether or not the track is from a local file."""

    is_playable: Optional[bool] = None
    """
    Part of the response when
    [Track Relinking](/documentation/web-api/concepts/track-relinking) is applied.
    If `true`, the track is playable in the given market. Otherwise `false`.
    """

    linked_from: Optional[LinkedTrackObject] = None
    """
    Part of the response when
    [Track Relinking](/documentation/web-api/concepts/track-relinking) is applied,
    and the requested track has been replaced with different track. The track in the
    `linked_from` object contains information about the originally requested track.
    """

    name: Optional[str] = None
    """The name of the track."""

    popularity: Optional[int] = None
    """The popularity of the track.

    The value will be between 0 and 100, with 100 being the most popular.<br/>The
    popularity of a track is a value between 0 and 100, with 100 being the most
    popular. The popularity is calculated by algorithm and is based, in the most
    part, on the total number of plays the track has had and how recent those plays
    are.<br/>Generally speaking, songs that are being played a lot now will have a
    higher popularity than songs that were played a lot in the past. Duplicate
    tracks (e.g. the same track from a single and an album) are rated independently.
    Artist and album popularity is derived mathematically from track popularity.
    _**Note**: the popularity value may lag actual popularity by a few days: the
    value is not updated in real time._
    """

    preview_url: Optional[str] = None
    """A link to a 30 second preview (MP3 format) of the track. Can be `null`"""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    restrictions: Optional[TrackRestrictionObject] = None
    """Included in the response when a content restriction is applied."""

    track_number: Optional[int] = None
    """The number of the track.

    If an album has several discs, the track number is the number on the specified
    disc.
    """

    type: Optional[Literal["track"]] = None
    """The object type: "track"."""

    uri: Optional[str] = None
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    track.
    """
