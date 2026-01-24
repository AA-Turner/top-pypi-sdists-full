# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["EvaluatorCriteria"]


class EvaluatorCriteria(BaseModel):
    config: Optional[object] = None

    created_at: datetime

    evaluator_family: Optional[str] = None

    is_patronus_managed: bool

    name: Optional[str] = None

    public_id: str

    revision: int

    description: Optional[str] = None
