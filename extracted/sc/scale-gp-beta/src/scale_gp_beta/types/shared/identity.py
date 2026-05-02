# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["Identity"]


class Identity(BaseModel):
    id: str

    type: Literal["user", "service_account"]

    object: Optional[Literal["identity"]] = None
