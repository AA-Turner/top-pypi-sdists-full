# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Experiment"]


class Experiment(BaseModel):
    id: str

    created_at: datetime

    metadata: Optional[object] = None

    name: str

    project_id: str

    tags: Optional[object] = None
    """Tags are key-value pairs used to label resources"""
