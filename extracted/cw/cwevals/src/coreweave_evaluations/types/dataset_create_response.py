# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DatasetCreateResponse"]


class DatasetCreateResponse(BaseModel):
    attributes: Dict[str, object]

    created_at: datetime

    dataset_id: str

    head_version_id: str
    """ID of the current pending dataset version.

    Publishing this version freezes its contents and opens a new pending version.
    """

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str
