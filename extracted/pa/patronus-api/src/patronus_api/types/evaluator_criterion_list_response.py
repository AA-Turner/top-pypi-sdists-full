# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .evaluator_criteria import EvaluatorCriteria

__all__ = ["EvaluatorCriterionListResponse"]


class EvaluatorCriterionListResponse(BaseModel):
    evaluator_criteria: List[EvaluatorCriteria]
