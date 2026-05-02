# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ExternalURLObject"]


class ExternalURLObject(BaseModel):
    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    spotify: Optional[str] = None
    """
    The [Spotify URL](/documentation/web-api/concepts/spotify-uris-ids) for the
    object.
    """
