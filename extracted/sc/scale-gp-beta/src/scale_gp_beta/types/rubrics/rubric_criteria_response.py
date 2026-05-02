# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RubricCriteriaResponse"]


class RubricCriteriaResponse(BaseModel):
    id: str

    created_at: datetime

    rubric_id: str

    title: str

    version: int

    annotations: Optional[Dict[str, object]] = None

    object: Optional[Literal["rubric_criteria"]] = None

    weight: Optional[float] = None
