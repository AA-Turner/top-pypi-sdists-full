# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .span import Span
from .._models import BaseModel

__all__ = ["APIListSpan"]


class APIListSpan(BaseModel):
    items: List[Span]

    object: Optional[Literal["list"]] = None
