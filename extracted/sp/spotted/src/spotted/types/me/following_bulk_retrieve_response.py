# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from ..shared.artist_object import ArtistObject

__all__ = ["FollowingBulkRetrieveResponse", "Artists", "ArtistsCursors"]


class ArtistsCursors(BaseModel):
    """The cursors used to find the next set of items."""

    after: Optional[str] = None
    """The cursor to use as key to find the next page of items."""

    before: Optional[str] = None
    """The cursor to use as key to find the previous page of items."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """


class Artists(BaseModel):
    cursors: Optional[ArtistsCursors] = None
    """The cursors used to find the next set of items."""

    href: Optional[str] = None
    """A link to the Web API endpoint returning the full result of the request."""

    items: Optional[List[ArtistObject]] = None

    limit: Optional[int] = None
    """
    The maximum number of items in the response (as set in the query or by default).
    """

    next: Optional[str] = None
    """URL to the next page of items. ( `null` if none)"""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    total: Optional[int] = None
    """The total number of items available to return."""


class FollowingBulkRetrieveResponse(BaseModel):
    artists: Artists
