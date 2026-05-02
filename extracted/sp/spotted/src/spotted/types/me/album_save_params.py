# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from ..._types import SequenceNotStr

__all__ = ["AlbumSaveParams"]


class AlbumSaveParams(TypedDict, total=False):
    ids: SequenceNotStr[str]
    """
    A JSON array of the
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
    `["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]`<br/>A maximum of 50 items
    can be specified in one request. _**Note**: if the `ids` parameter is present in
    the query string, any IDs listed here in the body will be ignored._
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """
