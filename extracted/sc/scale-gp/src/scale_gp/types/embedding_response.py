# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["EmbeddingResponse"]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[object]]

    tokens_used: Optional[int] = None
