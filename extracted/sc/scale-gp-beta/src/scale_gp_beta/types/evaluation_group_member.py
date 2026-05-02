# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["EvaluationGroupMember"]


class EvaluationGroupMember(BaseModel):
    """Response model for evaluation group member"""

    id: str
    """Unique identifier of the member record"""

    created_at: datetime
    """When this member was added to the group"""

    evaluation_group_id: str
    """ID of the evaluation group"""

    evaluation_id: str
    """ID of the evaluation"""

    deleted_at: Optional[datetime] = None
    """When this membership was soft-deleted (if applicable)"""

    evaluation_created_at: Optional[datetime] = None
    """When the evaluation was created"""

    evaluation_name: Optional[str] = None
    """Name of the evaluation"""

    evaluation_tags: Optional[List[str]] = None
    """Tags of the evaluation"""

    object: Optional[Literal["evaluation_group.member"]] = None
