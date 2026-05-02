# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .shared.paging_playlist_object import PagingPlaylistObject

__all__ = ["BrowseGetFeaturedPlaylistsResponse"]


class BrowseGetFeaturedPlaylistsResponse(BaseModel):
    message: Optional[str] = None
    """The localized message of a playlist."""

    playlists: Optional[PagingPlaylistObject] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """
