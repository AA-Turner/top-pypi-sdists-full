# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ....._models import BaseModel

__all__ = ["CompareSearchResponse", "Row", "RowEvaluation", "RowEvaluationRow", "RowEvaluationRowScore"]


class RowEvaluationRowScore(BaseModel):
    id: str

    scorer_id: str

    scorer_version_id: str

    value: object


class RowEvaluationRow(BaseModel):
    """Absent when this version has no row with the example key."""

    attributes: Dict[str, object]

    case_id: str

    output: object

    scores: List[RowEvaluationRowScore]

    variant: Optional[str] = None


class RowEvaluation(BaseModel):
    evaluation_version_id: str

    row: Optional[RowEvaluationRow] = None
    """Absent when this version has no row with the example key."""


class Row(BaseModel):
    id: str
    """
    Identifies the matched row within this comparison: the hash of its example key
    in hex, a colon, and its occurrence within each version, counted from 0. A row
    written before the service hashed example keys has its Case ID, a colon, and its
    version's index in evaluations instead.
    """

    evaluations: List[RowEvaluation]
    """One entry per compared version, reference first."""

    input: object
    """The input of the first version with the row.

    Rows matched by a client example key can differ in input.
    """


class CompareSearchResponse(BaseModel):
    rows: List[Row]

    total_rows: int
    """Matched rows across every page."""

    next_cursor: Optional[str] = None
