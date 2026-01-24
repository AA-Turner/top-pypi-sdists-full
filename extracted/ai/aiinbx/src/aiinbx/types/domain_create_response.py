# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DomainCreateResponse", "Record"]


class Record(BaseModel):
    name: str

    type: Literal["TXT", "CNAME", "MX"]

    value: str

    priority: Optional[float] = None


class DomainCreateResponse(BaseModel):
    domain_id: str = FieldInfo(alias="domainId")

    records: List[Record]
