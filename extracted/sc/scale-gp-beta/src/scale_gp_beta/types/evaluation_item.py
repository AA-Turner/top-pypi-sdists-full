# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .task_error import TaskError
from .shared.identity import Identity

__all__ = ["EvaluationItem"]


class EvaluationItem(BaseModel):
    id: str

    created_at: datetime

    created_by: Identity
    """The identity that created the entity."""

    data: Dict[str, object]

    evaluation_id: str

    archived_at: Optional[datetime] = None

    dataset_item_id: Optional[str] = None

    dataset_item_version_num: Optional[int] = None

    files: Optional[Dict[str, str]] = None

    object: Optional[Literal["evaluation.item"]] = None

    task_errors: Optional[Dict[str, TaskError]] = None
    """Map of task alias to error info."""
