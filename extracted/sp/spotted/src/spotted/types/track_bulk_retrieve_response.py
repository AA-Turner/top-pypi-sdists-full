# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .shared.track_object import TrackObject

__all__ = ["TrackBulkRetrieveResponse"]


class TrackBulkRetrieveResponse(BaseModel):
    tracks: List[TrackObject]
