# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .dataset import Dataset
from .._models import BaseModel
from .shared.identity import Identity
from .evaluation_tasks_progress_schema import EvaluationTasksProgressSchema

__all__ = ["Evaluation"]


class Evaluation(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by: Identity
    """The identity that created the entity."""

    datasets: List[Dataset]

    name: str

    status: Literal["failed", "completed", "running"]

    tags: List[str]
    """The tags associated with the entity"""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    description: Optional[str] = None

    error_count: Optional[int] = None
    """Number of task errors across all items in this evaluation."""

    metadata: Optional[Dict[str, object]] = None
    """Metadata key-value pairs for the evaluation"""

    object: Optional[Literal["evaluation"]] = None

    progress: Optional[EvaluationTasksProgressSchema] = None
    """Progress of the evaluation's underlying async job"""

    status_reason: Optional[str] = None
    """Reason for evaluation status"""

    tasks: Optional[List["EvaluationTask"]] = None
    """Tasks executed during evaluation. Populated with optional `task` view."""


from .evaluation_task import EvaluationTask
