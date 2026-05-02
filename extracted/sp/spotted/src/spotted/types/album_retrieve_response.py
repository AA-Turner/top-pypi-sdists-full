# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.image_object import ImageObject
from .shared.copyright_object import CopyrightObject
from .shared.external_id_object import ExternalIDObject
from .shared.external_url_object import ExternalURLObject
from .shared.simplified_track_object import SimplifiedTrackObject
from .shared.album_restriction_object import AlbumRestrictionObject
from .shared.simplified_artist_object import SimplifiedArtistObject

__all__ = ["AlbumRetrieveResponse", "Tracks"]


class Tracks(BaseModel):
    """The tracks of the album."""

    href: str
    """A link to the Web API endpoint returning the full result of the request"""

    limit: int
    """
    The maximum number of items in the response (as set in the query or by default).
    """

    next: Optional[str] = None
    """URL to the next page of items. ( `null` if none)"""

    offset: int
    """The offset of the items returned (as set in the query or by default)"""

    previous: Optional[str] = None
    """URL to the previous page of items. ( `null` if none)"""

    total: int
    """The total number of items available to return."""

    items: Optional[List[SimplifiedTrackObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class AlbumRetrieveResponse(BaseModel):
    id: str
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    album.
    """

    album_type: Literal["album", "single", "compilation"]
    """The type of the album."""

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

    artists: Optional[List[SimplifiedArtistObject]] = None
    """The artists of the album.

    Each artist object includes a link in `href` to more detailed information about
    the artist.
    """

    copyrights: Optional[List[CopyrightObject]] = None
    """The copyright statements of the album."""

    external_ids: Optional[ExternalIDObject] = None
    """Known external IDs for the album."""

    genres: Optional[List[str]] = None
    """**Deprecated** The array is always empty."""

    label: Optional[str] = None
    """The label associated with the album."""

    popularity: Optional[int] = None
    """The popularity of the album.

    The value will be between 0 and 100, with 100 being the most popular.
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

    tracks: Optional[Tracks] = None
    """The tracks of the album."""
