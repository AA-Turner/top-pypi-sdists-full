# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TextContent"]


class TextContent(BaseModel):
    """Text content for documents."""

    text: str
    """Text content to be embedded"""

    type: Optional[Literal["text"]] = None
    """Content type identifier"""
