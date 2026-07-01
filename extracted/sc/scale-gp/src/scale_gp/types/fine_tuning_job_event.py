# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["FineTuningJobEvent"]


class FineTuningJobEvent(BaseModel):
    level: str

    message: str

    timestamp: Optional[float] = None
