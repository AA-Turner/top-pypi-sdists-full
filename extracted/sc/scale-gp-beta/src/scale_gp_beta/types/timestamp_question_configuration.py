# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TimestampQuestionConfiguration"]


class TimestampQuestionConfiguration(BaseModel):
    multi: Optional[bool] = None
    """Whether to allow multiple timestamps"""
