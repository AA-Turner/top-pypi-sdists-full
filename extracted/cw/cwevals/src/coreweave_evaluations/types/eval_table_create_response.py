# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["EvalTableCreateResponse"]


class EvalTableCreateResponse(BaseModel):
    attributes: Dict[str, object]

    dataset_id: str

    evaluation_id: str

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str
