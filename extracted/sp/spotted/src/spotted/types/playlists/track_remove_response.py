# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["TrackRemoveResponse"]


class TrackRemoveResponse(BaseModel):
    snapshot_id: Optional[str] = None
