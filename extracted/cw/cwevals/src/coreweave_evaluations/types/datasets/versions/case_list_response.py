# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ...._models import BaseModel

__all__ = ["CaseListResponse", "Case"]


class Case(BaseModel):
    attributes: Dict[str, object]

    case_id: str

    commit_id: int

    example_key: Optional[str] = None

    input: object

    output: object

    variant: Optional[str] = None


class CaseListResponse(BaseModel):
    cases: List[Case]

    next_cursor: Optional[str] = None
