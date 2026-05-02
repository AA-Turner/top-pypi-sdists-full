# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .context_object import ContextObject
from ..shared.track_object import TrackObject
from ..shared.episode_object import EpisodeObject

__all__ = ["PlayerGetCurrentlyPlayingResponse", "Actions", "Item"]


class Actions(BaseModel):
    """
    Allows to update the user interface based on which playback actions are available within the current context.
    """

    interrupting_playback: Optional[bool] = None
    """Interrupting playback. Optional field."""

    pausing: Optional[bool] = None
    """Pausing. Optional field."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    resuming: Optional[bool] = None
    """Resuming. Optional field."""

    seeking: Optional[bool] = None
    """Seeking playback location. Optional field."""

    skipping_next: Optional[bool] = None
    """Skipping to the next context. Optional field."""

    skipping_prev: Optional[bool] = None
    """Skipping to the previous context. Optional field."""

    toggling_repeat_context: Optional[bool] = None
    """Toggling repeat context flag. Optional field."""

    toggling_repeat_track: Optional[bool] = None
    """Toggling repeat track flag. Optional field."""

    toggling_shuffle: Optional[bool] = None
    """Toggling shuffle flag. Optional field."""

    transferring_playback: Optional[bool] = None
    """Transfering playback between devices. Optional field."""


Item: TypeAlias = Annotated[Union[TrackObject, EpisodeObject], PropertyInfo(discriminator="type")]


class PlayerGetCurrentlyPlayingResponse(BaseModel):
    actions: Optional[Actions] = None
    """
    Allows to update the user interface based on which playback actions are
    available within the current context.
    """

    context: Optional[ContextObject] = None
    """A Context Object. Can be `null`."""

    currently_playing_type: Optional[str] = None
    """The object type of the currently playing item.

    Can be one of `track`, `episode`, `ad` or `unknown`.
    """

    is_playing: Optional[bool] = None
    """If something is currently playing, return `true`."""

    item: Optional[Item] = None
    """The currently playing track or episode. Can be `null`."""

    progress_ms: Optional[int] = None
    """Progress into the currently playing track or episode. Can be `null`."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    timestamp: Optional[int] = None
    """Unix Millisecond Timestamp when data was fetched"""
