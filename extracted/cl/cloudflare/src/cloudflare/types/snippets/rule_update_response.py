# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["RuleUpdateResponse"]


class RuleUpdateResponse(BaseModel):
    """Define a snippet rule."""

    id: str
    """Specify the unique ID of the rule."""

    expression: str
    """Define the expression that determines which traffic matches the rule."""

    last_updated: datetime
    """Specify the timestamp of when the rule was last modified."""

    snippet_name: str
    """Identify the snippet."""

    description: Optional[str] = None
    """Provide an informative description of the rule."""

    enabled: Optional[bool] = None
    """Indicate whether to execute the rule."""
