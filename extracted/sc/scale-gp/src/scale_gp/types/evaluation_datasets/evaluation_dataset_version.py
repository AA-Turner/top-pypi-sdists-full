# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["EvaluationDatasetVersion"]


class EvaluationDatasetVersion(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    draft: bool
    """Boolean to check whether or not the evaluation dataset is in draft mode"""

    evaluation_dataset_id: str
    """The ID of the associated evaluation dataset."""

    num: int
    """The version number, automatically incremented on creation"""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    published_at: Optional[datetime] = None
    """
    The date and time that all test case results for the evaluation were completed
    for the evaluation in ISO format.
    """
