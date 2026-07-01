# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["AutoEvaluationParameters"]


class AutoEvaluationParameters(BaseModel):
    batch_size: Optional[int] = None

    temperature: Optional[float] = None
