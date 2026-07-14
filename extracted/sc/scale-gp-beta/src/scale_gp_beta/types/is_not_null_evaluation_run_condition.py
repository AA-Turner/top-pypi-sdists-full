# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["IsNotNullEvaluationRunCondition"]


class IsNotNullEvaluationRunCondition(BaseModel):
    operands: List[object]

    op: Optional[Literal["is_not_null"]] = None
