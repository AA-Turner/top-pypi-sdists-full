# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .shared.artist_object import ArtistObject

__all__ = ["ArtistBulkRetrieveResponse"]


class ArtistBulkRetrieveResponse(BaseModel):
    artists: List[ArtistObject]
