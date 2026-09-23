# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["GroupRenameResponse", "Data"]


class Data(BaseModel):
    from_number: Optional[str] = None
    """Sendblue line that performed the change"""

    group_id: str

    group_name: str
    """Device-verified name; empty when cleared"""


class GroupRenameResponse(BaseModel):
    data: Data

    status: Literal["OK"]
