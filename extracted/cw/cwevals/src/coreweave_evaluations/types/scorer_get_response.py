# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ScorerGetResponse"]


class ScorerGetResponse(BaseModel):
    created_at: datetime

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str

    scorer_id: str
