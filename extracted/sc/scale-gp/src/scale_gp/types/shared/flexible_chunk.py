# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["FlexibleChunk"]


class FlexibleChunk(BaseModel):
    text: str

    metadata: Optional[Dict[str, object]] = None
