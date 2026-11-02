# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ComparisonGetResponse", "Member"]


class Member(BaseModel):
    case_id: str

    role: Optional[str] = None


class ComparisonGetResponse(BaseModel):
    attributes: Dict[str, object]

    commit_id: int

    comparison_id: str

    members: List[Member]

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str
