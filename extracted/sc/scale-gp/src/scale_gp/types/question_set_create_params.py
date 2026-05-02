# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr
from .shared_params.question_set_question_config import QuestionSetQuestionConfig

__all__ = ["QuestionSetCreateParams"]


class QuestionSetCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    name: Required[str]

    question_ids: Required[SequenceNotStr[str]]
    """IDs of questions in the question set"""

    instructions: str
    """Instructions to answer questions"""

    question_id_to_config: Dict[str, QuestionSetQuestionConfig]
    """
    Specifies additional configurations to use for specific questions in the context
    of the question set. For example,
    `{<question_a_id>: {required: true}, <question_b_id>: {required: true}}` sets
    two questions as required.
    """
