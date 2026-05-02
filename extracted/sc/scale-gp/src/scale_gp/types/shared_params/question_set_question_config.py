# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["QuestionSetQuestionConfig"]


class QuestionSetQuestionConfig(TypedDict, total=False):
    required: bool
    """Whether the question is required. False by default."""
