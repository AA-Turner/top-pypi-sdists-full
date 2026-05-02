# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .evaluation_schema_response import EvaluationSchemaResponse

__all__ = ["EvaluationGroupRetrieveSchemaResponse"]


class EvaluationGroupRetrieveSchemaResponse(BaseModel):
    """Per-evaluation schemas for all members of an evaluation group"""

    evaluation_group_id: str
    """The ID of the evaluation group"""

    evaluation_schemas: List[EvaluationSchemaResponse]
    """Schema for each member evaluation in the group, one entry per active evaluation"""

    object: Optional[Literal["evaluation_group_schema"]] = None
