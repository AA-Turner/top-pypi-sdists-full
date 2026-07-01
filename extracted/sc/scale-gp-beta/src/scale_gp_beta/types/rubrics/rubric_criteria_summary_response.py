# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["RubricCriteriaSummaryResponse"]


class RubricCriteriaSummaryResponse(BaseModel):
    """Slim criteria projection for list endpoints (title + weight only)."""

    title: str

    weight: Optional[float] = None
