# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .question import Question
from .shared.question_set_question_config import QuestionSetQuestionConfig

__all__ = ["QuestionSetWithQuestions"]


class QuestionSetWithQuestions(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    questions: List[Question]

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    instructions: Optional[str] = None
    """Instructions to answer questions"""

    question_id_to_config: Optional[Dict[str, QuestionSetQuestionConfig]] = None
    """
    Specifies additional configurations to use for specific questions in the context
    of the question set. For example,
    `{<question_a_id>: {required: true}, <question_b_id>: {required: true}}` sets
    two questions as required.
    """
