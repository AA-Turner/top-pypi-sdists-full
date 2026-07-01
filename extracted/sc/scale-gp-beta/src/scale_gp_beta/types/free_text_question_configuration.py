# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["FreeTextQuestionConfiguration"]


class FreeTextQuestionConfiguration(BaseModel):
    max_length: Optional[int] = None
    """Maximum characters allowed"""

    min_length: Optional[int] = None
    """Minimum characters required"""
