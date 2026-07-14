# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["InEvaluationRunCondition"]


class InEvaluationRunCondition(BaseModel):
    left: object

    operands: List[object]

    op: Optional[Literal["in"]] = None
