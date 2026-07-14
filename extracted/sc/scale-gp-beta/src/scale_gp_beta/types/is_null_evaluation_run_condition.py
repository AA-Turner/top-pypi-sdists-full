# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["IsNullEvaluationRunCondition"]


class IsNullEvaluationRunCondition(BaseModel):
    operands: List[object]

    op: Optional[Literal["is_null"]] = None
