# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AdmeDeleteDataResponse"]


class AdmeDeleteDataResponse(BaseModel):
    id: str
    """ID of the resource whose data was deleted"""

    data_deleted: Literal[True]

    data_deleted_at: datetime
    """When the data was deleted"""
