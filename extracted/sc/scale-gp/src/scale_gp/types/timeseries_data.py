# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["TimeseriesData", "Value"]


class Value(BaseModel):
    label: str

    value: List[float]


class TimeseriesData(BaseModel):
    bins: List[datetime]

    values: List[Value]

    unit: Optional[str] = None
