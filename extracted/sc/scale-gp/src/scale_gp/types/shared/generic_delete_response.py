# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["GenericDeleteResponse"]


class GenericDeleteResponse(BaseModel):
    count: int

    success: bool
