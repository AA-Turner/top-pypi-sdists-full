# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .shared.identity import Identity
from .rubrics.rubric_criteria_response import RubricCriteriaResponse
from .rubrics.rubric_criteria_summary_response import RubricCriteriaSummaryResponse

__all__ = ["RubricResponse", "Criterion"]

Criterion: TypeAlias = Union[RubricCriteriaResponse, RubricCriteriaSummaryResponse]


class RubricResponse(BaseModel):
    id: str

    created_at: datetime

    created_by: Identity
    """The identity that created the entity."""

    tags: List[str]
    """The tags associated with the entity"""

    title: str

    version: int

    archived_at: Optional[datetime] = None

    criteria: Optional[List[Criterion]] = None
    """Full criteria on get, summary (title + weight) on list"""

    object: Optional[Literal["rubric"]] = None

    updated_at: Optional[datetime] = None
