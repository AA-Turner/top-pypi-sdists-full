# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["NotInEvaluationRunCondition"]


class NotInEvaluationRunCondition(BaseModel):
    left: object

    operands: List[object]

    op: Optional[Literal["not_in"]] = None
