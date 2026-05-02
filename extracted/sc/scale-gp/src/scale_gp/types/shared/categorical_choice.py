# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional

from ..._models import BaseModel

__all__ = ["CategoricalChoice"]


class CategoricalChoice(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None
