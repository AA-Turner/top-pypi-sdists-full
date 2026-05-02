# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .external_url_object import ExternalURLObject
from .linked_track_object import LinkedTrackObject
from .simplified_artist_object import SimplifiedArtistObject
from .track_restriction_object import TrackRestrictionObject

__all__ = ["SimplifiedTrackObject"]


class SimplifiedTrackObject(BaseModel):
    id: Optional[str] = None
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    track.
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

    external_urls: Optional[ExternalURLObject] = None
    """External URLs for this track."""

    href: Optional[str] = None
    """A link to the Web API endpoint providing full details of the track."""

    is_local: Optional[bool] = None
    """Whether or not the track is from a local file."""

    is_playable: Optional[bool] = None
    """
    Part of the response when
    [Track Relinking](/documentation/web-api/concepts/track-relinking/) is applied.
    If `true`, the track is playable in the given market. Otherwise `false`.
    """

    linked_from: Optional[LinkedTrackObject] = None
    """
    Part of the response when
    [Track Relinking](/documentation/web-api/concepts/track-relinking/) is applied
    and is only part of the response if the track linking, in fact, exists. The
    requested track has been replaced with a different track. The track in the
    `linked_from` object contains information about the originally requested track.
    """

    name: Optional[str] = None
    """The name of the track."""

    preview_url: Optional[str] = None
    """A URL to a 30 second preview (MP3 format) of the track."""

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

    type: Optional[str] = None
    """The object type: "track"."""

    uri: Optional[str] = None
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    track.
    """
