# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["ScorerAddResponse", "Scorer"]


class Scorer(BaseModel):
    scorer_id: str

    version_id: str


class ScorerAddResponse(BaseModel):
    scorers: List[Scorer]
    """The ScorerVersions the next EvaluationVersion selects, in order."""
