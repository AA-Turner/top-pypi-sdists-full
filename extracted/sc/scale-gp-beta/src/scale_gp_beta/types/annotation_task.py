# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AnnotationTask"]


class AnnotationTask(BaseModel):
    id: str

    evaluation_id: str

    evaluation_item_id: str

    priority: int

    queue_id: str

    status: Literal["NOT_READY", "PENDING", "PENDING_REDO", "COMPLETED", "FIXED"]

    task_type: Literal["EVALUATION_ANNOTATION", "EVALUATION_AUDIT", "CONTRIBUTOR_ANNOTATION", "CONTRIBUTOR_AUDIT"]

    updated_at: datetime

    assigned_to: Optional[str] = None

    assignment_expires_at: Optional[datetime] = None

    duration_seconds: Optional[int] = None

    flagged_for_review: Optional[bool] = None

    object: Optional[Literal["annotation_task"]] = None

    review_comment: Optional[str] = None
