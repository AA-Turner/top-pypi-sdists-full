# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Dict, List

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SessionAgentTracesResponse"]


class SessionAgentTracesResponse(BaseModel):
    events: List[Dict[str, object]]

    has_more: bool = FieldInfo(alias="hasMore")

    total: float
