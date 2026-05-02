# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["RerankingResponse"]


class RerankingResponse(BaseModel):
    chunk_scores: List[float]

    tokens_used: Optional[int] = None
