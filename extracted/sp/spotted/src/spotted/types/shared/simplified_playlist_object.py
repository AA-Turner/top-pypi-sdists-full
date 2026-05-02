# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .image_object import ImageObject
from .external_url_object import ExternalURLObject
from .playlist_user_object import PlaylistUserObject
from .playlist_tracks_ref_object import PlaylistTracksRefObject

__all__ = ["SimplifiedPlaylistObject", "Owner"]


class Owner(PlaylistUserObject):
    """The user who owns the playlist"""

    display_name: Optional[str] = None
    """The name displayed on the user's profile. `null` if not available."""


class SimplifiedPlaylistObject(BaseModel):
    id: Optional[str] = None
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    playlist.
    """

    collaborative: Optional[bool] = None
    """`true` if the owner allows other users to modify the playlist."""

    description: Optional[str] = None
    """The playlist description.

    _Only returned for modified, verified playlists, otherwise_ `null`.
    """

    external_urls: Optional[ExternalURLObject] = None
    """Known external URLs for this playlist."""

    href: Optional[str] = None
    """A link to the Web API endpoint providing full details of the playlist."""

    images: Optional[List[ImageObject]] = None
    """Images for the playlist.

    The array may be empty or contain up to three images. The images are returned by
    size in descending order. See
    [Working with Playlists](/documentation/web-api/concepts/playlists). _**Note**:
    If returned, the source URL for the image (`url`) is temporary and will expire
    in less than a day._
    """

    items: Optional[PlaylistTracksRefObject] = None
    """
    A collection containing a link ( `href` ) to the Web API endpoint where full
    details of the playlist's items can be retrieved, along with the `total` number
    of items in the playlist. Note, a track object may be `null`. This can happen if
    a track is no longer available.
    """

    name: Optional[str] = None
    """The name of the playlist."""

    owner: Optional[Owner] = None
    """The user who owns the playlist"""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    snapshot_id: Optional[str] = None
    """The version identifier for the current playlist.

    Can be supplied in other requests to target a specific playlist version
    """

    tracks: Optional[PlaylistTracksRefObject] = None
    """**Deprecated:** Use `items` instead.

    A collection containing a link ( `href` ) to the Web API endpoint where full
    details of the playlist's tracks can be retrieved, along with the `total` number
    of tracks in the playlist. Note, a track object may be `null`. This can happen
    if a track is no longer available.
    """

    type: Optional[str] = None
    """The object type: "playlist" """

    uri: Optional[str] = None
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    playlist.
    """
