# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ...._models import BaseModel

__all__ = ["CaseListResponse", "Case"]


class Case(BaseModel):
    attributes: Dict[str, object]

    case_id: str

    child_trajectory_ids: List[str]
    """
    Trajectories nested under this trajectory whose root is this case, in the order
    they were created. Empty when there are none.
    """

    commit_id: int

    example_key: Optional[str] = None

    input: object

    output: object

    variant: Optional[str] = None


class CaseListResponse(BaseModel):
    cases: List[Case]

    next_cursor: Optional[str] = None
