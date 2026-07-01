# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["EvaluationGroupRowIdentifier"]


class EvaluationGroupRowIdentifier(BaseModel):
    """Response model for evaluation group row identifier"""

    column_name: str
    """Name of the column used as row identifier"""

    evaluation_id: str
    """ID of the evaluation"""

    object: Optional[Literal["evaluation_group.row_identifier"]] = None
