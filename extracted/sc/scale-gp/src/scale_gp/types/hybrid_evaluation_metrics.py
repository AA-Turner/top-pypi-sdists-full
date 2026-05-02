# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = ["HybridEvaluationMetrics", "AllQuestionInfo"]


class AllQuestionInfo(BaseModel):
    agreement_rate: float

    evaluation_question: str

    is_conditional_question: bool

    num_correct: int

    num_free_text: int

    num_inconclusive: int

    num_wrong: int

    question_title: str

    question_type: str

    total_time: float

    total_tokens: float

    choices: Optional[List[object]] = None


class HybridEvaluationMetrics(BaseModel):
    all_question_info: Dict[str, AllQuestionInfo]
    """Information about all questions."""
