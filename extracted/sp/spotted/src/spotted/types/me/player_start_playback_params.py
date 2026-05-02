# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from ..._types import SequenceNotStr

__all__ = ["PlayerStartPlaybackParams"]


class PlayerStartPlaybackParams(TypedDict, total=False):
    device_id: str
    """The id of the device this command is targeting.

    If not supplied, the user's currently active device is the target.
    """

    context_uri: str
    """Optional.

    Spotify URI of the context to play. Valid contexts are albums, artists &
    playlists. `{context_uri:"spotify:album:1Je1IMUlBXcx1Fz0WE7oPT"}`
    """

    offset: Dict[str, object]
    """Optional.

    Indicates from where in the context playback should start. Only available when
    context_uri corresponds to an album or playlist object "position" is zero based
    and can’t be negative. Example: `"offset": {"position": 5}` "uri" is a string
    representing the uri of the item to start at. Example:
    `"offset": {"uri": "spotify:track:1301WleyT98MSxVHPZCA6M"}`
    """

    position_ms: int
    """Indicates from what position to start playback.

    Must be a positive number. Passing in a position that is greater than the length
    of the track will cause the player to start playing the next song.
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    uris: SequenceNotStr[str]
    """Optional.

    A JSON array of the Spotify track URIs to play. For example:
    `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh", "spotify:track:1301WleyT98MSxVHPZCA6M"]}`
    """
