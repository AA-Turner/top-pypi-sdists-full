# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PlaylistCreateParams"]


class PlaylistCreateParams(TypedDict, total=False):
    name: Required[str]
    """The name for the new playlist, for example `"Your Coolest Playlist"`.

    This name does not need to be unique; a user may have several playlists with the
    same name.
    """

    collaborative: bool
    """Defaults to `false`.

    If `true` the playlist will be collaborative. _**Note**: to create a
    collaborative playlist you must also set `public` to `false`. To create
    collaborative playlists you must have granted `playlist-modify-private` and
    `playlist-modify-public`
    [scopes](/documentation/web-api/concepts/scopes/#list-of-scopes)._
    """

    description: str
    """
    value for playlist description as displayed in Spotify Clients and in the Web
    API.
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """
