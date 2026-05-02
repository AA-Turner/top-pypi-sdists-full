# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from ..shared.image_object import ImageObject
from ..shared.followers_object import FollowersObject
from ..shared.external_url_object import ExternalURLObject
from ..shared.playlist_user_object import PlaylistUserObject
from ..shared.playlist_track_object import PlaylistTrackObject

__all__ = ["PlaylistCreateResponse", "Items", "Owner", "Tracks"]


class Items(BaseModel):
    """The items of the playlist.

    _**Note**: This field is only available for playlists owned by the current user or playlists the user is a collaborator of._
    """

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

    items: Optional[List[PlaylistTrackObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Owner(PlaylistUserObject):
    """The user who owns the playlist"""

    display_name: Optional[str] = None
    """The name displayed on the user's profile. `null` if not available."""


class Tracks(BaseModel):
    """**Deprecated:** Use `items` instead. The tracks of the playlist."""

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

    items: Optional[List[PlaylistTrackObject]] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class PlaylistCreateResponse(BaseModel):
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

    followers: Optional[FollowersObject] = None
    """Information about the followers of the playlist."""

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

    items: Optional[Items] = None
    """The items of the playlist.

    _**Note**: This field is only available for playlists owned by the current user
    or playlists the user is a collaborator of._
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

    tracks: Optional[Tracks] = None
    """**Deprecated:** Use `items` instead. The tracks of the playlist."""

    type: Optional[str] = None
    """The object type: "playlist" """

    uri: Optional[str] = None
    """
    The [Spotify URI](/documentation/web-api/concepts/spotify-uris-ids) for the
    playlist.
    """
