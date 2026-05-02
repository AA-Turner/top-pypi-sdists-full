# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .evaluation_group_member import EvaluationGroupMember
from .evaluation_group_row_identifier import EvaluationGroupRowIdentifier

__all__ = ["EvaluationGroup"]


class EvaluationGroup(BaseModel):
    """Response model for evaluation group"""

    id: str
    """Unique identifier of the evaluation group"""

    account_id: str
    """Account that owns this evaluation group"""

    created_at: datetime
    """When the group was created"""

    name: str
    """Name of the evaluation group"""

    tags: List[str]
    """The tags associated with the entity"""

    deleted_at: Optional[datetime] = None
    """When the group was soft-deleted"""

    description: Optional[str] = None
    """Optional description"""

    members: Optional[List[EvaluationGroupMember]] = None
    """Evaluation members in this group. Populated with 'members' view."""

    metadata: Optional[Dict[str, object]] = None
    """Optional metadata key-value pairs"""

    object: Optional[Literal["evaluation_group"]] = None

    row_identifiers: Optional[List[EvaluationGroupRowIdentifier]] = None
    """Row identifier mappings. Populated with 'row_identifiers' view."""
