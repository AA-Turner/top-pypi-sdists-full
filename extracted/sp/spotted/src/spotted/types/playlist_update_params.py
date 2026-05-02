# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PlaylistUpdateParams"]


class PlaylistUpdateParams(TypedDict, total=False):
    collaborative: bool
    """
    If `true`, the playlist will become collaborative and other users will be able
    to modify the playlist in their Spotify client. <br/> _**Note**: You can only
    set `collaborative` to `true` on non-public playlists._
    """

    description: str
    """
    Value for playlist description as displayed in Spotify Clients and in the Web
    API.
    """

    name: str
    """The new name for the playlist, for example `"My New Playlist Title"`"""

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """
