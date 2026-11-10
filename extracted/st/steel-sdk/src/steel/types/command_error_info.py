# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["CommandErrorInfo"]


class CommandErrorInfo(BaseModel):
    code: str
    """Error code, such as stale_ref or not_actionable."""

    message: str

    reason: Optional[str] = None
    """More detail, such as covered or detached."""
