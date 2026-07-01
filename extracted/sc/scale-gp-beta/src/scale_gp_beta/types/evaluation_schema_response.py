# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["EvaluationSchemaResponse", "Field"]


class Field(BaseModel):
    """Schema information for a single field in evaluation item data"""

    data_type: str
    """JSON type: 'string', 'number', 'boolean', 'object', 'array', or 'null'"""

    field_name: str
    """The flattened JSON key path (e.g., 'metadata.category')"""

    item_count: int
    """Number of evaluation items containing this field"""

    source: Literal["data", "task_result_cache"]
    """The source of the field: 'data' or 'task_result_cache'"""

    object: Optional[Literal["field_schema"]] = None


class EvaluationSchemaResponse(BaseModel):
    """Schema information for an evaluation's item data structure"""

    evaluation_id: str
    """The ID of the evaluation"""

    fields: List[Field]
    """List of all discovered fields, ordered alphabetically by field_name"""

    total_items: int
    """Total number of evaluation items"""

    is_sampled: Optional[bool] = None
    """Whether schema was computed from a sample of items (for large evaluations)"""

    object: Optional[Literal["evaluation_schema"]] = None

    sample_size: Optional[int] = None
    """Number of items sampled for schema inference, if applicable"""
