# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .shared.show_base import ShowBase
from .shared.image_object import ImageObject
from .shared.track_object import TrackObject
from .shared.artist_object import ArtistObject
from .shared.audiobook_base import AudiobookBase
from .shared.external_url_object import ExternalURLObject
from .shared.paging_playlist_object import PagingPlaylistObject
from .shared.album_restriction_object import AlbumRestrictionObject
from .shared.simplified_artist_object import SimplifiedArtistObject
from .shared.simplified_episode_object import SimplifiedEpisodeObject

__all__ = ["SearchQueryResponse", "Albums", "AlbumsItem", "Artists", "Audiobooks", "Episodes", "Shows", "Tracks"]


class AlbumsItem(BaseModel):
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


class Albums(BaseModel):
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

    items: Optional[List[AlbumsItem]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Artists(BaseModel):
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

    items: Optional[List[ArtistObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Audiobooks(BaseModel):
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

    items: Optional[List[AudiobookBase]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Episodes(BaseModel):
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

    items: Optional[List[SimplifiedEpisodeObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Shows(BaseModel):
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

    items: Optional[List[ShowBase]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Tracks(BaseModel):
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

    items: Optional[List[TrackObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class SearchQueryResponse(BaseModel):
    albums: Optional[Albums] = None

    artists: Optional[Artists] = None

    audiobooks: Optional[Audiobooks] = None

    episodes: Optional[Episodes] = None

    playlists: Optional[PagingPlaylistObject] = None

    shows: Optional[Shows] = None

    tracks: Optional[Tracks] = None
