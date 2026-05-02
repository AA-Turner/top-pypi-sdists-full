# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["PlaylistTracksRefObject"]


class PlaylistTracksRefObject(BaseModel):
    href: Optional[str] = None
    """
    A link to the Web API endpoint where full details of the playlist's tracks can
    be retrieved.
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    total: Optional[int] = None
    """Number of tracks in the playlist."""
