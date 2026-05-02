# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["TrackRestrictionObject"]


class TrackRestrictionObject(BaseModel):
    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    reason: Optional[str] = None
    """The reason for the restriction. Supported values:

    - `market` - The content item is not available in the given market.
    - `product` - The content item is not available for the user's subscription
      type.
    - `explicit` - The content item is explicit and the user's account is set to not
      play explicit content.

    Additional reasons may be added in the future. **Note**: If you use this field,
    make sure that your application safely handles unknown values.
    """
