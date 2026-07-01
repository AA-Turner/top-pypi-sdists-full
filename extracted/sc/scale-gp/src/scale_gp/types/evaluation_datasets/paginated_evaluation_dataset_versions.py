# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .evaluation_dataset_version import EvaluationDatasetVersion

__all__ = ["PaginatedEvaluationDatasetVersions"]


class PaginatedEvaluationDatasetVersions(BaseModel):
    current_page: int
    """The current page number."""

    items: List[EvaluationDatasetVersion]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
