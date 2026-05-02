# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["LastKMemoryStrategyParams"]


class LastKMemoryStrategyParams(BaseModel):
    k: int
    """The maximum number of previous messages to remember."""
