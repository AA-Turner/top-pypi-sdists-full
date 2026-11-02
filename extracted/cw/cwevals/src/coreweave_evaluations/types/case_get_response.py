# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CaseGetResponse"]


class CaseGetResponse(BaseModel):
    attributes: Dict[str, object]

    case_id: str

    commit_id: int

    example_key: Optional[str] = None

    input: object

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    output: object

    scope_ref: str

    variant: Optional[str] = None
