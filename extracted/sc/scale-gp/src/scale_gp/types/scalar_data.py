# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ScalarData"]


class ScalarData(BaseModel):
    value: float

    unit: Optional[str] = None
