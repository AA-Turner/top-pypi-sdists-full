# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from ...shared.track_object import TrackObject
from ...shared.episode_object import EpisodeObject

__all__ = ["QueueGetResponse", "CurrentlyPlaying", "Queue"]

CurrentlyPlaying: TypeAlias = Annotated[Union[TrackObject, EpisodeObject], PropertyInfo(discriminator="type")]

Queue: TypeAlias = Annotated[Union[TrackObject, EpisodeObject], PropertyInfo(discriminator="type")]


class QueueGetResponse(BaseModel):
    currently_playing: Optional[CurrentlyPlaying] = None
    """The currently playing track or episode. Can be `null`."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    queue: Optional[List[Queue]] = None
    """The tracks or episodes in the queue. Can be empty."""
