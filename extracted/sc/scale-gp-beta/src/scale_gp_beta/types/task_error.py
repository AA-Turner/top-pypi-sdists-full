# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["TaskError"]


class TaskError(BaseModel):
    message: str
    """Error message"""

    type: str
    """Error type/category"""
