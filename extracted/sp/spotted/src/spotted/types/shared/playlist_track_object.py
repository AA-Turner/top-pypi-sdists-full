# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .track_object import TrackObject
from .episode_object import EpisodeObject
from .playlist_user_object import PlaylistUserObject

__all__ = ["PlaylistTrackObject", "Item", "Track"]

Item: TypeAlias = Annotated[Union[TrackObject, EpisodeObject], PropertyInfo(discriminator="type")]

Track: TypeAlias = Annotated[Union[TrackObject, EpisodeObject], PropertyInfo(discriminator="type")]


class PlaylistTrackObject(BaseModel):
    added_at: Optional[datetime] = None
    """The date and time the track or episode was added.

    _**Note**: some very old playlists may return `null` in this field._
    """

    added_by: Optional[PlaylistUserObject] = None
    """The Spotify user who added the track or episode.

    _**Note**: some very old playlists may return `null` in this field._
    """

    is_local: Optional[bool] = None
    """
    Whether this track or episode is a
    [local file](/documentation/web-api/concepts/playlists/#local-files) or not.
    """

    item: Optional[Item] = None
    """Information about the track or episode."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    track: Optional[Track] = None
    """**Deprecated:** Use `item` instead. Information about the track or episode."""
