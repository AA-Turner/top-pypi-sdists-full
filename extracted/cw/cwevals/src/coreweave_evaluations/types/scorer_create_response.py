# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ScorerCreateResponse"]


class ScorerCreateResponse(BaseModel):
    allowed_target_kinds: List[Literal["case", "comparison", "trajectory"]]

    description: Optional[str] = None

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str

    scorer_id: str

    value_type: Literal["null", "boolean", "integer", "number", "string", "json"]

    version_id: str
