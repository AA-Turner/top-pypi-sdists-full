# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["TaggingInformationAll"]


class TaggingInformationAll(BaseModel):
    tags_to_apply: Optional[Dict[str, object]] = None

    type: Optional[Literal["all"]] = None
