# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ExternalIDObject"]


class ExternalIDObject(BaseModel):
    ean: Optional[str] = None
    """
    [International Article Number](http://en.wikipedia.org/wiki/International_Article_Number_%28EAN%29)
    """

    isrc: Optional[str] = None
    """
    [International Standard Recording Code](http://en.wikipedia.org/wiki/International_Standard_Recording_Code)
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    upc: Optional[str] = None
    """[Universal Product Code](http://en.wikipedia.org/wiki/Universal_Product_Code)"""
