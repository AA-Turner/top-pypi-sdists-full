# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import TYPE_CHECKING, Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .approval_status import ApprovalStatus
from .assessment_type import AssessmentType

__all__ = ["SpanAssessment"]


class SpanAssessment(BaseModel):
    """Response model for span assessment"""

    assessment_id: str
    """Unique identifier for the assessment"""

    assessment_type: AssessmentType
    """Type of assessment"""

    created_by: str
    """User who submitted the assessment"""

    span_id: str
    """The span this assessment is attached to"""

    trace_id: str
    """The trace this assessment is attached to"""

    account_id: Optional[str] = None
    """Account this assessment belongs to"""

    approval: Optional[ApprovalStatus] = None
    """Approval status (approved/rejected)"""

    comment: Optional[str] = None
    """Raw text feedback"""

    created_at: Optional[datetime] = None
    """When this assessment was created"""

    metadata: Optional[Dict[str, object]] = None
    """Arbitrary JSON object for additional data"""

    object: Optional[Literal["span.assessment"]] = None

    overwrite: Optional[Dict[str, builtins.object]] = None
    """User corrections to span output"""

    rating: Optional[int] = None
    """Numerical rating (1-5)"""

    rubric: Optional[Dict[str, str]] = None
    """Rule key-value pairs for rubric evaluation"""

    updated_at: Optional[datetime] = None
    """When this assessment was last updated"""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, builtins.object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> builtins.object: ...
    else:
        __pydantic_extra__: Dict[str, builtins.object]
