# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["QuestionSetQuestionConfig"]


class QuestionSetQuestionConfig(BaseModel):
    required: Optional[bool] = None
    """Whether the question is required. False by default."""
