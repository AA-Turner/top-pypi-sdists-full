# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["MetricListResponse", "Metric"]


class Metric(BaseModel):
    commit_id: int

    name: str

    subject: Optional[str] = None

    value: object

    value_type: Literal["boolean", "number", "string", "json"]


class MetricListResponse(BaseModel):
    metrics: List[Metric]
    """Newest value per subject and name, ordered by subject and then name.

    Values without a subject come first.
    """

    published_commit_id: int
    """Publication cutoff used to select the returned metric values."""
