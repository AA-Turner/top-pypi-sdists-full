# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["NumberQuestionConfiguration"]


class NumberQuestionConfiguration(BaseModel):
    max: Optional[float] = None
    """Maximum value for the number"""

    min: Optional[float] = None
    """Minimum value for the number"""
