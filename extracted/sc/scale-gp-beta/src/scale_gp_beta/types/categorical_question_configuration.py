# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["CategoricalQuestionConfiguration"]


class CategoricalQuestionConfiguration(BaseModel):
    choices: List[str]
    """Categorical answer choices (must contain at least one entry)"""

    dropdown: Optional[bool] = None
    """Whether the question is displayed as a dropdown in the UI."""

    multi: Optional[bool] = None
    """Whether the question allows multiple answers."""
