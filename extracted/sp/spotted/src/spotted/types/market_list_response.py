# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["MarketListResponse"]


class MarketListResponse(BaseModel):
    markets: Optional[List[str]] = None
