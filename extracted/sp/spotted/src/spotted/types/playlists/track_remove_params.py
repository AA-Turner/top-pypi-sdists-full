# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["TrackRemoveParams", "Track"]


class TrackRemoveParams(TypedDict, total=False):
    tracks: Required[Iterable[Track]]
    """
    An array of objects containing
    [Spotify URIs](/documentation/web-api/concepts/spotify-uris-ids) of the tracks
    or episodes to remove. For example:
    `{ "tracks": [{ "uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh" },{ "uri": "spotify:track:1301WleyT98MSxVHPZCA6M" }] }`.
    A maximum of 100 objects can be sent at once.
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    snapshot_id: str
    """
    The playlist's snapshot ID against which you want to make the changes. The API
    will validate that the specified items exist and in the specified positions and
    make the changes, even if more recent changes have been made to the playlist.
    """


class Track(TypedDict, total=False):
    uri: str
    """Spotify URI"""
