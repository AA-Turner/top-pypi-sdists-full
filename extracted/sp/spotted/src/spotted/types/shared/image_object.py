# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ImageObject"]


class ImageObject(BaseModel):
    height: Optional[int] = None
    """The image height in pixels."""

    url: str
    """The source URL of the image."""

    width: Optional[int] = None
    """The image width in pixels."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """
