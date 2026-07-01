# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["EvaluationTasksProgressSchema", "Items", "ItemsFailedItem", "Workflows"]


class ItemsFailedItem(BaseModel):
    item_id: str

    error: Optional[str] = None

    error_type: Optional[str] = None


class Items(BaseModel):
    failed: int

    pending: int

    successful: int

    total: int

    failed_items: Optional[List[ItemsFailedItem]] = None


class Workflows(BaseModel):
    completed: int

    failed: int

    pending: int

    total: int


class EvaluationTasksProgressSchema(BaseModel):
    items: Optional[Items] = None

    workflows: Optional[Workflows] = None
