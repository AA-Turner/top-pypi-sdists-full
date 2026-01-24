# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .evaluator_criteria import EvaluatorCriteria

__all__ = ["EvaluatorCriterionCreateResponse"]


class EvaluatorCriterionCreateResponse(BaseModel):
    evaluator_criteria: Optional[EvaluatorCriteria] = None
