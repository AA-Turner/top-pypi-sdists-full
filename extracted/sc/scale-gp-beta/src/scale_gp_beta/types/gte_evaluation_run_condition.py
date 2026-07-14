# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["GteEvaluationRunCondition"]


class GteEvaluationRunCondition(BaseModel):
    left: object

    right: object

    op: Optional[Literal["gte"]] = None
