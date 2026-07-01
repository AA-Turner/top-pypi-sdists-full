# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CustomChunkingStrategyConfig"]


class CustomChunkingStrategyConfig(BaseModel):
    endpoint: str
    """Endpoint path to call for custom chunking"""

    strategy: Literal["custom"]

    params: Optional[Dict[str, object]] = None
    """Parameters that will be appended to the body of the request for the chunk."""
