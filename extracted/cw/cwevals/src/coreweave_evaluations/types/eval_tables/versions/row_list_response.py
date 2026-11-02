# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ...._models import BaseModel

__all__ = ["RowListResponse", "Row", "RowScore"]


class RowScore(BaseModel):
    id: str

    scorer_id: str

    scorer_version_id: str

    value: object


class Row(BaseModel):
    attributes: Dict[str, object]

    case_id: str

    example_key: Optional[str] = None

    input: object

    output: object

    scores: List[RowScore]

    variant: Optional[str] = None


class RowListResponse(BaseModel):
    rows: List[Row]

    next_cursor: Optional[str] = None
